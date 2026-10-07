## Motivation

For a positive integer $n$, **Jacobsthal's function** $j(n)$ is the least positive integer $m$ such that every run of $m$ consecutive integers contains an integer coprime to $n$. Writing $\omega(n)$ for the number of distinct prime divisors of $n$ (with $\omega(1)=0$), the uniform version is

$$h(k)=\sup\{\,j(n) : n\ge 1,\ \omega(n)\le k\,\},\qquad k\ge 1 .$$

Since $j(n)$ depends only on the set of primes dividing $n$, $h(k)-1$ is the greatest length of an interval that can be covered by the divisibility classes of at most $k$ primes; by the Chinese remainder theorem this is the same as covering an interval by one arbitrary forbidden residue class modulo each of at most $k$ primes. The same covering constructions produce long gaps between consecutive primes, which ties $h(k)$ to Rankin's construction and to the Ford–Green–Konyagin–Maynard–Tao theorem on prime gaps.

Jacobsthal asked whether $h(k)\ll k^2$; Erdős recorded the question in 1962. The OpenAI preprint proves $h(k)\ll k^2/(\log\log(3k))^2$, which answers the question affirmatively and removes a further iterated-logarithmic factor. This mission asks for the quadratic bound itself, $h(k)\le Ck^2$; the sibling mission asks for the sharper form.

*Timeline.* Jacobsthal introduced $j(n)$ in a series of papers beginning in 1960. Erdős (1962) recorded the quadratic-bound question and observed that Brun's method gives $h(k)\ll k^{C_0}$ for some absolute exponent $C_0$. Iwaniec's 1971 work on the error term in the linear sieve gave order $k^2\log^2 k$ when the prime divisors are the first $k$ primes. Vaughan (1977) proved $j(n)\ll \omega(n)^2(\log 2\omega(n))^4$ uniformly for $n>1$, and Iwaniec (1978) obtained $h(k)\ll k^2\log^2 k$ for arbitrary prime sets. On the lower side, Hajdu and Saradha (2012) found $j(P_{24})=234<236=h(24)$, where $P_k$ is the product of the first $k$ primes, refuting Jacobsthal's suggestion that primorials are always extremal; Ford, Green, Konyagin, Maynard and Tao (2018) give $j(P_k)\gg k(\log k)^2\log\log\log k/\log\log k$, hence a lower bound for $h(k)$ of the same order. The OpenAI preprint (September 2026) proves $h(k)\ll k^2/(\log\log(3k))^2$.

## Setting

Objects live in the natural numbers $\mathbb{N}=\{0,1,2,\dots\}$, the integers $\mathbb{Z}$ and the reals $\mathbb{R}$. For $n\in\mathbb{N}$, the **distinct prime divisors** of $n$ form the finite set `n.primeFactors`; its cardinality `n.primeFactors.card` is $\omega(n)$, with $\omega(0)=\omega(1)=0$ in Lean. Two natural numbers $x,n$ are **coprime**, written `x.Coprime n`, when $\gcd(x,n)=1$. For $b\in\mathbb{Z}$, `b.natAbs` is $|b|\in\mathbb{N}$, and $|b|$ is coprime to $n$ exactly when $b$ and $n$ share no prime divisor.

Fix $k,m\in\mathbb{N}$. Say that $m$ is a **Jacobsthal bound** for $k$, written `IsJacobsthalBound k m`, when for every $n\in\mathbb{N}$ with $n>0$ and $\omega(n)\le k$, and every starting point $a\in\mathbb{Z}$, there is an offset $i\in\mathbb{N}$ with $i<m$ such that $|a+i|$ is coprime to $n$. In words: every block $a,a+1,\dots,a+m-1$ of $m$ consecutive integers, beginning at any signed integer, contains an integer coprime to $n$, uniformly over all positive $n$ with at most $k$ distinct prime divisors. The property is monotone in $m$, and $m=0$ is never a Jacobsthal bound. The paper's $h(k)$ is exactly the least $m$ with `IsJacobsthalBound k m`; the Lean file does not define $h$, it only uses the predicate.

The **quadratic Jacobsthal statement** `JacobsthalQuadratic` is the proposition that there is a real constant $C>0$ such that for every $k\in\mathbb{N}$ with $k>0$ there exists $m\in\mathbb{N}$ with `IsJacobsthalBound k m` and $m\le Ck^2$, the inequality taken in $\mathbb{R}$ after casting $m$ and $k$.

## Formalization targets

### Goal

$$\exists\,C\in\mathbb{R},\ C>0,\ \ \forall k\in\mathbb{N},\ k>0,\ \ \exists\,m\in\mathbb{N}:\ \ \mathrm{IsJacobsthalBound}(k,m)\ \wedge\ m\le C\,k^2 .$$

Equivalently, $h(k)\le Ck^2$ for every $k\ge 1$ with one absolute constant $C$. The statement leaves unfixed the value of $C$ (the preprint does not make it explicit), the true order of growth of $h(k)$ (upper and lower bounds remain far apart), and which prime sets attain $h(k)$. It gives no lower bound and says nothing about primorials specifically.

### Related missions

- Row 2 (Jacobsthal bound with an iterated-logarithm saving): mission "A quadratic bound for Jacobsthal's function" (https://prove2.me/missions/b1214931-d74b-402a-8fd3-0d397c8238d3); goal theorem `OAI.Erdos970.Erdos970Final.erdos_970_iterated_log`.

This row is the weaker form of row 2: since $\log\log(3k)\ge\log\log 3>0$ for $k\ge1$, the quadratic bound follows from the iterated-logarithm bound with constant $C/(\log\log 3)^2$, provided the sibling's Lean statement is phrased through the same predicate. Solvers may import sibling theorems that are already published on the platform as reductions.

## Significance

The result gives a uniform quadratic bound on the longest interval that at most $k$ primes can cover, with no restriction on the sizes of the primes or on where the interval starts. It settles the question Erdős attributed to Jacobsthal and improves Iwaniec's $k^2\log^2 k$ by two logarithms. The preprint derives it from a quantitative covering estimate (its Theorem 1.2): for residue classes $a_p \bmod p$ prescribed at every prime $p\le z$, the number of integers in $[1,Y]$, $Y=\lfloor z^2/(\log z)^2\rfloor$, avoiding all of them is at least $c\,YV_0/B^2$, where $V_0=\prod_{p\le w}(1-1/p)$, $w=\log z/(\log\log z)^2$ and $B=\log z/\log w$. The survivor count, rather than mere positivity, is what permits the passage from a prime cutoff $z$ to a bound in the number of prime divisors.

Status: the theorem is proved on paper in the OpenAI preprint and is admitted with `sorry` in the Lean comparator file; nothing is machine-checked yet. A Lean proof would be the first formal verification of any bound on $h(k)$ of quadratic order, and would require a substantial body of sieve theory that Mathlib does not currently contain in usable form.

## Difficulty

The newcomer's first idea is a union bound: among $m$ consecutive integers, each prime $p\mid n$ removes at most $\lceil m/p\rceil$, so at most $m\sum_{p\mid n}1/p+k$ are removed. This yields a survivor only when $\sum_{p\mid n}1/p<1$, which already fails for $n=2\cdot3\cdot5\cdot7$; small primes must be sieved, not union-bounded. The second idea, Legendre's inclusion–exclusion, carries an error term of size $2^k$ and is useless beyond $k$ of logarithmic size. Brun's sieve gives a polynomial bound and the linear sieve gives $k^2$ up to logarithms, but the quadratic scale is exactly where the linear sieve stops: Vaughan explained the exponent $2$ through the one-dimensional sieve's restriction to moduli near the square root of the interval length, which in standard notation is the vanishing of the lower sieve function $f$ at sieve parameter $2$. Any argument reaching $h(k)\ll k^2$ must operate at this limiting parameter, where the leading lower-sieve term is zero.

According to the preprint's introduction, the proof keeps a boundary contribution that disappears from the leading linear-sieve term, evaluates it through a reference calculation for a decreasing-prime expansion, and then controls the discrepancy between this reference and the actual prescribed classes; that comparison requires an inverse estimate and stopped counts, since positivity of the reference calculation alone does not give a lower bound for the original sieve. The prime divisors of $n$ above the cutoff $z=A_0k\log k/\log\log k$ are removed afterwards by a progression upper sieve, whose loss the covering estimate must dominate. The bounded range of $k$, where asymptotic estimates say nothing, needs separate handling.

## Formalization scope

The target is `OAI.Erdos970.Erdos970Final.erdos_970_quadratic`, with definitions in namespace `OAI.Erdos970.NumberTheoryLean.Targets`:

```lean
def IsJacobsthalBound (k m : ℕ) : Prop :=
  ∀ n : ℕ, 0 < n → n.primeFactors.card ≤ k →
    ∀ a : ℤ, ∃ i : ℕ, i < m ∧ (a + i).natAbs.Coprime n

def JacobsthalQuadratic : Prop :=
  ∃ C : ℝ, 0 < C ∧ ∀ k : ℕ, 0 < k →
    ∃ m : ℕ, IsJacobsthalBound k m ∧ (m : ℝ) ≤ C * (k : ℝ) ^ 2

theorem erdos_970_quadratic : NumberTheoryLean.Targets.JacobsthalQuadratic := by
  sorry
```

The theorem and the definition bundle (`Definitions.Def_Jacobsthal`) are already published verbatim from openai/math commit adc7f12 in the default environment (Lean 4.33.1, Mathlib 0df444a) and are referenced, not redrafted.

Conventions the statement commits to:

- `n : ℕ` with `0 < n`; $n=1$ (no prime factors) is admitted, so any Jacobsthal bound is at least $1$.
- `n.primeFactors.card ≤ k` counts distinct prime divisors, multiplicity ignored, with no restriction on their size.
- `a : ℤ` is an arbitrary signed start; `a + i` is `a + (i : ℤ)` with `i : ℕ`, so the block is $a,\dots,a+m-1$.
- Coprimality is `Nat.Coprime` of `(a + i).natAbs` with `n`; since $\gcd(|b|,n)=\gcd(b,n)$, this is ordinary coprimality of the integer $a+i$ with $n$.
- `C : ℝ`, `0 < C`, is quantified before `k`, so it is one absolute constant; `m : ℕ` may depend on `k`; `(m : ℝ) ≤ C * (k : ℝ) ^ 2` is a real inequality after casting.
- `0 < k` is needed: for $k=0$ the only admissible $n$ is $1$, which still needs $m\ge1$, while $C\cdot0^2=0$.
- No `tsum`, `sSup` or decidability instance appears; $h(k)$ is not defined, only witnessed.

No trivializing reading exists: $m$ must satisfy the full universal predicate over all $n$ and $a$, and the quantifier order forbids choosing $C$ after $k$. Infrastructure needed, none of it in Mathlib in the required form: the linear sieve with its functions $f,F$ and the fundamental lemma, an upper sieve for primes in arithmetic progressions, Mertens' product estimate, and the inverse and renewal-type estimates of the preprint. Contributions formalizing the covering estimate (Theorem 1.2) as a standalone lemma, the sieve inputs of Section 2, or the passage from a prime cutoff to a bound in $\omega(n)$ (Section 11) are welcome, as is a direct derivation of this row from the sibling theorem once that one is proved.

## Selected references

- OpenAI, *A quadratic bound for Jacobsthal's function*, preprint, September 25, 2026. https://github.com/openai/math/blob/main/preprints/A-quadratic-bound-for-Jacobsthals-function-September-25-2026/paper.pdf
- Lean comparator statement `Jacobsthal.lean`, openai/math commit adc7f12. https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/lean/ComparatorChallenges/Jacobsthal.lean
- P. Erdős, *On the integers relatively prime to $n$ and on a number-theoretic function considered by Jacobsthal*, Mathematica Scandinavica 10 (1962), 163–170. https://doi.org/10.7146/math.scand.a-10523
- H. Iwaniec, *On the error term in the linear sieve*, Acta Arithmetica 19 (1971), 1–30. https://doi.org/10.4064/aa-19-1-1-30
- R. C. Vaughan, *On the order of magnitude of Jacobsthal's function*, Proceedings of the Edinburgh Mathematical Society 20 (1977), 329–331. https://doi.org/10.1017/S0013091500026560
- H. Iwaniec, *On the problem of Jacobsthal*, Demonstratio Mathematica 11 (1978), 225–231. https://doi.org/10.1515/dema-1978-0121
- L. Hajdu and N. Saradha, *Disproof of a conjecture of Jacobsthal*, Mathematics of Computation 81 (2012), 2461–2471. https://doi.org/10.1090/S0025-5718-2012-02581-6
- K. Ford, B. Green, S. Konyagin, J. Maynard and T. Tao, *Long gaps between primes*, Journal of the American Mathematical Society 31 (2018), 65–105. https://doi.org/10.1090/jams/876
- J. Friedlander and H. Iwaniec, *Opera de Cribro*, AMS Colloquium Publications 57, 2010. https://doi.org/10.1090/coll/057
