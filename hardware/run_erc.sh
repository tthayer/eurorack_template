#!/bin/sh
# Regenerate the schematic, run ERC, export the netlist, run the netlist assertions.
# Exit status is non-zero if ERC has errors or any netlist check fails.
cd "$(dirname "$0")" || exit 1
CLI=${KICAD_CLI:-/opt/homebrew/bin/kicad-cli}
python3 gen_sch.py || exit 1
SCH=$(ls *.kicad_sch | head -1)
NAME=${SCH%.kicad_sch}
"$CLI" sch erc --format json --severity-all -o erc.json "$SCH" 2>&1 | grep -v Fontconfig
python3 - <<'EOF' || ERC_FAIL=1
import json, sys
from collections import Counter
d = json.load(open("erc.json"))
v = [x for s in d["sheets"] for x in s["violations"]]
print("ERC:", dict(Counter((x["severity"], x["type"]) for x in v)) or "clean")
for x in v[:40]:
    print(" ", x["severity"], x["type"], x["description"], [i["description"] for i in x["items"]])
sys.exit(1 if any(x["severity"] == "error" for x in v) else 0)
EOF
"$CLI" sch export netlist --format kicadxml -o "$NAME.xml" "$SCH" 2>&1 | grep -v Fontconfig
"$CLI" sch export pdf -o "$NAME.pdf" "$SCH" 2>&1 | grep -v Fontconfig
"$CLI" sch export bom -o "${NAME}_bom.csv" "$SCH" 2>&1 | grep -v Fontconfig
python3 check_netlist.py || exit 1
[ -z "$ERC_FAIL" ] || { echo "ERC has errors"; exit 1; }
