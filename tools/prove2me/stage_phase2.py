#!/usr/bin/env python3
"""Quick-test stager for Phase 2: carry one Comparator challenge's OAI proof
closure into the Prove2Me layout and emit the platform-style Eval check.

Layout produced under --lake (a lake project with Definitions/Theorems/Solutions libs):

  Definitions/Def_<Chal>.lean, Theorems/Thm_<fq>.lean   copied from the Phase 1 split
  Definitions/Def_<Chal>__<module slug>.lean             every OAI module of the closure,
                                                         minus defs the Phase 1 Def already
                                                         declares, minus the target theorems
  Solutions/Sol_<fq>.lean                                private lemmas of the target's module
                                                         + the target hoisted to `theorem solution`
  Solutions/Eval_<fq>.lean                               `theorem _check : @<fq> = @solution := rfl`

Positions come from convert_challenges.split_blocks (line-based); this is the
quick-test tool, not the Stage 1/2 pipeline.  Everything it writes is meant
to be compiled, never uploaded.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import convert_challenges as cc  # noqa: E402

LEAN = cc.LEAN
WRAP = re.compile(r"^(omit|include|set_option|open)\b.*\bin\s*$", re.S)

# Lean 4.34.1 -> 4.33.1 compatibility, same rules as the Phase 1 split (its README).
IMPORT_RENAMES = {
    "Mathlib.Basic.Complex.Basic": "Mathlib.Data.Complex.Basic",
    "Mathlib.Basic.Real.Basic": "Mathlib.Data.Real.Basic",
}
THEOREM_ALIASES = {
    "ite_eq_left": "private theorem ite_eq_left.{u} {c : Prop} {h : Decidable c} (hc : c) {α : Sort u} {t e : α} : (ite c t e) = t := @if_pos c h hc α t e",
    "ite_eq_right": "private theorem ite_eq_right.{u} {c : Prop} {h : Decidable c} (hc : ¬c) {α : Sort u} {t e : α} : (ite c t e) = e := @if_neg c h hc α t e",
    "dite_eq_left": "private theorem dite_eq_left.{u} {c : Prop} {h : Decidable c} (hc : c) {α : Sort u} {t : c → α} {e : ¬c → α} : (dite c t e) = t hc := @dif_pos c h hc α t e",
    "dite_eq_right": "private theorem dite_eq_right.{u} {c : Prop} {h : Decidable c} (hc : ¬c) {α : Sort u} {t : c → α} {e : ¬c → α} : (dite c t e) = e hc := @dif_neg c h hc α t e",
}


COMPAT_BUNDLE = "Definitions.Def_Compat433"   # the Phase 1 backports (TensorProduct.inductionOn, MfldCat, …)


def compat(text: str) -> str:
    """Apply the import renames, import the shared backport bundle, and insert
    the private 4.33 aliases after the import block."""
    for old, new in IMPORT_RENAMES.items():
        text = text.replace(f"import {old}\n", f"import {new}\n")
    body = re.sub(r"^import .*$", "", text, flags=re.M)
    needed = [THEOREM_ALIASES[n] for n in THEOREM_ALIASES if re.search(r"\b" + n + r"\b", body)]
    lines = text.split("\n")
    last_import = max((i for i, ln in enumerate(lines) if ln.startswith("import ")), default=-1)
    extra = [f"import {COMPAT_BUNDLE}"]
    if needed:
        extra += ["", "-- Lean 4.33.1 equivalents of the Lean 4.34 theorem names."] + needed
    lines[last_import + 1:last_import + 1] = extra
    return "\n".join(lines)


def slug(mod: str) -> str:
    return mod.replace(".", "_")


def closure(graph: dict, root: str) -> list[str]:
    seen, order, st = set(), [], [root]
    while st:
        x = st.pop()
        if x in seen:
            continue
        seen.add(x)
        order.append(x)
        st += [i for i in graph.get(x, []) if i in graph]
    return order


def module_imports(mod: str) -> list[str]:
    text = open(os.path.join(LEAN, mod.replace(".", "/") + ".lean"), encoding="utf-8").read()
    return cc.imp_re.findall(text[:20000]) if hasattr(cc, "imp_re") else re.findall(r"^import\s+([\w.«»\-]+)", text, re.M)


def rewrite_imports(block_text: str, chal: str, in_closure: set[str]) -> str:
    out = []
    for line in block_text.rstrip("\n").split("\n"):
        m = re.match(r"^import\s+([\w.«»\-]+)", line)
        if m and m.group(1).startswith("OAI."):
            mod = m.group(1)
            out.append(f"import Definitions.Def_{chal}__{slug(mod)}" if mod in in_closure else f"-- dropped: import {mod}")
        else:
            out.append(line)
    return "\n".join(out) + "\n"


def subtract(mod: str, chal: str, drop_fq: set[str], in_closure: set[str]) -> tuple[str, list[str], list[cc.Block]]:
    path = os.path.join(LEAN, mod.replace(".", "/") + ".lean")
    bs = cc.split_blocks(open(path, encoding="utf-8").read())
    out: list[str] = []
    dropped: list[str] = []
    for b in bs:
        if b.kind == "import":
            out.append(rewrite_imports(b.text, chal, in_closure))
            continue
        if b.fq in drop_fq:
            dropped.append(b.fq)
            while out and WRAP.match(out[-1].strip()):   # wrapper of a deleted declaration
                out.pop()
            continue
        out.append(b.text)
    text = "\n".join(out)
    text = compat(re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n")
    return text, dropped, bs


def stage(chal: str, lake: str, phase1: str, graph: dict) -> dict:
    cfg = json.load(open(os.path.join(cc.CHAL, chal + ".json")))
    root = cfg["solution_module"]
    targets = list(cfg["theorem_names"])
    mods = closure(graph, root)
    in_closure = set(mods)
    chal_blocks = cc.split_blocks(open(os.path.join(cc.CHAL, chal + ".lean"), encoding="utf-8").read())
    dup = {b.fq for b in chal_blocks if b.kind in ("def", "mutual") and b.fq}
    report = {"challenge": chal, "root": root, "closure": mods, "targets": targets, "dup_defs_removed": {}, "bundles": [], "sols": [], "warnings": []}

    # Phase 1 artifacts
    for d in ("Definitions", "Theorems", "Solutions"):
        os.makedirs(os.path.join(lake, d), exist_ok=True)
    p1def = os.path.join(phase1, "Definitions", f"Def_{chal}.lean")
    has_p1def = os.path.exists(p1def)
    if has_p1def:
        shutil.copy(p1def, os.path.join(lake, "Definitions"))
    for t in targets:
        src = os.path.join(phase1, "Theorems", f"Thm_{slug(t)}.lean")
        if not os.path.exists(src):
            report["warnings"].append(f"Phase 1 stub missing: {src}")
            continue
        shutil.copy(src, os.path.join(lake, "Theorems"))

    # support bundles, one per OAI module (dependencies first)
    for mod in reversed(mods):
        text, dropped, _ = subtract(mod, chal, dup | set(targets), in_closure)
        if dropped:
            report["dup_defs_removed"][mod] = dropped
        if has_p1def:
            text = f"import Definitions.Def_{chal}\n" + text
        name = f"Def_{chal}__{slug(mod)}"
        with open(os.path.join(lake, "Definitions", name + ".lean"), "w", encoding="utf-8") as f:
            f.write(text)
        report["bundles"].append(name)
        if re.search(r"^\s*(macro|syntax|elab|macro_rules|run_cmd|run_elab)\b", text, re.M):
            report["warnings"].append(f"{name}: contains elaboration-time commands the platform code guard rejects")

    # one Sol per target: private lemmas of its module + the target hoisted
    for t in targets:
        tmod = next((m for m in mods if any(b.fq == t for b in cc.split_blocks(open(os.path.join(LEAN, m.replace('.', '/') + '.lean'), encoding='utf-8').read()))), None)
        if tmod is None:
            report["warnings"].append(f"{t}: not found as a top-level theorem in the closure")
            continue
        bs = cc.split_blocks(open(os.path.join(LEAN, tmod.replace(".", "/") + ".lean"), encoding="utf-8").read())
        idx = next(i for i, b in enumerate(bs) if b.fq == t)
        tb = bs[idx]
        imports = [f"import Definitions.Def_{chal}"] if has_p1def else []
        imports += [f"import Definitions.Def_{chal}__{slug(m)}" for m in reversed(mods)]
        imports += [ln for ln in (b.text.strip() for b in bs if b.kind == "import") if not ln.startswith("import OAI.")]
        pre = [ln for ln in cc.preamble_at(bs, idx) if not WRAP.match(ln.strip())]
        privates = [b.text for b in bs[:idx] if b.kind in ("thm", "def") and re.search(r"^\s*(?:@\[[^\]]*\]\s*)?private\b", b.text, re.M)]
        wrapper = bs[idx - 1].text.strip() + "\n" if idx and bs[idx - 1].kind == "scope" and WRAP.match(bs[idx - 1].text.strip()) else ""
        body = cc.strip_docstring_and_attrs(tb.text)
        body = re.sub(r"^(" + cc.MODIFIERS + r")(theorem|lemma)\s+" + re.escape(tb.name), "theorem solution", body, count=1)
        ns = ".".join(tb.ns)
        parts = ["\n".join(imports), "", "\n".join(pre), ""]
        if privates:
            parts += [f"namespace {ns}", "", "\n".join(privates), f"end {ns}", ""]
        parts += [wrapper + body.rstrip(), ""]
        sol = compat("\n".join(parts))
        sname = f"Sol_{slug(t)}"
        with open(os.path.join(lake, "Solutions", sname + ".lean"), "w", encoding="utf-8") as f:
            f.write(sol)
        with open(os.path.join(lake, "Solutions", f"Eval_{slug(t)}.lean"), "w", encoding="utf-8") as f:
            f.write(f"import Theorems.Thm_{slug(t)}\nimport Solutions.{sname}\n\n"
                    f"theorem _check : @{t} = @solution := rfl\n#print axioms _check\n#print axioms solution\n")
        report["sols"].append(sname)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lake", required=True, help="lake project with Definitions/Theorems/Solutions libs")
    ap.add_argument("--phase1", required=True, help="root of the Phase 1 split (has Definitions/ and Theorems/)")
    ap.add_argument("--graph", required=True, help="import graph json from imports.py")
    ap.add_argument("names", nargs="+")
    a = ap.parse_args()
    graph = json.load(open(a.graph))
    for nm in a.names:
        r = stage(nm, a.lake, a.phase1, graph)
        print(f"{nm}: closure={len(r['closure'])} bundles={len(r['bundles'])} sols={len(r['sols'])} "
              f"dups_removed={sum(len(v) for v in r['dup_defs_removed'].values())}"
              + (f"  WARN: {'; '.join(r['warnings'])}" if r["warnings"] else ""))
        with open(os.path.join(a.lake, f"stage_{nm}.json"), "w") as f:
            json.dump(r, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
