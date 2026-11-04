# Statement and public-proof audit (2026-11-04)

Task: `erdosproblems-41-erdos-41-refute`. Only this direction and the retained definitions were assessed. No proof was added.

## 5. Retained statement

Read all of `tests/golden_env/FormalConjecturesBench/Target.lean`, including `Erdos41.NtupleCondition`, and the pinned upstream source:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/41.lean

The target is the negation of the universal triple-sum assertion for infinite subsets of Nat, with real-valued liminf of `ncard (A ∩ Icc 1 N) / N^(1/3)`. It is NOT the pairwise solved variant and is NOT a proof of the positive conjecture. The extra quantified Type/AddCommMonoid instance is unused; its domain has inhabitants (e.g. Nat), so it does not make the assertion vacuous.

The pinned `NtupleCondition` uses Finsets: sums of three distinct elements, not repetitions. Current upstream uses Multisets after PR https://github.com/google-deepmind/formal-conjectures/pull/5241 (read the PR body and full diff). E.g. `1+1+3 = 1+2+2` cannot be represented by the old predicate. This is a distinct-summand variant, not by itself evidence that this refutation is impossible. The task faithfully negates its pinned upstream statement. No concrete contradiction, counterexample to the task, interval/domain/normalization error, or definition making the goal impossible was found. Status `consistent` means this limited assessment, not that the refutation is known true. Definitions and statements were not changed.

Sources read:
- https://www.erdosproblems.com/41 and /history/41: direct fetch HTTP 403; indexed primary-source results recover the triple-sum/liminf statement and open status.
- https://github.com/teorth/erdosproblems : independently cloned the community source data at `c443d8c7d726d633a0284ffaf75b76240b48adf5`; `data/problems.yaml` lines 661–675 marks #41 open, formal_status unformalized.
- Christian Táfula, *Infinite Sidon-type sets for zero-sum linear forms*, https://arxiv.org/html/2607.20753 , Introduction: corresponding infinite Bh problem for odd h remains open. Read the relevant introduction and conclusions. This is context for the classical repeated-summand problem, not a proof of the present distinct-summand refutation.

## 6. Public complete Lean4 proof search

Exact CSV lookup: Python csv.DictReader of skill `references/public-lean4-proofs.csv`, `task == 'erdosproblems-41-erdos-41-refute'`: zero rows.

Multiple web-search groups actually executed:
- `Erdos problem 41 B3 distinct triple sums liminf disproof`
- `"erdos 41" "Lean"`, `"Erdos41" Lean proof`
- `"Erdos41" "formal_conjectures_bench_refutation"`
- `"Erdős" "41" "Lean" "counterexample"`, `"B3" "liminf" "Lean"`
- `site:github.com "erdos_41" proof`
- `site:erdosproblems.com/41 "infinite" "triple"`
- `site:github.com "NtupleCondition" "sorry"`
- `"Erdos 41" "Lean4" proof refutation`, `"B_3" "Lean" "Sidon"`
- `"Erdos41" "Finset" Lean proof`
- `"Erdős" "41" "Lean" github proof fork`
- `"NtupleCondition" refutation Lean`
- `"Christian Táfula" "Lean" "41"`

Sources and candidate exclusions:
1. Pinned and current raw FormalConjectures `ErdosProblems/41.lean` read completely. Main theorem is `sorry`, pairwise variant is also `sorry`; neither is this refutation. Current Multiset definition does not silently replace the task's Finset definition.
2. GitHub API issue/PR search `repo:google-deepmind/formal-conjectures NtupleCondition` returned #615 (original statement) and #5241 (multiplicity repair). Read both diffs; they leave theorem proofs as `sorry`. Neither proves the negative direction.
3. https://conjectures.io/problems/erdos41-erdos-41?mode=counterexample read fully, including actual `Challenge.lean` displayed there: placeholder `sorry`, no attempts/contributions. Followed its contribution-repository link by a separate successful sparse git clone of https://github.com/conjectures-io/conjectures-contribution at `a4a026e7f77ce991d0bdd1fd33e3a206d39106a3`. `contributions/erdos-41/index.md` says Contributions (0); full git tree has no proof for #41.
4. Mathlib pinned source locally searched for `NtupleCondition|erdos_41`: no matches. Source-search and problem-name searches found no Mathlib proof covering the target.
5. https://erdosproblemaday.com/day/41-b3-density read: expressly partial, classical parity obstruction and conditional smooth-gap result; no Lean solution and no refutation. The cited primary paper above also leaves odd h open. Author-page lookup gave no Lean-related result.
6. https://github.com/Jayyhk/erdos-lean catalog inspected (301 proofs); no #41 entry or matching proof. Search did not identify an effective #41 proof fork/branch.
7. arXiv:2601.07421 was inspected and is about #728, not #41. Sidon counterexample results for #707, references to #541/#441/#915, and proofs for other problem numbers were excluded rather than treated as this target's proof.

Access limits: primary erdosproblems website direct HTTP 403, some unauthenticated GitHub API endpoints rate-limited. Recovered the important contribution listing via git clone, upstream code/PR changes via raw/diff, and source status via teorth's git data and primary arXiv. No remaining identified promising proof link is pending verification. Result: `public_lean4_proof=false`, status `searched`: after the above search no known public complete Lean4 proof of this retained negative target was found. This does not prove nonexistence. No external proof was compiled in this task environment or placed in the image.
