// Toddler play kitchen, hutch version: real sink and faucet, two jugs and a pump, oven with a window.
// OpenSCAD 2021.01. Units: INCHES. Frame: X across, Y front-to-back (0 = front), Z up.
//
//   part = "assembly"   everything, with the bought sink, faucet, jugs, pump and tubing ghosted in
//   part = "exploded"   same, pulled apart
//   part = "side" | "back" | "counter" | "bottom" | "tank" | "top" | "divider" | "udivider" | "door" | "ovdoor" | "oven" | "dry"
//                       one part flat on XY for a look (the cut files come from design.py, not from here)
//   (burners, knobs, toys, pickup foot, funnel and window clips are printed parts: printed.scad)
//
// Every number lives in params.scad, which design.py generates. Change design.py, rerun it, and the cut sheets follow.

include <params.scad>;
part = "assembly";
show_bought = true;      // ghost the sink, faucet, jugs, pump, rack and tubing
show_doors = true;       // false = look into the cabinets
open_angle = 0;          // 0 = doors shut; 95 = every door swung open on its hinges
show_toys = true;        // printed pan, plates and canisters
$explode = 0;            // 0 = assembled; 6 = a good exploded view
$fn = 96;

OAK   = [0.86, 0.72, 0.50];
OAK2  = [0.80, 0.65, 0.44];
WHITE = [0.95, 0.95, 0.93];        // upper doors
BLUE  = [0.80, 0.88, 0.94];        // lower doors, a very pale powder blue
STEEL = [0.75, 0.77, 0.78];
CHROME = [0.82, 0.84, 0.86];
JUG   = [0.55, 0.70, 0.90];
TUBE  = [0.55, 0.75, 0.95];

module rrect(w, h, r) { offset(r) offset(-r) square([w, h], center = true); }
module knob_hole(x, y) translate([x, y, -1]) cylinder(d = KNOB_HOLE, h = T + 2);

// ---------------------------------------------------------------- parts (each drawn flat: X = length, Y = width, Z = T)
module dado(x, y, w, h) translate([x, y, T - DADO]) cube([w, h, DADO + 1]);                      // DADO deep, into the up face
module recess(x, y, w, h) translate([x, y, T - HINGE_RECESS]) cube([w, h, HINGE_RECESS + 1]);     // 1 mm hinge-leaf recess
function hinge_z(z0, door_h) = [z0 + REVEAL + HINGE_IN, z0 + REVEAL + door_h - HINGE_IN];
// Side: X = height from the floor, Y = depth from the front, inside face up. The notch above the counter is the hutch step.
module side_p(right = false) difference() {
    cube([H, D, T]);
    translate([HC, -1, -1]) cube([H - HC + 1, NOTCH_D + 1, T + 2]);                          // the set-back above the counter
    dado(-1, -1, DADO_W + 1 - 0.005, CTR_D + 1);                                              // bottom rabbet (floor edge)
    dado(HC - T - 0.005, -1, DADO_W, CTR_D + 1);                                              // counter dado, full depth
    dado(TANK_Z - T - 0.005, NOTCH_D - 1, DADO_W, UP_SHELF_D + 1);                            // upper shelf dado
    dado(H - T - 0.005, NOTCH_D - 1, DADO_W + 1, UP_SHELF_D + 1);                             // top rabbet
    if (right) {
        dado(OVEN_Z - T - 0.005, CTR_D - SHELF_D, DADO_W, SHELF_D + 1);                       // oven floor, stopped at the front
        for (zc = concat(hinge_z(OVEN_Z, OVEN_DOOR_H), hinge_z(T, WARM_DOOR_H))) recess(zc - HINGE_L / 2 - 0.03, -1, HINGE_L + 0.06, HINGE_LEAF_W + 0.03 + 1);
    } else {
        for (zc = hinge_z(T, DOOR_H)) recess(zc - HINGE_L / 2 - 0.03, -1, HINGE_L + 0.06, HINGE_LEAF_W + 0.03 + 1);
        for (py = PEG_Y) translate([PEG_Z, py, -1]) cylinder(d = BIT, h = T + 2);                  // peg holes, through
    }
}
// Back: X = width, Y = height from the bottom, front face up. Cord hole behind the pump.
module back_p() difference() {
    cube([INNER_W, BACK_H, T]);
    translate([CORD_X - T, CORD_Z - T, -1]) cylinder(d = BIT, h = T + 2);
}
// Horizontal panels are PANEL_L long: their x = 0 sits DADO inside the left side. Divider dados on the faces that meet them.
DIVX = [SINK_BAY + DADO, SINK_BAY + T + DRY_BAY + DADO];   // divider positions from the panel's left end
DIVX_UP = [for (x = UDIV_X) x - T + DADO];                   // the three upper dividers, equally spaced
module counter_p() difference() {                           // show face DOWN in this frame: dados on top (= the underside)
    cube([PANEL_L, CTR_D, T]);
    translate([SINK_CX - T + DADO, SINK_CY, -1]) linear_extrude(T + 2) rrect(SINK_CUT, SINK_CUT, SINK_CUT_R);
    for (k = KNOBS) knob_hole(k[0] - T + DADO, k[1]);
    translate([PORT_X - T + DADO, PORT_Y, -1]) cylinder(d = PORT_D, h = T + 2);                   // fill port
    for (x = DIVX) dado(x, -1, DADO_W, CTR_D + 2);
}
module bottom_p() difference() {
    cube([PANEL_L, CTR_D, T]);
    for (x = DIVX) dado(x, -1, DADO_W, CTR_D + 2);
    translate([DIRTY_CX - T + DADO - JUG_HOLE / 2, -1, -1]) cube([JUG_HOLE, JUG_NOTCH_D + 1, T + 2]);   // notch from the front edge: the dirty jug stands on the floor and slides out
}
module tank_p() difference() { cube([PANEL_L, UP_SHELF_D, T]); for (x = DIVX_UP) dado(x, -1, DADO_W, UP_SHELF_D + 2); }   // upper shelf
module top_p()  difference() { cube([PANEL_L, UP_SHELF_D, T]); for (x = DIVX_UP) dado(x, -1, DADO_W, UP_SHELF_D + 2); }
module divider_p(which = "A") difference() {                             // flat: X = depth, Y = height (from the bottom end), LEFT face up
    cube([DIV_D, DIV_H, T]);
    if (which == "B") dado(CTR_D - SHELF_D, DRY_Z - T - (T - DADO), SHELF_D + 1, DADO_W);    // drying shelf dado
    for (zc = hinge_z(T, DOOR_H)) recess(-1, zc - (T - DADO) - HINGE_L / 2 - 0.03, HINGE_LEAF_W + 0.03 + 1, HINGE_L + 0.06);
}
module udivider_p() cube([UP_DIV_D, UP_DIV_H, T]);
module door_p(w, h, knob_x, panel = true) difference() {                 // front face is z = T
    cube([w, h, T]); knob_hole(knob_x, h / 2);
    if (panel) translate([w / 2, h / 2, T - PANEL_DEPTH]) linear_extrude(1) rrect(w - 2 * FRAME, h - 2 * FRAME, DADO_R);   // Shaker panel
}
module oven_p() cube([OVEN_L, SHELF_D, T]);
module dry_p()  cube([DRY_L, SHELF_D, T]);
// Oven door: window through, acrylic pocket on the inside face (z = 0 here), pull dimples on the inside face too.
module ovdoor_p() difference() {
    cube([OVEN_DOOR_W, OVEN_DOOR_H, T]);
    translate([OVEN_DOOR_W / 2, WIN_CZ, -1]) linear_extrude(T + 2) rrect(WIN_W, WIN_H, WIN_R);
    translate([OVEN_DOOR_W / 2, WIN_CZ, -1]) linear_extrude(1 + WIN_POCKET) rrect(ACR_W + ACR_SLACK, ACR_H + ACR_SLACK, 0.3);
    for (sx = [-1, 1]) translate([OVEN_DOOR_W / 2 + sx * HANDLE_CC / 2, HANDLE_Z, -1]) cylinder(d = MARK_D, h = 1 + HINGE_RECESS);
}
module burner_p() {   // printed drip pan + coil (printed.scad); drawn here for the assembly only
    color([0.78, 0.78, 0.8]) difference() { cylinder(d1 = BURNER_D - 0.9, d2 = BURNER_D, h = 0.45); translate([0, 0, 0.1]) cylinder(d1 = BURNER_D - 1.0, d2 = BURNER_D - 0.1, h = 0.5); }
    color([0.2, 0.2, 0.22]) translate([0, 0, 0.1]) {
        s = BURNER_D / 5;                                                                                       // the spiral scales with the pan
        for (i = [0 : 71]) { a0 = 360 * i / 24; a1 = 360 * (i + 1) / 24; r0 = (0.55 + 1.5 * i / 72) * s; r1 = (0.55 + 1.5 * (i + 1) / 72) * s;
            hull() { translate([r0 * cos(a0), r0 * sin(a0), 0]) cylinder(d = 0.26 * s + 0.05, h = 0.24, $fn = 12); translate([r1 * cos(a1), r1 * sin(a1), 0]) cylinder(d = 0.26 * s + 0.05, h = 0.24, $fn = 12); } }
        cylinder(d = 1.3 * s, h = 0.16);
    }
}
module stove_knob_p() {   // printed knob with pointer, on its bezel
    color([0.6, 0.6, 0.62]) difference() { cylinder(d = 1.97, h = 0.06); translate([0, 0, -1]) cylinder(d = 1.5, h = 2); }
    color([0.15, 0.15, 0.17]) translate([0, 0, 0.06]) { cylinder(d1 = 1.42, d2 = 1.34, h = 0.28); translate([0, 0, 0.28]) cylinder(d1 = 1.02, d2 = 0.86, h = 0.55);
        translate([0, 0, 0.28]) linear_extrude(0.5) hull() { circle(d = 0.3); translate([0.5, 0]) circle(d = 0.16); } }
}

// ---------------------------------------------------------------- placement
module ex(v) translate(v * $explode) children();
X_A = T + SINK_BAY + T;                 // divider A's right face... (A spans T+SINK_BAY .. T+SINK_BAY+T)
X_DRY = T + SINK_BAY + T;               // left face of the drying bay
X_STOVE = X_DRY + DRY_BAY + T;          // left face of the stove bay

// side_p is drawn X = height, Y = depth; rotate([0,-90,0]) stands it up (X -> Z, Z -> -X), then shift it back by T
module place_side(right) ex([right ? 1 : -1, 0, 0])
    translate([right ? W - T : 0, 0, 0]) translate([T, 0, 0]) rotate([0, -90, 0]) color(OAK)
        if (right) side_p(true); else mirror([0, 0, 1]) translate([0, 0, -T]) side_p(false);   // left side's pockets face +x
module place_back() ex([0, 1.2, 0]) translate([T, D, T]) rotate([90, 0, 0]) color(OAK2) back_p();
module place_counter() ex([0, 0, 1])   translate([T - DADO, 0, HC]) mirror([0, 0, 1]) color(OAK) counter_p();   // flipped: dados face down
module place_bottom()  ex([0, 0, -0.6]) translate([T - DADO, 0, 0]) color(OAK2) bottom_p();
module place_tank()    ex([0, 0, 1.4]) translate([T - DADO, NOTCH_D, TANK_Z - T]) color(OAK) tank_p();
module place_top()     ex([0, 0, 2.2]) translate([T - DADO, NOTCH_D, H]) mirror([0, 0, 1]) color(OAK) top_p();   // flipped: dado faces down
// divider_p is drawn left face up (+z); rotate([90,0,90]) puts +z at +x, so mirror it to face -x (the left)
module place_divider() ex([0, -0.6, 0]) {
    translate([T + SINK_BAY + T, 0, T - DADO]) mirror([1, 0, 0]) rotate([90, 0, 90]) color(OAK) divider_p("A");
    translate([X_STOVE, 0, T - DADO]) mirror([1, 0, 0]) rotate([90, 0, 90]) color(OAK) divider_p("B");
}
module place_udivider() ex([0, -0.6, 0.6]) for (i = [0 : 2])
    translate([UDIV_X[i], NOTCH_D, TANK_Z - DADO]) rotate([90, 0, 90]) color(OAK) udivider_p();
module place_pegs() ex([-1, 0, 0]) for (py = PEG_Y) translate([T, py, PEG_Z]) rotate([0, -90, 0]) color(OAK2) cylinder(d = 0.5, h = PEG_L - T + T);   // oak dowels, glued through the left side
// Fill port: printed funnel in the counter over the clean jug's neck, with its lid on; tube below to the jug cap.
module fill_port() translate([PORT_X, PORT_Y, HC]) {
    color([0.2, 0.2, 0.22]) { cylinder(d = 2.0, h = 0.12); translate([0, 0, 0.12]) cylinder(d1 = 2.0, d2 = 3.15, h = 1.0); translate([0, 0, -T - 0.8]) cylinder(d = 1.4, h = T + 0.8); }
    color([0.93, 0.9, 0.85]) translate([0, 0, 1.12]) cylinder(d = 3.3, h = 0.12);               // lid
    color(OAK2) translate([0, 0, 1.24]) { cylinder(d = 0.9, h = 0.35); translate([0, 0, 0.35]) cylinder(d1 = 1.2, d2 = 1.5, h = 0.6); }   // its knob
    color(TUBE, 0.9) translate([0, 0, -(HC - T - JUG_H)]) cylinder(d = 0.62, h = HC - T - JUG_H - T);   // tube down to the cap
}
module place_oven() ex([0.5, 0, 0.3]) translate([X_STOVE, CTR_D - SHELF_D, OVEN_Z - T]) {
    color(OAK2) oven_p();
    color([0.75, 0.75, 0.77]) translate([1.0, 2.0, T]) { for (i = [0 : 9]) translate([0, i * 0.8, 0.3]) cube([9.7, 0.08, 0.08]); for (x = [0, 9.6]) translate([x, 0, 0]) cube([0.1, 7.3, 0.4]); }   // wire oven rack
}
module place_dry()  ex([0, 0, 0.3]) translate([X_DRY, CTR_D - SHELF_D, DRY_Z - T]) color(OAK2) dry_p();
// Doors are drawn with +z toward the front; rotate([90,0,0]) at y = T (lower) or NOTCH_D + T (upper) puts the front face flush.
// hinge = "L" swings the door open about its left edge, "R" about its right edge, by open_angle degrees. The knob rides on the door.
module knob() color(OAK2) { cylinder(d = 0.8, h = 0.4); translate([0, 0, 0.4]) cylinder(d1 = 1.05, d2 = 1.3, h = 0.6); }   // 1.3 in mushroom knob
module swing(x, y, z, w, hinge) {
    if (hinge == "L") translate([x, y, z]) rotate([0, 0, -open_angle]) children();
    else translate([x + w, y, z]) rotate([0, 0, open_angle]) translate([-w, 0, 0]) children();
}
module door_at(x, y, z, w, h, knob_x, c, hinge, panel = true) swing(x, y, z, w, hinge) rotate([90, 0, 0]) { color(c) door_p(w, h, knob_x, panel); translate([knob_x, h / 2, T]) knob(); }
module place_doors() ex([0, -1.5, 0]) {
    door_at(T + REVEAL, T, T + REVEAL, DOOR_W, DOOR_H, DOOR_W - DOOR_KNOB_IN, BLUE, "L");                     // sink left, hinged on the left side
    door_at(T + REVEAL + DOOR_W + REVEAL, T, T + REVEAL, DOOR_W, DOOR_H, DOOR_KNOB_IN, BLUE, "R");           // sink right, hinged on divider A
    door_at(X_DRY + REVEAL, T, T + REVEAL, DRY_DOOR_W, DOOR_H, DOOR_KNOB_IN, BLUE, "R");                     // drying, hinged on divider B
    door_at(X_STOVE + REVEAL, T, T + REVEAL, OVEN_DOOR_W, WARM_DOOR_H, DOOR_KNOB_IN, BLUE, "R", true);    // Shaker panel, like the sink doors             // warming drawer, hinged on the right side
    swing(X_STOVE + REVEAL, T, OVEN_Z + REVEAL, OVEN_DOOR_W, "R") rotate([90, 0, 0]) {                        // oven door, hinged on the right side
        color(BLUE) ovdoor_p();
        color([0.75, 0.88, 0.97], 0.35) translate([OVEN_DOOR_W / 2, WIN_CZ, 0]) linear_extrude(ACR_T) rrect(ACR_W, ACR_H, 0.3);   // acrylic
        color(CHROME) translate([0, HANDLE_Z, T]) { for (sx = [-1, 1]) translate([OVEN_DOOR_W / 2 + sx * HANDLE_CC / 2, 0, 0]) cylinder(d = 0.45, h = 1.2);
                                                   translate([OVEN_DOOR_W / 2 - 3, 0, 1.2]) rotate([0, 90, 0]) cylinder(d = 0.5, h = 6); }   // bar pull
    }
}

module place_burners() ex([0, 0, 2]) for (b = BURNERS) translate([b[0], b[1], HC]) burner_p();
module place_knobs() ex([0, 0, 2]) for (k = KNOBS) translate([k[0], k[1], HC]) rotate([0, 0, -90]) stove_knob_p();   // printed stove knobs, pointer at OFF

// ---------------------------------------------------------------- bought parts, ghosted
module sink() color(STEEL, 0.85) translate([SINK_CX, SINK_CY, HC]) {
    difference() { linear_extrude(0.1) rrect(SINK_RIM, SINK_RIM, 1.875); translate([0, 0, -1]) linear_extrude(2) rrect(SINK_BOWL[0], SINK_BOWL[1], 1.5); }
    translate([0, 0, -SINK_BOWL[2]]) difference() {
        linear_extrude(SINK_BOWL[2]) rrect(SINK_BOWL[0], SINK_BOWL[1], 1.5);
        translate([0, 0, 0.06]) linear_extrude(SINK_BOWL[2]) rrect(SINK_BOWL[0] - 0.12, SINK_BOWL[1] - 0.12, 1.44);
    }
    translate([0, 0, -SINK_BOWL[2] - 1.6]) cylinder(d = 1.5, h = 1.6);          // basket strainer body below the bowl
}
// Single-handle bar faucet in the sink's rear-deck hole: base, riser, 7-shaped high arc forward, handle on the right.
module faucet() color(CHROME) translate([FAUCET_X, FAUCET_Y, HC + 0.1]) {
    R = 1.0; ZT = FAUCET_TOP - 0.4;
    cylinder(d = 2.0, h = 0.4);
    cylinder(d1 = 1.6, d2 = 1.2, h = 2.7);
    translate([0, 0, 2.7]) cylinder(d = 0.9, h = ZT - R - 2.7);
    translate([0, -R, ZT - R]) rotate([90, 0, 90]) rotate_extrude(angle = 90) translate([R, 0]) circle(d = 0.8);
    translate([0, -R, ZT]) rotate([90, 0, 0]) cylinder(d = 0.8, h = FAUCET_REACH - R);
    translate([0, -FAUCET_REACH, FAUCET_H + 0.5]) cylinder(d = 0.8, h = ZT - FAUCET_H - 0.5);
    translate([0, -FAUCET_REACH, FAUCET_H - 0.3]) cylinder(d1 = 0.8, d2 = 0.65, h = 0.8);
    translate([0.6, 0, 2.2]) rotate([0, 90, 0]) cylinder(d = 0.5, h = 2.7);
    translate([0, 0, -1.3]) cylinder(d = 1.3, h = 1.3);
}
module water() color(TUBE, 0.5) translate([FAUCET_X, FAUCET_Y - FAUCET_REACH, HC - SINK_BOWL[2] + 0.1]) cylinder(d = 0.25, h = FAUCET_H + SINK_BOWL[2] - 0.5);
// Bought rubber-coated wire dish rack on the drying bay counter: 7 3/4 x 11 in, long axis front to back.
module rack() color([0.3, 0.3, 0.32], 0.9) translate([X_DRY + DRY_BAY / 2, CTR_D / 2 - 0.5, HC]) {
    for (sx = [-1, 1]) translate([sx * 3.6, -5.5, 0]) cube([0.2, 11, 1.8]);
    for (i = [0 : 6]) translate([-3.8, -5.3 + i * 1.75, 0]) cube([7.6, 0.2, 1.8]);
    for (i = [0 : 1]) translate([-3.8, -5.5, 0.1 + i * 1.6]) cube([7.6, 11, 0.12]);
}
// Printed toys (printed.scad): a frying pan on the front burner, spatula by the stove, plates in the rack, canisters by the sink.
module toys() {
    color([0.2, 0.2, 0.22]) translate([BURNERS[0][0], BURNERS[0][1], HC + 0.35]) {
        difference() { cylinder(d = 4.3, h = 1.0); translate([0, 0, 0.12]) cylinder(d = 4.0, h = 1); }
        translate([0, -2.0, 0.6]) rotate([90, 0, 0]) hull() { cylinder(d = 0.6, h = 0.01); translate([0, 0.3, 2.8]) cylinder(d = 0.5, h = 0.01); }
    }
    color([0.2, 0.2, 0.22]) translate([X_STOVE - 1.4, 2.2, HC]) rotate([0, 0, 15]) { cube([1.0, 2.8, 0.1]); translate([0.3, 2.8, 0]) cube([0.4, 4.3, 0.3]); }   // spatula
    color([0.93, 0.9, 0.85]) for (i = [0 : 2]) translate([X_DRY + DRY_BAY / 2 - 1.75 + i * 1.75, CTR_D / 2 - 0.5, HC + 0.3 + 2.0]) rotate([0, 90, 0]) cylinder(d = 3.9, h = 0.2);   // plates in the rack
    for (i = [0 : 2]) color([0.93, 0.9, 0.85]) translate([T + 2.0 + i * 3.3, NOTCH_D + 4.0, TANK_Z]) {           // canisters on the first open shelf
        cylinder(d = [2.4, 2.8, 3.2][i], h = [2.8, 3.4, 4.0][i]);
        translate([0, 0, [2.8, 3.4, 4.0][i]]) color([0.35, 0.3, 0.25]) cylinder(d = [2.6, 3.0, 3.4][i], h = 0.3);
    }
}
// Two 5 gal square jugs under the sink. Clean on the left (pickup foot and float switch inside, through its cap); dirty on the
// right, standing on the floor through the hole in the bottom panel, printed funnel in its neck under the strainer.
module jug(x0, z0) color(JUG, 0.55) translate([x0, JUG_Y0, z0]) {
    difference() { linear_extrude(JUG_H) rrect_at(JUG_W, JUG_D, 0.6); translate([0.15, 0.15, 0.15]) linear_extrude(JUG_H) rrect_at(JUG_W - 0.3, JUG_D - 0.3, 0.5); }
    translate([JUG_W / 2, JUG_D - JUG_NECK_IN, JUG_H - 0.7]) cylinder(d = JUG_NECK_D + 0.3, h = 0.7);   // cap, at the back edge of the top
}
module rrect_at(w, h, r) translate([w / 2, h / 2]) rrect(w, h, r);
module jugs() {
    jug(CLEAN_X0, T);
    jug(DIRTY_X0, 0);
    color([0.2, 0.2, 0.22]) translate([DIRTY_CX, NECK_Y, JUG_H]) cylinder(d1 = 1.5, d2 = FUNNEL_D, h = 0.9);   // printed funnel in the cap
    for (f = [[CLEAN_X0 + JUG_W / 2 + 2.5, T + CLEAN_FLOAT_Z], [DIRTY_CX, DIRTY_FLOAT_Z]]) translate([f[0], JUG_Y0 + JUG_D, f[1]]) {   // side-mount float switches through the back walls
        color([0.15, 0.15, 0.15]) rotate([-90, 0, 0]) cylinder(d = 0.63, h = 0.9);                             // thread and nut outside
        color([0.9, 0.9, 0.9]) translate([0, -1.2, -0.1]) cube([0.5, 1.1, 0.35], center = true);               // float inside, hanging down (dry)
    }
}
// 12 V demand pump on the back panel behind the jugs, long axis across, feet to the back. Wiring box beside it.
module pump() {
    translate([PUMP_X0, CTR_D - PUMP_H, PUMP_Z0]) {
        color([0.25, 0.25, 0.28]) translate([0, 0, 0]) cube([PUMP_L, PUMP_H - 0.3, PUMP_W]);
        color([0.1, 0.1, 0.1]) for (x = [0.4, PUMP_L - 0.4]) for (z = [0.3, PUMP_W - 0.3]) translate([x, PUMP_H - 0.3, z]) rotate([-90, 0, 0]) cylinder(d = 0.5, h = 0.3);   // rubber feet on the back
        color([0.75, 0.75, 0.75]) for (x = [-0.6, PUMP_L]) translate([x, 0.8, PUMP_W / 2]) rotate([0, 90, 0]) cylinder(d = 0.45, h = 0.6);   // barbs
    }
    color([0.88, 0.88, 0.86]) translate([WBOX_X0, CTR_D - WBOX_D, WBOX_Z0]) cube([WBOX_W, WBOX_D, WBOX_H]);   // printed wiring box: relay and Wagos inside, over the cord hole
}
// Tubing: clean jug cap -> pump inlet (left barb); pump outlet (right barb) -> up to the faucet tee. Float lead runs with the pickup.
module tubing() color(TUBE, 0.9) {
    pin  = [PUMP_X0 - 0.6, CTR_D - PUMP_H + 0.8, PUMP_Z0 + PUMP_W / 2];
    pout = [PUMP_X0 + PUMP_L + 0.6, CTR_D - PUMP_H + 0.8, PUMP_Z0 + PUMP_W / 2];
    cap  = [CLEAN_X0 + JUG_W / 2, NECK_Y, T + JUG_H];
    hull() { translate(pin) sphere(d = 0.5); translate([cap[0], cap[1], cap[2] + 1.2]) sphere(d = 0.5); }
    hull() { translate([cap[0], cap[1], cap[2] + 1.2]) sphere(d = 0.5); translate(cap) sphere(d = 0.5); }
    hull() { translate(pout) sphere(d = 0.5); translate([FAUCET_X, FAUCET_Y, HC - 2.5]) sphere(d = 0.5); }
}

module assembly() {
    place_side(false); place_side(true);
    place_back(); place_counter(); place_bottom(); place_tank(); place_top();
    place_divider(); place_udivider(); place_oven(); place_dry();
    if (show_doors) place_doors();
    place_pegs(); fill_port();
    place_burners(); place_knobs();
    if (show_bought) { sink(); faucet(); jugs(); pump(); tubing(); water(); rack(); }
    if (show_toys) toys();
}

if (part == "assembly") assembly();
else if (part == "exploded") { $explode = 6; assembly(); }
else if (part == "side") side_p();
else if (part == "sideR") side_p(true);
else if (part == "back") back_p();
else if (part == "counter") counter_p();
else if (part == "bottom") bottom_p();
else if (part == "tank") tank_p();
else if (part == "top") top_p();
else if (part == "divider") divider_p();
else if (part == "dividerB") divider_p("B");
else if (part == "udivider") udivider_p();
else if (part == "door") door_p(DOOR_W, DOOR_H, DOOR_W - DOOR_KNOB_IN);
else if (part == "ovdoor") ovdoor_p();
else if (part == "oven") oven_p();
else if (part == "dry") dry_p();
else if (part == "faucet") faucet();
