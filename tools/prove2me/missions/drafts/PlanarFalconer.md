## Motivation

The **Falconer distance problem** asks how large a set in Euclidean space must be, measured by Hausdorff dimension, before the set of distances it determines has positive Lebesgue measure. It is the continuum analogue of the Erdős distinct-distances problem. The conjectured threshold is $d/2$ in $\mathbb R^d$, so $1$ in the plane. The OpenAI preprint *The Falconer distance conjecture in all dimensions* (September 2026) proves the conjecture for every $d \ge 2$; this mission is the planar case $d = 2$.

*Timeline.* Falconer (1985) proved that Hausdorff dimension greater than $(d+1)/2$ (so $3/2$ in the plane) suffices, and gave lattice-type examples at dimension $d/2$ showing that the inequality must be strict. Mattila (1987) reduced the problem to decay of spherical averages of Fourier transforms of measures. Wolff (1999) lowered the planar threshold to $4/3$. Guth, Iosevich, Ou and Wang (2020) proved that a compact planar set of dimension greater than $5/4$ has a pinned distance set of positive measure for some pin. Liu (2026) obtained the planar positive-measure conclusion with a pin when Hausdorff and packing dimensions agree. The preprint removes all regularity hypotheses and reaches the conjectured threshold.

## Setting

The **plane** is `Plane := EuclideanSpace ℝ (Fin 2)`; its metric `dist x y` is the Euclidean distance $\lVert x - y\rVert = \sqrt{(x_1-y_1)^2 + (x_2-y_2)^2}$.

For $E \subset \mathbb R^2$, the **distance set** of $E$ is
$$
\Delta(E) = \{\, r \in \mathbb R : \exists\, x \in E,\ \exists\, y \in E,\ \lVert x - y \rVert = r \,\},
$$
written `distanceSet E`. It is a subset of the real line and contains $0$ whenever $E$ is nonempty.

The **Hausdorff dimension** $\dim_H E$ is Mathlib's `dimH E`, the supremum of the exponents $s$ with Hausdorff measure $\mu_H[s](E) = \infty$; it takes values in $[0,\infty]$ and is $0$ for the empty set and for countable sets.

**Lebesgue measure** on $\mathbb R$ is Mathlib's `volume`, an outer measure defined on every subset of $\mathbb R$; `volume (distanceSet E)` needs no measurability hypothesis.

A set is **compact** (`IsCompact E`) if every open cover has a finite subcover, i.e. closed and bounded in the plane.

The **Falconer distance conjecture** in dimension $d$ asserts that compact $E \subset \mathbb R^d$ with $\dim_H E > d/2$ has $\mathcal L^1(\Delta(E)) > 0$. The planar case is the proposition `MainTarget`.

## Formalization targets

### Goal

Prove `MainTarget`:
$$
\forall\, E \subset \mathbb R^2:\quad E \text{ compact},\ \ \dim_H E > 1 \ \Longrightarrow\ \mathcal L^1\bigl(\Delta(E)\bigr) > 0 .
$$

The statement fixes the strict threshold $1 = d/2$, the Euclidean metric, compactness of $E$, and positivity of the Lebesgue outer measure of $\Delta(E)$. It leaves unfixed the size of $\mathcal L^1(\Delta(E))$ and says nothing about pinned distance sets $\Delta_y(E) = \{\lvert x - y\rvert : x \in E\}$, about the endpoint $\dim_H E = 1$, or about non-compact Borel sets.

### Related missions

- Row 2 (Falconer distance theorem in every dimension): mission "The Falconer distance conjecture in all dimensions" (https://prove2.me/missions/320bf9ec-21dc-48b1-93d4-a5543af18d62)

This row is the special case $d = 2$ of the all-dimensional statement of row 2. Solvers may import sibling theorems that are already published on the platform as reductions, provided the ambient space, metric and distance-set definitions are matched to the planar ones used here.

## Significance

The result closes the planar Falconer problem at the conjectured threshold: any compact planar set of Hausdorff dimension exceeding $1$ determines a set of distances of positive length, with no assumption of equal Hausdorff and packing dimensions, Ahlfors regularity, product structure, or Fourier decay. It subsumes the planar thresholds $3/2$ (Falconer) and $4/3$ (Wolff), and the strict inequality is sharp by Falconer's examples.

Status: the theorem is proved on paper in the OpenAI preprint as the case $d = 2$ of its Theorem 1.1. In Lean it is only stated; `mainTarget_proved` is admitted with `sorry`, and nothing is machine-checked. A proof would be the first verified Falconer-type theorem at the conjectured threshold, and would bring Frostman measures, the Fourier analysis of measures and multiscale decompositions into Mathlib terms, all reusable beyond this problem.

## Difficulty

A newcomer's first idea is to view $\Delta(E)$ as the image of $E \times E$ under the Lipschitz map $(x,y) \mapsto \lVert x - y\rVert$ and argue by dimension. This fails twice: Lipschitz images can only lose dimension, so one gets at most an upper bound $\dim_H \Delta(E) \le 1$; and even $\dim_H \Delta(E) = 1$ would not give positive Lebesgue measure. The preprint states explicitly that "a distance set of Hausdorff dimension one alone would not suffice."

The second idea is the classical Fourier route. Mattila's criterion derives $\mathcal L^1(\Delta(E)) > 0$ from decay of the spherical averages $\int_{S^1} \lvert \hat\mu(R\theta)\rvert^2\, d\theta$ of a Frostman measure $\mu$ on $E$, and this produced the thresholds $3/2$ and $4/3$. A compact set of dimension slightly above $1$ need not carry any measure with the required Fourier decay, and the regularity hypotheses of the later pinned results (packing dimension equal to Hausdorff dimension) do not follow from $\dim_H E > 1$.

According to the preprint's introduction, the proof instead works at a fixed dyadic frequency, decomposes Frostman measures into almost uniform dyadic classes, records how the mass of each class decays beyond the critical exponent, and runs a recursion on two quantities, a count of pairs with nearly equal distances and a product of spherical Fourier energies. Angular tests, a graph estimate, a two-depth potential and a monotone shell reconstruction lemma close the recursion. The argument invokes no decoupling theorem and no earlier distance theorem; its one external incidence input is the planar theorem of Orponen and Shmerkin. None of this reduces to an existing Mathlib result.

## Formalization scope

The statement is the file `PlanarFalconer.lean` from the OpenAI comparator challenges:

```lean
import Mathlib

namespace OAI

namespace PlanarFalconer
open MeasureTheory Set

abbrev Plane := EuclideanSpace ℝ (Fin 2)

def distanceSet (E : Set Plane) : Set ℝ :=
  {r | ∃ x ∈ E, ∃ y ∈ E, dist x y = r}

def MainTarget : Prop :=
  ∀ E : Set Plane, IsCompact E → 1 < dimH E → 0 < volume (distanceSet E)

end PlanarFalconer

namespace PlanarFalconer

theorem mainTarget_proved : MainTarget := by
  sorry

end PlanarFalconer

end OAI
```

The theorem `OAI.PlanarFalconer.mainTarget_proved` and the definition bundle `PlanarFalconer` (`Plane`, `distanceSet`, `MainTarget`) are published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and referenced, not redrafted. A solution proves `MainTarget` as stated; unfolding it is part of the task.

Conventions the statement commits to:

- **Metric.** `Plane` is `EuclideanSpace ℝ (Fin 2)`, so `dist` is the Euclidean ($\ell^2$) distance, not the sup metric of `Fin 2 → ℝ`.
- **Distance set.** `distanceSet E` is an arbitrary `Set ℝ`; no measurability is assumed, and none is needed since `volume` is an outer measure.
- **Hausdorff dimension.** `dimH E : ℝ≥0∞`; the hypothesis `1 < dimH E` compares with `(1 : ℝ≥0∞)`. Since `dimH ∅ = 0` and countable sets have `dimH = 0`, it excludes the empty set and all countable sets; nonemptiness is not a separate assumption.
- **Conclusion.** `0 < volume (distanceSet E)` is an inequality in `ℝ≥0∞` for Lebesgue measure on `ℝ`: positive measure, not positive dimension.
- **Compactness.** `IsCompact E` is the only regularity hypothesis, the form proved in the preprint.

No trivializing reading exists: `volume` and `dimH` are the genuine Lebesgue measure and Hausdorff dimension, and the hypothesis rules out every degenerate `E`.

Infrastructure to be built: a Frostman lemma giving a measure $\mu$ on compact $E \subset \mathbb R^2$ with $\mu(B(x,r)) \lesssim r^s$ for $s < \dim_H E$; Fourier transforms of finite measures on $\mathbb R^2$ with Mattila's spherical-average identities; stationary-phase estimates; dyadic multiscale decompositions of measures; the Orponen–Shmerkin incidence input; and the recursion machinery of the preprint. Contributions of these components as `sorry`-free lemmas, or of the full theorem reduced to clearly stated analytic inputs, are welcome; weaker thresholds such as $3/2$ or $4/3$ count as partial progress, not as the goal.

## Selected references

- OpenAI, *The Falconer distance conjecture in all dimensions*, OpenAI Math Release preprint, 23 September 2026. https://github.com/openai/math/blob/main/preprints/The-Falconer-distance-conjecture-in-all-dimensions-September-23-2026/paper.pdf
- Lean statement: `lean/ComparatorChallenges/PlanarFalconer.lean`, openai/math commit adc7f12. https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/PlanarFalconer.lean
- K. J. Falconer, *On the Hausdorff dimensions of distance sets*, Mathematika 32 (1985), 206–212. https://doi.org/10.1112/S0025579300010998
- P. Mattila, *Spherical averages of Fourier transforms of measures with finite energy; dimensions of intersections and distance sets*, Mathematika 34 (1987), 207–228. https://doi.org/10.1112/S0025579300013462
- T. Wolff, *Decay of circular means of Fourier transforms of measures*, International Mathematics Research Notices 1999, no. 10, 547–567. https://doi.org/10.1155/S1073792899000288
- L. Guth, A. Iosevich, Y. Ou, H. Wang, *On Falconer's distance set problem in the plane*, Inventiones Mathematicae 219 (2020), 779–830. https://doi.org/10.1007/s00222-019-00917-x
- T. Orponen, P. Shmerkin, *On the Hausdorff dimension of Furstenberg sets and orthogonal projections in the plane*, Duke Mathematical Journal 172 (2023), 3559–3632. https://arxiv.org/abs/2106.03338
- B. Liu, *Lebesgue measure of distance sets with regular pins and multi-scale Mizohata–Takeuchi-type estimates*, preprint (2026). https://arxiv.org/abs/2603.15328
