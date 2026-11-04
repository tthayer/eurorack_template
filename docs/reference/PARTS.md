# Preferred through-hole parts

Pick from this list first. Every part here is through-hole and stocked (Mouser, Tayda,
Thonk). The KiCad symbols and footprints are wired up in `hardware/schlib.py`.

## Active

| Use | Part | Package | Notes |
|---|---|---|---|
| General op-amp | TL072 (dual), TL074 (quad) | DIP-8 / DIP-14 | Audio, buffers, summers, comparators-ish. Swing ±10.5 V on ±11.6 V. |
| Slow servo / expo loops | **TL062 / TL064** | DIP-8 / DIP-14 | Low-power JFET, ≈1 MHz GBW. Faster amps (TL072, OPA2134) can oscillate in expo servo loops (LESSONS L5). |
| Low-noise audio | NE5532 | DIP-8 | Bipolar input: bias current too high for µA expo/integrator nodes. |
| Comparator | LM311 | DIP-8 | Open collector, needs pull-up. Or a TL07x with hysteresis. |
| OTA / VCA | LM13700 | DIP-16 | Replaces CA3080 / LM13600. |
| Voltage reference | **LM4040xIZ-10.0 / -5.0 / -4.1** | TO-92 | Shunt. KiCad symbol **`LM4040LP-xx`** (TO-92: pin 2 = K, pin 3 = A). Not `LM4040DBZ` (SOT-23 pinout). |
| Regulator +5 V | 78L05 (≤ 100 mA), L7805 (≤ 1 A) | TO-92 / TO-220 | From +12 V. 330 nF in, 10 µF + 100 nF out. |
| NPN / PNP | 2N3904 / 2N3906 | TO-92 | Expo pairs: two 2N3904, flats glued together, tempco bonded to them. No matching. |
| Schottky | 1N5819 (rails), BAT85 (signal clamp) | DO-41 / DO-35 | |
| Signal diode | 1N4148 | DO-35 | |
| LED | 3 mm diffused | THT | 1–4 mA via 1–3.3 kΩ from a ±10 V op-amp output, or 330 Ω from 3.3 V GPIO. |
| MCU | Raspberry Pi Pico 2 (RP2350) | module, socket on female headers | 3.3 V logic. Feed VSYS from +5 V via a 1N5819 (USB and rack power coexist). |
| DAC | MCP4725 **breakout board** | 6-pin header | The chip is SOT-23 only. Wire breakouts by pin NAME; order varies by vendor. |

## Passive

| Use | Part | Notes |
|---|---|---|
| Resistors | ¼ W 1 % metal film | 0.1 % only where it sets a scale (e.g. the 1 V/oct input resistor). |
| Tempco | 2 kΩ or 1 kΩ, +3300…3500 ppm/K, THT | Thermally bonded to the expo pair. |
| Timing / filter caps | C0G/NP0 ceramic (≤ 10 nF), polypropylene or polyester film (> 10 nF) | Never X7R where the value sets pitch or frequency. |
| Decoupling | 100 nF X7R, 5.08 mm radial | One per IC supply pin. |
| Electrolytic | 10–47 µF, 25 V (rails are ±12 V) | |
| Trimmer, multi-turn | Bourns 3296W | Tuning (V/oct, HF). |
| Trimmer, single-turn | Bourns 3386P or 3362P | Offsets, symmetry. |
| Panel pot | Alpha 9 mm (RD901F) 100 k B (linear) | 16 mm Alpha for big tuning knobs. |

## Panel hardware

| Part | Notes |
|---|---|
| Thonkiconn PJ398SM (mono, switched) | Pins: Tip, Tip-normal (TN), Sleeve. KiCad: `AudioJack2_SwitchT`. Unpatched input normal: TN → GND or to a normalled signal. |
| Thonkiconn PJ366ST (stereo) | For TRS (e.g. MIDI). No stock KiCad footprint. |
| Mini toggle SPDT ON-ON / ON-OFF-ON | 2 or 3 positions, 1 pole. DPDT also common. ON-ON-ON parts exist but their centre wiring varies by vendor; avoid. |
| Alpha SR2511F-family rotary | 1P12T, 2P6T, 3P4T, 4P3T. Use when you need 3+ positions × 2+ poles. |
| 2×5 shrouded box header | Power. |

## Obsolete → replacement

| Obsolete | Use instead |
|---|---|
| LM394 / MAT02 matched pair | 2 × 2N3904, glued + tempco bonded |
| LF442 / LF353 in slow loops | TL062 |
| CA3080, LM13600 | LM13700 |
| XR-2206, ICL8038, MAX038 | No new part. XR-2206 stock is second-source; socket it, buy spares, test each one. |
| ±15 V designs | Rescale for ±11.6 V (CALCS.md C1). |
