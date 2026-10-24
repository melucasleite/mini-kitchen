# Mini Kitchen

A toddler play kitchen with a real sink that runs, a stove and an oven with a window. It's a 45 7/8 × 18 × 45 in
hutch, cut on a CNC from five 48 × 48 in panels of 3/4 in red oak plywood, and the parts are 3D-printed.

![Mini Kitchen](cover.jpg)

## What's here

- **`shop-sheet.pdf`**: everything you need to build it: cut list, sheet layouts, budget, wiring, plumbing, assembly and finish.
- **`cnc/`**: Carbide Create files, one per sheet, toolpaths set for a 1/4 in downcut bit.
- **`cut-sheets/`**: the same sheets as 1:1 SVGs, for any other CAM software.
- **`stl/`, `plates/`**: the printed parts.
- **`kitchen.scad`, `printed.scad`**: the OpenSCAD models.

## Changing it

Every number lives in `design.py`. Change it there, then regenerate:

```bash
python3 design.py params.scad && python3 gen_sheets.py && python3 gen_html.py && python3 gen_c2d.py
```

Measure your plywood with calipers first and set `T` and `T_MAX`, then run the Carbide Create simulation before you
cut anything.
