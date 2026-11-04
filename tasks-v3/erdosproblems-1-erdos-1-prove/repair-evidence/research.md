# Statement and public-proof review (2026-11-04)

Task: `erdosproblems-1-erdos-1-prove`, **positive** `Erdos1.erdos_1`.
No public proof source is bundled with the task or image.

## Statement

Read the pinned upstream source in full:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/1.lean

The frozen task correctly retains that revision's positive uniform bound, including
`A ⊆ Icc 1 N`, injectivity on every subset (including the empty subset), a universal
constant `C > 0`, all finite cardinalities and `N ≠ 0`. Strict inequality is
compatible with the traditional lower-bound formulation after shrinking the
constant; excluding zero avoids the empty-interval degeneracy. No prefix bug was found.

However, current upstream explicitly calls this positive statement false and
records **its negation**, with a pinned formal-proof reference:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/1.lean
https://github.com/tadamcz/erdos1/blob/0e395153306f34b3829d118b85bdd704136f2843/Erdos1/Resolutions/Erdos1_219usd_38h.lean#L2419

Read the public Lean source (2427 lines, indexed for declarations and forbidden
proof placeholders). Its predicate agrees with the task, it imports only Mathlib,
and its final `Erdos1.erdos_1.disproof` is the exact negation of this task. No
`sorry`, `admit` or task-local axiom was found in that proof module. The final
argument reduces the assumed constant to `ErdosCounter.no_uniform_subset_bound`,
contradicting the small-normalized-determinant construction. This provides a
specific mathematical obstruction to the retained positive direction; mark
`statement_status=mismatch`, without changing any mathematical input. The public
external disproof was inspected, not compiled in this repair.

https://www.erdosproblems.com/1 and /history/1 were attempted but Cloudflare/403
prevented direct reading. Search-index content and the readable MathWorld page
were also checked; MathWorld still describes the older open-problem status:
https://mathworld.wolfram.com/ErdosDistinctSubsetSumsProblem.html
The newer explicit upstream correction and exact opposite-direction Lean source
are more specific evidence than this older status summary.

## Public Lean4 proof search

Exact `task`-column CSV lookup in the skill's `references/public-lean4-proofs.csv`:
no match for the full task ID. This alone was not used to infer absence.

Queries (multiple search groups):
- `Erdos problem 1 distinct subset sums N constant 2^n`
- `Erdos Moser distinct subset sums conjecture erdosproblems 1`
- `"Erdos1.erdos_1" Lean proof`
- `"Erdős" "distinct subset sums" "Lean" proof`
- `"erdos problem 1" "Lean4"`
- `site:github.com "erdos_1" "proof" "∃ C"`
- `site:github.com/leanprover-community/mathlib4 "sum" "distinct" "Erdos"`
- `site:github.com/google-deepmind/formal-conjectures/pull "1" "disproof"`
- `"distinct subset sums" "Lean" "proof" -site:github.com/tadamcz/erdos1`

Read and excluded these promising candidates for this **positive** target:
1. `tadamcz/erdos1`: README, definitions, dependency import and final proof source
   at the upstream-pinned revision. A complete **disproof**, not a positive proof.
2. https://raw.githubusercontent.com/plby/lean-proofs/main/src/latest/ErdosProblems/Erdos1.lean
   Actual Lean declarations `erdos_1`, `not_erdos_1` are negative. The quantitative
   construction gives `N < 2^(n+1) / log₂ n`, also contradicting the positive task.
   Related claim page was read:
   https://erdosproblems.ai/wiki/problems/additive_combinatorics/E0001/claims/2026_09_15_alexeev
3. https://github.com/lyfar/erdos-moser-distinct-subset-sums-lean
   Read README and `LeanPool/ErdosMoser/Bounds.lean`: variance and square-root
   lower bounds, explicitly not the uniform positive constant of this task.
4. Pinned and current FormalConjectures source: pinned positive declaration is
   `sorry`; current declaration is opposite direction with the reference above.
   Current `lb_strong` fork reference concerns a weaker square-root bound, not
   this task. Mathlib-targeted and upstream PR searches found no positive proof;
   unrelated Erdős 34/350 hits do not state this target.

Conclusion: sufficiently broad searches found no known public complete Lean4
proof of the retained **positive** statement (`public_lean4_proof=false`, status
`searched`). This is not an absolute nonexistence claim. Opposite-direction
proofs must not set this task's flag to true. No promising positive proof lead
remains unexamined; access limits on the historical problem website are noted
above, and its relevant formalization/proof links were retrieved directly.
