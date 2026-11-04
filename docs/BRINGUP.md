# __MODULE__ — bring-up log

Fill in as you build. Measured values go next to the SPEC targets.

## 1. Before power
- [ ] LAYOUT.md "Checks before power-up" done
- [ ] Resistance +12 V→GND and −12 V→GND, no ICs: > 1 kΩ (record: ___ / ___)

## 2. Smoke test (current-limited supply ≈ 50 mA, or a rack with a fuse)
- [ ] No ICs: rails after diodes = ___ / ___ V (target ±11.4…11.8)
- [ ] References (if any): ___ / ___ V (target ±0.5 %)
- [ ] ICs fitted: current +12 V ___ mA, −12 V ___ mA (SPEC §3: ___ / ___)

## 3. Block checks
One line per SPEC §5 block: stimulus → expected → measured.

| Block | Stimulus | Expected | Measured | OK |
|---|---|---|---|---|
| | | | | |

## 4. Calibration (SPEC §8)
| Step | Trimmer | Target | Final reading |
|---|---|---|---|
| | | | |

## 5. Acceptance (SPEC §9)
Copy the checklist here and tick with measured values.
