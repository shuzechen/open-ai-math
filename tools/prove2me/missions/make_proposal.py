#!/usr/bin/env python3
"""Create (or update) a Prove2Me mission proposal from a JSON spec.

spec = {
  "name": ..., "mission_type": "ResearchPaper", "field_ids": [...], "description_file": "...md",
  "items": [ {"theorem_id": "...", "role": "definition"|"goal"|"milestone"|"support",
              "milestone_title": "...", "milestone_description": "..."} , ... ]   # in item_order
}
Idempotent: if a Draft proposal with the same name exists, it is reused and only missing items are added.
Only ever talks to https://prove2.me/api/v1.
"""
import json, subprocess, sys, os, time
SP = os.path.dirname(os.path.abspath(__file__))
BASE = "https://prove2.me/api/v1"

def token():
    return subprocess.check_output([os.path.join(SP, "tok.sh")], text=True).strip()

def api(method, path, body=None, ok=(200, 201, 204, 409)):
    cmd = ["curl", "-sS", "--retry", "5", "--retry-all-errors", "--retry-delay", "1",
           "-X", method, BASE + path, "-H", "Authorization: Bearer " + token(),
           "-H", "Content-Type: application/json", "-w", "\n%{http_code}"]
    if body is not None:
        cmd += ["-d", json.dumps(body)]
    out = subprocess.check_output(cmd, text=True)
    text, code = out.rsplit("\n", 1)
    code = int(code)
    data = json.loads(text) if text.strip() else {}
    if code not in ok:
        raise SystemExit(f"{method} {path} -> {code}: {text[:800]}")
    return code, data

def main(spec_path):
    spec = json.load(open(spec_path))
    desc = open(os.path.join(os.path.dirname(spec_path), spec["description_file"]), encoding="utf-8").read()
    # 1. reuse an existing Draft with the same name
    _, mine = api("GET", "/mission-proposals?limit=200")
    existing = [p for p in mine["proposals"] if p["name"] == spec["name"] and p["status"] in ("Draft", "Changes requested")]
    if existing:
        pid = existing[0]["id"]
        api("PATCH", f"/mission-proposals/{pid}", {"description": desc, "field_ids": spec["field_ids"], "mission_type": spec["mission_type"]})
        print("reusing proposal", pid)
    else:
        _, p = api("POST", "/mission-proposals", {"name": spec["name"], "description": desc,
                                                  "mission_type": spec["mission_type"], "field_ids": spec["field_ids"]})
        pid = p["id"]; print("created proposal", pid)
    # 2. reference items
    _, p = api("GET", f"/mission-proposals/{pid}")
    have = {it.get("theorem_id"): it["id"] for it in p["items"] if it.get("theorem_id")}
    order = []
    for it in spec["items"]:
        tid = it["theorem_id"]
        if tid in have:
            iid = have[tid]
        else:
            code, r = api("POST", f"/mission-proposals/{pid}/items", {"kind": "reference", "theorem_id": tid})
            iid = r["id"]; have[tid] = iid
            print(f"  added {it['role']:10s} {tid} -> item {iid}")
        it["item_id"] = iid
        order.append(iid)
    # 3. goal + order
    goal = [it for it in spec["items"] if it["role"] == "goal"]
    assert len(goal) == 1, "exactly one goal"
    api("PATCH", f"/mission-proposals/{pid}", {"main_item_id": goal[0]["item_id"], "item_order": order})
    # 4. milestones
    for it in spec["items"]:
        if it["role"] == "milestone":
            api("POST", f"/mission-proposals/{pid}/milestones",
                {"item_id": it["item_id"], "milestone_title": it["milestone_title"], "milestone_description": it["milestone_description"]})
            print(f"  milestone: {it['milestone_title']}")
    _, p = api("GET", f"/mission-proposals/{pid}")
    _, ms = api("GET", f"/mission-proposals/{pid}/milestones")
    print(json.dumps({"id": pid, "name": p["name"], "status": p["status"], "fields": [f["slug"] for f in p["fields"]],
                      "main_item_id": p["main_item_id"], "n_items": len(p["items"]),
                      "milestones": [m.get("title") for m in (ms.get("milestones", ms) if isinstance(ms, dict) else ms)]}, indent=1, ensure_ascii=False))
    return pid

if __name__ == "__main__":
    for s in sys.argv[1:]:
        main(s)
