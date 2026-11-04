# __MODULE__ — perfboard layout

Pad-per-hole perfboard, 2.54 mm pitch. Columns are letters (A = left edge, seen from the
component side), rows are numbers (1 = top). A part's position is the hole of its pin 1.

## Board

| Item | Value |
|---|---|
| Board | TBD × TBD holes (TBD × TBD mm). Width from EURORACK.md perfboard row. |
| Orientation | Parallel / perpendicular to the panel |
| Mounting | e.g. L-brackets on the jack nuts, or standoffs to a control board |

## Rails

Run bare tinned-wire buses along the long edges: +12 V on the top row, GND on the next
row, −12 V on the bottom row (or GND in the middle as a split). Mark the bus rows here:

| Bus | Row(s) | Fed from |
|---|---|---|
| +12V | TBD | D1 cathode |
| GND | TBD | J1 3–8 |
| −12V | TBD | D2 anode |

## Placement

Place by signal flow: power entry at the rear edge, ICs in the middle with their 100 nF
caps across the supply pins, inputs near the harness header, sensitive nodes (summing
junctions, expo pair, references) short and away from warm parts (regulators, 1N5819s).

| Ref | Pin-1 hole | Orientation | Notes |
|---|---|---|---|
| J1 | TBD | key notch toward board edge, stripe = pin 1 | pins 1–2 −12 V |
| TBD | | | |

## Cuts and links

Pad-per-hole boards have no tracks to cut. List any wire links that cross other parts:

| From | To | Net | Over/under |
|---|---|---|---|
| | | | |

## Checks before power-up

- [ ] Power header: no bridge across pin pairs (continuity +12 V↔GND, −12 V↔GND open)
- [ ] Every IC: supply pins to the right buses (DIP-8: 8 = V+, 4 = V−; DIP-14 quad: 4 = V+, 11 = V−)
- [ ] Electrolytic polarity, diode bands
