#!/usr/bin/env python3
"""Prototype: turn lean/ComparatorChallenges/X.lean + X.json into Prove2Me-style files.

Phase A of the Prove2Me migration: statements only (no proofs).  For each
challenge we emit

  Definitions/Def_OAI_Challenge_<X>.lean   the challenge file minus the target
                                            theorems (defs, instances, helper
                                            lemmas; skipped when empty)
  Theorems/Thm_<slug>.lean                  one sorry-stub per theorem_name:
                                            preamble + formal_statement
  meta/<X>.json                             upload payloads (submit-definition /
                                            submit-problem bodies) + plan

Scope: the Comparator challenge files are uniform (import Mathlib, `namespace
OAI`, column-0 commands, `theorem ... := by\n  sorry`), so a line-based block
splitter is enough here.  This is NOT the official skeleton-subtraction oracle
(scripts/extract_sketch_info.lean) and must not be reused for the OAI proof
tree.  Every output has to be compile-checked (lake build) before upload.

Usage:
  python3 tools/prove2me/convert_challenges.py --out /path/to/out NAME [NAME ...]
  python3 tools/prove2me/convert_challenges.py --out /path/to/out --all
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAN = os.path.join(ROOT, "lean")
CHAL = os.path.join(LEAN, "ComparatorChallenges")
DOCS = os.path.join(LEAN, "docs")
REPO_URL = "https://github.com/shuzechen/open-ai-math"
DEF_PREFIX = "OAI_Challenge_"

MODIFIERS = r"(?:(?:private|protected|noncomputable|unsafe|partial|nonrec|scoped|local)\s+)*"
DECL_KW = r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|axiom|opaque|example)"
DECL_RE = re.compile(r"^" + MODIFIERS + DECL_KW + r"\b")
THM_RE = re.compile(r"^" + MODIFIERS + r"(theorem|lemma)\s+([^\s:({\[]+)")
SCOPE_KW = ("namespace", "section", "noncomputable section", "end", "open", "universe",
            "variable", "set_option", "attribute", "notation", "local notation",
            "local instance", "scoped notation", "include", "omit", "macro", "syntax",
            "macro_rules", "elab", "export", "alias", "deriving instance", "initialize",
            "declare_syntax_cat", "infix", "infixl", "infixr", "prefix", "postfix")
SCOPE_RE = re.compile(r"^(" + "|".join(re.escape(k) for k in SCOPE_KW) + r")\b")


@dataclass
class Block:
    kind: str                 # import | scope | def | thm | comment | mutual | hash
    text: str
    start: int                # 1-based line
    end: int
    name: str | None = None   # short declared name for def/thm
    fq: str | None = None     # namespace-qualified name
    ns: tuple[str, ...] = ()  # namespace stack at the block


def starts_command(line: str) -> bool:
    if not line or line[0] in " \t":
        return False
    return bool(DECL_RE.match(line) or SCOPE_RE.match(line) or line.startswith(("import ", "@[", "/--", "/-!", "/-", "#", "mutual", "--")))


def split_blocks(text: str) -> list[Block]:
    """Split a challenge file into column-0 command blocks.

    Comment / docstring / attribute lines are merged into the declaration that
    follows them, `mutual … end` is one block, and block comments `/- … -/`
    are never split in the middle."""
    lines = text.split("\n")
    n = len(lines)
    i = 0
    raw: list[tuple[int, int]] = []   # (start_idx, end_idx exclusive)
    while i < n:
        if not starts_command(lines[i]):
            i += 1
            continue
        start = i
        # swallow a block comment that begins here
        if lines[i].startswith("/-"):
            while i < n and "-/" not in lines[i]:
                i += 1
            i += 1
        elif lines[i].startswith("mutual"):
            i += 1
            while i < n and lines[i].rstrip() != "end":
                i += 1
            i += 1
        else:
            i += 1
        while i < n and not starts_command(lines[i]):
            i += 1
        raw.append((start, i))
    # merge leading comments/docstrings/attributes into the following block
    merged: list[tuple[int, int]] = []
    pending: int | None = None
    for s, e in raw:
        head = lines[s]
        attach = head.startswith(("/--", "@[", "--")) or (head.startswith("/-") and not head.startswith("/-!"))
        if attach:
            if pending is None:
                pending = s
            continue
        merged.append((pending if pending is not None else s, e))
        pending = None
    if pending is not None:
        merged.append((pending, n))

    blocks: list[Block] = []
    ns: list[str] = []
    for s, e in merged:
        body = "\n".join(lines[s:e])
        # first non-attached line decides the kind
        j = s
        while j < e and lines[j].startswith(("/--", "@[", "--")) or (j < e and lines[j].startswith("/-") and not lines[j].startswith("/-!")):
            if lines[j].startswith("/-") and "-/" not in lines[j]:
                while j < e and "-/" not in lines[j]:
                    j += 1
            j += 1
        head = lines[j] if j < e else ""
        kind, name = "def", None
        if head.startswith("import "):
            kind = "import"
        elif head.startswith("/-!") or head.startswith("--"):
            kind = "comment"
        elif head.startswith("#"):
            kind = "hash"
        elif head.startswith("mutual"):
            kind = "mutual"
        elif SCOPE_RE.match(head):
            kind = "scope"
        else:
            m = THM_RE.match(head)
            if m:
                kind, name = "thm", m.group(2)
            else:
                m2 = re.match(r"^" + MODIFIERS + DECL_KW + r"\s+([^\s:({\[]+)", head)
                if m2 and m2.group(1) not in ("instance", "example"):
                    name = m2.group(2)
        blk = Block(kind, body, s + 1, e, name, None, tuple(ns))
        if name:
            blk.fq = ".".join(ns + [name]) if ns else name
        blocks.append(blk)
        if kind == "scope":
            if head.startswith("namespace "):
                ns.append(head.split()[1])
            elif head.startswith("end "):
                tgt = head.split()[1]
                if ns and ns[-1] == tgt:
                    ns.pop()
    return blocks


@dataclass
class Scope:
    label: str | None        # namespace name, or None for section
    lines: list[str] = field(default_factory=list)
    noncomputable: bool = False


def preamble_at(blocks: list[Block], idx: int) -> list[str]:
    """Flatten the scope commands in effect at block idx into a preamble.

    namespace A / namespace B  ->  open A, open A.B   (full path)
    section … end              ->  dropped with everything declared inside
    open / universe / variable / set_option / attribute / notation -> kept verbatim
    noncomputable section      ->  emitted once if still active"""
    stack: list[Scope] = [Scope("<root>")]
    ns_path: list[str] = []
    for b in blocks[:idx]:
        if b.kind != "scope":
            continue
        head = b.text.strip().split("\n")[-1] if b.text.strip().startswith("--") else b.text.strip().split("\n")[0]
        # scope blocks are single commands; use the command text without trailing blanks
        cmd = b.text.rstrip()
        if cmd.startswith("namespace "):
            nm = cmd.split()[1]
            ns_path.append(nm)
            stack.append(Scope(nm))
            stack[-1].lines.append(f"open {'.'.join(ns_path)}")
        elif cmd.startswith("noncomputable section"):
            stack.append(Scope(None, noncomputable=True))
        elif cmd.startswith("section"):
            stack.append(Scope(None))
        elif cmd.startswith("end"):
            parts = cmd.split()
            if len(parts) == 1:
                # anonymous end: closes innermost unnamed section
                for k in range(len(stack) - 1, 0, -1):
                    if stack[k].label is None:
                        del stack[k:]
                        break
            else:
                tgt = parts[1]
                for k in range(len(stack) - 1, 0, -1):
                    if stack[k].label == tgt:
                        del stack[k:]
                        if ns_path and ns_path[-1] == tgt:
                            ns_path.pop()
                        break
        else:
            stack[-1].lines.append(cmd)
    out: list[str] = []
    if any(s.noncomputable for s in stack):
        out.append("noncomputable section")
    for s in stack:
        out.extend(s.lines)
    return out


def strip_docstring_and_attrs(text: str) -> str:
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("/--") or (ln.startswith("/-") and not ln.startswith("/-!")):
            while i < len(lines) and "-/" not in lines[i]:
                i += 1
            i += 1
        elif ln.startswith(("@[", "--")) or not ln.strip():
            i += 1
        else:
            break
    return "\n".join(lines[i:]).rstrip()


def make_stub(block: Block, fq: str) -> str:
    body = strip_docstring_and_attrs(block.text)
    # rename to the fully-dotted name (binding occurrence only)
    body = re.sub(r"^(" + MODIFIERS + r")(theorem|lemma)\s+" + re.escape(block.name), r"\1theorem " + fq, body, count=1)
    body = re.sub(r"^protected\s+", "", body)
    # normalise the proof to `:= by sorry`
    m = re.search(r":=\s*by\s+sorry\s*$", body)
    if m:
        body = body[: m.start()] + ":= by sorry"
    else:
        m = re.search(r":=\s*(by)?\s*$", body)
        if m:
            raise ValueError(f"{fq}: unexpected proof shape (ends with ':=' but no sorry)")
        raise ValueError(f"{fq}: cannot find ':= by sorry' at the end of the declaration")
    return body


# ---------------------------------------------------------------- metadata --

def load_docs() -> tuple[dict[str, list[dict]], dict[str, dict]]:
    """challenge name -> [{family, title}] ; family -> {papers, scope}"""
    chal2fam: dict[str, list[dict]] = {}
    fam: dict[str, dict] = {}
    for fn in sorted(os.listdir(DOCS)):
        if not fn.endswith(".md"):
            continue
        fid = fn[:-3]
        s = open(os.path.join(DOCS, fn), encoding="utf-8").read()
        papers = re.findall(r"^- \[([^\]]+)\]\(\.\./\.\./preprints/([^)]+)\)", s, re.M)
        title = s.split("\n", 1)[0].lstrip("# ").strip()
        scope = ""
        m = re.search(r"^## Scope\s*\n(.*?)(?=^## |\Z)", s, re.M | re.S)
        if m:
            scope = m.group(1).strip()
        fam[fid] = {"title": title, "papers": [{"title": t, "path": p} for t, p in papers], "scope": scope}
        for row_title, name in re.findall(r"^\|\s*([^|]+?)\s*\|\s*\[[^\]]+\]\(\.\./ComparatorChallenges/(\w+)\.lean\)", s, re.M):
            chal2fam.setdefault(name, []).append({"family": fid, "title": row_title})
    return chal2fam, fam


def kebab(s: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", s).lower()


# ---------------------------------------------------------------- driver ----

def convert(name: str, out: str, sha: str, chal2fam, fam) -> dict:
    lean_path = os.path.join(CHAL, name + ".lean")
    cfg = json.load(open(os.path.join(CHAL, name + ".json")))
    text = open(lean_path, encoding="utf-8").read()
    blocks = split_blocks(text)
    targets = set(cfg["theorem_names"])
    found = {b.fq: i for i, b in enumerate(blocks) if b.kind == "thm" and b.fq in targets}
    missing = targets - set(found)
    if missing:
        raise ValueError(f"{name}: theorem_names not found as top-level theorems: {sorted(missing)}")

    imports = [b.text.strip() for b in blocks if b.kind == "import"]
    rest = [b for i, b in enumerate(blocks) if i not in found.values()]
    has_content = any(b.kind in ("def", "thm", "mutual", "hash") for b in rest)
    def_name = DEF_PREFIX + name
    rows = chal2fam.get(name, [])
    fams = sorted({r["family"] for r in rows})
    field = cfg["solution_module"].split(".")[1]
    tags = ["open-ai-math", kebab(field)] + [f"family-{f}" for f in fams]
    papers = [p for f in fams for p in fam[f]["papers"]]
    src_common = (f"{REPO_URL}/blob/{sha}/lean/ComparatorChallenges/{name}.lean ; "
                  + " ; ".join(f"{p['title']} — {REPO_URL}/blob/{sha}/preprints/{p['path']}" for p in papers))
    plan = {"challenge": name, "definition": None, "theorems": [], "warnings": []}

    if has_content:
        def_text = "\n".join(b.text for b in rest).rstrip() + "\n"
        def_text = re.sub(r"\n{3,}", "\n\n", def_text)
        if re.search(r"\bsorry\b", def_text):
            plan["warnings"].append("definition bundle contains `sorry` — the platform will reject it; needs manual repair")
        if re.search(r"^axiom\b", def_text, re.M):
            plan["warnings"].append("definition bundle contains `axiom` — not allowed on the platform")
        os.makedirs(os.path.join(out, "Definitions"), exist_ok=True)
        with open(os.path.join(out, "Definitions", f"Def_{def_name}.lean"), "w", encoding="utf-8") as f:
            f.write(def_text)
        plan["definition"] = {
            "definition_name": def_name,
            "definition_title": f"Definitions for {rows[0]['title'] if rows else name}",
            "definition": def_text,
            "natural_language_statement": "DRAFT — " + (fam[fams[0]]["scope"] if fams else ""),
            "source": src_common,
            "tags": tags,
        }

    os.makedirs(os.path.join(out, "Theorems"), exist_ok=True)
    for fq, i in found.items():
        b = blocks[i]
        pre = []
        pre += [f"import Definitions.Def_{def_name}"] if has_content else []
        pre += imports
        pre += preamble_at(blocks, i)
        preamble = "\n".join(pre)
        stmt = make_stub(b, fq)
        slug = fq.replace(".", "_")
        with open(os.path.join(out, "Theorems", f"Thm_{slug}.lean"), "w", encoding="utf-8") as f:
            f.write(preamble + "\n\n" + stmt + "\n")
        doc = re.search(r"/--(.*?)-/", b.text, re.S)
        title = rows[0]["title"] if len(rows) == 1 else (rows[0]["title"] + f" — {b.name}" if rows else fq)
        plan["theorems"].append({
            "theorem_name": fq,
            "theorem_title": title[:200],
            "preamble": preamble,
            "formal_statement": stmt,
            "natural_language_statement": "DRAFT — " + (doc.group(1).strip() if doc else "") + ("\n\n" + fam[fams[0]]["scope"] if fams else ""),
            "source": f"{REPO_URL}/blob/{sha}/lean/ComparatorChallenges/{name}.lean#L{b.start}-L{b.end} ; " + src_common.split(" ; ", 1)[1],
            "tags": tags,
        })
    os.makedirs(os.path.join(out, "meta"), exist_ok=True)
    with open(os.path.join(out, "meta", f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    return plan


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    sha = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip()
    chal2fam, fam = load_docs()
    names = a.names
    if a.all:
        names = sorted(f[:-5] for f in os.listdir(CHAL) if f.endswith(".lean"))
    ok = fail = 0
    for nm in names:
        try:
            plan = convert(nm, a.out, sha, chal2fam, fam)
            ok += 1
            w = f"  WARN: {'; '.join(plan['warnings'])}" if plan["warnings"] else ""
            print(f"ok   {nm}: def={'yes' if plan['definition'] else 'no '} thms={len(plan['theorems'])}{w}")
        except Exception as e:  # noqa: BLE001 - report and continue
            fail += 1
            print(f"FAIL {nm}: {e}")
    print(f"{ok} ok, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
