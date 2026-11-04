# Infrastructure validation (not a mathematical proof)

Only this task was modified. Public Target, both golden environments,
GoldenCheck.lean, theorem header and frozen SHA256 remain unchanged.

## Ordered checks and implementation

1. `instruction.md` now explicitly searches `/app`, `/opt/formal-conjectures`,
   and `/opt/formal-conjectures/.lake/packages`. The exact three-root rg command
   was run as ubuntu in the final Harbor container, matching the package's
   `bernoulli'` definition (exit 0, `search-path.log`).
2. Target has only ProblemImports and Submission imports: no additional upstream
   precompile target is required. Added the required terminal Dockerfile
   `RUN lake build +FormalConjecturesBench.Target` after `ENV HOME` and
   `USER ubuntu`. The final Harbor build exercised this stage successfully;
   ordinary dependency permissions were not relaxed.
3. Ran `/root/FormalConjectures-Bench/skills/lean-task-repair/scripts/check_unicode_header.py`
   against the absolute task root, before and after repair: exit 0 / no_issue.
   The script checks both checker constants, original/golden inputs, unchanged
   header, altered-header rejection and missing `:=` rejection.
4. Fixed Spec, as described below. Source restrictions, frozen checks, theorem
   axiom checks and sorry canary are retained. No general import whitelist or
   compiler/plugin sandbox was added.
5–6. See `research.md`; metadata only was changed for these checks.

## Trusted Spec generation and identity

Spec generation ran in a NEW task-owned container, not a candidate environment:
`fcb-agohgiuga-prove-spec-20261104`, ID
`8deefb24c7a92c80defc6eb7d6f179229c3a02ca6596669aa25da72cc97ffa98`.
It reused the PREEXISTING trusted dependency-only image
`fcb-repair/erdosproblems-252-k-eq-four:252four-20261102-183405`
(`e21dc171550d4c49aceba963047d00d1a350ce711019cbd9cb32c4770c7a39df`),
whose history pins the same FormalConjectures revision and whose dependency
manifest matches the required Mathlib revision. This shared image is not owned
by this repair and will NOT be deleted. An initial reference to a concurrently
removed 41-task image failed before creating any resource; no registry task was
substituted. The matching existing dependency-only base was then inspected.

Only original golden input and the repair-time generator were copied into a
fresh `/tmp/agohgiuga-prove-generate/tests/` in that container. No candidate Lake
configuration, .lake cache, helper code or Submission import was used.
Generation command (exit 0):

```
docker exec fcb-agohgiuga-prove-spec-20261104 bash /tmp/agohgiuga-prove-generate/tests/trusted_spec/reproduce.sh
```

The delivered `generate.py` uses Lean parser/elaborator for the original target,
extracts `ConstantInfo.type` and ordered universe parameters, restores the old
environment (discarding the temporary placeholder theorem), and exports only
a definition whose VALUE is that type. Prefix definitions retain their real
names. No expected-type string is re-elaborated in the candidate environment.
`AuditSpec.lean` independently imports the compiled module and checks:
- temporary target is absent;
- ExpectedType is a definition of Prop, with zero external declaration binders
  and ordered universe list `[]` (the universal p and p>=2 quantifiers reside
  inside the original `AgohGiugaCongr` prefix definition);
- the transitive axiom closures of ExpectedType and BOTH original prefix
  definitions contain only propext, Classical.choice and Quot.sound.

The generation warning about sorry is from the discarded temporary theorem;
no sorryAx or temporary target remains in the delivered definition's closure.
Audit output is delivered in both packages as `audit.log`.

Toolchain: Lean 4.27.0, db93fe1608548721853390a10cd40580fe7d22ae,
x86_64-unknown-linux-gnu. FormalConjectures:
233a10e857ef78e79fd9fe661d37db724089170a; Mathlib:
a3a10db0e9d66acbebf76c5e6a135066525ac900.

SHA256:
- original golden Target: 6fc3cd24297d1e9a92114cde1b591229b59738654798f12b73cae2c003e3c39c
- generated Spec source: 8cf3aaed4ade6625d96bb131c198f1450696e1d78ad8ab5f2e68a1c11da0946c
- Spec .olean: a2ec0c0c9110ea94bfe792cd53046921dd455bc3bd2b6ae881539b81e8e6f11f
- manifest: 9291bcd9b44f4d99bdb123cd8315b047d953ace77873c499bd6de7ffe971edfe

`tests/trusted_spec/` and `environment/data/checker/trusted_spec/` are byte-identical.
The pinned manifest records all golden-file hashes, code/source/artifact hashes,
version, platform, dependency revisions and ordered universe parameters.
Both checkers validate the manifest's own pinned hash before its artifact/input
hashes and Lean/dependency-manifest compatibility. Missing artifacts fail closed;
there is no runtime generation or source-compilation fallback for Spec.

The compiler is the fixed toolchain binary. Its sanitized environment ignores
candidate LEAN_PATH / LEAN_SYSROOT. Search order is the validated SPEC_DIR,
fixed dependency libraries/toolchain, then the fresh candidate project. Trusted
Spec and its dependencies cannot be replaced by candidate same-name caches.
Candidate compilation runs as ubuntu. Normal imports are still resolved/built;
no external-import whitelist or dependency permissions scan was introduced.
The temporary Target imports Spec BEFORE Submission, uses the Spec's original
prefix definitions and retains `open scoped Nat` / `namespace AgohGiuga`.
The type checker references `_root_.FCBTrustedSpec.ExpectedType` and
`@_root_.AgohGiuga.agoh_giuga`, never the original GoldenCheck reparsing path.
GoldenCheck.lean itself was not modified.

## Local-task Harbor builds and actual entrances

Read the installed CLI help independently (`harbor --help`, `harbor run --help`,
`harbor trial start --help`) and used the trial JSON interface with agent `nop`.
No new pi agent was launched.

Initial build (local task, exit 0):
`harbor trial start -c /tmp/agohgiuga-prove-harbor-config.json`
created task-owned image tag `fcb-agohgiuga-prove-accept-20261104__env-main:latest`
and container `037d959658a3...`. An attempt to rebuild the final metadata revision
built an image but hit Docker address-pool exhaustion during network creation.
Retried using ONLY this task's already-created bridge network via
`/tmp/agohgiuga-prove-own-network.yaml`. No shared/user network was removed.

FINAL successful command (exit 0):
`harbor trial start -c /tmp/agohgiuga-prove-harbor-final2-config.json`
- local task root: /root/FormalConjectures-Bench/tasks-v3/wikipedia-agohgiuga-agoh-giuga-prove
- image: fcb-agohgiuga-prove-final2-20261104__env-main:latest
- image ID: sha256:6dcde57323d2e4005193dcd91b3e53b51e2b44aefc21ae30fa9d1cb48d2de939
- container: fcb-agohgiuga-prove-final2-20261104__env-main-1, c66b39292a53...
- Harbor reward: 0 (expected unfinished proof)

This final image was built by Harbor from the CURRENT local task Dockerfile and
context, not pulled from an old registry. Spec-generation container was not used
as final acceptance. Configs, final Docker history, Harbor logs/result and exact
resource IDs are saved here. Harbor uploaded the host `tests/` at verifier stage
and provided `/logs/verifier`. Compared every local file in tests/ and the
preinstalled checker copy to the corresponding container files: 33 hashes match,
including checker, both Spec packages, golden environments and GoldenCheck.
See `container-hashes.json`.

Ran in that SAME final Harbor container:
- `docker exec ... bash /tests/test.sh`: exit 1, reward.txt = 0.
  This entry explicitly sets FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests.
- `docker exec -u ubuntu -w /app ... bash /app/check.sh`: exit 1.
  This entry explicitly sets FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker.
Both stop at the original banned sorry; no infrastructure exception is being
reported as a proof failure.

### Independent coverage after early exit

Copied only `supplement.py` to container `/tmp`, NOT to /app or /tests, and ran:

```
docker exec fcb-agohgiuga-prove-final2-20261104__env-main-1 python3 /tmp/agohgiuga-prove-supplement.py /tests
docker exec -u ubuntu fcb-agohgiuga-prove-final2-20261104__env-main-1 python3 /tmp/agohgiuga-prove-supplement.py /opt/formal-conjectures-bench-checker
```

Both exit 0. The independent driver imports the ACTUAL checker and calls its
real functions without changing/relaxing any formal checks:
- fixed package validation with hostile candidate environment overrides;
- independently imported Spec/type/prefix transitive axiom audit;
- original placeholder fixture compilation as ubuntu;
- full original theorem type comparison: PASS;
- target axiom audit detects/rejects sorryAx: EXPECTED rejection;
- sorry canary: PASS;
- same-name local module and .lake cache cannot replace fixed Spec: PASS;
- frozen-prefix edit and out-of-bounds source: rejected;
- Submission's ordinary def `AgohGiuga.bernoulli'` cannot reinterpret the shared
  trusted prefix: compiled candidate still has the correct original type;
- REAL semantic negative with ENTIRE frozen text/header unchanged: a normal
  external test-only precompiled dependency supplies a scoped Nat name notation
  `AgohGiugaCongr => True`. Editable helper contains only its ordinary import,
  and the target proof is trivial. All original source/frozen/confinement checks
  pass; the actual candidate compiles as ubuntu and its theorem has no extra
  axioms. It has type True, while the Spec still means the original Bernoulli
  proposition. The actual full type comparison rejects with **Type mismatch**
  (not unknown-name error or a build failure). The external fixture does not
  replace Spec or any trusted dependency; this tests semantic comparison, not
  an import sandbox. No normal import rule was broadened or tightened;
- missing and hash-corrupted .olean: explicit rejection, no runtime regeneration.

All proof placeholders and the hostile external notation exist ONLY in isolated
/tmp fixtures; public Target/golden were not modified. No proof of the open
conjecture was attempted or placed in the task. The logs' final RESULTS_JSON
records each reached stage. No relevant verifier stage remains untested after
the formal entry's expected early sorry rejection. Generic plugin sandboxing,
arbitrary initializer effects and every possible external cache traversal are
outside this repair's scope and are not claimed to have been tested.

## Cleanup

The report and evidence were saved before removal. Cleanup targets only the
three named task-owned containers, three explicitly recorded task image tags,
and this task's own Harbor bridge. See `docker-cleanup.log` and the final report
for verified removal IDs. Preexisting dependency image, user containers, other
agents' images/networks, and all shared build caches are preserved.
