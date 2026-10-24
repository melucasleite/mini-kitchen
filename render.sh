#!/bin/zsh
# Every preview the shop sheet and README use, from the model. Run after any change to kitchen.scad, printed.scad or design.py.
set -e
cd "$(dirname "$0")"
python3 design.py >/dev/null
OS=/Applications/OpenSCAD-2021.01.app/Contents/MacOS/OpenSCAD
C="--colorscheme=Tomorrow"
$OS -o exploded.png -D 'part="exploded"' --camera=23,9,26,62,0,28,195 --projection=p --imgsize=1600,1200 $C kitchen.scad 2>/dev/null
$OS -o open.png -D 'show_doors=false' --camera=16,9,24,72,0,25,95 --projection=p --imgsize=1600,1200 $C kitchen.scad 2>/dev/null
$OS -o previews/iso.png --camera=23,9,22,62,0,28,135 --projection=p --imgsize=1600,1200 $C kitchen.scad 2>/dev/null
$OS -o previews/front.png --camera=23,9,22,90,0,0,120 --projection=o --imgsize=1600,1200 $C kitchen.scad 2>/dev/null
$OS -o previews/faucet_close.png -D 'show_doors=false' --camera=16,12,24,70,0,25,30 --projection=p --imgsize=1200,900 $C kitchen.scad 2>/dev/null
$OS -o previews/printed.png -D 'part="burner_preview"' --camera=90,0,10,55,0,25,520 --projection=p --imgsize=1600,900 $C printed.scad 2>/dev/null
$OS -o previews/toys.png -D 'part="toys_preview"' --camera=170,-40,20,55,0,25,1000 --projection=p --imgsize=1600,900 $C printed.scad 2>/dev/null
$OS -o previews/wire_box_wired.png -D 'part="none"' --camera=117,48,0,0,0,0,330 --projection=o --imgsize=2300,1150 $C wire_box_wired.scad 2>/dev/null
echo "previews rendered"
