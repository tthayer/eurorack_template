"""Minimal KiCad s-expression parser/serializer and symbol-library helpers."""
import re

import os
SYMDIR = os.path.join(os.environ.get("KICAD_SHARE", "/Applications/KiCad/KiCad.app/Contents/SharedSupport"), "symbols")


class Sym(str):
    """Bare (unquoted) atom."""


def parse(text):
    tok = re.compile(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+')
    stack = [[]]
    for m in tok.finditer(text):
        t = m.group(0)
        if t == "(":
            stack.append([])
        elif t == ")":
            e = stack.pop()
            stack[-1].append(e)
        elif t.startswith('"'):
            stack[-1].append(t[1:-1].replace('\\"', '"').replace("\\\\", "\\"))
        else:
            stack[-1].append(Sym(t))
    return stack[0]


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def dump(e, ind=0):
    if isinstance(e, list):
        if not any(isinstance(x, list) for x in e):
            return "\t" * ind + "(" + " ".join(dump(x) for x in e) + ")"
        head = []
        rest = []
        for x in e:
            if isinstance(x, list) or rest:
                rest.append(x)
            else:
                head.append(x)
        s = "\t" * ind + "(" + " ".join(dump(x) for x in head)
        for x in rest:
            s += "\n" + (dump(x, ind + 1) if isinstance(x, list) else "\t" * (ind + 1) + dump(x))
        return s + "\n" + "\t" * ind + ")"
    if isinstance(e, Sym):
        return str(e)
    if isinstance(e, str):
        return q(e)
    if isinstance(e, float):
        return ("%.4f" % e).rstrip("0").rstrip(".")
    return str(e)


_libcache = {}


def load_lib(lib):
    if lib not in _libcache:
        with open(f"{SYMDIR}/{lib}.kicad_sym") as f:
            tree = parse(f.read())[0]
        _libcache[lib] = {x[1]: x for x in tree if isinstance(x, list) and x and x[0] == "symbol"}
    return _libcache[lib]


def get_flat(lib, name):
    """Return the symbol flattened (extends resolved), renamed to 'lib:name'."""
    import copy
    syms = load_lib(lib)
    s = copy.deepcopy(syms[name])
    ext = [x for x in s if isinstance(x, list) and x[0] == "extends"]
    if ext:
        parent = get_flat(lib, ext[0][1])
        pname = parent[1].split(":", 1)[1]
        cprops = [x for x in s if isinstance(x, list) and x[0] == "property"]
        cnames = {x[1] for x in cprops}
        # KiCad flattening: parent fields kept unless overridden by the child
        props = [x for x in parent if isinstance(x, list) and x[0] == "property" and x[1] not in cnames]
        props = [x for x in parent if isinstance(x, list) and x[0] == "property" and x[1] in cnames
                 for x in [next(c for c in cprops if c[1] == x[1])]] + props
        props += [c for c in cprops if c[1] not in {x[1] for x in props}]
        out = [Sym("symbol"), name]
        for x in parent[2:]:
            if isinstance(x, list) and x[0] == "property":
                continue
            out.append(x)
        # insert child props before first sub-symbol
        idx = next(i for i, x in enumerate(out) if isinstance(x, list) and x[0] == "symbol")
        out[idx:idx] = props
        for x in out:
            if isinstance(x, list) and x[0] == "symbol":
                x[1] = name + x[1][len(pname):]
        s = out
    s[1] = f"{lib}:{name}"
    return s


def pins(symflat):
    """List of dicts: unit, number, name, type, x, y, angle, length."""
    res = []
    base = symflat[1].split(":", 1)[1]
    for sub in symflat:
        if not (isinstance(sub, list) and sub[0] == "symbol"):
            continue
        m = re.match(re.escape(base) + r"_(\d+)_(\d+)$", sub[1])
        unit = int(m.group(1))
        for p in sub:
            if isinstance(p, list) and p[0] == "pin":
                d = {"unit": unit, "type": str(p[1])}
                for f in p:
                    if isinstance(f, list):
                        if f[0] == "at":
                            d["x"], d["y"] = float(f[1]), float(f[2])
                            d["angle"] = float(f[3]) if len(f) > 3 else 0.0
                        elif f[0] == "length":
                            d["length"] = float(f[1])
                        elif f[0] == "name":
                            d["name"] = f[1]
                        elif f[0] == "number":
                            d["number"] = f[1]
                res.append(d)
    return res
