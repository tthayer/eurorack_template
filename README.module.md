# __MODULE__

Eurorack module, __HP__HP, through-hole parts on pad-per-hole perfboard.
Built from `eurorack_template`. Status: **Phase 0 (requirements)**.

| Path | What |
|---|---|
| `CLAUDE.md` | Operating manual for the agent: rules, phases, gates, when to stop |
| `docs/SPEC.md` | Design spec, the single source of truth |
| `docs/PLAN.md` | Phases and gate checklists |
| `docs/DECISIONS.md` | Decision log (append-only) |
| `docs/LAYOUT.md` | Perfboard placement plan |
| `docs/BRINGUP.md` | Build and calibration log |
| `docs/panel.csv` | Panel drill spec → `make panel` |
| `docs/wiring/` | WireViz diagrams → `make wiring` / `make wiring-print` |
| `docs/reference/` | Eurorack facts, preferred THT parts, calculation recipes, lessons, examples |
| `hardware/` | Schematic generator (`gen_sch.py` + `schlib.py`), ERC + netlist checks → `make erc` |
| `tools/` | `check.py` gate checker (`make check`), `panel.py` drill template |

Tools: `brew install graphviz librsvg qpdf poppler` + KiCad 10 + `pipx install wireviz`.

## Notes
