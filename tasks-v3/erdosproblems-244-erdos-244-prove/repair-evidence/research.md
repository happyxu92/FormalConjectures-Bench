# Statement and public Lean4 proof review (2026-11-04)

Task: `erdosproblems-244-erdos-244-prove`, positive direction only.

## Statement review

Read the entire golden Target and its prefix. It imports ProblemImports and the initially empty Submission; there are no task-local mathematical definitions. The actual target is
`∀ C > (1 : ℝ), 0 < { p + ⌊C ^ k⌋₊ | (p) (k) (_ : p.Prime) }.lowerDensity`.
Here `p,k : ℕ`, `p.Prime` is Nat.Prime, the floor is the natural floor, and Set.lowerDensity is the liminf of relative counts below n in ℕ. Checked the dependency's density definition (partialDensity, lowerDensity), not merely the theorem header. Since C > 1 and k is natural, C^k is positive, so natural floor agrees with integer floor. The zero exponent is intentional. No obvious domain/quantifier/sign/density-definition error was found.

Sources read:
- Pinned upstream: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/244.lean — its `answer(sorry) ↔` RHS is exactly this positive task. The separate Romanoff variant has C : ℕ and is not this task.
- Current upstream: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/244.lean — still has `sorry` for both statements.
- Yuchen Ding, *On two Romanoff type problems of Erdős*, https://arxiv.org/html/2503.22700v5, abstract and Introduction through Theorems 1.1–1.4. Explicitly formulates the same every-real-base lower-density question. Almost-everywhere, integer-base, and golden-ratio results do not settle it. The paper explains k ≥ 1 versus k ≥ 0 does not affect lower density, since P+1 has density zero.
- https://erdosproblems.ai/wiki/problems/primes/E0244 and its Romanoff/Ding claims, accessed and read in full. Same lower-density interpretation; no every-base claim.
- https://www.erdosproblems.com/244 and non-www alternative were attempted, but direct fetching hit Cloudflare/403. Search snippets and the cited paper provide the source formulation independently.

Conclusion: `statement_status = consistent`; this is the positive side of the original question, not a proof or assertion that the open question is solved. No mathematical statement was edited.

## Public proof review

First exact CSV lookup: `task == erdosproblems-244-erdos-244-prove` in the skill's references/public-lean4-proofs.csv: no match.

Web search groups actually run:
1. `Erdos problem 244 C floor powers prime positive density`; `Erdos 244 Romanoff C real greater than 1 density prime floor`.
2. `"Erdos244.erdos_244" Lean proof`; `"erdos_244" "sorry" Lean`; `"Erdos 244" "Lean" proof`.
3. `"Romanoff" "Lean4"`; `"Romanoff" "Lean" "density"`; `"erdos_244" site:github.com -google-deepmind/formal-conjectures`; `"Yuchen Ding" "Lean"`.
4. `"244" "Romanoff" "Lean" github proof`; `"244.lean" proof fork pull request`; `"Kalmár" "Lean" primes density`; `"floor" "powers" "positive lower density" "Lean"`.
5. `site:github.com/openai/math "244" "Romanoff"`; `site:github.com "erdos_244" "proof" -google-deepmind`; `"Erdos 244" formalization proof Lean fork`; `"Romanoff" site:leanprover-community.github.io/mathlib4_docs`.

Follow-up and exclusions:
- Read actual pinned and current upstream Lean source, as above: `sorry`, no complete proof.
- Read https://firsching.ch/formal-conjectures/src/FormalConjectures/ErdosProblems/%C2%AB244%C2%BB/ — generated source also contains `sorry`, including Romanoff.
- GitHub PR search https://github.com/google-deepmind/formal-conjectures/pulls?q=is%3Apr+244 returned six closed hits. The potentially relevant #2538 and #3063 were investigated via actual patch sources:
  https://patch-diff.githubusercontent.com/raw/google-deepmind/formal-conjectures/pull/2538.patch
  https://patch-diff.githubusercontent.com/raw/google-deepmind/formal-conjectures/pull/3063.patch
  Both only change the integer Romanoff variant's category attribute to claim it formally solved; their unchanged Lean theorem still ends `sorry`. They do not contain a proof, and do not cover every real C anyway. Patch copies retained here. #244 is a class-number problem, #179 is density statement infrastructure, #68 is answer annotation, #4748 is link maintenance, not matching full proofs.
- Read https://raw.githubusercontent.com/plby/lean-proofs/main/ErdosProblems/README.md and https://raw.githubusercontent.com/plby/lean-proofs/main/data/sources.yaml: no Problem 244 entry or Romanoff proof lead. Search hits for other Erdős numbers are not this statement.
- Read https://erdosproblems.ai/wiki/problems/primes/E0244/claims/1934_12_01_romanoff and /2025_03_17_ding in full: respectively integer bases and almost every base/golden ratio, informal results, not this full Lean4 target.
- Read https://www.plasma.ai/research/erdos and the above catalog; no matching full-proof link. Its general links to proof registries/collections are not evidence of a proof of this task.
- Cuuper22/Erdos is a proof-agent prototype README, not an Erdős 244 proof repository. No relevant source lead.
- Local pinned Mathlib Lean-source search for `romanoff|erdos_244` produced no matches. Online Mathlib-doc and GitHub/OpenAI/fork queries did not yield matching proof source.

Access limitations: erdosproblems.com/history/244 and /16 hit 403; GitHub API/PR-reader paths hit unauthenticated rate limits; the relevant PR search and patch contents were recovered independently. GitHub code-search page was login-only, so public search and accessible raw source/patches were used. No still-promising matching full-proof lead remained after these follow-ups. A search-provider summary asserted Romanoff had been formalized, but was not accepted as evidence; actual inspected integer-variant source/patches still contain sorry and in any event have the wrong quantifier domain.

Result: `public_lean4_proof = false`, status `searched`: after this multi-source search no known public complete Lean4 proof covering the present positive every-real-base target was found. This is a search finding, not a claim that no proof exists. No public solution was copied into the task or image, and no candidate complete proof was available to compile.
