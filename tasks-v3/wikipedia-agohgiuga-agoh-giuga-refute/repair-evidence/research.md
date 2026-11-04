# Statement and public-proof checks

Task: `wikipedia-agohgiuga-agoh-giuga-refute`. Only this task was changed.

## Statement fidelity

Read `task.toml`, the entire original golden Target and upstream
`FormalConjectures/Wikipedia/AgohGiuga.lean` at
`233a10e857ef78e79fd9fe661d37db724089170a` (both the pinned image checkout and
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/AgohGiuga.lean).
The task intentionally asks for `¬ AgohGiuga.AgohGiugaCongr`, not the positive
upstream theorem. The two prefix definitions are unchanged. In particular the
quantifier is over natural numbers p >= 2, k is integral, B is
`bernoulli' (p-1)`, and the equation is p*B.num+B.den=k*p^2. `AgohGiugaSum`
uses the open interval 0<i<p and exponent p-1; it is not the target.

Read the source exposition at
https://mathworld.wolfram.com/AgohsConjecture.html and the author-hosted
Borwein et al. paper https://www.cecm.sfu.ca/~pborwein/PAPERS/P114.pdf.
The PDF text extraction is poor; the MathWorld page explicitly gives the
Bernoulli congruence, and the equivalent denominator-one condition
N/n+D/n^2, consistent with the task's numerator/denominator equation.
Read also the 2025 exposition
https://www.sherynjri.com/static/pdfs/The_Agoh-Giuga_Conjecture.pdf and
https://arxiv.org/abs/math/0409259 (equivalence of the formulations).
The convention B'_1=+1/2 at p=2 gives 2*1+2=4, and does not introduce an
obvious small-prime defect. The deliberate negation is a paired challenge,
not a statement mismatch. No specific counterexample to the definition or
obvious impossible-goal defect was found. Open status is not evidence of a
misstatement. Set `statement_status = "consistent"`; mathematical inputs were
not edited.

## Exact local lookup

Python `csv.DictReader` exact comparison of the complete task ID against
`skills/lean-task-repair/references/public-lean4-proofs.csv`: zero matching
rows. This was followed by actual online searches, not treated as a negative
proof result on its own.

## Search groups actually executed

- Agoh Giuga conjecture Bernoulli n B n-1 -1 prime formulation
- Giuga conjecture Borwein Girgensohn 1996 primality pdf
- Agoh Giuga conjecture refutation counterexample
- `"AgohGiugaCongr" Lean proof refutation`
- `"Agoh Giuga" "Lean" proof github`
- `"agoh_giuga" "refutation" Lean4`
- `site:github.com "AgohGiuga" "¬" Lean`
- `site:github.com "AgohGiugaCongr" proof`
- `site:github.com/leanprover-community/mathlib4 "Giuga"`
- `"Agoh Giuga" "Lean 4" counterexample disproof`
- `site:github.com/google-deepmind/formal-conjectures/pull Agoh Giuga`
- `"AgohGiugaCongr" "False"`
- `"AgohGiuga.formal_conjectures_bench_refutation"`
- Agoh Giuga Lean formal proof Bernoulli refutation counterexample fork

Also searched pinned Mathlib source with `rg 'AgohGiuga|agoh_giuga'`; exit 1,
no matches (not a claim about all possible equivalent Mathlib results).

## Followed candidates and exclusions

1. Read upstream main's complete relevant definitions and target declarations:
   https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/AgohGiuga.lean
   Positive conjecture still has `sorry`; no proof of this negation.
2. Read linked fork
   https://raw.githubusercontent.com/mo271/formal-conjectures/2663234a28260853790aa5752d8d4550ff0ab1ca/FormalConjectures/Wikipedia/AgohGiuga.lean
   It proves a characterization of *weak* Giuga numbers, not existence of a
   counterexample or this target negation.
3. Read SamuelSchlesinger's README, `AgoGiuga/Basic.lean`, and
   `AgoGiuga/Reduction.lean` from
   https://github.com/SamuelSchlesinger/agoh-giuga-conjecture .
   `agoh_giuga_forward` is only the prime implication;
   `conjecture_iff_no_carmichael_giuga` is a reduction;
   `no_carmichael_giuga` has `sorry`. The positive conjecture depends on it.
   Neither a full positive proof nor a refutation. The author's
   https://github.com/SamuelSchlesinger/open-conjecture-formalizations
   points back to this same repository.
4. Read https://prove2.me/theorems/cfd804b3-fea5-4679-a1e8-d43b16ad4b88 .
   Open arithmetic-form conjecture, `by sorry`, not a negation proof.
5. Read https://raw.githubusercontent.com/chokmah-me/fragile-proof-audit/main/docs/audits/agoh-giuga.md .
   Seven known weak-Giuga composites fail Korselt; explicitly does not decide
   the conjecture. These are not strong-Giuga counterexamples.
6. Read https://www.proofatlas.ai/collaboration/agoh-giuga-conjecture/ .
   Research routes and conditional reductions, explicitly open, no concrete
   composite counterexample and no Lean proof artifact.
7. Read MathWorld's linked Lean source:
   https://raw.githubusercontent.com/epoch-research/LeanOpenProblems-results/61137ec/runs/oeis-full-50usd-ant-j0j0g4uzligm1k41/oeis_309132_conjecture_2/Submission/Spec.lean .
   Actual final theorem is `A309132_conjecture ↔ agoh_giuga_conjecture`.
   An equivalence does not prove either conjecture or this task's negation.
8. Read https://raw.githubusercontent.com/Joe975/math-lab/main/STATUS.md and
   https://joe975.github.io/math-lab/giuga.html .
   Finite enumeration/search and bounds; explicitly no existence/nonexistence
   claim for odd Giuga numbers, no full Lean refutation.
9. Actually fetched the upstream PR search
   https://github.com/google-deepmind/formal-conjectures/pulls?q=Agoh+Giuga
   (six results), then read PRs 7660, 6819, 3019, 2983, 2482, 515.
   - 7660 links weak/strong-Giuga characterizations and nine-prime lower bound.
     Read raw `Solution.lean` at danielpuri1901/erdos-lean-formalization
     commits d4e112619d3d00a40b39ccb50b8fdf9cf46db2ab,
     9e79333b40ff376cb761f200d9989193113387bf,
     d22ecd7653a24f616d6bfb523fbc973ff40ef1d6. Their actual final declarations
     prove those variants, not the open conjecture or its negation.
   - 6819 proves `isStrongGiuga_implies_isCarmichael`; read raw source at
     anatoliiohorodnyk/lean-fc-proofs, commit
     394ec1c1ff92bdf2fa10f30d62ae9d0455d3ce20,
     `Proofs/T_AgohGiuga_agoh_giuga_variants_isStrongGiuga_implies_isCarmichael.lean`.
     It is a conditional implication, not a counterexample.
   - 3019/2983/2482 concern solved variants and explicitly acknowledge
     `sorryAx`; no full refutation.
   - 515 changes an auxiliary weak-Giuga definition, not the target Bernoulli
     definition in this task.
   Tracking issue https://github.com/google-deepmind/formal-conjectures/issues/3623
   was closed because the conjecture had already been *added*, not solved.

## Conclusion and limitations

After these searches no known public complete Lean4 proof of the **negative**
target was found. Metadata uses `public_lean4_proof = false` with status
`searched`; this does not establish that no proof exists. No external proof
was compiled or inserted into the task/image.

Wikipedia requests returned 403/Too Many Requests. Alternative MathWorld,
author-hosted paper, original upstream, GitHub raw sources, and exposition
were accessible. GitHub PR fetches used REST fallback (review/check metadata
not available), but their statements and the promising linked raw Lean
sources were read. No remaining candidate purporting to prove this full
negation was left unexamined.
