## Motivation

Let $F=\mathbb{Q}(\sqrt{-3})$ with ring of integers $\mathcal{O}$, and write $N\mathfrak{a}=|\mathcal{O}/\mathfrak{a}|$ for the **norm** of a nonzero ideal. A **finite-order Hecke character** modulo a nonzero ideal $\mathfrak{f}$ is a character of the ray class group modulo $\mathfrak{f}$, extended by zero to ideals not coprime to $\mathfrak{f}$; its **Hecke $L$-function** is $L_F(s,\eta)=\sum_{\mathfrak{a}\ne0}\eta(\mathfrak{a})(N\mathfrak{a})^{-s}$ for $\Re s>1$, continued meromorphically. Classical zero-free regions (Thorner–Zaman, Theorem 3.1) shrink to the line $\Re s=1$ as conductor or height grows and may allow one real exceptional zero; zero-density estimates count zeros right of a line without excluding them. **Uniform exclusion** asks for one $\sigma_0<1$, independent of character, conductor and height, with $L_F(s,\eta)\ne0$ for $\Re s>\sigma_0$.

The OpenAI preprint of 30 September 2026 proves $\sigma_0=7/8$ for every finite-order Hecke $L$-function over $F$ (Theorem 1.1), the pole at $s=1$ of a principal character allowed. The Hecke family is the primary object of the proof: Dirichlet $L$-functions and $\zeta$ follow by transfer (Section 11.2), and the whole family is needed even for $\zeta$, since the Poisson expansion the proof uses has rows that are quotients of Hecke $L$-functions.

*Timeline.* Dirichlet (1837) introduced character $L$-series; Riemann (1859) tied the zeros of $\zeta$ to the primes; Hadamard and de la Vallée Poussin (1896) proved nonvanishing on $\Re s=1$; Hecke (1918–1920) defined the character zeta functions of number fields. No fixed zero-free half-plane was known for any of these families before 2026.

## Setting

Write $K$ for Mathlib's `CyclotomicField 3 ℚ`, which is $F$, and $\mathcal{O}$ for `NumberField.RingOfIntegers K`. Let $\omega\in\mathcal{O}$ be the **primitive cube root of unity** `omega` selected by `IsCyclotomicExtension.zeta_spec 3 ℚ K`; then $\mathcal{O}=\mathbb{Z}[\omega]$, `coordinateElement x y` is $x+y\omega$ for $x,y\in\mathbb{Z}$, and $N(x+y\omega)=x^2-xy+y^2$. $\mathcal{O}$ has six units $\pm1,\pm\omega,\pm\omega^2$ and class number one.

A **character** is a term of the bundle's structure `Character`, with fields

- `modulus : Ideal O`, written $\mathfrak{m}$, and `modulus_ne_bot : 𝔪 ≠ ⊥`;
- `residue : MulChar (O ⧸ 𝔪) ℂ`, a **multiplicative character** of the quotient ring: multiplicative, $1$ at $1$, zero on nonunits of $\mathcal{O}/\mathfrak{m}$;
- `unit_trivial : ∀ u : Oˣ, residue (Ideal.Quotient.mk 𝔪 u) = 1`;
- `period : ℕ`, written $N$, with `period_pos : 0 < N` and `period_mem : (N : O) ∈ 𝔪`.

Since $\mathcal{O}$ is a principal ideal domain and `residue` is trivial on units and zero off $(\mathcal{O}/\mathfrak{m})^\times$, the rule $(\alpha)\mapsto$ `residue α` is a well-defined function of nonzero ideals: this is how the structure encodes a finite-order Hecke character modulo $\mathfrak{m}$. The **coefficients** are `coefficients χ (a, b) = χ.residue (mk 𝔪 (a + b ω))` for $(a,b)\in$ `Fin N × Fin N`, which depend only on residues modulo $N$ because $N\in\mathfrak{m}$.

The $L$-function lives in Mathlib's **`WeakFEPair`** framework: functions $f,g$ on $(0,\infty)$, weight $k>0$, sign $\varepsilon\ne0$, constants $f_0,g_0$, the functional equation $f(1/x)=\varepsilon x^{k}g(x)$, and faster-than-polynomial decay of $f-f_0$, $g-g_0$ at infinity. Mathlib attaches to such a pair a total function `Λ : ℂ → ℂ`, equal for $\Re s>k$ to the Mellin transform of $f-f_0$ and elsewhere to its meromorphic continuation, with at most simple poles at $s=0$ and $s=k$; at those two points Lean's `1/0 = 0` makes `Λ` a junk value. From Mathlib's **Hurwitz even pair** `HurwitzZeta.hurwitzEvenFEPair a` ($a\in\mathbb{R}/\mathbb{Z}$, kernel $\sum_{n\in\mathbb{Z}}e^{-\pi(n+a)^2t}$, weight $1/2$) the bundle defines `product` (weights add, signs and constants multiply), `rescale` by $u>0$ ($f(x)\mapsto f(ux)$, $g(x)\mapsto g(x/u)$, $\varepsilon\mapsto\varepsilon u^{-k}$), `rectangularPair a b u v` (product of the even pairs for $a,b$ rescaled by $u,v$; weight $1$) and, for $L>0$, $e\in\{0,1\}$, `parityPair a b L e`: the rectangular pair with shifts $(2a-b-Le)/(2L)$, $(b+Le)/(2L)$ and scalings $L^2$, $3L^2$. `finitePair` combines weight-$1$ pairs with complex weights $w_i$ into the weight-$1$ pair with $\varepsilon=1$, $f=\sum w_if_i$, $g=\sum w_i\varepsilon_ig_i$. For $w$ on `Fin N × Fin N`, `HeckeTheta.pair w` sums the parity pairs over $(a,b)$ and $e$ with $L=N$ and weight $w(a,b)$; `completed w` is its `Λ`; `latticeL w s = π^s · (Γ s)⁻¹ · completed w s`; `continuedLattice χ = latticeL (coefficients χ)`; and

$$\texttt{LFunction χ s} \;=\; \texttt{continuedLattice χ s}\,/\,6 .$$

Unwinding, the $f$ of `pair (coefficients χ)` is $t\mapsto\sum_{z\in\mathcal{O}}\chi(z)e^{-\pi N(z)t}$: the parities $e$ and the shifts cover each coset $x\equiv a$, $y\equiv b\pmod N$ of $\mathbb{Z}^2$ once, via $x^2-xy+y^2=X^2+3Y^2$, $X=x-y/2$, $Y=y/2$. Its Mellin transform is $\pi^{-s}\Gamma(s)\sum_{z\ne0}\chi(z)N(z)^{-s}$ for $\Re s>1$, and each nonzero ideal has six generators, hence the division by $6$. So `LFunction χ s` is designed to agree with $L_F(s,\chi)$, but the bundle asserts no identification, Euler product or functional equation as a theorem. Below, $L(\chi,s)$ denotes `LFunction χ s`.

## Formalization targets

### Goal

$$\chi:\texttt{Character},\quad s\in\mathbb{C},\quad \Re s>\tfrac78,\quad \neg\bigl(\chi.\mathrm{residue}=1\ \wedge\ s=1\bigr)\ \Longrightarrow\ L(\chi,s)\ne0 .$$

Here `1` is the trivial `MulChar` (one on units, zero on nonunits), so the only excluded point is $s=1$ for the principal character modulo $\mathfrak{m}$; for nonprincipal residue $s=1$ is part of the claim. The target leaves unfixed the boundary $\Re s=7/8$, the zeros in $\Re s\le7/8$, and any growth or value information.

### Related missions

- Row 1 (Riemann zeta 7/8 bound): mission "The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8" (https://prove2.me/missions/7027d1c8-efd1-4103-a710-a744510abb5e)
- Row 2 (Dirichlet L-function 7/8 bound): no mission yet; goal theorem `OAI.DirichletCharacter.LFunction_ne_zero_of_seven_eighths_lt_re`
- Row 4 (Uniform real-zero gap): mission "Uniform exclusion of Landau–Siegel zeros" (https://prove2.me/missions/77d01e65-f943-4099-83ed-f1f8dbf5e373)

This row is the primary statement of the source and is stronger than rows 1 and 2, which the source derives from it by transfer (Section 11.2: compose a Dirichlet character with the ideal norm of $F$); row 4 is an independent result from a second preprint. Solvers may import sibling theorems already published on the platform as reductions, although no sibling statement implies this one.

## Significance

The result is the first fixed zero-free half-plane for the finite-order Hecke $L$-functions of $F$, uniform in modulus and character; it excludes any exceptional real zero in $(7/8,1)$, confines the nontrivial zeros of primitive characters to $1/8\le\Re s\le7/8$ by the functional equation, and by the standard explicit-formula argument gives power-saving error terms for primes in ray classes of $F$. It does not approach the generalized Riemann hypothesis, which remains open.

Status: the theorem is proved on paper in the OpenAI preprint and admitted with `sorry` in Lean; nothing is machine-checked. Mathlib has `WeakFEPair`, the Hurwitz kernels, `MulChar` and cyclotomic rings of integers, but no Hecke $L$-functions, ray class characters, large sieves or cubic theta series; a formalization would add these as reusable infrastructure.

## Difficulty

The newcomer's first idea is to sharpen the classical zero-free region. That cannot work: the de la Vallée Poussin and Vinogradov–Korobov arguments control $L'/L$ near $\Re s=1$ through positivity of $3+4\cos\theta+\cos2\theta$ and necessarily yield regions shrinking to the line. Deducing this row from the Dirichlet and $\zeta$ rows fails in the other direction: Hecke characters of $F$ include cubic and sextic residue characters whose $L$-functions are not products of Dirichlet $L$-functions. The functional equation of the pair maps $\Re s>7/8$ to $\Re s<1/8$ and says nothing about existence of zeros.

The source instead compares two representations of a completed cubic-theta sum built from Patterson's series (through the cusp expansions recorded by Dunn and Radziwiłł), a completed cubic reflection and an exact Poisson series whose rows are quotients of Hecke $L$-functions, and continues $1/L_F(s,\eta)$ across the rightmost possible zeros from a power saving in both comparisons. Part I obtains $11/12$ with balanced scales (Theorem 3.1); Part II reaches $7/8$ with prime compensation, asymmetric scales and two further moment estimates. All exponent margins are explicit and independent of the target character; a formalization has to carry them exactly.

## Formalization scope

The statement, in namespace `OAI.SevenEighths.HeckeFamily`:

```lean
theorem LFunction_ne_zero_of_seven_eighths_lt_re
    (χ : Character) {s : ℂ} (hs : (7 / 8 : ℝ) < s.re)
    (hpole : ¬ (χ.residue = 1 ∧ s = 1)) : LFunction χ s ≠ 0 := by sorry
```

It and the definition bundle `HeckeSevenEighths` (imported as `Definitions.Def_HeckeSevenEighths`) are published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and are referenced, not redrafted. Conventions the statement commits to:

- `hs` is a strict inequality on the real part, with `7 / 8` a real literal; `s` is implicit.
- `Character` requires only `modulus ≠ ⊥`: the unit ideal is allowed (then `O ⧸ 𝔪` is the zero ring and `residue` is forced to be `1`), primitivity is not required, and `period` is any positive integer in `𝔪`, not necessarily the least, so the theorem covers every choice of period for the same modulus and residue.
- `residue` is a `MulChar` on the quotient ring, so coefficients at elements not coprime to `𝔪` vanish by definition; `unit_trivial` ranges over all of `Oˣ`.
- `χ.residue = 1` is equality of `MulChar`s with the trivial character; for nonprincipal residue `hpole` holds automatically.
- `LFunction` is total: `(Real.pi : ℂ) ^ s` is the complex power, `(Complex.Gamma s)⁻¹` and `/ 6` use Lean's inverse and division in `ℂ`, and `WeakFEPair.Λ` is Mathlib's continuation. In $\Re s>7/8$ the only point where `Λ` can take a junk value is $s=1$ with principal residue, which is excluded.
- Coefficients are indexed by `Fin χ.period × Fin χ.period`, cast through `ℕ` and `ℤ` into `O`.

No trivializing reading exists: the claim is nonvanishing of a concretely defined function on an open half-plane. Infrastructure needed includes `WeakFEPair.hasMellin` applied to the lattice-coset bookkeeping above, the Dirichlet series and Euler product of `LFunction` for $\Re s>1$, Gauss sums for sextic residue characters of $\mathbb{Z}[\omega]$, the planar additive and sextic large sieves (Lemma 9.1, extending Heath-Brown's cubic estimate), the Kubota–Patterson cubic theta expansion, the zero detector of Section 8 and the moment inductions of Sections 17 and 18. Any of these as platform lemmas in the mission namespace is a welcome contribution.

## Selected references

- OpenAI, *The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane $\Re(s)>7/8$*, OpenAI Math Release preprint, 30 September 2026. [paper](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf)
- OpenAI, *Uniform exclusion of Landau–Siegel zeros*, OpenAI Math Release preprint, 1 October 2026 (source of row 4). [paper](https://github.com/openai/math/blob/main/preprints/Uniform-exclusion-of-Landau-Siegel-zeros-October-1-2026/paper.pdf)
- Lean statement: [HeckeSevenEighths.lean](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/HeckeSevenEighths.lean)
- E. Hecke, *Eine neue Art von Zetafunktionen und ihre Beziehungen zur Verteilung der Primzahlen*, Math. Z. 1 (1918), 357–376; 6 (1920), 11–51. [doi:10.1007/BF01465095](https://doi.org/10.1007/BF01465095)
- J. Thorner and A. Zaman, *A unified and improved Chebotarev density theorem*, Algebra & Number Theory 13 (2019), 1039–1068. [doi:10.2140/ant.2019.13.1039](https://doi.org/10.2140/ant.2019.13.1039)
- S. J. Patterson, *A cubic analogue of the theta series*, J. reine angew. Math. 296 (1977), 125–161. [doi:10.1515/crll.1977.296.125](https://doi.org/10.1515/crll.1977.296.125)
- A. Dunn and M. Radziwiłł, *Bias in cubic Gauss sums: Patterson's conjecture*, Ann. of Math. 200 (2024), 967–1057. [doi:10.4007/annals.2024.200.3.3](https://doi.org/10.4007/annals.2024.200.3.3)
- D. R. Heath-Brown, *Kummer's conjecture for cubic Gauss sums*, Israel J. Math. 120 (2000), 97–124. [doi:10.1007/s11856-000-1273-y](https://doi.org/10.1007/s11856-000-1273-y)
