# Statement and public-proof inspection

Task: books-uniformdistributionofsequences-equidistribution-isequidistributedmoduloone-three-halves-pow-refute

## Statement fidelity (no mathematics changed)

The actual target is **not** equidistribution of `(3/2)^n`, nor the statement about every transcendental multiplier. It is the closed proposition
`¬ Equidistribution.IsEquidistributedModuloOne (fun n => (3 / 2 : ℝ)^n)`.

Inspected the entire original prefix: `IsEquidistributed` counts indices `m < n` in every closed subinterval and divides by `(n : ℝ)`, tending to `(d-c)/(b-a)`; `IsEquidistributedModuloOne` applies this to `Int.fract` on `[0,1]`. Here the denominator interval length is 1, not zero. Beginning at n=0 instead of n=1 only changes finitely many terms. Closed-interval/singleton conventions are standard equivalent uniform-distribution criteria; no endpoint contradiction arises. The unrelated accumulation-point definition and subsequence lemma do not occur in the target's transitive dependencies. No concrete contradiction or definition error was found.

Read sources:
- Pinned upstream source: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Books/UniformDistributionOfSequences/Equidistribution.lean . Same definitions; original affirmative theorem is marked `research open` with `sorry`. The benchmark deliberately asks its negation, as specified in task.toml. The retained affirmative docstring is not the actual benchmark direction.
- Kuipers–Niederreiter, *Uniform Distribution of Sequences*: https://math.rice.edu/~michael/teaching/426_Spr14/Kuipers_Nied_UD.pdf . Read Chapter 1 definition/exercises (including equivalent closed-interval criterion, Exercise 1.4), and printed p.36 after Corollary 4.2: it is not known whether `(e^n)`, `(π^n)` or `((3/2)^n)` is uniformly distributed modulo 1. The almost-all-base result is not a theorem about this particular base.
- Publisher: https://store.doverpublications.com/products/9780486149998 . Confirms book identity/authors.
- https://arxiv.org/abs/1806.03559 (On the Uniformity of (3/2)^n Modulo 1): computational evidence for uniformity, not a proof in either direction.
- https://mathworld.wolfram.com/PowerFractionalParts.html : contextual power fractional-parts discussion.
- Wikipedia direct fetch returned HTTP 403; the actual book PDF and upstream source were accessible, so this did not block statement checking.

Conclusion: `statement_status = consistent` means no obvious statement/definition defect was found, not that the negative conjecture is known true. Open status alone is not an error.

## Public complete Lean4 proof search

First checked the skill CSV by exact equality on the full task column. No match.

Search groups actually run (web tool, not inferred from the CSV):
1. `"Lean" "three_halves_pow" equidistribution`; `"Lean4" "3/2" "equidistributed"`; `"isEquidistributedModuloOne_three_halves_pow" proof`; `"formal_conjectures_bench_refutation" "Equidistribution"`.
2. `"Lean" "not equidistributed" "3/2"`; `"Lean4" "three halves" "proof"`; `site:github.com "IsEquidistributedModuloOne" "¬"`; `site:github.com/leanprover-community/mathlib4 equidistribution powers rational 3 2`.
3. `site:github.com "three_halves_pow" "proof" "Equidistribution"`; `"Lean" "Kuipers" "Niederreiter" "proof" equidistribution`; `"Lean" "3/2" "non-equidistribution"`; `"Lean" "three_halves" "neg" equidistributed`.
4. Source/context searches using Kuipers/Niederreiter, Vijayaraghavan, powers 3/2, open status and uniform distribution. Also searched the pinned Mathlib Lean sources for `three_halves`, `IsEquidistributedModuloOne`, and equidistribution (mathlib-search.txt).

Relevant leads followed and excluded:
- Current upstream Lean source https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Books/UniformDistributionOfSequences/Equidistribution.lean was read completely. Affirmative fixed-base target still has `sorry`; no full negative proof appears. It contains complete proofs of accumulation-point auxiliary results, which do not settle equidistribution/non-equidistribution.
- Issue https://github.com/google-deepmind/formal-conjectures/issues/5003 and merged PR https://github.com/google-deepmind/formal-conjectures/pull/5838 were read. They negate the **universal transcendental-multiplier** claim, not this fixed base, fixed multiplier 1 target. The issue explicitly says the fixed-base question remains open; the updated Lean theorem for the different multiplier claim itself still has `sorry`. No proof link for the present direction was found in the issue/PR.
- https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/Mahler32.lean was read. Flatto–Lagarias–Pollington bounds and Mahler Z-number statements have different quantifiers/conclusions; they are not this theorem.
- https://arxiv.org/abs/2609.19007 (Ralf Stephan, transcendence criteria for the minimal word of rational base 3/2) was read: it concerns a rounded recurrence and a transcendence/automaticity criterion (on three cited axioms), not non-equidistribution of the exact powers. It supplies no matching proof.
- https://raw.githubusercontent.com/openai/math/main/lean/docs/015.md was read: torus-packet equidistribution in prime/quartic/sextic degrees, unrelated to this sequence.
- https://www.theoremdb.org/statements/P2818/ : the three-halves bound for distinct squares in circular words, a naming collision.
- https://aixiv.online/trace/66/view was searched through its stored contents for this theorem and equidistribution: a large source-triage trace listing the open fixed-base theorem and the different multiplier issue/PR, not a proof of this target.
- https://wcook04.github.io/plectis/maths/documents/comparator-1049.html initially redirected through an HTML meta-refresh; followed its raw canonical link to https://wcook04.github.io/practical-formal-verification/maths/documents/comparator-1049.html . It certifies a numerical log inequality for a Lambert-series problem at base 7/2 and explicitly does not settle its own base 3/2 case; not the present target.
- https://prove2.me/theorems/7d760991-9809-4055-8ac1-29d5e77c70c6 : a product inequality, unrelated.

Result: after the above sufficiently varied searches and source/lead checks, no known public complete Lean4 proof of **this negative direction** was found. `public_lean4_proof = false`, status `searched`, is a bounded search result, not a claim that no such proof exists. No public answer was copied into the task or image. No matching public proof was compiled. Search provider's unrelated results were not treated as proof candidates merely because they mention 3/2.
