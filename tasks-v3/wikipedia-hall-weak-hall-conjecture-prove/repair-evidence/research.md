# Mathematical and public-proof checks (2026-11-04)

## Actual task and statement fidelity

Task: `wikipedia-hall-weak-hall-conjecture-prove`.
The public Target lines 37–41 define HallIneq over **all integers** x,y, with
`y^2 ≠ x^3`, the positive real constant chosen after epsilon, and a strict
lower bound using real rpow of `|x|`. Lines 83–84 ask for every real epsilon>0
`HallConjectureExp (1/2-epsilon)`. The pinned upstream source agrees:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/Wikipedia/Hall.lean

Read the complete prefix, not only the header. Hall's stronger exponent=1/2
and Danilov's **larger** exponent=1/2+delta appear in the prefix, but neither
is the present goal. The paired refute Target (read only) negates the
universal epsilon>0 proposition; this report concerns the positive direction
only and does not modify that task.

Sources actually read:
- Everest et al., *A repulsion motif in Diophantine equations*, section 3 and
  section 4, https://eprints.whiterose.ac.uk/109022/1/siegelhallAMMformatfinalversion.pdf
  Section 3 Conjecture 1 states the equivalent logarithmic bound with a
  constant depending on epsilon; section 4 gives the power 1/2-epsilon bound.
- https://arxiv.org/abs/2609.35252 (Karsten Mueller, *Weak Hall's conjecture,
  approximation gains, and continued fractions*): equivalent asymptotic
  formulations and the conditional abc implication, not an unconditional proof.
- https://nitaj.users.lmno.cnrs.fr/abc.html (abc background).
- Wikipedia was located by searches, but direct fetch returned HTTP 403;
  the paper and upstream supplied independent readable statements.

No obvious mathematical error found. Strict > versus >= is immaterial after
shrinking the existential constant. Extending the usual positive-x formulation
to negative x causes no obstruction (the gap is at least |x|^3); x=0 is harmless
by choosing C<1 even at exponent 0, with Lean's total rpow convention. Exponents
<=0 for epsilon>=1/2 are easier integer-gap cases. These observations inspect
fidelity and boundary cases, not a proof of the open positive-exponent case.
Status: consistent. No mathematical input was changed.

## Public complete Lean4 proof search

Exact CSV lookup of the full task ID in the skill reference: no matching row
(`public-local-lookup.json`). Then three groups (11 queries) of network searches:

1. `"Hall.weak_hall_conjecture" Lean proof`, `"Hall conjecture" "Lean4"`,
   `"weak_hall_conjecture" proof github`.
2. `site:github.com "HallConjectureExp"`,
   `site:github.com "weak_hall_conjecture" "by"`,
   `site:github.com/leanprover-community/mathlib4 "Hall" conjecture square cube`,
   `"weak Hall" "Lean" proof Danilov Elkies`.
3. `site:github.com/google-deepmind/formal-conjectures/pull "Hall"`,
   `"HallConjectureExp" proof Lean fork`,
   `"Hall's conjecture" "Lean 4" "proof" -"marriage"`,
   `"Hall" "square" "cube" Lean proof github abc`.

Read and followed the following sources/candidates:
- Current upstream raw Hall.lean (same path on main): weak_hall_conjecture still
  `by sorry`. The pinned source and rendered
  https://firsching.ch/formal-conjectures/src/FormalConjectures/Wikipedia/Hall/
  likewise are statements, not proofs.
- GitHub PR search with exact weak_hall_conjecture: 0 results.
  Search with Hall.lean: PRs 7660, 3022, 2991. Read all three `.patch` URLs.
  PRs 3022/2991 merely annotate Danilov and retain `sorry`.
  PR 7660 links a genuine-looking Danilov source:
  https://raw.githubusercontent.com/danielpuri1901/erdos-lean-formalization/f58f69bace20b89f6c0fc3d47944089a2e8b63f5/Solution.lean
  Read the entire Lean source: final theorem `hall_danilov : type_of% @Hall.danilov`.
  It concerns **negation at 1/2+delta**, not this positive weak 1/2-epsilon
  theorem (nor the paired negation of weak Hall). Excluded; not compiled here.
- Also read PR 4453.patch from broad search; it is not a weak Hall proof.
- https://provetogether.ai/ledger: Corpus.WikipediaHall.hall_conjecture is the
  stronger original conjecture, explicitly marked open, not a weak Hall proof.
- https://raw.githubusercontent.com/google-deepmind/superhuman/main/leap/README.md:
  the Hall hit is Erdős 394, an unrelated Erdős–Hall combinatorial variant.
- https://raw.githubusercontent.com/theofilxeff/erdos_366/main/README.md:
  conditional square-full/cube-full bound under explicit abc, not our target.
- https://raw.githubusercontent.com/SamuelSchlesinger/open-conjecture-formalizations/main/lean-difficulty.md:
  statement/difficulty assessment of Marshall Hall, not a proof.
- Mathlib Hall/Basic.lean and arXiv:2101.00127: Hall's **marriage** theorem,
  unrelated to square–cube gaps. Local pinned Mathlib source search also found
  no HallConjectureExp or weak_hall_conjecture declaration (see mathlib-search.log).
- https://epoch.ai/frontiermath/open-problems/hall-conjecture: open problem
  discussion, not Lean proof.

Access limits: GitHub API commit history/PR endpoint was rate-limited; direct
raw Lean, GitHub web PR searches, and `.patch` downloads worked and resolved
all concrete relevant PR/proof leads. Wikipedia direct access was blocked,
but the primary paper and other sources were accessible. No unverified promising
complete-proof lead remains from the performed searches.

Conclusion: after these searches, no known public **complete Lean4 proof of
this exact positive weak Hall statement** was found. Mark `public_lean4_proof=false`,
status `searched`; this is not a claim of mathematical or absolute nonexistence.
No public proof was placed in the task or image, and no candidate proof was
compiled as an answer.

Web tool stored-response IDs (audit trail): mw1w90qrz4yq9h, mw1w9rzptduogi,
mw1w9zq7vkkobm, mw1wb91no22bzu, mw1wc4bw9izfc9, mw1wcnsc1zy7mw,
mw1wda0be43jaw, mw1wdhayr8y9g2, mw1wecw7rjk92p, mw1weu25oeh1tr,
mw1wf3mdv2ffs1.
