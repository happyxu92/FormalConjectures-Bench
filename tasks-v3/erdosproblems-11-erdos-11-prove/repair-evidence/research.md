# Scope and source checks

Task: `erdosproblems-11-erdos-11-prove`. Checked the **positive, all odd n > 1** direction, not a counterexample target or an eventual/finite variant. No public proof has been installed in the task.

## Statement fidelity

- Pinned source read: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/11.lean . Target agrees with its `Erdos11.erdos_11`.
- Full task prefix has imports and namespace only, no custom mathematical definitions. `Odd` and `Squarefree` resolve to standard definitions on naturals. Existential exponent is natural (including zero); the equality is addition, not truncated subtraction. The strict lower bound excludes n = 1. No obvious false-statement defect identified.
- Author source: Granville and Soundararajan, *A Binary Additive Problem of Erdős and the Order of 2 mod p²*, Ramanujan Journal 2 (1998), 283–298, https://dms.umontreal.ca/~andrew/PDF/wieferich.pdf . First page/Conjecture 1 read as a rendered image because PDF text extraction was garbled. It asks for a squarefree summand plus a power of two for odd positive integers; the task's n > 1 avoids the trivial exceptional value.
- Direct erdosproblems.com/11 requests hit Cloudflare/403. This did not prevent checking the original author's paper and the pinned Lean source.
- Current upstream source additionally read: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/11.lean . Its main theorem is now eventual, but the exact all-odd statement is retained as `erdos_11.variants.all_odd` (still `sorry`). PR https://github.com/google-deepmind/formal-conjectures/pull/6650.diff confirms the distinction. This task is an acceptable retained stronger variant, not a mistaken eventual statement.
- PR https://github.com/google-deepmind/formal-conjectures/pull/5817.diff corrects a DIFFERENT theorem about non-Wieferich primes; that theorem is absent from this task's prefix and does not invalidate this target. No paired task was changed.

## Public complete Lean4 proof search

The skill CSV `references/public-lean4-proofs.csv` was read with `csv.DictReader` and matched by the complete `task` column; no match for this exact ID.

Web searches (separate varied groups):

1. `"Erdos11.erdos_11" Lean proof`; `"Erdos" "11" "squarefree" "Lean" proof`; `"squarefree" "power of 2" "Lean4"`.
2. `site:github.com "erdos_11" "by" "squarefree"`; `site:github.com "Erdos11" proof Lean fork`; `"Granville" "Soundararajan" "Lean" "squarefree"`; `"Erdős 11" "Lean" proof`.
3. `"erdos_11.variants.all_odd" proof Lean`; `"squarefree" "power of two" "Lean" "proof"`; `site:github.com "erdos-11" "proof" "squarefree"`.
4. Source searches for Erdős 11, Granville–Soundararajan, and the author's 1998 paper.

Sources and candidate exclusions:

- Both pinned and current FormalConjectures files were read. The exact current alias `variants.all_odd` still has `sorry`; the proved `eventually_of_all_odd` has the full target as an assumption, so is not a solution.
- GitHub upstream PR search via `https://api.github.com/search/issues?q=repo%3Agoogle-deepmind%2Fformal-conjectures+is%3Apr+%2211%22+squarefree&per_page=30` returned 13 results. Relevant PRs 240, 5817, 6650 were followed and their diffs read; they introduce or correct statements, not a complete proof. Other result titles concern different problems. Upstream file history and the contribution repository's branches were also inspected via public GitHub API.
- https://conjectures.io/problems/erdos11-erdos-11?mode=counterexample identifies an unsolved task and one contribution. The page's counterexample mode is NOT this task's direction; its displayed original conjecture agrees with ours.
- Followed that page's actual public Lean4 source: https://raw.githubusercontent.com/conjectures-io/conjectures-contribution/main/contributions/erdos-11/9912bf43713402fa030c83358b48a3fe22041358846f121c30389f4e1775d74a/script.lean . Entire file read. It proves witness elimination, parity/doubling and conditional variant reductions, plus a bounded n < 1024 theorem. Its global implications explicitly assume the conjecture; it does not prove this unbounded positive target. Sources/metadata directory and `sources.md` also inspected. This is partial progress, not a complete proof, and its proof source was not copied into this task.
- https://erdosproblemaday.com/problem/11 reports open/no Lean solution; treated as corroboration, not as sole evidence.
- Current Mathlib `Mathlib/Data/Nat/Squarefree.lean` read and Mathlib squarefree docs/search checked. They supply local arithmetic facts/decidability, not the global additive conjecture.
- https://arxiv.org/abs/2411.01964 (*On the Sum of Squarefree Integers and a Power of Two*) only verifies up to 2^50 using GPU computation, not a complete unbounded Lean proof.
- Granville–Soundararajan's author paper supplies conditional/analytic results, not a Lean4 proof. Search hit LeanGenius Erdős 10 concerns primes, not this squarefree problem. The `openai-math-slop/lean/docs/020.md` hit concerns squarefree quartics, unrelated. arXiv:2601.07421 is about Erdős 728, not 11. Validator API documentation mentioning Erdos11 merely illustrates task submission; it is not proof source.

Result: after these searches and following the promising actual Lean contribution, no known public complete Lean4 proof of this task's exact statement/direction was found (`public_lean4_proof=false`, status `searched`). This is not a proof of nonexistence. No remaining concrete promising proof link was left unexamined; erdosproblems.com access restrictions are recorded above.
