# Statement and public-proof review (2026-11-04)

Task: `wikipedia-firoozbakht-firoozbakht-conjecture-prove` (positive direction).

## Statement fidelity

Read the entire pinned upstream `FormalConjectures/Wikipedia/Firoozbakht.lean`
at commit `233a10e857ef78e79fd9fe661d37db724089170a`, the golden Target,
and the original Prime Puzzles source:

- https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/Firoozbakht.lean
- https://www.primepuzzles.net/conjectures/conj_030.htm
- https://raw.githubusercontent.com/leanprover-community/mathlib4/master/Mathlib/Data/Nat/Prime/Nth.lean

The source describes strictly decreasing `p_k^(1/k)` for every `k >= 1`.
Lean's `Nat.nth Prime` is zero-indexed (0 maps to 2, 1 to 3); the
`(n + 1 : Real)` denominator compensates exactly. The actual elaborated
sequence is `fun n => (Nat.nth Prime n : Real) ^ (1 / ((n : Real) + 1))`.
The theorem covers all natural `n`, comparing the next term strictly with the
current term. There is no zero denominator, omitted initial prime, reversed
inequality, or natural-number division. The n=0 case is sqrt(3) < 2.
The task is the conjecture itself, not the conditional prime-gap consequence
that follows it in upstream. No obvious statement/definition error found;
metadata marked `consistent`. No mathematical input was modified.
Wikipedia fetch returned HTTP 403; the original Prime Puzzles reference was
successfully read instead.

## Public complete Lean4 proof search

Exact `task` match in the skill's `references/public-lean4-proofs.csv`: no rows.
Searches used multiple query groups (web search response IDs
`mw1vgjcjqh4emm`, `mw1vgzzqh8y7ak`, `mw1vi8casvjlw4`):

- `"Firoozbakht" "Lean4" proof`
- `"Firoozbakht.firoozbakht_conjecture"`
- `"Firoozbakht" Lean theorem proof GitHub`
- `"Firoozbakht" site:github.com "proof" Lean`
- `"firoozbakhtSeq" "by"`
- `"Firuzbakht" "Lean"`
- `"Firoozbakht" "Lean" Kourbatov Sabihi Feliksiak`
- `"Firoozbakht" site:github.com/google-deepmind/formal-conjectures/pull`
- `"Firoozbakht" site:github.com/leanprover-community/mathlib4`
- `"prime" "nth root" "strictAnti" Lean`
- `"Firoozbakht" Lean proof fork branch`

Candidates actually followed/read:

1. Current upstream Lean source still has `by sorry` and `research open`:
   https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/Firoozbakht.lean
2. Upstream issue #170 concerns organizing formalized statements; its linked
   PR #234 was read as a complete patch. All five commits introduce/edit
   statements and leave this target `sorry`; the solved annotation belongs
   only to the conditional consequence:
   https://github.com/google-deepmind/formal-conjectures/issues/170
   https://github.com/google-deepmind/formal-conjectures/pull/234.patch
3. Cairn Commons displays this exact Lean statement with zero claims/verified
   results: https://cairn-commons.com/problems/firoozbakht
   The Prove Together search result also lists the open statement, not a proof.
4. The SamuelSchlesinger catalogue README and linked number-theory page only
   list the open problem, with no Lean solution link:
   https://raw.githubusercontent.com/SamuelSchlesinger/open-conjecture-formalizations/main/open-problems/README.md
   https://raw.githubusercontent.com/SamuelSchlesinger/open-conjecture-formalizations/main/open-problems/number-theory.md
5. Search hit lean-genius issue #30054 was followed to its actual Lean file:
   https://github.com/rjwalters/lean-genius/issues/30054
   https://raw.githubusercontent.com/rjwalters/lean-genius/main/proofs/Proofs/Erdos4Problem.lean
   `firoozbakht_conjecture` there is only a `def ... : Prop`, not a theorem.
   The Maynard result is an unrelated axiom; the proved comparison is about
   different logarithmic bounds. Thus it is not a proof of this task (and its
   zero-index convention also differs from this task's compensated exponent).
6. Mathlib named/structural searches did not produce a proof. Its actual
   `Mathlib/Data/Nat/Prime/Nth.lean` was read: it gives initial prime values,
   not monotonicity of the prime-root sequence.
7. Kourbatov https://arxiv.org/abs/1503.01744 and Visser
   https://arxiv.org/abs/1904.00499 explicitly give finite computational
   verification, not this unrestricted theorem and not complete Lean4 code.
   Sabihi https://arxiv.org/abs/1603.08917 is a prose proof claim, not a
   complete Lean4 development. Prime Puzzles also records withdrawn/prose
   claims; no associated Lean4 proof link was found in the author/name search.
8. Search hit upstream issue #4596 was read and excluded: it concerns Written
   on the Wall II 198a, not Firoozbakht. The two harmoniclib Telegram hits were
   also fetched; the returned pages contain no Lean proof or relevant link.

GitHub API rate-limited issue fetching, but direct raw HTML retrieved issues
#170, #30054 and #4596 successfully; PR patches/raw Lean sources also loaded.
A guessed `open-problems/firoozbakht.lean` URL returned 404; the actual linked
number-theory catalogue was then read. No promising proof branch/fork or
unverified Lean solution link remained. No complete public Lean4 proof found
by these searches; this is not a claim that no such proof can exist. No public
answer was added to the task and no candidate public proof was compiled.
