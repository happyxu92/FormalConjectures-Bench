# Statement and public-proof review (2026-11-04)

Task: `books-uniformdistributionofsequences-equidistribution-isequidistributedmoduloone-three-halves-pow-prove`.
Target: positive equidistribution of `(3/2 : ℝ)^n`, **not** its negation, not `n^(3/2)`, not all transcendental multipliers, and not merely existence/infinitude of accumulation points.

## Statement fidelity

Read the complete golden prefix and target and the pinned upstream file:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Books/UniformDistributionOfSequences/Equidistribution.lean
(web result `mw1qyzw9dr9ns1`, full upstream text read).

Read the actual cited book, Kuipers and Niederreiter, *Uniform Distribution of Sequences*, Chapter 1, Corollary 4.2 and following paragraph, printed pp.35–36 (PDF p.52):
https://web.maths.unsw.edu.au/~josefdick/preprints/KuipersNied_book.pdf
(`mw1r3ic1e9pmua`, index 2). It explicitly says it is not known whether sequences `(e^n)`, `(π^n)`, or even `((3/2)^n)` are uniformly distributed modulo one. The publisher listing was also read: https://store.doverpublications.com/products/9780486149998 .

Read Neeley, Taylor-Rodriguez, Veerman and Roth, *On the Uniformity of (3/2)^n Modulo 1*, abstract, introduction and Definition 2.1:
https://web.pdx.edu/~veerman/numbertheorypaper.pdf
(`mw1qzkrawwm7aw`, index 0). This is numerical evidence, not a proof, and describes precisely this question as open. Its counting definition uses closed subintervals, consistent with the task.

Lean `IsEquidistributed` quantifies all closed subintervals and counts indices in `Finset.range n`, coerces cardinality to ℝ and divides by real n; the modulo-one definition applies `Int.fract`. The task specializes the ambient interval to [0,1], whose length is nonzero. Including n=0 as the first sequence index, allowing singleton test intervals, and the value at denominator n=0 do not change the limiting property. No obvious contradictory quantifier, wrong division domain, or endpoint defect was found. The unrelated original prefix accumulation lemma is not used by the target type.

Read issue https://github.com/google-deepmind/formal-conjectures/issues/5003 in full (`mw1qzkrawwm7aw`, index 1). Its counterexample concerns **every transcendental multiplier**, a different sibling declaration. The issue explicitly excludes the present target from its refutation. Accordingly this task is marked `consistent`, not `mismatch`. No mathematical inputs were edited.

Wikipedia direct retrieval returned HTTP 403; the cited book and author-hosted article were successfully read instead, so this did not block fidelity assessment.

## Public Lean4 proof search

First exactly matched the complete task ID against the skill's `references/public-lean4-proofs.csv`; no match (see `public-index.txt`). Then used independent groups of searches, not just the target name:

- `Kuipers Niederreiter Uniform Distribution sequences (3/2)^n open problem distribution powers`
- `3/2 powers fractional parts equidistributed open problem Mahler Weyl`
- `"isEquidistributedModuloOne_three_halves_pow" Lean proof`
- `"(3/2)^n" "Lean" equidistribution proof`
- `"three_halves_pow" "proof" Lean`
- `site:github.com "Equidistribution" "three_halves" Lean`
- `site:github.com leanprover-community mathlib "equidistributed" "3 / 2"`
- `"Uniform Distribution of Sequences" "Lean4" proof`
- `"Kuipers" "Niederreiter" "Lean" "3/2"`
- `"Ralf Stephan" "steering" "Lean" github`
- `"isEquidistributedModuloOne_three_halves_pow" site:github.com/google-deepmind/formal-conjectures/pull`
- `"3/2" "equidistribution" "Lean4" proof GitHub`

Search result IDs: `mw1qzh38p2m4zz`, `mw1r0ddxn2epik`, `mw1r0s148nkdjv`, `mw1r25qohzk2aq`. Search summaries sometimes conflated sibling problems; conclusions below use the fetched original sources instead.

Sources and follow-up exclusions:

1. Read pinned **and current main** upstream Lean source. Current main is at https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Books/UniformDistributionOfSequences/Equidistribution.lean (`mw1r1gnh8fmo9s`, index 3): the exact target remains `by sorry` and `research open`. Main now proves some accumulation-point statements, but these are strictly weaker and do not count. Issue #5003 and referenced PRs about the multiplier or accumulation lemma are likewise not proofs of this target.
2. Searched local pinned Mathlib/FormalConjectures sources (see `local-mathlib-source-search.txt`) and targeted GitHub/Mathlib web searches. No matching complete proof found.
3. Ralf Stephan's arXiv:2607.11648 and arXiv:2610.30937 claim Lean formalizations for **subword-complexity bounds**, not uniform distribution. Followed the source link to https://github.com/rwst/Superlinear-Complexity ; cloned and inspected actual `TH/KernelDirect.lean`, `TH/KernelReduction.lean`, `Solution.lean`, `Challenge.lean`, and `CITED/SubspaceTheorem.lean`. `TH.complexity_superlinear` concludes `∀ C, ∃ K, ∀ k≥K, C*k < complexity k`; it is not the target, and the development also permits external axiom `Subspace.evertseSchlickewei`. No equidistribution theorem in its Lean sources. Excluded on statement (and axiom footprint), not treated as a completed target proof.
4. https://github.com/jjc16/mahler-3-2-lean4 was actually cloned by the fetch tool; inspected README and searched its Lean sources. Read `SolenoidRigidityDiscrepancyAndRenormalization.lean` lines 208–297: its discrepancy-to-escape and Erdos–Turan theorems explicitly **assume** needed discrepancy bounds; they do not prove uniform distribution or a limit of the counting ratios. The repository states Mahler's Z-number question remains open. Not a target proof.
5. https://github.com/ghywel/placego/blob/main/MAHLER.md is Mahler research, not a proof of this equidistribution theorem; its Lean link leads to the jjc16 repository inspected above.
6. https://github.com/motanova84/Riemann-adelic/blob/main/LEAN_FORMALIZATION_TRILOGY_README.md claims a Weyl formalization. Followed to actual https://raw.githubusercontent.com/motanova84/Riemann-adelic/main/formalization/lean/WeylEquidistribution.lean and read the full source (`mw1r3ic1e9pmua`, index 0). It addresses `(n:ℝ)*α`, **not** `(3/2)^n`, and its criterion and analytic lemmas contain `sorry` (with additional unrelated axioms). Excluded.
7. https://aixiv.online/trace/66/view was fetched and searched: unrelated Erdős-problem trace, no occurrence of this target theorem. The HuggingFace formal-conjectures mirror is a statement/placeholder collection, not proof evidence. Numerical uniformity article is not a Lean proof. OpenAI `lean/docs/015.md` concerns torus packets, a different problem. Polynomial `n^(3/2)` search hits are also a different sequence.

Result: `public_lean4_proof=false`, status `searched`: after varied searches, reading the major sources and following relevant Lean repositories, no known public complete Lean4 proof of this positive target was found. This is a bounded search result, not an absolute assertion of nonexistence. No unresolved relevant proof lead or key access blocker remains; retrieved unrelated proofs were not compiled in the task environment or copied into the task/image.
