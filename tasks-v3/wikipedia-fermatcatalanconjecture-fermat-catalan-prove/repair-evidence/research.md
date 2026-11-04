# Statement and public-proof checks (2026-11-04)

Task: `wikipedia-fermatcatalanconjecture-fermat-catalan-prove`.
Direction checked: **prove** `FermatCatalanConjecture.fermat_catalan`, i.e. finiteness of the image of primitive positive natural-number solutions under `(a,b,c,m,n,k) ↦ (a^m,b^n,c^k)`, with varying positive exponents and real reciprocal sum strictly below 1. Not the negation and not the fixed-exponent Darmon–Granville variant.

## Statement fidelity: consistent

Read the complete public Target prefix/definitions (definitions at lines 36–48) and declaration (line 59), and pinned upstream source:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/FermatCatalanConjecture.lean

The upstream definitions agree. Positivity quantifies over all six entries; pairwise coprimality is imposed on distinct indices 0,1,2 (not on a value set that could discard repeated bases). `Finset.Icc 3 5` in `Fin 6` selects the three exponents; the reciprocals are real. The target is finite **power-value triples**, not finite exponent sextuples. Thus the arbitrary powers of the base 1 do not create a counterexample. No obvious false-statement/definition issue was found; mathematical openness is not an error.

Sources actually read:
- https://arxiv.org/html/2410.21552v1, Adam S. Sikora, *Fermat-Catalan and Tijdeman-Zagier conjectures for products*, §2: explicitly formulates finitely many `(x^n,y^m,z^k)` with positive variables, coprimality and `1/n+1/m+1/k<1`; distinguishes fixed-exponent Darmon–Granville.
- https://www.math.buffalo.edu/~asikora/research.htm (author bibliography).
- https://mathworld.wolfram.com/Fermat-CatalanConjecture.html: same finiteness and reciprocal inequality, including `1^p+2^3=3^2`.
- Original linked Wikipedia URL and en-dash URL both returned Wikimedia HTTP 403/rate-limit errors. The accessible paper and MathWorld suffice for the statement comparison.

No mathematical input, public Target, golden, frozen hash, or GoldenCheck was changed.

## Public complete Lean4 proof: unknown (no verified complete proof found)

First exact-match lookup of the full task ID in the skill's `references/public-lean4-proofs.csv`: zero rows. Repeated final exact lookup also zero rows.

Multi-group online queries actually issued:
- `"Fermat Catalan" "Lean" proof`
- `"FermatCatalanConjecture.fermat_catalan"`
- `"fermatCatalanConjecture" Lean proof github`
- `site:github.com "FermatCatalan" "by"`
- `site:github.com "fermat_catalan" proof Lean`
- `"Fermat Catalan" "Lean4" finiteness proof`
- `"Fermat-Catalan" "formal-conjectures" pull request proof`
- `"elamaunt" "Euclids-path" "Catalan"`
- `"FermatCatalanSet" proof`
- `"Fermat-Catalan" "Lean" "finiteness" Darmon Granville proof`
- `"Fermat Catalan" "Lean" "Sikora"`

Sources and promising candidates followed:
1. Pinned upstream source above, and current `main` raw source: target remains `by sorry`. Also read the distinct Darmon–Granville target, which is not this task.
2. GitHub issue search API for `repo:google-deepmind/formal-conjectures "Fermat Catalan"` returned three hits (#104, PR #2610, PR #3134). Read #104; it is a list of formalization targets, not a proof. Both apparently promising solve PRs were followed to their actual `.diff` and raw `refs/pull/<id>/head/.../FermatCatalanConjecture.lean`. Each only changes the **fixed-exponent variant's category attribute**; both the main conjecture and that variant still have `sorry`. They are not complete Lean4 proofs:
   - https://github.com/google-deepmind/formal-conjectures/pull/2610.diff
   - https://github.com/google-deepmind/formal-conjectures/pull/3134.diff
   - https://raw.githubusercontent.com/google-deepmind/formal-conjectures/refs/pull/3134/head/FormalConjectures/Wikipedia/FermatCatalanConjecture.lean
   - corresponding raw pull/2610 source.
3. Mathlib's actual Lean source was read in full:
   https://raw.githubusercontent.com/leanprover-community/mathlib4/master/Mathlib/NumberTheory/FLT/Polynomial.lean
   `Polynomial.flt_catalan` is a genuine proof about nonconstant polynomials over a field, not finiteness of natural integer power triples. Excluded by domain and conclusion, not merely by theorem name.
4. https://github.com/seewoo5/lean-poly-abc and its README: Jineon Baek/Seewoo Lee polynomial Mason–Stothers/FLT formalization, now in Mathlib; same domain mismatch, not this task.
5. https://github.com/anthropics/fermats-last-theorem (README fetched): FLT, not varying-exponent Fermat–Catalan finiteness. The regular-prime FLT search results likewise do not cover this target.
6. https://api.github.com/repos/rjwalters/lean-genius/issues/22638 and actual `research/problems/fermat-defect-one/problem.md`: a reduction/literature attempt for **Fermat defect-one**, not a proof of this conjecture.
7. https://provetogether.ai/problems/243: statement provenance calls it research-open; no source-level complete proof is presented in the fetched record. Its submissions API returned one accepted **formalization** (#257), not a proof (`solved_target_id: null`). Read https://provetogether.ai/api/v1/submissions/257/source: it defines `fermat_catalan : Prop := fermatCatalanConjecture` and explicitly says this defines an open target, not a proof. The lemmas collection was empty. https://theoremdb.org/statements/fermat-catalan-conjecture/ similarly distinguishes the open varying-exponent statement from the fixed-exponent theorem.
8. Search also indexed https://github.com/elamaunt/Euclids-path/ and `EuclidsPath.lean` / `prose/54_OpenNeighbors.md`, describing an open-neighbors discussion rather than a completed proof. However all direct repository, raw `main`/`master`, GitHub raw, and GitHub Pages attempts returned HTTP 404. Therefore this indexed lead could not be source-verified. Later GitHub API calls also hit the shared unauthenticated rate limit; raw PR sources remained accessible.

Because the indexed Euclids-path lead cannot be verified at source, metadata/report conservatively record **unknown**, not false. The search did not establish an available complete proof and does not claim that none can exist. No external proof was compiled in this task and no public answer was added.

Web retrieval IDs: mw1usiilyix638, mw1utbr5w5cy9b, mw1uxsld69z3zo, mw1uxz2nqc48je, mw1uyrtaivcatt, mw1uz0nuakqgb4, mw1v3qhnqnz0b1, mw1v40rmbxpifz, mw1v4kjdmr203d, mw1v56uwf65fkn, mw1v5fvw05ro5l, mw1v707tgqd8bi, mw1vaamir1q6gu.
