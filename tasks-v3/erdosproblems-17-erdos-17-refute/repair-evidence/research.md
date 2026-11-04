# Statement and public-proof review (2026-11-04)

Task: `erdosproblems-17-erdos-17-refute`.
Actual target: `Erdos17.formal_conjectures_bench_refutation`, **not** infinitude: `¬ {p : ℕ | Erdos17.IsClusterPrime p}.Infinite`.

## Statement fidelity

Read the complete golden prefix and target (Target.lean lines 29–48), metadata and pinned upstream:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/17.lean
The upstream asks `answer(sorry) ↔ {p | IsClusterPrime p}.Infinite`; the benchmark intentionally selects the **negative** answer. This is not an accidental reversal to repair.

Primary source inspected: Christian Elsholtz, *On cluster primes*, Acta Arith. 109.3 (2003), pp. 281–284:
https://www.math.tugraz.at/~elsholtz/WWW/papers/papers13clusteractarith.pdf
Its introduction defines cluster primes using positive even integers at most p−3 and primes at most p, and describes infinitude as an open question. The Lean predicate uses natural even n and integer subtraction/coercions, not truncated natural subtraction. Its extra n=0 is harmless (choose q₁=q₂=p). Inclusion of p=2 rather than p>2 changes a finite set only. Bounds and witnesses otherwise agree. No obvious definition error forces either answer; the known counting upper bounds do not imply finiteness. Marked consistent, without modifying mathematics.

Direct problem page and /latex/17 returned Cloudflare 403; primary author's paper and pinned upstream were readable. The working report at https://www.erdosproblemaday.com/report/17 independently quotes the live definition and records the unresolved question, finite computations and reductions only.

## Public complete Lean4 proof search

First precisely matched the complete task ID against the skill's `references/public-lean4-proofs.csv`: no row. This alone was not treated as a negative result.

Ran these query groups with web_search:
- `Erdos problem 17 cluster primes finite infinitely Blecksmith Selfridge Elsholtz`
- `"cluster primes" Lean proof`; `"Erdos17" "Lean" proof refutation`
- `site:github.com "IsClusterPrime" "Infinite"`
- `site:github.com "cluster primes" "Lean"`; `"Erdos17.erdos_17" proof`
- `"cluster primes" finite Lean4 Blecksmith Elsholtz`
- `site:github.com/google-deepmind/formal-conjectures/pull "17" "cluster"`
- `site:github.com/leanprover-community/mathlib4 "cluster prime"`
- `"cluster primes" "Lean4" finite proof refuted`
- `"Erdos17" "proof" "sorry" "Finite"`

Sources and candidate exclusions:
- Read pinned and current main `FormalConjectures/ErdosProblems/17.lean` Lean source. Main infinitude still has `sorry`; known bounds likewise have placeholders. The complete 97 least-noncluster theorem is a finite result, not a proof of the negated infinitude target.
- GitHub/Mathlib/PR searches found no complete refutation branch or fork; results mainly point to that upstream statement.
- https://conjectures.io/problems/erdos17-erdos-17?mode=counterexample explicitly displays the negative target, no published proof/refutation, and a submitted-but-unpublished proof. The submission is not public proof evidence.
- Followed its public contribution link via GitHub API and read https://raw.githubusercontent.com/conjectures-io/conjectures-contribution/main/contributions/erdos-17/index.md : Contributions (0). No Lean proof source to validate.
- https://www.erdosproblemaday.com/report/17 : finite calculations/reductions, explicitly not a solution; no complete Lean proof.
- https://www.theoremdb.org/statements/P2972/ : unresolved statement, not proof code.
- Read https://raw.githubusercontent.com/williamjblair/lean-proofs/main/README.md : indexed proofs concern 730,154,94,399,1074, not 17.
- Old search hits in `mehmetmars7/Erdosproblems-llm-hunter` for `attacks/erdos/gpt_5.2/17.tex` and `gpt_pro_5.2/17.tex` returned 404; GitHub fallback confirmed paths absent from current clone. Followed replacement public catalog https://we-solve.github.io/problems/erdos-problem-17-edf8e6f4/ and read all four linked attempt manuscripts (`attempt-{1,2,3,4}/r1/`). They explicitly conclude unresolved, offering finite examples or infinitely many non-cluster primes, which does not establish finitely many cluster primes. They contain no complete Lean4 proof.
- A search hit at https://starks.provably.fast/threads/bt1_564c00dfef850321a5d7fb1b?reply=bp1_5ba246322fb7e480b92b4c7b was fetched: unrelated capacity thread, no cluster-prime/Erdos17 matches.
- Author's paper proves sparsity, not finiteness, and is not Lean code.

Conclusion: after these searches no known public complete Lean4 proof of this task's **negative direction** was found. `public_lean4_proof=false`, status `searched`, means this search result only, not mathematical or absolute proof of absence. No public answer was added and no external proof was compiled into the task.

Web retrieval records: mw1s4qlu41rtrc, mw1s5c8z5by7fi, mw1s5fwejeotuy, mw1s79xbx8urcu, mw1sf432s7sd8g, mw1sfjr6bgm1th, mw1sgdzxthnob8, mw1sheyej724qw.
