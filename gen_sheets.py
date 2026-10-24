#!/usr/bin/env python3
"""Cut-sheet SVGs (1:1 inches) for the CNC, plus the HTML fragments the shop sheet needs.

Writes cut-sheets/S*.svg, and fragments/{sheets,parts,checklist}.html. design.py owns every number.
Layers: outside profiles (Cutout, through), inside profiles (Contour inside, through), 1/2 in holes (Contour inside with
the 1/4 in bit, through), dado pockets (Pocket, 1/4 in deep), break lines (Contour no offset, through, last).
"""
import os, re
from design import *

OUT = "cut-sheets"; FRAG = "fragments"
os.makedirs(OUT, exist_ok=True); os.makedirs(FRAG, exist_ok=True)

def f(x): return f"{x:.4f}".rstrip("0").rstrip(".")

def rrect_path(cx, cy, w, h, r):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    return (f"M{f(x0 + r)} {f(y0)}H{f(x1 - r)}A{f(r)} {f(r)} 0 0 1 {f(x1)} {f(y0 + r)}V{f(y1 - r)}A{f(r)} {f(r)} 0 0 1 {f(x1 - r)} {f(y1)}"
            f"H{f(x0 + r)}A{f(r)} {f(r)} 0 0 1 {f(x0)} {f(y1 - r)}V{f(y0 + r)}A{f(r)} {f(r)} 0 0 1 {f(x0 + r)} {f(y0)}Z")

def corner_path(x, y, w, h, rs):
    """Rectangle with per-corner radii [tl, tr, br, bl]; a 0 radius is a sharp corner."""
    tl, tr, br, bl = rs
    p = f"M{f(x + tl)} {f(y)}H{f(x + w - tr)}"
    if tr: p += f"A{f(tr)} {f(tr)} 0 0 1 {f(x + w)} {f(y + tr)}"
    p += f"V{f(y + h - br)}"
    if br: p += f"A{f(br)} {f(br)} 0 0 1 {f(x + w - br)} {f(y + h)}"
    p += f"H{f(x + bl)}"
    if bl: p += f"A{f(bl)} {f(bl)} 0 0 1 {f(x)} {f(y + h - bl)}"
    p += f"V{f(y + tl)}"
    if tl: p += f"A{f(tl)} {f(tl)} 0 0 1 {f(x + tl)} {f(y)}"
    return p + "Z"

def dado_path(x, y, w, h, open_edges):
    """Dado pocket outline. Closed ends are rounded with the bit radius; open ends run 1/8 in past the part edge so the
    pocket breaks out cleanly."""
    r = DADO_R; ext = 0.125
    x0, y0, x1, y1 = x, y, x + w, y + h
    if "l" in open_edges: x0 -= ext
    if "r" in open_edges: x1 -= -ext
    if "t" in open_edges: y0 -= ext
    if "b" in open_edges: y1 += ext
    horizontal = (x1 - x0) >= (y1 - y0)
    if horizontal:   # rounded ends on the closed left/right ends
        rl = 0 if "l" in open_edges else r; rr = 0 if "r" in open_edges else r
        return corner_path(x0, y0, x1 - x0, y1 - y0, [rl, rr, rr, rl])
    rt = 0 if "t" in open_edges else r; rb = 0 if "b" in open_edges else r
    return corner_path(x0, y0, x1 - x0, y1 - y0, [rt, rt, rb, rb])

def recess_path(x, y, w, h, open_edges):
    """Hinge recess: runs 1/8 in past its open edge so the two corners there are square; the closed corners keep the bit radius."""
    ext = 0.125
    if "l" in open_edges: x -= ext; w += ext
    if "r" in open_edges: w += ext
    if "t" in open_edges: y -= ext; h += ext
    if "b" in open_edges: h += ext
    sq = lambda a, b: 0 if (a in open_edges or b in open_edges) else DADO_R
    return corner_path(x, y, w, h, [sq("t", "l"), sq("t", "r"), sq("b", "r"), sq("b", "l")])

def notch_path(x, y, w, h, nw, nh, side="l"):
    """Rectangle with its top-left (or top-right) corner removed (the hutch sides): the L-shaped outside profile."""
    if side == "r": return f"M{f(x)} {f(y)}H{f(x + w - nw)}V{f(y + nh)}H{f(x + w)}V{f(y + h)}H{f(x)}Z"
    return f"M{f(x + nw)} {f(y)}H{f(x + w)}V{f(y + h)}H{f(x)}V{f(y + nh)}H{f(x + nw)}Z"

def fnotch_path(x, y, w, h, nx, nw, nd):
    """Rectangle with a notch cut in from its top edge (the front edge of a panel drawn y-from-the-front)."""
    return f"M{f(x)} {f(y)}H{f(x + nx)}V{f(y + nd)}H{f(x + nx + nw)}V{f(y)}H{f(x + w)}V{f(y + h)}H{f(x)}Z"

def check_inside(label, w, h, feat):
    """Every feature must land on its own part: a part turned on the sheet with features in the wrong frame fails here."""
    eps = 1e-6
    for cx, cy, cw, ch, oe in feat.get("dados", []):                # a dado may run past its own open edges, nowhere else
        if (cx < -eps and "l" not in oe) or (cy < -eps and "t" not in oe) or (cx + cw > w + eps and "r" not in oe) or (cy + ch > h + eps and "b" not in oe) \
                or cx > w or cy > h or cx + cw < 0 or cy + ch < 0:
            raise SystemExit(f"{label}: dado at ({cx:.3f}, {cy:.3f}) size {cw:.3f} x {ch:.3f} falls outside the {w:.3f} x {h:.3f} part")
    boxes = [(cx - cw / 2, cy - ch / 2, cw, ch) for cx, cy, cw, ch, *_ in feat.get("cutouts", []) + feat.get("pockets", [])]
    for rx, ry, rw, rh, oe in feat.get("recesses", []):              # a recess runs off its open edge, nowhere else
        if (rx < -eps and "l" not in oe) or (ry < -eps and "t" not in oe) or (rx + rw > w + eps and "r" not in oe) or (ry + rh > h + eps and "b" not in oe):
            raise SystemExit(f"{label}: recess at ({rx:.3f}, {ry:.3f}) falls outside the {w:.3f} x {h:.3f} part")
        if not oe or not ((rx < eps and "l" in oe) or (rx + rw > w - eps and "r" in oe) or (ry < eps and "t" in oe) or (ry + rh > h - eps and "b" in oe)):
            raise SystemExit(f"{label}: hinge recess at ({rx:.3f}, {ry:.3f}) does not open onto an edge")
    boxes += [(cx - d / 2, cy - d / 2, d, d) for cx, cy, d in feat.get("holes", []) + feat.get("marks", [])]
    for bx, by, bw, bh in boxes:
        if bx < -eps or by < -eps or bx + bw > w + eps or by + bh > h + eps:
            raise SystemExit(f"{label}: feature at ({bx:.3f}, {by:.3f}) size {bw:.3f} x {bh:.3f} falls outside the {w:.3f} x {h:.3f} part")

def part_geometry(label, w, h, x, y, kind):
    """Returns (profile_path, inside_paths, hole_elems, dado_paths, recess_paths, pocket_paths, mark_elems) in sheet coordinates."""
    feat = local_features(kind) if kind else dict(dados=[], holes=[], cutouts=[], corners=[0, 0, 0, 0])
    check_inside(label, w, h, feat)
    if feat.get("notch"): profile = notch_path(x, y, w, h, *feat["notch"], feat.get("notch_side", "l"))
    elif feat.get("fnotch"): profile = fnotch_path(x, y, w, h, *feat["fnotch"])
    else: profile = corner_path(x, y, w, h, feat["corners"])
    inside = [rrect_path(x + cx, y + cy, cw, ch, r) for cx, cy, cw, ch, r in feat["cutouts"]]
    holes = [f'<circle cx="{f(x + cx)}" cy="{f(y + cy)}" r="{f(d / 2)}"/>' for cx, cy, d in feat["holes"] if d <= BIT + 1e-9]
    inside += [rrect_path(x + cx, y + cy, d, d, d / 2) for cx, cy, d in feat["holes"] if d > BIT + 1e-9]   # bigger than the bit: contour inside
    dados = [dado_path(x + dx, y + dy, dw, dh, oe) for dx, dy, dw, dh, oe in feat["dados"]]
    recesses = [recess_path(x + rx, y + ry, rw, rh, oe) for rx, ry, rw, rh, oe in feat.get("recesses", [])]
    pockets = [rrect_path(x + cx, y + cy, pw, ph, pr) for cx, cy, pw, ph, pr, _ in feat.get("pockets", [])]
    marks = [f'<circle cx="{f(x + cx)}" cy="{f(y + cy)}" r="{f(d / 2)}"/>' for cx, cy, d in feat.get("marks", [])]
    return profile, inside, holes, dados, recesses, pockets, marks

FACE_DOWN = {"counter", "top"}
LEFT_UP = {"divA", "divB"}
RIGHT_UP = set()
INSIDE_UP = {"ovdoor"}
def face_label(kind, sep="  "):
    if kind in FACE_DOWN: return sep + "FACE DOWN"
    if kind in LEFT_UP: return sep + "LEFT FACE UP"
    if kind in RIGHT_UP: return sep + "RIGHT FACE UP"
    if kind in INSIDE_UP: return sep + "INSIDE FACE UP"
    return ""
sheets = layout()
slugs = {}
for code, title, parts, note in sheets:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    slugs[code] = f"{code}-{slug}.svg"
    g_out, g_in, g_hole, g_dado, g_rec, g_pock, g_lab = [], [], [], [], [], [], []
    for label, w, h, x, y, kind in parts:
        profile, inside, holes, dados, recesses, pockets, marks = part_geometry(label, w, h, x, y, kind)
        g_out.append(f'    <path d="{profile}"/>')
        g_in += [f'    <path d="{p}"/>' for p in inside]
        g_hole += ["    " + e for e in holes]
        g_dado += [f'    <path d="{p}"/>' for p in dados]
        g_rec += [f'    <path d="{p}"/>' for p in recesses] + ["    " + e for e in marks]
        g_pock += [f'    <path d="{p}"/>' for p in pockets]
        face = face_label(kind)
        ny = local_features(kind).get("notch")[1] if kind and local_features(kind).get("notch") else 0   # label below the notch on the sides
        if h > w and w < 6: g_lab.append(f'    <text transform="translate({f(x + 1.0)} {f(y + 0.5)}) rotate(90)">{label}  {frac(w)} × {frac(h)}{face}</text>')
        else: g_lab.append(f'    <text x="{f(x + 0.5)}" y="{f(y + ny + 1.1)}">{label}  {frac(w)} × {frac(h)}{face}</text>')
    xr, yb = break_lines(parts)
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<!-- {code} {title}. Units: inches, 1:1, sheet 48 x 48. Cut with a 1/4 in downcut bit (see gen_c2d.py). Parts sit {f(KERF)} in apart. -->',
        '<!-- Layers: outside profiles = Cutout, outside the line, through. inside profiles = Contour inside the line, through. -->',
        f'<!-- holes = {f(BIT)} in, Contour inside the line with the 1/4 in bit, through. dados = Pocket, {f(DADO)} in deep, inside the outline. -->',
        f'<!-- {f(HOLD)} in all round is never cut by a part: hold-down screws go there. Red break lines are on-path through cuts to the edge; cut them LAST with a screw in each leftover. -->',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{f(SHEET)}in" height="{f(SHEET)}in" viewBox="0 0 {f(SHEET)} {f(SHEET)}">',
        '  <g id="sheet-outline" fill="none" stroke="#999999" stroke-width="0.02">', f'    <rect x="0" y="0" width="{f(SHEET)}" height="{f(SHEET)}"/>', '  </g>',
        '  <g id="hold-down-zones-delete-before-cutting" fill="#dddddd" stroke="none">',
        f'    <path fill-rule="evenodd" d="M0 0H{f(SHEET)}V{f(SHEET)}H0Z M{f(HOLD)} {f(HOLD)}H{f(SHEET - HOLD)}V{f(SHEET - HOLD)}H{f(HOLD)}Z"/>', '  </g>',
    ]
    if g_dado: svg += [f'  <g id="dados-pocket-{f(DADO)}in-deep" fill="none" stroke="#0000ff" stroke-width="0.01">', *g_dado, '  </g>']
    if g_rec: svg += [f'  <g id="recesses-and-dimples-pocket-{f(HINGE_RECESS)}in-deep" fill="none" stroke="#00aaaa" stroke-width="0.01">', *g_rec, '  </g>']
    if g_pock: svg += [f'  <g id="panel-and-window-pockets-{f(WIN_POCKET)}in-deep" fill="none" stroke="#8800ff" stroke-width="0.01">', *g_pock, '  </g>']
    if g_hole: svg += [f'  <g id="holes-drill-{f(BIT)}in-through" fill="none" stroke="#ff00ff" stroke-width="0.01">', *g_hole, '  </g>']
    if g_in: svg += ['  <g id="inside-profiles-contour-inside-through" fill="none" stroke="#008800" stroke-width="0.01">', *g_in, '  </g>']
    svg += ['  <g id="outside-profiles-cutout-through" fill="none" stroke="#000000" stroke-width="0.01">', *g_out, '  </g>',
            '  <g id="break-lines-on-path-through-cut-last" fill="none" stroke="#ff0000" stroke-width="0.01">',
            f'    <line x1="{f(xr)}" y1="0" x2="{f(xr)}" y2="{f(SHEET)}"/>', f'    <line x1="0" y1="{f(yb)}" x2="{f(SHEET)}" y2="{f(yb)}"/>', '  </g>',
            '  <g id="labels-delete-before-cutting" fill="#888888" font-family="Helvetica, Arial, sans-serif" font-size="0.6">', *g_lab,
            f'    <text x="{f(SHEET / 2)}" y="{f(SHEET - HOLD / 2 + 0.2)}" text-anchor="middle">{frac(HOLD)} IN HOLD-DOWN BORDER ALL ROUND, SCREWS HERE, NO PARTS</text>', '  </g>', '</svg>', '']
    open(os.path.join(OUT, slugs[code]), "w").write("\n".join(svg))

# --- sheet diagrams for the HTML -------------------------------------------------------
blocks = []
for code, title, parts, note in sheets:
    xr, yb = break_lines(parts)
    body = [f'        <svg viewBox="-1 -1 50 50" role="img" aria-label="{code}: {title}">',
            '          <rect class="board" x="0" y="0" width="48" height="48"/>',
            f'          <path class="keep" fill-rule="evenodd" d="M0 0H48V48H0Z M{f(HOLD)} {f(HOLD)}H{f(SHEET - HOLD)}V{f(SHEET - HOLD)}H{f(HOLD)}Z"/>',
            f'          <line class="brk" x1="{f(xr)}" y1="0" x2="{f(xr)}" y2="48"/>', f'          <line class="brk" x1="0" y1="{f(yb)}" x2="48" y2="{f(yb)}"/>']
    for label, w, h, x, y, kind in parts:
        profile, inside, holes, dados, recesses, pockets, marks = part_geometry(label, w, h, x, y, kind)
        body.append(f'          <path class="ply" d="{profile}"/>')
        for p in dados: body.append(f'          <path class="groove" fill="none" d="{p}"/>')
        for p in recesses + pockets: body.append(f'          <path class="groove" fill="none" d="{p}"/>')
        for e in marks: body.append('          ' + e.replace('<circle', '<circle class="groove" fill="none"'))
        for p in inside: body.append(f'          <path class="hole" d="{p}"/>')
        for e in holes: body.append('          ' + e.replace('<circle', '<circle class="hole"'))
    for label, w, h, x, y, kind in parts:
        face = face_label(kind, " · ")
        tall = h > w
        if tall and w < 9:
            if w < 4:
                body.append(f'          <text class="dim" transform="translate({f(x + w / 2 + 0.9)} {f(y + 1.0)}) rotate(90)">{label} {frac(w)} × {frac(h)}</text>')
            else:
                body.append(f'          <text transform="translate({f(x + 1.0 + 2.3)} {f(y + 1.0)}) rotate(90)">{label}</text>'
                            f'<text class="dim" transform="translate({f(x + 1.0 + 2.3 + 2.2)} {f(y + 1.0)}) rotate(90)">{frac(w)} × {frac(h)}</text>')
        else:
            ny = local_features(kind).get("notch")[1] if kind and local_features(kind).get("notch") else 0
            body.append(f'          <text x="{f(x + 1.0)}" y="{f(y + ny + 2.6)}">{label}{face}</text><text class="dim" x="{f(x + 1.0)}" y="{f(y + ny + 4.8)}">{frac(w)} × {frac(h)}</text>')
    body.append('        </svg>')
    blocks.append("\n".join(['      <div class="sheet">',
        f'        <div class="sheet-head"><h3>{code} <span>{title}</span></h3><a class="mono" href="cut-sheets/{slugs[code]}">{slugs[code]}</a></div>',
        *body, f'        <div class="note">{note} Break lines free a {frac(SHEET - xr - KERF / 2)} in wide strip on the right and a {frac(SHEET - yb - KERF / 2)} in strip below.</div>', '      </div>']))
open(os.path.join(FRAG, "sheets.html"), "w").write('    <div class="sheets">\n' + "\n\n".join(blocks) + '\n    </div>\n')

# --- parts table and checklist ---------------------------------------------------------
rows, check = [], []
work = {"SIDE": "dados · recesses", "BACK": "cord hole", "DIV": "recesses", "UDIV": "—",
        "OVEN": "—", "DRYSH": "—", "CTR": "cutout · port · dados · holes", "BOT": "dados · hole", "TANK": "dados", "TOP": "dados",
        "DOOR": "hole · panel", "DRYDOOR": "hole · panel", "OVDOOR": "window · pocket · dimples", "WARMDOOR": "hole · panel"}
for code, label, qty, L, Wd, notes, sheet in PARTS:
    rows.append(f'          <tr><td>{label}</td><td class="num">{qty}</td>'
                f'<td class="num">{frac(L)}<span class="dec">{dec(L)} · {mm(L)} mm</span></td>'
                f'<td class="num">{frac(Wd)}<span class="dec">{dec(Wd)} · {mm(Wd)} mm</span></td>'
                f'<td>{notes}</td><td><span class="sheet-tag">{sheet}</span></td></tr>')
    for i in range(qty):
        name = label if qty == 1 else f"{label} {'LR'[i] if qty == 2 else i + 1}"
        if code == "DIV": name = f"Divider {'AB'[i]}"
        if code == "BOT": wk = "dados · notch"
        if code == "UDIV": wk = "—"
        if code == "BACK": wk = "cord hole"
        wk = work[code]
        if code == "DIV": wk = "recesses" if i == 0 else "dado · recesses"
        if code == "SIDE": wk = "dados · 2 recesses · 2 peg holes" if i == 0 else "dados · 4 recesses"
        hbox = '<span class="cnt">—</span>' if wk == "—" else f'<span class="cb"></span><span class="cnt">{wk}</span>'
        check.append(f'        <tr><td class="box"><span class="cb"></span></td><td class="box">{hbox}</td>'
                     f'<td>{name}</td><td class="num">{frac(L)} <span class="dec-inline">{dec(L)} in · {mm(L)} mm</span></td>'
                     f'<td class="num">{frac(Wd)} <span class="dec-inline">{dec(Wd)} in · {mm(Wd)} mm</span></td><td><span class="sheet-tag">{sheet}</span></td></tr>')
total = sum(q for _, _, q, *_ in PARTS)
rows.append(f'          <tr class="total"><td>Whole kitchen</td><td class="num">{total}</td><td></td><td></td><td>{len(sheets)} sheets of 48 × 48</td><td></td></tr>')
open(os.path.join(FRAG, "parts.html"), "w").write("\n".join(rows) + "\n")
open(os.path.join(FRAG, "checklist.html"), "w").write("\n".join(check) + "\n")
print("wrote", len(sheets), "svgs,", total, "parts")
