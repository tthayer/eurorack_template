# Worked examples (read-only — never edit these repos)

| Project | Path | What to learn from it |
|---|---|---|
| th_xr_vco | `~/projects/th_xr_vco` | Adapting a published ±15 V analog design: original-circuit table with source refs kept, change tables (original → Eurorack value + reason), ±10 V references, switch pole/position table, calibration order, acceptance criteria, deferred options. Docs-only (Phase 0/1). |
| midi_cv2 | `~/projects/midi_cv2` | MCU module (Pico 2) all the way through Phase 2: `hardware/gen_sch.py` driven by DESIGN.md, `check_netlist.py` with exact pin-set assertions, perfboard notes on the power header, wiring diagrams for a two-board build, firmware with host tests. |

Patterns worth copying:
- **Change tables** (th_xr_vco SPEC §3): `Ref | Original | Eurorack | Reason`, so a reviewer can check every change against the source sheet.
- **Per-block "why" column with numbers** (both), e.g. "±10.5 V × 2.0/4.2 → ±5.0 V".
- **One header pin map** asserted pin-for-pin in the netlist check (midi_cv2 J6/J7).
- **Notes on the part** in WireViz (midi_cv2): small passives listed where they solder, values from the spec.
