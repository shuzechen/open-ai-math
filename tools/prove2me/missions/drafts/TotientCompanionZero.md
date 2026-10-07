## Motivation

Euler's **totient function** $\varphi(n)$ counts the integers $1\le m\le n$ coprime to $n$. An integer $v$ is a **totient value** if $v=\varphi(n)$ for some $n\ge 1$; $\mathcal V$ is the set of totient values and $V(x)=\#\{v\in\mathcal V: v\le x\}$. Distinct integers can share a totient, so counting distinct values is harder than counting integers with a prescribed factorization (OpenAI 2026, Section 1). The preprint gives an explicit asymptotic equivalent $V(x)\sim \frac{x}{\log x}G_mA(1;\theta)$ (Theorem 2.1) and proves $V(cx)/V(x)\to c$ for every fixed $c>0$, a question posed by Erdős and Hall (1976, p. 3) and repeated by Erdős (1979, p. 80). Ford's bound $V(cx)-V(x)\asymp_c V(x)$ (Ford 1998, Theorem 4) does not determine the limiting ratio.

The same passage of Erdős (1979, p. 80) asks, for each fixed positive integer $k$, about the number of values $v\le x$ whose **least preimage** $\ell(v)=\min\{n\ge1:\varphi(n)=v\}$ satisfies $kx<\ell(v)\le(k+1)x$. Section 7 of the preprint gives a weighted asymptotic for this count and proves that it has order $V(x)$ precisely when some totient $d$ satisfies $\ell(d)>kd$; otherwise the count vanishes identically. The positive alternative holds for $k=1,2$; which other $k$ satisfy this **seed condition** is not determined, and whether $\ell(d)/d$ is unbounded (Erdős 1995, Section I.9) remains open. The present row is the zero alternative: if no totient $d$ has $kd<\ell(d)$, both the count and the coefficient are identically zero.

*Timeline* (after Section 1 of the preprint). Pillai (1929) proved that totient values have density zero. Erdős (1935) sharpened the upper bound to $V(x)\ll_\varepsilon x/(\log x)^{1-\varepsilon}$ and later (1945) obtained the lower bound $(1+o(1))x\log_2x/\log x$. Erdős and Hall (1976) raised the lower bound by a factor $\exp\{a(\log_3x)^2\}$ for every $0<a<1/\log16$; Pomerance (1986) brought the upper bound onto the same scale; Maier and Pomerance (1988) found the leading constant, $V(x)=\frac{x}{\log x}\exp\{(C_0+o(1))(\log_3x)^2\}$ with $C_0=0.8178146\ldots$. Ford (1998, Theorem 1) reduced the uncertainty to a bounded multiplicative factor, with a second constant $D_0=2.1769687\ldots$; here $C_0=1/(2\lambda)$ and $D_0=(1+\log(\lambda/\gamma))/\lambda-\tfrac12$ in the notation below.

## Setting

All objects live in the Lean namespace `OAI.TotientAsymptotic`; notation follows the Lean names, which match Section 2 of the preprint.

**Totient values.** `IsTotient v` means $\exists n\ge1,\ \varphi(n)=v$ (`Nat.totient`). Every totient value is $\ge1$. The least preimage `ell v`, written $\ell(v)$, is $\min\{n\ge1:\varphi(n)=v\}$ (`Nat.find`) when $v$ is a totient and $0$ otherwise. For instance $\ell(1)=1$, $\ell(2)=3$, and $\ell(v)>v$ for every totient $v\ge2$ because $\varphi(n)<n$ for $n\ge2$.

**Companion count.** For $k\in\mathbb N$, $x\in\mathbb R$, `N k x`, written $N_k(x)$, is the cardinality, cast to $\mathbb R$, of
$$\{\,v\in\mathbb N : 1\le v\le\lfloor x\rfloor_+,\ \text{IsTotient}(v),\ k\,x<\ell(v)\le (k+1)\,x\,\},$$
with $\lfloor x\rfloor_+$ the `Nat.floor` ($0$ for $x<1$) and the inequalities taken between real casts; this is $N_k(x)$ of (2.9).

**Weight.** `fk k r` is $f_k(r)=\min\!\big(1,\tfrac{k+1}{r}\big)-\min\!\big(1,\tfrac{k}{r}\big)$, the weight of (2.9), extended to all of $\mathbb R$ with Lean's convention $t/0=0$.

**Renewal constants.** `a j` is $a(j)=(j+1)\log(j+1)-j\log j-1=\int_j^{j+1}\log t\,dt$, the positive sequence $a_j$ of (2.1). `RenewalRootSet` is $\{z\in(0,1):\sum_{j\ge0}a(j+1)z^{j+1}=1\}$ (a `tsum`, equal to $0$ when not summable); `rho` is $\rho=\inf\text{RenewalRootSet}$ (`sInf`, which is $0$ on $\emptyset$). The preprint shows the root is unique in $(0,1)$ and traces it to Maier and Pomerance (1988, Section 1); the Lean definition asserts neither existence nor uniqueness. `lam` is $\lambda=\log(1/\rho)$; `gamma` is $\gamma=\big(\sum_{j\ge0}(j+1)a(j+1)\rho^{j+1}\big)^{-1}$ (the constant Ford denotes $\lambda$); `alpha s` is $\alpha(s)=\lambda e^{\lambda s}$, the preprint's $\alpha_s$ for the **phase** $s\in[0,1)$; `P H` is $P(H)=\lfloor\log\log H\rfloor_+$.

**Tail data and witnesses.** A `TailDatum H` is a pair $\eta=(Q,c)$ with $Q:\mathrm{Fin}\,H\to\mathbb N$ and a **cofactor** $c\in\mathbb N$ (the preprint's integer $a$). `tailPrime η h` is $Q(h)$ for $h<H$ and $1$ otherwise; `tailLog η h` is $\log\log$ of it, the preprint's $v_h=\log_2Q_h$. `IsWitness H s η` encodes the **tail witness** conditions (2.5): $Q(h)=1$ for $h<P(H)$, $c>0$, and for every $P(H)\le h<H$: $Q(h)$ prime, $\tfrac{9}{10}\alpha(s)h\rho^{-h}\le\mathrm{tailLog}(h)\le\tfrac{11}{10}\alpha(s)h\rho^{-h}$, and $\sum_{P(H)\le l<h}a(h-l)\,\mathrm{tailLog}(l)\le(1+10^{-4}e^{-h/40})\,\mathrm{tailLog}(h)$; moreover the largest prime factor of $c$ (`largestPrimeFactor`, at least $1$) is at most $Q(P(H))$ and $\log c\le\exp(2\alpha(s)P(H)\rho^{-P(H)})$. The **weight** `w η` is $c\prod_{P(H)\le h<H}Q(h)$; `witnesses H s d` is the set $W_{H,s}(d)$ of witnesses with $\varphi(w(\eta))=d$; `D h η` is $\sum_{P(H)\le l<H}a(h-l)\,\mathrm{tailLog}(l)$, as in (2.6); `maxD h T` is its maximum over a finite set $T$ of tail data ($0$ if $T=\emptyset$).

**Coefficient.** `AH H f s`, written $A_H(f,s)$, is the inclusion–exclusion formula (2.8),
$$\rho^{H(H-1)/2}\Big(\tfrac{\gamma}{\alpha(s)}\Big)^{H}\sum^{\mathrm f}_{d}[\text{IsTotient}(d)]\,\frac{f(\ell(d)/d)}{d}\sum^{\mathrm f}_{T}[T\neq\emptyset,\ T\subseteq\text{witnesses}(H,s,d)]\,(-1)^{|T|-1}\exp\!\Big(-\tfrac{\gamma}{\alpha(s)}\sum_{n\ge0}\rho^{H+n}\mathrm{maxD}(H+n,T)\Big),$$
where $\sum^{\mathrm f}$ is Mathlib's `finsum` (the sum over the support when finite, $0$ otherwise), $T$ ranges over `Finset (TailDatum H)`, and $H(H-1)/2$ is natural-number division; in the preprint the witness set is finite for fixed $H$. `A f s`, written $A(f,s)$, is `limUnder atTop (fun H => AH H f s)`: the limit of $H\mapsto A_H(f,s)$ when it exists, and an unspecified real otherwise. The preprint defines $A(f;s)$ only when the limit exists.

## Formalization targets

### Goal

$$\forall k\in\mathbb N,\ 0<k\Longrightarrow\neg\exists d,\ \big(\text{IsTotient}(d)\wedge k\,d<\ell(d)\big)\Longrightarrow\Big(\forall x\in\mathbb R,\ 0<x\Rightarrow N_k(x)=0\Big)\wedge\Big(\forall s\in[0,1),\ A(f_k,s)=0\Big).$$

The hypothesis $0<k$ is present (`_hk`) but not needed. The target does not say whether `hno` is satisfiable for any $k$: for $k=1$ it fails, since $\ell(2)=3>2$, and the preprint leaves $k\ge3$ undetermined. It fixes nothing about $\rho$, $\gamma$ or the convergence of $A_H$ in general, and asserts vanishing only for $x>0$ and $s\in[0,1)$.

### Related missions

- Row 1 (Totient-count asymptotics and regular variation): mission "An asymptotic formula for the number of totients" (https://prove2.me/missions/5bb42299-ae17-4482-a4fb-01065db3c2f0)

This row is the independent degenerate alternative to the weighted companion theorem of Row 1 (`weighted_totient_asymptotic`, `weighted_totient_one_two`, `coefficient_nonnegative`), which treats the case where a totient $d$ with $kd<\ell(d)$ exists. Solvers may import sibling theorems already published on the platform as reductions; none is required here.

## Significance

The theorem fixes the meaning of the family's seed condition: when it fails, the companion count is the zero function and the coefficient $A(f_k,s)$ vanishes with it, so Row 1 and this row form the case analysis announced in Section 1 of the preprint.

On status: the result is proved on paper in the OpenAI preprint, as alternative (ii) of Theorem 2.2 (Section 2.3), proved in Section 7.3 ("The positive and zero alternatives"): if no totient $d$ satisfies $\ell(d)>kd$, then $N_k(x)=0$ for every $x>0$ and $A(f_k;s)=0$ for every $s\in[0,1)$, which is exactly the Lean conclusion. In Lean the theorem `companion_zero_case` is admitted with `sorry`; nothing is machine-checked. Formalizing it validates the bundle's conventions on `limUnder`, `finsum` and casts in the degenerate case, for the whole family.

## Difficulty

The number-theoretic content is short; the obstacles lie in the conventions of the Lean definitions.

For the first conjunct, the counted $v$ are constrained by real inequalities $k\,x<\ell(v)$ with $v\le\lfloor x\rfloor_+$, while `hno` is a natural-number statement; the casts have to be reconciled, and `N` is a `Finset.filter` built under `classical`, so the decidability instance must be matched rather than assumed.

For the second conjunct, the newcomer's idea is that "the limit of an empty sum is zero". This fails on both counts. `limUnder` is not $0$ by default: if $H\mapsto A_H(f_k,s)$ did not converge, `A (fk k) s` would be an arbitrary real, so the sequence must be shown to converge. And `finsum` is $0$ on infinite support, which cannot be invoked positively; the summands themselves must vanish, which hinges on the value of $f_k$ at $\ell(d)/d$ for totients $d$, with the real division by the cast of $d$; $\rho$, $\gamma$ and the witness sets never need evaluating.

## Formalization scope

The target is the declaration below, published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and referenced, not redrafted. The definition bundle `Def_TotientCompanionZero` (`IsTotient`, `ell`, `a`, `RenewalRootSet`, `rho`, `lam`, `gamma`, `P`, `alpha`, `largestPrimeFactor`, `TailDatum`, `tailPrime`, `tailLog`, `IsWitness`, `w`, `witnesses`, `D`, `maxD`, `AH`, `A`, `N`, `fk`) is likewise published verbatim and imported.

```lean
def A (f : ℝ → ℝ) (s : ℝ) : ℝ := limUnder atTop (fun H : ℕ => AH H f s)

def N (k : ℕ) (x : ℝ) : ℝ := by
  classical
  exact (((Finset.Icc 1 ⌊x⌋₊).filter fun v =>
    IsTotient v ∧ (k : ℝ) * x < ell v ∧ (ell v : ℝ) ≤ (k+1 : ℝ) * x).card : ℝ)

def fk (k : ℕ) (r : ℝ) : ℝ := min 1 ((k+1 : ℝ) / r) - min 1 ((k : ℝ) / r)

/-- Without a totient value whose least preimage exceeds its prescribed multiple,
both the weighted count and its limiting coefficient vanish. -/
theorem companion_zero_case (k : ℕ) (_hk : 0 < k)
    (hno : ¬ ∃ d : ℕ, IsTotient d ∧ k*d < ell d) :
    (∀ x : ℝ, 0 < x → N k x = 0) ∧
    (∀ s ∈ Set.Ico (0 : ℝ) 1, A (fk k) s = 0) := by
  sorry
```

Conventions the statement commits to:

- `ell` is total on $\mathbb N$, returning $0$ for non-totients; `hno` quantifies over all `d : ℕ`, guarded by `IsTotient d`, and `k*d < ell d` is a natural-number inequality.
- `N k x` is the real cast of a `Finset.card` over `Finset.Icc 1 ⌊x⌋₊` (`Nat.floor`); the inequalities on `ell v` are in $\mathbb R$ with casts `(k : ℝ)`, `(k+1 : ℝ)`; the filter predicate is decided by a `classical` instance.
- `fk k` is passed to `A` as a function `ℝ → ℝ`, with real division ($t/0=0$), whereas the preprint's $f_k$ is a function $[1,\infty)\to[0,1]$.
- `A` is `Filter.limUnder` along `atTop` on `ℕ`; `AH` uses two nested `finsum`s and a `tsum`; `rho` is `sInf` of a set not asserted nonempty; `maxD` uses `Finset.sup'` guarded by nonemptiness; `H*(H-1)/2` is `Nat` division; `D` and `IsWitness` use `a (h-l)` with natural subtraction.
- The quantifier over $s$ is `s ∈ Set.Ico (0 : ℝ) 1`; `_hk : 0 < k` is unused.

No trivializing reading exists: `limUnder` does not evaluate to $0$ on a non-convergent sequence, and refuting `hno` for every $k\ge1$ is not available, since the preprint leaves the seed condition undetermined beyond $k=1,2$.

Infrastructure needed: `Nat.totient` positivity and `Nat.totient_lt`, `Nat.find` specification lemmas, cast monotonicity between $\mathbb N$ and $\mathbb R$, `Finset.card_eq_zero`, `finsum` vanishing lemmas, and `Filter.Tendsto.limUnder_eq`. Welcome contributions: the two conjuncts as separate lemmas, and a lemma that `AH H (fk k) s = 0` for every `H` under `hno`.

## Selected references

- OpenAI, *An asymptotic formula for the number of totients*, preprint, September 25, 2026, https://github.com/openai/math/blob/main/preprints/An-asymptotic-formula-for-the-number-of-totients-September-25-2026/An-asymptotic-formula-for-the-number-of-totients-September-25-2026.pdf
- OpenAI, *An asymptotic formula for the number of totients*, docs page, https://github.com/openai/math/blob/main/lean/docs/024.md
- Lean statement, `OAI.TotientAsymptotic.companion_zero_case`, https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/TotientCompanionZero.lean
- S. S. Pillai, *On some functions connected with $\phi(n)$*, Bull. Amer. Math. Soc. 35 (1929), 832–836, https://www.ams.org/journals/bull/1929-35-06/S0002-9904-1929-04799-2/S0002-9904-1929-04799-2.pdf
- P. Erdős, *On the normal number of prime factors of $p-1$ and some related problems concerning Euler's $\phi$-function*, Quart. J. Math. 6 (1935), 205–213, https://doi.org/10.1093/qmath/os-6.1.205
- P. Erdős, *Some remarks on Euler's $\phi$ function and some related problems*, Bull. Amer. Math. Soc. 51 (1945), 540–544, https://users.renyi.hu/~p_erdos/1945-08.pdf
- P. Erdős and R. R. Hall, *Distinct values of Euler's $\phi$-function*, Mathematika 23 (1976), 1–3, https://doi.org/10.1112/S0025579300006100
- P. Erdős, *Some unconventional problems in number theory*, Journées Arithmétiques de Luminy, Astérisque 61 (1979), 73–82, https://www.numdam.org/item/AST_1979__61__73_0/
- P. Erdős, *Some of my favourite problems in number theory, combinatorics, and geometry*, Resenhas IME-USP 2 (1995), 165–186, https://doi.org/10.11606/resimeusp.v2i2.74798
- C. Pomerance, *On the distribution of the values of Euler's function*, Acta Arith. 47 (1986), 63–70, https://doi.org/10.4064/aa-47-1-63-70
- H. Maier and C. Pomerance, *On the number of distinct values of Euler's $\varphi$-function*, Acta Arith. 49 (1988), 263–275, https://doi.org/10.4064/aa-49-3-263-275
- K. Ford, *The distribution of totients*, Ramanujan J. 2 (1998), 67–151; revised version https://arxiv.org/abs/1104.3264v2
