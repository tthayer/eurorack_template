# __MODULE__ — decision log

Append-only. Never re-propose a rejected option without new information (LESSONS L15).
Template-wide decisions (D0.x) apply to every module from this template.

| # | Date | Decision | Alternatives rejected | Reason |
|---|---|---|---|---|
| D0.1 | template | Through-hole parts only | SMD, mixed | Hand-built on perfboard |
| D0.2 | template | Pad-per-hole perfboard, no PCB | Stripboard, PCB fab | Build style; stripboard bridges are error-prone |
| D0.3 | template | 10-pin power, 1N5819 series per rail | Shunt diode / polyfuse; 16-pin | No +5 V or bus CV needed by default; series Schottky blocks a flipped cable |
| D0.4 | template | No transistor matching; thermally bond expo pairs | Hand matching, matched-pair ICs | Modern 2N3904s are consistent enough; matched pairs are SMD |
| D0.5 | template | Pitch-critical voltages from LM4040 references | Raw rails | Rail ripple → pitch wobble |
