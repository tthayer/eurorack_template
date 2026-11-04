# Eurorack reference (verified facts — use these, don't recall from memory)

## Power

| Item | Value |
|---|---|
| Module header | 2×5 shrouded (keyed) box header, 2.54 mm |
| 10-pin pinout | **1–2 = −12 V (red stripe), 3–8 = GND, 9–10 = +12 V** |
| 16-pin bus pinout | 1–2 −12 V, 3–8 GND, 9–10 +12 V, 11–12 +5 V, 13–14 CV, 15–16 GATE |
| +5 V | **Not available on a 10-pin cable.** Make it on board (78L05 / 7805) if needed. |
| Reverse protection | 1N5819 in series with each rail. +12 V: anode at header, cathode at board. −12 V: cathode at header, anode at board. A flipped ribbon swaps ±12 V; both diodes block; GND (3–8) is symmetric. |
| Rails after Schottky | ≈ ±11.6 V (use this, not 12, in every calculation) |
| Bulk + HF decoupling | 10–22 µF/25 V electrolytic + 100 nF per rail at the header; 100 nF at every IC supply pin |
| Perfboard header | Pin pairs (1+2, 3+4, …, 9+10) are the same net. Solder-bridge only within a pair; a bridge across pairs shorts a rail. |

## Signal levels (conventions)

| Signal | Level | Notes |
|---|---|---|
| Audio out | ±5 V (10 Vpp) | Through a **1 kΩ series resistor** (short protection). |
| Bipolar CV | ±5 V | |
| Unipolar CV | 0…+5 V or 0…+8/10 V | Say which in SPEC. |
| Pitch | 1 V/oct | Tracking target: ±5 cents over 5 octaves. |
| Gate | 0 / +5…+10 V | Inputs should trigger at ≈ +1…2 V. |
| Trigger | short pulse (1–10 ms), 0 / +5…10 V | |
| Input impedance | ≈ 100 kΩ | Inputs must survive ±12 V indefinitely. |
| TL07x swing on ±11.6 V | ≈ ±10.5 V typical, ±9 V worst case | Rail-to-rail ±12 V DIP parts are rare; design for this swing. |

## Mechanics

| Item | Value |
|---|---|
| Panel height | 128.5 mm (3U) |
| HP | 5.08 mm. Panel widths: 4HP 20.0, 6HP 30.0, 8HP 40.3, 10HP 50.5, 12HP 60.6, 14HP 70.8, 16HP 80.9 mm |
| Rails | Top and bottom ≈ 10 mm of panel are behind the rails: keep controls out of y < 12 and y > 116.5 mm. |
| Board height behind panel | ≈ 108 mm max (between rails) |
| Mounting holes | Ø 3.2 mm, centres 3.0 mm from top/bottom edge, 7.5 mm from left edge. Panels ≥ 10HP: second column at 7.5 + (HP−3)×5.08 mm. |
| Depth | Aim ≤ 40 mm (skiff-friendly); state it in SPEC. |
| Perfboard width | 2.54 mm pitch: holes across ≈ floor((panel width − 3) / 2.54). 6HP ≈ 10 holes, 8HP ≈ 14, 10HP ≈ 18, 12HP ≈ 22. |

## Panel-fit rule of thumb (for picking HP in Phase 0)

| Part | Min centre-to-centre | Panel hole |
|---|---|---|
| Thonkiconn PJ398SM jack | 12 mm (14 mm comfortable) | 6.0 mm |
| Alpha 9 mm pot (small knob ≤ 12 mm) | 15 mm (18 mm comfortable) | 7.0 mm |
| Alpha 16 mm pot (big knob) | 22 mm | 7.5 mm |
| Mini toggle (Dailywell/Salecom) | 12 mm | 6.2 mm (¼") |
| Alpha SR2511F-family rotary (≈24 mm body) | 26 mm; needs its own row | 10 mm (check datasheet) |
| 3 mm LED | 6 mm | 3.2 mm (or 5.0 mm bezel) |

Rough HP: columns = floor(usable width / pitch), rows within ≈ 100 mm of usable height.
Two pot columns + three jack columns fit 10HP; 6HP fits two jack columns.
