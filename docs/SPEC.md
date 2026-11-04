# __MODULE__ — design specification

Status: **Phase 0 (requirements).** Build: through-hole parts on pad-per-hole perfboard.
<!-- Replace every TBD. `make check STRICT=1` fails while any TBD remains. -->

Source design: TBD (name, author, revision, URL — or "original").
License / use terms of the source: TBD. If "personal use only", keep the repo private.

---

## 1. Function

One paragraph: what the module does and what makes it worth building.
TBD

**Goals**
1. TBD

**Non-goals (v1)**
- TBD

## 2. Front panel I/O

| Jack | Name | Dir | Range | Impedance | Feeds / fed by |
|---|---|---|---|---|---|
| J? | TBD | in/out | e.g. ±5 V, 1 V/oct, 0–10 V gate | 100 kΩ in / 1 kΩ out | TBD |

| Control | Ref | Part (PARTS.md) | Label | Function |
|---|---|---|---|---|
| TBD | RV? / S? | TBD | TBD | TBD |

## 3. Power, size and build

| Item | Value | Notes |
|---|---|---|
| Width | TBD HP | Justify with EURORACK.md panel-fit table |
| Depth | ≤ TBD mm | |
| +12 V draw | TBD mA | CALCS C10, 30 % margin |
| −12 V draw | TBD mA | |
| +5 V | none / on-board 78L05 / 7805 | 10-pin header has no +5 V |
| Boards | TBD | e.g. one main perfboard + panel-mounted controls on a harness, or main + control perfboard on a header |
| Perfboard size | TBD × TBD holes | EURORACK.md perfboard width |

---

## 4. Power entry (standard — keep)

| Ref | Part | Value | Notes |
|---|---|---|---|
| J1 | 2×5 shrouded header | — | Pins 1–2 = −12 V (red stripe), 3–8 = GND, **9–10 = +12 V**. No +5 V. Bridge pads only within a pin pair. |
| D1 | 1N5819 | — | Series, +12 V: anode = J1 9–10, cathode = board +12 V |
| D2 | 1N5819 | — | Series, −12 V: cathode = J1 1–2, anode = board −12 V |
| C1, C2 | electrolytic | 22 µF 25 V | Bulk per rail after the diodes |
| C3, C4 | X7R | 100 nF | HF per rail after the diodes |

Rails after the diodes ≈ ±11.6 V. All calculations use this.

## 5. Circuit blocks

Repeat this subsection per block (references, each signal path, outputs). Use SPEC net
names that will appear verbatim in `gen_sch.py` and the wiring YAML (UPPER_SNAKE).

### 5.1 TBD block name

Function: TBD (one or two sentences).

| Ref | Part | Value | Net(s) | Why / calculation (CALCS.md id) |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

Checks: swing (C3) TBD · trimmer position (C5) TBD · current (C10) TBD.

## 6. Board-to-board / harness pin map

Only if the build has more than one board or a panel harness. This table is mirrored in
`docs/wiring/system.yml` and asserted pin-for-pin in `check_netlist.py`.

| Pin | Net | From → to |
|---|---|---|
| 1 | GND | |

## 7. Bill of materials

| Ref(s) | Qty | Part | Value | Package | Source |
|---|---|---|---|---|---|
| J1 | 1 | Shrouded box header 2×5 | — | THT | Tayda/Thonk |
| D1, D2 | 2 | 1N5819 | — | DO-41 | |
| TBD | | | | | |

All THT. Resistors ¼ W 1 % metal film. Caps ≥ 25 V. Sockets for every DIP IC.

## 8. Calibration

Ordered steps: what to set, what to measure, the target value.
1. Rails: ±11.4…11.8 V at the board after D1/D2, with no ICs fitted.
2. TBD

## 9. Acceptance criteria (definition of done)

- [ ] Current within §3 budget on both rails. Survives a reversed ribbon.
- [ ] TBD (one measurable line per goal in §1)

## 10. Deferred options

- TBD (ideas considered and postponed; link DECISIONS.md entries)
