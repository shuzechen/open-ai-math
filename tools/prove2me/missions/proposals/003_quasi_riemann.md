## Motivation

For $\Re s>1$ the **Riemann zeta function** is $\zeta(s)=\sum_{n\ge1}n^{-s}$, continued meromorphically to $\mathbb{C}$ with a single pole at $s=1$. Its nontrivial zeros lie in the critical strip $0<\Re s<1$, and the Riemann hypothesis places them on $\Re s=\tfrac12$. The **quasi-Riemann hypothesis** asks for much less: one fixed $\sigma_0<1$, valid at every height, such that $\zeta(s)\ne0$ whenever $\Re s>\sigma_0$. Even this weaker statement was open: every classical zero-free region, from de la Vallée Poussin's $\Re s>1-c/\log|t|$ to the Vinogradov–Korobov region, shrinks to the line $\Re s=1$ as the height grows, and zero-density estimates such as Guth–Maynard bound the number of zeros to the right of a line without excluding all of them.

The same question for **Dirichlet $L$-functions** $L(s,\chi)=\sum_{n\ge1}\chi(n)n^{-s}$ is the uniform formulation of Friedlander and Goldston: a single $\sigma_0<1$ independent of the character and its conductor. A fixed Dirichlet zero-free half-plane has classical consequences, among them a polylogarithmic bound for the least quadratic nonresidue modulo a prime and a deterministic polynomial-time square-root algorithm over prime fields (Corollary 1.2 of the source).

*Timeline.* Dirichlet (1837) introduced the character $L$-series. Riemann (1859) tied the zeros of $\zeta$ to the distribution of primes. Hadamard and de la Vallée Poussin (1896) proved $\zeta(1+it)\ne0$, giving the prime number theorem. Hecke (1918–1920) developed $L$-functions of characters over number fields. Siegel (1935) proved $L(1,\chi)\gg_\varepsilon q^{-\varepsilon}$ with an ineffective constant, and Page (1935) showed that at most one primitive real character of conductor $\le Q$ has a real zero in $(1-c/\log Q,1)$; the possibility of a sequence of real zeros $\beta$ with $(1-\beta)\log q\to0$, the **Landau–Siegel zero** problem, remained open. OpenAI (30 September 2026) proved the zero-free half-plane $\Re s>7/8$ for $\zeta$, all Dirichlet $L$-functions and all finite-order Hecke $L$-functions over $\mathbb{Q}(\sqrt{-3})$; OpenAI (1 October 2026) proved the uniform logarithmic exclusion of Landau–Siegel zeros.

## Setting

Let $F=\mathbb{Q}(\sqrt{-3})=\mathbb{Q}(\zeta_3)$ with ring of integers $\mathcal{O}=\mathbb{Z}[\omega]$, $\omega$ a primitive cube root of unity. A **finite-order Hecke character** of modulus a nonzero ideal $\mathfrak{m}\subset\mathcal{O}$ is a character of the ray class group modulo $\mathfrak{m}$; concretely, a multiplicative character $\chi$ of $(\mathcal{O}/\mathfrak{m})^\times$ that is trivial on the image of the units $\mathcal{O}^\times$, extended by zero. Its $L$-function is $L_F(s,\chi)=\sum_{\mathfrak{a}\ne0}\chi(\mathfrak{a})(N\mathfrak{a})^{-s}$ for $\Re s>1$, continued meromorphically.

A **Dirichlet character** modulo $q\ge1$ is a homomorphism $(\mathbb{Z}/q)^\times\to\mathbb{C}^\times$ extended by zero; $\chi$ is **principal** when it is identically $1$ on units, **primitive** when it is induced from no smaller modulus, and **real** when it takes real values. For the principal character the $L$-function has a simple pole at $s=1$; for every other character it is entire.

In Lean, `riemannZeta` and `DirichletCharacter.LFunction χ s` are Mathlib's meromorphic continuations. The Hecke family is modelled in the definition bundle `HeckeSevenEighths` (namespace `OAI.SevenEighths`): a `Character` is a structure carrying a modulus ideal `𝔪 ≠ ⊥` of `𝒪 = NumberField.RingOfIntegers (CyclotomicField 3 ℚ)`, a `MulChar (𝒪 ⧸ 𝔪) ℂ` called `residue` that is trivial on every unit, and a positive **period** $N$ with $N\in\mathfrak{m}$. Its coefficients are indexed by $(x,y)\in\{0,\dots,N-1\}^2$ with value `residue (x + y ω)`, and `LFunction χ s` is $\tfrac16\,\pi^s\,\Gamma(s)^{-1}\Lambda(s)$, where $\Lambda$ is the completed function of a `WeakFEPair` built from products of Hurwitz even theta kernels over the hexagonal lattice. The factor $1/6$ accounts for the six units of $\mathcal{O}$.

## Formalization targets

### Goal: the quasi-Riemann hypothesis

$$\Re s>\tfrac78\ \Longrightarrow\ \zeta(s)\ne0.$$

This is the $\zeta$ case of Theorem 1.1 of the source. The boundary $\Re s=7/8$ is not included.

### Dirichlet $L$-functions

$$\Re s>\tfrac78,\ \neg(\chi=1\wedge s=1)\ \Longrightarrow\ L(s,\chi)\ne0,$$

uniformly over every modulus $q\ge1$ and every character $\chi$ modulo $q$, with only the principal pole excluded.

### Finite-order Hecke $L$-functions over $\mathbb{Q}(\sqrt{-3})$

$$\Re s>\tfrac78,\ \neg(\chi_{\mathrm{res}}=1\wedge s=1)\ \Longrightarrow\ L_F(s,\chi)\ne0,$$

for every `Character` $\chi$ of the bundle. In the source this is the primary statement; the Dirichlet and $\zeta$ cases follow by composing a Dirichlet character with the ideal norm and factoring the resulting Hecke $L$-function as $L(s,\chi)L(s,\chi\chi_{-3})$ up to finitely many nonzero Euler factors.

### Uniform exclusion of Landau–Siegel zeros

$$\exists\,c>0\ \ \forall q\ge3\ \ \forall\chi\ \text{primitive, nonprincipal, real mod }q\ \ \forall\beta\in(0,1):\ L(\beta,\chi)=0\ \Longrightarrow\ (1-\beta)\log q\ge c.$$

This is Theorem 1 of the second source. It is logically independent of the $7/8$ half-plane (which excludes real zeros in $(7/8,1)$ but says nothing about $(0,7/8]$) and is included because the OpenAI release groups the two results under one heading; the comparator file states it twice, with the three hypotheses on $\beta$ curried and as one conjunction.

## Significance

*The results.* The $7/8$ half-plane is the first fixed zero-free half-plane for $\zeta$, and it is uniform over all Dirichlet and all finite-order Hecke characters of $\mathbb{Q}(\sqrt{-3})$. By the functional equation every nontrivial zero of a primitive Dirichlet $L$-function lies in $1/8\le\Re s\le7/8$, which makes the weak-GRH hypothesis of Bhargava–Ivanyos–Mittal–Saxena unconditional and so yields Vinogradov's least-nonresidue conjecture $n(p)\ll_\delta p^\delta$ and deterministic polynomial-time square roots in $\mathbb{F}_p$. The Landau–Siegel exclusion makes $L(1,\chi)\gg1/\log q$ effective and removes the exceptional zero from the theory of primes in arithmetic progressions. Neither result approaches the Riemann hypothesis, which remains open.

*Formalizing it.* Both proofs exist only on paper; the Lean statements in the OpenAI release are admitted. Mathlib has `riemannZeta`, `DirichletCharacter.LFunction`, their functional equations, nonvanishing on $\Re s=1$ and the `WeakFEPair` machinery, but no large-sieve inequalities, no cubic theta series, no Hecke $L$-functions of ray class characters and no interpolation-determinant method. A complete formalization would add all of these as reusable infrastructure. The Hecke $L$-function of the bundle is defined analytically from theta kernels rather than as a Dirichlet series over ideals; identifying the two is itself a worthwhile milestone-level fact that the source assumes through the ordinary Hecke functional equation.

## Difficulty

The first idea every newcomer has is to sharpen the classical zero-free region. That cannot work: the de la Vallée Poussin and Vinogradov–Korobov arguments bound $\zeta'/\zeta$ near $\Re s=1$ using positivity of $3+4\cos\theta+\cos2\theta$, and the region they produce necessarily tends to the line as $|t|\to\infty$. Zero-density estimates bound how many zeros lie right of a line, never that there are none.

The source instead proves a *common continuation principle* (Section 2): for a target character $\eta$ and a scale $Z$, a normalized character sum is bounded directly and compared with a Mellin integral containing $1/L_F(s,\eta)$; a power saving in both comparisons continues the reciprocal across the rightmost possible zeros. The character sum averages smoothed Fourier coefficients of Patterson's **cubic theta series** against sextic residue characters, and it has two exact representations: a completed cubic reflection and a Poisson expansion whose rows are quotients of Hecke $L$-functions. The whole family of finite-order Hecke characters is needed even for $\zeta$, because the Poisson rows twist the target by Hecke characters. Part I reaches $11/12$ with balanced scales; Part II reaches $7/8$ with prime compensation, asymmetric scales and two additional moment estimates proved by separate inductions. The margins are explicit positive exponents chosen independently of the target character; any formalization must carry them exactly.

For the Siegel-zero result the obstacle is different: a real zero close to $1$ forces a shortage of primes with $\chi(p)=1$, and the source turns the surplus of primes with $\chi(p)=-1$ into divisibility of an interpolation determinant over a biquadratic field $\mathbb{Q}(\sqrt d,\sqrt2)$, comparing a size bound of order $\tfrac34\log U$ against a divisibility bound of order $\log U$.

## Formalization scope

All five statements are already published on this platform, verbatim from the OpenAI release at commit `adc7f12`, in the default environment (Lean 4.33.1, Mathlib `0df444a`). They are referenced, not redrafted. Conventions fixed by the Lean statements:

- `(7 / 8 : ℝ) < s.re` with `s : ℂ`; the boundary is excluded.
- The Dirichlet statement takes `{q : ℕ} [NeZero q]` and `χ : DirichletCharacter ℂ q`, so $q=1$ (hence $\zeta$) is included; the pole is excluded by `¬ (χ = 1 ∧ s = 1)`.
- The Hecke statement quantifies over the bundle's `Character` structure, not over Mathlib ray class characters; the pole is excluded by `¬ (χ.residue = 1 ∧ s = 1)`.
- The Siegel-zero statements require `3 ≤ q`, `χ.IsPrimitive`, `χ ≠ 1`, real values via `∀ a : ZMod q, (χ a).im = 0`, and the zero `χ.LFunction (β : ℂ) = 0` for a real `β` with `0 < β < 1`; the constant `c` is a single real existentially quantified before all other variables, so it is absolute. Both comparator variants must be proved; the second follows from the first by rearranging hypotheses.

No trivializing reading exists: every statement is a nonvanishing claim about Mathlib's own `riemannZeta` and `LFunction`, or about an $L$-function defined in a published bundle. Welcome contributions include: the transfer lemmas (Dirichlet from Hecke by norm composition; $\zeta$ from Dirichlet at $q=1$), the identification of the bundle's `LFunction` with the Dirichlet series over ideals in $\Re s>1$, the planar additive and quadratic/sextic large sieves over $\mathbb{Z}[\omega]$, the Patterson–Kubota cubic theta expansion, the zero detector of Section 8, and the two moment inductions of Sections 17 and 18, each as a platform lemma in the mission namespace.

## Selected references

- OpenAI, *The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane $\Re(s)>7/8$*, OpenAI Math Release preprint, 30 September 2026. [paper](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf)
- OpenAI, *Uniform exclusion of Landau–Siegel zeros*, OpenAI Math Release preprint, 1 October 2026. [paper](https://github.com/openai/math/blob/main/preprints/Uniform-exclusion-of-Landau-Siegel-zeros-October-1-2026/paper.pdf)
- Lean statements: [QuasiRiemannHypothesis.lean](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/QuasiRiemannHypothesis.lean), [DirichletSevenEighths.lean](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/DirichletSevenEighths.lean), [HeckeSevenEighths.lean](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/HeckeSevenEighths.lean), [SiegelZeros.lean](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/SiegelZeros.lean)
- J. B. Friedlander and D. A. Goldston, *Sums of three or more primes*, Trans. Amer. Math. Soc. 349 (1997), 287–310. [doi:10.1090/S0002-9947-97-01652-8](https://doi.org/10.1090/S0002-9947-97-01652-8)
- L. Guth and J. Maynard, *New large value estimates for Dirichlet polynomials*, Ann. of Math. 203 (2026), 623–675. [arXiv:2405.20552](https://arxiv.org/abs/2405.20552)
- A. Dunn and M. Radziwiłł, *Bias in cubic Gauss sums: Patterson's conjecture*, Ann. of Math. 200 (2024), 967–1057. [arXiv:2109.07463](https://arxiv.org/abs/2109.07463)
- S. J. Patterson, *A cubic analogue of the theta series*, J. reine angew. Math. 296 (1977).
- V. Blomer, L. Goldmakher and B. Louvel, *$L$-functions with $n$-th-order twists*, Int. Math. Res. Not. 2014, 1925–1955. [arXiv:1112.1650](https://arxiv.org/abs/1112.1650)
- D. R. Heath-Brown, *Kummer's conjecture for cubic Gauss sums*, Israel J. Math. 120 (2000), 97–124. [doi:10.1007/s11856-000-1273-y](https://doi.org/10.1007/s11856-000-1273-y)
- V. Bhargava, G. Ivanyos, R. Mittal and N. Saxena, *Irreducibility and deterministic $r$-th root finding over finite fields*, ISSAC 2017, 37–44. [doi:10.1145/3087604.3087620](https://doi.org/10.1145/3087604.3087620)
- C. L. Siegel, *Über die Classenzahl quadratischer Zahlkörper*, Acta Arith. 1 (1935), 83–86. [doi:10.4064/aa-1-1-83-86](https://doi.org/10.4064/aa-1-1-83-86)
- A. Page, *On the number of primes in an arithmetic progression*, Proc. London Math. Soc. 39 (1935), 116–141. [doi:10.1112/plms/s2-39.1.116](https://doi.org/10.1112/plms/s2-39.1.116)
- J. B. Friedlander and H. Iwaniec, *A note on Dirichlet $L$-functions*, Expo. Math. 36 (2018), 343–350. [doi:10.1016/j.exmath.2018.06.003](https://doi.org/10.1016/j.exmath.2018.06.003)
- M. Laurent, *Sur quelques résultats récents de transcendance*, Astérisque 198–200 (1991), 209–230. [numdam](https://www.numdam.org/item/AST_1991__198-199-200__209_0/)
