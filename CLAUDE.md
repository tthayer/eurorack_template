# Agent operating manual — Eurorack module (through-hole, protoboard)

You are planning and documenting a DIY Eurorack module that the builder will make by hand on
**pad-per-hole perfboard with through-hole parts only**. There is no PCB, no SMD part and
no fab step. Follow this file exactly. When it conflicts with your general knowledge,
this file and `docs/reference/` win. Where they are silent, ask instead of guessing.

## Hard rules (never break)

1. **Through-hole only.** No SOT, SOIC, TSSOP, MSOP, QFN, 0603/0805/1206 or "SMD" parts.
   If the only good part is SMD-only, say so and pick the best THT alternative, or a
   ready-made breakout module (DIP-pinned) if the SPEC allows it. `make check` enforces this.
2. **Protoboard build.** The build documents are the WireViz diagrams (`docs/wiring/`) and
   the perfboard placement plan (`docs/LAYOUT.md`). Never plan PCB layout, Gerbers or fab.
3. **Spec before implementation.** Do not write `hardware/gen_sch.py` content, wiring or
   layout until the SPEC phase gate is passed (`docs/PLAN.md`).
4. **One source of truth per fact.** Values and nets live in `docs/SPEC.md`. Everything else
   (generator, wiring YAML, layout, BOM) is downstream. Change SPEC first, then the rest
   in the same commit.
5. **Eurorack power is fixed:** 10-pin header, pins 1–2 = −12 V (red stripe), 3–8 = GND,
   9–10 = +12 V. **There is no +5 V on a 10-pin header.** Copy the power section from the
   template; do not redraw it from memory. (A wrong copy of this pinout once shorted
   +12 V to GND on paper. See `docs/reference/LESSONS.md` L1.)
6. **Show the math.** Every resistor/capacitor value that sets a gain, level, frequency,
   current, offset or trim range gets a one-line calculation in SPEC, using the recipes
   in `docs/reference/CALCS.md`. Trimmers must sit near mid-travel at the nominal value.
7. **Read the source, don't infer it.** When adapting an existing design, read its
   schematic pin by pin and quote the reference designators. If a sheet is an image,
   view it. Never describe a connection you haven't seen (LESSONS L4).
8. **No transistor matching steps.** Modern 2N3904/2N3906 are consistent enough; thermally
   bond expo pairs and their tempco instead.
9. **Stay in this repo.** Other projects (`~/projects/*`) are read-only references. Never
   edit, commit or push them, and don't offer to.
10. **Don't push or publish** unless the builder asks. Adapted designs may carry "personal use
    only" terms; record them in README and keep the repo private.

## Workflow

Work strictly phase by phase (`docs/PLAN.md`). Each phase ends with a **gate**: run the
listed commands, fix failures, then stop and summarize for the builder. Don't start the next
phase until he says so.

| Phase | Output | Gate command |
|---|---|---|
| 0 Requirements | SPEC §1–3 filled (function, I/O, controls, HP, power budget) | `make check` |
| 1 Circuit design | SPEC §4–8 filled: every block, values with math, BOM, calibration, acceptance | `make check STRICT=1` |
| 2 Schematic | `hardware/gen_sch.py`, `hardware/check_netlist.py` | `make erc` |
| 3 Wiring + layout | `docs/wiring/*.yml`, `docs/LAYOUT.md` | `make wiring check` + look at every PNG |
| 4 Panel | `docs/panel.yml` drill spec | `make panel`, print at 100 %, test-fit parts |
| 5 Build + bring-up | `docs/BRINGUP.md` filled while building | every SPEC acceptance box ticked |

## How to do each phase

**Phase 0.** Ask the builder (in one message, max 4 questions) whatever you cannot infer: what the
module does, inputs/outputs, controls, target HP, any source design. Fill SPEC §1–3. Pick
HP from the panel-fit table in `docs/reference/EURORACK.md`; justify it in one line.

**Phase 1.** Split the circuit into blocks (power, references, each signal path, outputs).
For each block write a table: Ref | Part | Value | Why. Use parts from
`docs/reference/PARTS.md` first; if you need one that isn't there, say why. Then fill
the BOM, the calibration procedure and the acceptance checklist. Log every non-obvious
choice in `docs/DECISIONS.md` (decision, alternatives, reason).

**Phase 2.** Translate SPEC into `gen_sch.py` block by block (API in `hardware/schlib.py`).
Use SPEC net names verbatim. For every SPEC connection, add a `check()` to
`check_netlist.py` that asserts the exact pin set. `make erc` must end with
`ERC: clean` (or only warnings you have explained in SPEC) and `0 failure(s)`.

**Phase 3.** Wiring YAML conventions are in `docs/wiring/README.md`. Plan the perfboard in
`docs/LAYOUT.md` (grid, rails, placement table). Render with `make wiring` and **open
every PNG** to check it: crossed or missing wires are common.

**Phase 4.** Fill `docs/panel.yml` (hole positions, sizes from PARTS.md) and run
`make panel`. Check that the drill positions match the control positions in LAYOUT.md.

**Phase 5.** The builder builds. You help interpret measurements against SPEC values. Never ask
him to run loud or stressful tests without saying first what he will hear or see.

## Stop and ask when

- a requirement is ambiguous or two requirements conflict;
- a part is obsolete, SMD-only, or you can't confirm its pinout;
- a calculation puts a trimmer outside 25–75 % of travel or an op-amp output beyond its
  swing (`CALCS.md` C3);
- a gate command fails twice after your fixes;
- you are about to change something already marked decided in `docs/DECISIONS.md`.

## Reporting

Keep summaries short: what changed (files), gate results (command + pass/fail),
open questions, and the next phase. Quote numbers with units. No filler.
