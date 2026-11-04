# Statement and public-proof review — erdosproblems-41-erdos-41-prove

Review date: 2026-11-04. This review concerns **the positive direction of the retained finite-subset version**, not the paired refutation, pairwise variant, or a newly corrected upstream statement. No mathematical input was changed and no public proof was bundled.

## Statement review (step 5)

- Pinned source: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/41.lean (read in full). Target lines 30–59 preserve its `NtupleCondition` and positive triple-sum declaration, apart from task packaging/attributes.
- Author source actually read: Paul Erdős, *Some of My Favourite Problems in Number Theory, Combinatorics, and Geometry*, section I.6, pp. 4–5: https://www.ime.usp.br/~yoshi/resenhas/abstracts/Erdos.pdf . It asks whether distinct triple sums imply `limsup a_n/n^3 = infinity`; the counting-function formulation is `liminf A(N)/N^(1/3)=0`. The pairwise result is a separate known result.
- https://www.erdosproblems.com/41 was searched; direct page fetch (www and non-www) returned HTTP 403. Its indexed text and the author paper agree on the triple-sum question. https://www.erdosproblemaday.com/day/41-b3-density was also read as a secondary explanation, not as proof evidence.
- Full definitions checked: arbitrary natural-number set; three-element **Finsets** on both sides, subset membership, both cardinalities 3, sum equality implies equality of subsets; infinitude; `Set.Icc 1 N`; finite intersection so `ncard` is the intended count; real division and real exponent `1/3`; natural index atTop. N=0 and possible membership of 0 only affect a finite initial segment. No evident contradiction/counterexample or missing domain/positivity condition was found.
- Important variant distinction: Finsets forbid repeated summands. Current upstream uses Multisets, preserving repetitions. Read current source https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/41.lean and merged PR https://github.com/google-deepmind/formal-conjectures/pull/5241.diff plus its API description. The PR explicitly explains this distinction; it does not prove either theorem. The retained task is a stronger finite-subset version, not literally the standard multiplicity-based B3 hypothesis. This difference alone is not a demonstrated false statement, under this repair's reasonable-variant policy. Marked `consistent` meaning no obvious impossibility found, not exact equivalence with the original question or proof of validity. Definitions/Target/Spec were not corrected to Multiset.

## Public complete Lean4 proof search (step 6)

First exact lookup in `skills/lean-task-repair/references/public-lean4-proofs.csv`, task column `erdosproblems-41-erdos-41-prove`: **no rows**.

Actual keyword groups searched (multiple web-search batches):

1. `"Erdos41.erdos_41" Lean proof`; `"Erdos" "41" "Lean4" triple sums proof`; `"erdos_41" "NtupleCondition" proof`.
2. `"Erdos 41" Lean proof GitHub`; `"B3" "liminf" "Lean"`; `site:github.com "NtupleCondition" "41"`; `site:github.com/google-deepmind/formal-conjectures/pull "41" triple`.
3. `"Sidon" "triple" "Lean" proof`; `"Erdős 41" "proof" "Lean" -site:conjectures.io`; `"B_3" "liminf" formal proof Lean`; `"Erdos41" -site:conjectures.io -site:github.com/google-deepmind/formal-conjectures`.
4. `"zhenningdavidliu" "41" Lean`; `"Erdős problem 41" "Lean" proof fork`; `site:github.com "erdos_41" -repo:google-deepmind/formal-conjectures`; `"triple sums" "liminf" "formal" proof`.

Sources/lines followed and exclusions:

- Pinned and current upstream Lean source read in full. Both main declarations end in `sorry`; neither proves the task. Current source also has a different (Multiset) hypothesis. The separately labelled pairwise statement does not cover the triple direction.
- GitHub issue/PR search: https://api.github.com/search/issues?q=repo%3Agoogle-deepmind%2Fformal-conjectures+%22NtupleCondition%22 returned exactly #615 (original formalization) and #5241 (multiplicity correction). Both diffs read: https://github.com/google-deepmind/formal-conjectures/pull/615.diff and /pull/5241.diff . They retain `sorry`, no full proof or proof branch identified. Search hit issue #3458 could not be fetched through the GitHub API due to rate limit; no search result identified it as a #41 proof. This incidental rate limit does not conceal an identified proof lead.
- Conjectures.io https://conjectures.io/problems/erdos41-erdos-41?mode=proof read: no contributions/attempts. Followed source repository directory https://github.com/conjectures-io/conjectures-contribution/tree/main/contributions/erdos-41 . Its actual `index.md` records `Contributions (0)`, no Lean proof. Direction of page labels was not used to infer the positive task's status.
- TheoremDB https://theoremdb.org/statements/erdos-problem-41/ and /statements/P2994/ read, and Firsching/upstream documentation searched: statement/open-problem mirrors, no complete proof.
- Relevant actual Lean source read: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjecturesForMathlib/Combinatorics/Basic.lean . Contains Sidon insertion/greedy infrastructure, not a triple-sum liminf theorem (no `liminf` or `NtupleCondition`). Pinned Mathlib and FormalConjecturesForMathlib searched in the acceptance container for `NtupleCondition|Sidon.*liminf|liminf.*Sidon`: no matches (exit 1, no path errors). Generic Mathlib liminf docs are API, not a proof.
- arXiv:2605.03274 (David Barros Hulak, *Formalizing Singer Sidon Constructions and Sidon Set Infrastructure in Lean 4*) read: formalizes finite Singer constructions and Problem 30 bounds/conditional reductions, not this infinite B3 liminf claim.
- arXiv:2601.07421 read: *Resolution of Erdős Problem #728*, unrelated target. arXiv:2605.02064: multiplicative Sidon gaps, unrelated. Other returned adjacent problem numbers (401, 411, 541, 647) do not state this target.
- Even-summand/B2 results and conditional B3 discussions do not provide the retained unconditional three-element Finset theorem. No plausible remaining link claimed a complete Lean4 proof of this direction.

Result: **searched / no known complete public Lean4 proof found**, not a claim of absolute nonexistence. No external proof was compiled because none covering this target was located. Access limits: original problem webpage and ScienceDirect HTTP 403; one unrelated GitHub issue API rate limit; one alternative author-paper URL failed but the author paper above was successfully read. None was an identified inaccessible Lean proof candidate. Web retrieval result IDs: mw1tp5vt8d51ti, mw1tpohmgacnnf, mw1tqdp3fer047, mw1tqrsuvztobu, mw1triqhgyxjh2, mw1tsd5ip6ionq, mw1tsux5ic7koe, mw1ttpdxw19ed3, mw1tu0h0b9j6jv.
