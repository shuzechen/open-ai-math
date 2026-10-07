#!/usr/bin/env python3
"""Turn plan10.json + drafts/<chal>.md + drafts/<chal>.milestones.json into proposals/<chal>.json specs."""
import json, os, sys
SP = os.path.dirname(os.path.abspath(__file__))
F = {"number-theory": "e76e77ab-38dd-426d-a533-0b37fb6dbabc", "algebraic-geometry": "d311bb23-6a7a-4f34-9f38-e55cf9e9c179",
     "algebra": "9a29f641-3f6a-4ce2-a4a6-1f6b1b4ee922", "analysis": "b2d3e691-5991-46d9-917d-047b9d4de3c7",
     "harmonic-analysis": "0a150745-b6ac-464f-872e-0f5cfd4d3558", "combinatorics": "55eec41b-ff24-45ad-96b6-49d7a6869286",
     "discrete-geometry": "eacb2bf6-9021-46c9-87ac-f30638efffb3"}
FIELDS = {"DirichletSevenEighths": ["number-theory"], "HeckeSevenEighths": ["number-theory"], "OrdinaryElliott": ["number-theory"],
          "OstmannPrimes": ["number-theory", "combinatorics"], "Jacobsthal": ["number-theory"], "TotientCompanionZero": ["number-theory"],
          "EgyptianFractions": ["number-theory", "combinatorics"], "CommutingDerivations": ["algebraic-geometry", "algebra"],
          "BrennanSharp": ["analysis"], "PlanarFalconer": ["harmonic-analysis", "discrete-geometry"]}
plan = json.load(open(f"{SP}/plan10.json"))
os.makedirs(f"{SP}/proposals", exist_ok=True)
for p in plan:
    c = p["challenge"]
    md = f"{SP}/drafts/{c}.md"; mj = f"{SP}/drafts/{c}.milestones.json"
    if not os.path.exists(md):
        print("MISSING draft", c); continue
    ms = json.load(open(mj)) if os.path.exists(mj) else []
    by = {m["theorem_id"]: m for m in ms}
    items = []
    if p["def_id"]:
        items.append({"theorem_id": p["def_id"], "role": "definition", "name": c})
    items.append({"theorem_id": p["goal"], "role": "goal"})
    for name, tid in p["milestones"]:
        m = by.get(tid)
        if not m:
            print(f"  {c}: no milestone text for {name}; adding as plain support item"); items.append({"theorem_id": tid, "role": "support", "name": name}); continue
        items.append({"theorem_id": tid, "role": "milestone", "name": name, "milestone_title": m["milestone_title"][:200], "milestone_description": m["milestone_description"]})
    spec = {"name": p["name"], "mission_type": "ResearchPaper", "field_ids": [F[f] for f in FIELDS[c]], "description_file": f"../drafts/{c}.md", "items": items}
    json.dump(spec, open(f"{SP}/proposals/{c}.json", "w"), ensure_ascii=False, indent=1)
    words = len(open(md).read().split())
    print(f"{c:24s} words={words:5d} items={len(items)} milestones={sum(1 for i in items if i['role']=='milestone')}")
