# erdosproblems-32-erdos-32-prove infrastructure validation

## Trusted inputs and products

Public Target, both golden copies, both GoldenCheck files, prefix hash and EXPECTED_HEADER were not changed. Golden Target SHA256: `b3d63c8b25f85a05e0e84458748ae54390c9ac0f772594a9225b763349828361`.

Spec manifest SHA256: `fa4a8d73425f772051d6801f38ff4dd9896ab3c73f76062b6f76b426fada1ee0`. Each manifest records all golden input, source, generation code and artifact hashes, exact Lean version, x86_64 platform, dependency revisions and ordered universe parameters (`[]`). Both packages are byte-identical. ExpectedType retains the existential natural-number set binder and complete conjunction, and has zero outer forall binders. The temporary target is removed before exporting the definition. The two preexisting prefix variant placeholders are retained but are not dependencies of ExpectedType or IsAdditiveComplementToPrimes. Independent import/collectAxioms audits both, allowing only propext/Classical.choice/Quot.sound.

Generation used the existing immutable matching dependency image `sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`, not a final acceptance substitute:

```
docker run -d --network none --name fcb32-prove-spec-20261104 erdos1062-import-20261102__env-main:latest sleep infinity
docker cp <task>/tests/trusted_spec fcb32-prove-spec-20261104:/tmp/erdos32-bundle/trusted_spec
docker cp <task>/tests/golden_env fcb32-prove-spec-20261104:/tmp/erdos32-bundle/golden_env
docker exec -u root fcb32-prove-spec-20261104 bash /tmp/erdos32-bundle/trusted_spec/reproduce.sh
```

No candidate Lake configuration/source/cache was in the generation import path. Lean 4.27.0 exact version and dependency lake-manifest hash (`5b99b5f4f807cbba67bbcd22e5e486c17d6a8d970ea218de08d05830ab350c26`) were checked. An initial dangling documentation-comment parser failure was corrected in the generator; final generation and independent audit exit 0.

## Local Harbor acceptance

Read `harbor --help`, `harbor run --help`, and `harbor task start-env --help` independently. Initial build succeeded but startup failed because preexisting networks exhausted Docker's default address pools. No existing network was removed. Retried with task-specific default IPAM subnet `10.253.32.0/24` in `/tmp/erdos32-network.yaml`. Second run was successful, but `--no-delete` alone still removes containers; inspected installed Harbor's keep_containers option and repeated with it enabled:

```
harbor run -p /root/FormalConjectures-Bench/tasks-v3/erdosproblems-32-erdos-32-prove -a nop --env docker --force-build --no-delete --ek keep_containers=true --extra-docker-compose /tmp/erdos32-network.yaml --job-name fcb32-prove-accept3-20261104 --jobs-dir /tmp/fcb32-prove-harbor -n 1
```

This used the current task Dockerfile/build context with its final ordinary-user `RUN lake build +FormalConjecturesBench.Target`. It reused matching local build cache, not an old registry task. Successful Harbor trial: `erdosproblems-32-erdos-32-prove__sc9hhtx`. Container `4e8f67347c2350aad1d2ee9c03dfbeb1a8c1b949a24a510ac3841dce78a0f39d`, image `sha256:4b232a2053f2d1c38cefdee8c10a3d84c5f44a1eaf9fb01e1f9af6a3806d2a39`. Container had no mounts, Docker socket, or extra host dependency. Harbor uploaded `/tests` and supplied `/logs/verifier`. After Harbor stopped the preserved container it was restarted for supplemental tests.

All 33 files under uploaded `/tests` and installed `/opt/formal-conjectures-bench-checker` match their respective current host files, including both checker, Spec and golden trees; see erdos32-container-hashes.json. Python AST parsing and package synchronization pass.

- `docker exec 4e8f67347c23 bash /tests/test.sh`: exit 1, reward 0, expected original proof `sorry` rejection. Entrypoint explicitly sets FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests.
- `docker exec -u ubuntu 4e8f67347c23 /app/check.sh`: exit 1, same expected rejection; selects /opt/formal-conjectures-bench-checker.
- `docker exec -e FCB_TASK_DIR=/app -e FCB_TESTS_DIR=/tests 4e8f67347c23 python3 /tmp/erdos32-supplement.py`: exit 0.
- Same supplemental script run as ubuntu with FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker and that checker path argument: exit 0, uid 1000.

The isolated fixture invokes actual checker functions without changing their checks. It covers fixed manifest/artifact loading, trusted type audit, candidate compilation as ubuntu, complete type equality (passes unchanged target), target axiom audit (rejects sorryAx), and sorry canary (detects sorryAx). Placeholder source is used only to reach later infrastructure paths, never as an accepted solution.

Negative tests: changed frozen prefix; changed header; missing assignment; banned proof placeholder; added source outside editable tree; same-name root/cached FCBTrustedSpec modules and hostile Lean environment variables (cannot replace the verified module); absent compiled artifact; corrupted artifact; corrupted manifest (all explicitly fail with no regeneration). A normal helper `def Erdos32.Real.log (_ : ℝ) : ℝ := 0` leaves public frozen target text untouched and passes helper syntax checks and compilation, but complete type comparison rejects its candidate proposition referencing Erdos32.Real.log instead of the fixed Real.log. See supplemental logs for actual Lean type mismatch.

Source search command executes in the matching generation and final containers, explicitly including all three instructed paths. Known package definition: `noncomputable def log (x : ℝ) : ℝ` in mathlib/Mathlib/Analysis/SpecialFunctions/Log/Basic.lean:44; exit 0, no path errors. No extra upstream imports were present in Target.

No complete proof was requested or produced. Main entrypoints intentionally stop at original sorry; supplemental tests cover the otherwise-unreached paths. Arbitrary successful proof/acceptance of the open theorem is not claimed.

## Cleanup

See cleanup.log and repair-report.json. Only explicitly recorded task-created container/image/network identities are eligible; the shared generation base image and all preexisting/other-agent resources are retained.
