# Public-proof search and statement check (2026-11-04)

Task: `greensopenproblems-26-open-refute`. Exact CSV lookup in
`skills/lean-task-repair/references/public-lean4-proofs.csv`, column `task`: no rows.
This is **the negation** of the all-prime additive basis conjecture, not the
positive p=3 theorem and not its four-cube variant. No answer was imported.

## Statement/source check

Read pinned upstream:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/GreensOpenProblems/26.lean
and current upstream:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/GreensOpenProblems/26.lean

Read Green's original problem and comments (Problem 26, PDF pp.15–16):
https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf
Green distinguishes the solved p=3 problem from the open general-prime problem.
Read Yang Yu, https://arxiv.org/html/2510.01300v2 (Conjecture 1 and Theorem 3).
Conjecture 1 quantifies over each prime p, a constant c(p), all dimensions, and
all families of c(p) bases. A cube is precisely the set of 0/1 subset sums of a
basis, hence the Minkowski sum of cubes matches the multiset-union formulation.
Yu's positive result is only for p=3. The task deliberately asks for the formal
negation of the general-prime assertion. There is no obvious definition error
or contradiction forced by the sources. The dimensions n=0, p=2, and C=0 do not
by themselves refute the existential all-dimension statement. No mathematical
input, golden file, public Target, or frozen hash was changed.

## Search groups actually submitted

- `"additive basis conjecture" "Lean" proof`
- `"Green26" "formal_conjectures_bench_refutation"`
- `"green_26.variants.open" proof Lean`
- `"additive basis conjecture" counterexample prime fields`
- `site:github.com "Green26" "IsCube"`
- `site:github.com "additive basis" "lean"`
- `site:github.com/google-deepmind/formal-conjectures "26" "basis"`
- `Yang Yu additive basis conjecture formalization Lean4 refutation counterexample`
- `"Jaeger" "Linial" "Payan" "Lean"`
- `"GreensOpenProblems/26.lean" proof fork`
- `"Green26" "proof" Lean -squares -packing`
- `"additive bases of vector spaces" "Lean4"`
- `site:github.com "green_26" "refutation"`

Searches cover the exact declaration, aliases, equivalent mathematics, authors,
GitHub, FormalConjectures, Mathlib documentation and related formalizations.

## Leads followed / rejected

- Both pinned/current upstream Lean sources were read: all relevant theorem
  proofs still use `sorry`; neither gives the negative all-prime result.
- GitHub PR search was read:
  https://github.com/google-deepmind/formal-conjectures/pulls?q=is%3Apr+%22Green%22+%2226%22
  It returned two apparently promising formally-solved claims, PRs 2467/2999.
  Their complete public `.diff` files were fetched using curl and read:
  https://github.com/google-deepmind/formal-conjectures/pull/2467.diff
  https://github.com/google-deepmind/formal-conjectures/pull/2999.diff
  Both only change metadata of `green_26`, `yu25`, and `alm91`; the bodies retain
  `sorry`. They do not prove this task or even provide complete Lean proofs of
  the positive variants. No proof branch/fork link occurs in those diffs.
- https://aixiv.online/trace/66/view was fetched and searched for Green26, the
  exact target, and additive basis. It reproduces problem statements/literature,
  not a complete proof of this target. Square-packing matches are unrelated.
- https://conjectures.io/results/af89c6c1-a843-4e5d-a9ad-1716430cc1e2
  was fetched: it is Green Problem 3, not 26.
- Mathlib basis/vector-space documentation is about linear bases, not the
  all-prime cube covering refutation; integer additive-basis formalizations
  (Erdős 35/870/868/881) are different domains/statements.
- Yu's manuscript gives a positive p=3 result in ordinary mathematics, not a
  Lean4 refutation of the general conjecture. Weak/generalized additive basis
  papers found by search likewise do not supply this target.

## Access limitations and conclusion

GitHub's API-backed PR fetch returned HTTP 403/rate limits. The public PR search
and complete `.diff` endpoints worked, so both promising claims were inspected
without that API. ArXiv v3 returned 404; v2 worked and was read. One ALM PDF fetch
failed; its claimed result is also stated in the accessible primary Green/Yu
sources and was not a Lean-proof lead. GitHub code search requires login and
was supplemented with varied public indexed queries, raw upstream source and
PR diffs. No unresolved promising proof link remains from these results.

Result: `public_lean4_proof=false`, status `searched`: after the searches above,
no known public complete Lean4 proof of this **negative** all-prime target was
found. This is not an assertion that no such proof can exist, and no public
proof was compiled in this task environment.
