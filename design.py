#!/usr/bin/env python3
"""Single source of numbers for the toddler play kitchen (hutch version, Oct 2026).

Every generator (params.scad, cut sheets, shop sheet) imports this module, so a change here ripples everywhere.
Units: inches. Coordinate frame of the model: X across the width (0 = left outside face), Y depth (0 = front face),
Z up from the floor.

Shape: a 45 7/8 x 18 x 45 in hutch. The base is 18 in deep to the counter at 23 in; above the counter the sides step
back to an 8 1/2 in deep upper cabinet, so the counter is reachable from the front and the faucet has 10 1/2 in of
headroom. Three bays: sink (23 in, two jugs and the pump below), drying (8 1/2 in, cupboard below), stove (11 1/2 in,
oven with a window and a warming drawer below). Four upper cupboards with doors. No open shelf anywhere.

Joinery: dados. Every horizontal panel sits in a 1/4 in deep dado in the sides (the top and bottom in rabbets); the
dividers sit in through dados in the bottom, counter, upper shelf and top; the two mid shelves in stopped dados (right
side, divider B). Parts that sit in dados are 2 x DADO longer than the opening they span. Pockets only cut into the up
face of a part, so each divider carries its pockets on ONE face (its left face).

Water: clean jug -> printed pickup foot with a float switch -> 1/2 in tube -> pump on the back panel -> faucet.
Sink -> basket strainer -> printed funnel in the dirty jug's neck. The dirty jug stands on the floor through a hole
in the bottom panel so the strainer clears it.
"""
import math

# --- stock and machine ------------------------------------------------------
T = 0.72             # 3/4 nominal oak ply, measured 0.715 to 0.725 in. Model and part sizes use the middle.
T_MAX = 0.725        # thickest reading: the dados are cut to fit this
SHEET = 48.0         # 4 x 4 half sheets (six on hand, five used)
BIT = 0.5            # 1/2 in: part spacing and hole size (nested for a 1/2 in bit; now cut with the 1/4 in downcut in gen_c2d.py)
KERF = BIT
HOLD = 1.0           # hold-down border, untouched all round (screws within it)
LEFT = HOLD + KERF   # parts start here so the outside profile pass ends exactly on the border
BRK = 1.5 * KERF     # break lines sit one clean channel past the parts
REVEAL = 3 / 32      # door gap all round
DADO = 0.25          # dado / rabbet depth
DADO_W = T_MAX + 0.01   # dado width: the thickest stock plus a hair so it goes together with glue in it
DADO_R = BIT / 2     # a stopped dado ends in a half-round of the bit; mating corners get this radius

# --- overall ----------------------------------------------------------------
D = 18.0             # outside depth of the base
UP_D = 8.5           # outside depth of the upper cabinet (from the back)
NOTCH_D = D - UP_D   # 9.5: how far the sides step back above the counter
H = 45.0             # side height, floor to the top. 45 is the longest part a 48 in sheet takes inside a 1 in border.
HC = 23.0            # counter height, top of the counter. The kid is 32 in at 1 1/2 and growing.
TOE = 0.0            # no toe kick: the bottom panel sits on the floor so the jugs fit under the sink
SINK_BAY = 23.0      # left bay: two 10 in jugs side by side with the pump on the back wall
DRY_BAY = 8.5        # middle bay: a bought rubber dish rack on the counter, a cupboard below
STOVE_BAY = 11.5     # right bay: four burners; oven with a stock 8 x 10 window and a warming drawer below
INNER_W = SINK_BAY + DRY_BAY + STOVE_BAY + 2 * T   # 44.44, the clear width between the sides
W = INNER_W + 2 * T  # 45.88 outside width
PANEL_L = INNER_W + 2 * DADO   # 44.94, length of every horizontal panel (it sits 1/4 in into each side)
CTR_D = D - T        # counter / bottom depth, 17.28 (the back panel takes the rest)
UP_SHELF_D = UP_D - T   # 7.78: upper shelf and top depth
BACK_H = H - T       # back panel sits on the bottom panel, runs to the top: 44.28
TANK_Z = 34.25       # top face of the upper shelf (floor of the upper cupboards)
HEADROOM = TANK_Z - T - HC   # 10.53 over the counter, under the upper shelf: the 9.3 in faucet fits
DIV_D = CTR_D        # dividers are full depth now that every bay has a door
DIV_H = HC - T - T + 2 * DADO   # 22.06: opening plus 1/4 into the bottom and 1/4 into the counter
UP_DIV_D = UP_SHELF_D
UP_DIV_H = H - T - TANK_Z + 2 * DADO  # 10.53
OVEN_Z = 9.75        # top face of the oven floor (the oven shelf): oven cavity above, warming drawer below
DRY_Z = 11.0         # top face of the drying cupboard's shelf
SHELF_D = CTR_D - 1.0   # mid shelves stop 1 in behind the front, in stopped dados
OVEN_L = STOVE_BAY + DADO   # 11.75: 1/4 into the right side, screwed to divider B's right face
DRY_L = DRY_BAY + DADO      # 8.75: 1/4 into divider B's left face, screwed to divider A's right face
HINGE_L, HINGE_LEAF_W = 2.6, 0.75    # Zorveiio 2 1/2 in butt hinge: 66 x 38 mm open, 1.4 mm leaves. MEASURE YOURS.
HINGE_RECESS = 0.055                 # 1.4 mm, one leaf deep: the cabinet leaf sits flush, the door leaf fits the 3/32 reveal
HINGE_IN = 2.0                       # hinge centres this far from each end of the door
KNOB_HOLE = BIT         # knob holes are bit-sized (1/2 in, circled by the 1/4 in bit); a printed bushing with a 3/16 bore presses in for the 8-32 screw
FRAME = 1.75            # Shaker frame width on the sink, drying and warming doors; the oven door stays flat like an appliance
DOOR_KNOB_IN = FRAME / 2   # knob centred on the stile, clear of the recessed panel
# doors: lower
DOOR_W = (SINK_BAY - 3 * REVEAL) / 2            # 11.36, two doors under the sink
DOOR_H = (HC - T) - T - 2 * REVEAL              # 21.37, floor-of-bay to counter underside
DRY_DOOR_W = DRY_BAY - 2 * REVEAL               # 8.31
OVEN_DOOR_W = STOVE_BAY - 2 * REVEAL            # 11.31
OVEN_DOOR_H = (HC - T) - OVEN_Z - 2 * REVEAL    # 12.34
WARM_DOOR_H = (OVEN_Z - T) - T - 2 * REVEAL     # 8.12, the warming drawer below the oven
# up top: four equal OPEN compartments at her eye level, no doors (Montessori: she sees her dishes and puts them back).
UP_BAY = (INNER_W - 3 * T) / 4                  # 10.57 clear width of each compartment
UDIV_X = [T + (i + 1) * UP_BAY + i * T for i in range(3)]   # kitchen x of each upper divider's left face
UP_OPEN_H = H - T - TANK_Z                      # 10.03 clear height
# fill port: a 1 1/2 in hole in the counter straight above the clean jug's neck; a printed funnel with a lid sits in it
PORT_D = 1.5
# peg hooks: two 1/2 in oak dowels through the left side's outer face, apron and towel, at her shoulder
PEG_Z = 27.0
PEG_Y = [11.0, 15.0]                            # from the front edge: on the upper portion of the side, which starts 9 1/2 in back
PEG_L = 3.0                                     # dowel length, 2 1/4 in proud
# oven window: a stock 8 x 10 x 1/8 acrylic sheet, uncut, sits in a pocket on the door's inside face
WIN_W, WIN_H, WIN_R = 8.5, 6.5, 0.5             # the opening
ACR_W, ACR_H, ACR_T = 10.0, 8.0, 0.125          # the acrylic as bought, 3/4 in lip all round
ACR_SLACK = 0.2                                 # the pocket is this much bigger than the sheet
WIN_POCKET = 0.13                               # pocket depth: acrylic flush with the inside face
PANEL_DEPTH = WIN_POCKET                        # Shaker panel recess, same pass as the window pocket
WIN_CZ = 5.0                                    # window centre, up from the bottom of the oven door
HANDLE_CC = 3.78                                # 96 mm bar pull
HANDLE_Z = OVEN_DOOR_H - 1.0                    # bar pull centre line, down from the top edge
MARK_D = 0.35                                   # drill-guide dimples for the pull's screws
# stove
BURNER_D = 4.0       # four 4 in burners in a 2 x 2 grid; 5 in pans would not leave room for the four knobs
BURNER_GROOVE_R = 1.5
STOVE_CX = T + SINK_BAY + T + DRY_BAY + T + STOVE_BAY / 2
BURNER_DX, BURNER_Y0, BURNER_DY = 2.375, 4.5, 5.0          # 3/4 in between pans across, front row 4 1/2 in in (clear of the knobs), back row 5 in behind it
BURNERS = [(STOVE_CX + sx * BURNER_DX, BURNER_Y0 + j * BURNER_DY) for j in (0, 1) for sx in (-1, 1)]
KNOBS = [(STOVE_CX + i * 2.6, 1.3) for i in (-1.5, -0.5, 0.5, 1.5)]   # four in a row along the front edge, 2.6 in apart (the bezels are 2 in)
BURNER_X = [b[0] for b in BURNERS]; BURNER_Y = BURNERS[0][1]; KNOB_Y = KNOBS[0][1]; KNOB_X = [k[0] for k in KNOBS]

# --- bought parts the geometry depends on -----------------------------------
SINK_RIM = 15.0      # Elkay Dayton D115151, 15 x 15 rim
SINK_CUT = 14.375    # cutout, from the Elkay template (14 3/8)
SINK_CUT_R = 1.5     # cutout corner radius
SINK_BOWL = (12.0, 10.0, 5.0)   # bowl w, d, depth
SINK_DRAIN = 2.0
SINK_CX = T + SINK_BAY - 0.5 - SINK_CUT / 2    # 16.03: sink pushed to the right of its bay so the dirty jug can sit under the drain
SINK_CY = 9.0                     # pushed back so the drain lands over the dirty jug's neck, which sits at the jug's back edge
FAUCET_X = SINK_CX               # the sink's own faucet hole, centred on the rear deck
FAUCET_Y = SINK_CY + SINK_RIM / 2 - 1.25
FAUCET_H, FAUCET_REACH, FAUCET_TOP = 7.0, 5.0, 9.3    # ARCORA bar faucet: spout outlet 7 in up, 5 in reach, 9.3 in overall
# two 5 gal square jugs (yours): 10 x 10 x 14. Clean on the left, dirty on the right under the drain.
JUG_W, JUG_D, JUG_H = 10.0, 10.0, 14.0
JUG_NECK_D = 2.25                               # the opening: 2 1/4 in across, tangent to one edge of the top
JUG_NECK_IN = JUG_NECK_D / 2                    # neck centre from that edge, 1 1/8 in; both jugs stand neck to the back
JUG_GAP = 0.4
JUG_Y0 = T + 0.25                               # just behind the doors
CLEAN_X0 = T + 0.3                              # clean jug, against the left side
DIRTY_X0 = CLEAN_X0 + JUG_W + JUG_GAP           # 11.42: dirty jug beside it, centre at 16.42, drain at 16.03
DIRTY_CX = DIRTY_X0 + JUG_W / 2
CLEAN_CX = CLEAN_X0 + JUG_W / 2                 # 6.02
NECK_Y = JUG_Y0 + JUG_D - JUG_NECK_IN           # 9.85: neck centre of both jugs, kitchen y
PORT_X, PORT_Y = CLEAN_CX, NECK_Y               # the fill port sits straight over the clean jug's neck
DIRTY_FLOAT_Z = 12.0                            # side-mount float through the dirty jug's back wall: pump stops when the water reaches it (about 4 gal)
CLEAN_FLOAT_Z = 2.0                             # the other switch of the pair, low on the clean jug's back wall: pump stops when the water drops below it
CLEAN_FLOAT_GAL = (CLEAN_FLOAT_Z * JUG_W * JUG_D) / 231
DIRTY_FLOAT_GAL = (DIRTY_FLOAT_Z * JUG_W * JUG_D) / 231
assert PORT_X + 1.6 + 0.5 <= SINK_CX - SINK_RIM / 2, "fill port mouth hits the sink rim"
DRAIN_OFF = ((SINK_CX - DIRTY_CX) ** 2 + (SINK_CY - NECK_Y) ** 2) ** 0.5   # drain to neck, 0.94 in
JUG_HOLE = JUG_W + 0.5                          # the dirty jug stands on the floor in a notch this wide in the bottom panel
JUG_NOTCH_D = JUG_Y0 + JUG_D + 0.25             # the notch runs from the front edge to here, so the jug slides out without lifting
FUNNEL_D = 100 / 25.4                           # printed funnel mouth, 3.94 in: the strainer's 1 1/2 in outlet lands inside it with the drain an inch off the neck
STRAINER_DROP = 1.6                             # the basket strainer hangs about this far below the bowl
DRAIN_CLEAR = (HC - 0.1 - SINK_BOWL[2] - 0.2 - STRAINER_DROP) - (JUG_H + 1.0)   # strainer bottom to funnel rim
PUMP_L, PUMP_W, PUMP_H = 8.3, 4.3, 3.5          # ECO-WORTHY T33-12V envelope
PUMP_X0 = T + 0.8                               # pump on the back panel, long axis across, feet to the back
PUMP_Z0 = 16.5                                  # above the jugs' shoulders, below the counter
WBOX_X0 = PUMP_X0 + PUMP_L + 0.6                # printed wiring box on the back panel, right of the pump, behind the jugs
WBOX_Z0 = 11.6
WBOX_W, WBOX_H, WBOX_D = 6.0, 4.0, 1.6          # 152.4 x 101.6 mm on the panel, 40.6 mm deep with its lid: relay, six Wagos
CORD_X = WBOX_X0 + 2.5                          # 1/2 in cord hole in the back, kitchen x: inside the box's footprint
CORD_Z = 15.0

assert DIRTY_X0 + JUG_W + JUG_GAP <= T + SINK_BAY + 1e-9, "two jugs do not fit the sink bay"
assert DRAIN_OFF + 0.75 <= FUNNEL_D / 2, f"drain too far from the dirty jug's neck: {DRAIN_OFF:.2f} in"
assert SINK_CY + SINK_RIM / 2 + 0.3 <= CTR_D and SINK_CY + SINK_CUT / 2 + 1.0 <= CTR_D, "sink too far back for the rear clips"
assert SINK_CX + SINK_CUT / 2 <= T + SINK_BAY - 0.45, "sink cutout too close to divider A"
assert DRAIN_CLEAR >= 0.5, f"strainer hits the funnel: {DRAIN_CLEAR:.2f} in"
assert PUMP_Z0 + PUMP_W <= HC - T - 0.5, "pump hits the counter"
assert WBOX_Z0 + WBOX_H <= PUMP_Z0 - 0.5 and WBOX_X0 >= PUMP_X0 + PUMP_L + 0.5, "wiring box hits the pump"
assert WBOX_X0 + WBOX_W <= T + SINK_BAY - 0.5, "wiring box runs into divider A"
assert CTR_D - WBOX_D >= JUG_Y0 + JUG_D + 4.0, "wiring box in the jugs' way"
assert CTR_D - WBOX_D >= SINK_CY + SINK_BOWL[1] / 2 + 1.0, "wiring box under the bowl"
assert WBOX_X0 + 1.0 <= CORD_X <= WBOX_X0 + WBOX_W - 1.0 and WBOX_Z0 + 1.0 <= CORD_Z <= WBOX_Z0 + WBOX_H - 0.5, "cord hole not inside the wiring box"
assert 2 * (DOOR_KNOB_IN) + REVEAL - 1.5 >= 0.3, "the two sink-door knobs would touch"
assert HEADROOM >= FAUCET_TOP + 1.0, "faucet does not fit under the upper shelf"

# --- parts list: (code, label, qty, length_along_grain, width, notes, sheet) -----------------
PARTS = [
    ("SIDE",   "Side",            2, H,           D,           "Hutch profile: 18 in deep to the counter, 8 1/2 in above it. Rabbets top and bottom, dados for the counter and upper shelf. Right: oven shelf dado. Hinge recesses at the lower front edge. Left: two 1/2 in peg holes. Grain vertical.", "S1"),
    ("TANK",   "Upper shelf",     1, PANEL_L,     UP_SHELF_D,  "Floor of the four upper cupboards; three through dados on its top face for the upper dividers.", "S5"),
    ("UDIV",   "Upper divider",   3, UP_DIV_H,    UP_DIV_D,    "1/4 in into the upper shelf and the top, plain: four equal open compartments. All three in a row on S4.", "S4"),
    ("BACK",   "Back",            1, BACK_H,      INNER_W,     "Fills S2. Sits on the bottom, runs to the top, screwed through the sides. 1/2 in cord hole behind the pump.", "S2"),
    ("CTR",    "Counter",         1, PANEL_L,     CTR_D,       "Cut FACE DOWN: through dados for the dividers on the underside. Sink cutout, 1 1/2 in fill port, knob holes.", "S3"),
    ("BOT",    "Bottom",          1, PANEL_L,     CTR_D,       "On the floor. Through dados on the top face; a 10 1/2 in notch from the front edge where the dirty jug stands on the floor and slides out.", "S3"),
    ("TOP",    "Top",             1, PANEL_L,     UP_SHELF_D,  "Cut FACE DOWN: three upper divider dados on the underside. Sits in the sides' top rabbets.", "S3"),
    ("DIV",    "Divider",         2, DIV_H,       DIV_D,       "Full depth, 1/4 in into the bottom and the counter. A: hinge recesses on its left face. B: drying shelf dado and hinge recesses on its left face.", "S4"),
    ("DRYSH",  "Drying shelf",    1, DRY_L,       SHELF_D,     "1/4 in into divider B, screwed to divider A. Front corners rounded.", "S4"),
    ("OVEN",   "Oven floor",      1, OVEN_L,      SHELF_D,     "1/4 in into the right side, screwed to divider B. Oven above, warming drawer below.", "S4"),
    ("DOOR",   "Sink door",       2, DOOR_H,      DOOR_W,      "Two inset doors under the sink, 3/32 in reveal, grain vertical. Shaker panel: cut FRONT FACE UP. Light blue.", "S5"),
    ("DRYDOOR", "Drying door",    1, DOOR_H,      DRY_DOOR_W,  "Inset door on the drying cupboard, hinged on divider B. Shaker panel: cut FRONT FACE UP. Light blue.", "S5"),
    ("OVDOOR", "Oven door",       1, OVEN_DOOR_H, OVEN_DOOR_W, "Cut INSIDE FACE UP: window opening, 1/8 in pocket for the stock 8 x 10 acrylic, two dimples for the bar pull. Hinged on the right side. Light blue.", "S5"),
    ("WARMDOOR", "Warming door",  1, WARM_DOOR_H, OVEN_DOOR_W, "Below the oven, hinged on the right side. Shaker panel: cut FRONT FACE UP. Light blue.", "S5"),
]

def frac(x):
    """Nearest 1/32 as a mixed fraction string."""
    n = round(x * 32); whole, rem = divmod(n, 32)
    if rem == 0: return f"{whole}"
    g = math.gcd(rem, 32)
    s = f"{rem // g}/{32 // g}"
    return s if whole == 0 else f"{whole} {s}"

def mm(x): return f"{x * 25.4:.1f}"
def dec(x): return f"{x:.3f}"

# --- cut sheets: (code, title, [(label, w_x, h_y, x, y, kind)], note) ------------------------
# x,y = top-left on the sheet, w along X, h along Y. Each part's local frame (for dados and holes) is documented in
# local_features(); the up face is the one that gets the pockets.
def layout():
    k = KERF; L = LEFT
    s1_parts = [
        ("SIDE L", D, H, L, L, "sideL"),
        ("SIDE R", D, H, L + D + k, L, "sideR"),
    ]   # the upper shelf and upper dividers 1 and 3 moved to S5 and S4 after the first S1 runs spoiled them
    s2_parts = [
        ("BACK", INNER_W, BACK_H, L, L, "back"),
    ]
    s3_parts = [
        ("COUNTER", PANEL_L, CTR_D, L, L, "counter"),
        ("BOTTOM", PANEL_L, CTR_D, L, L + CTR_D + k, "bottom"),
        ("TOP", PANEL_L, UP_SHELF_D, L, L + 2 * CTR_D + 2 * k, "top"),
    ]
    s4_parts = [
        ("DIVIDER A", DIV_D, DIV_H, L, L, "divA"),
        ("DIVIDER B", DIV_D, DIV_H, L + DIV_D + k, L, "divB"),
        ("DRY SHELF", DRY_L, SHELF_D, L + 2 * DIV_D + 2 * k, L, "dry"),
        ("OVEN FLOOR", OVEN_L, SHELF_D, L, L + DIV_H + k, "oven"),
        ("UPPER DIV 2", UP_DIV_D, UP_DIV_H, L + OVEN_L + k, L + DIV_H + k, "udivp"),
        ("UPPER DIV 1", UP_DIV_D, UP_DIV_H, L + OVEN_L + UP_DIV_D + 2 * k, L + DIV_H + k, "udivp"),
        ("UPPER DIV 3", UP_DIV_D, UP_DIV_H, L + OVEN_L + 2 * UP_DIV_D + 3 * k, L + DIV_H + k, "udivp"),
    ]
    s5_parts = [
        ("SINK DOOR L", DOOR_W, DOOR_H, L, L, "doorL"),
        ("SINK DOOR R", DOOR_W, DOOR_H, L + DOOR_W + k, L, "doorR"),
        ("DRYING DOOR", DRY_DOOR_W, DOOR_H, L + 2 * DOOR_W + 2 * k, L, "drydoor"),
        ("OVEN DOOR", OVEN_DOOR_W, OVEN_DOOR_H, L + 2 * DOOR_W + DRY_DOOR_W + 3 * k, L, "ovdoor"),
        ("WARMING DOOR", OVEN_DOOR_W, WARM_DOOR_H, L + 2 * DOOR_W + DRY_DOOR_W + 3 * k, L + OVEN_DOOR_H + k, "warmdoor"),
        ("UPPER SHELF", PANEL_L, UP_SHELF_D, L, L + DOOR_H + k, "tankh"),     # full length below the doors; this sheet goes on grain left-right
    ]
    sheets = [
        ("S1", "Sides", s1_parts,
         "Both sides inside-face up, so they are mirror images: Side L's front edge is on the left, Side R's on the right; the notch at the top of each is the upper cabinet's set-back, at the front. The left side's two peg holes go straight through."),
        ("S2", "Back", s2_parts,
         "The back fills the sheet; the cord hole is the only feature."),
        ("S3", "Counter, bottom, top", s3_parts,
         "Counter FACE DOWN, front edge at the top of the sheet (its dados are underneath; the knob holes run along the front). Bottom face up, front edge (the jug notch) at the top too, which puts its left end on the RIGHT. Top FACE DOWN in the strip below."),
        ("S4", "Dividers, mid shelves, upper dividers", s4_parts,
         "Dividers stand upright, LEFT face up, front edge on the RIGHT, bottom end DOWN (hinge recesses along the front edge of both; the drying shelf dado across B). Shelves below and beside, the three plain upper dividers in a row beside the oven floor."),
        ("S5", "Doors, upper shelf", s5_parts,
         "Load this sheet with the grain running LEFT TO RIGHT, so the upper shelf's grain runs its length; the doors are painted, so their cross grain never shows. The two sink doors, the drying door and the warming door are FRONT FACE UP for their Shaker panels; the oven door INSIDE FACE UP for its window pocket. The upper shelf runs full length below them, face up, its three dados on top."),
    ]
    for code, title, parts, note in sheets:
        for label, w, h, x, y, kind in parts:
            assert x >= LEFT - 1e-9 and y >= LEFT - 1e-9, (code, label, "inside the border")
            assert x + w + KERF <= SHEET - HOLD + 1e-9, (code, label, "into the right hold-down strip", x + w + KERF)
            assert y + h + KERF <= SHEET - HOLD + 1e-9, (code, label, "into the bottom hold-down strip", y + h + KERF)
    # the upper dividers sit inside the sides' notches: check they clear the notch edges by a kerf
    assert UP_DIV_D + KERF <= NOTCH_D and UP_DIV_H + KERF <= H - HC, "upper divider does not fit the side's notch"
    return sheets

def break_lines(parts):
    xr = max(x + w for _, w, h, x, y, _ in parts) + BRK
    yb = max(y + h for _, w, h, x, y, _ in parts) + BRK
    return min(xr, SHEET), min(yb, SHEET)

# --- part-local features ------------------------------------------------------------------------
# Returns dict(dados=[(x, y, w, h, open_edges)], holes=[(cx, cy, d)], cutouts=[(cx, cy, w, h, r)],
#              corners=[r_tl, r_tr, r_br, r_bl], recesses=[(x, y, w, h, open_edges)], pockets=[(cx, cy, w, h, r, depth)],
#              marks=[(cx, cy, d)], notch=(w, h) or None) in the part's sheet frame (x right, y down, as drawn).
# open_edges says which ends of a dado run off the part (no rounded end there): subset of "lrtb".
def hinge_centres(z0, door_h):
    """Hinge centre heights for a door whose opening starts at z0."""
    return [z0 + REVEAL + HINGE_IN, z0 + REVEAL + door_h - HINGE_IN]

def recess_at_x(x, zc, y_from_top):
    """Hinge-leaf recess for a side (x = depth, y = height from the top), open at the front edge (x = 0) so the bit runs
    off the edge and the two corners there come out square."""
    return (x, y_from_top - HINGE_L / 2 - 0.03, HINGE_LEAF_W + 0.03, HINGE_L + 0.06, "l")

def local_features(kind):
    f = dict(dados=[], holes=[], cutouts=[], corners=[0, 0, 0, 0], recesses=[], pockets=[], marks=[], notch=None, fnotch=None)
    r = DADO_R
    if kind in ("sideL", "sideR"):
        # Worked out as the LEFT side: x = depth from the FRONT edge, y = height from the TOP, inside face up, front on the left.
        # The right side lies inside face up too, which puts its front on the RIGHT: it is mirrored at the end of this block.
        f["notch"] = (NOTCH_D, H - HC)                                 # the upper cabinet's set-back, top-left (top-right on the right side)
        f["dados"].append((0, H - T, CTR_D, DADO_W, "lrb"))             # bottom rabbet, open at the floor edge
        f["dados"].append((0, H - HC, CTR_D, DADO_W, "lr"))             # counter dado, full depth (its top runs into the notch)
        f["dados"].append((NOTCH_D, H - TANK_Z, UP_SHELF_D, DADO_W, "lr"))   # upper shelf dado, upper portion only
        f["dados"].append((NOTCH_D, 0, UP_SHELF_D, DADO_W, "lrt"))      # top rabbet
        if kind == "sideR":
            f["dados"].append((CTR_D - SHELF_D, H - OVEN_Z, SHELF_D, DADO_W, "r"))   # oven floor: stopped at the front
            lower = hinge_centres(OVEN_Z, OVEN_DOOR_H) + hinge_centres(T, WARM_DOOR_H)
        else:
            lower = hinge_centres(T, DOOR_H)
        for zc in lower: f["recesses"].append(recess_at_x(0, zc, H - zc))
        if kind == "sideL":                                        # peg hooks through the outer face: the bit plunges them
            for py in PEG_Y: f["holes"].append((py, H - PEG_Z, BIT))
        if kind == "sideR":                                        # mirror image: front edge on the right
            swap = {"l": "r", "r": "l"}
            f["dados"] = [(D - x - w, y, w, h, "".join(swap.get(c, c) for c in oe)) for x, y, w, h, oe in f["dados"]]
            f["recesses"] = [(D - x - w, y, w, h, "".join(swap.get(c, c) for c in oe)) for x, y, w, h, oe in f["recesses"]]
            f["notch_side"] = "r"
    elif kind == "bottom":
        # Top face up with the FRONT edge (the jug notch) at the top of the sheet, which turns the panel end for end: x is measured
        # from its RIGHT end. (Front at the top and x from the left would be the mirror image.)
        for xk in (T + SINK_BAY, T + SINK_BAY + T + DRY_BAY): f["dados"].append((PANEL_L - (xk - (T - DADO)) - DADO_W, 0, DADO_W, CTR_D, "tb"))
        f["fnotch"] = (PANEL_L - (DIRTY_CX - (T - DADO) + JUG_HOLE / 2), JUG_HOLE, JUG_NOTCH_D)   # open to the front: the dirty jug slides out on the floor
    elif kind == "tankh":
        # Lies full length across S5, face up: x = length from either end (UDIV_X is symmetric), three through dados.
        for xk in UDIV_X: f["dados"].append((xk - (T - DADO), 0, DADO_W, UP_SHELF_D, "tb"))
    elif kind == "tank":
        # Lies on S1 turned a quarter turn, its length running DOWN the sheet: x = depth, y = length from the left end.
        # Three through dados across it, face up, for the upper dividers (UDIV_X is symmetric, so either end can be the left).
        for xk in UDIV_X: f["dados"].append((0, xk - (T - DADO), UP_SHELF_D, DADO_W, "lr"))
    elif kind in ("counter", "top"):
        # Cut FACE DOWN, flipped over about its long edge: x = from the left end, y = from the FRONT edge (front at the top of the sheet).
        depth = CTR_D if kind == "counter" else UP_SHELF_D
        xs = (T + SINK_BAY, T + SINK_BAY + T + DRY_BAY) if kind == "counter" else UDIV_X
        for xk in xs: f["dados"].append((xk - (T - DADO), 0, DADO_W, depth, "tb"))
        if kind == "counter":
            f["cutouts"].append((SINK_CX - (T - DADO), SINK_CY, SINK_CUT, SINK_CUT, SINK_CUT_R))
            f["holes"].append((PORT_X - (T - DADO), PORT_Y, PORT_D))                           # fill port, bigger than the bit: contour inside
            for kx, ky in KNOBS: f["holes"].append((kx - (T - DADO), ky, KNOB_HOLE))
    elif kind in ("divA", "divB", "udiv", "udivp"):
        # Worked out with z = height from the BOTTOM end and d = depth from the FRONT edge, then turned into the way the panel
        # lies on its sheet: LEFT face up, front edge on the RIGHT, bottom end at the BOTTOM, so sheet x = DIV_D - d and
        # sheet y = DIV_H - z. (Upper dividers are plain.)
        zd = []                                                    # (z0, d0, z_len, d_len, open edges as b/t = bottom/top end, f/r = front/rear)
        if kind == "divB":                                         # drying shelf dado, stopped at the front, open at the rear
            zd.append(((DRY_Z - T) - (T - DADO), CTR_D - SHELF_D, DADO_W, SHELF_D, "r"))
        if kind in ("divA", "divB"):                               # sink right door (A), drying door (B): recesses on the front edge
            for zc in hinge_centres(T, DOOR_H):
                f["recesses"].append((DIV_D - (HINGE_LEAF_W + 0.03), DIV_H - (zc - (T - DADO) + HINGE_L / 2 + 0.03), HINGE_LEAF_W + 0.03, HINGE_L + 0.06, "r"))   # open at the front edge
        for z0, d0, zl, dl, oe in zd:
            sheet_oe = "".join({"b": "b", "t": "t", "f": "r", "r": "l"}[c] for c in oe)
            f["dados"].append((DIV_D - (d0 + dl), DIV_H - (z0 + zl), dl, zl, sheet_oe))
    elif kind in ("oven", "dry"):
        f["corners"] = [r, r, 0, 0]                                # front corners rounded to the stopped dado ends
    elif kind == "back":
        # Front face up. x = width from the left end (at the left side's inner face), y = height from the TOP.
        f["holes"].append((CORD_X - T, H - CORD_Z, BIT))
    elif kind == "doorL":
        f["holes"].append((DOOR_W - DOOR_KNOB_IN, DOOR_H / 2, KNOB_HOLE))   # hinged on the left: knob at the right edge
        f["pockets"].append((DOOR_W / 2, DOOR_H / 2, DOOR_W - 2 * FRAME, DOOR_H - 2 * FRAME, DADO_R, PANEL_DEPTH))   # Shaker panel
    elif kind in ("doorR", "drydoor", "warmdoor"):
        h = WARM_DOOR_H if kind == "warmdoor" else DOOR_H
        f["holes"].append((DOOR_KNOB_IN, h / 2, KNOB_HOLE))          # hinged on the right: knob at the left edge
        w = {"drydoor": DRY_DOOR_W, "warmdoor": OVEN_DOOR_W}.get(kind, DOOR_W)   # Shaker panel on the sink, drying and warming doors
        f["pockets"].append((w / 2, h / 2, w - 2 * FRAME, h - 2 * FRAME, DADO_R, PANEL_DEPTH))
    elif kind == "ovdoor":
        # INSIDE FACE UP. x across, y from the top. Window through, acrylic pocket round it, dimples for the pull's screws.
        cx, cy = OVEN_DOOR_W / 2, OVEN_DOOR_H - WIN_CZ
        f["cutouts"].append((cx, cy, WIN_W, WIN_H, WIN_R))
        f["pockets"].append((cx, cy, ACR_W + ACR_SLACK, ACR_H + ACR_SLACK, 0.3, WIN_POCKET))
        for sx in (-1, 1): f["marks"].append((cx + sx * HANDLE_CC / 2, OVEN_DOOR_H - HANDLE_Z, MARK_D))
    return f

# How each part's up face is drawn on its sheet, in kitchen axes (x = right, y = back, z = up): the face's outward normal,
# then the kitchen directions that point to the sheet's right and to the sheet's top. A drawing is the face as you see it,
# not its mirror image, only when right x top = normal. Parts whose features are symmetric either way are left out.
SHEET_FRAMES = {
    "sideL": ("+x", "+y", "+z"), "sideR": ("-x", "-y", "+z"),
    "divA": ("-x", "-y", "+z"), "divB": ("-x", "-y", "+z"),
    "back": ("-y", "+x", "+z"),
    "bottom": ("+z", "-x", "-y"), "counter": ("-z", "+x", "-y"),
    "doorL": ("-y", "+x", "+z"), "doorR": ("-y", "+x", "+z"), "drydoor": ("-y", "+x", "+z"), "warmdoor": ("-y", "+x", "+z"),
}
def _ax(s): v = [0, 0, 0]; v["xyz".index(s[1])] = 1 if s[0] == "+" else -1; return v
for _k, (_n, _r, _u) in SHEET_FRAMES.items():
    _a, _b = _ax(_r), _ax(_u)
    _c = [_a[1] * _b[2] - _a[2] * _b[1], _a[2] * _b[0] - _a[0] * _b[2], _a[0] * _b[1] - _a[1] * _b[0]]
    assert _c == _ax(_n), f"{_k} is drawn as its mirror image"
# and the features agree with those frames where it is easy to see:
_ctr = local_features("counter"); assert all(y < 2.0 for x, y, d in _ctr["holes"] if d == KNOB_HOLE), "counter: the knob holes run along the front edge, at the top"
assert all(x > PANEL_L / 2 for x, y, d in _ctr["holes"] if d == KNOB_HOLE), "counter: the stove knobs belong at the right end"
assert local_features("bottom")["fnotch"][0] > PANEL_L / 2, "bottom: the jug notch is near the left end, which is drawn on the right"
assert local_features("sideR").get("notch_side") == "r", "right side: the notch (front) is on the right"

def write_params(path):
    lines = ["// GENERATED by design.py. Edit design.py, not this file. Units: inches."]
    for k in ["T", "W", "D", "H", "HC", "TOE", "UP_D", "NOTCH_D", "INNER_W", "PANEL_L", "CTR_D", "UP_SHELF_D", "BACK_H",
              "SINK_BAY", "STOVE_BAY", "DRY_BAY", "DIV_D", "DIV_H", "STOVE_CX", "TANK_Z", "UP_DIV_D", "UP_DIV_H",
              "UP_BAY", "UP_OPEN_H", "PORT_D", "PORT_X", "PORT_Y", "PEG_Z", "PEG_L", "CLEAN_CX", "OVEN_Z", "DRY_Z", "SHELF_D", "OVEN_L", "DRY_L",
              "HINGE_L", "HINGE_LEAF_W", "HINGE_RECESS", "HINGE_IN", "FAUCET_X", "FAUCET_Y", "FAUCET_H", "FAUCET_REACH", "FAUCET_TOP",
              "PUMP_L", "PUMP_W", "PUMP_H", "PUMP_X0", "PUMP_Z0", "WBOX_X0", "WBOX_Z0", "WBOX_W", "WBOX_H", "WBOX_D", "CORD_X", "CORD_Z",
              "JUG_W", "JUG_D", "JUG_H", "JUG_NECK_D", "JUG_NECK_IN", "NECK_Y", "DIRTY_FLOAT_Z", "CLEAN_FLOAT_Z", "JUG_Y0", "CLEAN_X0", "DIRTY_X0", "DIRTY_CX", "JUG_HOLE", "JUG_NOTCH_D", "FUNNEL_D",
              "DOOR_W", "DOOR_H", "DRY_DOOR_W", "OVEN_DOOR_W", "OVEN_DOOR_H", "WARM_DOOR_H", "REVEAL",
              "WIN_W", "WIN_H", "WIN_R", "ACR_W", "ACR_H", "ACR_T", "ACR_SLACK", "WIN_POCKET", "PANEL_DEPTH", "FRAME", "WIN_CZ", "HANDLE_CC", "HANDLE_Z", "MARK_D",
              "BURNER_D", "BURNER_GROOVE_R", "BURNER_Y", "KNOB_Y",
              "SINK_RIM", "SINK_CUT", "SINK_CUT_R", "SINK_DRAIN", "SINK_CX", "SINK_CY", "KNOB_HOLE", "DOOR_KNOB_IN",
              "BIT", "DADO", "DADO_W", "DADO_R"]:
        lines.append(f"{k} = {globals()[k]:.4f};")
    lines.append("BURNERS = [" + ", ".join(f"[{x:.4f}, {y:.4f}]" for x, y in BURNERS) + "];")
    lines.append("KNOBS = [" + ", ".join(f"[{x:.4f}, {y:.4f}]" for x, y in KNOBS) + "];")
    lines.append("UDIV_X = [" + ", ".join(f"{x:.4f}" for x in UDIV_X) + "];")
    lines.append("PEG_Y = [" + ", ".join(f"{y:.4f}" for y in PEG_Y) + "];")
    lines.append(f"SINK_BOWL = [{SINK_BOWL[0]}, {SINK_BOWL[1]}, {SINK_BOWL[2]}];")
    with open(path, "w") as fh:
        fh.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    import sys
    write_params(sys.argv[1] if len(sys.argv) > 1 else "params.scad")
    for code, title, parts, note in layout():
        print(code, title, "break lines at", [round(v, 3) for v in break_lines(parts)])
    print("W", frac(W), " doors", frac(DOOR_W), "x", frac(DOOR_H), " oven door", frac(OVEN_DOOR_W), "x", frac(OVEN_DOOR_H),
          " divider", frac(DIV_D), "x", frac(DIV_H), " panels", frac(PANEL_L), " drain clearance", round(DRAIN_CLEAR, 2), " headroom", round(HEADROOM, 2))
