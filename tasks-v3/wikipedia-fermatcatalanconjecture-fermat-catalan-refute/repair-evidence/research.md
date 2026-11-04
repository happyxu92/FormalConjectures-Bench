# Statement and public-proof review (2026-11-04)

## Actual direction and mathematical statement

Task: `wikipedia-fermatcatalanconjecture-fermat-catalan-refute`.
The actual goal is **not** the upstream positive conjecture: it is
`¬ FermatCatalanConjecture.fermatCatalanConjecture`, i.e. non-finiteness of the
set of distinct power-value triples. Producing one additional solution, or
infinitely many exponent representations of one fixed value triple, does not
prove this goal.

Read the full local golden prefix and the pinned upstream source:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/FermatCatalanConjecture.lean

Local `Target.lean` definitions (lines 37–52) require all six natural values to
be positive, coprimality of bases at distinct indices 0,1,2, the power equation,
and the real reciprocal sum over Fin 6 indices 3,4,5 strictly below 1. The image
set retains power values, not sextuples. This avoids the trivial infinitely
many exponent presentations of `1^m + 2^3 = 3^2`. The refutation header is the
deliberate paired-task negation of that precise finiteness proposition.

Source checked: https://mathworld.wolfram.com/Fermat-CatalanConjecture.html
It describes finitely many relatively prime power triples, reciprocal sum
strictly less than 1, and distinguishes fixed-exponent results. Wikipedia's
linked page and en-dash alias returned HTTP 403, so MathWorld was read as an
independent source. No obvious definition error making the target impossible
was found. An open conjecture or an intentionally reversed paired challenge
is not itself a statement mismatch. Status: `consistent`. No mathematical
input was changed.

## Public Lean4 proof search

Exact CSV lookup of the full task ID in skill references/public-lean4-proofs.csv
returned no rows. This was not treated as evidence of absence.

Actual web queries, grouped across three search calls:
- `"Fermat Catalan" "Lean" proof`
- `"fermatCatalanConjecture" Lean`
- `"Fermat-Catalan" refutation formal proof Lean4`
- `site:github.com "FermatCatalanSet"`
- `"FermatCatalanConjecture" "proof" Lean github`
- `"fermat_catalan" "sorry" Lean`
- `"Fermat Catalan" "Lean4" "infinite"`
- `"Darmon Granville" "Lean" formalization`
- `"elamaunt" "Euclids-path" "fermatCatalanConjecture"`
- `"FermatCatalanConjecture" Lean proof refute github pull request`
- `"Fermat-Catalan" "Lean" "refutation"`
- `site:github.com/google-deepmind/formal-conjectures "FermatCatalan" proof`

Search response IDs: mw1v3q35c4843l, mw1v4yy35chnzt, mw1vc7i4tflgeq.
Web summaries were used only as leads, not as proof verification.

Sources and exclusions:
1. Pinned upstream (above) and current main
   https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/FermatCatalanConjecture.lean
   were actually read. Positive conjecture and fixed-exponent Darmon–Granville
   variant still use `sorry`; neither is a proof of the present negation.
   PROOFS.md was also read; no external `formal_proof` link occurs in the target.
2. Mathlib Lean source actually read:
   https://raw.githubusercontent.com/leanprover-community/mathlib4/master/Mathlib/NumberTheory/FLT/Polynomial.lean
   `Polynomial.flt_catalan` concerns polynomials over fields and concludes
   constant degree. It does not imply this natural-number non-finiteness goal.
3. https://github.com/seewoo5/lean-poly-abc was cloned read-only into
   `/tmp/fcb-fermat-refute-poly-repo` (HEAD a0e58b7734acd4e6251a021e66af431ea59582ad).
   `LeanPolyABC/Corollaries/FltCatalan.lean` was inspected; this is also the
   polynomial analogue, not the required direction/domain. Repository branches
   were listed with `git ls-remote`; no integer-refutation branch was identified.
4. https://raw.githubusercontent.com/openai/math/main/lean/ComparatorChallenges/Catalan.lean
   was read: it imports the separate Catalan problem, not this refutation.
5. https://provetogether.ai/problems/243 and its complete accepted-submission
   listing (`next_cursor: null`) were read. The sole accepted item 257 is a
   formalization, with `solved_target_id: null`. Its actual Lean source at
   https://provetogether.ai/api/v1/submissions/257/source only defines the
   positive proposition, explicitly without proving or assuming it.
6. TheoremDB https://theoremdb.org/statements/P8/ reports the primitive
   finiteness problem unresolved, not a verified Lean proof. The FLT project
   README https://raw.githubusercontent.com/anthropics/fermats-last-theorem/main/README.md
   is about FLT; proving FLT does not prove the present infinite-solution claim.
7. Important access limitation: indexed search results point to
   https://github.com/elamaunt/Euclids-path/blob/main/EuclidsPath.lean and
   https://elamaunt.github.io/Euclids-path/en/54_OpenNeighbors/.
   Search summaries describe a refutation of a *sextuple-counting* variant,
   while retaining the canonical value-triple conjecture as open. However,
   actual GitHub/raw/prose fetches returned 404 and `git ls-remote` failed with
   an authentication/private-or-unavailable-repository error. The source could
   not be inspected, so the reported refutation is neither accepted as a proof
   nor definitively excluded on unverified snippets alone.

Conclusion: no publicly retrieved complete Lean4 proof of **this negated
value-triple finiteness proposition** was verified. Because the indexed
refutation lead was unavailable, use `public_lean4_proof = "unknown"`, status
`blocked`, not false. No public answer was added to the task.
