import Definitions.Def_FiniteCongruenceGraph
import Definitions.Def_FCG_Congruence
import Definitions.Def_FCG_GraphCriterion
import Mathlib

open OAI OAI.FiniteCongruence

theorem solution (Lat : Type) [Fintype Lat] [Lattice Lat] [OrderBot Lat] :
    Representable Lat ↔ HasGraphWitness Lat := by
  constructor
  · rintro ⟨size, positive, alg, ⟨equiv⟩⟩
    exact ⟨size, positive, principalColor equiv, principalColor_isGraphWitness equiv⟩
  · rintro ⟨size, positive, color, witness⟩
    have : Nonempty (Fin size) := ⟨⟨0, positive⟩⟩
    exact ⟨size, positive, graphAlgebra color, ⟨graphOrderIso color witness⟩⟩
