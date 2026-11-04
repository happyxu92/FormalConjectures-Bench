# Statement and public-proof review — erdosproblems-264-ii-prove

## Actual target and statement fidelity

`environment/data/FormalConjecturesBench/Target.lean:44–45` defines the predicate for `b : ℕ → ℕ`, bounded above and nowhere zero. The target (line 60) is the **affirmative** exact-factorial statement `IsIrrationalitySequence Nat.factorial`. This is not the negative paired task. The frozen earlier theorem about powers of two is irrelevant to the target's type/proof dependencies; it is not a solution of the factorial question.

Read the complete pinned source, https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/264.lean . Its `parts.ii` asks `answer(sorry) ↔ IsIrrationalitySequence Nat.factorial`; the benchmark selects the affirmative direction without changing the pinned definition.

Read Kovač–Tao, *On several irrationality problems for Ahmes series*, https://arxiv.org/html/2406.17593 , especially §2.1.3 (Type 3 sequences), Theorems 2.5 and 2.7, and the discussion of factorials. Type 3 quantifies over bounded nonzero **integer** perturbations; the paper explicitly also discusses positive perturbations. Our pinned natural-valued/nowhere-zero perturbations are a weaker, reasonable positive-perturbation variant, not the full signed-integer question. Beginning at zero adds only a rational finite term. For factorials all denominators are positive and the series is dominated by the summable reciprocal-factorial series. No zero-denominator or nonsummability defect is apparent. Open status is not evidence that the selected assertion is false.

The current upstream has changed the predicate to signed integers with both bounds; see https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/264.lean and issue 4264 / PR 4289. That broader definition is not silently substituted into this pinned task. No statement, Target, golden, GoldenCheck, header or frozen-prefix hash was changed. Metadata is marked `consistent` under the skill's reasonable-variant criterion.

Direct erdosproblems.com problem/LaTeX/forum fetches returned 403. Search-index results and https://erdosproblems.ai/wiki/problems/irrationality/E0264 supplied corroboration of the open factorial question. The accessible primary paper and pinned Lean source support the fidelity assessment independently of that access limit.

## Public Lean4 proof search

First exact `task`-column match in `skills/lean-task-repair/references/public-lean4-proofs.csv`: no row for **erdosproblems-264-ii-prove**. Rows for `264-i` and `264-example` were used only as pointers to other results, never as proof of this task.

Performed multiple live searches (not just the exact-name lookup):

- `site:erdosproblems.com/264 factorial irrationality sequence`
- `Erdos 264 factorial bounded positive integers n! irrationality sequence`
- `"Erdos264.erdos_264.parts.ii" Lean proof`
- `"erdos_264" "factorial" Lean proof`
- `"irrationality sequence" "factorial" "Lean"`
- `"Erdos 264" "Lean4" proof factorial`
- `"IsIrrationalitySequence" "factorial" -site:conjectures.io`
- `"Kovac" "Tao" "264" Lean proof github`
- `site:github.com "264" "factorial" "irrational" Lean`
- `"Erdős" "264" "Aristotle" "github"`
- `site:erdosproblems.com/forum/thread/264 "Lean"`
- `site:github.com "erdos_264" "by" -repo:google-deepmind/formal-conjectures`
- `site:github.com/leanprover-community/mathlib4 "irrational" "factorial"`
- `"264" "Nat.factorial" "sorry" Lean proof`
- `"factorial" "bounded perturbations" Lean proof`

Checked promising sources and excluded them against the actual affirmative factorial proposition:

1. **Upstream main/history/PRs and forks.** Current `264.lean` still has `parts.ii := by sorry`. Retrieved GitHub's file-history API and issue/PR search, including closed claimed-solving PRs 2488 and 2865. Read their head source files at `theaustinhatfield/formal-conjectures` commits `d31915604cd9750c81ee81a649f371061e547ae9` and `14841df8f477d583c9a8a24ac89e2f4ce3dc1a87`: the factorial theorem remains `sorry`; their 'formally solved' claims merely relabel other sorry declarations. These are not complete proofs.
2. **Actual author/Aristotle Lean files.** Read https://raw.githubusercontent.com/plby/lean-proofs/main/src/latest/ErdosProblems/Erdos264b.lean and https://raw.githubusercontent.com/VjekoKovac/erdosproblems/main/Erdos264.lean . The former explicitly says partial results, proves the negative powers-of-two and positive double-exponential cases; it has no factorial theorem. The latter explicitly formalizes the first half, a bounded `{1,…,5}` perturbation of `2^n`, not factorials. Neither implies this task. Also read the linked `plby/lean-proofs/ErdosProblems/Erdos264.md` and the claim pages below.
3. **Alternate names/definitions.** Read https://raw.githubusercontent.com/rjwalters/lean-genius/main/proofs/Proofs/Erdos263Problem.lean . It concerns a different (relative-perturbation) irrationality-sequence predicate; its key Kovač–Tao/positive-condition results use `sorry`, and its factorial result is conditional on a missing theorem. It is not this additive bounded-perturbation affirmative statement. The search result's multiplicative factorial counterexample likewise addresses another definition and is not a refutation or proof of our target.
4. **Community records.** Read https://raw.githubusercontent.com/wiki/teorth/erdosproblems/AI-contributions-to-Erd%C5%91s-problems.md , https://erdosproblems.ai/wiki/problems/irrationality/E0264 and claim pages `/claims/2025_12_18_alexeev` and `/claims/2024_11_27_kovac_tao`. They distinguish the partial powers-of-two formalizations from the unresolved factorial case. Read https://www.erdosproblemaday.com/report/264 : it labels its outcome PARTIAL and leaves the uniform factorial irrationality step open. The search hit arXiv:2601.07421 concerns Erdős 728, not 264, and was excluded after fetching its abstract.
5. **Mathlib.** Queried the public mathlib4 repository with factorial/irrationality keywords and searched the task's actual pinned `Mathlib` sources for `IsIrrationalitySequence|factorial.*Irrational|Irrational.*factorial`; no matching result was found. Classical irrationality of e is not a bounded additive-perturbation theorem.

Access limits: erdosproblems.com direct fetches and a Tao blog URL were 403; source content of the relevant linked public Lean proofs was obtained directly from GitHub, and the paper was read on arXiv. A guessed `borisalexeev/lean-proofs` URL and an initially wrong wiki raw URL were 404; the correct `plby/lean-proofs` and `raw.githubusercontent.com/wiki/...` sources were subsequently found and read. No pending relevant factorial proof lead remains from these searches. No candidate proof was compiled or copied into the task.

Conclusion: **searched, no known complete public Lean4 proof found for this task's affirmative exact-factorial, bounded-positive-natural-perturbation statement**. This is not an absolute claim that no proof exists. Do not reuse the `264-i` or `264-example` public-proof result for this direction.
