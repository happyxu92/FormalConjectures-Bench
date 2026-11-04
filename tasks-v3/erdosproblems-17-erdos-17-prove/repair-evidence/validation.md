# Infrastructure acceptance

## Changes

- Search instructions explicitly include `/app`, `/opt/formal-conjectures`, and its hidden `.lake/packages`. In the final Harbor container, ubuntu ran the documented `rg --glob '*.lean' 'def IsPrimePow'` command successfully (exit 0; package definition found).
- Target has no extra upstream imports. Added the mandatory **final** `RUN lake build +FormalConjecturesBench.Target` after `USER ubuntu`; build succeeds with its original placeholder warning. Dependency permissions were not loosened.
- Skill Unicode script: `no_issue`, original header accepted, altered header/missing assignment rejected, both original/golden inputs and checker copies match. Reran after checker repair.
- Both checkers now load an authenticated precompiled Spec at `TESTS_DIR/trusted_spec`, construct a temporary Target sharing Spec's original prefix constants, and compare complete theorem type against the already-elaborated ExpectedType value. Frozen/source/axiom/canary checks remain. No GoldenCheck or golden/public input edits.

## Spec provenance

Precompile command:

```
docker build -t fcb-erdos17-prove:spec-20261104 /root/FormalConjectures-Bench/tasks-v3/erdosproblems-17-erdos-17-prove/environment
docker run -d --name fcb-erdos17-prove-spec-20261104 fcb-erdos17-prove:spec-20261104 sleep infinity
# Copy only tests/trusted_spec and tests/golden_env to /tmp/erdos17-generation.
docker exec -u root fcb-erdos17-prove-spec-20261104 bash /tmp/erdos17-generation/trusted_spec/reproduce.sh
```

The generation working directory does not load `/app`, candidate caches, Lake config, or Submission. It strips Submission from the trusted golden prefix, elaborates the full original declaration, extracts its actual type and ordered universe parameters, restores the pre-placeholder environment, and exports only a definition of ExpectedType. The original namespace/prefix definition is retained. Independent AuditSpec import confirms the temporary theorem is absent, ExpectedType is a proposition definition, has no sorry, and ExpectedType plus IsClusterPrime have only `[propext]` in their transitive axiom closures. Universe parameters are `[]`. Lean/platform/revisions and hashes for all golden inputs, generation/audit source, `.olean`/`.ilean` and log are in the two identical Spec manifests. Their manifest SHA256 is `fba076a5db68120cda62ad100e282c9f6cd78c663bff1cefe044e9ec09bcfbed` (pinned in both checkers).

## Actual local-task Harbor build

Read `harbor --help` and `harbor run --help` independently. First current-task build produced `erdosproblems-17-erdos-17-prove__ablsgsv__env-main:latest`, but startup failed because the host's default Docker address pools were exhausted. No existing networks were removed. A temporary task-only compose overlay selected unused `10.247.17.0/24`; no socket, host dependency mounts or privileges were added.

```
harbor run -p /root/FormalConjectures-Bench/tasks-v3/erdosproblems-17-erdos-17-prove -a nop --env docker --force-build --no-delete --ek keep_containers=true --extra-docker-compose /tmp/erdos17-compose-subnet.yaml --job-name fcb-erdos17-prove-final-20261104 --jobs-dir /tmp/erdos17-harbor-jobs -n 1
```

An earlier successful non-retained trial (`6AYUN6C`) was automatically removed by Harbor despite `--no-delete` (in this Harbor version that option alone preserves images, not containers). Reading the installed Docker backend identified `keep_containers` as the retention option; final retained trial is `c3fJ6QP`, actual project `erdosproblems-17-erdos-17-prove__c3fj6qp__env`. It was restarted after Harbor stopped it for the same-container supplements.

- Final image: `erdosproblems-17-erdos-17-prove__c3fj6qp__env-main:latest`, ID `sha256:09357defd7bd9851ffeb98ca01ab5a0cea6b4c50251692b8deb6fdd8a2a2084d`.
- Container: `a9818543cb80`, `erdosproblems-17-erdos-17-prove__c3fj6qp__env-main-1`.
- Local Dockerfile used, not an old registry task. Build history records final ubuntu Lake Target build. Precompile image was not used as final acceptance substitute.
- Harbor uploaded `/tests`; every local test/checker/Spec/golden file was byte-compared to both `/tests` and `/opt/formal-conjectures-bench-checker` snapshots, all identical.
- Harbor supplied `/logs/verifier`. Its verifier phase ran the official test script, reward 0 (expected original sorry).
- Reran `docker exec a9818543cb80 bash /tests/test.sh`: exit **1**, reward **0**, original sorry source ban. Script explicitly sets `FCB_TASK_DIR=/app`, `FCB_TESTS_DIR=/tests`.
- Ran `docker exec -u ubuntu a9818543cb80 bash /app/check.sh`: exit **1**, same original sorry source ban. Local script sets `FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker`.

Neither early exit is proof success or evidence of later branches. The original target was not solved or edited.

## Same-container supplements

`/tmp/erdos17-supplement.py` imports the actual checker module and invokes its actual functions in isolated temporary fixtures, with no checker modifications or relaxed rules. Runs as root (the candidate compiler drops to ubuntu), ubuntu, and ubuntu with local `/opt` TESTS_DIR all exited **0**, `ALL SUPPLEMENTAL CHECKS PASSED`.

Covered:

1. Fixed precompiled Spec authentication, import, definition/universe/transitive axiom audit.
2. Original placeholder fixture compiles as ubuntu, complete type comparison succeeds, target axiom audit **rejects sorryAx**, sorry canary detects it. Source sorry ban was tested separately and not disabled in the formal checker.
3. Frozen prefix modification, changed header, missing assignment, and out-of-subtree Lean source all rejected.
4. Compiled candidate namesake Spec module placed in project root and `.lake/build/lib/lean`, plus malicious ambient LEAN_PATH; dependency resolution still names the authenticated `/tests/trusted_spec/FCBTrustedSpec.olean` (or `/opt` for local run), not the impostor. Trusted printed type and full comparison unchanged.
5. **Actual same-header semantic negative:** an isolated Submission uses an existing-syntax elaboration attribute to redirect the name `IsClusterPrime` to `Hacker.IsClusterPrime := True` in set-builder elaboration. This deliberately adversarial fixture is not an allowed proof technique or an answer. Original physical Target prefix and complete theorem header are unchanged; frozen/source/tree checks pass. Candidate successfully compiles, and its axiom audit has no forbidden axioms. Its actual printed type is `(setOf Hacker.IsClusterPrime).Infinite`. The actual full-type comparison rejects it as not `FCBTrustedSpec.ExpectedType`. No new blanket source bans or plugin hardening were added.
6. Missing `.olean` and hash-corrupt `.olean` fail explicitly **before any compiler call**, do not regenerate anything, and never use a candidate replacement.

AST/TOML parsing, two-package byte identity, manifest hash validation, protected tracked-file comparisons to HEAD, and the unchanged frozen hash/header are recorded in `static-validation.json`. Public Target, both complete golden trees and both GoldenCheck files remain byte-for-byte unchanged. No incomplete theorem is counted as a solution. No full valid proof acceptance was tested or claimed.

## Resource ownership and cleanup

Before creating resources, existing Docker containers/images were recorded in `/tmp/erdos17-existing-{containers,images}.txt`. Exact created tags/IDs, rather than a global concurrent diff, are used for cleanup. Owned retained containers are the precompile container `0a9673985473` and final Harbor container `a9818543cb80`; only these and their recorded four task image tags plus the final project network are cleanup targets. Initial failed/non-retained trials had no remaining containers; a one-shot image-hash inspection container was automatically removed with `--rm`. No existing/shared base image or build cache is a deletion target. Final cleanup result is in `cleanup.log` and repair-report.json.
