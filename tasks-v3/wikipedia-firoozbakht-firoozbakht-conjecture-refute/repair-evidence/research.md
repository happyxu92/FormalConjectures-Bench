# Statement and public-proof review

Task: `wikipedia-firoozbakht-firoozbakht-conjecture-refute`.

## Statement (step 5)

- Read pinned upstream `FormalConjectures/Wikipedia/Firoozbakht.lean` at https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/Firoozbakht.lean and the complete local golden prefix/target.
- Source https://www.primepuzzles.net/conjectures/conj_030.htm explicitly states that `(p_n)^(1/n)` decreases, and asks for proof or disconfirmation. Read its opening statement, not purported informal arguments in later correspondence.
- Local `Target.lean` lines 35–53 defines `firoozbakhtSeq n = (Nat.nth Prime n : Real) ^ (1 / (n+1) : Real)` and asks `¬ (∀ n, firoozbakhtSeq (n+1) < firoozbakhtSeq n)`. The task is explicitly the **refutation**, not a proof of the positive conjecture.
- Pinned Mathlib `Mathlib/Data/Nat/Nth.lean` documentation and definition establish zero-indexing; thus `Nat.nth Prime 0` is the first prime, and denominator `n+1` is appropriate. The audit output confirms real rather than natural division. No missing positivity assumptions or empty-prime degeneracy occur (infinitely many primes). This is the literal negation of the universal original statement, not its conditional prime-gap consequence.
- No obvious mathematical misstatement found: `statement_status = consistent`. This does not assert that the refutation is true or solvable. Open status alone is not evidence of an erroneous statement. Nothing mathematical was modified.
- Wikipedia fetch returned HTTP 403; the primary problem page and pinned Lean source were accessible.

## Public complete Lean4 proof (step 6)

Exact CSV lookup: `/root/FormalConjectures-Bench/skills/lean-task-repair/references/public-lean4-proofs.csv`, matching the complete task ID, returned no rows (also saved as `proof-index.json`). This alone was NOT used to infer a negative result.

Actual web-search groups:

1. `Firoozbakht conjecture Lean4 proof refutation counterexample`; `"firoozbakht_conjecture" Lean proof github`; `"Firoozbakht" "Lean" "sorry"`.
2. `site:github.com Firoozbakht Lean refutation disproof`; `"firoozbakhtSeq" proof lean -site:cairn-commons.com`; `"Firoozbakht" "Mathlib" proof`; `"Firoozbakht" "Lean4" counterexample Faride Kourbatov`.
3. `"Firoozbakht.formal_conjectures_bench_refutation"`; `"Firoozbakht" "Lean" (proof OR disproof) -site:cairn-commons.com -site:provetogether.ai -site:github.cnmirror.space`; `site:github.com/google-deepmind/formal-conjectures/pull Firoozbakht`; `"Firoozbakht" "Lean" fork branch`.

Sources/leads actually followed:

- Current upstream source https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/Firoozbakht.lean: complete definition unchanged, conjecture still `by sorry`; its consequence is also `sorry`, conditional on the positive conjecture, and not this refutation.
- https://github.com/google-deepmind/formal-conjectures/pull/234.patch: all five patches read; initial formalization, exponent typing correction and status changes, no proof. https://github.com/google-deepmind/formal-conjectures/issues/170 raw HTML: formalization-organization discussion, not proof; no linked proof branch/PR.
- https://cairn-commons.com/problems/firoozbakht: read full page, catalogue of exactly the prime-root statement with zero claims/verified/refuted results. Prove Together search results also index an open statement, not a proof.
- Pinned Mathlib `Mathlib/` recursively searched for `firoozbakht`: no matches (rg exit 1; not a path error). Public Mathlib queries found no matching refutation either.
- Fork lead `alreadydone/formal-conjectures`: remote HEAD `2f67ab01cb6581150c303e8f98291b48c76bcc32`, default branch main. Raw Firoozbakht path returned 404. A depth-one filtered clone and full HEAD tree listing were performed in `/tmp/fcb-firooz-refute-fork`; no Firoozbakht or prime-gap path, no indexed proof claim was attached to this generic fork lead.
- https://github.com/google-deepmind/formal-conjectures/issues/7643 raw HTML: a **different** Firoozbakht conjecture, OEIS A108569, about totients and even terms. Its claimed Lean counterexample does not refute prime-root monotonicity, so excluded without copying its proof.
- https://www.trureturing.org/research/oeis-a092028-least-self-divisor-power-minus-one/: source page read, theorem is `∀ n > 2, a(n) = minFac (n-1)` for a divisibility sequence; different definitions/statement, excluded.
- https://arxiv.org/abs/1904.00499 (Visser) and https://arxiv.org/abs/1503.01744 (Kourbatov): finite computational verification of the positive conjecture, not an unbounded refutation or complete Lean4 proof. https://github.com/mhawarey/prime-gap-explorer/blob/main/README.md is exploratory computation, not Lean4 proof.
- https://arxiv.org/abs/2605.13171: Formal Conjectures benchmark description, not a proof of this task.

Access limits: Wikipedia 403; GitHub API issue retrieval rate-limited and public code-search requires login. Issue bodies were successfully inspected via raw HTML instead; raw upstream source, PR patch and filtered fork git tree were accessible. No identified relevant proof candidate remains unverified. Search is not exhaustive over all internet history and cannot prove nonexistence.

Result: `public_lean4_proof = false`, status `searched`: after the above multi-source/multi-query review, no known public **complete Lean4 proof of the negated direction** was found. No public answer was added, and no claimed external proof was compiled in this task environment.
