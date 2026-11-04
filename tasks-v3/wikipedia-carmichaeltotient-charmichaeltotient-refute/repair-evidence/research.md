# Statement and public-proof inspection

Task: `wikipedia-carmichaeltotient-charmichaeltotient-refute`.

## 5. Statement fidelity

Read the complete public/golden Target and the pinned upstream file:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/CarmichaelTotient.lean

The task is intentionally the **negation** of upstream `CarmichaelTotient.charmichaelTotient`: there exists a positive natural n with no distinct natural m sharing its Euler totient. The prefix defines `CarmichaelTotientFor n` as `∃ m, m ≠ n ∧ φ m = φ n`. Although m ranges over all naturals, m=0 cannot witness it for positive n, since φ(0)=0 and φ(n)>0. The explicit 0<n assumption correctly excludes the known zero edge case. The existing zero and odd-number lemmas have complete proofs and match these definitions. There are no asymptotic/analytic hypotheses or hidden real-number domain issues here. Declaring unused universes u v does not add universe parameters to this target.

Primary source read: Kevin Ford, *The distribution of totients*, introduction §1.3 and Theorem 6:
https://arxiv.org/html/1104.3264v2
https://arxiv.org/abs/1104.3264

Ford states that the existence of a totient with exactly one preimage remains open and proves only a very large lower bound on such a counterexample. Thus this task asks for the counterexample/refutation direction, not Ford's bounded positive result. Open status is not a statement error. No obvious erroneous definition or impossible-statement issue was found: `statement_status=consistent`. The original statement, golden, public Target, frozen hashes and GoldenCheck were not changed.

The linked Wikipedia page (including printable URL) returned HTTP 403. This was bypassed for mathematical source checking by reading the cited original Ford paper, not treated as proof that no public formal proof exists. MathWorld was also successfully read:
https://mathworld.wolfram.com/CarmichaelsTotientFunctionConjecture.html

## 6. Public complete Lean4 proof search

First used Python csv.DictReader to match the **entire task ID** in skill `references/public-lean4-proofs.csv`; no hit (`/tmp/ctrefute-public-csv-check.txt`). Then ran these distinct online queries:

- `"Carmichael" "totient" "Lean4" proof counterexample`
- `"CarmichaelTotient" "formal_conjectures_bench_refutation"`
- `"charmichaelTotient" proof Lean`
- `"Carmichael" totient conjecture disproof formalization Lean GitHub`
- `site:github.com/google-deepmind/formal-conjectures "CarmichaelTotient" "pull"`
- `site:github.com "CarmichaelTotient" "refutation"`
- `site:github.com "totient" "∃!" "Carmichael" Lean`
- `"Carmichael totient" "Lean" "counterexample" "proof"`

Search response IDs: `mw1ur15tw8m9rn`, `mw1ustdmnga698`. Fetched sources and actual promising Lean code, rather than relying on generated search summaries:

1. Current upstream source: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/CarmichaelTotient.lean . Main conjecture and lower-bound result still contain `sorry`. The proved zero and odd-number lemmas do not prove this refutation direction.
2. https://github.com/SamuelSchlesinger/carmichael-totient-conjecture . Read README, `CarmichaelTotient/Conjecture.lean`, `Defs.lean`, and `SmallCases.lean` from a fresh fetched clone. Main theorem `carmichael_totient_conjecture` contains `sorry`; small cases prove positive-direction nonuniqueness, not a counterexample. GitHub API `/branches` returned only main, `/forks` and `/pulls?state=all` returned empty lists.
3. https://conjectures.io/problems/carmichaeltotient-charmichaeltotient . No published attempts/pieces. Formal target contains `sorry`; it explicitly accepts proof or refutation. This is not a completed proof in either direction.
4. GitHub API `search/issues?q=repo:google-deepmind/formal-conjectures+CarmichaelTotient` returned issue 2211 and PRs 2567/3091. Read issue/comments and both actual `.diff` files. Both PRs merely replace category metadata for `carchimaelTotient_bound` while retaining `sorry`; moreover that bounded positive result is not the current negation. Neither is a complete allowed-axiom proof. Separate `search/issues?...+charmichaelTotient` returned zero items.
   - https://github.com/google-deepmind/formal-conjectures/pull/3091.diff
   - https://github.com/google-deepmind/formal-conjectures/pull/2567.diff
5. https://leanprover-community.github.io/mathlib4_docs/Mathlib/Data/Nat/Totient.html . Contains Euler totient basics, no complete counterexample. The search result for `Mathlib.NumberTheory.ArithmeticFunction.Carmichael` concerns the different Carmichael lambda function, not this conjecture.
6. Followed incidental results: https://aixiv.online/trace/66/view contains a catalog reference to the bounded upstream theorem, not a proof of this negation; https://github.com/jdb19937/carmichael/blob/main/carmichael.tex concerns constructing Carmichael pseudoprime numbers (different problem); https://arxiv.org/abs/2609.31334 is Carleson's theorem (unrelated).

Conclusion: **searched, no known public complete Lean4 proof of this exact refutation direction found**. This is not an assertion that such a proof cannot exist. No unresolved promising proof link remained after these checks. No purported public full proof was compiled, and no public answer was placed in task inputs or image. Wikipedia access restriction does not block the above available primary sources, Lean sources and proof-repository inspection.
