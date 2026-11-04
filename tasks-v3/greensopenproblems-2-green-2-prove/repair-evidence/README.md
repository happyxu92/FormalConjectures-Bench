# Repair validation: greensopenproblems-2-green-2-prove

## Infrastructure (steps 1–4)

- Added the explicit hidden packages path to instruction source search. In the final Harbor container the exact three-path rg search for `^(def|theorem) card` returned 0, with matches including Mathlib/Data/Finset/Card.lean (`def card`). No path/permission errors.
- Target imports only ProblemImports and local Submission. No extra upstream modules need precompilation. Added final Dockerfile `RUN lake build +FormalConjecturesBench.Target` after `USER ubuntu`; the clean image build completed (original sorry warning expected).
- Unicode tool: `python3 /root/FormalConjectures-Bench/skills/lean-task-repair/scripts/check_unicode_header.py /root/FormalConjectures-Bench/tasks-v3/greensopenproblems-2-green-2-prove` returned 0/no_issue before and after checker changes.
- Spec generated from unchanged golden Target, with Submission import removed, in dedicated matching Docker container fcb-green2prove-specgen-nt40 (7290bdf9a389). Generation uses Lean parser/elaborator; captures the full declaration type and universe parameters, resets environment, and exports only ExpectedType. Its type contains the full eventual quantifier, all A/n/card binders and casts. Universe parameters: [].
- Generation uses explicit pinned precompiled upstream search paths, not /app sources, candidate Lake configuration or candidate caches. `trusted_spec/reproduce.sh`, `generate.py`, generated source, audit source, olean/ilean, and audit log are delivered in two byte-identical packages. Full hashes and revisions are in their manifest. Manifest SHA256: 06ad60b8ab45ad57a0dd856a36db7025451013acd177e1ef844466585ae01efd. Golden Target SHA256: f44b16d4276c108421224e09ab68e1f6b7bebac1e4c3328c447046c45da99c25.
- Audit independently imports the compiled Spec, requires absence of temporary Green2.green_2, checks the ExpectedType definition value and universes, and recursively audits ExpectedType and maxRestrictedSumAvoidingSubsetSize: only propext, Classical.choice, Quot.sound; no sorryAx. The generation-time warning about the discarded temporary proof is not an exported dependency.
- Checker validates trusted location, pinned manifest and file/input hashes, Lean version, dependency revision manifest and architecture; missing/corrupt artifacts fail without compilation fallback. It invokes the pinned compiler with sanitized environment and Spec/dependency roots before fresh candidate source roots. Candidate caches are not copied. It compiles normal helper imports as ubuntu. Temporary Target imports Spec first, reuses its prefix definition, and preserves original namespace/open/scoped context. Full type comparison references only ExpectedType and the root-qualified candidate theorem. GoldenCheck.lean remains untouched and is no longer the comparison path. Original source/frozen checks, target axiom audit and sorry canary remain in main.

## Actual local Harbor builds and entrypoints

Commands (all task paths refer to this task, not a registry):

```
docker build -t fcb-green2prove-specbase:nt40 /root/FormalConjectures-Bench/tasks-v3/greensopenproblems-2-green-2-prove/environment
harbor run --path /root/FormalConjectures-Bench/tasks-v3/greensopenproblems-2-green-2-prove --agent nop --env docker --job-name fcb-green2prove-nt40-accept --jobs-dir /tmp/green2prove-harbor --n-concurrent 1 --no-delete
harbor run --path /root/FormalConjectures-Bench/tasks-v3/greensopenproblems-2-green-2-prove --agent nop --env docker --job-name fcb-green2prove-nt40-accept2 --jobs-dir /tmp/green2prove-harbor --n-concurrent 1 --no-delete --ek keep_containers=true
docker start e1c36b9fca0f
docker exec e1c36b9fca0f bash /tests/test.sh
docker exec --user ubuntu e1c36b9fca0f bash /app/check.sh
docker exec e1c36b9fca0f python3 /tmp/green2prove-supplement.py
docker exec --user root e1c36b9fca0f python3 /tmp/green2prove-supplement.py
```

CLI help was independently read. First run completed, then Harbor removed its container despite --no-delete. Second run used keep_containers=true and retained stopped container e1c36b9fca0f (greensopenproblems-2-green-2-pro__3jzgcqs__env-main-1). Final image ID: sha256:23f327517fd531e6befbe816eceb9a9a2236e6831a2b959f98bc4473ec9ad08a. See owned-images.txt for all three owned images. Harbor's diagnostic about its nominal hb__ image name is cosmetic: Compose built a uniquely named project image; inspect/history and all local/container content hashes were checked. No prebuilt registry task was used.

Harbor uploaded /tests and supplied /logs/verifier. Container copies of both checkers, every golden file and both Spec packages match local hashes (container-hashes.log). Formal test.sh explicitly selects FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests. check.sh selects /opt/formal-conjectures-bench-checker. Both entries returned 1 for original banned sorry, reward 0, as expected. This is not a proof success.

Supplement program invoked the unchanged checker's real functions in the same Harbor container (both ubuntu and root callers, with candidate compilation always ubuntu). Both final supplement runs returned 0:

- Spec fixed loading and recursive trusted type audit passed.
- Placeholder fixture compiled and passed complete type comparison, then target axiom audit correctly rejected sorryAx. Canary detected sorryAx.
- Ordinary helper `Green2.Real.log` shadowed the target's Real.log, leaving public frozen prefix/header intact. The isolated negative fixture compiled with an actual placeholder-free proof of its weakened goal and passed target axiom audit. Full type comparison rejected it with the logged Real.log vs Green2.Real.log mismatch.
- Frozen prefix modification and outside-editable source rejected.
- Same-name candidate Spec source/cache plus hostile inherited LEAN_PATH did not replace trusted import; --deps resolved the fixed Spec artifact.
- Missing and corrupt Spec artifacts rejected before compilation, without regeneration.

No full proof of the research theorem was constructed; formal entry's post-sorry paths were covered only through isolated fixtures, not inferred from early exit.

## Mathematical fidelity (step 5)

Read locked upstream FormalConjectures/GreensOpenProblems/2.lean and Ben Green's source https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf, Problem 2, pp. 3–4. Upstream target is answer(sorry) iff the same eventual lower bound. This task is precisely its positive direction, not the paired refutation. Prefix maximizes card over powerset subsets with Disjoint restrictedSumset A. Read pinned FormalConjecturesForMathlib/Combinatorics/Additive/RestrictedSumset.lean: S.offDiag.image (p.1+p.2), correctly enforcing distinct summands. Nat Finset sup is a finite maximum; the empty subset is eligible. Eventual n avoids small-n/log boundary problems. Natural log, real comparison and exponent 100 match the asymptotic question. Sanders/Beker lower bounds with exponent 1+c do not settle exponent 100. No obvious false-definition/statement issue found; statement_status=consistent. No mathematical inputs changed.

## Public Lean4 proof search (step 6)

Exact full ID lookup in skill CSV returned no rows. Subsequent varied web searches included:

- `"Green2.green_2" Lean proof`, `"maxRestrictedSumAvoidingSubsetSize" Lean`, `"Green problem 2" "Lean" sum avoiding`;
- `"sum-avoiding" "Lean" proof`, `"Erdős–Moser" "Lean4"`, `"green_2" "proof" "github"`, `"Adrian Beker" "Lean" sum-free`;
- `site:github.com "GreensOpenProblems/2.lean" proof`, `site:github.com "Green2" "green_2" -gist`, `site:github.com "sum-free" "Sanders" Lean`, `"Green's open problem 2" proof Lean formalization`.

Sources/lead resolution:

- Read locked and current upstream raw Lean source: target still by sorry. Current source is preserved in upstream-main.lean.
- Read https://conjectures.io/problems/green2-green-2: target wrapper has sorry, withdrawn at author's request, no published contribution. Followed its linked conjectures-io/conjectures-contribution/contributions/green-2/index.md; repository index explicitly Contributions (0), not a proof. Read linked upstream revision 7d1a8c9912747679d0093f6d1216420c33ee5ffa too.
- GitHub issue searches for exact green_2 and Green 2 found PRs #3386, #2468, #2848 and original formalization #1871. Followed all relevant claimed bound proofs. API files requests returned 403; retried successfully through patch-diff.githubusercontent.com. Read all three patches (saved here): they merely change category attributes, add no proofs, retain sorry, concern different weaker/upper bounds, and do not prove this target. These are excluded, not accepted as public proofs.
- https://aixiv.online/trace/66/view contains only a catalog list of the four auxiliary Green2 bounds, not a proof of green_2. Inspected all occurrences of the definition name in fetched trace.
- Other search hits: finite distinct subset sum inequalities, Erdős–Moser equation k=1, tournament theorem, square-sum-avoiding permutations, and an Erdős42 sum-free result do not state this uniform log^100 target. No purported complete Lean proof of this target was found in those leads.
- A conjectures.io result link resolved to Green42; arxiv:2609.31334 is Carleson's theorem, both unrelated. Green's source/author references provide mathematical bounds, not Lean4 code proving this target.

Outcome: searched, no known public complete Lean4 proof found for this positive task. This is a bounded search result, not an absolute nonexistence claim. No unverified promising proof lead remains. No public answer was inserted or compiled.

## Artifacts and cleanup

Raw temporary scripts, help and full Harbor results: /tmp/green2prove-* (own uniquely named files). Essential validation logs are saved here; trusted package hashes are in its manifest. Existing Docker resources were recorded in /tmp/green2prove-before-containers.txt and /tmp/green2prove-before-images.txt before any creation. Only explicitly owned resources in owned-images.txt and the two recorded containers are eligible for cleanup; no shared caches or other tasks' resources are claimed. Cleanup outcome is recorded in cleanup.log and repair-report.json after evidence/report persistence.
