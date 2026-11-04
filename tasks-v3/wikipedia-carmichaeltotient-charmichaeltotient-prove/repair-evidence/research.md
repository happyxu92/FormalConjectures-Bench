# Statement and public-proof checks (2026-11-04)

## Actual direction and mathematical input

Task: `wikipedia-carmichaeltotient-charmichaeltotient-prove`, positive proof direction.
Target.lean lines 40–66 define
`CarmichaelTotientFor n := ∃ m : ℕ, m ≠ n ∧ Nat.totient m = Nat.totient n`
and request `∀ ⦃n : ℕ⦄, 0 < n → CarmichaelTotientFor n`.
The zero-case lemma and odd-n lemma in the full prefix are consistent with this definition.
The pinned upstream file was read from the clean dependency image and fetched online:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/CarmichaelTotient.lean
It contains the identical positive conjecture, marked research open, with sorry.

Primary source read: Kevin Ford, *The distribution of totients*,
https://arxiv.org/abs/1104.3264 and https://arxiv.org/html/1104.3264v2
(also the PDF). Section 1.3 defines multiplicity and states Carmichael's conjecture:
no positive totient has multiplicity one. This is equivalent to this task's goal.
Theorem 6 is only a bound on possible counterexamples, not a proof of the entire goal.
Mathlib's `Nat.totient_pos` and `totient_eq_zero` imply a witness m cannot equal zero
when n > 0, so using ℕ rather than positive naturals for m does not introduce an error.
Small n=1 has witness 2; zero is correctly excluded. No evident statement/definition error.
Secondary source read:
https://mathworld.wolfram.com/CarmichaelsTotientFunctionConjecture.html
Wikipedia direct fetch returned 403; the actual primary source and alternative reference
were accessible. No mathematical statements, golden files, or hashes were changed.

## Public Lean4 proof search

First: exact full `task` column match in the skill's
`references/public-lean4-proofs.csv`: zero matches (not a conclusion by itself).

Web search groups (OpenAI search provider; eleven distinct queries):
- `"Carmichael" "totient" "Lean4" proof`
- `"CarmichaelTotient" "charmichaelTotient"`
- `"Carmichael totient conjecture" "Lean" proof github`
- `site:github.com/google-deepmind/formal-conjectures "CarmichaelTotient" "3091"`
- `"charmichaelTotient" proof Lean github -site:conjectures.io`
- `"Carmichael" "totient" "Lean" "Ford" proof`
- `"CarmichaelTotientFor" proof`
- `"totient" "conjecture" "Lean 4" "unique"`
- `site:github.com "CarmichaelTotient" "proof" -SamuelSchlesinger`
- `site:github.com/google-deepmind/formal-conjectures/pull "Carmichael"`
- `"Carmichael totient" "formal proof" "Lean"`

Sources and candidate exclusions, with actual source inspection:

1. Upstream current main source:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/CarmichaelTotient.lean
still has sorry for the full target. Odd-n and zero lemmas do not cover all positive n.
2. https://github.com/SamuelSchlesinger/carmichael-totient-conjecture
was fetched/cloned and `CarmichaelTotient/Conjecture.lean` read in full.
Its equivalent non-unique-positive-preimage theorem ends `intro n; sorry`.
Only small cases are proved. The repository's branches endpoint listed only main;
forks endpoint returned an empty array. Author index also checked:
https://samuelschlesinger.github.io/open-conjecture-formalizations/
3. GitHub issue search API `repo:google-deepmind/formal-conjectures CarmichaelTotient`
returned PRs 2567, 3091 and issue 2211. Both PR diffs and fork branch Lean source
were fetched. They merely relabel the bounded theorem as formally solved and
retain sorry, and are not proofs of the unbounded goal (nor clean bounded proofs).
https://github.com/google-deepmind/formal-conjectures/pull/2567
https://github.com/google-deepmind/formal-conjectures/pull/3091
Issue 2211's comment only links the original statement formalization.
4. https://conjectures.io/problems/carmichaeltotient-charmichaeltotient
reports no published solution. Its linked contribution directory was checked via
GitHub API and contains only index.md, with Contributions (0):
https://raw.githubusercontent.com/conjectures-io/conjectures-contribution/main/contributions/wikipedia-carmichaeltotient-charmichaeltotient/index.md
5. Mathlib sources/docs inspected:
https://raw.githubusercontent.com/leanprover-community/mathlib4/master/Mathlib/Data/Nat/Totient.lean
https://leanprover-community.github.io/mathlib4_docs/Mathlib/NumberTheory/ArithmeticFunction/Carmichael.html
The latter is the different Carmichael lambda function. The former has totient
identities/positivity, not a complete proof of this conjecture.
6. Author Ford's https://www.ford126.web.illinois.edu/papers-ann.html was retrieved
in raw mode after readable-mode extraction failed. It links ordinary number-theory
papers, including the primary totient paper; no Lean proof was found.
7. aiXiv trace https://aixiv.online/trace/66/view mentions only the bounded theorem
and the invalid relabeling PR; the full target name does not occur.
8. Search distractors followed: https://github.com/jdb19937/carmichael is about
finding Carmichael numbers in quasipolynomial time, not totient fiber multiplicity;
https://github.com/creelie/eLhmr concerns Lehmer's different divisibility problem;
https://arxiv.org/abs/2609.31334 is about Carleson's theorem.
https://proofweave.org/publications/openai-math/024 and its linked Lean scope
https://raw.githubusercontent.com/openai/math/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/docs/024.md
concern asymptotic counts of totients, not non-uniqueness of every positive fiber.

Result: searched, no known publicly available complete Lean4 proof found for this
positive direction. This is not a claim of absolute nonexistence. All promising
proof/scaffold/PR leads above were resolved; Wikipedia's 403 is not a missing key
Lean-proof source. No external proof was installed or added to the task.

Search/fetch stored response IDs include mw1uoadbdfn9p4, mw1upk4pg33enf,
mw1uqsjmof0uog, mw1uog6m3uek4g, mw1uprap8h12gu, mw1uq2h536o3vv,
mw1urd5gnetfn5, mw1ust0ebobjgp, mw1uv94f7w7e6w.
