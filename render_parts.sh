#!/bin/zsh
# One PNG per printed part for the 3D Printed Parts grid. Run after any change to printed.scad.
set -e
cd "$(dirname "$0")"
OS=/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD
C="--colorscheme=Tomorrow --autocenter --viewall --projection=p --imgsize=600,450 --camera=0,0,0,55,0,25,100"
for p in drip_pan coil stove_knob knob_boss bezel washer pan spatula plate bushing pickup funnel cap_plug fill_port fill_lid window_clip wire_box wire_box_lid; do
  $OS -o previews/parts/$p.png -D "part=\"$p\"" ${=C} printed.scad 2>/dev/null &
done
for s in S M L; do
  $OS -o previews/parts/canister-$s.png -D 'part="canister"' -D "size=\"$s\"" ${=C} printed.scad 2>/dev/null &
  $OS -o previews/parts/lid-$s.png -D 'part="lid"' -D "size=\"$s\"" ${=C} printed.scad 2>/dev/null &
done
wait
echo "parts rendered"
