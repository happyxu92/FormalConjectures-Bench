# Infrastructure validation

## Changes
- instruction.md explicitly searches `/app`, `/opt/formal-conjectures`, and hidden `.lake/packages`.
- Target has no extra imports beyond ProblemImports/Submission. Dockerfile now ends with `USER ubuntu` then non-ignored `RUN lake build +FormalConjecturesBench.Target` after cleanup/permissions.
- Unicode script case `no_issue`; both baseline/header checks passed, no Unicode edits.
- Both checkers retain frozen/header checks, tree confinement, banned syntax, target axiom audit and sorry canary. The old candidate-time GoldenCheck elaboration was replaced by complete type comparison to a pinned precompiled Spec. GoldenCheck.lean itself was not changed.

## Repair-time Spec generation
Reused pre-existing trusted base `greensopenproblems-26-open-prove__jsmyxgx__env-main:latest`, image `sha256:c528d69a700cd44b3f9f2f1b590d3308b3e6507fc9ab3c8ce25c6f621bb3dca7`. Its build history pins FormalConjectures commit 233a10e857ef78e79fd9fe661d37db724089170a; dependency manifest hash 5b99b5f4f807cbba67bbcd22e5e486c17d6a8d970ea218de08d05830ab350c26 and Lean version were checked.

Created Spec container `fcb-odd-perfect-refute-spec-nt40`, ID c6f584eb2a153501210df3b19f33d0a5d545a391f6aafd81113100b8dec1b674. Only golden_env plus generation sources were copied to `/tmp/odd-perfect-refute/tests`; no /app candidate or Lake config/cache was used. Ran:

```
docker exec fcb-odd-perfect-refute-spec-nt40 bash /tmp/odd-perfect-refute/tests/trusted_spec/reproduce.sh
```

Exit 0. Reproducible generator and shell commands are in each trusted_spec package. It removes the Submission import, elaborates the original full target with Lean's parser/elaborator, captures type and levelParams, restores the pre-target environment, exports only a safe definition with the captured value. The temporary target declaration is absent in the independent audit. No target proof is delivered. Existing unrelated prefix theorems remain as in golden, but neither ExpectedType nor Nat.Perfect depends on them. `collectAxioms` audits transitive dependencies; only propext, Quot.sound, Classical.choice were found. Universes []; quantified arguments [n, hn]. See generation log and package audit.log.

Both packages come from the same generation. Manifest SHA256:
`035bc1ef21be75cd802f4a253922d4510d7d3ba4bef3c010c05c485338a2bef6`.
It pins every package file, all golden inputs, toolchain/platform and dependency revisions. Original golden Target SHA256 remains `bf64c2b450cd48b749b8b63476b355a92546d1d7d9b0c727df25bf6a3662fa53`.

## Fixed verifier loading
SPEC_DIR is TESTS_DIR/trusted_spec; manifests are pinned in each checker. No generator is invoked by the verifier, and missing/corrupt artifacts fail explicitly. Direct locked Lean invocation uses fixed Spec path first, fixed trusted dependency libraries next, fresh candidate source directory last. Candidate .lake caches and LEAN_PATH overrides are not inherited. Ordinary editable helpers and ordinary imports remain allowed; no dependency whitelist/security sandbox was added. Candidate compilation runs as ubuntu. Temporary Target imports Spec before Submission and restores namespace PerfectNumbers/open Nat; original prefix declarations come only from Spec. Public Target is unchanged.

## Actual current-local-task Harbor build
CLI help was read independently, including `harbor run --help`, `harbor task --help`, `harbor task start-env --help`. Initial resources recorded before creation.

First command: `harbor run --path /root/FormalConjectures-Bench/tasks-v3/wikipedia-perfectnumbers-odd-perfect-number-conjecture-refute --agent nop --env docker --no-delete --job-name odd-perfect-refute-nt40 --jobs-dir /tmp/odd-perfect-refute-harbor-jobs`. Local Docker build succeeded, but Docker default address pools were exhausted at network creation. See harbor-address-pool-failure.txt. No shared network was removed. An isolated Compose IPAM overlay selected unused `10.253.246.0/28`. Second run with overlay succeeded; Harbor `--no-delete` retains images but still removes containers, so a third run used documented environment kwarg `keep_containers=true` after inspecting Harbor implementation (no modification to Harbor).

Final command:
```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/wikipedia-perfectnumbers-odd-perfect-number-conjecture-refute --agent nop --env docker --no-delete --ek keep_containers=true --extra-docker-compose /tmp/odd-perfect-refute.compose.yaml --job-name odd-perfect-refute-nt40-keep --jobs-dir /tmp/odd-perfect-refute-harbor-jobs
```
No registry task substitution, extra mounts, Docker socket, or privilege relaxation. Nop is not another pi agent. Final image `wikipedia-perfectnumbers-odd-per__txlzrbo__env-main:latest`, ID `sha256:a0f74514c8598764c90af327529f28f2c91334f8d451a9ddff8b6fd550d08aa2`. Harbor container `067e1e375d8c915c1e9afaa0b73d19526d099cdc4ebb758e2a415389388af6ca`, project `wikipedia-perfectnumbers-odd-per__txlzrbo__env`. Harbor stops retained containers, so restarted this same container for supplemental checks.

Harbor uploaded /tests and provided /logs/verifier. Official `/tests/test.sh` explicitly sets FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests. Local `/app/check.sh` sets FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker. Ran both actual entries in that container; both exit 1 for original sorry, official reward 0 (expected unfinished proof, not infrastructure failure). Both checkers, all golden files and all Spec package files were byte-compared against each other and host. Logs retain hashes.

## Same-container supplements
`docker exec --user ubuntu <same-ID> python3 /tmp/odd-perfect-refute.supplement.py`, exit 0. Script is retained here; it calls the actual uploaded checker's functions, not replacements. The only placeholders are in isolated fixtures to cover downstream checks.

Reached and validated:
- fixed package manifest, all input/artifact/toolchain hashes;
- independent precompiled ExpectedType and transitive axiom audit;
- ubuntu candidate compilation, original full-type comparison;
- target axiom audit actually rejects sorryAx; sorry canary succeeds;
- frozen prefix/header mutation, missing :=, out-of-tree source and non-Lean editable file rejection;
- semantic attack defines PerfectNumbers.Perfect=True and PerfectNumbers.Even=False in Submission, keeps frozen Target text/header intact, and supplies a genuine proof of the substituted proposition. It obeys existing syntax restrictions, compiles as ubuntu, and passes target axiom audit. Full trusted-type comparison actually rejects it; checker main also reaches and rejects it at this stage;
- counterfeit candidate FCBTrustedSpec.olean, candidate .lake cache, candidate ProblemImports.olean and malicious LEAN_PATH cannot replace fixed imports; dependency resolution shows `/tests/trusted_spec/FCBTrustedSpec.olean`;
- missing/corrupt precompiled .olean fails closed; before/after file hashes show no runtime generation;
- local checker copy independently loads `/opt/.../trusted_spec`, audits it, compiles the fixture, compares full type and runs canary, exit 0 (local-supplement.log).

No complete mathematical proof is asserted, and reward 1 was not expected. General external initializer/compiler sandbox attacks are outside this scoped change. No untested critical Spec/type-comparison paths remain. Public-proof search is conservatively blocked/unknown as described in research.md.

Docker cleanup is performed after repair-report.json is saved; cleanup.log records exact owned resource removal and verification. Shared base images, user resources and build caches are not deleted.
