include <printed.scad>   // the wired-box figure in the sheet; render.sh draws it
// Lid off, relay and lever connectors in place, wires roughly routed. Box coordinates, mm.
F = WB_FLOOR; WZ = F + 6;
function c(i) = wb_slot_v(i) + (WB_LCS[i][0] + LC_GAP) / 2;
L = WB_COL_U; R = WB_COL_U + LC_L;                        // outputs left, single end right
module wire(pts, col) color(col) for (k = [0 : len(pts) - 2]) hull() { translate(pts[k]) sphere(d = 2.2, $fn = 10); translate(pts[k + 1]) sphere(d = 2.2, $fn = 10); }
module lc(i) {
    w = WB_LCS[i][0];
    translate([L, wb_slot_v(i) + LC_GAP / 2, F]) {
        color([0.62, 0.63, 0.64]) cube([LC_L, w, LC_H - 1.5]);
        color([1, 0.45, 0.12]) translate([LC_L - 11, w / 2 - 2.5, LC_H - 2]) cube([10, 5, 2]);              // single-end lever, right
        for (k = [0 : (w > 10 ? 1 : 0)]) color([1, 0.45, 0.12])
            translate([1, (w > 10 ? 1.5 + k * 5.5 : w / 2 - 2.5), LC_H - 2]) cube([10, (w > 10 ? 4.5 : 5), 2]);   // output levers, left
    }
}
function out(i, k) = [L, c(i) + (WB_LCS[i][0] > 10 ? (k == 0 ? 2.75 : -2.75) : 0), WZ];   // k = 0 upper port, 1 lower
function sgl(i) = [R, c(i), WZ];
color([0.93, 0.93, 0.91]) wire_box();
RU = WB_RELAY[0]; RV = WB_RELAY[1];
color([0.15, 0.15, 0.17]) translate([RU + 1, RV + 20, F + 3]) cube([28, 27, 28]);   // relay
color([0.25, 0.25, 0.27]) translate([RU + 2, RV, F + 3]) cube([26, 20, 24]);        // socket, leads out the bottom
for (i = [0 : len(WB_LCS) - 1]) {
    lc(i);
    color([0.1, 0.1, 0.1]) translate([L - 2, c(i), F + 0.8]) linear_extrude(0.5) text(WB_LCS[i][1], size = 3.4, font = "Liberation Sans:style=Bold", halign = "right", valign = "center");
}
color([0.1, 0.1, 0.1]) translate([RU - 6, RV + WB_RELAY[3] + 3, F + 0.8]) linear_extrude(0.5) text("RELAY", size = 3.6, font = "Liberation Sans:style=Bold");
RED = [0.85, 0.15, 0.12]; BLK = [0.12, 0.12, 0.12]; ORG = [0.95, 0.55, 0.1]; BLU = [0.15, 0.35, 0.75]; GRY = [0.6, 0.6, 0.6]; YEL = [0.9, 0.8, 0.1];
// relay socket leads, nested so none cross: the ones going up turn left at descending heights into lanes beside the column,
// the two going down drop straight past them
module up(x, vh, lane, i, col) wire([[x, RV + 2, F + 14], [x, vh, WZ], [lane, vh, WZ], [lane, c(i), WZ], sgl(i)], col);
module dn(x, i, col) wire([[x, RV + 2, F + 14], [x, c(i), WZ], sgl(i)], col);
up(RU + 8, 34, R + 8, 0, ORG);     // 87 -> PUMP+
up(RU + 11.5, 31.5, R + 6, 1, BLK);// 86 -> GND
up(RU + 15, 29, R + 4, 2, RED);    // 30 -> +12V
dn(RU + 18.5, 4, BLU);             // 85 -> 85
dn(RU + 22, 5, GRY);               // 87a -> 87a, capped
// pump pair in through the top notch beside the column: red to PUMP+, black to GND's upper output
PN = WB_NOTCH[2][0];
wire([[PN + 1.5, WB_H + 6, WB_D - 6], [PN + 1.5, WB_H - 6, WB_D - 8], [PN + 1.5, 90, WZ], [PN + 1.5, out(0, 0)[1], WZ], out(0, 0)], RED);
wire([[PN - 1.5, WB_H + 6, WB_D - 6], [PN - 1.5, WB_H - 6, WB_D - 8], [PN - 1.5, 90, WZ], [PN - 1.5, out(1, 0)[1], WZ], out(1, 0)], BLK);
// supply pair up through the cord hole: black to GND's lower output, red to +12V's upper
wire([[WB_CORD[0] + 1.5, WB_CORD[1], F], [WB_CORD[0] + 1.5, WB_CORD[1] - 3, WZ], [WB_CORD[0] + 1.5, out(1, 1)[1], WZ], out(1, 1)], BLK);
wire([[WB_CORD[0] - 2, WB_CORD[1], F], [WB_CORD[0] - 2, WB_CORD[1] - 3, WZ], [WB_CORD[0] - 2, out(2, 0)[1], WZ], out(2, 0)], RED);
// float runs in through the bottom notches: clean red to +12V's lower output, clean black and dirty red to SERIES, dirty black to 85
CN = WB_NOTCH[0][0]; DN = WB_NOTCH[1][0];
module run(u, i, k, col) wire([[u, -6, WB_D - 6], [u, 6, WB_D - 8], [u, 10, WZ], [u, out(i, k)[1], WZ], out(i, k)], col);
run(CN - 1.5, 2, 1, RED); run(CN + 1.5, 3, 0, BLK); run(DN - 1.5, 3, 1, RED); run(DN + 1.5, 4, 0, BLK);
// callouts, in the margin right of the box, leader lines drawn over everything
NAVY = [0.1, 0.2, 0.45]; CZ = 45;
module callout(from, v_text, l1, l2) color(NAVY) {
    translate([from[0], from[1], CZ]) cylinder(d = 2.4, h = 0.5, $fn = 16);
    hull() { translate([from[0], from[1], CZ]) cylinder(d = 0.7, h = 0.5, $fn = 8); translate([WB_W + 4, from[1], CZ]) cylinder(d = 0.7, h = 0.5, $fn = 8); }
    hull() { translate([WB_W + 4, from[1], CZ]) cylinder(d = 0.7, h = 0.5, $fn = 8); translate([WB_W + 4, v_text, CZ]) cylinder(d = 0.7, h = 0.5, $fn = 8); }
    hull() { translate([WB_W + 4, v_text, CZ]) cylinder(d = 0.7, h = 0.5, $fn = 8); translate([WB_W + 7, v_text, CZ]) cylinder(d = 0.7, h = 0.5, $fn = 8); }
    translate([WB_W + 9, v_text + 0.8, CZ]) linear_extrude(0.5) text(l1, size = 4, font = "Liberation Sans:style=Bold", valign = "bottom");
    translate([WB_W + 9, v_text - 1.2, CZ]) linear_extrude(0.5) text(l2, size = 3.3, font = "Liberation Sans", valign = "top");
}
callout([R - 3, wb_slot_v(5) + 1.2], 14, "87a: capped on purpose", "live at +12 V when the relay is off");
callout([R - 3, wb_slot_v(3) + 2.4], 40, "SERIES: single end not used", "both float wires join on the left");
