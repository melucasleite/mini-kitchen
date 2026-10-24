#!/usr/bin/env python3
"""float.svg: both jugs in section, seen from the side (front on the left, back wall on the right), each with its side-mount
float switch; a detail of how a side-mount switch goes through the wall; the steps. Inches, numbers from design.py."""
from design import JUG_W, JUG_D, JUG_H, JUG_NECK_D, JUG_NECK_IN, CLEAN_FLOAT_Z, DIRTY_FLOAT_Z, CLEAN_FLOAT_GAL, DIRTY_FLOAT_GAL, frac
INK, INK2, CHALK, BIRCH, WATER, PAPER, DARK = "#1e2422", "#5a605c", "#2456a4", "#e6cda3", "#bfd6ec", "#f8f7f3", "#2a2a2c"
o = []
def f(x): return f"{x:.3f}"
def line(x1, y1, x2, y2, c=INK, w=0.03, dash=None):
    o.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else "") + '/>')
def rect(x, y, w, h, fill="none", c=INK, sw=0.03, r=0):
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(r)}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')
def poly(pts, fill="none", c=INK, sw=0.03):
    o.append('<path d="M' + " L".join(f"{f(x)} {f(y)}" for x, y in pts) + f'Z" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')
def text(x, y, s, size=0.32, c=INK, anchor="start", bold=False):
    o.append(f'<text x="{f(x)}" y="{f(y)}" style="font-family:Helvetica, Arial, sans-serif;font-size:{size}px;font-weight:{700 if bold else 400};fill:{c};text-anchor:{anchor}">{s}</text>')
def num(x, y, n):
    o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="0.28" fill="{CHALK}"/>'); text(x, y + 0.11, str(n), 0.32, PAPER, "middle", True)

def jug(x0, floor, level, label):
    top = floor - JUG_H
    rect(x0 + 0.1, floor - level, JUG_D - 0.2, level - 0.1, WATER, "none", 0)
    rect(x0, top, JUG_D, JUG_H, "none", INK, 0.05, 0.3)
    nx = x0 + JUG_D - JUG_NECK_IN                                    # neck at the back edge
    rect(nx - JUG_NECK_D / 2, top - 0.6, JUG_NECK_D, 0.6, PAPER, INK, 0.05)
    rect(nx - JUG_NECK_D / 2 - 0.15, top - 0.95, JUG_NECK_D + 0.3, 0.38, BIRCH, INK, 0.05, 0.08)
    text(x0 + JUG_D / 2, floor + 1.25, label, 0.4, INK, "middle", True)
    text(x0 - 0.2, floor + 0.05, "floor", 0.26, INK2, "end"); text(x0 + 0.1, floor + 0.45, "front", 0.26, INK2); text(x0 + JUG_D - 0.1, floor + 0.45, "back", 0.26, INK2, "end")
    return top, nx

def side_float(xw, z, floor, closed_up):
    """Side-mount float through the back wall at xw, height z: flange inside, nut and cable outside, float on a hinged arm."""
    y = floor - z
    rect(xw - 0.45, y - 0.32, 0.35, 0.64, DARK, INK, 0.02)            # flange inside
    rect(xw - 0.1, y - 0.2, 0.55, 0.4, "#555", INK, 0.02)            # thread through the wall
    rect(xw + 0.2, y - 0.3, 0.2, 0.6, "#888", INK, 0.02)             # nut outside
    for i, (dy, c) in enumerate([(0, "#ddd"), (0.55, "none")]):       # float up (solid) / down (ghost)
        fx = xw - 1.55
        if i == 0: rect(fx, y - 0.62, 1.0, 0.42, "#ddd", INK, 0.03, 0.12); line(fx + 1.0, y - 0.41, xw - 0.45, y - 0.05, INK, 0.04)
        else: o.append(f'<rect x="{f(fx)}" y="{f(y + 0.2)}" width="1" height="0.42" rx="0.12" fill="none" stroke="{INK2}" stroke-width="0.02" stroke-dasharray="0.08 0.06"/>')
    o.append(f'<path d="M{f(xw + 0.45)} {f(y)} q0.6 0 0.6 -0.6 V{f(y - 1.2)}" fill="none" stroke="#c33" stroke-width="0.04"/>')
    o.append(f'<path d="M{f(xw + 0.45)} {f(y + 0.08)} q0.75 0 0.75 -0.7 V{f(y - 1.2)}" fill="none" stroke="#333" stroke-width="0.04"/>')
    rect(xw + 0.75, y - 1.75, 0.6, 0.5, "#333", INK, 0.03, 0.06)
    text(xw + 1.5, y - 1.42, "2-pin plug", 0.26, INK2)
    text(xw - 1.7, y - 0.75, "float up = " + ("closed" if closed_up else "open: pump stops"), 0.26, INK2, "end")
    text(xw - 1.7, y + 0.9, "float down = " + ("open: pump stops" if closed_up else "closed"), 0.26, INK2, "end")

FLOOR = 18.6
# clean jug
X1 = 2.2
top, nx = jug(X1, FLOOR, 8.0, f"Clean jug, {frac(JUG_W)} × {frac(JUG_D)} × {frac(JUG_H)} in")
fx = X1 + 3.4                                                         # pickup foot on the floor
poly([(fx - 0.7, FLOOR - 0.05), (fx - 0.7, FLOOR - 1.0), (fx - 0.43, FLOOR - 1.45), (fx - 0.43, FLOOR - 1.9), (fx + 0.43, FLOOR - 1.9), (fx + 0.43, FLOOR - 1.45), (fx + 0.7, FLOOR - 1.0), (fx + 0.7, FLOOR - 0.05)], DARK)
for i in range(5): line(fx - 0.55 + i * 0.27, FLOOR - 0.25, fx - 0.55 + i * 0.27, FLOOR - 0.9, PAPER, 0.04)
o.append(f'<path d="M{f(fx - 0.31)} {f(FLOOR - 1.9)} V{f(FLOOR - 6)} Q{f(fx - 0.31)} {f(FLOOR - 9)} {f(nx - 0.31)} {f(FLOOR - 10)} V{f(top - 2.4)} h0.62 V{f(FLOOR - 10)} Q{f(fx + 0.31)} {f(FLOOR - 9)} {f(fx + 0.31)} {f(FLOOR - 6)} V{f(FLOOR - 1.9)} Z" fill="#dbe9f6" stroke="{CHALK}" stroke-width="0.03"/>')
text(nx - 0.5, top - 2.0, "to the pump", 0.26, CHALK, "end")
text(fx - 0.9, FLOOR - 1.2, "pickup foot", 0.28, INK, "end")
side_float(X1 + JUG_D, CLEAN_FLOAT_Z, FLOOR, True)
trip = FLOOR - CLEAN_FLOAT_Z - 0.45
line(X1 + 0.1, trip, X1 + JUG_D - 0.1, trip, CHALK, 0.025, "0.15 0.1")
text(X1 - 0.2, trip + 0.1, "pump stops", 0.28, CHALK, "end"); text(X1 - 0.2, trip + 0.45, f"{CLEAN_FLOAT_GAL:.1f} gal left", 0.26, INK2, "end")
num(X1 + JUG_D + 1.05, FLOOR - CLEAN_FLOAT_Z - 2.3, 1)

# dirty jug
X2 = 16.2
top2, nx2 = jug(X2, FLOOR, 6.0, "Dirty jug, on the floor in the notch")
poly([(nx2 - 2.0, top2 - 1.9), (nx2 + 2.0, top2 - 1.9), (nx2 + 0.75, top2 - 1.0), (nx2 + 0.75, top2 + 0.4), (nx2 - 0.75, top2 + 0.4), (nx2 - 0.75, top2 - 1.0)], DARK)
text(nx2, top2 - 2.15, "printed funnel, under the sink strainer", 0.28, INK, "middle")
side_float(X2 + JUG_D, DIRTY_FLOAT_Z, FLOOR, False)
full = FLOOR - DIRTY_FLOAT_Z - 0.45
line(X2 + 0.1, full, X2 + JUG_D - 0.1, full, CHALK, 0.025, "0.15 0.1")
text(X2 - 0.2, full + 0.1, "pump stops", 0.28, CHALK, "end"); text(X2 - 0.2, full + 0.45, f"about {DIRTY_FLOAT_GAL:.0f} gal in", 0.26, INK2, "end")
num(X2 + JUG_D + 1.05, FLOOR - DIRTY_FLOAT_Z - 2.3, 2)

# detail: a side-mount switch through the wall, 3x
DX, DY = 30.5, 3.0
text(DX, DY - 0.6, "A side-mount float, through the wall, 3×", 0.4, INK, "start", True)
wx = DX + 4.2; cy = DY + 3.0
rect(wx, DY, 0.35, 6.0, "#c9dceb", INK, 0.03)                        # jug wall
text(wx - 0.2, DY + 6.5, "inside", 0.3, INK2, "end"); text(wx + 0.55, DY + 6.5, "outside", 0.3, INK2)
rect(wx - 0.9, cy - 0.9, 0.9, 1.8, DARK, INK, 0.03)                   # flange inside
rect(wx - 0.08, cy - 0.95, 0.08, 1.9, "#444", INK, 0.02)              # gasket
rect(wx, cy - 0.55, 1.9, 1.1, "#555", INK, 0.03)                      # thread
for i in range(7): line(wx + 0.4 + i * 0.22, cy - 0.55, wx + 0.55 + i * 0.22, cy + 0.55, "#999", 0.02)
rect(wx + 0.4, cy - 0.85, 0.6, 1.7, "#888", INK, 0.03)                # nut
line(wx - 0.9, cy - 0.3, wx - 2.4, cy - 1.6, INK, 0.08)              # arm
rect(wx - 4.0, cy - 2.4, 1.8, 1.1, "#ddd", INK, 0.04, 0.25)           # float
o.append(f'<path d="M{f(wx + 1.9)} {f(cy - 0.12)} H{f(wx + 4.5)}" stroke="#c33" stroke-width="0.07" fill="none"/>')
o.append(f'<path d="M{f(wx + 1.9)} {f(cy + 0.12)} H{f(wx + 4.5)}" stroke="#333" stroke-width="0.07" fill="none"/>')
text(wx - 0.5, cy + 1.35, "flange + gasket", 0.28, INK2, "end"); text(wx + 0.7, cy + 1.35, "nut", 0.28, INK2, "start")
text(wx + 2.6, cy - 0.35, "two wires", 0.28, INK2)
text(wx - 3.1, cy - 2.65, "float on a hinged arm", 0.28, CHALK, "middle")
text(DX, DY + 7.4, "5/8 in hole. Goes in from inside: lower it through the", 0.3, INK)
text(DX, DY + 7.85, "neck on its lead, fish the lead out the hole, pull the", 0.3, INK)
text(DX, DY + 8.3, "thread through, nut on outside. Flip the float on its", 0.3, INK)
text(DX, DY + 8.75, "arm to swap open-on-empty and open-on-full.", 0.3, INK)

# steps
SX, SY = 30.5, 13.4
text(SX, SY, "In order", 0.4, INK, "start", True)
steps = [[f"Clean jug: 5/8 in hole in the back wall {frac(CLEAN_FLOAT_Z)} in up;", "float in, set closed with the float up."],
         [f"Dirty jug: 5/8 in hole in the back wall {frac(DIRTY_FLOAT_Z)} in up;", "float in, set closed with the float down."],
         ["A 2-pin pigtail on each lead, lever connectors, a foot of slack. Meter both:", "closed in normal use. They go in series on the relay."],
         ["Clean jug cap: two 5/8 in holes, pickup tube and", "fill tube. Foot on the tube end, down to the floor."],
         ["Dirty jug cap: 1 1/2 in hole, printed funnel in."]]
yy = SY + 0.75
for i, ls in enumerate(steps):
    num(SX + 0.3, yy, i + 1)
    for j, l in enumerate(ls): text(SX + 0.8, yy + 0.1 + j * 0.42, l, 0.3)
    yy += 0.55 + 0.42 * len(ls)
num(X1 + JUG_D / 2 + 3.2, top - 0.75, 4); num(nx2 + 2.4, top2 - 1.4, 5)
num(X1 + JUG_D + 1.05 - 0.0, FLOOR - CLEAN_FLOAT_Z - 2.3, 2) if False else None

W, H = 45.0, 21.2
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="The two jugs in section with their side-mount float switches, a detail of a side-mount switch through the wall, and the steps">'
       f'<rect width="{W}" height="{H}" fill="{PAPER}"/>' + "\n".join(o) + '</svg>')
open("float.svg", "w").write(svg)
print("wrote float.svg")
