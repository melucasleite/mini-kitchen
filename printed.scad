// 3D-printed parts for the play kitchen. OpenSCAD 2021.01. Units: MILLIMETRES (export straight to STL).
//
//   part = "drip_pan"    4 in drip pan, print 4 in silver or light grey. Coil drops into it.
//   part = "coil"        three-turn spiral element with a tall centre cap, print 4 in black. Flat, no supports. One #8 x 1 1/4 in
//                        screw through the cap holds coil and pan to the counter.
//   part = "burner"      pan + coil together, for a look
//   part = "stove_knob"  stove knob body, prints face down, no supports. Print 4 in black.
//   part = "knob_boss"   the knob's 12.4 mm axle, prints standing, glues into the body. Print 4.
//   part = "bezel"       tick ring glued round each knob hole. Print 4.
//   part = "rack"        (no longer used: the drying rack is a bought rubber-coated one)
//   part = "pan"         toy frying pan, 110 mm dish with a 70 mm handle, prints flat, no supports
//   part = "canister"    kitchen canister; size = "S" | "M" | "L" (60 / 70 / 80 mm across). Print 3 in a light colour.
//   part = "lid"         push-on lid for the canister of the same size; print in a contrast colour
//   part = "spatula"     toy turner, 180 mm, prints flat, no supports. Black.
//   part = "plate"       100 mm plate with a rim, fits between the rack fins. Print 4 to 6, light colour.
//   part = "bushing"     knob-screw bushing: 1/2 in OD, 3/16 in bore, presses into the bit-sized knob holes. Print 5.
//   part = "washer"      20 mm washer for the stove-knob screws, 2 mm thick, 4.6 mm bore. Print 4 (print 6).
//   part = "pickup"      pump pickup foot: sits on the clean jug's floor on the end of the 1/2 in ID pickup tube, keeps the inlet off the
//                        floor and the toys out. 36 mm across, passes the jugs' 2 1/4 in neck. Prints socket down, no supports. Black.
//   part = "funnel"      sits in the dirty jug's cap hole under the sink strainer: 100 mm mouth, 37.5 mm spout, 52 mm flange: fits a 1 1/2 to 1 3/4 in cap hole. Prints mouth down. Black.
//   part = "window_clip" 22 x 14 x 3 mm plate, one #6 x 1/2 screw: four hold the oven window's acrylic in its pocket. Print 4.
//   part = "cap_plug"    plugs the funnel hole in the dirty jug's cap while you carry it to the drain. Print 2.
//   part = "fill_port"   the refill funnel: 80 mm mouth above the counter, 36 mm spout through the 1 1/2 in counter hole, 1/2 in
//                        tube barb below, to the clean jug's cap. Prints mouth down, no supports. Black.
//   part = "fill_lid"    lid for the port: 84 mm disc with a ring that drops into the mouth; a spare wood knob screws to it. Prints ring up.
//   part = "hinge_shim"  65.5 x 18.6 mm shim for a hinge recess cut too deep; shim_t = recess depth - 1.4 mm. stl/hinge-shims/ has
//                        0.4 to 1.6 mm. Prints flat.
//   part = "wire_box"    wiring box, 152 x 102 x 38 mm: screws to the back panel over the cord hole; relay standing on zip-tie saddles
//                        on the right, six labelled slots for XALXMAW lever connectors (three 1-in-2-out, three 1-in-1-out) in the
//                        middle, outside wires in on the left. Prints floor down, no supports.
//   part = "wire_box_lid" its lid, 3 mm, four #6 x 1/2 screws in the corners, vents over the relay. Prints face down.
//   part = "hole_cover"  snap-in cover for a 1 1/2 in sink faucet hole. Not needed in the faucet version of the
//                        kitchen (the faucet lives in that hole); kept for a push-button-spigot build.
//
// Numbers that matter: BURNER_D matches BURNER_D in design.py (4 in); HOLE_D is the Elkay faucet hole (1 1/2 in);
// SINK_T is 23 ga stainless, the snap ring lands just under it.

part = "burner";
size = "M";              // canister / lid size
$fn = 96;

BURNER_D = 4 * 25.4;      // 101.6 mm
BURNER_T = 6;             // base disc thickness
RING_W = 5; RING_H = 3;   // coil rings
RING_PITCH = 11;
RIM = 4;                  // flat rim outside the last ring

HOLE_D = 1.5 * 25.4;      // 38.1 mm faucet hole
SINK_T = 0.7;             // sink metal
CAP_D = 46; CAP_T = 2.5;  // cap that sits on the sink rim
STEM_CLEAR = 0.5;         // stem diameter under the hole
SNAP_LIP = 0.9;           // how far the snap bumps stand proud of the stem
STEM_L = 7;
SLOTS = 4;

// Burner, two prints: a drip pan (silver or light grey) and a coil element (black) that drops into it.
DP_OD = 4 * 25.4; DP_FLOOR = 2.4; DP_H = 11; DP_HOLE = 22;         // drip pan: 101.6 mm, sloped wall, 91.6 mm floor
COIL_W = 6.5; COIL_H = 6; COIL_R0 = 13; COIL_R1 = 40; COIL_TURNS = 3;  // flat spiral, round-ish section, 2.5 mm between turns; outer edge at 43 mm on the 46 mm pan floor
HUB_H = 16; HEAD_CB = 2.5;                                             // centre cap height and countersink depth: 16 + 2.4 pan floor - 2.5 = 15.9 mm under the head, 0.62 in
DP_NOTCH = 10;   // notch in the rim for the coil's terminal tail, like a real drip pan
module drip_pan() difference() {
    cylinder(d1 = DP_OD - 10, d2 = DP_OD, h = DP_H);                                              // wall leans out 23 degrees: prints fine
    translate([0, 0, DP_FLOOR]) cylinder(d1 = DP_OD - 10 - 2 * 1.6, d2 = DP_OD - 2 * 1.6, h = DP_H);
    translate([0, 0, -1]) cylinder(d = DP_HOLE, h = DP_FLOOR + 2);                                // centre hole, like the real thing
    translate([DP_OD / 2 - 12, -DP_NOTCH / 2, DP_FLOOR + COIL_H * 0.35]) cube([20, DP_NOTCH, DP_H]);   // terminal notch, floor stays whole under it
}
module coil() {
    n = 48 * COIL_TURNS;
    for (i = [0 : n - 1]) {
        a0 = 360 * i / 48; a1 = 360 * (i + 1) / 48;
        r0 = COIL_R0 + (COIL_R1 - COIL_R0) * i / n; r1 = COIL_R0 + (COIL_R1 - COIL_R0) * (i + 1) / n;
        hull() {
            translate([r0 * cos(a0), r0 * sin(a0), 0]) coil_section();
            translate([r1 * cos(a1), r1 * sin(a1), 0]) coil_section();
        }
    }
    difference() {   // centre cap: tall enough that a #8 x 1 1/4 in screw through it bites 0.6 in into the counter and no more
        cylinder(d1 = 2 * COIL_R0 + COIL_W, d2 = 2 * COIL_R0 + COIL_W - 4, h = HUB_H);
        translate([0, 0, -1]) cylinder(d = 4.8, h = HUB_H + 2);                                          // screw bore
        translate([0, 0, HUB_H - HEAD_CB]) cylinder(d1 = 5, d2 = 10, h = HEAD_CB + 0.01);                 // countersink for the flat head
    }
    hull() { translate([COIL_R1, 0, 0]) coil_section(); translate([DP_OD / 2 - 2, 0, 0]) coil_section(); }   // terminal tail out through the pan's notch
}
module coil_section() { cylinder(d = COIL_W, h = COIL_H * 0.55, $fn = 24); translate([0, 0, COIL_H * 0.55]) cylinder(d1 = COIL_W, d2 = COIL_W * 0.55, h = COIL_H * 0.45, $fn = 24); }
module burner() { drip_pan(); translate([0, 0, DP_FLOOR]) coil(); }   // both, for a look

// Stove knob, two prints and no supports: the body prints face down (pointer up); the boss is a separate 12.4 mm plug that
// glues into a socket in the face and turns in the 1/2 in counter hole. An 8-32 nut drops into the hex pocket before the boss
// is glued in; the screw comes up from under the counter with a washer.
KNOB_D = 36; KNOB_SKIRT = 7; KNOB_GRIP_D = 26; KNOB_GRIP_H = 14; BOSS_D = 12.4; BOSS_L = 24; NUT_AF = 8.8; NUT_T = 3.4; SOCKET_H = 6;
module stove_knob() difference() {
    union() {
        cylinder(d1 = KNOB_D, d2 = KNOB_D - 2, h = KNOB_SKIRT);
        translate([0, 0, KNOB_SKIRT]) cylinder(d1 = KNOB_GRIP_D, d2 = KNOB_GRIP_D - 4, h = KNOB_GRIP_H);
        translate([0, 0, KNOB_SKIRT]) linear_extrude(KNOB_GRIP_H - 1) hull() { circle(d = 8); translate([KNOB_D / 2 - 5, 0]) circle(d = 4); }   // pointer
    }
    translate([0, 0, -1]) cylinder(d = BOSS_D + 0.3, h = SOCKET_H + 1);                                   // socket for the boss, from the face
    translate([0, 0, SOCKET_H - 0.01]) cylinder(d = NUT_AF / cos(30), h = NUT_T, $fn = 6);                  // nut pocket above the socket
    translate([0, 0, -1]) cylinder(d = 4.6, h = KNOB_SKIRT + KNOB_GRIP_H - 4);                             // screw bore, blind
}
module knob_boss() difference() {   // prints standing up
    cylinder(d = BOSS_D, h = BOSS_L);
    translate([0, 0, -1]) cylinder(d = 4.6, h = BOSS_L + 2);
}
// Knob bezel: a thin ring glued around the hole with OFF and three heat ticks, so the pointer has something to point at.
module bezel() difference() {
    union() {
        cylinder(d = 50, h = 1.6);
        for (a = [-135, -45, 45, 135]) rotate(a) translate([19, -1, 1.6]) cube([5, 2, 1.2]);          // ticks
        rotate(180) translate([19, -2.5, 1.6]) cube([5, 5, 1.2]);                                      // OFF mark, wider, at the back
    }
    translate([0, 0, -1]) cylinder(d = KNOB_D + 2, h = 4);
}

// Cap face down on the bed, stem up. The stem is split into SLOTS fingers; each finger carries a snap bump that
// pops through the hole and holds under the sink metal.
module hole_cover() {
    stem_d = HOLE_D - STEM_CLEAR;
    difference() {
        union() {
            cylinder(d = CAP_D, h = CAP_T);
            translate([0, 0, CAP_T - 0.01]) cylinder(d1 = CAP_D, d2 = CAP_D - 2 * CAP_T, h = 0.01);   // keeps the cap edge crisp in the preview
            translate([0, 0, CAP_T]) difference() {
                union() {
                    cylinder(d = stem_d, h = STEM_L);
                    translate([0, 0, SINK_T + 0.4]) cylinder(d1 = stem_d, d2 = stem_d + 2 * SNAP_LIP, h = 1.2);     // snap bump, ramp side first
                    translate([0, 0, SINK_T + 1.6]) cylinder(d1 = stem_d + 2 * SNAP_LIP, d2 = stem_d, h = 2.5);
                }
                translate([0, 0, -1]) cylinder(d = stem_d - 2 * 1.6, h = STEM_L + 2);                       // hollow stem, 1.6 mm wall
                for (a = [0 : 360 / SLOTS : 359]) rotate(a) translate([-0.8, 0, 1.5]) cube([1.6, stem_d, STEM_L]);   // slots make the fingers
            }
        }
        translate([0, 0, -1]) cylinder(d = 2, h = 1);   // nothing; keeps difference() non-empty for older OpenSCAD
    }
}

// Dish rack: a shallow tray with a raised lip and a drain notch at one end, six fins across so plates lean between them.
RACK_L = 216; RACK_W = 140; TRAY_T = 3; LIP_H = 8; LIP_T = 2.4;
FIN_N = 6; FIN_T = 5; FIN_H = 40; FIN_L = 110;
module rack() {
    difference() {
        union() {
            // tray with lip
            linear_extrude(TRAY_T) offset(r = 6) offset(delta = -6) square([RACK_L, RACK_W]);
            linear_extrude(LIP_H) difference() {
                offset(r = 6) offset(delta = -6) square([RACK_L, RACK_W]);
                translate([LIP_T, LIP_T]) offset(r = 4) offset(delta = -4) square([RACK_L - 2 * LIP_T, RACK_W - 2 * LIP_T]);
            }
            // fins, with a wider foot so they print without support and do not snap off
            for (i = [0 : FIN_N - 1]) translate([RACK_L / 2 - (FIN_N - 1) / 2 * (RACK_L - 40) / (FIN_N - 1) + i * (RACK_L - 40) / (FIN_N - 1), RACK_W / 2, TRAY_T]) {
                translate([-FIN_T / 2, -FIN_L / 2, 0]) cube([FIN_T, FIN_L, FIN_H]);
                hull() { translate([-FIN_T / 2 - 4, -FIN_L / 2, 0]) cube([FIN_T + 8, FIN_L, 0.01]); translate([-FIN_T / 2, -FIN_L / 2, 6]) cube([FIN_T, FIN_L, 0.01]); }
            }
        }
        translate([RACK_L - 30, -1, TRAY_T + 2]) cube([14, 10, LIP_H]);                                   // drain notch in the front lip, right end: tip it toward the sink
        for (x = [25 : 20 : RACK_L - 25], y = [20 : 20 : RACK_W - 20]) translate([x, y, -1]) cylinder(d = 4, h = TRAY_T + 2, $fn = 24);   // drip holes
    }
}

// Frying pan: flared dish, 2.4 mm wall, a flat-bottom handle with a hang hole. 110 + 70 mm long, fits a 220 bed diagonally or straight.
PAN_D = 110; PAN_H = 24; PAN_WALL = 2.4; PAN_FLOOR = 3; HANDLE_L = 70; HANDLE_W = 18; HANDLE_T = 8;
module pan() {
    difference() {
        cylinder(d1 = PAN_D - 12, d2 = PAN_D, h = PAN_H);
        translate([0, 0, PAN_FLOOR]) cylinder(d1 = PAN_D - 12 - 2 * PAN_WALL, d2 = PAN_D - 2 * PAN_WALL, h = PAN_H);
    }
    difference() {   // handle: a flat bar from the base of the dish, rising gently to the grip, like a toy skillet. Prints flat.
        hull() {
            translate([PAN_D / 2 - 14, 0, 0]) linear_extrude(HANDLE_T) offset(r = 4) square([1, HANDLE_W - 8], center = true);
            translate([PAN_D / 2 + HANDLE_L - 6, 0, 0]) linear_extrude(HANDLE_T + 3) circle(d = HANDLE_W);
        }
        translate([PAN_D / 2 + HANDLE_L - 8, 0, -1]) cylinder(d = 6, h = PAN_H + 20);                     // hang hole
    }
}

// Canisters: straight cups with a thickened rim; lids push on over the rim with 0.3 mm clearance.
CAN = ["S", "M", "L"]; CAN_D = [60, 70, 80]; CAN_H = [70, 85, 100]; CAN_WALL = 1.6; CAN_FLOOR = 2; LID_H = 12; LID_CLEAR = 0.3;
function ci() = search([$size == undef ? size : $size], CAN)[0];
module canister() difference() {
    union() { cylinder(d = CAN_D[ci()], h = CAN_H[ci()]); translate([0, 0, CAN_H[ci()] - 4]) cylinder(d = CAN_D[ci()] + 1.2, h = 4); }   // rim bead
    translate([0, 0, CAN_FLOOR]) cylinder(d = CAN_D[ci()] - 2 * CAN_WALL, h = CAN_H[ci()]);
}
module lid() difference() {
    cylinder(d = CAN_D[ci()] + 1.2 + 2 * LID_CLEAR + 2 * 2, h = LID_H);
    translate([0, 0, 2.5]) cylinder(d = CAN_D[ci()] + 1.2 + 2 * LID_CLEAR, h = LID_H);                     // sits over the rim bead
    translate([0, 0, -1]) cylinder(d = 14, h = 2);                                                       // finger dimple, bottom (prints as the top)
}

// Spatula: a slotted blade with a flat handle, one piece, 4 mm thick at the handle thinning to 2 mm at the blade edge.
module spatula() {
    hull() { translate([0, 0, 0]) linear_extrude(2) offset(r = 6) offset(delta = -6) square([70, 48], center = true);
             translate([35, 0, 0]) linear_extrude(3) square([1, 30], center = true); }
    difference() {
        linear_extrude(2) offset(r = 6) offset(delta = -6) square([70, 48], center = true);
        for (y = [-12, 0, 12]) translate([-10, y, -1]) linear_extrude(4) offset(r = 2) square([44, 1], center = true);   // slots
    }
    hull() { translate([35, 0, 0]) linear_extrude(3) square([1, 30], center = true); translate([60, 0, 0]) linear_extrude(4) square([1, 18], center = true); }
    hull() { translate([60, 0, 0]) linear_extrude(4) square([1, 18], center = true); translate([108, 0, 0]) linear_extrude(4) circle(d = 20); }
    translate([108, 0, 0]) difference() { linear_extrude(4) circle(d = 20); translate([0, 0, -1]) linear_extrude(6) circle(d = 5); }   // hang hole
}

// Plate: 100 mm, a shallow dish with a 2.4 mm floor and a 6 mm rim; stands between the rack fins (35 mm pitch).
PLATE_D = 100;
module plate() difference() {
    union() { cylinder(d = PLATE_D, h = 2.4); cylinder(d1 = PLATE_D, d2 = PLATE_D - 8, h = 6); }
    translate([0, 0, 2.4]) cylinder(d1 = PLATE_D - 14, d2 = PLATE_D - 10, h = 4);
}

// Bushing for the knob screws: the CNC plunges a 1/2 in hole; this fills it and centres the 8-32 screw.
module bushing() difference() { cylinder(d = 12.6, h = 17.5, $fn = 64); translate([0, 0, -1]) cylinder(d = 4.9, h = 20, $fn = 32); }   // 0.496 in OD, 0.19 in bore, 0.69 in long

// Pickup foot, printed socket-side down with no supports: tube socket boss, a 45 degree cone out to the wall, a slotted wall,
// and four legs cut from the far rim so the open end sits 5 mm off the pail floor. In use it is the other way up: tube in the
// socket, legs on the floor. Water comes in through the slots and the open end, down the hollow cone and through a 10 mm bore
// into the tube; the tube seats on a 2 mm shoulder at the end of the socket.
PK_D = 36; PK_WALL = 2; PK_BOSS_D = 22; PK_SOCKET = 12; PK_SHOULDER = 2; PK_TUBE = 16.1; PK_BORE = 10; PK_CONE = 11; PK_WALL_H = 20; PK_LEG = 5;
PK_Z0 = PK_SOCKET + PK_SHOULDER + PK_CONE;   // where the straight wall starts
module pickup() difference() {
    union() {
        cylinder(d = PK_BOSS_D, h = PK_SOCKET + PK_SHOULDER);                                              // socket boss (bottom on the bed)
        translate([0, 0, PK_SOCKET + PK_SHOULDER]) cylinder(d1 = PK_BOSS_D, d2 = PK_D, h = PK_CONE);        // cone to the wall, 35 degrees from vertical
        translate([0, 0, PK_Z0]) cylinder(d = PK_D, h = PK_WALL_H + PK_LEG);                               // wall and legs
    }
    translate([0, 0, -1]) cylinder(d = PK_TUBE, h = PK_SOCKET + 1);                                        // tube socket
    translate([0, 0, PK_SOCKET - 1]) cylinder(d = PK_BORE, h = PK_SHOULDER + 2);                           // water bore through the shoulder
    translate([0, 0, PK_SOCKET + PK_SHOULDER]) cylinder(d1 = PK_BORE, d2 = PK_D - 2 * PK_WALL, h = PK_CONE + 0.01);   // hollow cone, 45 degrees
    translate([0, 0, PK_Z0]) cylinder(d = PK_D - 2 * PK_WALL, h = PK_WALL_H + PK_LEG + 1);                 // hollow wall, open far end
    for (a = [0 : 15 : 359]) rotate(a) translate([PK_D / 2 - PK_WALL - 1, -0.6, PK_Z0 + 3]) cube([PK_WALL + 2, 1.2, PK_WALL_H - 6]);   // slots
    for (a = [45 : 90 : 359]) rotate(a) translate([0, 0, PK_Z0 + PK_WALL_H]) linear_extrude(PK_LEG + 1) polygon([[0, 0], [30, -14], [30, 14]]);   // notches between the legs
}
module pickup_cut() difference() { pickup(); translate([-50, 0, -1]) cube([100, 100, 100]); }   // half, to see the water path

// Funnel for the dirty jug: drops into a hole drilled in the jug's cap, mouth under the sink strainer. The 37.5 mm spout fits a
// 1 1/2 in hole and the 52 mm flange still bears on the cap round a 1 3/4 in one, so any of 1 1/2, 1 5/8 or 1 3/4 in works.
// Prints mouth down: the cone narrows going up, the flange is a 45 degree step, the spout is a straight tube.
FN_MOUTH = 100; FN_SPOUT = 37.5; FN_CONE_H = 22; FN_FLANGE = 52; FN_SPOUT_L = 16; FN_WALL = 1.6;
FN_FL_H = (FN_FLANGE - FN_SPOUT) / 2;                    // 45 degrees, no supports
module funnel() difference() {
    union() {
        cylinder(d1 = FN_MOUTH, d2 = FN_SPOUT, h = FN_CONE_H);
        translate([0, 0, FN_CONE_H]) cylinder(d1 = FN_SPOUT, d2 = FN_FLANGE, h = FN_FL_H);
        translate([0, 0, FN_CONE_H + FN_FL_H]) cylinder(d = FN_SPOUT, h = FN_SPOUT_L);
    }
    translate([0, 0, -1]) cylinder(d1 = FN_MOUTH - 2 * FN_WALL + 2, d2 = FN_SPOUT - 2 * FN_WALL - 2, h = FN_CONE_H + 2);
    translate([0, 0, FN_CONE_H - 1]) cylinder(d = FN_SPOUT - 2 * FN_WALL, h = FN_FL_H + FN_SPOUT_L + 2);
}

// Cap plug: a disc with a spigot that fits the funnel's hole in the dirty jug's cap, so the jug can be carried full without the funnel.
module cap_plug() { cylinder(d = FN_FLANGE + 4, h = 2.5); translate([0, 0, 2.5]) cylinder(d = FN_SPOUT - 0.4, h = 10); translate([0, 0, 2.5]) cylinder(d1 = FN_SPOUT + 2, d2 = FN_SPOUT - 0.4, h = 1.5); }

// Fill port, in use mouth up: z = 0 is the counter top. Printed mouth down (flip in the slicer, or it is modelled that way below).
FP_MOUTH = 80; FP_MOUTH_H = 25; FP_FLANGE = 50; FP_SPOUT = 36; FP_SPOUT_L = 40; FP_BARB = 16; FP_BARB_L = 20; FP_WALL = 1.6;
module fill_port() translate([0, 0, FP_MOUTH_H + 3]) mirror([0, 0, 1]) difference() {           // mirrored so the mouth is on the bed
    union() {
        translate([0, 0, 3]) cylinder(d1 = FP_FLANGE, d2 = FP_MOUTH, h = FP_MOUTH_H);                       // mouth, leaning out
        cylinder(d = FP_FLANGE, h = 3);                                                                 // flange on the counter
        translate([0, 0, -FP_SPOUT_L]) cylinder(d = FP_SPOUT, h = FP_SPOUT_L);                           // spout through the counter
        translate([0, 0, -FP_SPOUT_L - FP_BARB_L]) cylinder(d = FP_BARB, h = FP_BARB_L);                 // barb for the 1/2 in tube
        for (i = [0 : 2]) translate([0, 0, -FP_SPOUT_L - 4 - i * 6]) cylinder(d1 = FP_BARB, d2 = FP_BARB + 2, h = 2);
    }
    translate([0, 0, 3]) cylinder(d1 = FP_SPOUT - 2 * FP_WALL, d2 = FP_MOUTH - 2 * FP_WALL, h = FP_MOUTH_H + 1);   // funnel
    translate([0, 0, -FP_SPOUT_L + 12]) cylinder(d = FP_SPOUT - 2 * FP_WALL, h = FP_SPOUT_L);                   // spout bore
    translate([0, 0, -FP_SPOUT_L]) cylinder(d1 = FP_BARB - 2 * FP_WALL, d2 = FP_SPOUT - 2 * FP_WALL, h = 12.01);  // taper to the barb bore
    translate([0, 0, -FP_SPOUT_L - FP_BARB_L - 1]) cylinder(d = FP_BARB - 2 * FP_WALL, h = FP_BARB_L + 2);
}
module fill_lid() difference() {
    union() { cylinder(d = FP_MOUTH + 4, h = 3); translate([0, 0, 3]) difference() { cylinder(d = FP_MOUTH - 2 * FP_WALL - 1, h = 8); translate([0, 0, -1]) cylinder(d = FP_MOUTH - 2 * FP_WALL - 5, h = 10); } }
    translate([0, 0, -1]) cylinder(d = 4.6, h = 6);                                                      // the wood knob's 8-32 screw, from the ring side
}

// Window clip: lies flat on the oven door's inside face across the pocket edge, 10 mm over the acrylic, one #6 x 1/2 screw.
module window_clip() difference() {
    linear_extrude(3) offset(r = 3) offset(delta = -3) square([22, 14]);
    translate([6, 7, -1]) { cylinder(d = 3.8, h = 5, $fn = 32); translate([0, 0, 2.2]) cylinder(d1 = 3.8, d2 = 7.5, h = 1.9, $fn = 32); }   // countersunk
}

// Wiring box: screwed to the back panel over the cord hole, right of the pump. Base prints floor down, lid prints face down; no
// supports. u across the kitchen, v up the back panel, from the box's outer bottom-left corner (kitchen x 10.42, z 11.6 in).
// Two sides, nothing crosses: the relay stands on the right, socket down, its five leads going left into the single-wire ends
// of a column of six XALXMAW lever connectors; every outside wire (supply through the cord hole, pump through the top notch,
// float runs through the bottom notches) comes in on the left and lands on the connectors' output ends. Each connector lies on
// its side in a slot, resting on the rib below it; a bar on the lid stops them falling forward. A zip tie through each of the
// relay's two saddles holds it. Four #6 x 1/2 screws on a rectangle hold it to the panel, four in the corners hold the lid.
WB_W = 152.4; WB_H = 101.6; WB_D = 37.6; WB_LID = 3; WB_WALL = 2.4; WB_FLOOR = 3; WB_R = 4;
WB_CORD = [63.5, 86.4];                                   // the back panel's 1/2 in cord hole, in box coordinates
LC_L = 32; LC_H = 13.5; LC_GAP = 0.3;                     // XALXMAW lever connector: 32 long (wire axis), 13.5 tall; 8 wide (1 in 1 out), 13 (1 in 2 out)
WB_LCS = [[8, "PUMP+"], [13, "GND"], [13, "+12V"], [13, "SERIES"], [8, "85"], [8, "87a"]];   // top to bottom, in the order the outside wires arrive: pump, supply, clean, dirty
WB_RIB = 1.6; WB_RIB_H = 9; WB_COL_U = 76;                // ribs between the slots; column's left (output) end
WB_COL_V = WB_WALL - WB_RIB;                              // the bottom rib is the wall
WB_BOSS = [for (u = [7, WB_W - 7]) for (v = [7, WB_H - 7]) [u, v]];          // lid screws, in the corners
WB_SCREWS = [for (u = [20, WB_W - 20]) for (v = [10, WB_H - 10]) [u, v]];   // to the back panel, countersunk inside: a 112 x 82 mm rectangle
WB_NOTCH = [[18, 0], [34, 0], [72, 1]];                   // [u, 0 = bottom wall (clean, dirty float runs) / 1 = top wall (pump, just left of the column)]
WB_NOTCH_W = 9; WB_NOTCH_D = 8;
WB_RELAY = [118, 38, 30, 48];                             // u0, v0, width, length: relay above, socket below, leads out the bottom
// v of the bottom of slot i (0 = top slot), counting up from the column's bottom rib
function wb_slot_v(i) = i == len(WB_LCS) - 1 ? WB_COL_V + WB_RIB : wb_slot_v(i + 1) + WB_LCS[i + 1][0] + LC_GAP + WB_RIB;
WB_COL_TOP = wb_slot_v(0) + WB_LCS[0][0] + LC_GAP;        // underside of the top rib
module wb_outline(inset = 0) offset(r = WB_R - inset) offset(delta = -WB_R) square([WB_W, WB_H]);
module wb_screw_cs(d1 = 3.8, d2 = 7.5, h = 1.9) { cylinder(d = d1, h = 20, center = true, $fn = 32); cylinder(d1 = d1, d2 = d2, h = h, $fn = 32); }
module wire_box() difference() {
    union() {
        linear_extrude(WB_D) difference() { wb_outline(); wb_outline(WB_WALL); }                          // walls
        linear_extrude(WB_FLOOR) wb_outline();                                                             // floor
        for (b = WB_BOSS) translate(b) cylinder(d = 9, h = WB_D, $fn = 48);                               // lid bosses
        for (v = [WB_COL_V, for (i = [0 : len(WB_LCS) - 1]) wb_slot_v(i) + WB_LCS[i][0] + LC_GAP])        // ribs under and over each slot
            translate([WB_COL_U + 3, v, 0]) cube([LC_L - 6, WB_RIB, WB_FLOOR + WB_RIB_H]);
        for (i = [0 : len(WB_LCS) - 1])                                                                   // labels at the output end
            translate([WB_COL_U - 2, wb_slot_v(i) + (WB_LCS[i][0] + LC_GAP) / 2, WB_FLOOR - 0.01])
                linear_extrude(0.61) text(WB_LCS[i][1], size = 3.4, font = "Liberation Sans:style=Bold", halign = "right", valign = "center");
        for (dv = [10, 34]) translate([WB_RELAY[0], WB_RELAY[1] + dv, 0]) cube([WB_RELAY[2], 6, WB_FLOOR + 3]);   // relay saddles
        for (du = [1, WB_RELAY[2] - 4]) translate([WB_RELAY[0] + du, WB_RELAY[1] - 3, 0]) cube([3, 3, WB_FLOOR + 10]);   // feet it stands on, leads between
        translate([WB_RELAY[0] - 6, WB_RELAY[1] + WB_RELAY[3] + 3, WB_FLOOR - 0.01]) linear_extrude(0.61)
            text("RELAY", size = 3.6, font = "Liberation Sans:style=Bold");
    }
    for (dv = [10, 34]) translate([WB_RELAY[0] - 1, WB_RELAY[1] + dv + 0.75, WB_FLOOR]) cube([WB_RELAY[2] + 2, 4.5, 1.8]);   // zip-tie tunnels
    for (b = WB_BOSS) translate([b[0], b[1], WB_D - 14]) cylinder(d = 2.8, h = 15, $fn = 24);             // pilot for #6 screws
    translate([WB_CORD[0], WB_CORD[1], -1]) cylinder(d = 16, h = WB_FLOOR + 2, $fn = 64);                 // over the cord hole
    for (sc = WB_SCREWS) translate([sc[0], sc[1], WB_FLOOR - 1.9]) wb_screw_cs();
    for (n = WB_NOTCH) translate([n[0], n[1] ? WB_H - WB_WALL - 1 : -1, WB_D - WB_NOTCH_D]) {             // wire notches, open to the lid
        translate([-WB_NOTCH_W / 2, 0, WB_NOTCH_W / 2]) cube([WB_NOTCH_W, WB_WALL + 2, WB_NOTCH_D]);
        translate([0, 0, WB_NOTCH_W / 2]) rotate([-90, 0, 0]) cylinder(d = WB_NOTCH_W, h = WB_WALL + 2, $fn = 32);
    }
}
// Lid, modelled face down as it prints: u is mirrored (u' = WB_W - u). Tongues drop 3 mm into each notch and leave a 5 mm wire slot.
module wire_box_lid() difference() {
    union() {
        linear_extrude(WB_LID) wb_outline();
        for (n = WB_NOTCH) translate([WB_W - n[0] - WB_NOTCH_W / 2 + 0.3, n[1] ? WB_H - WB_WALL : 0, WB_LID - 0.01]) cube([WB_NOTCH_W - 0.6, WB_WALL, 3]);
        translate([WB_W - (WB_COL_U + LC_L / 2) - 1, WB_WALL, WB_LID - 0.01])                             // keeper bar: stops 1 mm above the connectors
            cube([2, WB_COL_TOP - WB_WALL, WB_D - WB_FLOOR - LC_H - 1]);
    }
    for (b = WB_BOSS) translate([WB_W - b[0], b[1], 0]) mirror([0, 0, 1]) translate([0, 0, -1.9]) wb_screw_cs();   // countersunk on the face
    for (i = [0 : 3]) translate([WB_W - WB_RELAY[0] - 7 - i * 6.5, WB_RELAY[1] + 6, -1]) cube([2.4, WB_RELAY[3] - 12, WB_LID + 2]);   // vents over the relay coil
    translate([WB_W / 2 + 10, 40, -0.01]) mirror([1, 0, 0]) linear_extrude(0.6) text("12 V", size = 9, font = "Liberation Sans:style=Bold", halign = "center");
}

// Hinge shim: fills a hinge recess cut too deep so the leaf sits flush again (recess 1.4 mm = the leaf). The shape of the
// recess with a hair off: square corners at the panel edge, the bit's 1/4 in radius on the two inner corners. Drop it in,
// hinge leaf on top, drill through the hinge's own holes. shim_t = recess depth - 1.4 mm.
SHIM_L = 65.5; SHIM_W = 18.6; shim_t = 0.4;
module hinge_shim(t = shim_t) linear_extrude(t) hull() {
    square([0.01, SHIM_L]);                                                     // edge side, square
    for (y = [6.35, SHIM_L - 6.35]) translate([SHIM_W - 6.35, y]) circle(r = 6.35, $fn = 48);
}

module washer() difference() { cylinder(d = 20, h = 2, $fn = 64); translate([0, 0, -1]) cylinder(d = 4.6, h = 4, $fn = 32); }

if (part == "burner") burner();
else if (part == "washer") washer();
else if (part == "funnel") funnel();
else if (part == "window_clip") window_clip();
else if (part == "cap_plug") cap_plug();
else if (part == "fill_port") fill_port();
else if (part == "fill_lid") fill_lid();
else if (part == "pickup") pickup();
else if (part == "pickup_cut") pickup_cut();
else if (part == "drip_pan") drip_pan();
else if (part == "coil") coil();
else if (part == "stove_knob") stove_knob();
else if (part == "knob_boss") knob_boss();
else if (part == "bezel") bezel();
else if (part == "rack") rack();
else if (part == "pan") pan();
else if (part == "spatula") spatula();
else if (part == "plate") plate();
else if (part == "bushing") bushing();
else if (part == "canister") canister();
else if (part == "lid") lid();
else if (part == "burner_preview") { burner(); translate([170, 0, 0]) { bezel(); translate([0, 0, 2]) stove_knob(); translate([45, 0, 0]) knob_boss(); } }
else if (part == "toys_preview") {   // all the toys together, for the shop sheet
    pan();
    translate([0, -110, 0]) spatula();
    translate([150, -110, 0]) plate();
    translate([240, -110, 0]) bushing();
    translate([290, -110, 0]) pickup();
    translate([240, -150, 0]) washer();
    translate([380, -110, 0]) funnel();
    translate([380, 0, 0]) window_clip();
    translate([470, -110, 0]) cap_plug();
    translate([470, 0, 0]) fill_port();
    translate([570, 0, 0]) fill_lid();
    for (i = [0 : 2]) translate([150 + i * 95, 0, 0]) { $size = CAN[i]; canister(); translate([0, 0, CAN_H[i] + 14]) rotate([180, 0, 0]) lid(); }
}
else if (part == "hole_cover") hole_cover();
else if (part == "hinge_shim") hinge_shim();
else if (part == "wire_box") wire_box();
else if (part == "wire_box_lid") wire_box_lid();
else if (part == "wire_box_preview") { wire_box(); translate([0, WB_H + 15, 0]) wire_box_lid(); }
