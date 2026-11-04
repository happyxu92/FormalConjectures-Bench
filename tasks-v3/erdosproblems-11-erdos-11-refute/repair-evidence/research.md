# Statement and public-proof review (2026-11-04)

Task: `erdosproblems-11-erdos-11-refute`, not its positive partner.

## Actual statement

`environment/data/FormalConjecturesBench/Target.lean:29–44` negates the universal statement that every odd natural n > 1 is k + 2^l with natural squarefree k and natural l. There are no task-local mathematical prefix definitions. `Odd`, `Squarefree`, arithmetic and quantifiers have their standard imported meanings.

Read the pinned upstream file:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/11.lean

Its `Erdos11.erdos_11` is exactly the positive universally quantified statement negated here. Hercher, *On the Sum of Squarefree Integers and a Power of Two*, Conjecture 1, states the same all-odd-n>1 conjecture and reports finite verification through 2^50, not a general proof or disproof:
https://arxiv.org/html/2411.01964

Granville–Soundararajan (1998), original paper retrieved (PDF text extraction has broken font encoding):
https://dms.umontreal.ca/~andrew/PDF/wieferich.pdf

The modern upstream `main` file now calls the all-odd formulation `erdos_11.variants.all_odd`, whereas `erdos_11` asks only about sufficiently large odd n. PR #6650 explains this rename/scope distinction. A single exceptional odd n would refute this task's pinned all-odd formulation; it would not refute the modern eventual formulation. This is an intentional paired refutation challenge, not evidence of an erroneous or impossible statement. No obvious definition/quantifier error found. The upstream Granville–Soundararajan variant had an unrelated Wieferich-sign error corrected by #5817; that variant is not included in this Target.

https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/11.lean
https://github.com/google-deepmind/formal-conjectures/pull/6650
https://github.com/google-deepmind/formal-conjectures/pull/5817

Direct fetches of erdosproblems.com/11, /latex/11 and /history/11 returned HTTP 403. The pinned upstream and full Hercher paper were accessible and sufficient to check this task's formulation. No mathematical input was changed.

## Public complete Lean4 refutation search

Exact CSV lookup of the complete task ID in the skill's `references/public-lean4-proofs.csv` returned no rows (`/tmp/erdos11-refute-csv-match.json`). Then performed multiple independent web searches, followed actual links and read candidate Lean sources. Searches included:

- `Erdos11 erdos_11 Lean proof`
- `Erdős 11 Lean squarefree refutation`
- `squarefree power of two Lean`
- `Erdos11 Lean counterexample Squarefree github`
- `erdos_11 site:github.com proof`
- `Granville Soundararajan Lean squarefree`
- `Erdos problem 11 Lean4 disproof`
- `erdos_11.variants.all_odd proof counterexample`
- `formal_conjectures_bench_refutation Erdos11`
- `squarefree 2 ^ l ¬ Erdos Lean`
- `Erdos 11 refutation Lean GitHub`

Sources/candidate exclusions:

1. Current upstream file: both eventual and all-odd main claims still `sorry`; no refutation. Read full file. GitHub commits API for `FormalConjectures/ErdosProblems/11.lean` and issue/PR search for `erdos_11` also checked. History and search saved in `/tmp/erdos11-refute-history.json` and `/tmp/erdos11-refute-pr-search.json`.
2. PRs #2811 and #3327 advertise solved variants, but actual head Lean files still contain `sorry` in every research theorem. They merely change category attributes and do not refute the all-odd conjecture. Read both full files from head commits 864b727f0acaf72f09d6d2d59b6effa1a0b0d9bd and b30b4922b5d5736a5ca297c33823d4bd1cf28788. Saved only under `/tmp/erdos11-refute-pr*.lean`.
3. https://conjectures.io/problems/erdos11-erdos-11?mode=counterexample explicitly has the same negated all-odd target and says no full proof/refutation attempt. Followed its one contribution and read all of `script.lean`: witness elimination, conditional reductions, and a finite bound 1024; not a refutation. Some theorems assume the original conjecture. Source:
https://raw.githubusercontent.com/conjectures-io/conjectures-contribution/main/contributions/erdos-11/9912bf43713402fa030c83358b48a3fe22041358846f121c30389f4e1775d74a/script.lean
4. https://github.com/google-deepmind/alphaproof-nexus-results — read README, successful-output tree and attempted-problem list. Erdős 11 appears in attempted problems, not successful proofs. Searched the cloned repository for its theorem and mathematical shape.
5. Mathlib `Mathlib/Data/Nat/Squarefree.lean` and generated documentation inspected; squarefreeness API, not a refutation of this conjecture.
6. Search found a purported Aristotle/GPT claim. Followed https://discoveria.ai/entry/erdos-11-aristotle-gpt-1a to the primary https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems . The primary table marks problem 11 `Incorrect claim made`; it supplies no complete accepted Lean refutation. Not counted as proof.
7. https://github.com/Jayyhk/erdos-lean — read catalog and searched actual cloned Lean tree for exact `Erdos11`, `erdos_11` and the squarefree-add-power statement. No matching problem/statement; broad matches were other numbered problems and products of powers, not this target.
8. https://www.erdosproblemaday.com/problem/11 still describes the problem as open. Hercher's paper supplies computation/heuristics, not a complete Lean4 proof in either direction.

Result: after the above searches and candidate exclusions, no known public complete Lean4 proof of THIS REFUTATION was found. Metadata `public_lean4_proof=false`, status `searched` means this search result, not a proof of universal nonexistence. No public proof was copied into the task, and no candidate was counted based on a positive-direction result or a partial lemma. No external proof was compiled in this task environment.

Web tool result IDs: mw1ree2g6rzprl, mw1rf14bwknppy, mw1rf941udsu0r, mw1rftegwaok3s, mw1ri13gvt5o7c, mw1ri8izrywrp7, mw1riitiyzaab0, mw1rp7t2o8ji0c, mw1rpgkq4m6p5i.
