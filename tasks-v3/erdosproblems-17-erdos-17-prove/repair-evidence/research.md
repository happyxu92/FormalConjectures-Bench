# Statement and public-proof inspection (2026-11-04)

Task: `erdosproblems-17-erdos-17-prove`. Only the **positive infinitude** proposition is being checked, not its refutation or the separate finite 97 test. No proof answer was installed.

## 5. Statement

- Pinned source read in full: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/17.lean
- Task `environment/data/FormalConjecturesBench/Target.lean`, lines 31–45, retains the definition and fixes the positive side of the upstream yes/no question (`answer(sorry) ↔ ...`). The target asks that the set of cluster primes is infinite, not that all sufficiently large primes are cluster primes.
- Primary author source read: Christian Elsholtz, *On cluster primes*, Acta Arithmetica 109.3 (2003), pp. 281–284: https://www.math.tugraz.at/~elsholtz/WWW/papers/papers13clusteractarith.pdf . Page 281 defines odd prime p using every positive even 2r ≤ p−3, equal to q−q′ for primes q′≤q≤p, and identifies infinitude as the open question. Its upper bounds do not establish either finiteness or infinitude.
- Lean uses natural n and primes, with comparison and subtraction in integers. At positive n, the integer equality forces q₁>q₂. Including n=0 is harmless (use q₁=q₂=2 for any prime p≥2); permitting p=2 adds only a finite exceptional element and cannot change infinitude. No nonemptiness, strictness, or quantifier error found. Status: **consistent**.
- Secondary definition checked: https://mathworld.wolfram.com/ClusterPrime.html . Direct erdosproblems.com/17 access returned a Cloudflare challenge/403; the primary paper and pinned upstream source were accessible. Upstream issue https://github.com/google-deepmind/formal-conjectures/issues/196 also transcribes the original question.

## 6. Public complete Lean4 proof search

Exact CSV task-column lookup in the skill's `references/public-lean4-proofs.csv` returned no match (record: `public-csv.json`). This was not itself used as evidence of absence.

Actual multi-group web queries included:

- `"Erdos17.erdos_17" Lean proof`; `"cluster primes" "Lean" proof`; `"erdos_17" "sorry" Lean4`;
- `"cluster primes" "Lean4" github proof`; `"IsClusterPrime" Lean github`; `"erdos_17" proof pull request formal-conjectures`; `"cluster primes" formalization mathlib`;
- `"infinitely many cluster primes" "Lean"`; `"Blecksmith" "Lean"`; `site:github.com "erdos_17" "by"`; `site:github.com "cluster primes" "proof" Lean`;
- the author/paper and original problem searches used in step 5.

Followed results and exclusions:

1. Current upstream Lean source was actually read: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/17.lean . The positive main theorem remains `by sorry`; the explicit completed proof is only `isClusterPrime_97_isLeast_non_cluster`. The upper-bound variants remain placeholders and would not imply this target anyway.
2. GitHub issue/PR API searches for `"cluster primes"` and `"erdos_17"` were retrieved, including https://api.github.com/search/issues?q=repo%3Agoogle-deepmind%2Fformal-conjectures+%22cluster+primes%22 . Results were original formalization #212, original question #196, and PRs #4194/#4299. The actual patch and branch Lean source of #4194 were inspected (head 45a9fe127857f7f871a9cbb131e6546e47ae6df9); only the finite 97 test is discharged. #4299 is the merged 97 proof visible in current main, not infinitude. No full-positive-proof branch was identified.
3. https://conjectures.io/problems/erdos17-erdos-17 says one proof submitted but nothing published. The public contribution directory API was checked and contains only index.md, not Lean proof files: https://api.github.com/repos/conjectures-io/conjectures-contribution/contents/contributions/erdos-17 . Its displayed `True ↔ ...` positive goal is equivalent to our direction. An unpublished submission is not a public proof.
4. https://www.theoremdb.org/statements/P2972/ and https://theoremdb.org/records/erdos-problem-17-claim-status-20260731/ were read. Followed the apparent attempt to https://theoremdb.org/records/R1215/ : it is explicitly `open_strategy`, with zero embedded source files and no executable replay; not a proof. The generic `/record/?ref=...` page was initially only a JavaScript shell; the static `/records/R1215/` route resolved it.
5. Read https://raw.githubusercontent.com/williamjblair/lean-proofs/main/README.md : its proof index is for other problems, and its cluster-prime contribution is the upstream 97 test. Read https://api.github.com/repos/rjwalters/lean-genius/issues/38612 : this search hit is about toolchain migration, not cluster primes. Read https://raw.githubusercontent.com/Cuuper22/Erdos/main/README.md : generic solver infrastructure, not a proof of #17.
6. Searched the pinned public Mathlib source tree in the accepted container for `IsClusterPrime|cluster primes|erdos_17` (`rg` returned 1: no matches, not a path failure). Separate Mathlib/formalization web searches found no equivalent complete proof.
7. Informal `.tex` attempt links from `mehmetmars7/Erdosproblems-llm-hunter` returned 404 on raw retrieval. Its repository README was accessible and describes LLM informal attempts, not a complete Lean proof. These are not live Lean-proof leads. The `erdos.constellate.science/finding.html?n=17` aggregator had DNS failure; no proof source was identified there. Direct original-problem-site access had 403 as recorded above; this did not prevent reading the actual mathematical paper or upstream Lean source/PRs.

Result: **searched; no known public complete Lean4 proof of the retained positive infinitude goal found**. This is a bounded public search, not a proof of nonexistence. No pending credible complete-Lean-proof lead remained after the inspections above. No external proof was compiled or copied into the task.

Web tool records (retrievable in this session): `mw1sdfgjkwx1w0`, `mw1se1dyh62vpi`, `mw1se7fh7s181z`, `mw1sey0brm48zh`, `mw1sfiq02b5u5r`, `mw1sfvb4yiobex`, `mw1sggr4kmh9ea`, `mw1shesu8fvp0q`, `mw1shnajnuxfjk`, `mw1sijjls3q24o`, `mw1sj039ikmz4m`.
