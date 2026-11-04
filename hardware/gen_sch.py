#!/usr/bin/env python3
"""Generate __MODULE__.kicad_sch from docs/SPEC.md.

Rules (see CLAUDE.md "Phase 2"):
- docs/SPEC.md is the authority. Every ref/value here must match a SPEC table row.
- One section per SPEC block, in SPEC order, each starting with text("...").
- Connectivity is by net name. Use the SAME net names as the SPEC and the wiring YAML.
- Every pin of every placed unit appears in conns (None = no-connect).
- After editing: `make erc` must report 0 errors and check_netlist.py 0 failures.

The power section and the example output buffer below are working, ERC-clean
starting points. Keep the power section; replace the example with the real circuit.
"""
from schlib import *  # noqa: F403

init("__MODULE__", title="__MODULE__ - Eurorack module, __HP__HP")

# ---------------------------------------------------------------- POWER (keep; edit only values)
# 10-pin Eurorack: 1-2 = -12V (red stripe), 3-8 = GND, 9-10 = +12V. NO +5V on a 10-pin header.
text("POWER  (Eurorack 10-pin, +/-12 V, series Schottky reverse protection)", 15, 20)
place(PWR_HDR, "J1", "Eurorack_2x5", 30, 50,
      {"1": "-12V_IN", "2": "-12V_IN", "3": "GND", "4": "GND", "5": "GND", "6": "GND",
       "7": "GND", "8": "GND", "9": "+12V_IN", "10": "+12V_IN"}, footprint=FP["PWR2x5"])
# D1: anode = +12V_IN (header), cathode = +12V (board). D2: anode = -12V (board), cathode = -12V_IN (header).
place(D_SCHOTTKY, "D1", "1N5819", 65, 35, {"2": "+12V_IN", "1": "+12V"}, footprint=FP["DO41"])
place(D_SCHOTTKY, "D2", "1N5819", 65, 65, {"2": "-12V", "1": "-12V_IN"}, footprint=FP["DO41"])
cap("C1", "22uF 25V", 85, 35, "+12V", "GND", pol=True)
cap("C2", "22uF 25V", 85, 65, "GND", "-12V", pol=True)
cap("C3", "100nF", 97, 35, "+12V", "GND")
cap("C4", "100nF", 97, 65, "GND", "-12V")
pwr_flag("+12V", 110, 25)
pwr_flag("-12V", 110, 75)
pwr_flag("GND", 120, 25)

# ---------------------------------------------------------------- EXAMPLE: input -> inverting buffer -> output (replace)
text("EXAMPLE  (input jack -> TL072 inverting buffer -> 1k -> output jack)", 15, 100)
place(JACK, "J2", "IN", 30, 120, {"T": "IN", "TN": None, "S": "GND"}, footprint=FP["JACK"])
res("R1", "100k", 50, 120, "IN", "U1A_INV")
res("R2", "100k", 70, 110, "U1A_INV", "U1A_OUT")
place(OPAMP2, "U1", "TL072", 70, 125, {"2": "U1A_INV", "3": "GND", "1": "U1A_OUT"}, unit=1, footprint=FP["DIP8"])
res("R3", "1k", 90, 125, "U1A_OUT", "OUT")
place(JACK, "J3", "OUT", 110, 125, {"T": "OUT", "TN": None, "S": "GND"}, footprint=FP["JACK"])
# Unused op-amp half: follower with +in to GND (never leave an op-amp input floating).
place(OPAMP2, "U1", "TL072", 70, 150, {"5": "GND", "6": "U1B_OUT", "7": "U1B_OUT"}, unit=2, footprint=FP["DIP8"])
place(OPAMP2, "U1", "TL072", 70, 175, {"8": "+12V", "4": "-12V"}, unit=3, footprint=FP["DIP8"])
cap("C5", "100nF", 90, 170, "+12V", "GND")
cap("C6", "100nF", 90, 182, "GND", "-12V")

emit()
