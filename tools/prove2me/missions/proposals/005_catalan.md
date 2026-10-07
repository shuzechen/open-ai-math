## Motivation

**Catalan's constant** is the real number

$$G=\sum_{j=0}^{\infty}\frac{(-1)^j}{(2j+1)^2}=1-\frac19+\frac1{25}-\frac1{49}+\cdots\approx 0.9159655941.$$

It is the value $\beta(2)$ of the **Dirichlet beta function** $\beta(s)=\sum_{j\ge0}(-1)^j(2j+1)^{-s}$, equivalently $L(2,\chi_{-4})$ for the odd quadratic character of conductor $4$. For odd $s$ the values $\beta(s)$ are rational multiples of $\pi^s$; the even values are a different arithmetic problem, and $G$ is the simplest of them. Whether $G$ is irrational was a long-standing open question in the arithmetic of special values of $L$-functions, in the same family as the irrationality of $\zeta(3)$ (Apéry, 1979) and of odd zeta values.

*Timeline.*

- Apéry (1979) proved $\zeta(2)$ and $\zeta(3)$ irrational through recurrences; Beukers (1979) gave integral proofs. Both succeed because the integer linear forms $A_mG-B_m$ built from the approximants tend to zero after denominators are cleared.
- Rivoal and Zudilin (2003) proved that infinitely many even beta values are irrational and that at least one of $\beta(2),\beta(4),\dots,\beta(14)$ is irrational; Zudilin (2003) reduced the finite list to the six values through $\beta(12)$, and Lai and Zhou (2022) to the five values $\beta(2),\dots,\beta(10)$. None of these identifies $\beta(2)$ itself.
- Zudilin (2003) constructed Apéry-like recurrences, a continued fraction and double-integral representations for $G$, and made the obstruction explicit: the displayed integer linear forms do not tend to zero even though their rational quotients converge rapidly. Rivoal (2006) and Krattenthaler and Rivoal (2008) proved the conjectured denominator bounds for the hypergeometric approximants; the remaining denominator cost is still too large for the small-linear-form criterion.
- Fischler (2020) gave quantitative irrationality and linear-independence results in families of Dirichlet $L$-values, again without isolating $\beta(2)$.
- Calegari (2005) proved irrationality of a $2$-adic analogue $G_2\in\mathbb{Q}_2$; Calegari, Dimitrov and Tang (2024) proved $\mathbb{Q}$-linear independence of $1,\pi^2$ and $L(2,\chi_{-3})$, for the conductor-$3$ character rather than the conductor-$4$ character of $G$.
- OpenAI (September 2026) proved that $G$ is irrational by an interpolation-determinant argument; Sun (September 2026) has announced a proof of the same qualitative statement by a different route.

## Setting

Throughout, $G$ denotes the real number defined by the alternating series above. The series converges absolutely, since $\sum_j(2j+1)^{-2}<\infty$, so its sum is the ordinary limit of partial sums and no conditional-convergence convention is involved. A real number $x$ is **irrational** when there are no integers $p,q$ with $q\ne0$ and $x=p/q$.

No further objects are needed to state the target. The proof in the source introduces, for each $N\ge1$, determinants $\Delta_N$ of size $n=48N$ whose entries are mixed moments

$$M(i,j)=\int_{-1}^{1}\!\int_0^1\frac{|t|\,t^i s^j}{\sqrt{1-t^2}\,(1-ts)}\,ds\,dt,\qquad Z(i,j)=\int_0^1\!\int_0^1\frac{t^is^j}{1-ts}\,ds\,dt$$

of two elementary kernels; each moment is a rational linear combination of $1$, $G$ and $\zeta(2)$.

## Formalization targets

### Goal

$$G=\sum_{j=0}^{\infty}\frac{(-1)^j}{(2j+1)^2}\notin\mathbb{Q}.$$

This is Theorem 1.1 of the source and the only comparator statement attached to the paper. The statement asserts qualitative irrationality only: no irrationality measure, no linear-independence statement with $\pi^2$ or $\zeta(2)$, and no statement about other beta values. The source's Section 8 deduces irrationality of the minimum volume of an orientable complete finite-volume hyperbolic three-manifold with exactly two cusps; that consequence is outside the mission.

## Significance

*The result.* Irrationality of $G$ settles the first even beta value, which had resisted the Apéry–Beukers mechanism precisely because every known construction of rational approximations loses its decay after denominators are cleared. The proof shows that a determinant built from moments can bypass the small-linear-form criterion for an individual special value, and the same argument yields irrationality of certain arithmetic hyperbolic volumes.

*Formalizing it.* The result is proved in the source but nothing is machine-checked. The Lean statement is admitted with `sorry` in the OpenAI release; this mission asks for the proof. A complete development would add to Mathlib's irrationality toolkit the ingredients of the determinant method: rationality of moment matrices under a rationality hypothesis, $p$-adic valuation bounds for determinants with integer Chebyshev coefficients, and real-place upper bounds through logarithmic-potential estimates certified by explicit rational data. Each of these is reusable for other special values (odd zeta values, other even beta values, $L(2,\chi_{-3})$).

## Difficulty

The obvious route is Apéry's: produce integers $A_m,B_m$ with $0<|A_mG-B_m|\to0$. For $G$ every known family of approximants fails this test, as Zudilin's discussion of his Theorem 1 and the Calegari–Dimitrov–Tang remarks on the two Catalan families record: the quotients $B_m/A_m$ converge to $G$ with error exponent below $1$ (the best explicit exponent, due to Eskandari (2026), is $0.62$), but $|A_mG-B_m|$ does not tend to zero. Solvers should not expect a linear-form argument to work.

The source replaces linear forms by determinants $\Delta_N$ of size $48N$. The rows are chosen so that two prescribed expressions have identical initial Taylor coefficients; this contact cancels the $\zeta(2)$ component of every entry, so the single hypothesis $G\in\mathbb{Q}$ makes all determinants rational. The contradiction then comes from comparing, for the normalized logarithm $L_N=\log|\Delta_N|/(48N)^2-\tfrac12\log2$, a lower bound $\liminf L_N>-2.29084$ forced by the finite places (the $p$-adic content of the rational determinant, which needs only the ordinary prime number theorem) against an upper bound $\limsup L_N\le-2.290939875$ from the real place. The margin is about $10^{-4}$, so every estimate has to be carried with explicit constants, and the real-place bound rests on a finite certificate of rational data that exhausts the stationary points of a logarithmic energy. Nonvanishing of $\Delta_N$ along a sequence of primes $N$ is a separate step.

## Formalization scope

The goal is stated exactly as in the OpenAI release, in the namespace `OAI.InternalCatalan`, importing only Mathlib:

```lean
theorem catalan_irrational :
    Irrational (∑' j : ℕ, (-1 : ℝ) ^ j / ((2 * j + 1 : ℕ) : ℝ) ^ 2)
```

Conventions fixed by this statement:

- `Irrational` is Mathlib's predicate `x ∉ Set.range ((↑) : ℚ → ℝ)`.
- The sum is Mathlib's `tsum` over `ℕ` with real terms. Because the series is absolutely summable, `tsum` equals the limit of partial sums; a proof must establish `Summable` to use that identification (`tsum` of a non-summable family is `0`, which is rational, so summability is part of the content, not a side remark).
- The denominator is the real cast of the natural number $2j+1$, squared; the sign is the real power $(-1)^j$.

No trivializing reading exists: the series is a fixed real number and the claim is a genuine Diophantine statement.

A complete development needs: finite sums and determinants over $\mathbb{Q}$ (`Matrix.det`), $p$-adic valuations on $\mathbb{Q}$ (`padicValRat`), Chebyshev polynomials (`Polynomial.Chebyshev`), double integrals of the kernels above (`MeasureTheory` on $[-1,1]\times[0,1]$), the prime number theorem in a weighted form (the source proves the needed consequence locally, from the ordinary PNT), and real-analytic estimates with explicit constants. Welcome contributions include the moment identities of Section 2, the rationality and cancellation lemma, the $2$-adic and odd-prime valuation bounds (Sections 2 and 3), nonvanishing at prime scales (Section 4), and the real-place energy estimate with its certificate (Sections 5 to 7), each as a platform lemma that the final assembly (Section 8) can import.

## Selected references

- OpenAI, *Catalan's constant is irrational*, OpenAI Math Release preprint, 24 September 2026. [paper](https://github.com/openai/math/blob/main/preprints/Catalans-constant-is-irrational-September-24-2026/paper.pdf), [Lean statement](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/Catalan.lean)
- R. Apéry, *Irrationalité de $\zeta2$ et $\zeta3$*, Astérisque 61 (1979), 11–13. [numdam](https://numdam.org/item/AST_1979__61__11_0/)
- F. Beukers, *A note on the irrationality of $\zeta(2)$ and $\zeta(3)$*, Bull. London Math. Soc. 11 (1979), 268–272. [doi:10.1112/blms/11.3.268](https://doi.org/10.1112/blms/11.3.268)
- T. Rivoal and W. Zudilin, *Diophantine properties of numbers related to Catalan's constant*, Math. Ann. 326 (2003), 705–721. [doi:10.1007/s00208-003-0420-2](https://doi.org/10.1007/s00208-003-0420-2)
- W. Zudilin, *An Apéry-like difference equation for Catalan's constant*, Electron. J. Combin. 10 (2003), R14. [arXiv:math/0201024](https://arxiv.org/abs/math/0201024)
- L. Lai and L. Zhou, *At least two of $\zeta(5),\zeta(7),\dots,\zeta(35)$ are irrational*, Publ. Math. Debrecen 101 (2022), 353–372. [arXiv:2103.00904](https://arxiv.org/abs/2103.00904)
- S. Fischler, *Irrationality of values of $L$-functions of Dirichlet characters*, J. London Math. Soc. 101 (2020), 857–876. [doi:10.1112/jlms.12290](https://doi.org/10.1112/jlms.12290)
- F. Calegari, *Irrationality of certain $p$-adic periods for small $p$*, Int. Math. Res. Not. 2005, 1235–1249. [doi:10.1155/IMRN.2005.1235](https://doi.org/10.1155/IMRN.2005.1235)
- F. Calegari, V. Dimitrov and Y. Tang, *The linear independence of $1$, $\zeta(2)$, and $L(2,\chi_{-3})$*, preprint (2024). [arXiv:2408.15403](https://arxiv.org/abs/2408.15403)
- P. Eskandari, *Improved rational approximations to Catalan's constant*, preprint (2026). [arXiv:2609.26354](https://arxiv.org/abs/2609.26354)
- Z.-W. Sun, *Catalan's constant is irrational*, preprint (2026). [arXiv:2609.04176](https://arxiv.org/abs/2609.04176)
