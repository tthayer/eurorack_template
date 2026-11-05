# __MODULE__ — phased plan

Each phase ends at a gate. At a gate: run the commands, fix what fails, summarize for
the Builder, and **stop**. `docs/SPEC.md` is the authority; when a later phase changes a value,
update SPEC first.

## Phase 0 — Requirements
- [ ] SPEC §1 function, goals, non-goals
- [ ] SPEC §2 jacks and controls
- [ ] SPEC §3 HP (justified), depth, board split, current estimate
- [ ] Source design located and read (schematic viewed pin by pin), license noted
- **Gate:** `make check` passes. The Builder approves the I/O, controls and HP.

## Phase 1 — Circuit design
- [ ] SPEC §5 one subsection per block, every value with its calculation
- [ ] SPEC §6 harness/header pin map (if more than one board)
- [ ] SPEC §7 BOM (THT only), §8 calibration, §9 acceptance criteria
- [ ] DECISIONS.md: every non-obvious choice logged
- **Gate:** `make check STRICT=1` passes (no TBD, no SMD). The Builder reviews.

## Phase 2 — Schematic and netlist checks
- [ ] `hardware/gen_sch.py`: example replaced by the SPEC blocks, net names verbatim
- [ ] `hardware/check_netlist.py`: one check per SPEC connection, power checks kept
- **Gate:** `make erc` → `ERC: clean` and `0 failure(s)`. Schematic PDF looks sane.

## Phase 3 — Wiring diagrams and perfboard layout
- [ ] `docs/wiring/system.yml`: power, every IC with pin labels, rail taps, harness header
- [ ] `docs/wiring/panel.yml`: every jack, pot, switch, LED to the harness/control header
- [ ] `docs/LAYOUT.md`: perfboard size, rails, placement table, cut list
- **Gate:** `make wiring check` passes; every PNG opened and checked for crossed/missing wires.

## Phase 4 — Panel
- [ ] `docs/panel.csv` hole list (positions match LAYOUT.md, sizes from EURORACK.md)
- **Gate:** `make panel`; print `docs/panel_drill.pdf` at 100 %, check the scale bar, test-fit the parts.

## Phase 5 — Build, bring-up, calibration
- [ ] Follow `docs/BRINGUP.md` in order, recording measurements
- **Gate:** every SPEC §9 box ticked.

## Phase 6 — Optional enhancements
Only after v1 passes. Candidates live in SPEC §10.
