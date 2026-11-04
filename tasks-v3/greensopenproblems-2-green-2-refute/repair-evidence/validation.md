# Infrastructure validation

## Repair-time Spec

Trusted golden Target SHA-256: `4ce3c4f590e58dd939b3326693e7ff9ba4200d0dce65f3af4f7d22a7f3142ba5`.
Manifest SHA-256 pinned in both checkers: `fbad60e1ebfc0ff52a5912eccb8f053cb787423b9a6479e12b72e712a93c4fd5`.
All source/artifact hashes, dependency revisions, generation-image ID, toolchain/version/platform and ordered (empty) universe list are in both identical `trusted_spec/manifest.json` files.

Generation used a new network-disabled container `green2-refute-spec-20261104`, ID `5985de64fdf3` (full ID in `resources.json`), reusing the existing pinned-dependency image `erdos1062-import-20261102__env-main:latest`, ID `sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`. Only trusted golden input and generation scripts were copied into the generation directory. Direct locked Lean and `/opt` precompiled dependencies were used, not `/app`, candidate Lake configuration or caches.

Commands: see manifest `generation_command`, delivered `generate.py` and `reproduce.sh`. Generation exit 0. A temporary theorem was elaborated with its original full declaration; its environment was restored before adding the definition whose value is the extracted type. Independent import verified no temporary theorem was exported, no universe parameters/outer binders were dropped, the value is Prop-valued, and ExpectedType plus the prefix definition transitively use only the three permitted standard axioms. See `spec-generation.log` and package `audit.log`. The temporary placeholder generates a warning, but `sorryAx` is not in any delivered expected-type dependency.

## Checker

Both checker files parse with Python AST and are byte-identical. Both Spec trees are byte-identical. Original source restrictions, frozen-file/prefix/header validation, target axiom audit and sorry canary remain called. `GoldenCheck.lean` was not modified; its old run-time expected-statement re-elaboration path is replaced by a root-qualified reference to the precompiled ExpectedType value.

The temporary target imports Spec first and Submission second. Its prefix definition is from Spec; only namespace/open context and original marker-through-end are retained. Locked Lean, sanitized Lean environment and search order `[validated Spec, trusted dependency libraries, temporary candidate]` make candidate same-name files/caches ineffective. Dependency discovery and candidate compilation use direct Lean; candidates run as ubuntu. There is no runtime Spec generation/rebuild/fallback.

## Harbor builds and entries

Read `harbor --help` and `harbor run --help` independently (saved). Built current local task, not a registry task:

```bash
harbor run -p /root/FormalConjectures-Bench/tasks-v3/greensopenproblems-2-green-2-refute \
  -a nop --job-name green2-refute-accept3-20261104 \
  --jobs-dir /tmp/green2refute-harbor --no-delete --force-build \
  --ek keep_containers=true --extra-docker-compose /tmp/green2refute-compose.yaml
```

Initial build succeeded but container startup hit exhausted Docker address pools. No old resources were deleted. A task-only Compose overlay specifying unused subnet `10.249.202.0/24` resolved it. Second run passed through verifier but `--no-delete` alone still removed its container in this Harbor version. Third run retained a stopped container using `keep_containers=true`; it was restarted for supplemental testing. The overlay changes only task-local network IPAM, no privileges or mounts.

Final Harbor image: `greensopenproblems-2-green-2-ref__rzfuzbv__env-main:latest`, ID `sha256:cd5b77953fce1a1c753822781632ea8a50ea3bd66830b35fadc580d19af10cf9`.
Final Harbor child: `greensopenproblems-2-green-2-ref__rzfuzbv__env-main-1`, ID `447501fc0cd210550e2ec0eddeb08dc4a53dc9f3db74887bf3c15f7abaffe81d`.

- Harbor nop trial: zero exceptions, reward 0; its supplied `/tests/test.sh` invoked `FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests python3 /tests/test_target.py`.
- Explicit `docker exec <child> bash /tests/test.sh`: exit 1, reward file 0; expected original-source `sorry` rejection.
- `docker exec -u ubuntu <child> bash /app/check.sh`: exit 1, same expected `sorry` rejection. This entry selects `/opt/formal-conjectures-bench-checker/trusted_spec`.
- `docker exec -u ubuntu -w /app <child> lake build +FormalConjecturesBench.Target`: exit 0 (placeholder warning only). Dockerfile's final ubuntu build remains present.
- 32 files comprising the two container checkers, two golden trees and two complete Spec packages matched host hashes. The formal test script was separately compared byte-for-byte. See `delivery-hashes.json`.
- Instruction search ran as ubuntu over all three advertised paths and found Mathlib's `def IsCoprime`, exit 0.

## Supplemental coverage in that same Harbor child

Independent `supplement.py` imports the **actual** checker, not a replacement. Run as ubuntu once with `/tests/test_target.py` and `FCB_TESTS_DIR=/tests`, and again with the installed `/opt` checker and matching test directory. Both exit 0; see `supplement-formal.log` and `supplement-local.log`.

Covered:

1. Original frozen prefix/header accepted; changed frozen prefix, changed header and removed `:=` rejected.
2. Banned placeholder source and out-of-subtree Lean source rejected.
3. Manifest/input/version/artifact loading, independent trusted-type transitive audit.
4. Ubuntu candidate build in an isolated placeholder fixture; correct full target type matches Spec.
5. Target axiom audit actually detects and rejects `sorryAx`; sorry canary actually detects it.
6. Poison same-name candidate Spec source/olean, `.lake` cached Spec and dependency olean, plus `LEAN_PATH`, `LEAN_SYSROOT` and `ELAN_TOOLCHAIN` overrides: fixed Spec is still selected, compilation/type check/audit succeed. No submitted caches are copied into verification.
7. A normal helper `def Green2.Real.log` shadows `Real.log` while the original frozen text/header is unchanged. Candidate compilation succeeds; complete type comparison then rejects it with Lean `Type mismatch`, displaying `Green2.Real.log` versus the fixed ExpectedType. This is a genuine reached semantic-negative path, not early source rejection.
8. Missing `.olean`, corrupt `.olean` and corrupt manifest each fail explicitly. Missing artifact remains missing: no runtime regeneration occurs.

A first fixture run failed only because the test expected lowercase `type mismatch` while Lean prints `Type mismatch`. The fixture assertion was corrected; no checker or mathematical-source relaxation was made. Both complete reruns pass.

No proof of the mathematical target was supplied or accepted. All required infrastructure branches were covered using the isolated placeholder fixture; success of axiom/type acceptance for a real proof is not claimed.

## Resource accounting

Only the named containers/images from these specific generation/Harbor runs are owned by this repair. Initial all-resource snapshots were recorded before starting. `resources.json` lists exact owned identifiers; cleanup is recorded in `docker-cleanup.log` and the final report. Shared base images and build cache are never removed.
