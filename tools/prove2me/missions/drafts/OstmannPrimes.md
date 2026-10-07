## Motivation

Goldbach's problem asks which integers are sums of two primes. Its inverse asks whether the primes can themselves be a sumset: are there sets $A, B$ of nonnegative integers, each with at least two elements, such that $A + B$ agrees with the primes from some point on? Ostmann raised this in his 1956 treatise (Ostmann 1956, p. 13) and conjectured the answer is no: the primes are **asymptotically additively indecomposable**. The question is also known as the **inverse Goldbach problem**. It sits at the interface of sieve theory and additive combinatorics: a hypothetical decomposition imposes residue restrictions on $A$ and $B$ at every prime, the large sieve turns these into counting bounds, yet counting bounds have never sufficed to exclude a decomposition. Green and Harper (2014) formulated an inverse-sieve conjecture that would imply Ostmann's conjecture.

*Timeline.* Hornfeck (1954) obtained the first restrictions on a hypothetical decomposition. Laffer and Mann (1964, Theorem 12) showed both summands would have to be infinite. Sieve arguments of Pomerance, Sárközy and Stewart (1988), Hofmann and Wolke (1996) and Elsholtz (2001) tightened the restrictions; Elsholtz also ruled out three nontrivial summands. Elsholtz and Harper (2015) sharpened the counting bounds, Green and Harper (2014) gave the conditional inverse-sieve route, and Hanson (2020) and Croot, Mao, Pohoata and Yip (2026) proved partial inverse results. The OpenAI preprint "The additive indecomposability of the primes" (September 24, 2026) proves the conjecture on paper.

## Setting

Write $\mathbb{N} = \{0, 1, 2, \dots\}$ for the natural numbers, including $0$; this is the type `ℕ` of the Lean statement and the set $N_0$ of the preprint. The **primes** are $P = \{n \in \mathbb{N} : n \text{ is prime}\}$, with $0$ and $1$ not prime; in Lean, `{n : ℕ | Nat.Prime n}`.

For $A, B \subseteq \mathbb{N}$ the **sumset** is
$$A + B = \{a + b : a \in A,\ b \in B\}.$$
In Lean, `A + B` on `Set ℕ` is the pointwise sum provided by `open scoped Pointwise`; it is empty if either set is empty.

A set $A \subseteq \mathbb{N}$ is **nontrivial** if it contains two distinct elements; `Set.Nontrivial A` unfolds to `∃ x ∈ A, ∃ y ∈ A, x ≠ y`. This is the only hypothesis on the summands; it excludes the empty set and singletons, and a singleton $\{a\}$ would decompose any $S \subseteq [a, \infty)$ as $\{a\} + (S - a)$.

The **symmetric difference** of $X, Y \subseteq \mathbb{N}$ is $X \,\triangle\, Y = (X \setminus Y) \cup (Y \setminus X)$, the elements in exactly one of the two; in Lean, `X ∆ Y` via `open scoped symmDiff`. Two subsets of $\mathbb{N}$ are **asymptotically equal** if their symmetric difference is finite. A set is **infinite** (`Set.Infinite X`) when it is not `Set.Finite`.

Ostmann's conjecture says: $P$ is not asymptotically equal to $A + B$ for any nontrivial $A, B$.

## Formalization targets

### Goal

The target is Theorem 1.1 of the preprint, exactly as stated in `OstmannPrimes.lean`:
$$\forall\, A, B \subseteq \mathbb{N}:\quad A \text{ nontrivial} \ \wedge\ B \text{ nontrivial} \ \Longrightarrow\ (A + B)\,\triangle\, P \text{ is infinite}.$$

Equivalently, every finite modification of the primes is additively indecomposable into two sets with at least two elements each. Everything else is left unfixed: $A$ and $B$ may be finite or infinite, may contain $0$, may overlap, and carry no density or structural hypothesis. The conclusion does not say which side of the symmetric difference is infinite; the Lean target asks only for infinitude of the symmetric difference.

### Related missions

- Row 1 (Ostmann's inverse Goldbach theorem and the infinite-summands case): mission "The additive indecomposability of the primes" (https://prove2.me/missions/63001ea7-1f73-4952-a603-b32c036bd072); goal theorems `OAI.Ostmann.inverseGoldbach`, `OAI.Ostmann.twoInfiniteSummandsImpossible`.

This row restates the full result (Theorem 1.1) as a single quantified statement; up to the precise Lean phrasing it is the same result as `inverseGoldbach`, and it follows from `twoInfiniteSummandsImpossible` (Theorem 2.3, the two-infinite-summands case) together with the finite-summand reduction of Lemma 2.2. Solvers may import sibling theorems already published on the platform as reductions.

## Significance

The result settles a seventy-year-old conjecture: the primes, and every set differing from them in finitely many elements, cannot be written as a sumset of two sets each with at least two elements. The preprint's approach bypasses the inverse-sieve classification that Green and Harper identified as sufficient, working directly from the residue restrictions and prime coverage.

Status: the theorem is proved on paper in the OpenAI preprint listed below. In Lean it is admitted with `sorry`; nothing is machine-checked yet, and a solution would be the first formal verification of any part of the argument. Formalizing it would also bring reusable analytic number theory (large-sieve inequalities, character-sum mean values, primes in progressions) into Lean and independently check a long technical proof.

## Difficulty

The newcomer's first idea is counting. Under a hypothetical decomposition, every sufficiently large prime up to $x$ is a sum $a + b$ with $a, b \le x$, so $A(x) B(x) \gg x / \log x$ where $A(x) = |A \cap [0, x]|$. Conversely, each prime $p$ forces the residues of $A$ and $-B$ modulo $p$ to be disjoint, and the large sieve gives upper bounds. But, as the preprint notes, bounds of the shape $A(x) B(x) \ll x$ are compatible with the coverage lower bound, and even the Elsholtz–Harper bounds at the square-root scale leave room for a decomposition. Counting alone fails.

A second idea is a single modulus: all large primes are odd, so one might hope for a contradiction modulo $2$ or a small prime. This fails too: $A$ and $B$ can have complementary residue sets at every prime with no single modulus producing a contradiction, so all primes must be used simultaneously.

The preprint's introduction describes its route as follows. A short sieve argument (Lemma 2.2) reduces to two infinite summands (Theorem 2.3). The proof then shows the residue sets of the summands are approximately complementary and uniform on prime averages, rules out persistent correlations with translated multiplicative characters, extracts nonsparse additive transforms from prime coverage, and compares a positive statistic built by repeated Cauchy–Schwarz transfers with a finite-field model to reach a contradiction. The technical sections occupy roughly seventy pages; nothing beyond the reduction to two infinite summands is elementary.

## Formalization scope

The Lean statement is

```lean
import Mathlib

namespace OAI

open scoped Pointwise symmDiff

namespace Ostmann

theorem main : ∀ A B : Set ℕ, A.Nontrivial → B.Nontrivial →
    Set.Infinite ((A + B) ∆ {n : ℕ | Nat.Prime n}) := by
  sorry

end Ostmann

end OAI
```

The theorem is already published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and is referenced, not redrafted. There is no definition bundle: every notion used is from Mathlib.

Conventions the statement commits to:

- The summands are arbitrary `Set ℕ`, with $0 \in \mathbb{N}$, matching the preprint's $N_0$. Nothing beyond `Set.Nontrivial` (two distinct elements) is assumed; this is stronger than `Set.Nonempty` and rules out singleton decompositions.
- `A + B` is the pointwise sumset `Set.image2 (· + ·) A B`; addition is in `ℕ`, so no casts occur.
- `∆` is `symmDiff` on `Set ℕ`, equal to `(A + B) \ P ∪ P \ (A + B)`.
- `Set.Infinite S` is `¬ S.Finite`. No decidability instances are required; the statement is classical.
- Primality is `Nat.Prime`, under which `0` and `1` are not prime, so the prime set agrees with the positive primes of the preprint.

There is no trivializing reading: nontriviality forbids an empty or singleton sumset, and one composite sum or one uncovered prime does not discharge a goal demanding an infinite symmetric difference for every admissible pair.

Infrastructure needed, as far as the preprint's introduction and bibliography indicate: the additive large sieve in the form of Montgomery and Vaughan (1973); Mertens-type estimates; mean values of real character sums; Fourier analysis on $\mathbb{F}_p$ with probability normalization; prime estimates in arithmetic progressions allowing for an exceptional real character; and Kneser's addition theorem. Much of this is absent from Mathlib or present only in a different form.

Welcome contributions: formal proofs of Lemma 2.1 (fixed-shifts sieve bound) and Lemma 2.2 (finite-summand reduction), which reduce this mission to the sibling theorem `twoInfiniteSummandsImpossible`; the large sieve inequality in the preprint's form (2.1); finite-field Fourier infrastructure; and the residue and collision estimates of Section 2.

## Selected references

- OpenAI, *The additive indecomposability of the primes*, OpenAI Math Release preprint, September 24, 2026. https://github.com/openai/math/blob/main/preprints/the-additive-indecomposability-of-the-primes-September-24-2026/paper.pdf
- Lean statement `OAI.Ostmann.main`, `lean/ComparatorChallenges/OstmannPrimes.lean`, openai/math commit adc7f12. https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/OstmannPrimes.lean
- H.-H. Ostmann, *Additive Zahlentheorie. Erster Teil: Allgemeine Untersuchungen*, Springer, 1956. https://doi.org/10.1007/978-3-662-11030-0
- W. B. Laffer and H. B. Mann, *Decomposition of sets of group elements*, Pacific Journal of Mathematics 14 (1964), 547–558. https://doi.org/10.2140/pjm.1964.14.547
- C. Elsholtz, *The inverse Goldbach problem*, Mathematika 48 (2001), 151–158. https://doi.org/10.1112/S0025579300014406
- B. Green and A. J. Harper, *Inverse questions for the large sieve*, Geometric and Functional Analysis 24 (2014), 1167–1203. https://doi.org/10.1007/s00039-014-0288-1
- C. Elsholtz and A. J. Harper, *Additive decompositions of sets with restricted prime factors*, Transactions of the American Mathematical Society 367 (2015), 7403–7427. https://doi.org/10.1090/S0002-9947-2014-06384-8
- E. Croot, J. Mao, C. Pohoata and C. H. Yip, *A sharp inverse theorem for the quadratic large sieve*, arXiv:2607.15311, 2026. https://arxiv.org/abs/2607.15311v2
- H. L. Montgomery and R. C. Vaughan, *The large sieve*, Mathematika 20 (1973), 119–134. https://doi.org/10.1112/S0025579300004708
