#!/usr/bin/env python3
"""Assemble shop-sheet.html and BOM.md from design.py numbers and the fragments gen_sheets.py wrote."""
from design import *

css = open("shop-sheet.css").read()
parts_rows = open("fragments/parts.html").read()
sheets_block = open("fragments/sheets.html").read()
checklist_rows = open("fragments/checklist.html").read()
n_sheets = len(layout()); n_parts = sum(q for _, _, q, *_ in PARTS)
N_PRINTED = 52   # 4 pans, 4 coils, 4 knobs, 4 bosses, 4 bezels, 4 washers, pan, spatula, 4 plates, 3 canisters, 3 lids, 4 bushings, pickup foot, funnel, 2 cap plugs, fill port, lid, 4 window clips, wiring box and lid

# --- budget: (name, url, why, where, price, qty[, have]). Amazon prices are what was paid on 2026-10-13 (two
# orders); Home Depot prices read from the linked pages. have=True: in hand (ordered or already yours), Bought ticked.
# Every row counts in the total, the things you already had included.
HD = "https://www.homedepot.com/p/"
A = "https://www.amazon.com/dp/"
budget = [
    ("PureBond red oak plywood 3/4 in × 4 ft × 8 ft", HD + "Columbia-Forest-Products-3-4-in-x-4-ft-x-8-ft-PureBond-Red-Oak-Plywood-165956/100046409",
     "Columbia Forest Products 165956. Three sheets ripped in half make the six 48 × 48 panels on hand; the cut sheets use five. Measured 0.715 to 0.725 in; dados cut 0.735. Budget price, not read from the page.", "Home Depot", 95.00, 3, True),
    ("Red oak iron-on edge banding, 13/16 in × 50 ft", A + "B0G43Y98DV",
     "POWERTEC 72371, pre-glued (the Edge Supply roll went out of stock). About 44 ft used: every front edge of the carcass, the open shelves included, and all four edges of five doors.", "Amazon", 20.00, 1, True),
    ("Titebond III wood glue, 8 oz", HD + "Titebond-III-8-oz-Ultimate-Wood-Glue-1413/202960636", "Titebond 1413. Waterproof. Every dado gets it.", "Home Depot", 7.49, 1, True),
    ("BEHR Premium cabinet &amp; trim enamel, semi-gloss, 1 qt, light blue", HD + "BEHR-PREMIUM-1-qt-52-White-Semi-Gloss-Enamel-Interior-Exterior-Cabinet-Door-Trim-Paint-712004/312376157",
     "The five doors, in a very pale powder blue: pick a light blue at the paint desk and ask for it three steps lighter. Budget price.", "Home Depot", 23.38, 1, True),
    ("KILZ 2 primer, 1 qt", HD + "KILZ-KILZ-2-ALL-PURPOSE-1-qt-White-Interior-Exterior-Multi-Surface-Primer-Sealer-and-Stain-Blocker-20902/100144601", "KILZ 20902. One coat on the five doors before the enamel; plywood drinks paint.", "Home Depot", 12.98, 1, True),
    ("Elkay Dayton 15 in drop-in bar sink", A + "B001289TIS",
     "D115151. 15 × 15 rim, 12 × 10 × 5 bowl, 2 in drain, one 1 1/2 in faucet hole, 14 3/8 in cutout, clips included. The 5 in bowl leaves room for a 14 in jug under it. It sits 3/4 in back of centre in its bay so the drain lands over the dirty jug's neck.", "Amazon", 74.99, 1),
    ("ARCORA single-handle bar faucet, brushed nickel, with supply lines", A + "B0D7PXX12L",
     "9.3 in tall under 10 1/2 in of headroom, spout 7 in up, 5 in reach, 1.26 to 1.5 in hole. Hoses end in 1/2-14 NPSM nuts for the adapters below; if yours are 3/8 compression, use 3/8 compression × 3/8 barb fittings (B07DJ451LM) instead.", "Amazon", 43.19, 1),
    ("Niagara Tri-Max 0.5 / 1.0 / 1.5 GPM aerator", A + "B0096C2IVC",
     "Niagara Conservation N3610CH, dual thread, three click-stop flows. Run it on 0.5 so the sink never fills faster than it drains. Play water, not drinking water.", "Amazon", 8.50, 1),
    ("2 in bar sink drain with basket strainer", A + "B0G1BCT47B",
     "Phivan, stainless, fits the Elkay's 2 in drain. Hangs about 1 1/2 in under the bowl, straight over the funnel in the dirty jug. Keeney K5421 (B002JFUOBY) is the fallback.", "Amazon", 9.99, 1),
    ("1-1/2 in × 6 in sink tailpiece", A + "B000M2UJSO",
     "Plumb Pak PP905W. Already in the cart; cut it to a 1 in stub on the strainer to aim the stream into the funnel, or leave it out.", "Amazon", 5.99, 1),
    ("Plumber's putty, 9 oz", A + "B006E356S8", "Oatey 31177. Under the strainer flange.", "Amazon", 4.54, 1),
    ("Two 5 gal square water jugs, 10 × 10 × 14 in", None,
     "Yours, 2 1/4 in opening at the back edge of the top, both standing neck to the back. Clean on the left: pickup foot inside on its tube through a drilled cap, a side-mount float low on its back wall. Dirty on the right, on the floor in the notch, printed funnel in a 1 1/2 in hole in its cap. Already yours; no price to count.", "On hand", None, 2, True),
    ("ECO-WORTHY 12 V demand pump, 3.5 GPM, 45 psi, with strainer and fittings", A + "B0BVMDL77Y",
     "Model T33-12V. Its pressure switch runs it when the faucet opens and stops it when it closes; self-priming, can run dry. Use its own strainer and 1/2 in straight-thread barbs, not NPT. Screwed to the back panel behind the jugs; switch turned toward 25 psi.", "Amazon", 44.99, 1),
    ("12 V 10 A power supply, 120 W, 5.5 × 2.1 mm barrel", A + "B0D5CKC9V1",
     "Desktop supply with a barrel-to-screw-terminal adapter in the box. The pump can pull 6 A. Its plug is the adult off switch.", "Amazon", 20.98, 1),
    ("Side-mount float switch, M16, 2-pack", A + "B08B4JQHN9",
     "mxuteuk DPL-1-BK, polypropylene, both used. One through a 5/8 in hole low on the clean jug's back wall, 2 in up: it opens when the water drops below it and the pump stops before it can run dry. The other high on the dirty jug's back wall, 12 in up, set the other way: it opens when the dirty water lifts it, so the sink cannot overfill the jug. In series on the relay coil; rated 0.5 A, so they never carry the pump.", "Amazon", 5.99, 1),
    ("12 V 30 A automotive relay with socket, 5-pack", A + "B00RWV470O",
     "ESUPPORT 5-pin. Both float switches in series on the coil (85/86), supply positive to 30, pump positive off 87: clean jug empty or dirty jug full, no coil, no pump. Lies in the printed wiring box, held by two zip ties. Four spare.", "Amazon", 13.59, 1),
    ("2-pin waterproof pigtail plugs, 5 pairs", A + "B01A6LTK44",
     "MUYI, pre-wired, 4 in of 18 AWG on each half: no crimping. One pair on each float lead at the top of its jug's back wall, joined to the float wires and to the run to the wiring box with in-line lever connectors. Unplug and the jug walks away. Three pairs spare.", "Amazon", 7.59, 1),
    ("18 AWG two-conductor red/black wire, 25 ft", A + "B0G9NYN463",
     "Copper-clad aluminium, fine at 12 V and these lengths. Three runs into the wiring box: the supply pair from the barrel adapter through the cord hole (2 ft), and one pair to each jug's plug (clean about 3 ft, dirty about 2 ft). Red is the float's feed, black its return.", "Amazon", 7.99, 1, True),
    ("Lever wire connectors, 32-piece kit", A + "B0B28GQVVG",
     "XALXMAW: 18 one-in-one-out, 6 one-in-two-out, 4, 2 and 2 of the bigger splitters; 24–12 AWG. 14 used: three 1-in-2-out and three 1-in-1-out in the wiring box's labelled slots, and four 1-in-1-out at each jug where the float's leads meet its plug and the plug meets the run. Strip, lift the lever, push in, close it: no crimping.", "Amazon", 14.98, 1, True),
    ("1/2 in ID × 5/8 in OD clear vinyl tubing, 10 ft", A + "B0CYSM69DW",
     "Pickup line from the foot in the clean jug up through its cap to the pump's strainer and inlet; pump outlet to the reducer; and 9 in from the fill port down to the cap. About 7 ft used.", "Amazon", 8.99, 1),
    ("1/2 in to 3/8 in stainless barb reducer, 2-pack", A + "B088LQCQ4D",
     "Beduan 304 stainless: 1/2 in tube from the pump on one end, 3/8 in tube to the tee on the other, a clamp on each. One spare.", "Amazon", 10.99, 1),
    ("3/8 in ID × 1/2 in OD clear vinyl tubing, 10 ft", A + "B07NQSNBTG",
     "Eastman 98620, FDA-compliant PVC. About 3 ft used: reducer to tee to the two faucet adapters.", "Amazon", 7.88, 1),
    ("3/8 in stainless barb tee", A + "B08G1RJ38P",
     "Metaland 3/8 × 3/8 × 3/8. Splits the pump's outlet to both faucet supply lines so every handle position gives water.", "Amazon", 8.99, 1),
    ("3/8 in barb × 1/2 in NPT male nylon adapter, 6-pack", A + "B08G1833GN",
     "JoyTube. Screws straight into the faucet's 1/2-14 NPSM supply nuts (the hose's own cone washer seals it), 3/8 in tube on the barb. One per line, four spare.", "Amazon", 7.99, 1),
    ("SAE 6 stainless hose clamps (3/8 to 7/8 in), 10-pack", A + "B01MQCU44A",
     "Covers both tube sizes; one on every barb, nine used, one spare.", "Amazon", 11.90, 1),
    ("8 × 10 in clear cast acrylic, 1/8 in, 2-pack", A + "B0CQ2D2VCN",
     f"KAITELA, cast. It drops into the {frac(ACR_W + ACR_SLACK)} × {frac(ACR_H + ACR_SLACK)} in pocket on the oven door's inside face as it comes, film off, nothing to cut. One spare sheet.", "Amazon", 9.99, 1),
    ("Stainless cooling rack, 9.7 × 7.3 in, 2-pack", A + "B07NVBF3W7",
     "P&amp;P CHEF. One is the oven rack, on the oak oven floor behind the window. The other is a spare or a second shelf.", "Amazon", 8.29, 1),
    ("Small dish drying rack, 7.7 in wide", A + "B09SG532Q8",
     f"Rubber-footed slim rack for the drying bay counter, long axis front to back; the bay is {frac(DRY_BAY)} in wide, so anything under 8 in across works.", "Amazon", 21.69, 1),
    ("2-1/2 in stainless butt hinges, 10-pack", A + "B097QT8DF9",
     "Zorveiio, satin nickel, 66 × 38 mm, 1.4 mm leaves, screws included. Two on each of the five doors. The cabinet leaf sits flush in a 1.4 mm CNC recess, so the door leaf alone takes up the 3/32 in reveal.", "Amazon", 7.49, 1),
    ("1.3 in unfinished wood knobs, 20-pack", A + "B0CJQ4HFDR",
     "Cangder mushroom knobs, solid wood, M4 × 30 mm screws included. Four on the doors, each on a printed bushing in a 1/2 in CNC hole and centred on the stile, clear of the Shaker panel; one on the fill-port lid. Fifteen spare. The stove knobs are printed.", "Amazon", 9.99, 1),
    ("1/2 in × 36 in oak dowel", HD + "Waddell-1-2-in-x-36-in-Oak-Round-Dowel-6512U/100033232",
     "Two 3 in pegs cut from it, glued through the left side at her shoulder height: apron and hand towel. Budget price.", "Home Depot", 2.98, 1, True),
    ("6 in stainless bar pull, 96 mm centres", A + "B01A7D4LIG",
     "Pandora solid stainless. The oven door handle, above the window; the CNC dimples its two screw holes on the inside face.", "Amazon", 6.17, 1),
    ("#8-32 × 2 in stainless machine screws, 30", A + "B0G7Y5KY1R",
     "Twidec, pan head. Four hold the stove knobs: up from under the counter, through a printed washer and the knob's boss, into the nut captured in the knob.", "Amazon", 6.99, 1),
    ("#8-32 machine screw nuts, 100", A + "B000BQMMFY",
     "Hillman, zinc. One drops into the hex pocket in each stove knob before its boss is glued in.", "Amazon", 5.22, 1),
    ("#8 × 1-1/4 in flat head wood screws, 100", HD + "Everbilt-8-x-1-1-4-in-Phillips-Flat-Head-Zinc-Plated-Wood-Screw-100-Pack-801832/204275496",
     "Everbilt 801832, zinc. About 89 used: three screws through every dado joint on top of the glue, plus the back, shelves and one through each burner. Countersink them all.", "Home Depot", 7.97, 1, True),
    ("#6 × 1/2 in flat head wood screws, 100", A + "B06ZZBG6DC",
     "Rok Hardware, zinc. Four hold the oven window clips, four the pump's feet, four the wiring box to the back panel and four its lid.", "Amazon", 7.09, 1, True),
    ("3/8 in face-grain oak plugs, 100", A + "B00U0XFVEM",
     "WidgetCo. Flat plugs for the countersunk heads on the two outside faces and the top, about 36 used.", "Amazon", 15.76, 1),
    ("GE Advanced Silicone 2 kitchen &amp; bath sealant, clear, 2.8 oz", A + "B000PSE46S",
     "Bead under the sink rim and around the cutout edge; a thin bead round the acrylic in its pocket.", "Amazon", 8.52, 1),
    ("Furniture anti-tip strap kit", A + "B000FJRYAA",
     "QuakeHOLD! 4160, two 15 in nylon straps. A 45 in hutch with a toddler on the oven door is a ladder. Strap the back to a stud.", "Amazon", 11.58, 1),
    ("Sales tax on the two Amazon orders, less a $1.05 coupon", None,
     "$17.93 + $9.06 tax, −$1.05 coupon: the Amazon lines above plus this one come to the $442.70 charged. Home Depot prices are before tax.", "Amazon", 25.94, 1, True),
]
budget = [(*b, b[3] == "Amazon") if len(b) == 6 else b for b in budget]   # every Amazon row was ordered on 2026-10-13
total = sum(p * q for *_, p, q, have in budget if p)
hd_total = sum(p * q for *_, w, p, q, have in budget if w == "Home Depot" and p)
to_buy = sum(p * q for *_, p, q, have in budget if p and not have)
def money(x): return f"{x:.2f}" if x else "—"
def row(name, url, why, where, price, qty, have):
    label = f'<a href="{url}">{name}</a>' if url else name
    sub = money(price * qty if price else 0)
    box = f'<td class="box"><span class="cb">{"✓" if have else ""}</span></td>'
    return f'          <tr>{box}<td>{label}<span class="dec">{why}</span></td><td>{where}</td><td class="num">{money(price)}</td><td class="num">{qty}</td><td class="num">{sub}</td></tr>'
# Categories, in the order they print; a row goes to the first category with a keyword in its name.
CATS = [("Wood and finish", ["PureBond", "edge banding", "Titebond", "BEHR", "KILZ", "oak dowel"]),
        ("Fasteners", ["#8 × 1-1/4", "#6 × 1/2", "oak plugs"]),
        ("Doors and hardware", ["butt hinges", "wood knobs", "bar pull"]),
        ("Sink and faucet", ["Elkay", "ARCORA", "aerator", "basket strainer", "tailpiece", "Plumber", "Silicone"]),
        ("Water", ["water jugs", "demand pump", "1/2 in ID", "barb reducer", "3/8 in ID", "barb tee", "NPT male", "hose clamps"]),
        ("Electrical", ["power supply", "float switch", "relay", "pigtail", "18 AWG", "Lever wire"]),
        ("Oven, stove and dishes", ["acrylic", "cooling rack", "dish drying", "#8-32 ×", "#8-32 machine screw nuts"]),
        ("Safety", ["anti-tip"]),
        ("Tax", ["Sales tax"])]
def cat_of(name):
    for title, keys in CATS:
        if any(k in name for k in keys): return title
    raise SystemExit(f"budget row with no category: {name}")
by_cat = {t: [b for b in budget if cat_of(b[0]) == t] for t, _ in CATS}
def cat_sub(t): return sum(b[4] * b[5] for b in by_cat[t] if b[4])
budget_rows = "\n".join(
    f'          <tr class="cat"><td></td><td colspan="4">{t}</td><td class="num">{cat_sub(t):.2f}</td></tr>\n' + "\n".join(row(*b) for b in by_cat[t])
    for t, _ in CATS if by_cat[t])

PRINTED = [  # (part, qty, file, notes)
    ("Drip pan, 4 in", 4, "stl/drip_pan.stl", "Silver or light grey. Sloped wall, centre hole; the coil's screw clamps it down. About 35 g each."),
    ("Coil element", 4, "stl/coil.stl", "Black. Three-turn spiral with a 16 mm centre cap and a terminal tail, drops into the pan. One #8 × 1 1/4 in screw down through the cap holds coil and pan to the counter. About 25 g each."),
    ("Stove knob body", 4, "stl/stove_knob.stl", "Black, prints face down, pointer up. The hexagon in the face is a pocket for an 8-32 nut: drop the nut in, glue the boss over it. About 18 g each."),
    ("Knob boss", 4, "stl/knob_boss.stl", "The knob's 12.4 mm axle, prints standing. Glues into the knob face and turns in the 1/2 in counter hole; screw and washer from below. 3 g each."),
    ("Knob bezel", 4, "stl/bezel.stl", "Tick ring glued round each knob hole, OFF at the back. 5 g each."),
    ("Knob washer, 20 mm", 4, "stl/washer.stl", "Under each stove-knob screw head so it slides on the counter's underside when the knob turns. Print six, any colour."),
    ("Frying pan, 110 mm", 1, "stl/pan.stl", "Black, prints flat; the handle runs from the base so nothing hangs in the air. About 45 g."),
    ("Spatula, 180 mm", 1, "stl/spatula.stl", "Black, prints flat. About 25 g."),
    ("Plate, 100 mm", 4, "stl/plate.stl", "Light colour, for the dish rack. About 20 g each; print six if you like."),
    ("Canisters with lids, S/M/L", 3, "stl/canister-*.stl, stl/lid-*.stl", "Light colour cans, contrast lids, lids dimple-side down. They live on the first open shelf, where she can see them. About 150 g the set."),
    ("Door-knob bushing, 1/2 in OD × 3/16 bore", 4, "stl/bushing.stl", "Presses into each door's CNC'd knob hole so the wood knob's 8-32 screw runs centred. 2 g each; print five."),
    ("Fill port", 1, "stl/fill_port.stl", "Prints mouth down, no supports. An 80 mm funnel mouth standing 1 in above the counter, flange on the counter, 36 mm spout through the 1 1/2 in hole, 1/2 in barb below for the tube to the clean jug's cap. She refills the kitchen with her own pitcher. Black, about 45 g."),
    ("Fill port lid", 1, "stl/fill_lid.stl", "Prints flat, ring up. An 84 mm disc with a ring that drops into the mouth; a spare wood knob screws to it from the ring side. Any colour, 20 g."),
    ("Pump pickup foot", 1, "stl/pickup.stl", "Prints socket-side down, no supports. Slotted cup on four legs on the end of the pickup tube in the clean jug: water comes in through the slots, down the hollow cone and through a 10 mm bore into the tube. 36 mm across, so it drops through the jug's 2 1/4 in neck. Black, about 16 g."),
    ("Drain funnel", 1, "stl/funnel.stl", "Prints mouth down, no supports. 100 mm mouth, 37.5 mm spout, 52 mm flange: the spout drops into a 1 1/2 in hole drilled in the dirty jug's cap (a 1 5/8 or 1 3/4 in hole saw works too) and the mouth sits under the strainer. The neck is at the jug's back edge and the drain {frac(DRAIN_OFF)} in from it, well inside the mouth. Black, about 25 g."),
    ("Cap plug", 2, "stl/cap_plug.stl", "Prints flat. A disc with a spigot that fills the funnel hole in the dirty jug's cap: funnel out, plug in, carry the jug to the drain without a drip. One spare. Any colour, 10 g."),
    ("Wiring box", 1, "stl/wire_box.stl", "Prints floor down, no supports. 152 × 102 × 38 mm. Screws to the back panel over the cord hole on four #6 screws in a rectangle. The relay stands on the right on two zip-tie saddles; six labelled slots in the middle hold the lever connectors on their sides (GND, +12V and SERIES 1-in-2-out; PUMP+, 85 and 87a 1-in-1-out), outputs left toward the outside wires, relay leads into the single ends from the right, so nothing crosses. Three notches let the outside wires in. Slot widths are WB_LCS in printed.scad if your connectors differ. Any colour, about 100 g."),
    ("Wiring box lid", 1, "stl/wire_box_lid.stl", "Prints face down. 3 mm plate, four countersunk #6 × 1/2 into the box's corner bosses, vents over the relay coil, tongues that close the wire notches, a keeper bar that stops 1 mm in front of the connectors, 12 V on its face. About 50 g."),
    ("Oven window clip", 4, "stl/window_clip.stl", "22 × 14 × 3 mm plate, countersunk for a #6 × 1/2 screw. Four hold the acrylic in its pocket on the oven door's inside face, one per corner. Any colour, 2 g each."),
]

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mini Kitchen Shop Sheet</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap">
{css}
<style>
  figure.fig img {{ width: 100%; height: auto; display: block; border-radius: 3px; }}
  .callouts {{ grid-template-columns: repeat(3, 1fr); align-items: stretch; }}
  @media (max-width: 720px) {{ .callouts {{ grid-template-columns: repeat(2, 1fr); }} }}
  .fig-grid img {{ width: 100%; height: auto; display: block; }}
  .part-grid {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; }}
  #budget tr.cat td {{ font-family: "Barlow Condensed", sans-serif; font-weight: 600; font-size: 1.08em; letter-spacing: 0.02em; background: var(--paper-2); color: var(--ink); padding-top: 5px; padding-bottom: 3px; }}
  .part-grid figure {{ margin: 0; background: var(--paper-2); border-radius: 6px; padding: 6px 6px 8px; }}
  .part-grid img {{ width: 100%; height: auto; display: block; border-radius: 4px; }}
  .part-grid figcaption {{ font-family: "Barlow Condensed", sans-serif; font-weight: 600; font-size: 14px; text-align: center; margin-top: 4px; }}
  @media print {{ figure.fig img {{ max-height: 4.6in; width: auto; max-width: 100%; margin: 0 auto; }} #budget .tablewrap {{ break-inside: auto; }} #budget table {{ font-size: 6.9px; }} #budget td, #budget th {{ padding: 0 4px; }} #budget td .dec {{ font-size: 5.9px; line-height: 1.15; }} table.toolpaths {{ font-size: 8px; margin-bottom: 3px; }} section.no-break ul.notes {{ font-size: 8.2px; line-height: 1.3; }} section.no-break ul.notes li {{ margin-bottom: 2px; }} table.toolpaths td, table.toolpaths th {{ padding: 2px 5px; line-height: 1.25; }} table.toolpaths td .dec {{ display: inline; margin-left: 3px; font-size: 1em !important; color: var(--ink-2, #5a605c); }} .toolpath-foot {{ font-size: 8.4px; margin: 2px 0 8px; max-width: none; }} #budget tr.cat td {{ font-size: 7.6px; padding-top: 1px; padding-bottom: 0; line-height: 1.15; }} #budget td {{ line-height: 1.12; }} #budget .section-head {{ margin-bottom: 4px; }} #assembly .tablewrap {{ break-inside: auto; }} #assembly table {{ font-size: 9.5px; }} #assembly td, #assembly th {{ padding: 3px 6px; }} #assembly figure.fig img {{ max-height: 3.4in; }} #printed figure.fig img {{ max-height: 2.8in; }} ul.notes {{ font-size: 9.2px; line-height: 1.38; }} ul.notes li {{ margin-bottom: 3px; }} #checklist .tablewrap, header + section .tablewrap, #printed .tablewrap {{ break-inside: auto; }} #checklist table, #printed table {{ font-size: 8.8px; }} #checklist td, #checklist th, #printed td, #printed th {{ padding: 2px 6px; }} #checklist td.box:nth-child(2) {{ font-size: 8px; }} #finish table {{ font-size: 9.5px; }} #finish td, #finish th {{ padding: 3px 6px; }} #finish ol.steps {{ font-size: 10.5px; }} #finish ol.steps li {{ margin-bottom: 8px; }} #assembly ol.steps {{ font-size: 9.3px; line-height: 1.36; column-gap: 22px; }} #assembly ol.steps li {{ margin-bottom: 5px; }} #assembly ol.steps li b {{ font-size: 13.5px; }} #assembly figure.fig img {{ max-height: 7.6in; }} #assembly figure.fig:not(.float-fig) {{ break-before: page; page-break-before: always; }} figure.float-fig, figure.wiring-fig {{ break-before: page; page-break-before: always; }} figure.wiring-fig img {{ max-height: 6.4in !important; width: auto; }} #assembly figure.plumb-fig {{ break-before: auto !important; page-break-before: auto !important; margin-top: 18px; }} figure.plumb-fig img {{ max-height: 4.6in !important; width: auto; }} figure.box-fig img {{ width: 7in !important; height: auto !important; max-height: none !important; max-width: 100% !important; margin: 0 auto; }} figure.float-fig img {{ max-height: 6.4in !important; width: auto; }} #inside figure.fig img {{ max-height: 6.2in; }} .part-grid {{ display: grid !important; grid-template-columns: repeat(5, 1fr); gap: 8px; }} .part-grid figure {{ break-inside: avoid; page-break-inside: avoid; padding: 4px 4px 6px; }} .part-grid figcaption {{ font-size: 12px; }} #inside figcaption {{ font-size: 11px; }} .cover-img {{ max-height: 3.5in !important; }} .feature span {{ font-size: 9.8px !important; }} .cover h1 {{ font-size: 30px !important; }} header + section table {{ font-size: 8.8px; }} header + section td, header + section th {{ padding: 2px 6px; }} header + section td .dec {{ font-size: 7.8px; }} header {{ padding-bottom: 12px; }} header .spec {{ font-size: 12px; }} .callouts {{ display: grid !important; grid-template-columns: repeat(6, 1fr); gap: 8px; break-inside: avoid; }} .callout {{ float: none !important; width: auto !important; margin: 0 !important; padding: 10px 10px 8px; }} .callout .big {{ font-size: 26px; }} .callout .big small {{ font-size: 11px; }} .callout .muted {{ font-size: 8.5px; line-height: 1.3; }} .callout .eyebrow {{ font-size: 10px; }} .sheets .sheet {{ width: 23.5%; margin-right: 2%; margin-bottom: 8px; }} .sheets .sheet:nth-child(4n) {{ margin-right: 0; }} .sheet .note {{ font-size: 8.5px; }} .sheet-head h3 {{ font-size: 12px; }} .sheet-head a {{ font-size: 7.5px; }} .sheets {{ break-inside: avoid; page-break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="page">

  <section class="cover">
    <img class="cover-img" src="cover.jpg" alt="Render of the finished play kitchen: an oak plywood hutch with four open oak compartments up top, five pastel-blue lower doors including an oven door with a window and a bar handle, a stainless bar sink with a brushed-nickel faucet, a dish rack with plates and four coil burners with knobs">
    <div class="cover-text">
      <h1>Mini Kitchen</h1>
      <p class="cover-sub">A three-bay hutch for a two-year-old, in real oak plywood with open shelves up top and pale blue doors below, with a sink that really runs and a port she refills herself.</p>
      <div class="features">
        <div class="feature"><svg viewBox="0 0 48 48"><path d="M8 22h32l-3 14H11z"/><path d="M24 22V12a6 6 0 0 1 12 0v2"/><path d="M33 16v4"/><circle cx="24" cy="30" r="1.6"/></svg><b>Water that really runs</b><span>A real stainless sink and a real faucet: turn the handle and water comes out, like the big kitchen.</span></div>
        <div class="feature"><svg viewBox="0 0 48 48"><path d="M8 14h12v24H8z"/><path d="M28 14h12v24H28z"/><path d="M14 10v4M34 10v4"/><path d="M20 20h8"/><path d="M26 18l2 2-2 2"/></svg><b>Clean jug in, dirty jug out</b><span>A quiet pump drinks from a clean jug under the sink; the sink drains into a dirty one. She refills the clean jug herself through a lidded port with her own pitcher, and the pump stops itself when the clean jug is empty or the dirty one is full.</span></div>
        <div class="feature"><svg viewBox="0 0 48 48"><rect x="8" y="10" width="32" height="28"/><rect x="14" y="20" width="20" height="12"/><path d="M14 15h20"/><circle cx="16" cy="6" r="2.5"/><circle cx="32" cy="6" r="2.5"/></svg><b>An oven with a window</b><span>Side-opening door with a real acrylic window, a steel bar handle and a wire rack inside; four coil burners and four knobs that turn. Nothing ever heats up.</span></div>
        <div class="feature"><svg viewBox="0 0 48 48"><rect x="8" y="10" width="32" height="10" rx="1"/><rect x="8" y="24" width="32" height="14" rx="1"/><circle cx="24" cy="15" r="1.6"/><path d="M20 31h8"/></svg><b>A warming drawer</b><span>A second little door under the oven for the pans and the pretend leftovers.</span></div>
        <div class="feature"><svg viewBox="0 0 48 48"><path d="M6 34h36v6H6z"/><path d="M12 34V16M20 34V16M28 34V16M36 34V16"/><circle cx="16" cy="22" r="7"/></svg><b>Dishes to wash and dry</b><span>Plates, a frying pan, a spatula and three canisters, with a dish rack beside the sink.</span></div>
        <div class="feature"><svg viewBox="0 0 48 48"><rect x="8" y="6" width="32" height="36"/><path d="M8 20h32"/><path d="M24 6v14M24 20v22"/><circle cx="20" cy="13" r="1.6"/><circle cx="28" cy="13" r="1.6"/><circle cx="20" cy="31" r="1.6"/><circle cx="28" cy="31" r="1.6"/></svg><b>Her dishes where she can see them</b><span>Four open compartments up top at her eye level, so she can choose and put back without help. Everything else stays behind five doors.</span></div>
        <div class="feature"><svg viewBox="0 0 48 48"><rect x="6" y="10" width="36" height="28" rx="2"/><path d="M10 18c8-4 16 4 24 0M10 26c8-4 16 4 24 0M10 34c8-4 16 4 24 0"/><path d="M40 6l3 5a3.2 3.2 0 1 1-6 0z"/></svg><b>Oak and pale blue</b><span>Natural oak everywhere and pastel-blue Shaker doors, sealed so splashes wipe off.</span></div>
        <div class="feature"><svg viewBox="0 0 48 48"><rect x="6" y="14" width="22" height="28"/><path d="M28 18l12-6"/><path d="M40 6v36"/><path d="M6 42h34"/></svg><b>Built for a two-year-old who is growing</b><span>Counter at 23 in, shelves she can reach, two pegs for her apron and towel; rounded corners, a 12 V pump, and a strap to the wall so it cannot tip.</span></div>
      </div>
      <div class="spec">
        <span>Size <b>{frac(W)} W × {frac(D)} D × {frac(H)} H in</b></span>
        <span>Counter <b>{frac(HC)} in</b></span>
      </div>
    </div>
  </section>

  <section id="inside">
    <div class="section-head"><h2>Inside</h2></div>
    <figure class="fig"><img src="doors-open.jpg" alt="Render of the kitchen with every door open: four open compartments up top, the two water jugs and the pump under the sink, the drying cupboard shelf, the oak oven with its wire rack and the warming drawer"><figcaption>Every door open. Up top, four open compartments for her dishes. Under the sink the clean jug (left) feeds the pump on the back wall and the dirty jug (right) stands on the floor under the strainer; the oven is plain oak inside with a wire rack; the warming drawer and the drying cupboard are plain shelves behind doors. Rendered from the model with the doors swung on their hinges.</figcaption></figure>
  </section>

  <section id="budget">
    <div class="section-head">
      <h2>Budget</h2>
    </div>
    <div class="tablewrap">
      <table>
        <thead><tr><th class="box">Bought</th><th>Item</th><th>Where</th><th class="num">Each</th><th class="num">Qty</th><th class="num">Subtotal</th></tr></thead>
        <tbody>
{budget_rows}
          <tr class="total"><td></td><td>Total</td><td></td><td></td><td></td><td class="num">{total:.2f}</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <div class="section-head"><h2>Whole project</h2></div>
    <div class="callouts">
      <div class="callout"><span class="eyebrow">Plywood</span><span class="big">{n_sheets}<small>panels 48 × 48</small></span><span class="muted">Of the six on hand. S4 and S5 leave strips for door stops; the sixth panel is spare.</span></div>
      <div class="callout"><span class="eyebrow">Parts</span><span class="big">{n_parts}<small>CNC parts</small></span><span class="muted">Fourteen carcass panels in dados and rabbets, five doors. Four Shaker panels and the oven window come off the CNC too; the counter gets the sink cutout and the fill port.</span></div>
      <div class="callout"><span class="eyebrow">Printed</span><span class="big">{N_PRINTED}<small>parts</small></span><span class="muted">Four burners, four stove knobs with bezels and washers, pan, spatula, plates, canisters, four knob bushings, the pickup foot, the drain funnel, two cap plugs, the fill port and its lid, four window clips, the wiring box and its lid. No supports.</span></div>
      <div class="callout"><span class="eyebrow">Screws</span><span class="big">89<small>#8 × 1 1/4 in</small></span><span class="muted">Dados locate, glue holds, screws clamp: three per joint. Outside and top heads get oak plugs.</span></div>
      <div class="callout"><span class="eyebrow">Hardware</span><span class="big">10<small>hinges · 5 knobs · 1 pull</small></span><span class="muted">Two butt hinges per door, cabinet leaves flush in CNC recesses; wood knobs on four doors and the fill-port lid, a 6 in bar pull on the oven, two oak pegs. The stove knobs are printed.</span></div>
      <div class="callout"><span class="eyebrow">Water</span><span class="big">2<small>jugs · 2 floats</small></span><span class="muted">Clean jug to the pump to the faucet; sink to the dirty jug through a printed funnel. Two float switches cut the pump: clean jug empty, or dirty jug full.</span></div>
    </div>
  </section>

  <section class="no-break">
    <div class="section-head"><h2>Before you cut</h2></div>
    <div class="tablewrap"><table class="toolpaths">
      <thead><tr><th class="num">#</th><th>Feature (layer)</th><th>Toolpath</th><th class="num">Depth</th><th class="num">Per pass</th><th>Why this, why now</th></tr></thead>
      <tbody>
        <tr><td class="num">1</td><td>Dados and rabbets <span class="dec">blue</span></td><td>Pocket, inside the line</td><td class="num">{frac(DADO)} in</td><td class="num">1/8 in, 2 passes</td><td>First, while the sheet is one piece. The downcut flutes press the veneer down instead of tearing it up. Test one on an offcut.</td></tr>
        <tr><td class="num">2</td><td>Hinge recesses, pull dimples <span class="dec">cyan</span></td><td>Pocket</td><td class="num">{HINGE_RECESS:.3f} in (1.4 mm)</td><td class="num">1 pass</td><td>One hinge leaf deep. Measure a real hinge first: the hinge is the boss, the drawing is a suggestion.</td></tr>
        <tr><td class="num">3</td><td>Shaker panels, window pocket <span class="dec">purple</span></td><td>Pocket</td><td class="num">{frac(WIN_POCKET)} in</td><td class="num">2 passes</td><td>Four door panels and the acrylic's seat on the oven door. Shallow and on show: don't get greedy.</td></tr>
        <tr><td class="num">4</td><td>Holes <span class="dec">magenta</span></td><td>Contour inside the line</td><td class="num">through</td><td class="num">1/8 in</td><td>Every hole is 1/2 in: the 1/4 in bit circles inside it, so no tool change and no excuses.</td></tr>
        <tr><td class="num">5</td><td>Inside profiles <span class="dec">green</span></td><td>Contour inside the line</td><td class="num">through</td><td class="num">1/8 in</td><td>Sink cutout, fill-port hole, oven window. Before the outsides, so each part still holds on while its middle leaves.</td></tr>
        <tr><td class="num">6</td><td>Outside profiles <span class="dec">black</span></td><td>Contour outside the line, tabs</td><td class="num">through</td><td class="num">1/8 in</td><td>Tabs on the big panels or they go for a walk. The sides are L-shaped; Side R is Side L's mirror, on purpose.</td></tr>
        <tr><td class="num">7</td><td>Break lines <span class="dec">red</span></td><td>Contour on the line</td><td class="num">through</td><td class="num">1/8 in</td><td>Optional. Dead last if you cut them, a screw in each offcut; skip them and saw the parts out of the skeleton.</td></tr>
      </tbody>
    </table></div>
    <p class="muted toolpath-foot">Through = 0.785 in, 0.060 in into the spoilboard; tabs 0.186 in tall from the bottom of the cut, so 1/8 in of wood. The <span class="mono">cnc/</span> Carbide Create files have it all set. Before every sheet, check Z0 with paper: a wrong touch-plate thickness deepens every cut.</p>
    <ul class="notes">
      <li><b>The plywood measured 0.715 to 0.725.</b> Parts are sized to {T} in and the dados are cut {frac(DADO_W)} in wide: the thick end plus a hair. A thin spot in a dado is a glue line, a thick spot is a mallet, so the dados follow the thick reading. If a new sheet measures differently, change <span class="mono">T</span> and <span class="mono">T_MAX</span> in <span class="mono">design.py</span> and rerun.</li>
      <li><b>Cut a test dado first.</b> On offcut, pocket one 4 in dado and try a scrap from the thick end of the sheet in it. It should push in by hand with a little friction and no mallet; glue needs room. Too tight: add 0.005 to the <span class="mono">+ 0.01</span> in <span class="mono">DADO_W</span>. Too loose: take 0.005 off.</li>
      <li><b>Which face up.</b> Pockets only cut into the up face, so: both sides lie inside-face up, so they are mirror images: Side L's front edge on the left, Side R's on the right, each notch at the top front; bottom and upper shelf face up, the bottom with its front (the jug notch) at the top and so its left end on the right; counter and top FACE DOWN, the counter's front edge at the top; the back front-face up; dividers A and B LEFT face up; the three upper dividers are plain; the two sink doors, the drying door and the warming door FRONT FACE UP for their Shaker panels; the oven door INSIDE FACE UP. The sheets say it.</li>
      <li><b>Hinge recesses, ten of them.</b> 1.4 mm pockets, one leaf deep, the shape of the hinge's cabinet leaf, {frac(HINGE_LEAF_W)} × {frac(HINGE_L)} in plus a hair, flush with a front edge: two on the left side (lower-left sink door), four on the right side (oven, warming drawer), two each on dividers A and B. Each one runs 1/8 in off the front edge, so the two corners there come out square; the bit leaves the two inner corners with its 1/4 in radius. If your hinge leaf has square corners, square those two with a chisel, a few taps each; if it has 1/4 in round corners it drops straight in. The hinge sits located, and you drill through its own holes. Measure a hinge before S1 runs and set <span class="mono">HINGE_L</span> and <span class="mono">HINGE_LEAF_W</span>.</li>
      <li><b>Shaker panels.</b> The two sink doors, the drying door and the warming door under the oven get a {frac(PANEL_DEPTH)} in recessed panel inside a {frac(FRAME)} in frame, cut in the same pocket pass as the oven window; the bit leaves {frac(DADO_R)} in round inside corners, which is right on a toddler piece. Cut those four FRONT FACE UP. The knobs sit on the stile, {frac(DOOR_KNOB_IN)} in from the free edge, so their bases never bridge the step. The oven door stays flat, like an appliance, with its window.</li>
      <li><b>The oven window.</b> The opening is {frac(WIN_W)} × {frac(WIN_H)} in with {frac(WIN_R)} in corners; the pocket round it on the inside face is {frac(ACR_W + ACR_SLACK)} × {frac(ACR_H + ACR_SLACK)} in and {frac(WIN_POCKET)} in deep, so a stock 8 × 10 in sheet of 1/8 in acrylic drops in uncut. Do not try to cut acrylic with the wood bit: it melts and welds to the flutes. The pocket leaves {frac((OVEN_DOOR_W - ACR_W - ACR_SLACK) / 2)} in of full-thickness door beside it, and the hinge screws live in the door's edge at mid-thickness, well below the pocket floor. The two dimples above it are the bar pull's screw centres, {frac(HANDLE_CC)} in apart: drill them 5/32 in through from the inside after the door is painted.</li>
      <li><b>Rounded ends.</b> A stopped dado ends in a half-round of the bit, so the front corners of the two mid shelves are already rounded 1/4 in in the cut files. Do not square them up. The dividers are through-dadoed, square all round.</li>
      <li><b>The jug notch.</b> A {frac(JUG_HOLE)} in wide notch from the front edge of the bottom panel, {frac(JUG_NOTCH_D)} in deep, where the dirty jug stands on the floor: it buys the 3/4 in that lets the strainer clear the funnel ({frac(DRAIN_CLEAR)} in to spare), and because it is open to the front the full jug slides straight out with both sink doors open, no lifting. It leaves a 3/4 in slot at floor level under the doors; a loose 3/4 × 3/4 strip can sit in it. Both jugs stand with their 2 1/4 in neck to the back: the neck centre is {frac(JUG_NECK_IN)} in from the back edge, so the sink sits {frac(SINK_CY - CTR_D / 2)} in back of centre in its bay to put the drain {frac(DRAIN_OFF)} in from the dirty jug's neck, inside the funnel's {frac(FUNNEL_D)} in mouth. The cutout's back edge is {frac(CTR_D - SINK_CY - SINK_CUT / 2)} in from the back panel: enough for the rear sink clips, but check yours. The sink bay is {frac(SINK_BAY)} in wide and two 10 in jugs leave {frac(SINK_BAY - 2 * JUG_W - 0.3 - JUG_GAP)} in.</li>
      <li><b>Check the sink template.</b> The Elkay box has a paper cutout template. Lay it on the {frac(SINK_CUT)} in square in the counter file before S3 runs; the cutout is {frac(T + SINK_BAY - SINK_CX - SINK_CUT / 2)} in from divider A and the sink sits to the right and back of its bay on purpose, so the dirty jug's neck is under the drain with the clean jug beside it.</li>
      <li><b>Knob holes are 1/2 in on purpose.</b> The 1/4 in bit circles them out. On eight doors a printed bushing (1/2 in outside, 3/16 bore) presses in and the wood knob's 8-32 screw runs through it. On the counter the four printed stove knobs have their own 12.4 mm boss that is the axle in the hole; an 8-32 screw and washer from underneath hold them on and they turn.</li>
      <li><b>The fill port and the pegs.</b> A {frac(PORT_D)} in hole in the counter {frac(SINK_CX - SINK_RIM / 2 - PORT_X)} in left of the sink rim, straight over the clean jug's neck: Contour inside, through, like the cutout. The printed funnel drops in, a 9 in piece of 1/2 in tube from its barb to the second 5/8 in hole in the clean jug's cap, and the lid with its knob sits on top. Two 1/2 in holes through the left side's upper portion, {frac(PEG_Z)} in up and {frac(PEG_Y[0])} and {frac(PEG_Y[1])} in from the front: the bit circles them out, and 3 in oak pegs glue through for her apron and towel.</li>
      <li><b>The cord hole and the brick.</b> A 1/2 in hole in the back panel {frac(CORD_Z)} in up, behind the printed wiring box, which screws on over it. The pump can draw 6 A, so the supply is a 12 V 10 A brick; it stays outside, behind the kitchen, off the floor, and its plug is the adult off switch. The two float switches, a matched side-mount pair, only ever see the relay coil: the clean jug's opens on empty, the dirty jug's opens on full, and either one stops the pump.</li>
      <li><b>The faucet fits.</b> The ARCORA is 9.3 in tall; there is {frac(HEADROOM)} in between the counter and the underside of the upper shelf. The upper cabinet is only {frac(UP_D)} in deep, so the counter in front of it is open to the room.</li>
    </ul>
  </section>

  <header>
    <h1>Mini Kitchen Cut List</h1>
    <div class="spec">
      <span>Box <b>{frac(W)} × {frac(D)} × {frac(H)} in, counter at {frac(HC)}, upper cabinet {frac(UP_D)} deep</b></span>
      <span>Bays <b>sink {frac(SINK_BAY)} · drying {frac(DRY_BAY)} · stove {frac(STOVE_BAY)}</b></span>
      <span>Stock <b>{T} in red oak ply (measured 0.715 to 0.725), five 48 × 48 panels</b></span>
      <span>Bit <b>1/4 in downcut for everything</b></span>
      <span>Joinery <b>1/4 in dados and rabbets, glued and screwed</b></span>
      <span>Hold-down border <b>{frac(HOLD)} in all round</b></span>
      <span>Door reveal <b>3/32 in</b></span>
    </div>
  </header>

  <section>
    <div class="tablewrap">
      <table>
        <thead><tr><th>Part</th><th class="num">Qty</th><th class="num">Length (grain)</th><th class="num">Width</th><th>Notes</th><th>Sheet</th></tr></thead>
        <tbody>
{parts_rows}        </tbody>
      </table>
    </div>
  </section>

  <section>
    <div class="section-head">
      <h2>Sheet layouts</h2>
      <p class="muted">Four 48 × 48 panels (two 4 × 8 sheets ripped in half), drawn to scale. Parts sit 1/2 in apart inside a {frac(HOLD)} in hold-down border; the grey band is where your screws go. Red dashed lines are the break cuts: run them last, with a screw in each leftover, so the offcuts come away as rectangles. Blue outlines are dado pockets, 1/4 in deep, and the small blue rectangles at the front edges are the 1.4 mm hinge recesses; the green shape is the sink cutout; the small circles are 1/2 in holes the bit circles out. Parts marked FACE DOWN have their pockets on the underside; the dividers lie LEFT face up.</p>
    </div>
{sheets_block}
  </section>

  <section id="partgrid">
    <div class="section-head"><h2>3D Printed Parts</h2></div>
    <div class="part-grid">
      <figure><img src="previews/parts/drip_pan.png" alt="Drip pan"><figcaption>Drip pan</figcaption></figure>
      <figure><img src="previews/parts/coil.png" alt="Coil element"><figcaption>Coil element</figcaption></figure>
      <figure><img src="previews/parts/stove_knob.png" alt="Stove knob"><figcaption>Stove knob</figcaption></figure>
      <figure><img src="previews/parts/knob_boss.png" alt="Knob boss"><figcaption>Knob boss</figcaption></figure>
      <figure><img src="previews/parts/bezel.png" alt="Knob bezel"><figcaption>Knob bezel</figcaption></figure>
      <figure><img src="previews/parts/washer.png" alt="Knob washer"><figcaption>Knob washer</figcaption></figure>
      <figure><img src="previews/parts/pan.png" alt="Frying pan"><figcaption>Frying pan</figcaption></figure>
      <figure><img src="previews/parts/spatula.png" alt="Spatula"><figcaption>Spatula</figcaption></figure>
      <figure><img src="previews/parts/plate.png" alt="Plate"><figcaption>Plate</figcaption></figure>
      <figure><img src="previews/parts/canister-S.png" alt="Canister S"><figcaption>Canister S</figcaption></figure>
      <figure><img src="previews/parts/canister-M.png" alt="Canister M"><figcaption>Canister M</figcaption></figure>
      <figure><img src="previews/parts/canister-L.png" alt="Canister L"><figcaption>Canister L</figcaption></figure>
      <figure><img src="previews/parts/lid-S.png" alt="Lid S"><figcaption>Lid S</figcaption></figure>
      <figure><img src="previews/parts/lid-M.png" alt="Lid M"><figcaption>Lid M</figcaption></figure>
      <figure><img src="previews/parts/lid-L.png" alt="Lid L"><figcaption>Lid L</figcaption></figure>
      <figure><img src="previews/parts/bushing.png" alt="Knob bushing"><figcaption>Knob bushing</figcaption></figure>
      <figure><img src="previews/parts/pickup.png" alt="Pickup foot"><figcaption>Pickup foot</figcaption></figure>
      <figure><img src="previews/parts/funnel.png" alt="Drain funnel"><figcaption>Drain funnel</figcaption></figure>
      <figure><img src="previews/parts/cap_plug.png" alt="Cap plug"><figcaption>Cap plug</figcaption></figure>
      <figure><img src="previews/parts/fill_port.png" alt="Fill port"><figcaption>Fill port</figcaption></figure>
      <figure><img src="previews/parts/fill_lid.png" alt="Fill port lid"><figcaption>Fill port lid</figcaption></figure>
      <figure><img src="previews/parts/window_clip.png" alt="Window clip"><figcaption>Window clip</figcaption></figure>
      <figure><img src="previews/parts/wire_box.png" alt="Wiring box"><figcaption>Wiring box</figcaption></figure>
      <figure><img src="previews/parts/wire_box_lid.png" alt="Wiring box lid"><figcaption>Wiring box lid</figcaption></figure>
    </div>
  </section>

  <section id="assembly">
    <div class="section-head"><h2>Assembly</h2><p class="muted">Dado joinery, belt and braces: every panel edge sits 1/4 in into a pocket in its neighbour, glued with Titebond III, and then screwed through from the outside, three #8 × 1 1/4 in screws per joint, countersunk. The dado locates, the glue holds, the screws clamp it while the glue sets and keep it square when a toddler hangs off a door. Heads on the two outside faces and the top get oak plugs.</p></div>
    <div class="tablewrap"><table>
      <thead><tr><th>Joint</th><th>How</th><th class="num">Screws</th><th>Why</th></tr></thead>
      <tbody>
        <tr><td>Bottom, counter, upper shelf into the sides</td><td>Bottom in a rabbet at the floor edge, counter in a full-depth dado, upper shelf in a dado across the upper portion; glue, 3 screws through each side into each panel edge, plugged</td><td class="num">18</td><td>The panels are {frac(PANEL_L)} in long: 1/4 in into each side. Self-squaring.</td></tr>
        <tr><td>Top into the sides</td><td>Rabbet along the top of each side's upper portion, glue, 3 screws down through the top into each side, plugged</td><td class="num">6</td><td>Flush top, no end grain of the sides showing above it.</td></tr>
        <tr><td>Dividers A and B</td><td>Through dados in the bottom (top face) and counter (underside), glue; 3 screws up through the bottom into each, 2 toe-screws from inside the drying bay into the counter</td><td class="num">10</td><td>They are {frac(DIV_H)} in: the opening plus 1/4 in each end, full depth. Nothing shows on the counter.</td></tr>
        <tr><td>Upper dividers (3)</td><td>Through dados in the upper shelf and the top, glue; 3 screws up through the upper shelf and 3 down through the top into each, plugged</td><td class="num">18</td><td>Four equal open compartments, her dishes at eye level.</td></tr>
        <tr><td>Drying shelf</td><td>Stopped dado in divider B's left face, glue, 2 screws through B; left end butts divider A, 2 screws through A from the sink bay</td><td class="num">4</td><td>A's left face has the sink door's hinge recesses, so its right face stays plain and the dado went to B.</td></tr>
        <tr><td>Oven floor</td><td>Stopped dado in the right side, glue, 3 screws through the side, plugged; left end butts divider B, 2 screws through B from the drying bay</td><td class="num">5</td><td>Heads inside the drying cupboard, behind its door.</td></tr>
        <tr><td>Back</td><td>Butt joint between the sides, on the bottom panel, up to the top; glue, 6 screws through each side into its edges, plugged, and 4 each into the bottom, counter and upper shelf edges from behind</td><td class="num">24</td><td>The back is the shear panel; the strap goes through it into the wall.</td></tr>
        <tr><td>Doors (5)</td><td>Two 2 1/2 in butt hinges each, cabinet leaves flush in the 1.4 mm CNC recesses, door leaves on the door edges; stop strips glued behind</td><td class="num">20 (supplied)</td><td>Inset, 3/32 in reveal. Sink, drying and warming doors are Shaker-panelled, the oven door flat. Wood knobs on the stiles, {frac(DOOR_KNOB_IN)} in from the free edges, on printed bushings; the oven door gets the bar pull.</td></tr>
        <tr><td>Fill port, pegs</td><td>Printed funnel into the counter hole on a bead of silicone under its flange; 1/2 in tube from its barb to the clean jug's cap; two 3 in oak pegs glued through the left side, flush inside</td><td class="num">0</td><td>She refills the kitchen herself; apron and towel hang where she can reach them.</td></tr>
        <tr><td>Oven window</td><td>Acrylic in the pocket on the door's inside face on a thin bead of clear silicone, four printed clips over its corners, #6 × 1/2 screws</td><td class="num">4 (#6)</td><td>From the front the acrylic bears on the pocket shoulder, so it cannot be pushed in.</td></tr>
        <tr><td>Pump and wiring box</td><td>Pump's rubber feet screwed to the back panel behind the jugs, #6 × 1/2, long axis across; printed wiring box beside it over the cord hole, four #6 × 1/2 through its floor, four through its lid</td><td class="num">12 (#6)</td><td>Off the floor, out of the way of the jugs, barbs pointing at the jug and the faucet. Every wire joint is inside the box.</td></tr>
        <tr><td>Burners, stove knobs</td><td>Drip pan down, coil in, one #8 × 1 1/4 in screw through the coil's centre cap into the counter (7/64 pilot); nut in the knob, boss glued in, boss through the 1/2 in hole, bezel glued round it, 8-32 screw and washer from below, snug not tight</td><td class="num">4</td><td>Four knobs that turn and four burners that stay put.</td></tr>
      </tbody>
    </table></div>
    <figure class="fig"><img src="exploded.png" alt="Exploded view of the kitchen from the OpenSCAD model: the two L-shaped sides, bottom, back, counter with sink cutout, upper shelf, top, two dividers, three upper dividers, mid shelves, five doors, burners, with the sink, faucet, jugs, pump and rack ghosted in"><figcaption>Every panel, pulled apart, with the bought parts ghosted in. From the OpenSCAD model (<span class="mono">part = "exploded"</span>).</figcaption></figure>
    <figure class="fig float-fig"><img src="float.svg" alt="Section through the two jugs: the clean jug with the pickup foot on its floor and a side-mount float low on its back wall; the dirty jug with the funnel in its cap and a side-mount float high on its back wall; how a side-mount float goes in; the steps in order"><figcaption>Step 11, the jugs: one side-mount float low on the clean jug (stops the pump on empty), one high on the dirty jug (stops it on full), each on a 2-pin plug.</figcaption></figure>
    <figure class="fig plumb-fig"><img src="plumbing.svg" alt="The water run from left to right: the clean jug's drilled cap with the pickup tube and fill tube pushed through it, the pump with its strainer and barbs, the 1/2 to 3/8 reducer, the 3/8 barb tee, and two 3/8 barb by 1/2 NPT adapters screwed up into the faucet's two supply-hose nuts; close-ups of a clamped barb joint, an adapter with PTFE tape going into a hose nut, and the cap's two push-through holes"><figcaption>Step 13, the tubing: every coupler from the clean jug to the faucet, and how each kind of joint goes together.</figcaption></figure>
    <figure class="fig wiring-fig"><img src="wiring.svg" alt="Wiring: the 12 V supply's barrel adapter feeds a lever connector on the plus side and one on the ground side; plus goes to relay pin 30 and down through the clean jug's float, then the dirty jug's float, into relay coil pin 85; ground goes to coil pin 86 and the pump's black lead; relay pin 87 feeds the pump's red lead"><figcaption>Step 10, the wiring. Everything inside the dashed line lives in the printed wiring box, in its labelled connector slots. Both floats sit in series on the relay coil, so an empty clean jug or a full dirty jug stops the pump.</figcaption></figure>
    <figure class="fig box-fig"><img src="previews/wire_box_wired.png" alt="Top view of the open wiring box: relay standing on the right with its five leads going left into the connectors' single ends, 87a capped; six lever connectors in labelled slots in the middle; the pump pair down from the top notch, the supply pair up through the cord hole and the two float runs in from the bottom notches, all landing on the left, output ends; no wire crosses another"><figcaption>Step 10, inside the box, lid off, as you face it. Relay leads come in from the right, outside wires from the left, and nothing crosses. 87a is capped on purpose, and SERIES's single end stays empty.</figcaption></figure>
    <ol class="steps">
      <li><b>Dry fit, then label</b><p>Lay the left side flat, pockets up. Stand the bottom in its rabbet, the counter in its dado, the upper shelf in the dado across the upper portion, drop the top into its rabbet, then lower the right side on. Everything should seat by hand. Mark FRONT and INSIDE on every panel in pencil now; it is the last time you will see all the edges.</p></li>
      <li><b>Dividers, dry</b><p>Dividers A and B into the bottom's through dados, hinge recesses on both facing left, then the counter over them so its underside dados swallow their tops. Drying shelf into divider B's dado, oven floor into the right side's. The three upper dividers into the upper shelf, top over them. Note where the shelf screws go: through A into the drying shelf, through B into the oven floor.</p></li>
      <li><b>Glue and screw, the base</b><p>Take it apart. Glue in the left side's bottom rabbet and counter dado, the bottom's two dados, the counter's two. Rebuild in the same order with the left side flat, slide the shelves in and screw their free ends (2 screws each, countersunk, heads inside the sink bay and the drying bay), lower the right side on, clamp across the width at every panel, check the diagonals. Now the screws: pilot 7/64 in and countersink (on the two outside faces and the top, counterbore 3/8 in and 1/4 in deep so the oak plugs seat), three through each side into each panel edge, three up through the bottom into each divider, two toe-screws from the drying bay up into the counter. Let it sit an hour.</p></li>
      <li><b>Upper shelf, upper dividers, top</b><p>Glue in the sides' upper-shelf dados and top rabbets, the upper shelf's two dados and the top's. Upper shelf in, the three upper dividers in, top on. Three screws through each side into the upper shelf, three down through the top into each side and into each upper divider, three up through the upper shelf into each upper divider.</p></li>
      <li><b>Back</b><p>Lay the box on its face, back on: it sits on the bottom panel and runs to the top, cord hole low in the sink bay. Six screws through each side into its edges and four through it into each of the bottom, counter and upper shelf edges.</p></li>
      <li><b>Plug, then band</b><p>Glue a 3/8 in oak plug into every counterbore on the two outside faces and the top, grain lined up, trim flush with a flush-cut saw and a block. Then the edge banding: iron the oak banding onto every plywood edge that shows. The carcass first, as one continuous run per edge: the front edges of both sides including the step, the front edges of the top, upper shelf, counter and bottom between them, the front edges of the four dividers and both mid shelves. Then the doors, all four edges of each, before they are hung and before they are painted; the 3/32 in reveal already allows for the banding's thickness. Trim with a banding trimmer or a sharp block plane, break the corners with a sanding block.</p></li>
      <li><b>Doors and knobs</b><p>Seat each hinge's cabinet leaf in its recess and drill through the hinge's holes; screw it. Hold the door in its opening on 3/32 in shims, mark the door-edge leaf, drill through the hinge again, screw. Glue a 3/4 × 1 in offcut strip behind each door's top edge as a stop. Press a bushing into each knob hole, wood knobs on. The oven door: drill its two dimples 5/32 in through, bar pull on from the inside. Stove knobs: drop an 8-32 nut into the hex pocket in each knob's face, glue the boss over it, boss through the counter hole, bezel glued round it, 2 in screw and washer up from underneath into the nut, snug enough to turn with a little drag.</p></li>
      <li><b>Finish before the water parts go in</b><p>Everything in the Finish section happens now: poly on the carcass, primer and enamel on the doors, with the sink, faucet, pump and jugs still in their boxes. Then the window: peel the acrylic, a thin bead of clear silicone in the pocket, acrylic in, four printed clips over its corners with #6 × 1/2 screws.</p></li>
      <li><b>Pump and wiring box</b><p>The pump goes on the back panel in the sink bay, long axis across, feet to the back, {frac(PUMP_Z0)} in up, so it sits behind the jugs' shoulders: four #6 × 1/2 through its rubber feet. The printed wiring box goes right of it, and the cord hole places it: hold the box's big floor hole over the cord hole, RELAY label top right, two notches along the bottom edge and one in the top edge, edges square to the cabinet, and drive four #6 × 1/2 through its countersunk floor holes. It sits {frac(WBOX_D)} in off the back, behind the jugs, clear of the bowl and the faucet hoses. Lid off until the wiring is done.</p></li>
      <li><b>Wire the box</b><p>Two sides, and nothing crosses: the relay stands on the right and its five leads go left into the connectors' single-wire ends; every wire from outside comes in on the left and lands on their output ends. One lever connector per labelled slot, lying on its side, output end toward the label: 1-in-2-out in GND, +12V and SERIES, 1-in-1-out in PUMP+, 85 and 87a. Strip 11 mm, lift the lever, push the wire home, close it; wire each connector in your hand, then press it into its slot. <strong>Relay:</strong> into its socket, stood on the two feet at the bottom of its bay with the leads coming out between them, one small zip tie through each saddle's tunnel and round it. <strong>Relay leads</strong>, by the numbers moulded on the socket, not the colours, into the single ends: 87 to PUMP+, 86 to GND, 30 to +12V, 85 to 85, 87a alone in 87a as a cap. SERIES's single end stays empty. <strong>Pump:</strong> its pair in through the top notch beside the column, red to PUMP+, black to GND's upper output. <strong>Supply:</strong> 2 ft of the red/black wire, one end into the barrel adapter's screw terminals (red to +, black to −), the other pushed in from behind through the cord hole: black to GND's lower output, red to +12V's upper. <strong>Float runs:</strong> one length of red/black to each jug's plug, about 3 ft for the clean jug and 2 ft for the dirty. Clean, through the left bottom notch: red to +12V's lower output, black to SERIES's upper. Dirty, through the right bottom notch: red to SERIES's lower output, black to 85. The current goes +12V, clean float, SERIES, dirty float, 85, through the coil, 86, GND: both floats closed or nothing. At the far end each run meets the box-side half of its jug's 2-pin plug with two 1-in-1-out connectors. <strong>Test</strong> before the lid: plug both jugs in, water in the clean jug, plug the brick in: the relay clicks. Unplug either jug's plug: it clicks off. Lid on with four #6 × 1/2 in its corners; its tongues close the notches over the wires. The brick's plug at the wall is the off switch.</p></li>
      <li><b>Jugs, foot, funnel</b><p>Both jugs stand neck to the back, and each gets one of the two side-mount floats through a 5/8 in hole in its back wall. To fit one: lower the switch into the jug through the neck on its lead, fish the lead out through the hole from inside with a bent wire, pull the thread through, gasket on the inside under the flange, nut on the outside. (If yours has its flange at the cable end instead, it mounts from outside and the nut has to go on from inside; the dirty jug's hole is reachable through the neck, the clean jug's is not, so check before drilling.) Clean jug: hole {frac(CLEAN_FLOAT_Z)} in up; set the float so the switch is closed with the float up and opens when the water drops away (flip the float if not; a multimeter settles it). It stops the pump with about {CLEAN_FLOAT_GAL:.1f} gal left. Drill its spare cap 5/8 in for the pickup tube and a second 5/8 in for the fill tube; push the printed foot onto a 30 in piece of 1/2 in tube, through the cap, foot to the floor. Dirty jug: hole {frac(DIRTY_FLOAT_Z)} in up; set the float so the switch is closed with the float down and opens when water lifts it, about {DIRTY_FLOAT_GAL:.0f} gal: the sink stops before the jug can overflow. Drill its cap 1 1/2 in (1 5/8 or 1 3/4 in also fits the funnel), printed funnel in. Both: a 2-pin pigtail plug on each float's lead at the top of the jug's back wall, the float's two leads joined to one half with two 1-in-1-out lever connectors; the other half takes that jug's run from the wiring box (step 10) the same way. A foot of slack. Dirty jug on the floor in the notch in the bottom panel with the funnel under the strainer; 2 ft of slack in the pickup tube so the clean jug can come forward to the doors. There is {frac(DRAIN_CLEAR)} in between the strainer and the funnel rim; if your strainer hangs lower, trim the funnel's mouth.</p></li>
      <li><b>Sink, faucet, strainer</b><p>Silicone bead on the counter around the cutout, drop the sink in, tighten the clips, wipe the squeeze-out. Faucet in the rear-deck hole per its sheet, supply hoses hanging below; swap its aerator for the Tri-Max, set to 0.5 GPM. Basket strainer into the drain on plumber's putty; the tailpiece, cut to a 1 in stub, points it at the funnel.</p></li>
      <li><b>Tubing</b><p>Pickup line from the clean jug's cap to the strainer on the pump's inlet, clamp. From the pump's outlet barb a short 1/2 in tube to the big end of the stainless barb reducer, clamp, then 3/8 in tube from its small end to the tee, clamp both. From the tee's two legs, a short 3/8 tube each onto a 1/2 NPT × 3/8 barb adapter, clamp, and screw each adapter into one of the faucet's supply nuts; the washer inside the nut seals it. Two gallons in the clean jug, plug the brick in, open the faucet: the pump primes in a few seconds and the tap runs; close it and the pump stops. Lift the foot out of the water and the pump stops too.</p></li>
      <li><b>Emptying and refilling</b><p>Both sink doors open. Dirty jug: unplug its float lead, lift the funnel out of its cap, push the printed plug into the hole, slide the jug straight out on the floor through the notch, carry it to a drain, pour, plug out, funnel back in, slide it home under the strainer. Clean jug: day to day she refills it herself through the port beside the sink, a small pitcher at a time; the fill tube just drops into the cap's second hole. To take the jug out: slide it forward to the doors, unplug its float lead, lift the fill tube out, unscrew the drilled cap and lift cap, tube and foot out together (set the foot in a cup, it drips a spoonful), put the jug's own cap on and carry it. The tube stays connected to the pump the whole time.</p></li>
      <li><b>Fill port and pegs</b><p>Silicone under the funnel's flange, drop it into the counter hole, tube from its barb down into the cap's third hole, lid on with a spare wood knob screwed through it from the ring side. Cut two 3 in pegs from the oak dowel, glue them through the left side's two holes, flush on the inside, 2 1/4 in proud outside, and ease their ends with sandpaper.</p></li>
      <li><b>Strap it</b><p>Anti-tip strap from the back of the top panel to a wall stud. Then let the kid loose.</p></li>
    </ol>
  </section>

  <section id="finish">
    <div class="section-head"><h2>Finish</h2><p class="muted">Two finishes: clear polyurethane on everything oak, the open shelves and the oven included, and pale blue cabinet enamel on the five doors. The enemy is end grain and the cutout edge, which drink water. Seal them as if they were the top.</p></div>
    <div class="tablewrap"><table>
      <thead><tr><th>What</th><th>When</th><th>Why then</th></tr></thead>
      <tbody>
        <tr><td>Sand 150 then 180, ease the banded edges with a sanding block (no round-over bit: it would cut through the banding)</td><td>After plugs and banding, before any finish</td><td>An eased edge holds finish; a sharp one wears through to bare wood under small hands.</td></tr>
        <tr><td>Flood coat the sink cutout edge, the counter underside around the cutout, the jug hole, all end grain</td><td>Poly coat 1, thinned 10 percent</td><td>Thinned poly soaks into end grain instead of sitting on it.</td></tr>
        <tr><td>Three coats of poly on every oak surface, 220 scuff between coats; two more on the counter top, the cutout and the whole inside of the sink bay, floor included</td><td>Coats 1 to 5, 4 to 24 h apart per the can</td><td>Three is the minimum for a wipe-down surface; the sink bay lives under two jugs.</td></tr>
        <tr><td>Doors: one coat of primer, two of enamel, both faces and all four edges, 220 scuff between</td><td>Off the hinges, flat on blocks, after the banding</td><td>Flat doors are easy doors; a brush mark on a flat slab shows. Thin coats, or a foam roller.</td></tr>
        <tr><td>Cure</td><td>7 days before the first water, 7 before the doors are hung and handled</td><td>Dry to the touch is not cured; water on a soft film leaves white rings, fingers on soft enamel leave prints.</td></tr>
        <tr><td>Silicone under the sink rim and around the cutout edge; a thin bead round the acrylic</td><td>Installation day</td><td>Belt and braces: the poly seals the wood, the silicone keeps the water from reaching it.</td></tr>
      </tbody>
    </table></div>
    <ol class="steps">
      <li><b>Sand and ease</b><p>150 then 180 on every face, plugs flush, banding edges eased with a block, a few strokes at 45 degrees. Vacuum, then wipe with a tack cloth.</p></li>
      <li><b>Seal the thirsty parts</b><p>Brush thinned poly into the sink cutout, the jug hole, every end-grain edge, the underside of the counter and the inside of the sink bay. Let it soak, wipe the drips, let it dry.</p></li>
      <li><b>Build the film</b><p>Three thin coats over all the oak, scuffed with 220 between. Then two more on the counter, cutout, drying bay and the sink bay. The five wood knobs and the two pegs get the same three coats before they go on; the printed parts get nothing.</p></li>
      <li><b>Paint the doors</b><p>Off the hinges, flat on blocks: primer, 220, enamel, 220, enamel. All five doors pastel blue; edges too. On the Shaker doors, brush the recessed panel and its corners first, then roll the frame. A foam roller leaves no brush marks on a flat door. Keep the hinge recesses on the carcass clear of poly build-up.</p></li>
      <li><b>Wait a week, then plumb</b><p>Only after the full cure: window, silicone, sink, faucet, pump, jugs, tube. Tip the dirty jug out after play and leave the sink doors open to dry; the poly will outlast the toddler.</p></li>
    </ol>
  </section>

  <section id="printed">
    <div class="section-head"><h2>Printed parts</h2><p class="muted"><span class="mono">printed.scad</span>, millimetres, STLs in <span class="mono">stl/</span>. PLA or ASA, 0.2 mm layers, 3 walls, 15 percent infill. Every part prints in the orientation it is modelled in, with no supports. The dish rack is bought now, not printed. Tick Printed when it is off the bed and cleaned up, Fitted when it is on the kitchen.</p></div>
    <div class="tablewrap"><table>
      <thead><tr><th class="box">Printed</th><th class="box">Fitted</th><th>Part</th><th class="num">Qty</th><th>File</th><th>Notes</th></tr></thead>
      <tbody>
''' + "\n".join(f'        <tr><td class="box"><span class="cb"></span></td><td class="box"><span class="cb"></span></td><td>{n}</td><td class="num">{q}</td><td class="mono">{fl}</td><td>{note}</td></tr>' for n, q, fl, note in PRINTED) + f'''
      </tbody>
    </table></div>
  </section>


  <section id="checklist">
    <div class="section-head"><h2>Cut checklist</h2><p class="muted">Tick Cut when the part is off the CNC and measured, Holes when its pockets and holes are done. Parts with nothing but an outline show a dash.</p></div>
    <div class="tablewrap unit-check"><table>
      <thead><tr><th class="box">Cut</th><th class="box">Holes</th><th>Part</th><th class="num">Length (grain)</th><th class="num">Width</th><th>Sheet</th></tr></thead>
      <tbody>
{checklist_rows}      </tbody>
    </table></div>
  </section>

</div>
</body>
</html>
'''
open("shop-sheet.html", "w").write(html)

# --- BOM.md from the same list -------------------------------------------------------------
md = ["# Bill of materials", "",
      "Amazon prices are what was paid on 13 Oct 2026 (two orders, tax on its own line). Plywood, glue, dowel, paint, primer and #8 wood screws are Home Depot, before tax. `[x]` = in hand. Every row counts in the total, including what you already had.",
      "Polyurethane, sandpaper, PTFE thread tape and",
      "filament are assumed on hand. Generated by `gen_html.py` from the same list as the shop sheet.", "",
      "Water loop: clean jug → printed pickup foot → 1/2 in tube through the jug cap → the pump's own strainer → 12 V demand pump on the back panel → 1/2 to 3/8 barb reducer → 3/8 in tube → tee → one 1/2 NPT × 3/8 barb adapter into each faucet supply nut. Sink → basket strainer → printed funnel in the dirty jug's cap. A fill port in the counter refills the clean jug. The pressure switch runs the pump only while the tap is open; two float switches in series, through a relay, stop it when the clean jug is empty or the dirty jug is full.", "",
      "| Bought | Item | Store | Each | Qty | Subtotal | Notes |", "|:-:|---|---|---:|---:|---:|---|"]
for name, url, why, where, price, qty, have in [x for t, _ in CATS for x in ([("__cat__", t, "", "", None, 0, False)] + by_cat[t])]:
    if name == "__cat__":
        md.append(f"| | **{url}** | | | | **{cat_sub(url):.2f}** | |"); continue
    label = f"[{name}]({url})" if url else name
    md.append(f"| {'[x]' if have else '[ ]'} | {label.replace('&amp;', '&')} | {where} | {money(price)} | {qty} | {money(price * qty if price else 0)} | {why.replace('&amp;', '&')} |")
md += ["", "## Printed", "", "All in `printed.scad`, STLs in `stl/`. Black PLA or ASA unless noted.", "",
       "| Part | Qty | File | Notes |", "|---|---:|---|---|"]
for n, q, fl, note in PRINTED: md.append(f"| {n} | {q} | `{fl}` | {note} |")
md += ["", "## Total", "", "| | |", "|---|---:|", f"| Amazon | {total - hd_total:.2f} |", f"| Home Depot | {hd_total:.2f} |", f"| **Total** | **{total:.2f}** |", f"| Still to buy | {to_buy:.2f} |", ""]
open("BOM.md", "w").write("\n".join(md))
print("wrote shop-sheet.html and BOM.md, to buy", round(total, 2), "Home Depot", round(hd_total, 2), "still to buy", round(to_buy, 2))
