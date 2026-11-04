#!/usr/bin/env python3
"""Assert key nets of the exported netlist against docs/SPEC.md.

Add one check() per SPEC table row that defines a connection: every IC pin,
every jack tip, every board-to-board header pin. A check that cannot fail is
useless: assert the exact pin set where you can (nets.get(NET) == {...}).
The POWER checks below are mandatory and must stay.
"""
import glob
import os
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
xmls = [p for p in glob.glob(os.path.join(HERE, "*.xml"))]
if len(xmls) != 1:
    sys.exit(f"expected exactly one exported netlist *.xml in {HERE}, found {xmls}")
root = ET.parse(xmls[0]).getroot()

pin2net, nets = {}, {}
for n in root.iter("net"):
    name = n.get("name").lstrip("/")
    nodes = {(x.get("ref"), x.get("pin")) for x in n.iter("node")}
    nets[name] = nodes
    for nd in nodes:
        pin2net[nd] = name

fails = 0


def check(desc, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + desc)
    fails += 0 if ok else 1


def on(net, *pins):
    """All given (ref, pin) are on net."""
    return net in nets and all(p in nets[net] for p in pins)


def same(*pins):
    """All given (ref, pin) share one net."""
    s = {pin2net.get(p) for p in pins}
    return len(s) == 1 and None not in s


def net_of(ref, pin):
    return pin2net.get((ref, pin))


# ---------------------------------------------------------------- POWER (mandatory)
check("J1 1,2 = -12V_IN -> D2 cathode", same(("J1", "1"), ("J1", "2"), ("D2", "1")))
check("J1 3-8 = GND", all(net_of("J1", p) == "GND" for p in "345678"))
check("J1 9,10 = +12V_IN -> D1 anode (no +5V on a 10-pin header)",
      same(("J1", "9"), ("J1", "10"), ("D1", "2")))
check("D1 cathode = +12V, D2 anode = -12V", net_of("D1", "1") == "+12V" and net_of("D2", "2") == "-12V")
check("No +5V net unless SPEC adds a regulator", "+5V" not in nets or any(r.startswith("U") for r, _ in nets["+5V"]))

# ---------------------------------------------------------------- MODULE CHECKS (replace the example)
check("EXAMPLE U1A: +in GND, -in on R1/R2, out -> R3",
      net_of("U1", "3") == "GND" and same(("U1", "2"), ("R1", "2"), ("R2", "1"))
      and same(("U1", "1"), ("R2", "2"), ("R3", "1")))
check("EXAMPLE U1 power: 8 = +12V, 4 = -12V", net_of("U1", "8") == "+12V" and net_of("U1", "4") == "-12V")
check("EXAMPLE U1B unused: follower, +in GND", net_of("U1", "5") == "GND" and same(("U1", "6"), ("U1", "7")))
check("EXAMPLE OUT jack tip = OUT after R3", nets.get("OUT") == {("R3", "2"), ("J3", "T")})

print(f"\n{fails} failure(s)")
sys.exit(1 if fails else 0)
