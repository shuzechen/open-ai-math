-- Lean 4.33.1 / Mathlib 0df444a backports of names the OAI tree (Mathlib d13f23b) uses.
-- Verbatim from the Phase 1 split: scripts/compatibility/*.lean.txt
import Mathlib

-- ===== CharacterCriterion
-- Backport the two-case eliminator from Mathlib/LinearAlgebra/TensorProduct/Defs.lean
-- at d13f23b723b8a846827a245b89c10fc7d3f11612, using the 4.33.1 eliminator.
section Lean433TensorProductCompatibility
open scoped TensorProduct
variable {R M N : Type*} [CommSemiring R]
  [AddCommMonoid M] [AddCommMonoid N] [Module R M] [Module R N]
namespace TensorProduct
@[elab_as_elim, induction_eliminator]
protected theorem inductionOn {motive : M ⊗[R] N → Prop} (z : M ⊗[R] N)
    (tmul : ∀ x y, motive (x ⊗ₜ[R] y))
    (add : ∀ x y, motive x → motive y → motive (x + y)) : motive z :=
  TensorProduct.induction_on z
    (by simpa only [TensorProduct.zero_tmul] using tmul (0 : M) (0 : N)) tmul add
end TensorProduct
end Lean433TensorProductCompatibility

-- ===== EinsteinFour
-- Lean 4.33 compatibility: exact bundled-manifold carrier and instances from
-- Mathlib/Geometry/Manifold/Category/MfldCat/OfModel.lean at
-- d13f23b723b8a846827a245b89c10fc7d3f11612 (Lean 4.34.1).
-- Copyright (c) 2026 Jack McCarthy. Apache 2.0; author: Jack McCarthy.
-- Category morphisms are not used by this challenge and are omitted.
section Lean433MfldCatCompatibility
open scoped Manifold ContDiff
universe u v

namespace ModelWithCorners

variable {𝕜 : Type*} [NontriviallyNormedField 𝕜]
  {E : Type*} [NormedAddCommGroup E] [NormedSpace 𝕜 E]
  {H : Type*} [TopologicalSpace H]

/-- The category of `C^n` manifolds modeled on a fixed model with corners `I`. -/
structure MfldCat (I : ModelWithCorners 𝕜 E H) (n : ℕ∞ω) where
  _mkInternal ::
  /-- The underlying type. -/
  carrier : Type u
  [topologicalSpace : TopologicalSpace carrier]
  [chartedSpace : ChartedSpace H carrier]
  [isManifold : IsManifold I n carrier]

attribute [instance] MfldCat.topologicalSpace MfldCat.chartedSpace MfldCat.isManifold

initialize_simps_projections MfldCat (-topologicalSpace, -chartedSpace, -isManifold)

namespace MfldCat
variable {I : ModelWithCorners 𝕜 E H} {n : ℕ∞ω} {M N P : MfldCat I n} {X Y Z : Type u}
  [TopologicalSpace X] [ChartedSpace H X] [IsManifold I n X]
  [TopologicalSpace Y] [ChartedSpace H Y] [IsManifold I n Y]
  [TopologicalSpace Z] [ChartedSpace H Z] [IsManifold I n Z]

instance : CoeSort (MfldCat I n) (Type u) := ⟨MfldCat.carrier⟩

attribute [coe] MfldCat.carrier

end MfldCat
end ModelWithCorners
end Lean433MfldCatCompatibility

-- ===== JointDickman
-- Faithful backport of Mathlib/Data/Nat/MaxPrimeFac.lean at
-- d13f23b723b8a846827a245b89c10fc7d3f11612 (Lean 4.34.1).
-- Preserve the upstream defaults: maxPrimeFac 0 = 0 and maxPrimeFac 1 = 1.
def Nat.maxPrimeFac (n : ℕ) : ℕ := n.primeFactorsList.getLastD n

-- ===== MaximalSeshadriConstants
-- Mathlib 4.33.1 uses the original namespace for this same tensor product.
noncomputable abbrev PresheafOfModulesOfCommRing.Monoidal.tensorObj :=
  @PresheafOfModules.Monoidal.tensorObj

