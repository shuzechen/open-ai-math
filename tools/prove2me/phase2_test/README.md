# Phase 2 quick test (proof transplant), 2026-10-07

Two Comparator challenges carried end-to-end from the OAI proof tree to the
Prove2Me layout and checked the way the platform checks them
(`theorem _check : @<target> = @solution := rfl`, then `#print axioms`).

Environment: Lean 4.33.1, Mathlib 0df444a (the Phase 1 target). Phase 1's
`Def_<X>` / `Thm_<X>` files are taken verbatim from the prove2me/oai-math-oct-2026
split; they are not copied here.

| case | OAI closure | layout | Sol build (4 cores) | result |
|---|---|---|---|---|
| TruffetCounterexample | 2 files, 269 lines | Phase 1 Def + one Sol (16 lemmas inlined) | 27 s | type-equal, axioms = propext/choice/Quot.sound |
| FiniteCongruenceGraph | 2 files, 469 lines | Phase 1 Def + 2 support Def bundles (OAI defs/lemmas minus the 9 names Phase 1 already declares) + one Sol | 13 s | same |

No proof text was changed for Lean 4.33.1.

- `setup_lean.sh`: builds a scratch lake project pinned like Phase 1 and fetches the Mathlib cache (~4 min, 7.5 GB).
- `run_test.sh`: builds Def → Thm → Sol → Eval for both cases with per-module timing.
- `Definitions/`, `Solutions/`: the generated support bundles, solutions and eval files.
  They were produced with `convert_challenges.split_blocks` plus hand fixes
  (dropping `omit … in` wrappers of deleted declarations); the real pipeline
  must take positions from the Prove2Me Stage 1/2 Lean scripts instead.
