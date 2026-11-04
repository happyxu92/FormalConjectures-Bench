# Erdős 137 prove direction: statement and public-proof review

## Actual statement (unchanged)

`environment/data/FormalConjecturesBench/Target.lean:35-39` asks
`∀ k ≥ 3, ∀ n : ℕ, ¬ (∏ x ∈ Finset.Ioc n (n + k), x).Powerful`.
This is the universal **non-powerful** direction, not an existence/counterexample task,
not the perfect-power variant, and not a finiteness-only variant.

Read the entire pinned upstream file and `FormalConjecturesForMathlib/Data/Nat/Full.lean`:
- https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/137.lean
- https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjecturesForMathlib/Data/Nat/Full.lean

Pinned upstream uses `answer(sorry) ↔` this very proposition. `Full k n` requires
`p^k ∣ n` for all `p ∈ n.primeFactors`; `Powerful = (2).Full`.
Here `Ioc n (n+k)` consists of exactly the k positive integers n+1,...,n+k,
including the n=0 endpoint case. Thus the product is nonzero and the convention
on primeFactors of 0 is irrelevant. k≥3 excludes the known two-term examples.
No task-local prefix definitions, hidden parameters, rounding or asymptotic
qualifiers occur. No obvious mathematical defect was found; status consistent.
Open is not a defect and no truth/proof claim is made.

## Original literature/source cross-check

Direct source https://www.erdosproblems.com/137 and its /latex/137, /history/137
and forum thread variants returned Cloudflare/HTTP 403. Search indexing supplied
the problem wording and open classification. An independent primary source was read:
Terence Tao, *Products of consecutive integers with unusual anatomy*,
https://arxiv.org/html/2603.27990v3, §1.2 (26 September 2026).
It explicitly states that the Erdős–Selfridge conjecture that very bad intervals
have length at most two remains open, citing Problem #137; its definition of
very bad is exactly a powerful product. §1 starts with N≥0, matching this task.
Theorem 1.8 is an asymptotic density result, not the universal claim.

Current upstream main was also read. It now phrases the question existentially,
`∃ k ≥ 3, ∃ n, ...Powerful`, with `sorry`. That change is not imported into this
pinned prove-direction task and is not evidence of a defect in this task.
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/137.lean

## Public Lean4 proof search

Exact CSV lookup first: task column equal to
`erdosproblems-137-erdos-137-prove` in skill references/public-lean4-proofs.csv:
zero matches. This was not treated as a nonexistence result.

Web searches (multiple groups; response IDs available in session):
- `Erdos problem 137 product consecutive integers powerful numbers conjecture`
- `site.erdosproblems.com/137 powerful`
- `Erdos 137 powerful consecutive Lean4 proof`
- `"Erdos137.erdos_137" Lean proof`
- `"erdos_137" "by" "sorry" github`
- `"137" "powerful" "Lean" proof Granville Langevin`
- `site.github.com "consecutive" "Powerful" "137"`
- `site:github.com/google-deepmind/formal-conjectures "137" proof powerful pull`
- `site:github.com/leanprover-community/mathlib4 "powerful" consecutive`
- `"Erdős 137" "formal" proof -site:theoremdb.org`
- `"Erdos137" Lean proof fork branch`

Inspected promising result:
https://github.com/scottdhughes/erdos137 at
3027d9add77a1f2b203977501987c7def955475d. Read README, repository tree,
`Erdos137/Finiteness.lean`, `CombinedSplice.lean`, and base definitions.
- `erdos137_eventually_not_powerful` and `erdos137_finite` explicitly assume
  `hRadLB : RadLB k` and prove eventual non-powerfulness/finiteness only.
- `abstract_prime_sqfree_high_splice` assumes coverage, a prime-on-range
  input, a squarefree-capacity input, and a high-range non-powerfulness input.
- README explicitly says abc, Mertens, BHP and Pandey inputs are not formalized.
Even if its conditional theorems have zero sorry and only standard axioms,
they do not establish this task's unconditional universal statement.
No public proof was copied into task sources or the image.

Other leads checked:
- FormalConjectures issue https://github.com/google-deepmind/formal-conjectures/issues/372
  and current/pinned upstream both retain an open problem; current source has sorry.
- FormalConjectures generated docs / public dataset matches are statements, not proofs.
- https://raw.githubusercontent.com/openai/math/main/lean/docs/137.md was read;
  it is about one-tape time simulation in space, unrelated numbering.
- arXiv:2609.25011 concerns the different Erdős–Mollin–Walsh conjecture and a
  bounded computation, not this universal product claim.
- TheoremDB R1198 was read: it records unresolved status and no executable replay.
- Mathlib search found no matching full result; results on two consecutive
  powerful numbers / Problem 367 are not this k≥3 product theorem.

Limitations: source/forum Cloudflare 403; GitHub branches/forks/comment API
requests returned rate-limit 403. `git ls-remote --heads` for the promising
repository succeeded: main plus temp-pari-binary-transfer,
temp-pari-source-run, and temp-pari-transfer-run-2. These transfer branches and
inaccessible forum/fork/comment material were not fully audited. Consequently the metadata is conservatively
`public_lean4_proof="unknown"`, status `blocked`, not false. Substantial
search found no verified full proof for this direction, but coverage gaps remain.
No candidate proof was compiled or claimed to prove the target.
