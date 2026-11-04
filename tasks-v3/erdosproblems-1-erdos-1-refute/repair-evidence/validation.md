# erdosproblems-1-erdos-1-refute repair validation

## Scope and immutable inputs

Only this task was changed. No proof was installed. Public Target, all golden files, frozen prefix/hash/header, and both GoldenCheck.lean files are unchanged. `repair-report.json` is not copied into the environment.

## Checks 1–3

- Instruction explicitly searches `/app`, `/opt/formal-conjectures`, and `/opt/formal-conjectures/.lake/packages`.
- The command was exercised inside the matching Docker environment and final Harbor container with the search term `theorem card_powerset`. Exit 0; `Mathlib/Data/Finset/Powerset.lean` was found (see `search-final.log`). No inaccessible-path diagnostic.
- Target imports only ProblemImports and the local Submission. No extra upstream module needs precompilation. Dockerfile now ends with `RUN lake build +FormalConjecturesBench.Target` after `USER ubuntu`, HOME, final copying/permissions. Final image built this layer; independent ubuntu build exited 0 (`final-ubuntu-build.log`).
- The mandated Unicode script exited 0: `case=no_issue`, original header accepted, modified header and missing `:=` rejected, copies match. No surrogate issue. See `unicode.json` (pre-repair check) and `/tmp/erdos1-refute-unicode-final.json` (post-repair check).

## Trusted Spec generation and identity

- Generation base was the pre-existing, locally trusted image `fcb-local/erdosproblems-1-least-n-5:cache-smoke`, ID `sha256:0824de0f16475f1f619701869e59de4e4ce3229bfce229a5fd16f88072c37e8f`, using the same Lean 4.27.0, platform x86_64, pinned Formal Conjectures revision and dependency manifest. Its image was reused, not modified or claimed for cleanup.
- New isolated generation container: `fcb-erdos1-refute-spec-20261104`, network none. Original golden and this task's generator package alone were copied into `/tmp/erdos1-refute-bundle`. Command: `docker exec fcb-erdos1-refute-spec-20261104 bash /tmp/erdos1-refute-bundle/trusted_spec/reproduce.sh`. Exit 0. An initial detached doc-comment/parser error was diagnosed and fixed in the generator before successful generation.
- `generate.py` removes the Submission import, preserves prefix definitions and original namespaces, elaborates the original full target, takes its `ConstantInfo.type` and ordered `levelParams`, restores the original environment, and compiles the type expression as the value of `FCBTrustedSpec.ExpectedType`. No regex-built type or new axiom. The temporary theorem is absent from the compiled module.
- Independent audit imports the compiled module, verifies ExpectedType is a Prop-valued definition, verifies zero universe parameters, and traverses its and `Erdos1.IsSumDistinctSet`'s complete axiom dependencies. Only `propext`, `Classical.choice`, `Quot.sound`; no sorryAx. The extraction warning comes from the temporary, unexported original placeholder, not from ExpectedType's dependency graph.
- Original golden Target SHA256: `217475c0381df033e188f2e080eb683d43a26a341d9ab79e8fa7f3f3deae6a2a`.
- Both packages are identical. Their manifest pins every source/generator/audit/artifact, all golden input hashes, dependency revisions, platform/version and universe order. Manifest SHA256: `498b5c1fcdbab44688ef2bc7c70382156d4866ba13788de3600b146c6d2fdbe6`. See `tests/trusted_spec/manifest.json` for individual `.olean` / `.ilean` hashes.

## Checker changes

Both checkers retain original source restrictions, frozen checks, axiom policy and canary. They load only `SPEC_DIR = TESTS_DIR / "trusted_spec"`, require the pinned manifest/artifact/input/version hashes, and never generate or compile the Spec at runtime. A fixed absolute Lean binary and clean environment load verified Spec and trusted dependency libraries before candidate modules. No candidate Lake config or caches participate in Spec loading. Normal provided dependency imports and recursively compiled editable helper modules remain available; no new import whitelist or broader sandbox policy was added.

The temporary verification Target imports Spec first, then Submission, uses Spec's original prefix constants, and retains original namespace/scoped context. Only the temporary copy is transformed. Candidate compilation always drops to ubuntu. Full type comparison uses an `example : _root_.FCBTrustedSpec.ExpectedType := @_root_.Erdos1.formal_conjectures_bench_refutation`, not GoldenCheck or reparsed expected mathematics. Static AST checks passed for both checkers.

## Actual Harbor acceptance

Read `harbor --help`, `harbor task start-env --help` and `harbor trial start --help` independently. Used nop (not another proving agent). Commands used absolute current task paths, local Docker build context and no socket or extra host dependency mounts:

```
harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-1-erdos-1-refute --trial-name fcb-erdos1-refute-final2-20261104 --trials-dir /tmp/erdos1-refute-harbor --agent nop --env docker --no-delete --force-build --environment-kwarg keep_containers=true --extra-docker-compose /tmp/erdos1-refute-network.json
```

Initial local Harbor builds also passed. `--no-delete` alone removes containers on this CLI; `keep_containers=true` was needed for supplementary testing. A redundant final rebuild after metadata updates encountered exhausted default Docker address pools, not a Lean/build failure (`harbor-final.log` includes successful cached local build). Resolved by a Compose network-only overlay reusing this task's already-owned `fcb-erdos1-refute-verify-20261104__env_default` network. No unrelated network/container was touched; no privileges added.

Final image: `fcb-erdos1-refute-final2-20261104__env-main:latest`, ID `sha256:9e6d7fafd4a644e4b7bb8432f94c545141fffb9982ef6b5e045f0d1014f0d3f3`. Container ID `72676fcaebd8e31995357be4660bee505f5d7a69742a56d6a2eee465f8027356`.

Harbor uploaded `/tests` in verifier phase. In-container SHA256 values of BOTH checker copies, BOTH Spec packages, all golden files and test entry files exactly match the host (`hash-validation.json`). No extra bind mount was used; container inspect records `Mounts=[]`. `/tests/test.sh` uses `FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests`.

- `docker exec --user root <container> bash /tests/test.sh`: exit 1, reward 0, expected rejection of original proof-region `sorry`.
- `docker exec --user ubuntu <container> bash /app/check.sh`: exit 1, same expected sorry rejection.
- No theorem proof completion is claimed.

### Later-path supplementation in that same FINAL Harbor container

`/tmp/erdos1-refute-supplement.py` imports the actual checker selected by FCB_TESTS_DIR and calls its actual functions. It does not modify the formal checker, Target or golden; all fixtures are temporary. Ran root/default `/tests` and ubuntu with `FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker`; both exit 0. See `final-supplement.log`, `final-supplement-local.log`, and `supplement.py`.

Covered:

1. Fixed precompiled Spec load and independent trusted-type/transitive-axiom audit.
2. Ubuntu candidate build with original placeholder kept only in isolated fixture, followed by successful full type comparison.
3. Target axiom audit detects and rejects sorryAx; actual sorry canary detects it.
4. Frozen prefix mutation and out-of-bounds source both rejected.
5. An allowed high-priority `LT ℝ` instance makes comparisons false; a candidate with the UNCHANGED frozen prefix/header compiles and has no forbidden axioms, but its complete type is rejected against Spec. Thus rejection actually occurs at type comparison, not at a superficial source ban.
6. Candidate same-name Spec source, corrupt same-name `.olean`, `.lake` cache, and poisoned LEAN_PATH/LEAN_SYSROOT do not replace fixed Spec. Audited type and full comparison still succeed for the original-type fixture.
7. Missing/corrupt trusted `.olean` fails clearly at load/hash validation and never regenerates it.

No complete mathematical proof fixture was constructed or needed. No proof-success reward branch is claimed. All infrastructure paths required by the skill were exercised; earlier original-sorry exits were not treated as coverage of later stages.

## Mathematical statement and public proof marking (checks 5–6)

- Read pinned upstream: https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/1.lean . This task is EXACTLY the negation of `Erdos1.erdos_1`, not its positive direction or a finite-cardinality variant.
- Read source-linked https://erdosproblems.ai/wiki/problems/additive_combinatorics/E0001 and author repository https://github.com/tadamcz/erdos1 (README). Direct erdosproblems.com /1 fetches returned a Cloudflare challenge/403; no success claimed for that page. Also read https://mathworld.wolfram.com/ErdosDistinctSubsetSumsProblem.html for the classical formulation.
- `IsSumDistinctSet` means positive naturals bounded by N and injectivity of ALL powerset sums. N, A and real C are quantified correctly; N != 0 excludes the empty interval degeneracy. Empty A at positive N is harmless for a sufficiently small C. The strict inequality is equivalent to the usual weak lower bound after shrinking C. Negating the uniform-C proposition is intentional in this refute task. No obvious false-statement/definition issue found: `statement_status=consistent`. No mathematical input changed.
- Step 6 exact CSV lookup of FULL ID `erdosproblems-1-erdos-1-refute` HIT: https://github.com/tadamcz/erdos1/blob/0e395153306f34b3829d118b85bdd704136f2843/Erdos1/Resolutions/Erdos1_219usd_38h.lean#L2419 . Per skill, public_lean4_proof=true immediately; no further proof search was required. Also read pinned source definition and final declaration: `Erdos1.erdos_1.disproof` is precisely the SAME negation, not a proof of the positive direction. No public solution source was copied into the task/image or compiled here. Collection result and URLs are evidence of availability, not local compatibility verification.

## Resources

`resources-before.txt` records pre-existing resources. `owned-resources.txt` records only this task's positively identified containers/images. Final cleanup is recorded separately in `docker-cleanup.log` and repair-report.json; the existing trusted base, shared layers/cache and all other agents/user resources are excluded from deletion.
