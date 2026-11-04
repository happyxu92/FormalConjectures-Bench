# Mathematical statement and public-proof search

Task: `wikipedia-hall-weak-hall-conjecture-refute` (refutation direction only).

## Statement check

Read the complete pinned upstream `FormalConjectures/Wikipedia/Hall.lean` at
`233a10e857ef78e79fd9fe661d37db724089170a`, task metadata, public Target and trusted golden inputs.
Definitions quantify over integers x,y with unequal square/cube; the positive constant may depend on the real exponent, not x,y. The task is exactly
`¬ (∀ ε > 0, Hall.HallConjectureExp (1/2 - ε))`, not Danilov's assertion for `1/2 + δ`.
The real-power base is nonnegative `|x|`. Negative x and x=0 do not give an obvious contradiction; strict versus non-strict bounds are interchangeable by shrinking the positive constant. No demonstrated statement/definition error was found. Being the negation of an open conjecture is intentional in this paired challenge, not itself a mismatch or an impossibility result.

Sources actually read:
- https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/Hall.lean
- https://people.math.harvard.edu/~elkies/hall.html : weak Hall is `|k| > x^(1/2-o(1))`; it is a special case of abc; the table and Danilov family concern bounds at exponent 1/2, not a disproof below it.
- https://arxiv.org/abs/2609.35252 and https://arxiv.org/html/2609.35252v1 : Karsten Mueller, *Weak Hall's conjecture, approximation gains, and continued fractions*, equivalences/conditional abc implication, not an unconditional refutation.
- https://epoch.ai/frontiermath/open-problems/hall-conjecture : finite-record-search challenge, not a disproof of an existential constant.
- Wikipedia direct fetch returned HTTP 403. Search-indexed excerpts were available; author and original paper above supplied the substantive cross-check instead.

No mathematical statement, Target, golden, frozen hash, or GoldenCheck was changed.

## Public complete Lean4 proof search

First exact CSV lookup: full task ID in skill `references/public-lean4-proofs.csv`, no match. This was not used as evidence of nonexistence.

Multiple live web-search groups covered:
1. `Hall conjecture weak form exponent 1/2 epsilon abc conjecture Elkies Danilov`
2. `"weak_hall_conjecture" Lean proof`
3. `"HallConjectureExp" Lean github`
4. `"Hall's conjecture" "Lean" refutation counterexample`
5. `"weak Hall" "Lean4" proof`
6. `site:github.com "HallConjectureExp"`
7. `site:github.com "Hall" "conjecture" "mathlib"`
8. `"Hall.formal_conjectures_bench_refutation"`
9. `"weak_hall_conjecture" disproof Lean github`
10. `"Hall" "x^3" "y^2" "Lean" conjecture proof`
11. `"Hall's conjecture" "Lean 4" Danilov weak refutation`

Sources/candidates followed:
- Current upstream raw Hall.lean and https://firsching.ch/formal-conjectures/src/FormalConjectures/Wikipedia/Hall/ : weak Hall remains a `sorry` statement; no proof link resolving this refutation.
- GitHub PR search, including closed/merged and open PRs: `repo:google-deepmind/formal-conjectures Hall is:pr`, REST API returned 32 items, `incomplete_results=false`. All titles and relevant bodies were inspected (saved in `github-prs.json`). #192 adds the statement. #2491/#2991/#3022/#3031 concern Danilov and explicitly mention placeholder/loophole dependencies. They are not complete proofs of this task.
- PR #7660 links a substantive Danilov Lean proof. Actually read its pinned Lean source at https://raw.githubusercontent.com/danielpuri1901/erdos-lean-formalization/f58f69bace20b89f6c0fc3d47944089a2e8b63f5/Solution.lean . Its final declaration is `type_of% @Hall.danilov`, exponent `1/2 + δ`; it does not refute the below-half weak conjecture. Not compiled here; no answer copied into the task.
- https://raw.githubusercontent.com/Woett/Lean-files/main/Erd%C5%91sHall.lean and google-deepmind/superhuman LEAP README: Erdős/R.R. Hall interlocking-divisor/separable-number results, unrelated to Marshall Hall square/cube conjecture (also literature axioms in the former file).
- Mathlib current `Mathlib/Combinatorics/Hall/Basic.lean` actually read: Hall's marriage theorem, unrelated. Locked local Mathlib searched for `HallConjectureExp|weak_hall_conjecture|Hall.s conjecture`, no match.
- Elkies finite examples and the 2026 continued-fractions paper are neither complete Lean proofs nor disproofs of this task. Search results about weak Hellinger, Hall ratios in graph theory, and Hall marriage were excluded by their different mathematical statements.

Result: `public_lean4_proof=false`, status `searched`: sufficiently broad searches did not find a known public complete Lean4 proof of this exact refutation. This is not an absolute claim that no proof exists. No unresolved promising proof link remained. Wikipedia's direct-fetch limitation is disclosed above; no important candidate Lean source remained inaccessible.
