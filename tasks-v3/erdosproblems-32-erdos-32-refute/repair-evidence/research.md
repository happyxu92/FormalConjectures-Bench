# Statement and public-proof checks (2026-11-04)

## Actual task / statement review

Task ID: `erdosproblems-32-erdos-32-refute`. The target is **the negation** of existence of an additive complement to primes with counting function little-o of log-squared; it is not the positive existence theorem, the big-O variant, the density-one variant, or the O(log N) variant.

Read the complete pinned upstream file:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/32.lean
and the complete local Target prefix and declaration. Upstream `erdos_32` asks `answer(sorry) ↔ ∃ A, ...`; the task intentionally retains its RHS under negation. Natural-number domain, eventual `atTop` representation of every sufficiently large n as p+a, membership, `[1,N]` counting, real cast, natural logarithm, exponent 2 and little-o filter all match that underlying proposition. Excluding 0 from the count only changes a bounded term. The eventual assertion is not a density-one assertion.

Original source/author pages read:
- https://www.renyi.hu/~ruzsa/cikkek.html (author bibliography, links `comprim.dvi`).
- https://renyi.hu/~ruzsa/cikkek/comprim.dvi (web fetch returned full DVI data; intro, Theorem 1, Conjectures 1–3, Theorem 2, proof sections and references were inspected in extracted output; binary encoding limits readability). In its introduction, B(x)=|B∩[1,x]|; Erdős's O(log² x) result represents all but finitely many natural numbers. Kolountzakis's O(log x log log x) improvement and Ruzsa's ω(x)log x result have **density-one**, not eventual-all, coverage. Thus they do not contradict the present negative target. Theorem 2 gives a liminf/log lower bound e^gamma and does not establish the refutation here.
- https://theoremdb.org/statements/P2984/ also reproduces the underlying existence question and cites the maintained database.
- Official https://www.erdosproblems.com/32 and forum/thread/32 were attempted repeatedly, including alternate hostname and query; HTTP 403. Publisher PDF also HTTP 403. The author DVI was accessible through the web fetch route at the non-www hostname, although host curl requests were denied.

No concrete definition error or counterexample to the *actual negative task* was found. `statement_status = consistent` means no evident formalization defect; it does not assert that this side of the open question is true. Statement/definitions/golden/frozen hashes were not edited.

## Public complete Lean 4 proof

First exact-matched the skill CSV `task` column on the full task ID: zero rows. This is not evidence of absence.

Actual keyword groups searched (web search, varied independent queries):
- `Erdos32 Lean proof erdos_32`
- `Erdős 32 Lean additive`
- `IsAdditiveComplementToPrimes proof`
- `Erdos32 refutation Lean`
- `additive complement primes Lean4 proof`
- `ErdosProblems/32.lean proof pull request`
- `site:github.com erdos_32 by -google-deepmind/formal-conjectures`
- `site:github.com/leanprover-community/mathlib4 additive complement prime`
- `site:github.com Erdos32 -google-deepmind/formal-conjectures`
- `Ruzsa completion of primes Lean`
- `Erdos 32 Lean proof negation`
- Original mathematical statement / title / author searches including Ruzsa 1998, log-squared, little-o and additive completion.

Followed actual leads:
1. Read current upstream `main` 32.lean via raw GitHub: target and variants still contain `sorry`; not a complete proof in either direction.
2. GitHub issue https://github.com/google-deepmind/formal-conjectures/issues/2302 was reached via HTML after the API rate limit. It reports a status mismatch, not a proof. Followed closure link PR https://github.com/google-deepmind/formal-conjectures/pull/2325 and read its `.diff`: the 32.lean change only renames the log_squared variant; no refutation proof.
3. https://github.com/jaredwilder/additive-combinatorics-campaigns README concerns #52 and finite C3/C5 certificates, not this proposition.
4. https://github.com/williamjblair/lean-proofs/blob/main/README.md lists #730/#154/#94/#399/#1074; no #32 proof.
5. https://arxiv.org/abs/2608.08643 is a formalization of a conjecture's statement, not a full Lean proof of this task's negation.
6. https://theoremdb.org/statements/P2984/ records an open problem, no Lean solution.
7. Retrieved the maintained teorth/erdosproblems `data/problems.yaml` entry 32: informal open, formal unformalized; not a proof.
8. Secondary pages about an O(log N) lower bound concern a different variant and do not supply this full refutation or a Lean source. No unverified claimed Lean proof of this actual direction was found.

Outcome: **unknown / blocked**, not `false`. Searches found no verified public complete Lean4 proof of the refutation, but direct access to the official problem discussion (a key location for proof links) was blocked. GitHub API was rate limited, with the identified issue and PR successfully followed through HTML/diff. No proof code or public solution was added to the task/image.
