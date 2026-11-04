# Statement and public-proof inspection (2026-11-04)

Scope: **erdosproblems-264-ii-refute**, not the positive factorial task and not powers of two. Actual target: `¬ Erdos264.IsIrrationalitySequence Nat.factorial`.

## Statement

Read the entire public/golden Target and pinned upstream file:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/264.lean

The definition at Target lines 43–44 quantifies over natural-valued bounded perturbations, everywhere nonzero, with nonzero denominators, and asks irrationality of the real tsum. Target lines 60–64 negate that property for factorial. This is the negative side of upstream `erdos_264.parts.ii`, not a claimed known theorem. For factorial the terms have no zero denominators, and bounded positive perturbations do not introduce a convergence defect. Starting at zero contributes only finitely many initial terms compared with customary indexing. No concrete contradiction or definition making this direction impossible was found.

Read Kovač–Tao, *On several irrationality problems for Ahmes series*, https://arxiv.org/html/2406.17593, §2.1.3 (Type 3), Theorems 2.5/2.7 and discussion of factorials. The source explicitly permits the alternative positive-perturbation convention. Original signed-integer perturbations are broader than this pinned natural-valued variant; this difference is not by itself a false-statement finding. Upstream issue https://github.com/google-deepmind/formal-conjectures/issues/4264 and PR 4289 document the later change to integers. Mathematical input was not updated.

The negative criterion for powers of two is not applicable to factorial: `(n!)² * sum_{k>n} 1/(k!)²` tends to zero rather than having positive liminf. Existence of an irrationality sequence asymptotic to factorial does not imply the property for exact factorial. No assertion of a resolution of the open problem is made.

## Local collection

Exact `task`-column match in the skill's `references/public-lean4-proofs.csv`: **no match** for the full ID. This alone did not determine the result.

## Online searches actually issued

Three groups, via web_search (response IDs mw1t18pd3oo2an, mw1t1qeinhzi50, mw1t38o2e5tqmr):

1. `"Erdos264" "factorial" Lean proof`
2. `"Erdős 264" "Lean" factorial`
3. `"irrationality sequence" "factorial" formalization Lean`
4. `"IsIrrationalitySequence" "factorial" "¬"`
5. `"erdos_264.parts.ii" Lean proof github`
6. `"Kovač" "Tao" "Ahmes" Lean formalization factorial`
7. `site:github.com "264" "irrationality" "sorry"`
8. `"erdosproblems.com/forum/thread/264" Lean factorial Aristotle`
9. `"Erdos264" Lean github proof -site:github.com/google-deepmind/formal-conjectures`
10. `"factorial" "irrationality sequence" "Lean4" refutation`
11. `"erdos_264" proof pull request mathlib Lean`

## Followed candidates and exclusions

- Read pinned and current FormalConjectures `264.lean`. Factorial remains an open placeholder, not a proof of this direction. Also queried GitHub issues/PR search (`repo:google-deepmind/formal-conjectures 264`) and read file patches for PRs 2488 and 2865: they mark parts.i/example/ko_tao variants, not parts.ii; theorem bodies still have sorry. This is not evidence of a complete factorial refutation.
- Read actual Lean source https://raw.githubusercontent.com/rjwalters/lean-genius/main/proofs/Proofs/Erdos263Problem.lean. Its predicate concerns integer denominators with ratio tending to one (problem 263), not bounded additive perturbations. `kovac_tao_not_irrationality` uses sorry. `factorial_not_irrationality_if_kt` has an additional unproved theorem hypothesis. Growth estimates and a conditional result do not cover this target.
- Read https://conjectures.io/problems/erdos264-erdos-264-parts-ii?mode=counterexample . It publishes a placeholder negative challenge and reports no contribution. Queried https://api.github.com/repos/conjectures-io/conjectures-contribution/contents/contributions/erdos-264-parts-ii : only index.md, no Lean proof.
- Read https://www.erdosproblemaday.com/report/264 . It explicitly labels its result PARTIAL; separation estimates/finite experiments are not a proof of a bounded perturbation with rational sum.
- Read https://erdosproblems.ai/wiki/problems/irrationality/E0264 and its claims/2025_12_18_alexeev page. Related Lean claims cover `2^n` and `2^(2^n)`, explicitly not factorial. These cannot be copied to the current negative factorial direction.
- Searches covered Mathlib's irrationality/factorial material; irrationality criteria and problem 68 lemmas do not provide a bounded perturbation counterexample for this target. A guessed plby Erdos264 raw path returned 404, not proof of repository-wide absence.

## Limits and outcome

The primary erdosproblems.com page, latex view and forum (both www and bare host, including embed=1) repeatedly returned HTTP 403. The author blog URL also returned 403. Although indexed snippets and independently accessible claim pages exclude the visible powers-of-two results, the primary forum's outbound proof links could not all be audited directly. Accordingly metadata is **unknown / blocked**, not false. No complete public Lean4 proof for the actual negative factorial target was verified, and no public proof/answer source was placed in the task or image. A search miss cannot prove nonexistence.
