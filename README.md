# eurorack_template

A project template for designing **DIY Eurorack modules built by hand**, with
through-hole parts on pad-per-hole perfboard. No PCB, no SMD, no fab house.

It gives a module a fixed structure: a spec with required sections, a phased plan with a
check at the end of each phase, reference sheets (Eurorack power and levels, preferred
parts, calculation recipes, lessons learned) and scripts that catch the expensive
mistakes before you solder. The structure is strict on purpose, so that a person or a
smaller, cheaper AI model can plan a usable module by filling it in step by step.

## What you end up with

For each module:

- `docs/SPEC.md`: what it does, every jack and control, every part value with the math behind it, BOM, calibration, acceptance tests
- a KiCad schematic **generated from a Python script**, checked by KiCad's ERC and by netlist assertions you write against the spec
- WireViz wiring diagrams of the board and the panel, printable on letter paper
- a perfboard placement plan and a 1:1 panel drill template
- a bring-up log to fill in while you build

## Workflow

| Phase | You produce | Gate (must pass before moving on) |
|---|---|---|
| 0 Requirements | Function, jacks, controls, width (HP), power budget | `make check` |
| 1 Circuit design | Every block with values and calculations, BOM, calibration | `make check STRICT=1` (no TBD left, no SMD parts) |
| 2 Schematic | `hardware/gen_sch.py` + `hardware/check_netlist.py` | `make erc` (ERC clean, all netlist checks pass) |
| 3 Wiring + layout | `docs/wiring/*.yml`, `docs/LAYOUT.md` | `make wiring check`, then look at every PNG |
| 4 Panel | `docs/panel.csv` | `make panel`, print at 100 %, test-fit |
| 5 Build | `docs/BRINGUP.md` | every acceptance test in SPEC passes |

## Requirements

- Python 3 (standard library only)
- [KiCad](https://www.kicad.org/) 9 or 10 (for `kicad-cli` and the stock symbol libraries)
- [WireViz](https://github.com/wireviz/WireViz) and Graphviz
- librsvg (`rsvg-convert`), qpdf and poppler (`pdfinfo`) for PDFs and print tiles

macOS:

```sh
brew install graphviz librsvg qpdf poppler
brew install --cask kicad
pipx install wireviz
```

The scripts default to the macOS KiCad paths. On Linux or Windows, point them at your install:

```sh
export KICAD_CLI=/usr/bin/kicad-cli
export KICAD_SHARE=/usr/share/kicad      # the folder that contains symbols/ and template/
```

## Start a new module

**Option A: GitHub.** Click **Use this template**, create your repo, clone it, then convert it in place:

```sh
git clone https://github.com/<you>/<your_module>.git
cd <your_module>
./new_module.sh --here my_module 8        # name (lowercase, underscores), width in HP
```

**Option B: local copy.** Clone this template once and stamp out modules from it:

```sh
git clone https://github.com/tthayer/eurorack_template.git
cd eurorack_template
./new_module.sh my_module 8               # creates ~/projects/my_module with a fresh git repo
./new_module.sh my_module 8 ~/synth       # or choose the parent folder
```

Either way, the script fills in the module name and HP, swaps in the module README,
removes the template-only files and makes the first commit with your git identity
(override with `EURORACK_GIT_NAME` / `EURORACK_GIT_EMAIL`).

Check that everything works on the built-in example circuit (a power entry and a
TL072 buffer):

```sh
make check erc wiring panel
```

## Using it with an AI agent

`CLAUDE.md` is an operating manual for an AI coding agent such as
[Claude Code](https://claude.com/claude-code): the hard rules, what to produce in each
phase, which command is the gate, and when to stop and ask you. Other agents can read it
too (copy it to `AGENTS.md` if yours looks for that name).

Open the new module folder in the agent and work one phase at a time:

```text
Start Phase 0. I want a dual attenuverter with offset, 4HP, normalled to +5 V.
```
```text
Phase 0 looks right. Go to Phase 1.
```
```text
Adapt <published design, with link>. Start Phase 0 and read the schematic pin by pin.
```

The agent stops at each gate with a summary. Review it, answer its questions, then tell
it to continue. Because the decisions, calculations and checks are written down, a
smaller, cheaper model can do most of the work, and you review the result.

## Using it by hand

Work through `docs/PLAN.md` top to bottom. Fill `docs/SPEC.md`, using
`docs/reference/CALCS.md` for every value, and run the gate command at the end of each
phase. The reference sheets are written to be read by people as well as models.

## Commands

| Command | Does |
|---|---|
| `make check` | Spec structure, leftover placeholders, power-header pinout in the wiring files, through-hole only |
| `make check STRICT=1` | Also fails while any `TBD` remains in the spec |
| `make erc` | Regenerate the schematic, run ERC, export netlist/PDF/BOM, run `check_netlist.py` |
| `make wiring` | Render the WireViz diagrams to SVG/PNG/PDF |
| `make wiring-print` | Letter-size tiled PDFs of the diagrams for the bench |
| `make panel` | 1:1 panel drill template (SVG + PDF) from `docs/panel.csv`, with spacing warnings |

## Layout

```text
CLAUDE.md               rules and phase-by-phase instructions (for agents and people)
README.module.md        becomes the module's README
new_module.sh           create a module from the template
docs/
  SPEC.md               design spec, the single source of truth
  PLAN.md               phases and gate checklists
  DECISIONS.md          append-only decision log
  LAYOUT.md             perfboard placement plan
  BRINGUP.md            build and calibration log
  panel.csv             panel drill spec
  wiring/               WireViz sources (+ conventions in wiring/README.md)
  reference/
    EURORACK.md         power pinout, signal levels, panel sizes, HP fitting
    PARTS.md            preferred through-hole parts, obsolete → replacement
    CALCS.md            calculation recipes (gain, swing, trim centering, references, ...)
    LESSONS.md          mistakes already made, so you don't repeat them
    EXAMPLES.md         patterns from the author's modules
hardware/
  schlib.py             netlist-by-name KiCad schematic builder
  gen_sch.py            your circuit (example included)
  check_netlist.py      netlist assertions (power checks included)
  run_erc.sh, sexp.py   ERC/export runner, s-expression helpers
tools/
  check.py              gate checker
  panel.py              drill template generator
```

## Design rules baked in

- **Power:** 10-pin header, pins 1–2 = −12 V (red stripe), 3–8 = GND, 9–10 = +12 V,
  with a series 1N5819 on each rail. There is **no +5 V** on a 10-pin cable.
  `make check` fails if a wiring file says otherwise.
- **Levels:** audio ±5 V through 1 kΩ, inputs ≈ 100 kΩ and safe to ±12 V, op-amp outputs
  designed for ±9 V on ±11.6 V rails.
- **Parts:** through-hole only. Pitch-critical voltages come from LM4040 references, not the rails.
- **No transistor matching:** expo pairs are two 2N3904s glued together with the tempco bonded on.

These suit the author's builds. If yours differ (16-pin power, PCBs), change
`CLAUDE.md`, `docs/reference/` and `tools/check.py` together.

## Safety

Eurorack power can destroy modules and, through a shorted ribbon, other modules in
the case. Follow the checks in `docs/LAYOUT.md` and `docs/BRINGUP.md` before first power-up,
and use a current-limited supply for the smoke test. You build at your own risk.
