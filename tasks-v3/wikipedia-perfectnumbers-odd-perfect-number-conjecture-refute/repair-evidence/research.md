# Statement and public-proof review

## Actual task and statement (step 5)

Task: `wikipedia-perfectnumbers-odd-perfect-number-conjecture-refute`.
Pinned upstream: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/PerfectNumbers.lean
The entire upstream file was fetched and read. Its conjecture is
`odd_perfect_number_conjecture (n : ℕ) (hn : Perfect n) : Even n`.
The task is explicitly its refutation: `¬ (∀ (n : ℕ) (hn : Perfect n), Even n)`.
This is equivalent classically to an odd positive perfect natural number existing, NOT nonexistence and NOT Euler's conditional structure theorem.

The complete golden prefix was inspected. `open Nat` resolves `Perfect` to `Nat.Perfect`; the pinned Mathlib `Mathlib/NumberTheory/Divisors.lean:396–397` defines it by sum of proper divisors equalling n AND `0 < n`. Thus zero does not give a counterexample. There is no truncated interval, mistaken domain or missing positivity in the actual target. The two unrelated preceding admitted infinitude statements are not dependencies of ExpectedType or of the isolated candidate fixture; the transitive audits confirm this.

Source paper read (introduction/preliminaries): Pascal Ochem and Michaël Rao, *Odd perfect numbers are greater than 10^1500*, https://www.lirmm.fr/~ochem/opn/opn.pdf ; author page https://www.lirmm.fr/~ochem/opn/ . The paper defines perfection by the sum of proper positive divisors and explicitly identifies existence as open; lower bounds and Euler form are conditional, not existence results. Wikipedia was also requested but returned a Wikimedia rate-limit error; author sources were read instead. Search queries included `odd perfect numbers existence open problem Ochem Rao 2012 10^1500` and `Wikipedia perfect number odd perfect numbers unknown exist`.

Conclusion: `statement_status = consistent`. An intentional paired refutation of an open conjecture is not an obvious mathematical misstatement. No mathematical files or frozen baselines were changed.

## Public complete Lean4 proof review (step 6)

First, Python csv.DictReader matched the FULL task ID against the skill's `references/public-lean4-proofs.csv` task column: zero rows. This is not evidence of absence by itself.

Actual web search groups (web_search, OpenAI provider):
1. `"odd perfect number" "Lean" proof existence`; `"odd_perfect_number_conjecture" Lean github`; `"odd perfect" "Lean4"`.
2. `"exists" "odd perfect number" "Lean" proof -site:prove2.me -site:beta.prove2.me`; `site:github.com "odd" "Nat.Perfect" "∃"`; `site:github.com/leanprover-community/mathlib4 "odd_perfect"`; `site:github.com/google-deepmind/formal-conjectures/pull "perfect"`.
3. `"PerfectNumbers.formal_conjectures_bench_refutation"`; `"odd perfect number" "Lean" "counterexample"`; `"odd perfect number" "Lean" "existence proof"`; `"odd perfect" "Lean 4" "refutation"`.

Sources and exclusions actually checked:
- https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/PerfectNumbers.lean : still sorry for the conjecture; no proof of this refutation.
- Followed the upstream formal_proof URL to https://raw.githubusercontent.com/mzhorvath1/formal-conjectures/7deed78f7babe2ae9ea13969a8dfa26854982407/FormalConjectures/Wikipedia/PerfectNumbers.lean . Read the Lean source: proof is only `odd_perfect_number.euler_form`, conditional on an odd perfect number. The conjecture still has sorry. Not this direction.
- https://github.com/umpolungfish/odd-perfect-numbers : cloned read-only under /tmp by web tools; inspected actual `OddPerfectNumbers.lean` and its theorem declarations, including lines 355 and 554. `euler_opn_form` and `touchard_congruence` both ASSUME h_odd and h_perf. Neither constructs a number. Not this target, regardless of the completeness of those proofs.
- https://github.com/AEjonanonymous/OPN : cloned under /tmp; read both complete 45-line `OPN-Proof1.lean` and `OPN-Proof2.lean`. They conclude False from extra arithmetic hypotheses, advertise NONexistence and do not prove existence from Nat.Perfect. Opposite direction/conditional claims are not counted; no compilation claim made.
- Current Mathlib `Mathlib/NumberTheory/Divisors.lean` fetched, and pinned definition read in Docker. GitHub/Mathlib `odd_perfect` search gave no matching complete existence proof. A guessed `Mathlib/NumberTheory/PerfectNumbers.lean` URL returned 404, not treated as evidence of absence.
- Prove2Me mission https://prove2.me/missions/Odd_Perfect_Number_Conjecture was fetched, but returned only a generic frontend/about shell. Search also surfaced theorem pages; their full underlying proof collection was not available from the mission response.
- Additional lead https://github.com/elamaunt/Euclids-path/blob/main/prose/47_PerfectNumbers.en.md and the repository root both returned 404. The search describes partial perfect-number results, but the underlying source cannot be inspected.
- Other hits concern OddOrder, Euler/Touchard constraints, lower bounds or alleged nonexistence, not the present existence/refutation direction.

Result: substantial multi-query, direction-aware search found no VERIFIED matching complete Lean4 proof, but full Prove2Me collection and one repository lead could not be independently inspected. Conservatively `public_lean4_proof = "unknown"`, status `blocked`, not false and not a claim that no proof exists. No public proof was installed or included as an answer.

Web result IDs for reproducibility of this session: mw1w0m3evhaexs (pinned source/Wikipedia); mw1w19qtohn8cl (author page/paper); mw1w2jevmtmpwt, mw1w7e3gija7o9, mw1w8q0l30vvul (search groups); mw1w3ospb23f6w (upstream/fork/repositories/mission); mw1w8zouaag71k (Mathlib/source fetches).
