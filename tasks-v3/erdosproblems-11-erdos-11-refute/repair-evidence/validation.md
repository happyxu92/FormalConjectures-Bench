# Infrastructure validation

## Changes and trusted generation

Only this task was edited. Public Target, all golden files, GoldenCheck.lean, expected theorem header and frozen-prefix hash are byte-for-byte unchanged against git HEAD; `protected-hashes.json` records the checked files. No answer supplied.

Instruction source search now explicitly lists `/app`, `/opt/formal-conjectures`, `/opt/formal-conjectures/.lake/packages`. Actual ubuntu `rg --glob '*.lean' '^def Squarefree|^theorem squarefree_iff'` over these three roots returned 0, including Mathlib package matches; see `search-path.log`.

Target imports exactly ProblemImports and Submission: no additional upstream module needs precompilation. Dockerfile retains its original upstream build and ends with `WORKDIR /app`, `HOME=/home/ubuntu`, `USER ubuntu`, `RUN lake build +FormalConjecturesBench.Target`. The successful local Harbor image build exercises this last RUN (history saved).

Unicode skill command (also rerun after checker modifications):
`python3 /root/FormalConjectures-Bench/skills/lean-task-repair/scripts/check_unicode_header.py /root/FormalConjectures-Bench/tasks-v3/erdosproblems-11-erdos-11-refute`
Exit 0, `case=no_issue`; original headers pass, modified/missing-assignment negative cases rejected.

Candidate-free Spec generation used a pre-existing trusted local dependency image, not a registry task as final acceptance. Image `sha256:0824de0f16475f1f619701869e59de4e4ce3229bfce229a5fd16f88072c37e8f`, container `fcb-erdos11-refute-spec-20261104`, network none. Copied ONLY this task's golden_env and repair-time Spec tools into `/tmp/erdos11-refute-bundle`. Invoked `bash /tmp/erdos11-refute-bundle/trusted_spec/reproduce.sh`, exit 0. Fixed absolute Lean and dependency paths, no candidate Lake environment. Source generator uses Lean parser/elaborator, obtains full type and ordered universes, restores pre-target environment, then adds a definition whose VALUE is the extracted type. No prefix definitions in this task. Independent import confirms temporary target absent and transitive axioms exactly `[propext]`; universe list empty. Generation warning for temporary sorry does not enter exported ExpectedType or dependencies.

The same generated package is delivered byte-identically in tests/trusted_spec and environment/data/checker/trusted_spec. Pinned manifest SHA256: `69a26ec84e2347c26cf4d471691b400551dd97ad69a1beee209f31d34c1e390d`. Per-input/source/artifact hashes, dependency revisions, exact Lean version/platform and reproduction command are in that manifest. AST syntax, original source bans/frozen checks and both packages' equality checked on host.

## Actual local Harbor builds

CLI help was read independently (`/tmp/erdos11-refute-{harbor,run,trial-start}-help.txt`). All runs used this local task path, agent nop (no additional pi agent), Docker, no Docker socket or extra host dependency mounts.

First run:
`harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-11-erdos-11-refute --trial-name fcb-erdos11-refute-20261104 --trials-dir /tmp/erdos11-refute-harbor --agent nop --env docker --no-delete --force-build`
Successful build/reward 0. Harbor's `--no-delete` alone removes the container while retaining image. Inspected installed Harbor Docker implementation and used its `--environment-kwarg keep_containers=true` for subsequent runs.

Second run: same arguments with trial `fcb-erdos11-refute-final-20261104`, trials dir `/tmp/erdos11-refute-harbor-final` and `--environment-kwarg keep_containers=true`. Build and both entrypoints/supplements succeeded as infrastructure tests.

Final acceptance after task metadata marking:
`harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-11-erdos-11-refute --trial-name fcb-erdos11-refute-accept-20261104 --trials-dir /tmp/erdos11-refute-harbor-accept-retry --agent nop --env docker --no-delete --force-build --environment-kwarg keep_containers=true --extra-docker-compose /tmp/erdos11-refute-own-network.yaml`

The first acceptance attempt built successfully but failed creating a Docker network because predefined pools were exhausted. Retried using ONLY this task's existing final-run network via external-network Compose overlay; no shared network deleted, and no privilege relaxation. Retry completed successfully, no exception, reward 0. Image: `sha256:161102ca1b9b84888b9fa5af60c432d6ff3208f48b768b25fc5f3d249bbd5884`, tag `fcb-erdos11-refute-accept-20261104__env-main:latest`. Container: `79ff81b23454274fcb71769cd79576227ff71a42ae23142f6393096a11f4e9b7`.

## Entry points and supplemental coverage

In the final Harbor container (restarted after Harbor stopped it), actual `bash /tests/test.sh` exited 1, wrote `/logs/verifier/reward.txt=0`; actual `docker exec -u ubuntu ... bash /app/check.sh` exited 1. Both expectedly stop at original `sorry` source rejection, not infrastructure failure. Harbor supplied /tests and /logs/verifier. Official script explicitly sets FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests; check.sh uses /opt/formal-conjectures-bench-checker. Host/container SHA256 comparison of every checker, Spec and golden file in both trees, plus public Target/config, passed (`container-hashes.json`).

Independent supplemental script `/tmp/erdos11-refute-supplement.py` invokes the actual checker functions without modifying them or relaxing formal checks. Ran in same final container:
- ubuntu, FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests: exit 0;
- ubuntu, FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker and REPAIR_CHECKER pointing to local checker: exit 0;
- root formal checker functions, which drop candidate compilation to ubuntu: exit 0.

All three actually covered:
1. Manifest/input/version/platform/artifact validation and independent ExpectedType transitive audit.
2. Original placeholder candidate compilation as ubuntu in fresh temporary project, followed by successful complete type comparison.
3. Actual target axiom audit rejects sorryAx, then independent sorry canary detects it.
4. Same-named candidate Spec source/olean, candidate .lake cache and ambient LEAN_PATH do not replace fixed trusted Spec (Lean --deps returns trusted package path).
5. Isolated negative fixture: frozen public text retained, ordinary helper `def Erdos11.Squarefree (_ : Nat) : Prop := False`, and a sorry-free proof of the altered refutation. Original textual/source/frozen checks pass; ubuntu compilation and axiom audit pass; complete type comparison rejects actual mismatch. No formal/public candidate file modified.
6. Frozen-prefix mutation and out-of-subtree Lean source are rejected by original rules.
7. Isolated copies with missing precompiled artifact, corrupted artifact and corrupted manifest explicitly fail validation; no runtime fallback generation occurs.

Final entry logs and supplemental logs are delivered alongside this document. The proof-success/reward-1 branch for the original open task was not exercised and is not claimed. All requested infrastructure paths above were actually reached; a real proof is neither required nor supplied.

## Resource ownership and cleanup

Initial resource snapshots: `/tmp/erdos11-refute-initial-containers.txt`, `/tmp/erdos11-refute-initial-images.txt`. Only exact task-specific names/labels were used to identify new resources, never a concurrent global diff. The existing generation base and all other agents'/user resources are excluded from cleanup. `cleanup.log` records post-report cleanup and explicit absence checks. A superseded failed-attempt image `sha256:a62b543b0ec90e56d94a56910f239f058bee941c4809c524e2edff0833ea0ec7` was already absent after successful retry. Build cache is deliberately untouched.
