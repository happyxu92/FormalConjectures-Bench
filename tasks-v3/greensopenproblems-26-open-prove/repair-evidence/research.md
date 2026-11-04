# Statement and public-proof checks

## Actual target (positive direction)

`Green26.green_26.variants.open` asserts: for every prime p there is a natural
constant C (depending on p, not n) such that the sum of any C linear images of
{0,1}^n equals (ZMod p)^n, for every n. The task is not the p=3 result,
and is not the negation of the all-primes conjecture.

Read the entire prefix: F is `Fin n → ZMod p`; StandardCube requires each
coordinate to be 0 or 1; IsCube is an image under a linear automorphism.
The pointwise finite sum is the Minkowski sum. The n=0 case is compatible
with the zero-dimensional group, and p is constrained by `Fact p.Prime`.
There is no forced C=0 or dimension-independent restriction on the cube maps.
No obvious falsehood or definition defect was found. No mathematical input
was changed.

Sources actually read:

* Pinned upstream source:
  https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/GreensOpenProblems/26.lean
  The task retains the proposition on the right of `answer(sorry) ↔ ...`.
* Ben Green, 100 open problems, Problem 26, p.15:
  https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf#problem.26
  Downloaded PDF and read the complete Problem 26/comments/update (text lines
  690–701 in the temporary extraction). These define cubes by linear images,
  state the general F_p conjecture, and distinguish Yu's p=3 result.
* https://arxiv.org/abs/2510.01300 (Yang Yu): four bases for p=3,
  not the all-primes target. This is not a full Lean proof of this target.
* https://www.openproblemgarden.org/op/the_additive_basis_conjecture
  Same finite-vector-space additive-basis conjecture, with C depending on p.

Conclusion: `statement_status = consistent`; this is the positive all-primes
variant, not a demand to prove the original fixed-100 p=3 theorem.

## Public complete Lean4 proof search

First precisely matched the complete task ID
`greensopenproblems-26-open-prove` in the skill's
`references/public-lean4-proofs.csv`: no row matched.

Then ran multiple online query groups (web search response IDs
`mw1tsnsjdnwlrp`, `mw1tt3j1fjufwf`, `mw1tuo76smnuwm`, `mw1u32palazi6p`):

* `"Green26.green_26.variants.open" Lean`
* `"additive basis conjecture" "Lean"`
* `"Green" "problem 26" "Lean4"`
* `site:github.com "green_26" "proof"`
* `site:github.com "Jaeger" "Lean" "basis"`
* `"Yang Yu" "additive basis" "Lean"`
* `"additive bases of vector spaces" "Lean4"`
* `site:github.com/google-deepmind/formal-conjectures/pull "26" "Green"`
* `"green_26.variants.open" proof Lean4 github`
* `"additive basis conjecture" "formalization"`
* `"additive basis conjecture" "formal proof" Lean`
* `"Green26" "Lean" proof github -site:aixiv.online`
* `"Jaeger Linial Payan Tarsi" "Lean4"`
* `"additive basis conjecture" "formal-conjectures" proof fork`

Followed and checked the plausible leads, not just result summaries:

1. Current upstream Lean source
   https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/GreensOpenProblems/26.lean
   still has `sorry` in the exact all-primes theorem. The p=3 and logarithmic
   variants also have placeholders there. No full proof in this source.
2. Original PR https://github.com/google-deepmind/formal-conjectures/pull/2368
   and its `.diff`: introduction of statements, with `sorry`, not proofs.
   GitHub API retrieval hit rate limits; direct HTML and diff downloads
   succeeded (HTTP 200). No unresolved proof claim in this PR.
3. Search-returned issues 5005 and 1546 were retrieved by direct HTML after API
   failures. The former concerns answer-slot scoping in other Green problems;
   the latter is Green #7. Neither supplies a proof of Green26.
4. https://aixiv.online/trace/66/view was read at Green26 passages. It skims
   solved declarations green_26/yu25/alm91, quotes their statements, and calls
   green_26 a single unrefereed arXiv-note lead. It does not provide the
   complete all-primes Lean proof. Different direction/scope from this task.
5. https://github.com/plby/lean-proofs was actually cloned and searched at
   `8822f7ddef30fadbd92e1c6ab4ed897af356af5e` across its Lean and markdown files
   for Green26, additive basis/bases, Jaeger and Linial. The additive-basis
   matches concern sets of natural numbers (e.g. Erdos38/337/868/869), not
   sums of linear cubes over all prime fields. No Green26 proof found.
6. https://raw.githubusercontent.com/conjectures-io/conjectures-tasks/main/tiers/tier-1/RETIREMENTS.md
   has no Green26 proof/retirement entry; Green44's plby link is another theorem.
7. Pinned Mathlib sources were searched for Green26 and the vector-space
   additive-basis conjecture; no matching proof. Search results for Mathlib
   vector-space bases are the ordinary Module.Basis API, not this conjecture.
8. https://arxiv.org/abs/2610.13103 concerns zero-sum invariants in groups
   C_p ⊕ C_np, not a Lean proof of the all-primes, all-dimensions target.
   Number-theoretic Erdős–Turán/additive-basis results returned by generic
   searches were excluded by their different domains/statements.

No known public complete Lean4 proof of this precise positive direction was
found after these searches. This is a `searched` result, not a proof of
nonexistence. No candidate complete proof was found to compile. GitHub API
rate limits were worked around for relevant identified sources via raw files,
HTML/diff, and git clone. Search coverage cannot exhaust unindexed repositories.
No public solution was copied into this task or its image.
