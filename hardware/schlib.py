"""Netlist-by-name KiCad schematic builder (extracted from midi_cv2/gen_sch.py).

Every pin gets a short wire stub ending in a net label (signals) or a power
symbol (rails in POWER_NETS), so connectivity is defined by NET NAMES, not by
geometry. Coordinates only affect how readable the sheet is. Unused pins must
be listed with net None (no-connect flag) or ERC will complain.

Usage (see gen_sch.py):
    from schlib import *
    init("my_module", title="...")
    res("R1", "100k", 40, 40, "IN", "SUM")
    place(OPAMP2, "U1", "TL072", 60, 40, {"2": "SUM", "3": "GND", "1": "OUT"}, unit=1, footprint=FP["DIP8"])
    emit()
"""
import json
import math
import os
import uuid as _uuid

from sexp import Sym, dump, get_flat, pins

KICAD_SHARE = "/Applications/KiCad/KiCad.app/Contents/SharedSupport"
STUB = 2.54

# Rails drawn as power symbols. Anything else becomes a net label.
POWER_NETS = {"GND", "+12V", "-12V", "+5V", "+3V3"}

# Through-hole footprints that are known to exist in stock KiCad 10.
FP = {
    "R": "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal",
    "C": "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm",
    "C_FILM": "Capacitor_THT:C_Rect_L7.2mm_W2.5mm_P5.00mm_FKS2_FKP2_MKS2_MKP2",
    "CP": "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm",
    "LED": "LED_THT:LED_D3.0mm",
    "DO41": "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal",   # 1N5819, 1N400x
    "DO35": "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",    # 1N4148, BAT85
    "TO92": "Package_TO_SOT_THT:TO-92_Inline",
    "DIP8": "Package_DIP:DIP-8_W7.62mm",
    "DIP14": "Package_DIP:DIP-14_W7.62mm",
    "DIP16": "Package_DIP:DIP-16_W7.62mm",
    "JACK": "Connector_Audio:Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles",
    "TRIM_MT": "Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical",   # multi-turn
    "TRIM": "Potentiometer_THT:Potentiometer_Bourns_3386P_Vertical",     # single-turn
    "POT9": "Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical",
    "PWR2x5": "Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical",
}

# Frequently used symbols (verified pin numbers in comments).
R = "Device:R"
C = "Device:C"
CP = "Device:C_Polarized"                       # 1 = +, 2 = -
POT = "Device:R_Potentiometer"                  # 1, 3 = ends, 2 = wiper
TRIMPOT = "Device:R_Potentiometer_Trim"         # 1, 3 = ends, 2 = wiper
D_SCHOTTKY = "Diode:1N5819"                     # 1 = K, 2 = A
D_SIGNAL = "Diode:1N4148"                       # 1 = K, 2 = A
REF10_TO92 = "Reference_Voltage:LM4040LP-10"    # TO-92: 2 = K, 3 = A, 1 = NC
OPAMP2 = "Amplifier_Operational:TL072"          # units 1,2 = A,B; unit 3 = power (8 V+, 4 V-)
OPAMP4 = "Amplifier_Operational:TL074"          # units 1-4 = A-D; unit 5 = power (4 V+, 11 V-)
JACK = "Connector_Audio:AudioJack2_SwitchT"     # PJ398SM: T, TN (normal), S
PWR_HDR = "Connector_Generic:Conn_02x05_Odd_Even"

_state = {}
lib_symbols = {}
items = []
PIN_UUID = {}
_n = [0]
_pwr = [0]
_flg = [0]


def init(project, title, rev="A", paper="A3", out_dir=None):
    here = out_dir or os.path.dirname(os.path.abspath(__file__))
    ns = _uuid.uuid5(_uuid.NAMESPACE_URL, "eurorack/" + project)
    _state.update(project=project, title=title, rev=rev, paper=paper, dir=here, ns=ns,
                  root=str(_uuid.uuid5(ns, "root")))


def uid(tag=""):
    _n[0] += 1
    return str(_uuid.uuid5(_state["ns"], f"{tag}#{_n[0]}"))


def r(v):
    return round(v, 4)


def snap(v):
    return round(v / 2.54) * 2.54


def lib(lib_id):
    if lib_id not in lib_symbols:
        l, n = lib_id.split(":")
        lib_symbols[lib_id] = get_flat(l, n)
    return lib_symbols[lib_id]


def _font():
    return [Sym("effects"), [Sym("font"), [Sym("size"), 1.27, 1.27]]]


def _prop(name, value, x, y, hide=False):
    e = _font()
    if hide:
        e.append([Sym("hide"), Sym("yes")])
    return [Sym("property"), name, value, [Sym("at"), r(x), r(y), 0], e]


def _instance(lib_id, ref, value, x, y, unit=1, rot=0, footprint="", fields=None, dnp=False):
    s = lib(lib_id)
    pwr = ref.startswith("#")
    inst = [Sym("symbol"), [Sym("lib_id"), lib_id], [Sym("at"), r(x), r(y), rot], [Sym("unit"), unit],
            [Sym("exclude_from_sim"), Sym("no")], [Sym("in_bom"), Sym("no" if pwr else "yes")],
            [Sym("on_board"), Sym("no" if pwr else "yes")], [Sym("dnp"), Sym("yes" if dnp else "no")],
            [Sym("uuid"), uid(ref + str(unit))],
            _prop("Reference", ref, x + 2.54, y - 6.0, hide=pwr),
            _prop("Value", value, x + 2.54, y - 4.0 if not pwr else y + 3.5),
            _prop("Footprint", footprint, x, y, hide=True), _prop("Datasheet", "", x, y, hide=True)]
    for k, v in (fields or {}).items():
        inst.append(_prop(k, v, x, y, hide=True))
    for p in pins(s):
        if p["unit"] in (0, unit):
            pu = uid(ref + p["number"])
            PIN_UUID[(ref, p["number"])] = pu
            inst.append([Sym("pin"), p["number"], [Sym("uuid"), pu]])
    inst.append([Sym("instances"), [Sym("project"), _state["project"],
                 [Sym("path"), "/" + _state["root"], [Sym("reference"), ref], [Sym("unit"), unit]]]])
    items.append(inst)


def pin_geom(lib_id, x, y, unit, number):
    for p in pins(lib(lib_id)):
        if p["unit"] in (0, unit) and p["number"] == number:
            return x + p["x"], y - p["y"], (p["angle"] + 180) % 360
    raise KeyError(f"{lib_id} unit {unit} has no pin {number}")


def wire(x1, y1, x2, y2):
    items.append([Sym("wire"), [Sym("pts"), [Sym("xy"), r(x1), r(y1)], [Sym("xy"), r(x2), r(y2)]],
                  [Sym("stroke"), [Sym("width"), 0], [Sym("type"), Sym("default")]], [Sym("uuid"), uid("w")]])


def label(net, x, y, ang):
    just = {0: ["left", "bottom"], 90: ["left", "bottom"], 180: ["right", "bottom"], 270: ["right", "bottom"]}[ang]
    e = _font()
    e.append([Sym("justify")] + [Sym(j) for j in just])
    items.append([Sym("label"), net, [Sym("at"), r(x), r(y), ang], e, [Sym("uuid"), uid("l" + net)]])


def _power(net, x, y, out_ang):
    lib_id = "power:" + net
    rot = int((out_ang - pins(lib(lib_id))[0]["angle"]) % 360)
    _pwr[0] += 1
    _instance(lib_id, "#PWR%03d" % _pwr[0], net, x, y, rot=rot)


def pwr_flag(net, x, y):
    """Mark a net as driven (needed once per rail that only enters via a connector)."""
    x, y = snap(x), snap(y)
    _flg[0] += 1
    _instance("power:PWR_FLAG", "#FLG%02d" % _flg[0], "PWR_FLAG", x, y)
    wire(x, y, x, y + STUB)
    if net in POWER_NETS:
        _power(net, x, y + STUB, 270)
    else:
        label(net, x, y + STUB, 270)


def noconn(x, y):
    items.append([Sym("no_connect"), [Sym("at"), r(x), r(y)], [Sym("uuid"), uid("nc")]])


def place(lib_id, ref, value, x, y, conns, unit=1, footprint="", fields=None, dnp=False):
    """conns: {pin_number: net_name or None (no-connect)}. Every pin of the unit must appear."""
    x, y = snap(x), snap(y)
    _instance(lib_id, ref, value, x, y, unit=unit, footprint=footprint, fields=fields, dnp=dnp)
    done = set()
    for num, net in conns.items():
        px, py, oa = pin_geom(lib_id, x, y, unit, num)
        if (px, py) in done:
            continue
        done.add((px, py))
        if net is None:
            noconn(px, py)
            continue
        dx, dy = round(math.cos(math.radians(oa))), -round(math.sin(math.radians(oa)))
        ex, ey = px + dx * STUB, py + dy * STUB
        wire(px, py, ex, ey)
        if net in POWER_NETS:
            _power(net, ex, ey, oa)
        else:
            label(net, ex, ey, int(oa))


def text(t, x, y, size=2.54):
    items.append([Sym("text"), t, [Sym("exclude_from_sim"), Sym("no")], [Sym("at"), r(x), r(y), 0],
                  [Sym("effects"), [Sym("font"), [Sym("size"), size, size], [Sym("bold"), Sym("yes")]],
                   [Sym("justify"), Sym("left"), Sym("bottom")]], [Sym("uuid"), uid("t")]])


def res(ref, val, x, y, a, b, footprint=None):
    place(R, ref, val, x, y, {"1": a, "2": b}, footprint=footprint or FP["R"])


def cap(ref, val, x, y, a, b, pol=False, film=False):
    """pol=True: a = + (pin 1), b = - (pin 2)."""
    fp = FP["CP"] if pol else FP["C_FILM"] if film else FP["C"]
    place(CP if pol else C, ref, val, x, y, {"1": a, "2": b}, footprint=fp)


def emit(erc_exclusions=()):
    """Write <project>.kicad_sch and <project>.kicad_pro next to this file."""
    sch = [Sym("kicad_sch"), [Sym("version"), Sym("20250114")], [Sym("generator"), "eeschema"],
           [Sym("generator_version"), "9.0"], [Sym("uuid"), _state["root"]], [Sym("paper"), _state["paper"]],
           [Sym("title_block"), [Sym("title"), _state["title"]], [Sym("rev"), _state["rev"]],
            [Sym("comment"), 1, "Generated by hardware/gen_sch.py from docs/SPEC.md - edit the generator"]],
           [Sym("lib_symbols")] + list(lib_symbols.values())] + items + [
        [Sym("sheet_instances"), [Sym("path"), "/", [Sym("page"), "1"]]], [Sym("embedded_fonts"), Sym("no")]]
    out = os.path.join(_state["dir"], _state["project"] + ".kicad_sch")
    with open(out, "w") as f:
        f.write(dump(sch) + "\n")
    with open(f"{KICAD_SHARE}/template/kicad.kicad_pro") as f:
        pro = json.load(f)
    pro["meta"]["filename"] = _state["project"] + ".kicad_pro"
    pro["erc"] = {"erc_exclusions": [list(e) for e in erc_exclusions]}
    with open(os.path.join(_state["dir"], _state["project"] + ".kicad_pro"), "w") as f:
        json.dump(pro, f, indent=2)
    print(f"wrote {out}: {len(items)} items, {len(lib_symbols)} lib symbols")
