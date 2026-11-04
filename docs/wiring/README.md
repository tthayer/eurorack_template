# Wiring diagrams (WireViz)

`system.yml` = the main perfboard: power entry, rails, every IC with pin labels, and
the harness pads. `panel.yml` = everything on the panel (jacks, pots, switches, LEDs)
and the wires to the board. `make wiring` renders SVG/PNG/PDF, and `make wiring-print`
makes letter-size tiled PDFs. **Open every PNG after rendering.**

Conventions (copied from midi_cv2/th_xr_vco; keep them):
- Header comment: what the file covers and that `docs/SPEC.md` is the source of truth.
- `metadata.title`, `options: {fontname: Helvetica, bgcolor: WH, color_mode: short}`.
- Connector `type` starts with the ref (`U1 TL072 (DIP-8)`). Put small passives in
  `notes` on the part they sit at, with values copied from SPEC.
- IC `pinlabels` give the physical pin number + function + net, e.g. `"1 OUT A → R3"`.
- Wire colours: −12 V BU, +12 V RD, GND BK, signals any other colour.
- Panel parts: jacks `pins: [T, TN, S]`; pots `pins: [CW, W, CCW]`.
- The power connector labels must be exactly
  `[-12V, -12V, GND, GND, GND, GND, GND, GND, +12V, +12V]` (`make check` lints this).

WireViz gotchas (LESSONS L11): no `->` in labels (use `→`); no `R1.CW` dot notation in
`connections` (use `- R1: [CW]`); connector to connector needs a cable between.
