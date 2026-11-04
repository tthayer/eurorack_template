#!/usr/bin/env python3
"""Render docs/panel.csv to a 1:1 drill template SVG (docs/panel_drill.svg).

panel.csv format (mm, origin = top-left of the panel seen from the FRONT):
    # hp=10
    ref,label,x,y,hole
    J1,V/OCT,10,100,6.0
Mounting holes (Doepfer A-100) are added automatically. Print the PDF at 100 % and
check the 50 mm scale bar with a ruler before drilling.
"""
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "panel.csv")
OUT = os.path.join(ROOT, "docs", "panel_drill.svg")
H = 128.5
WIDTHS = {4: 20.0, 6: 30.0, 8: 40.3, 10: 50.5, 12: 60.6, 14: 70.8, 16: 80.9}

lines = open(SRC).read().splitlines()
hp = int(next(l for l in lines if l.startswith("# hp=")).split("=")[1])
W = WIDTHS.get(hp, round(hp * 5.08 - 0.3, 1))
rows = list(csv.DictReader(l for l in lines if l and not l.startswith("#")))

errs = []
for r in rows:
    x, y, d = float(r["x"]), float(r["y"]), float(r["hole"])
    if not (d / 2 + 1.5 <= x <= W - d / 2 - 1.5):
        errs.append(f"{r['ref']}: x={x} too close to the panel edge (width {W})")
    if not (12 <= y <= H - 12):
        errs.append(f"{r['ref']}: y={y} is behind the rails (keep 12 <= y <= {H - 12})")
for i, a in enumerate(rows):
    for b in rows[i + 1:]:
        dist = ((float(a["x"]) - float(b["x"])) ** 2 + (float(a["y"]) - float(b["y"])) ** 2) ** 0.5
        if dist < 11:
            errs.append(f"{a['ref']}-{b['ref']}: {dist:.1f} mm apart (< 11 mm; check EURORACK.md pitch table)")

mx = [7.5] + ([7.5 + (hp - 3) * 5.08] if hp >= 10 else [])
holes = [(x, y, 3.2, "") for x in mx for y in (3.0, H - 3.0)]
holes += [(float(r["x"]), float(r["y"]), float(r["hole"]), f"{r['ref']} {r['label']}") for r in rows]

VW = max(W + 20, 110)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{VW}mm" height="{H + 30}mm" '
       f'viewBox="-10 -10 {VW} {H + 30}" font-family="Helvetica" font-size="2.2">',
       f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="black" stroke-width="0.2"/>',
       f'<text x="0" y="-4">{os.path.basename(ROOT)} panel, {hp}HP ({W} x {H} mm), FRONT view, 1:1</text>']
for x, y, d, t in holes:
    svg.append(f'<circle cx="{x}" cy="{y}" r="{d / 2}" fill="none" stroke="black" stroke-width="0.15"/>')
    svg.append(f'<path d="M{x - 1} {y}H{x + 1}M{x} {y - 1}V{y + 1}" stroke="red" stroke-width="0.1"/>')
    if t:
        svg.append(f'<text x="{x}" y="{y + d / 2 + 2.5}" text-anchor="middle">{t} ⌀{d}</text>')
svg.append(f'<path d="M0 {H + 10}h50" stroke="black" stroke-width="0.4"/>'
           f'<text x="0" y="{H + 15}">50 mm: check with a ruler before drilling</text></svg>')
open(OUT, "w").write("\n".join(svg) + "\n")
print(f"wrote {OUT} ({len(rows)} holes + {len(mx) * 2} mounting)")
for e in errs:
    print("WARN", e)
sys.exit(0)
