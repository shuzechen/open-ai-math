## Motivation

The **Liouville function** $\lambda(n)=(-1)^{\Omega(n)}$, where $\Omega(n)$ counts prime factors with multiplicity, records the parity of the number of prime factors; Chowla conjectured that its values at distinct shifts are asymptotically uncorrelated [Cho65]: for distinct $h_1,\dots,h_k$,
$$\sum_{n\le X}\lambda(n+h_1)\cdots\lambda(n+h_k)=o(X).$$
Elliott extended the problem to bounded multiplicative functions [Ell92], asking for the same cancellation as soon as no factor is close to a twisted Dirichlet character $n\mapsto\chi(n)n^{it}$, the obstruction central to Halász's theory of mean values [Hal71]. Matomäki, Radziwiłł and Tao showed that Elliott's condition must be corrected for complex functions, since a function can imitate different twists at successive scales without imitating any fixed twist globally; the corrected condition requires non-closeness uniformly over frequencies $|t|\le N$ [MRT15, Section 1.1 and Appendix B]. The binary case $k=2$ of the corrected conjecture for **ordinary averages** $(1/N)\sum_{n\le N}$, as opposed to logarithmic averages $(1/\log N)\sum_{n\le N}(\cdot)/n$, is the statement formalized here: Theorem 1.2 of the OpenAI preprint *Ordinary two-point correlations of multiplicative functions* (24 September 2026).

*Timeline.* Chowla, 1965; Elliott, 1992. Matomäki, Radziwiłł and Tao (2015) proved cancellation averaged over slowly growing windows of shifts and formulated the corrected hypothesis. Tao (2016) proved the logarithmically averaged binary corrected Elliott theorem for nonproportional affine forms. For ordinary averages, Tao and Teräväinen (2019) obtained binary cancellation outside a set of scales of logarithmic density zero under the same hypothesis on one factor; Klurman, Mangerel and Teräväinen (2023) relaxed the hypothesis, with cancellation only along a set of scales of full upper logarithmic density. The preprint removes the exceptional scales.

## Setting

All functions are $f:\mathbb N\to\mathbb C$. The Lean development fixes the following definitions in the namespace `OAI.OrdinaryCorrelations`.

**One-bounded**: `OneBounded f` means $\|f(n)\|\le 1$ for every $n\in\mathbb N$, including $n=0$.

**Multiplicative**: `Multiplicative f` means $f(mn)=f(m)f(n)$ for all $m,n>0$ with $\gcd(m,n)=1$. No normalization $f(1)=1$ is imposed, $f(0)$ is unconstrained, and complete multiplicativity is not assumed, matching the preprint's class $f:\mathbb N\to\mathbb D$, $\mathbb D=\{|z|\le1\}$.

**Pretentious distance**: for a modulus $q$, a **Dirichlet character** $\chi$ modulo $q$ (a term of `DirichletCharacter ℂ q`), a real **frequency** $t$ and a real cutoff $X$,
$$\mathbb D(f,\chi,t;X)^2=\sum_{\substack{p\ \text{prime}\\ 2\le p\le\lfloor X\rfloor}}\frac{1-\operatorname{Re}\bigl(f(p)\,\overline{\chi(p)\,e^{it\log p}}\bigr)}{p},$$
and `distance f χ t X` is its nonnegative square root. Here $\chi(p)$ is $\chi$ at the residue of $p$ in $\mathbb Z/q\mathbb Z$ (so $\chi(p)=0$ when $p\mid q$) and $e^{it\log p}$ plays the role of $p^{it}$. This is the distance of the pretentious approach of Granville and Soundararajan [GS07, Section 3], display (1.1) of the preprint.

**Uniformly nonpretentious**: `UniformlyNonpretentious f` means that for every modulus $q>0$ and every Dirichlet character $\chi$ modulo $q$,
$$\inf_{t\in[-N,N]}\mathbb D(f,\chi,t;N)\longrightarrow\infty\qquad(N\to\infty,\ N\in\mathbb N).$$
The infimum is Lean's `sInf` of the image of $[-N,N]$, a nonempty set bounded below. The prime cutoff and the height bound are the same $N$, as in the preprint's condition (1.2); nothing is required of frequencies larger than $N$.

**Shift average**: for shifts $h_1,h_2\in\mathbb N$ and a length $N\in\mathbb N$,
$$\operatorname{shiftAverage}(f_1,f_2,h_1,h_2,N)=\frac1N\sum_{n=1}^{N}f_1(n+h_1)\,f_2(n+h_2),$$
a complex number. Each $n$ carries weight $1/N$, not $1/(n\log N)$. For $N=0$ Lean's convention $0^{-1}=0$ makes the value $0$.

## Formalization targets

### Goal

Let $f_1,f_2:\mathbb N\to\mathbb C$ be one-bounded and multiplicative, let at least one of them be uniformly nonpretentious, and let $h_1\neq h_2$ be natural numbers. Then
$$\lim_{N\to\infty}\frac1N\sum_{n=1}^{N}f_1(n+h_1)\,f_2(n+h_2)=0,$$
the limit taken along $N\in\mathbb N$ in $\mathbb C$.

This is the preprint's Theorem 1.2 (Binary corrected Elliott) with the same hypotheses: multiplicative $f_1,f_2:\mathbb N\to\mathbb D$, at least one satisfying (1.2), distinct nonnegative integers $h_1,h_2$, limit along $N\in\mathbb N$, no conjugation in the product. The statement fixes no rate of convergence (the preprint claims none for this class), does not say which of $f_1,f_2$ is nonpretentious, and never evaluates $f_i(0)$. The preprint's residue-class and affine extensions (Proposition 18.4, Corollary 1.3) are not part of this row.

### Related missions

- Row 2 (Ordinary Liouville and multiplicative two-point correlations): mission "Ordinary two-point correlations of multiplicative functions" (https://prove2.me/missions/11e8349d-5540-4448-90ed-3fd873cbd579); goal theorems `OAI.OrdinaryTwoPointCorrelations.liouville_log_saving`, `OAI.OrdinaryTwoPointCorrelations.binary_corrected_elliott`, `OAI.OrdinaryTwoPointCorrelations.affine_corrected_elliott`.

This row is the shifted-forms special case of the family: the sibling row additionally asks for the preprint's Theorem 1.1 (a power-of-logarithm saving for Liouville correlations on nonproportional affine forms) and Corollary 1.3 (affine forms $a_in+b_i$), and carries a theorem of the same name in its own namespace. Solvers may import sibling theorems already published on the platform as reductions.

## Significance

The result is the binary corrected Elliott conjecture for ordinary averages. Specializing $f_1=f_2=\lambda$ gives the two-point Chowla conjecture $\sum_{n\le N}\lambda(n+h_1)\lambda(n+h_2)=o(N)$ for every fixed pair of distinct shifts without logarithmic weights; the preprint records that Liouville satisfies (1.2) (Lemma 18.5) and proves a stronger $O(N/(\log N)^c)$ saving for Liouville separately (Theorem 1.1). Partial summation transfers ordinary cancellation to logarithmic cancellation, so this statement implies Tao's logarithmically averaged theorem [Tao16, Theorem 1.3] for shifted forms, and it strengthens the almost-all-scales results [TT19, Corollary 1.13; KMT23, Theorem 1.2] to every scale.

Status. The result is proved on paper in the OpenAI preprint (Theorem 1.2, Parts II and III). In Lean the theorem `binary_corrected_elliott` is admitted with `sorry`; nothing in this row is machine-checked. Replacing that `sorry` would be the first machine-verified two-point Elliott-type cancellation and requires analytic theory of multiplicative functions that Mathlib does not contain today.

## Difficulty

The newcomer's first idea is to take the logarithmically averaged theorem and remove the weights. This fails in the direction needed: by partial summation, ordinary cancellation implies logarithmic cancellation, not conversely. In the words of the preprint's introduction, logarithmic weighting combines information from many multiplicative scales, whereas an ordinary estimate must control the terminal scale itself; the almost-all-scales theorems [TT19, KMT23] show what scale-averaged arguments leave out.

The second idea is a Halász-type mean value theorem [Hal71], but $n\mapsto f_1(n+h_1)f_2(n+h_2)$ is not multiplicative in $n$. The third, the Matomäki–Radziwiłł short-interval theorem [MR16, Theorem 1], yields for a fixed shift only the bound $1-\delta(h)$ on the normalized Liouville correlation [MR16, Corollary 2]; its extension by Matomäki, Radziwiłł and Tao gives cancellation averaged over windows of shifts [MRT15], of which a fixed pair is a single term.

The preprint's route (Section 1.2) compares the correlation at $n,n+h$ with that at $dn,d(n+h)$ over multiplicative dilations, producing a graph on the integers bounded through closed walks; because the nonpretentiousness distance diverges with no prescribed rate, the graph is fixed before the long average is taken. Finally, the hypothesis is sharp in form: nonpretentiousness against each fixed $\chi(n)n^{it}$ does not suffice at every scale [MRT15], so a proof must use the uniformity over $|t|\le N$, and only that, since nothing is assumed for $|t|>N$.

## Formalization scope

The row consists of the definition bundle `Def_OrdinaryElliott` (the definitions in the Setting) and the single theorem below. Both are published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and are referenced, not redrafted.

```lean
theorem binary_corrected_elliott
    (f₁ f₂ : ℕ → ℂ) (hf₁ : OneBounded f₁) (hf₂ : OneBounded f₂)
    (hm₁ : Multiplicative f₁) (hm₂ : Multiplicative f₂)
    (hNP : UniformlyNonpretentious f₁ ∨ UniformlyNonpretentious f₂)
    (h₁ h₂ : ℕ) (hne : h₁ ≠ h₂) :
    Tendsto (shiftAverage f₁ f₂ h₁ h₂) atTop (nhds 0) := by
  sorry
```

Conventions the statement commits to:

- `OneBounded` quantifies over all $n$, including $0$; `Multiplicative` only over positive coprime pairs, without $f(1)=1$.
- `distanceSq` is a finite `Finset` sum over the primes in `Finset.Icc 2 ⌊X⌋₊` (natural-number floor; $X<2$ gives the empty sum), with real-cast denominator `(p : ℝ)`. `distance` is `Real.sqrt` (zero on negative input, which one-boundedness excludes). The twist is conjugated (`star`), i.e. $f(p)\overline{\chi(p)}p^{-it}$; since the condition ranges over $t\in[-N,N]$ and all characters, it is insensitive to this convention.
- `UniformlyNonpretentious` quantifies over every modulus `q` with `0 < q` and every `χ : DirichletCharacter ℂ q`, including $q=1$. The inner quantity is `sInf` over the image of `Set.Icc (-(N:ℝ)) (N:ℝ)`; the limit is `Tendsto … atTop atTop` along $N\in\mathbb N$.
- `shiftAverage` multiplies by the complex cast `(N : ℂ)⁻¹` and sums over `Finset.Icc 1 N`. The goal is `Tendsto … atTop (nhds 0)` in $\mathbb C$.
- `hNP` is a disjunction; `hne : h₁ ≠ h₂` excludes $h_1=h_2$, where the average need not vanish.

No trivializing reading is available: the hypotheses admit every one-bounded multiplicative function, including $\lambda$.

Infrastructure welcome as separate contributions: basic properties of the pretentious distance, uniform nonpretentiousness of the Liouville function (the preprint's Lemma 18.5), Halász-type mean value theorems and short-interval estimates in Mathlib's language of `Finset` sums and `Tendsto`, and lemmas relating `sInf` over an interval to attained minima.

## Selected references

- OpenAI, *Ordinary two-point correlations of multiplicative functions*, preprint, 24 September 2026 (Theorem 1.2): https://github.com/openai/math/blob/main/preprints/Ordinary-two-point-correlations-of-multiplicative-functions-September-24-2026/final.pdf
- OpenAI, Lean statement `OAI.OrdinaryCorrelations.binary_corrected_elliott`, openai/math commit adc7f12: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/OrdinaryElliott.lean
- OpenAI, docs page: https://github.com/openai/math/blob/main/lean/docs/007.md
- S. Chowla, *The Riemann Hypothesis and Hilbert's Tenth Problem*, Gordon and Breach, 1965.
- P. D. T. A. Elliott, *On the correlation of multiplicative functions*, Notas Soc. Mat. Chile 11 (1992), 1–11.
- G. Halász, *On the distribution of additive and the mean values of multiplicative arithmetic functions*, Studia Sci. Math. Hungar. 6 (1971), 211–233.
- A. Granville, K. Soundararajan, *Large character sums: pretentious characters and the Pólya–Vinogradov theorem*, J. Amer. Math. Soc. 20 (2007), 357–384. https://doi.org/10.1090/S0894-0347-06-00536-4
- K. Matomäki, M. Radziwiłł, T. Tao, *An averaged form of Chowla's conjecture*, Algebra & Number Theory 9 (2015), 2167–2196. https://doi.org/10.2140/ant.2015.9.2167
- K. Matomäki, M. Radziwiłł, *Multiplicative functions in short intervals*, Ann. of Math. 183 (2016), 1015–1056. https://doi.org/10.4007/annals.2016.183.3.6
- T. Tao, *The logarithmically averaged Chowla and Elliott conjectures for two-point correlations*, Forum Math. Pi 4 (2016), e8. https://doi.org/10.1017/fmp.2016.6
- T. Tao, J. Teräväinen, *The structure of correlations of multiplicative functions at almost all scales*, Algebra & Number Theory 13 (2019), 2103–2150. https://doi.org/10.2140/ant.2019.13.2103
- O. Klurman, A. P. Mangerel, J. Teräväinen, *On Elliott's conjecture and applications*, 2023. https://arxiv.org/abs/2304.05344v2
