#!/usr/bin/env python3
"""plumbing.svg: every coupler on the water run, clean jug to faucet, and close-ups of how the joints go together."""
INK, INK2, PAPER, BOX = "#1e2422", "#5a605c", "#f8f7f3", "#eceae3"
TUBE, TUBE_E, WATER, STEEL, NYLON, BRASS, CLAMP = "#cfe3f3", "#6f8fa8", "#dbe9f6", "#b9bec2", "#efe9d8", "#c9a24a", "#8a9096"
o = []
def f(x): return f"{x:.3f}"
def text(x, y, s, size=0.3, c=INK, anchor="start", bold=False):
    o.append(f'<text x="{f(x)}" y="{f(y)}" style="font-family:Helvetica, Arial, sans-serif;font-size:{size}px;font-weight:{700 if bold else 400};fill:{c};text-anchor:{anchor}">{s}</text>')
def rect(x, y, w, h, fill, rx=0.05, sw=0.035, stroke=INK):
    o.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def tube(pts, w=0.34):
    d = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
    o.append(f'<polyline points="{d}" fill="none" stroke="{TUBE_E}" stroke-width="{f(w + 0.07)}" stroke-linejoin="round" stroke-linecap="round"/>')
    o.append(f'<polyline points="{d}" fill="none" stroke="{TUBE}" stroke-width="{f(w)}" stroke-linejoin="round" stroke-linecap="round"/>')
def barb(x, y, length, d, horizontal=True, fill=STEEL, ridges=2):
    """A barb pointing +x (or +y if not horizontal) from (x, y), ridges drawn as small cones."""
    seg = length / ridges
    for i in range(ridges):
        if horizontal:
            a = x + i * seg
            o.append(f'<polygon points="{f(a)},{f(y - d / 2)} {f(a + seg)},{f(y - d / 2 + 0.06)} {f(a + seg)},{f(y + d / 2 - 0.06)} {f(a)},{f(y + d / 2)}" fill="{fill}" stroke="{INK}" stroke-width="0.03"/>')
        else:
            a = y + i * seg
            o.append(f'<polygon points="{f(x - d / 2)},{f(a)} {f(x - d / 2 + 0.06)},{f(a + seg)} {f(x + d / 2 - 0.06)},{f(a + seg)} {f(x + d / 2)},{f(a)}" fill="{fill}" stroke="{INK}" stroke-width="0.03"/>')
def clamp(x, y, horizontal=True, d=0.5):
    if horizontal: rect(x - 0.09, y - d / 2 - 0.04, 0.18, d + 0.08, CLAMP, 0.03, 0.025)
    else: rect(x - d / 2 - 0.04, y - 0.09, d + 0.08, 0.18, CLAMP, 0.03, 0.025)
def label(x, y, lines, anchor="start", size=0.27, bold_first=True):
    for i, s in enumerate(lines):
        text(x, y + i * (size + 0.1), s, size if i else size + 0.03, INK if (i == 0 and bold_first) else INK2, anchor, bold_first and i == 0)
def leader(x1, y1, x2, y2): o.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{INK2}" stroke-width="0.025"/>')
def num(x, y, n):
    o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="0.24" fill="#2456a4"/>'); text(x, y + 0.1, str(n), 0.28, "#fff", "middle", True)

# ---------------- the run, left to right ----------------
# clean jug, cap with two holes, pickup foot, fill tube
rect(0.8, 6.9, 5.0, 5.9, WATER, 0.25)
o.append(f'<rect x="0.86" y="8.6" width="4.88" height="4.14" rx="0.2" fill="#b9d4ec" opacity="0.6"/>')
rect(2.55, 6.35, 1.6, 0.6, "#fff", 0.04)          # neck
rect(2.4, 6.05, 1.9, 0.38, "#7a7f7b", 0.06)       # drilled cap
text(3.35, 13.25, "clean jug", 0.32, INK, "middle", True)
# fill port above, tube down into the cap's first hole
o.append(f'<polygon points="1.9,1.5 4.0,1.5 3.25,2.5 2.65,2.5" fill="#333" stroke="{INK}" stroke-width="0.03"/>')
barb(2.95, 2.5, 0.5, 0.36, horizontal=False, fill="#333")
tube([(2.95, 2.9), (2.95, 7.4)])
label(4.3, 1.75, ["printed fill port", "in the counter, barb below"])
# pickup tube from the foot up through the cap's second hole to the pump
tube([(3.85, 12.2), (3.85, 5.0), (7.6, 5.0), (7.6, 9.8), (8.75, 9.8)])
o.append(f'<path d="M3.45 12.15 h0.8 v0.55 h-0.8 z" fill="#333"/>')
for i in range(4): o.append(f'<line x1="{f(3.55 + i * 0.2)}" y1="12.3" x2="{f(3.55 + i * 0.2)}" y2="12.6" stroke="#ddd" stroke-width="0.05"/>')
leader(4.3, 12.4, 6.3, 12.4); label(6.4, 12.3, ["printed pickup foot", "pushes onto the tube"])
leader(4.35, 6.2, 6.2, 6.9); label(6.3, 6.95, ["cap: two 5/8 in holes,", "tubes push through, no fitting"])
num(5.0, 4.55, 1)
text(5.4, 4.65, "1/2 in tube, 30 in", 0.26, INK2)

# pump: strainer on the inlet, barbs both ends (they come with it)
barb(8.75, 9.8, 0.6, 0.42)
clamp(9.05, 9.8)
rect(9.35, 9.15, 1.5, 1.3, "#d7dbde", 0.12)
for i in range(5): o.append(f'<line x1="{f(9.55 + i * 0.27)}" y1="9.25" x2="{f(9.55 + i * 0.27)}" y2="10.35" stroke="{INK2}" stroke-width="0.03"/>')
rect(10.85, 8.8, 5.4, 2.0, "#3a3d40", 0.15)
text(13.55, 9.7, "pump", 0.34, "#fff", "middle", True)
text(13.55, 10.15, "ECO-WORTHY T33", 0.24, "#ddd", "middle")
barb(16.25, 9.8, 0.6, 0.42)
clamp(16.55, 9.8)
label(10.1, 8.05, ["its own strainer on the inlet,", "its own 1/2 in barbs, screwed in"], "middle")
num(9.95, 11.35, 2)
text(10.35, 11.45, "strainer + barb", 0.26, INK2)

# 1/2 tube to the reducer
tube([(16.85, 9.8), (18.3, 9.8)])
clamp(18.55, 9.8)
barb(18.3, 9.8, 0.55, 0.42)
rect(18.85, 9.55, 0.35, 0.5, STEEL, 0.05)
barb(19.2, 9.8, 0.55, 0.32)
clamp(19.45, 9.8, d=0.4)
num(19.0, 11.0, 3)
label(19.0, 11.55, ["1/2 → 3/8 reducer", "big end to the pump"], "middle")

# 3/8 tube to the tee
tube([(19.75, 9.8), (21.6, 9.8)], 0.26)
barb(21.6, 9.8, 0.5, 0.32)
clamp(21.85, 9.8, d=0.4)
rect(22.1, 9.5, 0.6, 0.6, STEEL, 0.06)
barb(22.7, 9.8, 0.5, 0.32)
barb(22.4, 9.0, 0.5, 0.32, horizontal=False)   # drawn as the up leg (ridges point down; fine at this scale)
clamp(22.95, 9.8, d=0.4); clamp(22.4, 9.25, horizontal=False, d=0.4)
num(22.4, 11.0, 4)
label(22.4, 11.55, ["3/8 barb tee", "in left, out up and right"], "middle")

# two short 3/8 tubes up to the adapters
tube([(22.4, 9.0), (22.4, 7.1)], 0.26)
tube([(23.2, 9.8), (25.4, 9.8), (25.4, 7.1)], 0.26)
for x in (22.4, 25.4):
    barb(x, 6.55, 0.55, 0.32, horizontal=False, fill=NYLON)        # 3/8 barb (bottom of the adapter)
    clamp(x, 6.85, horizontal=False, d=0.4)
    rect(x - 0.34, 6.25, 0.68, 0.3, NYLON, 0.03)                   # hex
    rect(x - 0.25, 5.55, 0.5, 0.7, NYLON, 0.03)                    # 1/2 NPT thread
    for k in range(5): o.append(f'<line x1="{f(x - 0.25)}" y1="{f(5.62 + k * 0.13)}" x2="{f(x + 0.25)}" y2="{f(5.68 + k * 0.13)}" stroke="{INK2}" stroke-width="0.025"/>')
    rect(x - 0.38, 4.6, 0.76, 0.8, BRASS, 0.05)                    # faucet hose nut, lifted to show the gap
    o.append(f'<line x1="{f(x)}" y1="4.6" x2="{f(x)}" y2="2.6" stroke="#9aa0a5" stroke-width="0.22" stroke-linecap="round"/>')
    o.append(f'<line x1="{f(x)}" y1="4.6" x2="{f(x)}" y2="2.6" stroke="#cfd3d6" stroke-width="0.12" stroke-dasharray="0.08 0.06"/>')
    o.append(f'<path d="M{f(x - 0.15)} 5.48 l0.15 -0.18 l0.15 0.18" fill="none" stroke="{INK}" stroke-width="0.04"/>')   # screws up into the nut
num(23.9, 6.0, 5)
label(21.9, 5.75, ["3/8 barb × 1/2 NPT adapter", "screws up into each hose nut"], "end")
# faucet
o.append(f'<path d="M22.2 2.6 h3.4 v-0.35 h-3.4 z" fill="{STEEL}" stroke="{INK}" stroke-width="0.03"/>')
o.append(f'<path d="M23.75 2.25 v-1.4 q0 -0.5 -0.5 -0.5 h-1.0 q-0.3 0 -0.3 0.3 v0.3" fill="none" stroke="#9aa0a5" stroke-width="0.32" stroke-linecap="round"/>')
text(26.0, 1.0, "faucet", 0.32, INK, "start", True)
label(26.5, 3.15, ["its two supply hoses:", "1/2-14 nuts with a", "washer inside"], bold_first=False)
text(21.95, 3.6, "hot", 0.24, INK2, "end"); text(25.65, 3.6, "cold", 0.24, INK2, "start")
text(14.5, 0.75, "Water: clean jug → pump → reducer → tee → two adapters → the faucet's two hoses", 0.34, INK, "middle", True)

# ---------------- close-ups ----------------
def panel(x, y, w, h, title):
    rect(x, y, w, h, "#fff", 0.15, 0.03, "#c9c7c0"); text(x + 0.3, y + 0.55, title, 0.33, INK, "start", True)
PY = 14.2
# A: a barb joint
panel(0.4, PY, 9.4, 5.6, "A · every barb joint (9 of them)")
barb(1.2, PY + 2.2, 2.4, 0.7, ridges=3)
rect(0.7, PY + 1.95, 0.5, 0.5, STEEL, 0.04)
o.append(f'<rect x="2.0" y="{f(PY + 1.72)}" width="3.6" height="0.96" rx="0.1" fill="{TUBE}" stroke="{TUBE_E}" stroke-width="0.04" opacity="0.75"/>')
rect(2.55, PY + 1.6, 0.42, 1.2, CLAMP, 0.05, 0.03)
o.append(f'<circle cx="2.76" cy="{f(PY + 1.45)}" r="0.14" fill="{CLAMP}" stroke="{INK}" stroke-width="0.03"/>')
leader(3.4, PY + 2.2, 3.4, PY + 3.15); text(3.4, PY + 3.4, "tube past the last ridge", 0.24, INK2, "middle")
leader(2.76, PY + 1.3, 3.6, PY + 1.05); text(3.7, PY + 1.12, "clamp over the ridges", 0.24, INK2)
steps = ["1  Slide the clamp onto the tube first.",
         "2  Dip the tube end in hot water for 30 s.",
         "3  Push it on past the last ridge, wiggling.",
         "4  Clamp over the ridges, screw snug. Not on bare tube."]
for i, s in enumerate(steps): text(0.8, PY + 3.95 + i * 0.4, s, 0.27, INK)
# B: adapter into a hose nut
panel(10.2, PY, 9.4, 5.6, "B · adapter into a faucet hose (2 of them)")
cx = 11.6
rect(cx - 0.45, PY + 0.95, 0.9, 1.0, BRASS, 0.06)
o.append(f'<rect x="{f(cx - 0.32)}" y="{f(PY + 1.62)}" width="0.64" height="0.1" fill="#333"/>')
o.append(f'<line x1="{f(cx)}" y1="{f(PY + 0.95)}" x2="{f(cx)}" y2="{f(PY + 0.75)}" stroke="#9aa0a5" stroke-width="0.25"/>')
rect(cx - 0.3, PY + 2.15, 0.6, 0.8, NYLON, 0.04)
for k in range(5): o.append(f'<line x1="{f(cx - 0.3)}" y1="{f(PY + 2.24 + k * 0.14)}" x2="{f(cx + 0.3)}" y2="{f(PY + 2.31 + k * 0.14)}" stroke="#7aa5d6" stroke-width="0.05"/>')
rect(cx - 0.42, PY + 2.95, 0.84, 0.32, NYLON, 0.03)
barb(cx, PY + 3.27, 0.7, 0.36, horizontal=False, fill=NYLON)
leader(cx + 0.5, PY + 1.45, 13.0, PY + 1.25); text(13.1, PY + 1.32, "hose nut, washer inside: it seals", 0.24, INK2)
leader(cx + 0.35, PY + 2.5, 13.0, PY + 2.35); text(13.1, PY + 2.42, "1/2 NPT thread, PTFE tape (blue)", 0.24, INK2)
leader(cx + 0.45, PY + 3.1, 13.0, PY + 3.15); text(13.1, PY + 3.22, "hex: the wrench goes here", 0.24, INK2)
steps = ["1  Three wraps of PTFE tape, clockwise looking at the thread end.",
         "2  Thread the adapter up into the hose nut by hand.",
         "3  Then about 1/4 turn with a wrench. Tape and washer seal it; don't crank.",
         "4  Push the 3/8 tube on, clamp (A)."]
for i, s in enumerate(steps): text(10.6, PY + 4.3 + i * 0.36, s, 0.25, INK)
# C: no coupler at the cap
panel(20.0, PY, 9.6, 5.6, "C · the cap: no couplers")
rect(21.0, PY + 1.6, 3.2, 0.5, "#7a7f7b", 0.06)
for xx in (21.8, 23.4):
    tube([(xx, PY + 0.9), (xx, PY + 3.3)])
text(21.8, PY + 3.75, "fill", 0.24, INK2, "middle"); text(23.4, PY + 3.75, "pickup", 0.24, INK2, "middle")
lines = ["The 5/8 in OD tube pushes straight", "through the 5/8 in holes in the cap,", "snug. To take the jug out, lift the", "fill tube and unscrew the cap: the", "pickup comes with it."]
for i, s in enumerate(lines): text(24.6, PY + 1.3 + i * 0.36, s, 0.25, INK)
text(20.4, PY + 4.6, "Clamps: SAE 6, fit both tube sizes. 9 used, 1 spare.", 0.25, INK2)
text(20.4, PY + 4.98, "Tubing: 1/2 in to the reducer, 3/8 in after it.", 0.25, INK2)

W, H = 30.0, 20.0
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Every coupler on the water run, clean jug to faucet">'
       f'<rect width="{W}" height="{H}" fill="{PAPER}"/>' + "\n".join(o) + '</svg>')
open("plumbing.svg", "w").write(svg)
print("wrote plumbing.svg")
