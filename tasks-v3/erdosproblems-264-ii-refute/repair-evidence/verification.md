# Infrastructure validation

## Inputs and generation

- Original golden Target SHA-256: `6c66ff862b176b6c4f5a7fa145dd1adf90737487edfcf46760dd726d4e42b634` (unchanged).
- Lean: `Lean (version 4.27.0, x86_64-unknown-linux-gnu, commit db93fe1608548721853390a10cd40580fe7d22ae, Release)`.
- FormalConjectures revision: `233a10e857ef78e79fd9fe661d37db724089170a`; Mathlib: `a3a10db0e9d66acbebf76c5e6a135066525ac900`.
- Manifest SHA-256: `5e2b65129d8758507b2b6be2951d1b5097658f7af23275fa19821cb99d0fdad4`. Manifest records every golden input and package artifact hash, versions, platform and dependency manifest hash.
- `ExpectedType` has no binders/universe parameters. Lean's parser/elaborator extracts the **entire** target type; generation resets the environment before exporting a kernel-checked definition. Temporary theorem/proof and target-name children are absent. Audit traverses ExpectedType and the referenced prefix definition; only propext, Classical.choice and Quot.sound occur. The original unrelated prefix theorem parts.i retains its original sorry but is not in these transitive dependencies. No task answer was created.

Commands (task root abbreviated as TASK only in this document):

```
TASK=/root/FormalConjectures-Bench/tasks-v3/erdosproblems-264-ii-refute
docker build -t fcb-264ii-refute:spec-20261104 "$TASK/environment"
docker run -d --name fcb-264ii-refute-spec-20261104 --user root fcb-264ii-refute:spec-20261104 sleep infinity
python3 "$TASK/tests/trusted_spec/generate.py"
# Copy tests to the clean image's /tmp/264ii-tests, not a candidate Lake project.
docker exec fcb-264ii-refute-spec-20261104 bash /tmp/264ii-tests/trusted_spec/reproduce.sh
docker exec fcb-264ii-refute-spec-20261104 python3 /tmp/264ii-tests/trusted_spec/make_manifest.py
```

Build and independent import/audit exit 0. The generation LEAN_PATH contains only the generation directory and trusted compiled dependencies, not /app or candidate caches. Sources, olean, ilean, audit and generation code copied back and synchronized byte-for-byte under both trusted_spec directories. Runtime never generates/recompiles the Spec or falls back to source.

## Harbor acceptance

Independently read `harbor --help` and `harbor run --help`. First local task run succeeded with expected reward zero, but `--no-delete` alone removes its container on this Harbor version. Read DockerEnvironment's retention behavior and reran with `--ek keep_containers=true`; no harness modifications. Final run after metadata marking:

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-264-ii-refute --agent nop --env docker --no-delete --force-build --ek keep_containers=true --n-concurrent 1 --job-name fcb-264ii-refute-final-20261104 --jobs-dir /tmp/264ii-harbor-jobs
```

Exit 0; no Harbor exceptions; reward 0. Final trial: `erdosproblems-264-ii-refute__cB7XmHe`. Current local Dockerfile and task configuration used, no registry task/prebuilt substitute, Docker socket mount, extra dependency mount or privilege relaxation. Final image `erdosproblems-264-ii-refute__cb7xmhe__env-main:latest`, ID `sha256:d139d88c772d4ba72d1bb516a63fa777abb3292aa45f8c91b85af74a53206f84`; retained container `20c608e7c9a1`.

After Harbor supplied /tests and /logs/verifier, restarted this same stopped child and ran:

```
docker exec 20c608e7c9a1 bash /tests/test.sh
docker exec --user ubuntu 20c608e7c9a1 bash /app/check.sh
docker exec --user ubuntu 20c608e7c9a1 python3 /tmp/264ii-supplement.py
docker exec --user ubuntu 20c608e7c9a1 python3 /tmp/264ii-supplement.py /opt/formal-conjectures-bench-checker
```

Exit codes respectively **1, 1, 0, 0**. Both official/local entrypoints reject original sorry before later checks; reward remains 0, intentionally not a proof pass. `container-parity.json` verifies every uploaded checker, golden and Spec file against the host, both /tests and /opt. Official test.sh sets FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests; local check.sh sets /opt/formal-conjectures-bench-checker. Both use their own fixed package, not runtime cross-comparison.

## Actual supplemental paths

The independent program calls the real checker's functions; formal checker and public/golden inputs remain untouched. Placeholders appear only in isolated fixture compilation to cover downstream rejection paths.

- Spec manifest/artifacts validate and independently import/audit.
- Candidate compiles with UID 1000 (ubuntu), locked direct Lean and trusted-first import paths; no candidate Lake configuration/caches are used for trusted modules.
- Full target type matches Spec for the original mathematical target fixture.
- Target axiom audit rejects sorryAx, and sorry canary detects it.
- Frozen-prefix/header mutation and outside-subtree Lean source are rejected.
- Legal helper definition `Erdos264.Nat.factorial` changes resolution without changing original frozen text. Candidate compiles, but **complete type comparison rejects** its altered target type. This is not merely an early source-ban rejection.
- Candidate same-name Spec source/invalid olean and hostile LEAN_PATH/LEAN_SYSROOT do not replace the fixed precompiled Spec; --deps resolves the verified /tests (or /opt) artifact.
- Missing olean, corrupt olean and corrupt manifest are explicitly rejected; missing file remains absent (no regeneration).

No original proof was constructed, no successful proof branch asserted. General compiler/plugin/initializer sandboxing and arbitrary external import bans were not added or claimed.

## Static and dependency checks

AST valid; two checkers and packages identical. Header/hash/bans/axioms preserved; public Target, golden and GoldenCheck unchanged. Only the two allowed baseline imports occur, so no extra upstream precompile is needed. Dockerfile **still ends with ubuntu `RUN lake build +FormalConjecturesBench.Target`**, actually built successfully in all local/Harbor images. Instruction search explicitly includes packages; ripgrep found Mathlib's add_comm declarations there without path/permission errors.

Initial resource snapshots: `/tmp/264ii-existing-containers.log`, `/tmp/264ii-existing-images.log`. Cleanup identities and results are recorded in cleanup.log and repair-report.json.
