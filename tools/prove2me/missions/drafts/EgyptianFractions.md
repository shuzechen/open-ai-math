# Short Egyptian fractions I: Short expansions, counting, and prescribed denominators

## Motivation

An **Egyptian-fraction expansion** of a positive rational number is a finite sum of distinct reciprocals of positive integers. The greedy algorithm shows that every $a/b$ with $1 \le a < b$ has one; the quantitative questions are harder: the worst-case length over a fixed denominator $b$, the number of $k$-term expansions of $1$, and which integers can be forced to appear as denominators. The OpenAI preprint *Short Egyptian fractions* (September 25, 2026) proves Erdős's conjecture, Erdős Problem 304, that the worst case is $O(\log\log b)$, and derives from it that the number $F(k)$ of $k$-term expansions of $1$ and the least integer $v(k) \ge 2$ never occurring as such a denominator both grow doubly exponentially in $k$.

*Timeline.* In 1950 Erdős proved $N(b) \ll \log b/\log\log b$ for the worst-case length $N(b)$, conjectured the double-logarithmic upper bound, and proved the matching lower order. The question reappears in Erdős and Graham (1980); Vose (1985) obtained $N(b) \ll \sqrt{\log b}$. Erdős and Graham also asked for estimates of $F(k)$: Konyagin (2014) proved a lower bound whose double logarithm has order $k/\log k$, and Elsholtz and Planitzer (2021) an upper bound with double logarithm $O(k)$. For prescribed denominators, van Doorn and Tang (2026) proved $v(k) \ge \exp(ck^2)$ and anticipated the connection with uniform short expansions.

## Setting

For $k \in \mathbb{N}$, a **finite sequence** of length $k$ is a function $n : \mathrm{Fin}\,k \to \mathbb{N}$, written $n_0, \dots, n_{k-1}$; it is **strictly increasing** (`StrictMono n`) when $i < j$ implies $n_i < n_j$, which encodes distinctness. Sums are taken in $\mathbb{Q}$, with $1/n_i = (1:\mathbb{Q})/(n_i:\mathbb{Q})$.

For $x \in \mathbb{Q}$, **`IsEgyptianExpansion x n`** holds when every $n_i \ge 2$, $n$ is strictly increasing, and $\sum_{i<k} 1/n_i = x$. For $a, b \in \mathbb{N}$, **`egyptianLengths a b`** is the set of $k$ admitting such an expansion of $(a:\mathbb{Q})/(b:\mathbb{Q})$, and **`egyptianLength a b`** is its infimum `sInf`, the least element when the set is nonempty and $0$ otherwise: the preprint's $N(a,b)$. **`maxEgyptianLength b`** is the `Finset.sup` over $a \in \{0,\dots,b-1\}$ of `egyptianLength a b` for $1 \le a$ and of $0$ for $a = 0$: the preprint's $N(b) = \max_{1 \le a < b} N(a,b)$.

A **one-expansion** of length $k$ (`IsOneExpansion n`) is a strictly increasing $n : \mathrm{Fin}\,k \to \mathbb{N}$ with every $n_i \ge 1$ and $\sum_{i<k} 1/n_i = 1$; the denominator $1$ is permitted, as in the preprint's $F(k)$. **`OneExpansions k`** is the set of these and **`F k`** its `Set.ncard` ($0$ for an infinite set). **`D k`** is the set of integers $m \ge 2$ occurring in some one-expansion of length $k$ (the preprint's $D_k$); **`missingDenominators k`** is $\{m \mid 2 \le m\} \setminus D(k)$; **`v k`** is `sInf (missingDenominators k)`; and **`prescribedSlope k`** is $\log(\log(v(k)))/k$ in $\mathbb{R}$.

## Formalization targets

### Goal

$$
\forall\, a\, b \in \mathbb{N},\ 1 \le a \to a < b \to
\Big(\exists\, n : \mathrm{Fin}(\mathrm{egyptianLength}\,a\,b) \to \mathbb{N},\ \mathrm{IsEgyptianExpansion}\big(\tfrac{a}{b}\big)\, n\Big)
\wedge
\Big(\forall\, k,\ \big(\exists\, n : \mathrm{Fin}\,k \to \mathbb{N},\ \mathrm{IsEgyptianExpansion}\big(\tfrac{a}{b}\big)\, n\big) \to \mathrm{egyptianLength}\,a\,b \le k\Big).
$$

For every $a/b$ with $1 \le a < b$, an Egyptian expansion of length exactly `egyptianLength a b` exists and no shorter one does, so this length is a genuine minimum rather than the junk value $0$ of an empty infimum: the well-definedness of the preprint's $N(a,b)$. It fixes no bound on length or denominators and nothing about $a = 0$ or $a \ge b$.

### Milestones

- Theorem 1.1 — $N(b)$ is of order $\log\log b$ (`main_double_log_order`)
- Supporting theorem: finiteness of $k$-term expansions of $1$, $F(k) \le k^{2^k-1}$, $n_i \le k^{2^i}$ (`one_expansions_finite_and_bounded`)
- Corollary 1.2 — $\log\log F(k)$ is of order $k$ (`counting_double_log_order`)
- Supporting theorem: padding an expansion of $1$ while retaining a denominator (`exact_marker_padding`)
- Supporting theorem: every $m \ge 2$ occurs as a denominator in some expansion of $1$ (`every_exact_marker_occurs`)
- Supporting theorem: prescribed denominator $m$ with at most $(257/\log 2 + \varepsilon)\log\log m$ terms (`quantitative_marked_length`)
- Supporting theorem: $D_k$ is finite and $v(k)$ is its least missing denominator (`missing_denominator_semantics`)
- Corollary 1.3 — double-exponential bounds for $v(k)$ and the slope $\log\log v(k)/k$ (`prescribed_denominator_corollary`)

### Related missions

- Row 2 (Optimal order of the shortest Egyptian-fraction expansions): mission "Short Egyptian fractions" (https://prove2.me/missions/10428f3d-f5b6-463d-8412-cb1e9f4d7927)

Row 2 states Theorem 1.1 as `OAI.ShortEgyptian.main` with its own definitions; milestone `main_double_log_order` is the same statement in the `Problem337` definitions, and this row's goal is the existence-and-minimality statement both presuppose. Solvers may import sibling theorems already published on the platform as reductions.

## Significance

The goal theorem makes `egyptianLength` meaningful: `sInf` on `ℕ` returns $0$ on the empty set, so without it "minimal length $0$" and "no expansion exists" coincide. Once proved, it certifies `egyptianLength a b` as the least number of distinct unit fractions summing to $a/b$, and `maxEgyptianLength b` as $N(b)$. The milestones record the preprint's Theorem 1.1 ($N(b) = \Theta(\log\log b)$), Corollary 1.2 ($\log\log F(k) = \Theta(k)$) and Corollary 1.3 ($\log\log v(k) = \Theta(k)$, slopes between $\log 2/257$ and $\log 2$), with the supporting bounds and constructions behind them.

On status: these results are proved on paper in the OpenAI preprint; in Lean all nine statements are admitted with `sorry`, and nothing is machine-checked yet. Formalizing the goal gives a verified foundation; the milestones would be the first machine-checked record of the quantitative results.

## Difficulty

The second conjunct is immediate (`Nat.sInf_le`). The content is the first conjunct, and the newcomer's first idea, applying `Nat.sInf_mem`, fails exactly where it matters: `Nat.sInf_mem` needs `egyptianLengths a b` to be nonempty, and nonemptiness is the existence of an Egyptian expansion of $a/b$. The preprint takes this from the greedy algorithm, whose step subtracts $1/\lceil C/A\rceil$ from a remainder $A/C$ and strictly decreases the numerator (its Lemma 2.3).

The second newcomer idea, $a$ copies of $1/b$, violates strict monotonicity, and repairing duplicates by splitting unit fractions does not obviously terminate (the preprint's Lemma 2.2 uses a finiteness argument). Any construction must keep every denominator at least $2$ (using $a < b$), order denominators strictly along the index, give exact equality in $\mathbb{Q}$ through casts, and terminate. In Lean the witness lives in `Fin (egyptianLength a b)`, so existence for some length $k$ must be transported through `Nat.sInf_mem`.

## Formalization scope

```lean
theorem egyptian_length_is_minimum :
    ∀ a b : ℕ, 1 ≤ a → a < b →
  (∃ n : Fin (egyptianLength a b) → ℕ,
    IsEgyptianExpansion ((a : ℚ) / (b : ℚ)) n) ∧
  (∀ k : ℕ, (∃ n : Fin k → ℕ,
    IsEgyptianExpansion ((a : ℚ) / (b : ℚ)) n) →
    egyptianLength a b ≤ k) := by
  sorry
```

The theorem and the definition bundle (`IsEgyptianExpansion` through `prescribedSlope`) are already published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and are referenced, not redrafted.

Conventions the statement commits to:

- **Hypotheses.** $a, b \in \mathbb{N}$ with $1 \le a < b$; hence $b \ge 2$ and $(a:\mathbb{Q})/(b:\mathbb{Q})$ lies in $(0,1)$. Lowest terms are not required.
- **Denominators.** Every $n_i \ge 2$ and `StrictMono n` on `Fin k`; a distinct but unordered sequence does not qualify. Total division is harmless since $n_i \ge 2$.
- **Length.** `egyptianLength a b` is `sInf` on `ℕ`, equal to $0$ on the empty set; the theorem certifies that this junk value does not occur. Length $0$ never qualifies, since the empty sum is $0 \ne a/b$.
- **Dependent witness.** The first conjunct quantifies over `Fin (egyptianLength a b) → ℕ`. No decidability instances are needed.

Milestone conventions: thresholds $b_0$, $k_0$, $m_\varepsilon$ are existential naturals, so junk values of `Real.log` never matter; exponents $2^k - 1$ and $2^{k-1}$ use natural-number subtraction; `Filter.liminf`/`Filter.limsup` of `prescribedSlope` are taken in $\mathbb{R}$ along `Filter.atTop`.

No trivializing reading exists: an expansion with strictly increasing denominators at least $2$ must be exhibited. Welcome infrastructure: an existence lemma for expansions of every $a/b$ with $1 \le a < b$, lemmas extending a `StrictMono` function on `Fin k` by a smallest term (`Fin.cons`, `Fin.sum_univ_succ`), and `Nat.sInf_mem` / `Nat.sInf_le` bookkeeping; milestone proofs are welcome.

## Selected references

- OpenAI, *Short Egyptian fractions*, preprint, September 25, 2026: https://github.com/openai/math/blob/main/preprints/Short-Egyptian-fractions-September-25-2026/Short-Egyptian-fractions-September-25-2026.pdf
- OpenAI, Lean statement `EgyptianFractions.lean` (openai/math, commit adc7f12): https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/EgyptianFractions.lean
- P. Erdős, "Az $1/x_1 + 1/x_2 + \cdots + 1/x_n = a/b$ egyenlet egész számú megoldásairól", Matematikai Lapok 1 (1950), 192–210. https://users.renyi.hu/~p_erdos/1950-02.pdf
- P. Erdős and R. L. Graham, *Old and New Problems and Results in Combinatorial Number Theory*, L'Enseignement Mathématique, Geneva, 1980. https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf
- M. D. Vose, "Egyptian fractions", Bulletin of the London Mathematical Society 17 (1985), 21–24. https://doi.org/10.1112/blms/17.1.21
- S. V. Konyagin, "Double exponential lower bound for the number of representations of unity by Egyptian fractions", Matematicheskie Zametki 95 (2014), 312–316. https://doi.org/10.4213/mzm10417
- C. Elsholtz and S. Planitzer, "Sums of four and more unit fractions and approximate parametrizations", Bulletin of the London Mathematical Society 53 (2021), 695–709. https://doi.org/10.1112/blms.12452
- W. van Doorn and Q. Tang, "The smallest denominator not contained in a unit fraction decomposition of $1$ with fixed length", Mathematical Proceedings of the Cambridge Philosophical Society (2026), 1–9. https://doi.org/10.1017/S0305004126102102 (arXiv:2512.22083)
- T. F. Bloom, Erdős Problem 304: https://www.erdosproblems.com/304
