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

## Organisation

- One mission per comparator row (one `ComparatorChallenges/<X>.lean`), named
  `<docs title> <roman numeral>: <row label>` (numeral only when the doc has several rows).
- Goal = first `theorem_names` entry; further entries of the same row = milestones titled by
  the preprint's numbering; the row's Def bundle = definition reference item.
- Rows whose goal theorem is already the goal of an existing mission (marwahaha's or wurtle's,
  see `missions_all.jsonl` logic in the session notes) are skipped.
- `DESCRIPTION_RULES.md` is the brief for drafting a description from `materials/<X>.json`
  (docs page + challenge Lean + platform statements + preprint pages + bibliography);
  `assemble_specs.py` turns `plan10.json` + `drafts/` into `proposals/<X>.json`.

First ten proposals (all Draft, see `plan10.json`): DirichletSevenEighths, HeckeSevenEighths,
OrdinaryElliott, OstmannPrimes, Jacobsthal, TotientCompanionZero, EgyptianFractions,
CommutingDerivations, BrennanSharp, PlanarFalconer. The human submits them from the website
(My missions → confirm items → Submit Proposal).
