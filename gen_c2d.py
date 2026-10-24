#!/usr/bin/env python3
"""Carbide Create (.c2d, build 853) files from the cut-sheet SVGs, with the toolpaths already set up.

The .c2d is SQLite: shapes and toolpaths live in `items` as zlib-compressed JSON. cnc/template.c2d is the user's own S1 file;
its stock, machine, tool (#11, 1/2 in) and feeds are kept, its shapes and toolpaths are replaced. Coordinates are mm with Y
up from the sheet's bottom-left corner. Break lines are left out (no cutoffs on this job).

    python3 gen_c2d.py            -> cnc/S1-....c2d ... cnc/S5-....c2d
"""
import json, math, re, shutil, sqlite3, uuid, zlib, copy
import xml.etree.ElementTree as ET
from design import HINGE_RECESS, WIN_POCKET, DADO

SHEET_IN = 48.0
MM = 25.4
H_MM = SHEET_IN * MM
NS = "{http://www.w3.org/2000/svg}"
from design import layout
SHEETS = [code + "-" + re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") for code, title, parts, note in layout()]
BREAK = 0.060 * MM          # breakthrough below the board: 0.060 in (the user's call, with an honest Z zero)
# One tool for the whole job: SpeTool 1/4 in downcut, 1 in cutting length, 1/4 in shank (the 1/2 in compression bit tripped
# the VFD on overcurrent). Downcut keeps the veneer clean; light passes keep the load low.
TOOL_D = 6.35; FEED = 2286.0; PLUNGE = 635.0; STEP = 3.175; STEPOVER = 2.54   # 1/4 in, 90 in/min, 25 in/min, 1/8 in deep, 40 %
RPM = 20000                 # spindle; slotting with the 1/2 in bit stalled at 12000 and at 17000, runs clean at 20000
TAB_WOOD = 3.2              # mm of plywood left in each tab, about 1/8 in
K = 0.5522847498            # quarter-circle Bezier handle length / radius

def new_uuid(): return "{" + str(uuid.uuid4()) + "}"
def to_cc(x, y): return [x * MM, H_MM - y * MM]          # SVG inches, Y down -> Carbide Create mm, Y up

# ---------- SVG path -> list of cubic segments (in SVG inches) ----------
def arc_to_cubics(x1, y1, rx, ry, phi, fa, fs, x2, y2):
    """SVG endpoint arc -> cubic Beziers (rx == ry here; phi ignored, always 0 in these sheets)."""
    r = rx
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    lam = (dx * dx + dy * dy) / (r * r)
    if lam > 1: r *= math.sqrt(lam)
    sign = -1 if fa == fs else 1
    sq = max(0.0, (r * r * r * r - r * r * dy * dy - r * r * dx * dx) / (r * r * dy * dy + r * r * dx * dx))
    coef = sign * math.sqrt(sq)
    cxp, cyp = coef * dy, -coef * dx
    cx, cy = cxp + (x1 + x2) / 2, cyp + (y1 + y2) / 2
    t1 = math.atan2(y1 - cy, x1 - cx); t2 = math.atan2(y2 - cy, x2 - cx)
    dt = t2 - t1
    if fs and dt < 0: dt += 2 * math.pi
    if not fs and dt > 0: dt -= 2 * math.pi
    n = max(1, int(math.ceil(abs(dt) / (math.pi / 2) - 1e-9)))
    segs = []; a = t1; step = dt / n
    for _ in range(n):
        b = a + step; k = 4 / 3 * math.tan((b - a) / 4) * r
        p0 = (cx + r * math.cos(a), cy + r * math.sin(a)); p3 = (cx + r * math.cos(b), cy + r * math.sin(b))
        c1 = (p0[0] - k * math.sin(a), p0[1] + k * math.cos(a)); c2 = (p3[0] + k * math.sin(b), p3[1] - k * math.cos(b))
        segs.append((c1, c2, p3)); a = b
    return segs

def parse_path(d):
    toks = re.findall(r"[MLHVAZ]|-?\d*\.?\d+(?:e-?\d+)?", d)
    i = 0; cur = None; start = None; segs = []
    def num():
        nonlocal i; v = float(toks[i]); i += 1; return v
    while i < len(toks):
        c = toks[i]; i += 1
        if c == "M": cur = (num(), num()); start = cur
        elif c in "LHV":
            p = (num(), num()) if c == "L" else ((num(), cur[1]) if c == "H" else (cur[0], num()))
            segs.append(((cur[0] + (p[0] - cur[0]) / 3, cur[1] + (p[1] - cur[1]) / 3), (cur[0] + 2 * (p[0] - cur[0]) / 3, cur[1] + 2 * (p[1] - cur[1]) / 3), p)); cur = p
        elif c == "A":
            rx, ry, phi, fa, fs, x, y = num(), num(), num(), num(), num(), num(), num()
            segs += arc_to_cubics(cur[0], cur[1], rx, ry, phi, int(fa), int(fs), x, y); cur = (x, y)
        elif c == "Z":
            if abs(cur[0] - start[0]) > 1e-9 or abs(cur[1] - start[1]) > 1e-9:
                p = start; segs.append(((cur[0] + (p[0] - cur[0]) / 3, cur[1] + (p[1] - cur[1]) / 3), (cur[0] + 2 * (p[0] - cur[0]) / 3, cur[1] + 2 * (p[1] - cur[1]) / 3), p)); cur = p
    return start, segs

def circle_path(cx, cy, r):
    start = (cx + r, cy); segs = []
    pts = [(cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r), (cx + r, cy)]
    for a, b in zip(pts, pts[1:]):
        ta = (-(a[1] - cy), a[0] - cx); tb = (-(b[1] - cy), b[0] - cx)          # tangent directions (y down, counter-clockwise on screen)
        c1 = (a[0] + K * ta[0], a[1] + K * ta[1]); c2 = (b[0] - K * tb[0], b[1] - K * tb[1])
        segs.append((c1, c2, b))
    return start, segs

def element(start, segs, tabs=None):
    """Carbide Create path element, the way build 853 writes an imported closed path."""
    p0 = to_cc(*start)
    points, cp1, cp2, ptype = [p0], [p0], [p0], [0]
    for c1, c2, p in segs:
        points.append(to_cc(*p)); cp1.append(to_cc(*c1)); cp2.append(to_cc(*c2)); ptype.append(3)
    term = [p0[0], H_MM - p0[1]]                     # build 853 ends each path with this marker (first point, Y not flipped)
    points.append(term); cp1.append(term); cp2.append(term); ptype.append(4)
    return {"behavior": 0, "cp1": cp1, "cp2": cp2, "geometryType": "path", "group_id": [], "id": new_uuid(),
            "layer": {"blue": 0, "green": 0, "locked": False, "name": "DEFAULT", "red": 0, "uuid": "", "visible": True},
            "point_type": ptype, "points": points, "position": [0, 0], "smooth": [1] * len(points), "tabs": tabs or []}

def tabs_for(start, segs, min_len=8.0, max_tabs=6):
    """Tabs at the middle of the long straight edges (inches); at least two on every part."""
    edges = []; cur = start
    for c1, c2, p in segs:
        straight = abs((c1[0] - cur[0]) * (p[1] - cur[1]) - (c1[1] - cur[1]) * (p[0] - cur[0])) < 1e-6
        L = math.hypot(p[0] - cur[0], p[1] - cur[1])
        if straight: edges.append((L, ((cur[0] + p[0]) / 2, (cur[1] + p[1]) / 2)))
        cur = p
    edges.sort(key=lambda e: -e[0])
    chosen = [e for e in edges if e[0] >= min_len][:max_tabs]
    if len(chosen) < 2: chosen = edges[:2]
    return [{"index": 0, "pos": to_cc(*m), "u": 0} for _, m in chosen]

# ---------- read one sheet ----------
def read_sheet(svg_path):
    root = ET.parse(svg_path).getroot(); layers = {}; labels = []
    for g in root.iter(NS + "g"):
        gid = g.attrib.get("id", "")
        shapes = []
        for e in g:
            tag = e.tag.replace(NS, "")
            if tag == "path": shapes.append(parse_path(e.attrib["d"]))
            elif tag == "circle": shapes.append(("circle", float(e.attrib["cx"]), float(e.attrib["cy"]), float(e.attrib["r"])))
            elif tag == "text" and gid.startswith("labels"):
                if "transform" in e.attrib: tx, ty = [float(v) for v in re.findall(r"-?\d*\.?\d+", e.attrib["transform"])[:2]]
                else: tx, ty = float(e.attrib["x"]), float(e.attrib["y"])
                labels.append((tx, ty, (e.text or "").split("  ")[0].strip()))
        layers[gid] = shapes
    return layers, labels

# ---------- build one .c2d ----------
def build(code, template="cnc/template.c2d"):
    out = f"cnc/{code}.c2d"
    shutil.copyfile(template, out)
    db = sqlite3.connect(out)
    rows = list(db.execute("select id, type, data from items"))
    stock = float(dict(db.execute("select key, value from params"))["thickness"])     # mm
    THROUGH = stock + BREAK                                                          # 18.415 + 1.524 = 19.939 mm, 0.785 in
    tp = {}; group_uuid = None
    for _id, typ, data in rows:
        if typ not in ("toolpath", "toolpath_group"): continue          # the model record is binary; it is kept as it is
        o = json.loads(zlib.decompress(data))
        if typ == "toolpath": tp.setdefault(o["type"], o)
        if typ == "toolpath_group": group_uuid = o["uuid"]
    db.execute("delete from items where type in ('element', 'toolpath')")
    db.execute("delete from sqlar where name in ('all.svg', 'preview.svg', 'gcode.egc')")   # caches of the old drawing; Carbide Create rebuilds them

    def put(kind, name, obj, typ):
        raw = (json.dumps(obj, indent=4) + "\n").encode()
        db.execute("insert into items (uuid, name, type, version, sz, data) values (?, ?, ?, 'J1', ?, ?)", (obj.get("id") or obj.get("uuid"), name, typ, len(raw), zlib.compress(raw, 1)))

    layers, labels = read_sheet(f"cut-sheets/{code}.svg")
    def lay(prefix): return next((v for k, v in layers.items() if k.startswith(prefix)), [])
    toolpaths = []
    def add_tp(kind, name, shapes, depth, stepdown, **extra):
        ids = []
        for s in shapes:
            if s[0] == "circle": st, sg = circle_path(s[1], s[2], s[3])
            else: st, sg = s
            el = element(st, sg, tabs_for(st, sg) if extra.get("tabs") else None)
            put("element", "path", el, "element"); ids.append({"uuid": el["id"]})
        if not ids: return
        t = copy.deepcopy(tp[kind]); t.update(name=name, elements=ids, end_depth=f"{depth:.3f}", stepdown=stepdown,
                                              uuid=new_uuid(), toolpath_group=group_uuid, enabled=True)
        t["speeds"] = {"feedrate": FEED, "plungerate": PLUNGE, "rpm": RPM}
        tool = t["tool"]; tool.update(diameter=TOOL_D, name="1/4 downcut", length=25.4, overall_length=63.5, plungerate=PLUNGE,
                                      slot_depth=STEP, slot_feedrate=FEED, slot_rpm=RPM, flutes=2, corner_radius=0, angle=0)
        if "stepover" in t: t["stepover"] = STEPOVER
        for k in ("ofset_dir", "climb", "ignore_tabs"):
            if k in extra: t[k] = extra[k]
        if extra.get("tabs"):
            # Tab height is measured up from the bottom of the cut, which is 0.1 in below the board: add the breakthrough,
            # or the tab is a paper-thin skin (3 mm of tab left 0.46 mm of wood on the first S1 run).
            t["tab_height"] = round(THROUGH - stock + TAB_WOOD, 3)
        toolpaths.append(t)

    rec = lay("recesses")
    add_tp("pocket_toolpath", "1 Dados and rabbets", lay("dados"), DADO * MM, STEP)
    add_tp("pocket_toolpath", "2 Hinge recesses", [s for s in rec if s[0] != "circle"], HINGE_RECESS * MM, 2.54)
    add_tp("pocket_toolpath", "3 Shaker panels, window pocket", lay("panel-and-window"), WIN_POCKET * MM, WIN_POCKET * MM / 2)
    add_tp("contour", "4 Holes, 1/2 in", lay("holes"), THROUGH, STEP, ofset_dir=-1, climb=False, ignore_tabs=True)   # the 1/4 in bit circles inside each 1/2 in hole
    add_tp("drilling_toolpath", "4b Pull dimples", [s for s in rec if s[0] == "circle"], HINGE_RECESS * MM, 6.35)
    add_tp("contour", "5 Inside profiles", lay("inside-profiles"), THROUGH, STEP, ofset_dir=-1, climb=False, ignore_tabs=True)   # -1 = Inside / Left, 1 = Outside / Right (checked in build 853)
    # One toolpath per part: the parts sit one bit apart, so their outside offsets touch, and inside a single toolpath
    # Carbide Create merges touching offsets into one outline round the whole group (seen in its simulation).
    def bbox(shape):
        st, sg = shape; xs = [st[0]] + [p[0] for _, _, p in sg]; ys = [st[1]] + [p[1] for _, _, p in sg]
        return min(xs) - 0.01, min(ys) - 0.01, max(xs), max(ys)
    outs = lay("outside-profiles"); boxes = [bbox(o) for o in outs]
    def owner(x, y):                       # the smallest part whose box holds the label (an upper divider sits in a side's notch)
        hits = [(b[2] - b[0]) * (b[3] - b[1]) for b in boxes]
        cands = [i for i, b in enumerate(boxes) if b[0] <= x <= b[2] and b[1] <= y <= b[3]]
        return min(cands, key=lambda i: hits[i]) if cands else None
    def name_of(shape):
        i = outs.index(shape); mine = [t for x, y, t in labels if owner(x, y) == i]
        return mine[0].title() if mine else "part"
    for k, s in enumerate(lay("outside-profiles"), 1):
        add_tp("contour", f"6.{k} Outside: {name_of(s)}", [s], THROUGH, STEP, ofset_dir=1, climb=False, ignore_tabs=False, tabs=True)
    for t in toolpaths: put("toolpath", t["type"], t, "toolpath")
    db.execute("update params set value = ? where key = 'num_toolpaths'", (str(len(toolpaths)),))
    db.commit(); db.close()
    return out, [(t["name"], len(t["elements"])) for t in toolpaths]

if __name__ == "__main__":
    for code in SHEETS:
        out, tps = build(code)
        print(out, "; ".join(f"{n} ({k})" for n, k in tps))
