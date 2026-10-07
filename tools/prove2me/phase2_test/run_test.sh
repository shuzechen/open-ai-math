#!/bin/bash
# Build the two staged Phase 2 test cases with per-module timing.
export PATH="$HOME/.elan/bin:$PATH"
cd /tmp/claude-0/-home-user/ed69dbd8-3ad7-5b81-913c-42b086063fe9/scratchpad/p2m_lean
mods=(Definitions.Def_TruffetCounterexample
      Theorems.Thm_OAI_TruffetV4Counterexample_finite_execution_not_optimal
      Solutions.Sol_OAI_TruffetV4Counterexample_finite_execution_not_optimal
      Solutions.Eval_Truffet
      Definitions.Def_FiniteCongruenceGraph
      Definitions.Def_FCG_Congruence
      Definitions.Def_FCG_GraphCriterion
      Theorems.Thm_OAI_FiniteCongruence_graph_criterion
      Solutions.Sol_OAI_FiniteCongruence_graph_criterion
      Solutions.Eval_FCG)
for m in "${mods[@]}"; do
  s=$(date +%s.%N)
  out=$(lake build "$m" 2>&1); rc=$?
  e=$(date +%s.%N)
  printf '%-75s rc=%d  %6.1fs\n' "$m" "$rc" "$(echo "$e - $s" | bc)"
  if [ $rc -ne 0 ]; then echo "$out" | grep -E "error|warning: declaration uses|^\S+\.lean:[0-9]+" | head -20; fi
  echo "$out" | grep -E "sorry|axioms" | head -5
done
