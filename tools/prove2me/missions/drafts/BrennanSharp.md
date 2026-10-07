## Motivation

**Brennan's conjecture** asks how strongly a conformal map can compress area near an arbitrary boundary: for every conformal bijection $\phi\colon W\to\mathbb D$ from a simply connected plane domain onto the unit disk, $\int_W|\phi'|^s\,dA<\infty$ should hold for all $4/3<s<4$, with no boundedness or boundary-regularity assumption on $W$. Passing to the inverse $f=\phi^{-1}\colon\mathbb D\to W$ and changing variables turns this into $\int_{\mathbb D}|f'|^t\,dA<\infty$ for every univalent $f$ on $\mathbb D$ and every $-2<t<2/3$, with $t=2-s$ (equation (1.1) of the OpenAI preprint). The preprint *Brennan's conjecture and sharp inverse-square integral means* proves this open range (its Theorem 1.1, the subject of Row 1 of this family). The present row is the companion statement that the range is **sharp**: Corollary 1.2 of the preprint exhibits the classical Koebe function as an example for which both endpoint integrals, $t=-2$ and $t=2/3$, diverge, so its inverse fails area integrability at both $s=4$ and $s=4/3$.

*Timeline.* The conjecture goes back to Brennan's 1978 work, which pushed the known upper range beyond $s=3$. Carleson and Makarov (1994) proved $B_{\mathcal S}(t)=|t|-1$ for all sufficiently negative $t$; Bertilsson's 1999 thesis reports the range $4/3<s<3.421$; Hedenmalm and Shimorin (2005) obtained $B_{\mathcal S}(-2)\le1.218$ and Sola later $1.206$. The preprint reports this history in its Section 1.1, calls the slit-plane endpoint obstructions "classical", and verifies them in Section 7.3.

## Setting

$\mathbb D=\{z\in\mathbb C:|z|<1\}$ is the **open unit disk** (`disk`, the metric ball of radius $1$ about $0$), and $dA$ is **planar Lebesgue measure** (`volume` on $\mathbb C$, normalized so that the unit square has measure $1$).

A function $f\colon\mathbb C\to\mathbb C$ is **univalent on** $U\subseteq\mathbb C$ (`UnivalentOn f U`) when it is complex differentiable at every point of $U$ (`DifferentiableOn ℂ f U`) and injective on $U$ (`Set.InjOn f U`). It is **schlicht** (`Schlicht f`) when it is univalent on $\mathbb D$ with $f(0)=0$ and $f'(0)=1$, where $f'(0)$ is Mathlib's `deriv f 0`.

The **Koebe map** is
$$k(z)=\frac{z}{(1-z)^2},$$
written `koebeMap` in Lean, a total function on $\mathbb C$; its value at $z=1$ is irrelevant since $1\notin\mathbb D$. On $\mathbb D$, $k'(z)=(1+z)/(1-z)^3$, which never vanishes but has a zero at the boundary point $z=-1$ and a pole at $z=1$. The **Koebe domain** is $\Omega=k(\mathbb D)$ (`koebeDomain`), and the **Koebe inverse** $k^{-1}$ (`koebeInverse`) is `Function.invFunOn koebeMap disk`: on $\Omega$ it returns the unique preimage in $\mathbb D$, while off $\Omega$ it takes an unspecified value. Since $\Omega$ is open, `deriv koebeInverse w` for $w\in\Omega$ is the genuine complex derivative of the inverse map.

For a function $f$, a set $U$ and a real exponent $t$, the **area moment** is the lower Lebesgue integral
$$\operatorname{areaMoment}(f,U,t)=\int^-_{U}\operatorname{ofReal}\bigl(\|f'(z)\|^{t}\bigr)\,dA(z)\in[0,\infty],$$
with $\|f'(z)\|^t$ the real power `Real.rpow` and `ENNReal.ofReal` the embedding into $[0,\infty]$. A real function $g$ is **integrable on** $E$ (`IntegrableOn g E volume`) when it is Bochner integrable for the restriction of $dA$ to $E$: almost-everywhere strongly measurable with $\int_E|g|\,dA<\infty$.

## Formalization targets

### Goal

The target is the defined proposition `SharpEndpointStatement`, a conjunction of five claims about the Koebe map:
$$
\begin{aligned}
&\text{(i)}\ \ k\ \text{is schlicht};\\
&\text{(ii)}\ \ \operatorname{areaMoment}(k,\mathbb D,-2)=\int^-_{\mathbb D}\operatorname{ofReal}\bigl(\|k'(z)\|^{-2}\bigr)\,dA=\top;\\
&\text{(iii)}\ \ \operatorname{areaMoment}(k,\mathbb D,2/3)=\int^-_{\mathbb D}\operatorname{ofReal}\bigl(\|k'(z)\|^{2/3}\bigr)\,dA=\top;\\
&\text{(iv)}\ \ w\mapsto\|(k^{-1})'(w)\|^{4}\ \text{is not integrable on }\Omega;\\
&\text{(v)}\ \ w\mapsto\|(k^{-1})'(w)\|^{4/3}\ \text{is not integrable on }\Omega.
\end{aligned}
$$
Here $\top$ is the point at infinity of $[0,\infty]$. Claims (ii)–(iii) are the endpoints $t=-2$ and $t=2/3$ of the open interval; (iv)–(v) are the endpoints $s=4$ and $s=4/3$ of Brennan's interval for the inverse map, stated directly on $\Omega$ rather than through a change of variables. There are no free parameters and nothing is asserted about any map other than $k$. The statement does not identify $\Omega$ with the slit plane $\mathbb C\setminus(-\infty,-1/4]$; that classical fact may or may not be needed.

### Related missions

- Row 1 (Brennan and inverse-square integral-means bounds): mission "Brennan's conjecture and sharp inverse-square integral means" (https://prove2.me/missions/b2f7097c-d218-4324-b7c5-2d77675ea5f9)
- Row 3 (Strict inverse-first-power bound and consequences): mission "A strict inverse-first-power bound for univalent functions" (https://prove2.me/missions/bb87ed37-4881-4262-b5e9-99834089557f)

This row is an independent, explicit-example result showing that the open range proved in Row 1 cannot be enlarged; it uses neither Row 1's uniform estimate nor Row 3's bound as input. Solvers may import sibling theorems already published on the platform as reductions, although none is expected to be needed here.

## Significance

The result pins down the exact integrability range in Brennan's problem: Theorem 1.1 of the preprint gives $\int_{\mathbb D}|f'|^t\,dA<\infty$ for every univalent disk map and every $-2<t<2/3$, and the present statement shows that neither endpoint can be added, even for a single explicit map. The preprint notes that the radial exponent $B_{\mathcal S}(-2)=1$ is compatible with divergence of the area integral at $t=-2$; the Koebe map realizes this.

As to status: the five claims are proved on paper in the preprint (Corollary 1.2, details in Section 7.3), and the Lean theorem `sharp_endpoints` is admitted with `sorry`. Nothing in this row is machine-checked yet. Formalizing it produces a checked, reusable record of the Koebe function's basic properties (schlicht, with exactly borderline derivative behaviour at $z=\pm1$) and forces concrete infrastructure (area integrals of rational functions of $|1\pm z|$ over the disk, the inverse of an explicit univalent map, a planar change of variables) that the harder positive results in Rows 1 and 3 will also need.

## Difficulty

The mathematics is classical, but each claim has a step at which the newcomer's first idea fails.

For (ii) and (iii), the first idea is to observe that $|k'|^{-2}=|1-z|^6/|1+z|^2$ is unbounded near $z=-1$ and $|k'|^{2/3}=|1+z|^{2/3}/|1-z|^2$ is unbounded near $z=1$, and conclude divergence. Unboundedness proves nothing in two dimensions: $|\zeta|^{-1}$ is area-integrable near $0$. The exponent $2$ in both integrands is exactly critical, so the divergence is only logarithmic, and any lower bound that loses a positive power of $|1\pm z|$ is useless. One has to prove $\int|\zeta|^{-2}dA=\infty$ over a half-neighbourhood of the boundary point inside $\mathbb D$ and transport it through Lean's lower integral in $[0,\infty]$.

For (iv) and (v), the first idea is the change of variables $\int_\Omega|(k^{-1})'|^s\,dA=\int_{\mathbb D}|k'|^{2-s}\,dA$, which is how the preprint states the consequence. In Lean this requires the real two-dimensional change-of-variables theorem for an injective map differentiable on a measurable set, the identification of the real Jacobian determinant of multiplication by $c\in\mathbb C$ as $|c|^2$, and the derivative of `Function.invFunOn koebeMap disk` on $\Omega$ as $1/k'\circ k^{-1}$; `IntegrableOn` of a real function must then be related to a `lintegral` statement. Each step crosses between the complex-analytic and the real-measure-theoretic layers of Mathlib. A direct estimate on $\Omega$ avoids this but requires the geometry of $\Omega$ near the slit.

For (i), injectivity of $k$ on $\mathbb D$ is the only non-mechanical part: $k(z)=k(w)$ gives $(z-w)(1-zw)=0$, and the second factor is nonzero for $|z|,|w|<1$.

## Formalization scope

The Lean statement is

```lean
theorem sharp_endpoints : SharpEndpointStatement := by
  sorry
```

with, from the definition bundle,

```lean
def disk : Set ℂ := Metric.ball 0 1

def UnivalentOn (f : ℂ → ℂ) (U : Set ℂ) : Prop :=
  DifferentiableOn ℂ f U ∧ Set.InjOn f U

def Schlicht (f : ℂ → ℂ) : Prop :=
  UnivalentOn f disk ∧ f 0 = 0 ∧ deriv f 0 = 1

def koebeMap (z : ℂ) : ℂ := z/(1-z)^2

def koebeDomain : Set ℂ := koebeMap '' disk

def koebeInverse : ℂ → ℂ := Function.invFunOn koebeMap disk

def areaMoment (f : ℂ → ℂ) (U : Set ℂ) (t : ℝ) : ℝ≥0∞ :=
  ∫⁻ z in U, ENNReal.ofReal (‖deriv f z‖ ^ t) ∂volume

def SharpEndpointStatement : Prop :=
  Schlicht koebeMap ∧
  areaMoment koebeMap disk (-2) = ⊤ ∧
  areaMoment koebeMap disk (2 / 3) = ⊤ ∧
  ¬ IntegrableOn (fun z => ‖deriv koebeInverse z‖ ^ (4 : ℝ)) koebeDomain volume ∧
  ¬ IntegrableOn (fun z => ‖deriv koebeInverse z‖ ^ (4 / 3 : ℝ)) koebeDomain volume
```

The theorem and the definition bundle `BrennanSharp` are already published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and are referenced, not redrafted. Conventions the statement commits to:

- `volume` on `ℂ` is Mathlib's Lebesgue measure on the complex plane, i.e. planar area under $\mathbb C\cong\mathbb R^2$.
- `areaMoment` is a lower integral `∫⁻` in `ℝ≥0∞` with no measurability hypothesis; `= ⊤` must be proved as an actual divergence. Exponents are real (`Real.rpow`); Mathlib's convention $0^t=0$ for $t\neq0$ plays no role since $k'$ does not vanish on $\mathbb D$, and a single point has measure zero, so no spurious infinity is available.
- `deriv` is total and returns $0$ at points of non-differentiability; on $\mathbb D$ and on the open set $\Omega$ the functions are differentiable, so these are the genuine derivatives.
- `koebeInverse` is total; its values off $\Omega$ are never used because both `IntegrableOn` claims are restricted to `koebeDomain`.
- `IntegrableOn g koebeDomain volume` unfolds to `AEStronglyMeasurable` plus finite integral of $|g|$ for `volume.restrict koebeDomain`. The integrand is continuous on the open set $\Omega$, so the measurability half holds and the negation cannot be obtained from a measurability failure: it must come from $\int_\Omega\|(k^{-1})'\|^{s}\,dA=\infty$.
- `Schlicht koebeMap` requires `DifferentiableOn ℂ koebeMap disk`, `Set.InjOn koebeMap disk`, `koebeMap 0 = 0` and `deriv koebeMap 0 = 1`.

No trivializing reading exists: all five conjuncts are substantive claims about one explicit map, and none follows from a degenerate convention.

Likely infrastructure: lower bounds for lower integrals via measurable minorants (`lintegral_mono`, `setLIntegral_mono`); polar coordinates or a dyadic-annulus decomposition around $z=\pm1$ giving $\int|\zeta|^{-2}dA=\infty$ on a half-disk; the `Function.invFunOn` API (`Function.invFunOn_eq`); openness of $\Omega$ and differentiability of the inverse there; and, on the change-of-variables route, `lintegral_image_eq_lintegral_abs_det_fderiv_mul` with the determinant of complex multiplication as a real-linear map. Welcome contributions: any of the five conjuncts proved separately, a general lemma $\int_{\mathbb D\cap B(\zeta_0,r)}|z-\zeta_0|^{-2}dA=\infty$ for $|\zeta_0|=1$, a change of variables for injective holomorphic maps on open subsets of $\mathbb C$, and a reusable development of the Koebe function (image, inverse, derivative) that the other rows of this family can share.

## Selected references

- OpenAI, *Brennan's conjecture and sharp inverse-square integral means*, preprint, September 24, 2026. https://github.com/openai/math/blob/main/preprints/Brennans-conjecture-and-sharp-inverse-square-integral-means-September-24-2026/paper.pdf
- OpenAI, *A strict inverse-first-power bound for univalent functions*, preprint, September 24, 2026. https://github.com/openai/math/blob/main/preprints/A-strict-inverse-first-power-bound-for-univalent-functions-September-24-2026/paper.pdf
- Lean comparator statement `BrennanSharp.lean` (openai/math, commit adc7f12). https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/BrennanSharp.lean
- Scope note for this family (openai/math docs). https://github.com/openai/math/blob/main/lean/docs/072.md
- J. E. Brennan, *The integrability of the derivative in conformal mapping*, J. London Math. Soc. (2) 18 (1978), 261–272.
- L. Carleson and N. G. Makarov, *Some results connected with Brennan's conjecture*, Ark. Mat. 32 (1994), 33–62.
- P. L. Duren, *Univalent Functions*, Grundlehren der mathematischen Wissenschaften 259, Springer, New York, 1983.
- H. Hedenmalm and S. Shimorin, *Weighted Bergman spaces and the integral means spectrum of conformal mappings*, Duke Math. J. 127 (2005), 341–393.
