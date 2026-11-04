# Lessons learned (th_xr_vco, midi_cv2)

Each entry: what went wrong or what worked, and the rule that follows.

**L1. Power pinout copied wrong.** A wiring diagram labelled the 10-pin header with
+12 V on pins 7–8 and +5 V on 9–10. Pins 7–8 are GND, so that board would short +12 V.
The error spread when the file was copied into a new project.
→ Use the template's power section and `make check` (it lints the header labels). Never
retype the pinout.

**L2. Wrong symbol for the package.** The SOT-23 `LM4040DBZ` symbol (pin 1 K, 2 A) was
used with a TO-92 footprint, whose pins are 2 = K, 3 = A.
→ Use `LM4040LP-xx` for TO-92. When you pair a symbol with a footprint, check the
pin numbers against the datasheet's package drawing.

**L3. Expo op-amp too fast.** The original XR-VCO author found TL072 "abysmal" and TL052
"squirrely" in the expo servo; the LF442 (≈1 MHz) worked. It's loop stability, not bias current.
→ TL062 in expo servo/integrator loops; add a footprint for a small cap across the
summer feedback resistor (populate only if it oscillates).

**L4. Misread schematic.** A second write-up of the same circuit said the waveform switch
went to the XR-2206 symmetry pin (16). It actually goes to pin 3 (multiplier output).
Built that way, the output would have had no bias.
→ View the source schematic image; quote pin numbers and refs; cross-check with the datasheet's pin table.

**L5. Trimmer pushed to its end.** A rescale "re-centred" an offset trimmer by lowering the
fixed resistor, which actually moved the nominal point to 88 % of travel.
→ Always compute the trimmer position at nominal (CALCS C5).

**L6. Switch pole count.** "3 positions" also needs enough poles: TRI/SIN/SQR needed 3
poles × 3 throws (amplitude resistor, sine shaper, output). DPDT ON-ON-ON can't do it.
→ Tabulate pole × position before choosing the part. An Alpha 4P3T rotary is the easy THT answer.

**L7. Headroom on ±12 V.** TL07x gives ≈ +10.2 V typical, ≈ +8.7 V worst case on a +11.7 V
rail. midi_cv2 limited pitch to 8 octaves for this reason. No good THT rail-to-rail ±12 V
op-amps exist.
→ Design outputs for ±9 V max (CALCS C3).

**L8. References beat rails.** Pitch-critical currents and tuning pots fed from the rails
turn rail ripple into pitch wobble. ±10 V LM4040 references fixed it, but the 1.6 V of
headroom needs the bias check (CALCS C6).

**L9. SMD-only parts.** Matched pairs, MCP4725, OPA4197 and others are SMD-only.
→ Use breakouts (DIP-pinned) or THT alternatives (PARTS.md). Don't "temporarily" spec SMD.

**L10. No transistor matching.** Tony's experience: modern 2N3904s are consistent enough.
Thermal bonding still matters.

**L11. WireViz gotchas.**
- `->` in a label breaks Graphviz (HTML labels): use `→`.
- `R33.CW`-style dot references in `connections` are parsed as templates: use `- R33: [CW]`.
- A connector can't connect straight to another connector: put a one-wire cable between.
- Render, then **look at the PNG**.

**L12. Board-to-board header = single source of truth.** Put the pin map in `system.yml`
and assert in `check_netlist.py` that both headers share every net pin-for-pin.

**L13. Perfboard, not stripboard.** Pad-per-hole only. Bridge pads only within the same
net; the power header pairs are the classic trap (L1).

**L14. MCU modules.** Pico 2 on female headers; feed VSYS from +5 V via a Schottky; 3.3 V
logic into 5 V-referenced parts needs a margin check (VIH).

**L15. Check decisions before proposing.** Before suggesting an alternative, read
`docs/DECISIONS.md`; don't re-propose something already rejected.
