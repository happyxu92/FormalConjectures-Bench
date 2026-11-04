# Mathematical statement and public-proof review (2026-11-04)

Task: `erdosproblems-126-erdos-126-refute`; this review is of the NEGATION, not the paired affirmative task. No proof source was placed in the task or image.

## Statement

Read task.toml, the entire public Target prefix and theorem, and the pinned upstream:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/126.lean

The upstream question is P := for every f satisfying IsMaximalAddFactorsCard, f(n)/log n tends to infinity. Target lines 44-50 require not P. The extremal definition is the greatest uniform lower bound for the number of distinct prime factors of the ordered off-diagonal product. Ordered pairs duplicate factors but not distinct prime support. Distinct natural entries have positive off-diagonal sums, even when 0 is present. Small n and log(0), log(1) do not affect the atTop limit. No defect in these definitions was identified.

Current upstream explicitly says the answer is yes and cites an affirmative formal proof:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/126.lean
https://github.com/tadamcz/erdos126/blob/2516785fe6bbc43e979cf6029c976d9f998a7fba/Erdos126/Resolutions/Erdos126_132usd_25h.lean#L3053

Read the author repository README, Solution.lean, exact definition (lines 13-18) and final theorem/proof (3053-3056), and the independent extremal-definition checks. The definition and affirmative limit are exactly the ones negated here. The primary resolution source contains no sorry/admit/axiom declarations in a local source scan. Author repository inspected at HEAD 158bfe26a3c13309613fe997f6f622f4ef3a5c17; the upstream-linked pinned source was also fetched. Its declared result is P, not not P. Thus the retained refutation contradicts this published result (P together with Target's not P yields False). Marked statement_status=mismatch ONLY; no mathematical repair, proof substitution, or re-generation of Spec on this basis. Published proof not compiled in this task environment.

The maintained source database independently records #126 as proved (Lean), formal update 2026-09-03:
https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml

Source-page limitations: erdosproblems.com/126 and its non-www form returned Cloudflare/403; the 1934 Erdős–Turán PDF at https://combinatorica.hu/~p_erdos/1934-03.pdf failed retrieval. These access limits do not leave an unexamined proof lead: current upstream, the linked author Lean source and the maintained database were accessible. TheoremDB's July 2026 open-status packet is older than the September affirmative result and was not treated as current.

## Public proof search: exact current direction

First exact CSV lookup: `/root/FormalConjectures-Bench/skills/lean-task-repair/references/public-lean4-proofs.csv`, task column equals the complete ID above: zero matches. No inference of absence was made from that lookup alone.

Web query groups actually run:
- `Erdos problem 126 f(n) prime factors sums Turan`
- `"erdosproblems.com/126" "log"`
- `"Erdos126.formal_conjectures_bench_refutation" Lean`
- `"erdos_126" "disproof" Lean`
- `"Erdos 126" Lean refutation counterexample`
- `site:github.com "IsMaximalAddFactorsCard" "sorry"`
- `site:github.com "IsMaximalAddFactorsCard" "disproof"`
- `site:github.com/leanprover-community/mathlib4 "erdos" "126"`
- `"Erdos 126" Lean "Adamczewski" proof Turan`

Read/followed sources:
- Pinned and current FormalConjectures files (URLs above): pinned file has sorry placeholders; current formal_proof link is affirmative only.
- https://github.com/tadamcz/erdos126 : four resolutions and Solution wrapper are advertised and implemented as affirmative proofs; not proofs of this negation. Reviewed exact final declaration and the matching extremal definition, not just repository title.
- https://github.com/epoch-research/LeanOpenProblems-results : the accepted Erdős126 entries are explicitly listed as proof, unlike other tasks explicitly listed disproof. This corroborates direction, not a claim that benchmark disproof stubs are proofs.
- https://raw.githubusercontent.com/epoch-research/LeanOpenProblems/77882c437ca1dfefab3b27fa00f1d29788100311/apn/data/erdos/Isolated/Erdos126.erdos_126.lean : fetched actual Lean source; the `.disproof : ¬ (type_of% @Erdos126.erdos_126)` declaration is `:= sorry`, so excluded.
- https://conjectures.io/problems/erdos126-erdos-126 and https://theoremdb.org/statements/P3040/ : problem/catalogue context, not complete proofs of the negation.
- https://erdosproblems.ai/wiki/problems/arithmetic_functions/E0126/claims/2026_09_03_adamczewski : affirmative square-root bound and author-repository link, not this direction.
- Mathlib-targeted and GitHub alias queries returned no complete negative proof; other number-theory tasks and intermediate counterexamples in failed proof attempts do not prove not P.

Conclusion: after multiple searches across upstream, Mathlib, author sources and benchmark results, no known public complete Lean4 proof of THIS NEGATED TARGET was found. public_lean4_proof=false, status=searched; not a universal nonexistence claim. The publicly available complete affirmative proof was deliberately NOT counted for this task.
