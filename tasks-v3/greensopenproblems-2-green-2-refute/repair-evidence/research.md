# Statement and public-proof review

Task: `greensopenproblems-2-green-2-refute`. Review performed 2026-11-04.

## Actual direction and definitions (check 5)

Pinned upstream read in full:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/GreensOpenProblems/2.lean

Author's source read: https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf, Problem 2, printed pp. 3–4. It asks for a subset of size (log n)^100 whose restricted pair-sums avoid A; the comment gives Sanders' lower bound with exponent 1+c, not a resolution for exponent 100.

The preserved task is the **negation** of the upstream question's eventual lower bound, not its affirmative direction and not `¬(answer(...) ↔ ...)`. Classically it asks for arbitrarily large cardinalities n with a counterexample finite integer set A. One small exceptional n would not prove it.

`Target.lean:47–49` maximizes `Finset.card` over subsets of A with `Disjoint S.restrictedSumset A`; the family includes the empty subset and is finite. The dependency's `Finset.restrictedSumset` is exactly `S.offDiag.image (fun p => p.1 + p.2)`, so equal summands are excluded as in Green's definition. `Target.lean:58–65` has natural n, integer sets, real natural logarithm, exponent 100 and `∀ᶠ ... atTop`. Integer cardinality compared with a real threshold correctly expresses 'at least' that size. Eventual quantification intentionally avoids small-n size issues. No concrete counterexample or definition error making this refutation impossible was found; an open question alone is not evidence of an invalid statement. Marked `statement_status = consistent`; no mathematical files were changed.

## Exact local lookup (check 6)

Read `skills/lean-task-repair/references/public-lean4-proofs.csv`, exactly matching the complete task column. No hit; see `public-csv.json`.

## Web searches

Varied searches included:

- `"Green2" "green_2" Lean proof`
- `"maxRestrictedSumAvoidingSubsetSize"`
- `"Erdős–Moser" "Lean" sum free`
- `"Green problem 2" "Lean4"`
- `"sum-avoiding subsets" "Lean"`
- `"Sanders" "Moser" "Lean4"`
- `"Green2" "refutation" Lean`
- `"green_2" proof site:github.com`
- `"Erdos Moser" "log" "100" counterexample`
- `"GreensOpenProblems/2.lean" proof`
- `"maxRestrictedSumAvoidingSubsetSize" Lean proof github`
- `"restrictedSumset" "log" "Lean" Green`
- `"Ben Green" "problem 2" Lean proof counterexample`
- `site:github.com/google-deepmind/formal-conjectures "Green" "2" "sum" "pull"`
- `site:github.com "Green2" "green_2" "by"`
- `site:github.com "sum-avoiding" "lean" -Cardinality`
- `"Ben Green" "sum" "refutation" Lean 2`
- `"formal-conjectures" "1546" "Green"`
- `"sum-avoiding" "Lean 4" counterexample`
- `"Green2.formal_conjectures_bench_refutation"`

Stored web tool result IDs: `mw1tt6dm43sndh`, `mw1tuja5iori49`, `mw1tv94wfqqt6z`, `mw1twwlas1bnl4`, `mw1tzuo35sh8kg`. Fetch records: `mw1trx9jeoo5d9`, `mw1ttecvbegowj`, `mw1tvh51h4r35p`, `mw1txbfgbsb98q`.

## Sources and candidate exclusions

1. Current upstream main was actually read: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/GreensOpenProblems/2.lean . Main `green_2` still has `sorry`; the known-bounds variants also have `sorry`. None supplies a refutation.
2. https://conjectures.io/problems/green2-green-2 was read. It is a withdrawn catalog entry, not a refutation, and its displayed target contains `sorry`. Its displayed proposition is affirmative, so even an affirmative proof would not establish this task's direction.
3. Followed the contribution repository, including both-direction task links. https://github.com/conjectures-io/conjectures-contribution/tree/main/contributions/green-2 was cloned by the fetch tool and its `index.md` actually read: `Contributions (0)`, `None yet`, with links to both counterexample and formalized bundles.
4. https://aixiv.online/trace/66/view was fetched and searched. Matches are listings of the known bounds for Green 2, not a completed proof or refutation.
5. Pinned Mathlib source searched for `Green2|green_2|maxRestrictedSumAvoidingSubsetSize|sum.avoiding`; no match (exit 1, not a path error). See `mathlib-search.log`.
6. https://raw.githubusercontent.com/rjwalters/lean-genius/main/proofs/Proofs/Erdos476Problem.lean was read. This is the Erdős–Heilbronn finite-field restricted-sumset lower bound, not an avoiding subset bound over integers. Its main result also relies on the task-specific `axiom erdos_heilbronn_bound`. Excluded on both statement and axiom grounds.
7. https://github.com/lyfar/erdos-moser-distinct-subset-sums-lean/blob/main/README.md was read. Its finite distinct-subset-sums inequality is a different Erdős–Moser problem, not this asymptotic restricted-sum-avoidance question.
8. https://www.trureturing.org/research/oeis-a367400-cardinality-sum-avoiding-subsets/ was read: it counts subsets of [n] with no pair summing to the subset's own cardinality, and proves a rational generating-function identity. That does not cover Green 2 in either direction.
9. https://www.trureturing.org/research/bhanja-2025-restricted-sumset-question/ was read: it compares minima of h-fold sumsets with at most r distinct summands, refuted in elementary 2-groups. Different domain, restriction and target. Followed both sites' pinned Lean anchors; both raw URLs returned 404. Their precisely stated claims already exclude them as matches; neither is an unverified claim of a Green-2 proof.
10. https://tecunningham.github.io/ai-discovery-data/math-green.html was read; it summarizes Green's source and does not report a proof of Problem 2.
11. Broad GitHub PR/issue search returned #895 (Green 8) and #1546 (Green 7), unrelated problems. Fetching #1546 hit the GitHub API rate limit; a follow-up title search established it concerns #7, not a matching proof claim.

No matching complete, standard-axiom-only Lean4 refutation was located after this bounded multi-source search. Metadata records `public_lean4_proof=false`, status `searched`: this means no known proof found in the reviewed scope, **not** a proof of nonexistence. Access limitations were the unrelated pinned-anchor 404s and unrelated issue API rate limit; no pending lead claiming the actual target was found. No public proof was inserted into the task or image.
