# Calculation recipes

Use these in SPEC. Write each as: formula → numbers → result → "✓" or the fix.
Use the rail **after the Schottky: V+ = +11.6 V, V− = −11.6 V**.

## C1. Rescaling a ±15 V design to Eurorack
For every resistor fed from a rail: keep the **current** the same.
`R_new = R_old × (V_new / V_old)`. E.g. 1.5 MΩ from +15 V (10 µA) → from a +10 V
reference: 1.0 MΩ. Prefer feeding pitch-critical nodes from LM4040 references (C6),
not the rails: rail ripple becomes pitch modulation (1 % ripple ≈ 17 cents).

## C2. Op-amp gain
- Inverting: `G = −Rf / Rin`. Input impedance = Rin.
- Non-inverting: `G = 1 + Rf / Rg`.
- Inverting summer: `Vout = −Rf × Σ(Vi / Ri)`.

## C3. Swing / headroom check (mandatory for every op-amp output)
`|Vout_max| ≤ 9 V` (TL07x worst case on ±11.6 V; 10.5 V typical). If a design needs more,
reduce the gain and scale up after, or accept clipping and say why.

## C4. Output level from a saturating stage (comparator, square)
`Vout = Vsat × R_shunt / (R_series + R_shunt)`; output impedance ≈ R_series ∥ R_shunt.
E.g. ±10.5 V, 2.2k / 2.0k → ±5.0 V at 1.05 kΩ.

## C5. Offset trim centering
Inverting stage with offset current from a rail through `R_fixed + R_trim`:
`R_total = Rf × V_rail / (G × V_dc)`, then pick `R_fixed ≈ R_total − R_trim/2`.
**Check:** the nominal sits at 25–75 % of the trimmer. Write the % in SPEC.

## C6. LM4040 shunt reference bias
`R_bias = (V_rail_min − V_ref) / (I_load + I_min)`, with V_rail_min = 11.4 V, I_min = 0.1 mA
(10 V part) and I_load = total current drawn from the reference node. Then check at
V_rail_max = 12.0 V that the shunt current stays < 15 mA. A 10 V reference from 11.6 V has
only 1.6 V of headroom: keep pot loads ≥ 100 kΩ. For more headroom, use the 5.0 V or 8.2 V part.

## C7. Pot as a voltage source between ±REF
Current per pot = `(V+ − V−) / R_pot`; add it to C6's I_load for both references.

## C8. RC corner
`f = 1 / (2π R C)`. AC-coupling into 100 kΩ: 1 µF → 1.6 Hz. Bias-node filter must sit
below the lowest frequency the module produces (LFO range!).

## C9. Exponential converter (NPN pair)
`ΔV_BE per octave = V_T × ln 2 = 17.9 mV at 25 °C`. Summer gain × divider must give
17.9 mV at the base per 1 V of input. Put the scale trimmer so this lands mid-travel.
Reference current 1–20 µA from a reference (C6), not a rail.

## C10. Current budget
Sum per rail: op-amps (TL072 ≈ 3 mA, TL074 ≈ 6 mA, TL062 ≈ 0.5 mA), references (bias
current), LEDs, regulators' load, plus 30 % margin. Report `+12 V xx mA, −12 V yy mA`.

## C11. Timing / frequency
Write the chip's own formula from its datasheet with the units, e.g. XR-2206
`f = I_T / (3 V × C)`. State the centre frequency and the range.
