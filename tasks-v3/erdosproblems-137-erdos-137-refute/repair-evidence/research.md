# Mathematical statement and public-proof research

Task: `erdosproblems-137-erdos-137-refute` (only this direction).

## Statement

Read pinned source:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/137.lean

The pinned universal non-powerfulness proposition is formally negated by this task. Classically the task asks for some k >= 3 and n : Nat whose product over Ioc n (n+k) is powerful. The integers in that interval are positive, including when n=0. The full prefix contains no local mathematical definitions. `Nat.Powerful` is `Nat.Full 2`, where Full quantifies over prime factors; the product here is positive, so the convention for zero causes no defect. No obvious impossible-statement/definition error was found. This is the counterexample direction of an open problem, not a claimed proof of universal non-powerfulness.

Definition source read:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjecturesForMathlib/Data/Nat/Full.lean

Sources cross-checked:
- https://github.com/google-deepmind/formal-conjectures/issues/372 (open problem description; issue was closed for adding the conjecture, not solving it)
- https://www.theoremdb.org/records/R1198/ (reported open; full statement)
- https://raw.githubusercontent.com/google-deepmind/formal-conjectures/master/FormalConjectures/ErdosProblems/137.lean (now states the existential direction directly; still `sorry`)
- https://firsching.ch/formal-conjectures/src/FormalConjectures/ErdosProblems/%C2%AB137%C2%BB/ (open declaration and placeholder proofs)
- https://www.erdosproblems.com/137 and its forum thread: direct fetch returned HTTP 403. Its problem text is reproduced by upstream issue 372.

## Public Lean4 proof

First used Python csv.DictReader to match the full task ID against the skill's references/public-lean4-proofs.csv: no match. This was not treated as a negative proof result.

Search groups actually run:
1. `Erdos problem 137 powerful consecutive integers squareful conjecture`; `"Erdos137" "Lean" proof`; `"erdos_137" proof Lean4 powerful`.
2. `"Erdos" "137" "counterexample" "Lean"`; `"formal_conjectures_bench_refutation" "Erdos137"`; `site:github.com "erdos_137" "by"`; `"powerful" "consecutive" "Lean4" refutation`.
3. `"Erdős 137" "Lean" proof github forks`; `"Scott D. Hughes" "137" counterexample`; `site:github.com/leanprover-community/mathlib4 "Powerful" consecutive`; `"Erdos137" "refutation" proof`.

Candidate sources followed:
- https://github.com/scottdhughes/erdos137 : fetched repository and read actual `Erdos137/Finiteness.lean`, especially definitions RadLB, Powerful and statements/proofs `erdos137_eventually_not_powerful` and `erdos137_finite` (lines 122-251). The final theorems assume an explicit radical-bound hypothesis and prove per-k finiteness/eventual non-powerfulness. Neither supplies a powerful-product witness, so these are NOT full proofs of this task, even if internally sorry-free. README's other modules also describe conditional bounds and elementary obstruction lemmas.
- Pinned and current FormalConjectures source plus Firsching rendered Lean: placeholders, not proofs.
- https://gist.github.com/declangessel/d8e15e5ff1b6c7e99e3d86d7c66f1d08 : fetched; title/content concern Erdős 488, not 137.
- https://www.theoremdb.org/records/R1198/ : fetched; records an unresolved statement, no executable proof.
- https://raw.githubusercontent.com/AxiomMath/erdos-public/main/README.md : fetched proof listing; no relevant 137 refutation located.
- Consecutive powerful pair (12167,12168) search hits concern k=2 and a different problem; k>=3 here is essential. Likewise finite verification of no three individually powerful numbers is neither a witness nor the same product predicate.

Limits: erdos.constellate.science/finding.html?n=137 failed DNS resolution. Final GitHub API requests for Hughes branches/forks and issue 372's closing PR timeline returned rate-limit HTTP 403. The award issue fetch also hit API rate limits. Therefore branch/PR follow-up cannot honestly be called exhaustive. Result is `unknown`/`blocked`, NOT false and NOT a claim that no public proof exists. No public answer was installed or compiled.
