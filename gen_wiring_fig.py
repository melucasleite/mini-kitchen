#!/usr/bin/env python3
"""wiring.svg: 12 V supply, relay, pump and the two float switches in series, with the pigtail plugs and lever connectors."""
INK, INK2, CHALK, PAPER, BOX = "#1e2422", "#5a605c", "#2456a4", "#f8f7f3", "#eceae3"
RED, BLK, BLU, ORG = "#c8312b", "#222222", "#2456a4", "#d9822b"
o = []
def f(x): return f"{x:.3f}"
def text(x, y, s, size=0.32, c=INK, anchor="start", bold=False):
    o.append(f'<text x="{f(x)}" y="{f(y)}" style="font-family:Helvetica, Arial, sans-serif;font-size:{size}px;font-weight:{700 if bold else 400};fill:{c};text-anchor:{anchor}">{s}</text>')
def box(x, y, w, h, title, sub=None, fill=BOX):
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="0.15" fill="{fill}" stroke="{INK}" stroke-width="0.04"/>')
    text(x + w / 2, y + 0.5, title, 0.34, INK, "middle", True)
    if sub: text(x + w / 2, y + 0.92, sub, 0.26, INK2, "middle")
def wire(pts, c, w=0.07):
    o.append('<polyline points="' + " ".join(f"{f(x)},{f(y)}" for x, y in pts) + f'" fill="none" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"/>')
def pin(x, y, label, side="l"):
    o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="0.11" fill="{PAPER}" stroke="{INK}" stroke-width="0.04"/>')
    text(x + (0.25 if side == "l" else -0.25), y + 0.11, label, 0.3, INK, "start" if side == "l" else "end", True)
def wago(x, y, n=3):
    o.append(f'<rect x="{f(x - 0.35)}" y="{f(y - 0.28)}" width="0.7" height="0.56" rx="0.08" fill="#f07a2a" stroke="{INK}" stroke-width="0.03"/>')
    text(x, y + 0.75, "connector", 0.22, INK2, "middle")
def plug(x, y, vertical=True):
    if vertical:
        o.append(f'<rect x="{f(x - 0.4)}" y="{f(y - 0.55)}" width="0.8" height="0.5" rx="0.06" fill="#333" stroke="{INK}" stroke-width="0.03"/>')
        o.append(f'<rect x="{f(x - 0.4)}" y="{f(y + 0.05)}" width="0.8" height="0.5" rx="0.06" fill="#555" stroke="{INK}" stroke-width="0.03"/>')
def dot(x, y, c): o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="0.1" fill="{c}"/>')

# --- power supply and adapter
box(0.8, 1.6, 4.2, 2.2, "12 V 10 A supply", "outside, behind the kitchen")
wire([(0.8, 2.7), (0.2, 2.7), (0.2, 5.4)], "#888", 0.09); text(0.35, 5.8, "to the wall", 0.26, INK2)
box(5.8, 1.9, 2.6, 1.7, "barrel adapter", None, "#fff")
text(7.1, 3.25, "screw terminals", 0.24, INK2, "middle")
wire([(5.0, 2.8), (5.8, 2.8)], "#888", 0.12)
for yy, lab in ((2.5, "+"), (3.2, "−")):
    o.append(f'<circle cx="8.4" cy="{yy}" r="0.11" fill="{PAPER}" stroke="{INK}" stroke-width="0.04"/>'); text(8.62, yy - 0.12, lab, 0.32, INK, "start", True)
text(7.1, 4.2, "outside, behind the kitchen", 0.24, INK2, "middle")
text(9.15, 4.9, "pair in through", 0.22, INK2, "end"); text(9.15, 5.2, "the cord hole", 0.22, INK2, "end")

# --- relay (coil pins 85 and 86 are interchangeable)
RX, RY = 13.0, 1.4
box(RX, RY, 4.4, 4.6, "relay, 12 V 30 A", "in its socket, zip-tied in the box")
pin(RX, RY + 2.0, "86", "l"); pin(RX, RY + 3.3, "85", "l")
pin(RX + 4.4, RY + 2.0, "30", "r"); pin(RX + 4.4, RY + 3.3, "87", "r"); pin(RX + 4.4, RY + 4.1, "87a", "r")
text(RX + 2.2, RY + 2.75, "coil", 0.26, INK2, "middle")
o.append(f'<path d="M{f(RX + 1.4)} {f(RY + 2.0)} q0.4 0.32 0 0.65 q-0.4 0.32 0 0.65" fill="none" stroke="{INK2}" stroke-width="0.04"/>')
text(RX + 4.0, RY + 4.85, "87a: capped in its own connector", 0.24, INK2, "end")

# --- pump
PX, PY = 23.5, 1.4
box(PX, PY, 4.8, 3.0, "pump, ECO-WORTHY T33", "pressure switch inside")
pin(PX, PY + 1.6, "red +", "l"); pin(PX, PY + 2.4, "black −", "l")

# --- + : adapter + to Wago A, split to relay 30 (over the top) and down to the clean float
WA = (10.4, 2.5)
wire([(8.4, 2.5), (WA[0] - 0.35, 2.5)], RED)
wire([(WA[0] + 0.35, 2.5), (11.6, 2.5), (11.6, 0.7), (RX + 5.4, 0.7), (RX + 5.4, RY + 2.0), (RX + 4.4, RY + 2.0)], RED)
wire([(WA[0], 2.78), (WA[0], 8.6)], RED)
wago(*WA)

# --- − : adapter − to Wago B, split to relay 86 and to the pump's black lead
WB = (11.2, 4.6)
wire([(8.4, 3.2), (9.4, 3.2), (9.4, 4.6), (WB[0] - 0.35, 4.6)], BLK)
wire([(WB[0] + 0.35, 4.6), (12.3, 4.6), (12.3, RY + 2.0), (RX, RY + 2.0)], BLK)
wire([(WB[0], 4.88), (WB[0], 6.6), (21.0, 6.6), (21.0, PY + 2.4), (PX, PY + 2.4)], BLK)
wago(*WB)
text(19.6, 6.45, "ground", 0.26, INK2)

# --- relay 87 to the pump's red lead: switched +12 V
wire([(RX + 4.4, RY + 3.3), (20.2, RY + 3.3), (20.2, PY + 1.6), (PX, PY + 1.6)], ORG)
text(20.4, PY + 1.35, "switched +12 V", 0.26, ORG)

# --- the jugs, each float on a 2-pin pigtail plug
def jug(x, y, label, float_z_frac, note):
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="3.0" height="4.2" rx="0.25" fill="#dbe9f6" stroke="{INK}" stroke-width="0.04"/>')
    fy = y + 4.2 * (1 - float_z_frac)
    o.append(f'<rect x="{f(x + 1.4)}" y="{f(fy - 0.2)}" width="1.0" height="0.4" rx="0.1" fill="#ddd" stroke="{INK}" stroke-width="0.03"/>')
    o.append(f'<rect x="{f(x + 2.85)}" y="{f(fy - 0.15)}" width="0.35" height="0.3" fill="#555" stroke="{INK}" stroke-width="0.02"/>')
    text(x + 1.5, y + 4.7, label, 0.3, INK, "middle", True)
    text(x + 1.5, y + 5.1, note, 0.24, INK2, "middle")
    return x + 3.2, fy
JY = 10.0
cx, cfy = jug(6.6, JY, "clean jug", 0.15, "float LOW: opens on empty")
dx, dfy = jug(13.7, JY, "dirty jug", 0.85, "float HIGH: opens on full")
for (x, fy) in ((cx, cfy), (dx, dfy)):
    wire([(x, fy - 0.05), (x + 0.6, fy - 0.05), (x + 0.6, JY - 0.4)], BLU)
    wire([(x, fy + 0.07), (x + 0.85, fy + 0.07), (x + 0.85, JY - 0.4)], BLU)
    plug(x + 0.72, JY - 0.9)
    text(x + 1.3, JY - 0.85, "2-pin plug", 0.24, INK2)
# + into the clean float
wire([(WA[0], 8.6), (cx + 0.6, 8.6), (cx + 0.6, JY - 1.45)], RED)
# clean float out, into the dirty float (the series join)
wire([(cx + 0.85, JY - 1.45), (cx + 0.85, 7.4), (dx + 0.6, 7.4), (dx + 0.6, JY - 1.45)], BLU)
WS = ((cx + dx) / 2 + 0.6, 7.4); wago(*WS)
text(WS[0], 7.05, "SERIES: floats in series", 0.26, BLU, "middle")
# dirty float out, up to relay 85
wire([(dx + 0.85, JY - 1.45), (dx + 0.85, 6.3), (12.7, 6.3)], BLU)
wire([(12.7, 6.3), (12.7, RY + 3.3), (RX, RY + 3.3)], BLU)
text(9.0, 13.9, "", 0.2)

# --- the printed wiring box: everything inside the dashed line
o.append('<rect x="9.45" y="0.25" width="9.65" height="8.2" rx="0.2" fill="none" stroke="#7a7f7b" stroke-width="0.05" stroke-dasharray="0.3 0.18"/>')
text(9.25, 6.7, "dashed line: the printed", 0.24, INK2, "end", True); text(9.25, 7.02, "wiring box, over the cord hole", 0.24, INK2, "end", True)
for (wx, wy), lab in ((WA, "+12V"), (WB, "GND")):
    text(wx + 0.45, wy - 0.33, lab, 0.2, INK, "start", True)
text(12.6, 6.12, "85", 0.2, INK, "end", True); text(19.05, RY + 3.15, "PUMP+", 0.2, INK, "end", True)
# --- notes
NX, NY = 22.0, 8.2
text(NX, NY, "How it works", 0.38, INK, "start", True)
notes = ["The relay's coil is fed through both floats in series.",
         "Both closed (water in the clean jug, room in the dirty jug):",
         "the coil pulls in, 30 connects to 87, the pump gets +12 V.",
         "Either float open: the coil drops out, the pump goes dead.",
         "The pump's own pressure switch then runs it only while",
         "the tap is open. The floats only ever carry the coil's",
         "~150 mA; the relay carries the pump's 6 A.",
         "",
         "In the box, one lever connector per labelled slot, relay",
         "leads on the single ends: GND, +12V and SERIES 1-in-2-out;",
         "PUMP+, 85 and 87a (a cap) 1-in-1-out. At each jug, 1-in-1-out",
         "connectors where the float and the run meet its plug.",
         "Wires that cross without a connector are not joined.",
         "Each 2-pin plug lets its jug leave the cabinet.",
         "Relay socket wire colours vary: go by the pin numbers",
         "moulded on the socket, not the colours."]
for i, n in enumerate(notes): text(NX, NY + 0.6 + i * 0.42, n, 0.28)
# legend
LY = 16.2
for i, (c, lab) in enumerate([(RED, "+12 V"), (BLK, "ground"), (ORG, "switched +12 V to the pump"), (BLU, "float loop, to relay coil 85")]):
    wire([(0.8 + i * 5.2, LY), (1.6 + i * 5.2, LY)], c, 0.1); text(1.8 + i * 5.2, LY + 0.1, lab, 0.28)

W, H = 30.5, 17.0
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Wiring: 12 V supply, relay, pump, and the two float switches in series">'
       f'<rect width="{W}" height="{H}" fill="{PAPER}"/>' + "\n".join(o) + '</svg>')
open("wiring.svg", "w").write(svg)
print("wrote wiring.svg")
