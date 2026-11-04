# Mathematical statement and public Lean4 proof review

Task: **erdosproblems-32-erdos-32-prove**, positive direction only. No mathematical input, answer, or paired task was changed.

## 5. Statement fidelity: consistent

Read all of the public Target, including its prefix definitions/variants, and the pinned upstream file:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/32.lean

Target.lean:40–42 defines an additive complement by `∀ᶠ n in atTop, ∃ p, p.Prime ∧ ∃ a ∈ A, n = p + a`. The target after the marker asserts existence of a set of natural numbers with that property and counting function over Icc 1 N little-o of `(Real.log N)^2`. It is the affirmative proposition underlying upstream erdos_32's answer-wrapper question, not the weaker log_squared big-O variant, not the log_bound question, not an almost-all/density-one complement. Natural-number coercion in log is correct, and the values at 0/1 have no effect on atTop. Allowing 0 in A changes counting by at most one, irrelevant to this asymptotic target. No obvious contradiction or definition error was found; openness alone is not an error.

Primary original source read: Paul Erdős, *Some results on additive number theory* (1954), pp.847–849, https://renyi.hu/~p_erdos/1954-09.pdf . Theorem 1 constructs a full additive complement with O(log² n) growth and the subsequent question asks whether it is best possible. This matches the stronger little-o existence question in this task rather than asserting a known big-O result suffices.

Original problem page/forum https://www.erdosproblems.com/32 and /forum/thread/32 returned Cloudflare/403. Successfully read the problem restatement and verbatim-source quotation in https://www.erdosproblemaday.com/report/32 and https://we-solve.github.io/problems/erdos-problem-32-1a10a7c3/ and the maintained https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml entry number "32": open, formal_status unformalized, statement formalized yes. No invalidity inferred from this status. Ruzsa PDF host matwbn.icm.edu.pl also returned 403; it was not used to claim a counterexample.

Read arXiv https://arxiv.org/abs/2610.14127 (v3, 2026-11-01): its abstract concerns the lower bound log X log log X and the negative answer to O(log X), which does NOT decide whether a complement is o(log² X). No reverse-direction conclusion was copied into this task.

## 6. Public complete Lean4 proof: searched, not found

First exact-match lookup of `task` in `/root/FormalConjectures-Bench/skills/lean-task-repair/references/public-lean4-proofs.csv`: zero matches for the complete task ID. Then multiple actual web-search groups:

1. `Erdos problem 32 additive complement primes little o log squared Ruzsa`; `site.erdosproblems.com/32 additive complement`; `Erdős 32 additive completion primes Lean4 proof`.
2. `"Erdos32.erdos_32" proof Lean`; `"IsAdditiveComplementToPrimes" Lean proof`; `"Erdos" "32" "Lean" "proof" primes complement GitHub`; `"Ruzsa" "additive completion" Lean4`.
3. `"W_tgqprufg_v1"`; `"additive complement" "Lean4" primes`; `"erdos_32" "sorry" proof github fork`; `"Erdős 32" "Lean 4" proof -"152"`.

Sources and candidate exclusion checks:

- Read current upstream Lean source at https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/32.lean . The exact positive erdos_32 statement still ends in `by sorry`; all nearby variants also retain placeholders. A category/solved label is not proof.
- GitHub API issue/PR searches in google-deepmind/formal-conjectures for `erdos_32` (4 hits) and `additive complement` (6 hits), and in leanprover-community/mathlib4 for `additive complement` (3 hits). The mathlib results concern group-action complements/cache tests, not prime additive complements.
- Read actual Lean diffs https://github.com/google-deepmind/formal-conjectures/pull/3165.diff and /pull/2641.diff . Despite proof claims in their descriptions, both only change annotations for the big-O and liminf/Ruzsa variants; they contain no proof of this little-o target. Read /pull/2038.diff : it introduced the statement with sorry, not a proof. https://api.github.com/repos/google-deepmind/formal-conjectures/issues/2302 records an annotation/status mismatch, with no proof or comments.
- https://www.erdosproblemaday.com/report/32 explicitly reports partial finite optimization/Python work, not a uniform complement or Lean proof. The we-solve page lists unverified LLM attempts without a complete Lean artifact.
- https://theoremdb.org/statements/P2984/ records precisely this sub-log-squared target as open, with no complete proof packet. Search hit https://theoremdb.org/records/R1822/ is actually a Lean proof for Erdős **152**, not 32.
- A potentially promising formal-proof hit https://hub.valency.io/works/W_tgqprufg_v1 exceeded the fetch tool's 5MB limit; retrieved its full 6.3MB HTML via curl to /tmp/erdos32-valency.html. Title/abstract identify *The additive indecomposability of the primes*, Ostmann's inverse Goldbach conjecture (P cannot equal A+B), not existence of a thin additive complement (P+A eventually contains all integers). Its linked openai/math Lean project concerns this different statement; excluded by scope, not mistaken for a solution here.
- Read shouqiaow/erdos README and recursive GitHub tree; no Erdos32/erdos_32 or /32/ proof entry. Other search results were different numbered problems, standard Lean algebra documentation, or unrelated papers. The Radomskii arXiv abstract and its secondary report concern a lower bound/log_bound negative direction, not this positive little-o task, and no covering Lean proof was linked.

Main relevant sources and concrete proof leads were followed; no remaining identified candidate claims to prove this exact direction with a complete allowed-axiom Lean4 artifact. Record `public_lean4_proof=false`, status `searched`: a search miss, NOT a mathematical assertion that no proof can exist. Access limits: original problem page/forum and one paper mirror returned 403; alternate statement/status sources were read, and no inaccessible specific Lean proof was identified. No purported proof was added to the task, compiled as an oracle, or included in its image.
