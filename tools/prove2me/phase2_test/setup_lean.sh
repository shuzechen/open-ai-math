#!/bin/bash
set -x
S=/tmp/claude-0/-home-user/ed69dbd8-3ad7-5b81-913c-42b086063fe9/scratchpad
cd $S/p2m_lean
echo "== $(date) install elan"
curl https://elan.lean-lang.org/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
export PATH="$HOME/.elan/bin:$PATH"
printf 'leanprover/lean4:v4.33.1\n' > lean-toolchain
cat > lakefile.lean <<'LF'
import Lake
open Lake DSL
package p2m where
  leanOptions := #[⟨`autoImplicit, false⟩]
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "0df444a360eaa60ab8c11dca51a86af692955474"
lean_lib Definitions where globs := #[`Definitions.+]
lean_lib Theorems where globs := #[`Theorems.+]
lean_lib Solutions where globs := #[`Solutions.+]
lean_lib OAI where globs := #[`OAI.+]
LF
mkdir -p Definitions Theorems Solutions OAI
echo "== $(date) lean toolchain"
elan toolchain install leanprover/lean4:v4.33.1 && lean --version
echo "== $(date) lake update"
lake update 2>&1 | tail -5
echo "== $(date) cache get"
lake exe cache get 2>&1 | tail -5
echo "== $(date) smoke"
mkdir -p Solutions && printf 'import Mathlib.Data.Real.Basic\nimport Mathlib.Tactic.Linarith\nexample (a b : ℝ) : a ^ 2 + b ^ 2 ≥ 2 * a * b := by nlinarith [sq_nonneg (a - b)]\n' > Solutions/SmokeTest.lean
time lake build Solutions.SmokeTest 2>&1 | tail -3
echo "== $(date) DONE"; du -sh .lake
