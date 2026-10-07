## Motivation

For $\Re s>1$ the **Riemann zeta function** is $\zeta(s)=\sum_{n\ge1}n^{-s}$, continued meromorphically to $\mathbb{C}$ with a single pole at $s=1$. The **quasi-Riemann hypothesis** asks for one fixed $\sigma_0<1$, valid at every height, such that $\zeta(s)\ne0$ whenever $\Re s>\sigma_0$. Every classical zero-free region shrinks to the line $\Re s=1$ as the height grows, and zero-density estimates such as Guth–Maynard bound the number of zeros to the right of a line without excluding all of them.

This mission concerns the same question for **Dirichlet $L$-functions** $L(s,\chi)=\sum_{n\ge1}\chi(n)n^{-s}$, in the uniform formulation of Friedlander and Goldston: a single $\sigma_0<1$ independent of the character, its modulus and the height. Classical zero-free regions for $L(s,\chi)$ are worse than for $\zeta$: they shrink as the conductor grows and may admit one simple real exceptional zero. A fixed Dirichlet zero-free half-plane has classical consequences, among them a polylogarithmic bound for the least quadratic nonresidue modulo a prime and a deterministic polynomial-time square-root algorithm over prime fields (Corollary 1.2 of the source); those applications are not part of this mission.

*Timeline.* Dirichlet (1837) introduced the character $L$-series. Riemann (1859) tied the zeros of $\zeta$ to the distribution of primes. Hadamard and de la Vallée Poussin (1896) proved $\zeta(1+it)\ne0$, giving the prime number theorem. Hecke (1918–1920) developed $L$-functions of characters over number fields. Friedlander and Goldston (1997) stated the uniform Dirichlet zero-free half-plane as a hypothesis. OpenAI (30 September 2026) proved the half-plane $\Re s>7/8$ for every Dirichlet $L$-function, including $\zeta$, and for every finite-order Hecke $L$-function over $\mathbb{Q}(\sqrt{-3})$.

## Setting

Fix an integer $q\ge1$, the **modulus**. A **Dirichlet character** modulo $q$ is a group homomorphism $(\mathbb{Z}/q\mathbb{Z})^\times\to\mathbb{C}^\times$, extended by zero to residue classes that are not units; it is viewed as a function $\chi:\mathbb{Z}\to\mathbb{C}$ by reduction modulo $q$. The character that is identically $1$ on units is the **principal character**, written $\chi=1$. For $q=1$ every residue class is a unit, so the only character modulo $1$ is principal and $L(s,1)=\zeta(s)$. The character is **primitive** when it is induced from no smaller modulus; the statement below does not require primitivity.

The **Dirichlet $L$-function** of $\chi$ is $L(s,\chi)=\sum_{n\ge1}\chi(n)n^{-s}$ for $\Re s>1$, together with its meromorphic continuation to $\mathbb{C}$. For the principal character modulo $q$ the continuation is $\zeta(s)\prod_{p\mid q}(1-p^{-s})$, with a simple pole at $s=1$; for every nonprincipal character it is entire. A **zero-free half-plane** for $L(\cdot,\chi)$ is a set $\{\Re s>\sigma_0\}$ on which $L(s,\chi)\ne0$ away from the pole.

In Lean, `DirichletCharacter ℂ q` is Mathlib's type `MulChar (ZMod q) ℂ`, whose `1` is the principal character, and `DirichletCharacter.LFunction χ s` is Mathlib's meromorphic continuation of the series, defined for all `s : ℂ` as a total function. The real part of `s : ℂ` is `s.re`.

## Formalization targets

### Goal

$$\Re s>\tfrac78,\quad \neg(\chi=1\wedge s=1)\ \Longrightarrow\ L(s,\chi)\ne0,$$

uniformly over every modulus $q\ge1$ and every Dirichlet character $\chi$ modulo $q$. This is the Dirichlet case of Theorem 1.1 of the source. The boundary $\Re s=7/8$ is not included, and the only excluded point is the pole of the principal character at $s=1$. The statement leaves unfixed where the zeros of $L(s,\chi)$ in $0<\Re s\le7/8$ lie; it says nothing about the critical line, about real zeros in $(0,7/8]$, or about zero counts.

### Related missions

- Row 1 (Riemann zeta 7/8 bound): mission "The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8" (https://prove2.me/missions/7027d1c8-efd1-4103-a710-a744510abb5e)
- Row 3 (Finite-order Hecke L-function 7/8 bound): no mission yet; goal theorem `OAI.SevenEighths.HeckeFamily.LFunction_ne_zero_of_seven_eighths_lt_re`
- Row 4 (Uniform real-zero gap): mission "Uniform exclusion of Landau–Siegel zeros" (https://prove2.me/missions/77d01e65-f943-4099-83ed-f1f8dbf5e373)

This row is strictly stronger than row 1, which is its $q=1$ special case; it is obtained in the source from row 3 by transfer (Section 11.2 of the source, composing a Dirichlet character with the ideal norm of $\mathbb{Q}(\sqrt{-3})$ and factoring the resulting Hecke $L$-function as $L(s,\chi)L(s,\chi\chi_{-3})$ up to finitely many nonzero Euler factors); and it is independent of row 4, which concerns real zeros in $(0,1)$ close to $1$ at logarithmic scale. Solvers may import sibling theorems that are already published on the platform as reductions.

## Significance

*The result.* The theorem is the first fixed zero-free half-plane for Dirichlet $L$-functions, uniform over all moduli and all characters, including $\zeta$. By the functional equation every nontrivial zero of a primitive Dirichlet $L$-function then lies in $1/8\le\Re s\le7/8$. The source resolves the quasi-Riemann hypothesis affirmatively; it does not establish the Riemann hypothesis or its generalized form, which place the nontrivial zeros on $\Re s=1/2$ and remain open.

*Formalizing it.* The proof exists only on paper: it is proved in the OpenAI preprint of 30 September 2026 and admitted with `sorry` in the Lean comparator file; nothing is machine-checked yet. Mathlib has `DirichletCharacter.LFunction`, its functional equation, nonvanishing on $\Re s=1$ and the `WeakFEPair` machinery, but no large-sieve inequalities, no cubic theta series, no Hecke $L$-functions of ray class characters over $\mathbb{Q}(\sqrt{-3})$ and no transfer from Hecke to Dirichlet $L$-functions. A complete formalization adds all of these as reusable infrastructure; a verified theorem would also make the source's downstream corollaries (least nonresidue, deterministic square roots) available as formal targets.

## Difficulty

The first idea every newcomer has is to sharpen the classical zero-free region. That cannot work: the de la Vallée Poussin argument bounds $L'/L$ near $\Re s=1$ using positivity of $3+4\cos\theta+\cos2\theta$, and the region it produces necessarily tends to the line as the height or conductor grows and may admit a real exceptional zero. Zero-density estimates bound how many zeros lie right of a line, never that there are none. Nonvanishing on $\Re s=1$, which Mathlib has, gives no fixed gap.

The source instead proves a *common continuation principle* (Section 2): a normalized character sum is bounded directly and compared with a Mellin integral containing the reciprocal of the $L$-function; a power saving in both comparisons continues the reciprocal across the rightmost possible zeros. The character sum averages smoothed Fourier coefficients of Patterson's **cubic theta series** against sextic residue characters and has two exact representations, a completed cubic reflection and a Poisson expansion whose rows are quotients of Hecke $L$-functions. The whole family of finite-order Hecke characters of $\mathbb{Q}(\sqrt{-3})$ is needed even for a Dirichlet target, because the Poisson rows twist the target by Hecke characters. Part I reaches $11/12$ with balanced scales (Theorem 3.1 of the source); Part II reaches $7/8$ with prime compensation, asymmetric scales and two additional moment estimates proved by separate inductions. The margins are explicit positive exponents chosen independently of the target character; a formalization must carry them exactly.

## Formalization scope

The theorem is already published on this platform verbatim from the OpenAI release (openai/math, commit `adc7f12`) in the default environment (Lean 4.33.1, Mathlib `0df444a`); it is referenced, not redrafted. There is no accompanying definition bundle: every symbol is Mathlib's.

```lean
theorem LFunction_ne_zero_of_seven_eighths_lt_re
    {q : ℕ} [NeZero q] (χ : DirichletCharacter ℂ q) {s : ℂ}
    (hs : (7 / 8 : ℝ) < s.re) (hpole : ¬ (χ = 1 ∧ s = 1)) :
    _root_.DirichletCharacter.LFunction χ s ≠ 0 := by
  sorry
```

Conventions fixed by the statement:

- `{q : ℕ} [NeZero q]`: the modulus is any natural number other than $0$ (Mathlib's `ZMod 0` is $\mathbb{Z}$, so `NeZero q` is what makes `LFunction` meaningful). The case $q=1$ is included; there `χ = 1` holds automatically, `LFunction χ s` equals `riemannZeta s` (Mathlib's `DirichletCharacter.LFunction_modOne_eq`), and `hpole` reduces to `s ≠ 1`.
- `χ : DirichletCharacter ℂ q` ranges over all characters modulo $q$, primitive or not. For an imprimitive character Mathlib's `LFunction` continues the series with $\chi$ extended by zero on nonunits, which differs from the primitive $L$-function by finitely many Euler factors at $p\mid q$; the statement is about the function as Mathlib defines it.
- `(7 / 8 : ℝ) < s.re` with `s : ℂ`; the boundary is excluded, and there is no hypothesis on `s.im`.
- `hpole : ¬ (χ = 1 ∧ s = 1)`: the principal pole is excluded. Mathlib's `LFunction` is total and takes a junk value at the pole; `hpole` makes the statement independent of it. For nonprincipal $\chi$ the point $s=1$ is included in the claim.
- The conclusion is `≠ 0` in `ℂ`; nothing is asserted about the size of $|L(s,\chi)|$.

No trivializing reading exists: the statement is a nonvanishing claim about Mathlib's own `DirichletCharacter.LFunction`, the genuine meromorphic continuation, and no decidability instance enters it.

Infrastructure needed, and contributions welcome as platform lemmas in the mission namespace: finite-order Hecke characters and $L$-functions of $\mathbb{Q}(\sqrt{-3})$ as Dirichlet series over ideals, identified with whatever analytic model is used; the Hecke-to-Dirichlet transfer lemma by norm composition and Euler-factor comparison (reducing this row to row 3 once that row is published); the specialization to $q=1$ (yielding row 1); the planar additive and quadratic/sextic large sieves over $\mathbb{Z}[\omega]$; the Patterson–Kubota cubic theta expansion; the zero detector of Section 8; and the two moment inductions of Sections 17 and 18.

## Selected references

- OpenAI, *The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane $\Re(s)>7/8$*, OpenAI Math Release preprint, 30 September 2026. [paper](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf)
- OpenAI, *Uniform exclusion of Landau–Siegel zeros*, OpenAI Math Release preprint, 1 October 2026 (source of the sibling row 4). [paper](https://github.com/openai/math/blob/main/preprints/Uniform-exclusion-of-Landau-Siegel-zeros-October-1-2026/paper.pdf)
- Lean statement: [DirichletSevenEighths.lean](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/DirichletSevenEighths.lean)
- J. B. Friedlander and D. A. Goldston, *Sums of three or more primes*, Trans. Amer. Math. Soc. 349 (1997), 287–310. [doi:10.1090/S0002-9947-97-01652-8](https://doi.org/10.1090/S0002-9947-97-01652-8)
- L. Guth and J. Maynard, *New large value estimates for Dirichlet polynomials*, Ann. of Math. 203 (2026), 623–675. [arXiv:2405.20552](https://arxiv.org/abs/2405.20552)
- P. G. L. Dirichlet, *Beweis des Satzes, daß jede unbegrenzte arithmetische Progression ... unendlich viele Primzahlen enthält*, Abh. Königl. Preuss. Akad. Wiss. Berlin (1837), 45–81. [English translation, arXiv:0808.1408](https://arxiv.org/abs/0808.1408)
- B. Riemann, *Ueber die Anzahl der Primzahlen unter einer gegebenen Grösse*, Monatsber. Königl. Preuss. Akad. Wiss. Berlin (1859), 671–680. [Clay Mathematics Institute transcription](https://www.claymath.org/library/historical/riemann/r.html)
- A. Dunn and M. Radziwiłł, *Bias in cubic Gauss sums: Patterson's conjecture*, Ann. of Math. 200 (2024), 967–1057. [arXiv:2109.07463](https://arxiv.org/abs/2109.07463)
- S. J. Patterson, *A cubic analogue of the theta series*, J. reine angew. Math. 296 (1977), 125–161. [doi:10.1515/crll.1977.296.125](https://doi.org/10.1515/crll.1977.296.125)
- V. Bhargava, G. Ivanyos, R. Mittal and N. Saxena, *Irreducibility and deterministic $r$-th root finding over finite fields*, ISSAC 2017, 37–44. [doi:10.1145/3087604.3087620](https://doi.org/10.1145/3087604.3087620)
