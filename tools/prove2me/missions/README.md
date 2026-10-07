# Missions for the OpenAI Math release (Prove2Me)

One mission per `lean/docs/NNN.md`: the doc's comparator theorems (already published on
Prove2Me by the Phase 1 upload, names = OAI fully-qualified names; definition bundles are
named after the challenge, e.g. `HeckeSevenEighths`) are added as `reference` items, the
headline result is the goal (`main_item_id`), the other comparator theorems become
milestones titled by their index in the preprint.

```
cp credentials.json tools/prove2me/missions/   # {"api_key": "p2m_..."} — never committed
python3 tools/prove2me/missions/make_proposal.py tools/prove2me/missions/proposals/003_quasi_riemann.json
```

`make_proposal.py` is idempotent: a Draft with the same name is reused, missing items are
added, order/goal/milestones are re-applied. Look up theorem ids with
`GET /theorems?theorem_name=<exact name>` (the `q=` search times out on the current library size).

Done so far: `003_quasi_riemann` (proposal `0969ce86-ba6c-4c0e-aae2-eba1ec72aa67`),
`005_catalan` (proposal `4577d8a1-b3af-424c-9278-3f7e04db991f`). Both are Drafts; the
human submits them from the website (My missions → confirm items → Submit Proposal).
