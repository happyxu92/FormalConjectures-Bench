# Statement and public Lean4 proof review

Task: `wikipedia-perfectnumbers-odd-perfect-number-conjecture-prove`.
Direction checked: **every positive perfect natural number is even**, not existence of an odd perfect number and not merely a constraint on one.

## Statement fidelity (step 5)

- Read the complete golden Target including both earlier conjectures, namespace `PerfectNumbers`, `open Nat`, and the target at lines 83–85. The target is `∀ n : ℕ, Nat.Perfect n → Even n`; there are no extra hypotheses or restricted ranges.
- Read pinned upstream `FormalConjectures/Wikipedia/PerfectNumbers.lean` at commit `233a10e857ef78e79fd9fe661d37db724089170a`, including the source comments, all preceding declarations and the target:
  https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/PerfectNumbers.lean
- Mathlib `Mathlib/NumberTheory/Divisors.lean:394–403` defines `Nat.Perfect n` as sum of proper divisors equal to n **and 0 < n**. Thus zero is not a spurious counterexample. The definition agrees with the positive-integer problem.
- Source cited by the task: https://en.wikipedia.org/wiki/Perfect_number#Odd_perfect_numbers . Direct fetch returned 403; web search retrieved its statement. Independently read the primary Ochem–Rao paper, introduction and preliminaries:
  https://www.lirmm.fr/~ochem/opn/opn.pdf . It defines perfect numbers using proper divisors and explicitly calls odd-perfect-number existence a long-standing open question. Its lower bound is conditional, not a contradiction of this conjecture.
- Also fetched https://mathworld.wolfram.com/OddPerfectNumber.html . No evident quantifier, domain, definition, or direction error was found. Mark `statement_status = consistent`, not a claim that the conjecture has been proved. No mathematical input was changed.

## Public Lean4 proof search (step 6)

First used Python `csv.DictReader` to match the **full** task ID against the skill's `references/public-lean4-proofs.csv` task column: zero matches.

Web query groups actually issued:

1. `odd perfect numbers conjecture all perfect numbers are even Wikipedia`; `odd perfect number Ochem Rao 2012 open problem`.
2. `"odd_perfect_number_conjecture" Lean proof`; `"odd perfect numbers" "Lean4" proof`; `"odd perfect number" "Lean" "github"`.
3. `site:github.com/leanprover-community/mathlib4 "perfect" "even" "theorem"`; `site:github.com "odd_perfect_number_conjecture" "pull"`; `"no odd perfect" "Lean" proof`; `"odd perfect" "formal proof" Lean Aristotle`.

Sources and candidate exclusions:

- Current upstream raw source was read:
  https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/PerfectNumbers.lean . The exact conjecture is still `research open` with `sorry`.
- Followed the upstream AlphaProof/fork link and read its entire relevant source:
  https://raw.githubusercontent.com/mzhorvath1/formal-conjectures/7deed78f7babe2ae9ea13969a8dfa26854982407/FormalConjectures/Wikipedia/PerfectNumbers.lean . The linked proof is **Euler form**, not this target; this exact target remains `sorry` in that fork.
- https://github.com/umpolungfish/odd-perfect-numbers was fetched/cloned (HEAD `8819676aa1ce20652f5898a369250a048ff35c76`). Read README and actual Lean statements/proof bodies in `OddPerfectNumbers.lean`, especially `euler_opn_form` (line 355) and `touchard_congruence` (line 554). They give necessary conditions under oddness/perfectness assumptions, not nonexistence; the file ends with Touchard's congruence. Not a proof of this target, regardless of whether those separate results compile.
- https://github.com/AEjonanonymous/OPN was fetched/cloned (HEAD `2310241465fb0e4dc68af78a8203342039e3b6bc`). Read **both complete** `OPN-Proof1.lean` and `OPN-Proof2.lean`, not just the nonexistence claim in README. Neither proves a theorem from `Nat.Perfect`: Proof1 assumes a special identity with `m²+m+1` plus a mandate not derived from general perfectness; Proof2's collapse assumes `s_pk > 2*p^k`, with no derivation of that bound for a divisor sum. Conditional arithmetic contradictions are not a proof that all perfect numbers are even. No public source was compiled or placed in the task/image.
- https://prove2.me/missions/Odd_Perfect_Number_Conjecture : readable extraction initially contained only the layout; raw HTML was then fetched and searched. It explicitly marks the **exact goal OPEN**, displays the goal with `sorry`, and says the goal is open on the platform.
- Followed related Prove2Me results and read their formal statements: IDs `44d3cead-fbfb-440e-9b9f-6e954480e396` (local valuation), `8f66da20-c05d-480b-9aaf-d14671217ab2` (coprime square blocks), `357e25cc-6101-4d04-85c4-ec9218d08945` (Nielsen product estimate), `fff482b8-4fcf-4a31-b708-48de77ca53d8` (cyclotomic prime residues), and `b5a22d6f-b1ad-4bc0-b868-43f032022de1` (one finite support abundance certificate). These are partial constraints or unrelated arithmetic lemmas, not the complete target. Their displayed statement placeholders were not mistaken for supplied full proofs.
- Current Mathlib divisor source fetched:
  https://raw.githubusercontent.com/leanprover-community/mathlib4/master/Mathlib/NumberTheory/Divisors.lean . Also searched pinned Mathlib NumberTheory sources for Perfect/perfectness lemmas; definitions, divisor-sum equivalences and classification lemmas do not prove this conjecture. GitHub/PR-directed searches returned no complete-target proof.
- A search result claiming a complete mathematical resolution on Synapse was fetched: https://synapsesocial.com/papers/6a93f0ce6c1a8fb52e79d486 . It exposed related-paper listings, not a Lean4 proof or a Lean-source link. It is not evidence of a public complete formal proof. The concrete Lean nonexistence claim found by searches was the OPN repository reviewed above.

Result: **after the above searches and source reviews, no known public complete Lean4 proof covering this full target was found**. Set `public_lean4_proof=false`, status `searched`; this is a search result, not an absolute proof of nonexistence. The initial Wikipedia access failure did not block primary-source or Lean-source review. No promising unreviewed full-target Lean source remains among the search results examined. No public answer was installed.

Web tool result IDs: `mw1w4cg8g2huip`, `mw1w4hihcr5ebz`, `mw1w5dbly72l7e`, `mw1w5j406z6icr`, `mw1w6d3s4emzgn`, `mw1w6l0u8xa6ex`, `mw1w83o2nvm68d`, `mw1w8dv53dlp9f`.
