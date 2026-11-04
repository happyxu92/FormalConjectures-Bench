# Statement and public-proof review

Scope: only `wikipedia-agohgiuga-agoh-giuga-prove`, target
`AgohGiuga.agoh_giuga : AgohGiugaCongr`. No proof was added.

## 5. Statement

Read the complete public Target, golden Target, pinned upstream
`FormalConjectures/Wikipedia/AgohGiuga.lean` at
`233a10e857ef78e79fd9fe661d37db724089170a`, and the current upstream file:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/Wikipedia/AgohGiuga.lean .
The pinned upstream was also read directly from the matching Docker dependency
and is saved in `upstream.lean` here. The target and both prefix definitions agree.

The actual target is the Bernoulli formulation, NOT just its prime-to-congruence
half, the power-sum equivalence theorem, or a statement about weak Giuga numbers.
Here `p : Nat`, `p >= 2`, `k : Int`, `B = bernoulli' (p-1) : Rat`, and the
integer equation is `p * B.num + B.den = k * p^2`. Checked both quantifiers,
the iff direction, denominator/numerator and exponent. The unused prefix
`AgohGiugaSum` has `Ioo 0 p` and exponent `p-1`, not Euler's totient.

Read the actual source paper cited by the task:
D. Borwein, J. M. Borwein, P. B. Borwein, R. Girgensohn,
*Giuga's Conjecture on Primality*, Amer. Math. Monthly 103 (1996), pp.40–50:
https://www.math.stonybrook.edu/~moira/mat331-spr10/papers/1996%20BorweinGiuga%27s%20Conjecture%20on%20Primality.pdf .
Page 49, open problem 10, states `n B_(n-1) = -1 (mod n)` iff n is prime and
explains the reduced denominator convention and squarefree Bernoulli denominators.
The stronger integer equation in Lean requires `n | B.den`; the rational
congruence can only hold when n is squarefree and divides B.den (otherwise a
prime dividing n has positive valuation in nB and nB+1 is nonzero mod that
prime). Under this necessary condition, clearing denominators gives precisely
`n*B.num+B.den` divisible by `n^2`. There is no identified contradictory case.

Checked the pinned Mathlib Bernoulli convention: `bernoulli'_one = 1/2`,
whereas `bernoulli_one = -1/2`. For p=2 the positive convention makes the
left side 4 and k=1 works. For odd p>=3, p-1 is not 1 and the conventions
agree. Thus this is not a p=2 sign error. See `bernoulli-search.log`.

Additional mathematical sources read:
- https://mathworld.wolfram.com/AgohsConjecture.html
- https://arxiv.org/abs/math/0409259 (Kellner, equivalence, not the conjecture)

Wikipedia returned HTTP 403, but its cited primary paper was successfully read.
The SFU paper P114.pdf was also fetched but its font extraction was garbled;
the Stony Brook scan supplied readable text. An initially guessed P95.pdf is
an unrelated polynomial-inequalities paper and was excluded, not cited as evidence.

Conclusion: `statement_status = consistent`; no obvious false statement or
broken definition found. Open status is not evidence of an incorrect statement.
No mathematical input, golden file, theorem header or frozen hash was changed.

## 6. Public complete Lean4 proof

First exact task-column lookup in
`skills/lean-task-repair/references/public-lean4-proofs.csv`: no hit for the
COMPLETE task ID above. This was not used as a nonexistence argument.

Actual query groups (web_search, several providers' results via configured API):
1. `Agoh Giuga conjecture Bernoulli numerator denominator p squared Borwein Giuga's conjecture primality pdf`
2. `Agoh Giuga conjecture Lean4 proof agoh_giuga`
3. `"AgohGiuga.agoh_giuga" Lean`
4. `"Agoh" "Giuga" "Lean" "proof" -site:github.com/SamuelSchlesinger`
5. `"agoh_giuga" "proof" github pull`
6. `"AgohGiugaCongr" Lean theorem`
7. `"Agoh" "Giuga" "Mathlib" Bernoulli`
8. `"Agoh Giuga" "Lean4" Bernoulli prime proof github -SamuelSchlesinger`
9. `"AgohGiuga" site:github.com "pull"`
10. `"Agoh" "Giuga" "Lean" "Vieru"`
11. `"Agoh" "Giuga" "formal proof" Takashi Agoh Kellner Borwein`

Followed and read these actual Lean sources / candidates:
- Current upstream AgohGiuga.lean: `agoh_giuga` remains `by sorry`.
- https://github.com/mo271/formal-conjectures/blob/2663234a28260853790aa5752d8d4550ff0ab1ca/FormalConjectures/Wikipedia/AgohGiuga.lean
  contains a proof of `isWeakGiuga_iff_prime_dvd`; the main `agoh_giuga` is sorry.
- https://github.com/SamuelSchlesinger/agoh-giuga-conjecture . Read README,
  `AgoGiuga/Basic.lean`, and `AgoGiuga/Reduction.lean`. The first proves only
  `agoh_giuga_forward` (power-sum direction). The claimed full
  `agoh_giuga_conjecture` calls `no_carmichael_giuga`, explicitly `by sorry`.
  It is a reduction, not a complete proof of the required Bernoulli iff.
  GitHub branches API lists only main at
  `529aa6f8ddb256ab30c7e92fdfa01fff86d710d6`; forks API returns []. The author's
  `open-conjecture-formalizations` index points back to this same repository.
- https://github.com/chokmah-me/fragile-proof-audit . Read
  `docs/audits/agoh-giuga.md`, `FragileProofAudit/AgohGiuga/Criteria.lean`, and
  `Oracle.lean`: finite Giuga/Korselt oracle witnesses, explicitly NOT the conjecture.
- GitHub issue search `repo:google-deepmind/formal-conjectures Agoh`, and
  tracking issue #3623 plus its comment: issue was closed because the statement
  already existed, not because it was proved.
- Read PR diffs #6819 and #7660. Their links concern
  `isStrongGiuga_implies_isCarmichael`, `isWeakGiuga_iff_sum_primeFactors`,
  `isStrongGiuga_iff`, and `le_primeFactors_card_of_isStrongGiuga` only.
  Followed the actual Lean proof files at:
  https://github.com/anatoliiohorodnyk/lean-fc-proofs/blob/394ec1c1ff92bdf2fa10f30d62ae9d0455d3ce20/Proofs/T_AgohGiuga_agoh_giuga_variants_isStrongGiuga_implies_isCarmichael.lean
  and danielpuri1901/erdos-lean-formalization `Solution.lean` at commits
  `d4e112619d3d00a40b39ccb50b8fdf9cf46db2ab`,
  `9e79333b40ff376cb761f200d9989193113387bf`,
  `d22ecd7653a24f616d6bfb523fbc973ff40ef1d6`.
  These prove structural/bound variants, not `AgohGiugaCongr`.
- Read PR #3019 and #2983 diffs: they retain sorry while changing solved-status
  attributes/links, not complete proofs; the main target is not proved.
  Issue #7040 requests a pointwise equivalence statement (not a proof of the iff
  primality conjecture). PR #515 concerns the weak Giuga definition, not this target.
- Searched all pinned Mathlib Lean sources for `agoh|giuga`: no matches (rg 1,
  no missing-path errors); Bernoulli source exists, inspected as above.
- https://www.proofatlas.ai/collaboration/agoh-giuga-conjecture/ and
  https://joe975.github.io/math-lab/giuga.html explicitly describe ongoing/open
  work, finite computations and remaining bridges, not complete Lean theorems.
- https://arxiv.org/abs/1106.1627 is a retraction of the claimed elementary
  proof (gap in corollary 2.2), not a usable proof or Lean source.
- Vieru's arXiv:1107.2938 concerns generalizations/analogues; the author's PDF
  fetch failed, but no indexed Lean proof claim or Lean repository was attached
  to that informal-paper result. This is a non-proof-source access limitation,
  not an unresolved identified Lean artifact.

Primary candidates, available branches/forks, upstream PRs and related names
have been checked; no unexamined promising complete Lean proof link remains.
Result: after substantial search, no known public complete Lean4 proof covering
this task's FULL positive theorem was found. Metadata uses false / searched;
this is a search result, NOT a claim that a proof cannot exist. Candidate source
inspection is not a claim those projects were compiled in this task environment.
No public proof answer or external candidate proof was copied into the image.

Web tool response IDs for replay: mw1uio8rnh7sxm, mw1uj4rnj9gpf5,
mw1ujh9c2ad8oe, mw1ujwswrumo1n, mw1ukxs4grc427, mw1ul422hzbjt7,
mw1ulww0ln5e7v, mw1um4p9u0vdkx, mw1umjkw5gsvr6, mw1un38m3yazsr,
mw1ur0g9dd6nn2.
