#!/usr/bin/env python3
"""Phase-gate checks for a module made from eurorack_template.

  python3 tools/check.py           # structure, power pinout, through-hole-only
  python3 tools/check.py --strict  # also: no TBD left in docs/SPEC.md (Phase 1 gate)

Exit 1 on any FAIL. Standard library only.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRICT = "--strict" in sys.argv
fails = 0


def rd(p):
    with open(os.path.join(ROOT, p)) as f:
        return f.read()


def report(ok, msg, warn=False):
    global fails
    tag = "PASS" if ok else ("WARN" if warn else "FAIL")
    print(f"{tag} {msg}")
    if not ok and not warn:
        fails += 1


PLACEHOLDER = "__" + "MODULE" + "__"  # split so new_module.sh does not rewrite it
is_template = os.path.exists(os.path.join(ROOT, ".template"))

# 1. Placeholders replaced (skipped in the template repo itself)
if not is_template:
    hits = [p for p in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True)
            if os.path.isfile(p) and p.endswith((".md", ".py", ".yml", ".csv", ".sh"))
            and PLACEHOLDER in open(p, errors="ignore").read()]
    report(not hits, "no template placeholders left" + (f": {[os.path.relpath(h, ROOT) for h in hits]}" if hits else ""))

# 2. SPEC structure and TBDs
spec = rd("docs/SPEC.md")
for n, name in enumerate(["Function", "Front panel I/O", "Power, size and build", "Power entry",
                          "Circuit blocks", "Board-to-board", "Bill of materials", "Calibration",
                          "Acceptance criteria", "Deferred options"], 1):
    report(re.search(rf"^## {n}\. {re.escape(name)}", spec, re.M) is not None, f"SPEC has '## {n}. {name}'")
tbd = len(re.findall(r"\bTBD\b", spec))
report(tbd == 0, f"SPEC TBD count = {tbd}", warn=not STRICT)

# 3. Power header pinout in every wiring file
GOOD = ["-12V", "-12V", "GND", "GND", "GND", "GND", "GND", "GND", "+12V", "+12V"]
for y in sorted(glob.glob(os.path.join(ROOT, "docs", "wiring", "*.yml"))):
    for m in re.finditer(r"(pinlabels|wirelabels):\s*\[([^\]]*)\]", open(y).read()):
        labels = [s.strip() for s in m.group(2).split(",")]
        if len(labels) == 10 and labels[0].startswith("-12V"):
            report(labels == GOOD, f"{os.path.relpath(y, ROOT)} power {m.group(1)} = 1-2 -12V, 3-8 GND, 9-10 +12V"
                   + ("" if labels == GOOD else f" (got {labels})"))

# 4. Through-hole only: SPEC body, generator, wiring
SMD = re.compile(r"\b(SOT-?\d+|SOIC|TSSOP|MSOP|QFN|DFN|SMD|0402|0603|0805|1206|SOD-?123|SOD-?323)\b")
for p in ["docs/SPEC.md", "hardware/gen_sch.py"] + [os.path.relpath(y, ROOT) for y in glob.glob(os.path.join(ROOT, "docs", "wiring", "*.yml"))]:
    bad = [f"{i}: {l.strip()[:80]}" for i, l in enumerate(rd(p).splitlines(), 1)
           if SMD.search(l) and not re.search(r"breakout|not used|rejected|instead|SMD-only|SMD only|no SMD|All THT", l, re.I)]
    report(not bad, f"{p}: through-hole only" + ("".join("\n     " + b for b in bad) if bad else ""))

# 5. Generator still has the standard power section
gen = rd("hardware/gen_sch.py")
report('"9": "+12V_IN", "10": "+12V_IN"' in gen and '"1": "-12V_IN", "2": "-12V_IN"' in gen,
       "gen_sch.py keeps the standard J1 power section")

print(f"\n{fails} failure(s)")
sys.exit(1 if fails else 0)
