# Writing a Prove2Me mission description for one OpenAI Math comparator row

You are given ONE materials JSON (fields: mission_name, family_title, row, nrows, label, challenge, doc_md,
challenge_lean, theorems[{name,id,formal_statement,preamble,nl}], definition{name,id,nl,definition} or null,
siblings[{row,label,challenge,theorems,existing_mission}], preprints[{title,dir,url,text,bib}], lean_url).

Write TWO files:
1. `<challenge>.md` — the mission description (Markdown + KaTeX: `$..$` inline, `$$..$$` display).
2. `<challenge>.milestones.json` — a JSON list, one entry per theorem in `theorems[1:]` (empty list if only one
   theorem): `{"theorem_id": ..., "milestone_title": ..., "milestone_description": ...}`.
   - milestone_title ≤ 200 chars and MUST start with the index in the source ("Theorem 1.2 — …", "Lemma 3.1 — …",
     "Corollary 4 — …"); if the preprint is unavailable use the Lean name's role ("Supporting theorem: …").
   - milestone_description: the lemma's statement in prose, faithful to the source (verbatim where possible),
     followed by one sentence naming the Lean hypotheses that pin it down. Never paste the natural-language
     statement from the platform wholesale.

## Description structure (exactly these `##` headings, in this order)
1. `## Motivation` — who cares and why, concretely, with citations. Add a short *Timeline* paragraph (who proved
   what, when, under which hypotheses) when there is genuine history; skip it otherwise.
2. `## Setting` — define the objects operationally from scratch, introducing every symbol; use the same notation
   as the Lean statement. Define before you cite.
3. `## Formalization targets` — `### Goal` with the target in display math, then what it leaves unfixed. If the
   row has several theorems, `### Milestones` listing each (same titles as the milestones file).
   Add a `### Related missions` list naming the sibling rows of the same family: for siblings with
   `existing_mission` write `- Row N (label): mission "<name>" (https://prove2.me/missions/<id>)`; for siblings
   without one write `- Row N (label): no mission yet; goal theorem(s) <names>`. Say in one sentence how this
   row relates to them (independent result / stronger / special case / transfer), and that solvers may import
   sibling theorems that are already published on the platform as reductions.
4. `## Significance` — what the result gives, and what formalizing it adds. Be honest about status: the result is
   proved on paper in the OpenAI preprint (if one is listed) and admitted with `sorry` in Lean; nothing is
   machine-checked yet. Distinguish "proved" from "formalized".
5. `## Difficulty` — which step of the obvious argument fails and why; rule out the newcomer's first idea. No
   proof strategy beyond what the preprint's introduction says.
6. `## Formalization scope` — the Lean representation and every convention the statement commits to
   (finiteness, nonemptiness, casts, which `tsum`/`sSup`, degenerate inputs of total functions, decidability
   instances, hypotheses that exclude trivial cases). Quote the Lean statement in a ```lean block. Say that the
   theorem (and the definition bundle, if any) is already published verbatim from openai/math commit adc7f12 in
   the default environment (Lean 4.33.1, Mathlib 0df444a) and referenced, not redrafted. If a trivializing
   reading exists, rule it out in one sentence. List infrastructure needed and which contributions are welcome.
7. `## Selected references` — author, title, venue, year, resolvable link. ALWAYS include the OpenAI preprint(s)
   (use `url`) and the Lean statement (`lean_url`). Other references ONLY from the preprint's bibliography (`bib`)
   or classical works you are certain of, with DOI/arXiv links from the bib. NEVER invent a reference, a year, a
   venue, or a DOI. If `preprints` is empty, cite only the Lean statement, the docs page
   https://github.com/openai/math/blob/main/lean/docs/<doc> and well-known classical references you are sure of.

## Style
- Neutral register: no "beautiful", "groundbreaking", "exciting". No first person, no meta-commentary.
- 800–1500 words. Bold each technical term at first use. One definition per source concept.
- Faithfulness over everything: every hypothesis and conclusion of the Lean statement must be reflected in the
  prose Target/Scope; do not claim more or less than the Lean statement says. Read `formal_statement` and `nl`
  carefully; use `challenge_lean` and `definition.definition` to understand the definitions the statement uses.
- Do not mention this instruction file, the platform API, or the writing process.
