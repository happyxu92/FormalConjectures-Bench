# Infrastructure validation

No public Target, golden input, frozen prefix hash/header, or GoldenCheck.lean was changed. No proof of the open target was supplied.

## Generation

Built the current task locally:

```
docker build --progress=plain -t fcb-three-halves-prove:spec-stage-20261104 /root/FormalConjectures-Bench/tasks-v3/books-uniformdistributionofsequences-equidistribution-isequidistributedmoduloone-three-halves-pow-prove/environment
```

Build exit 0, including the final `USER ubuntu; RUN lake build +FormalConjecturesBench.Target`. No additional upstream imports were found beyond ProblemImports; Submission is local. Original source's sorry warnings are expected here.

Created dedicated container `fcb-three-halves-prove-spec-20261104`, copied the original tests/golden input and repair-time extraction code to `/tmp/fcb-spec`, then ran:

```
docker exec fcb-three-halves-prove-spec-20261104 bash /tmp/fcb-spec/trusted_spec/reproduce.sh
```

Final generation/audit exit 0. The initial extraction's unattached target docstring caused a parser error, fixed in the repair-time generator before packaging. Generator removes only the editable helper import and target docstring before its `run_cmd`, elaborates the entire original target in a saved environment, obtains `info.type` and ordered `levelParams`, restores the pre-target environment and exports a safe definition of the expression. It never exports the temporary target proof or its auxiliary declarations; independent audit checks that. Prefix original definitions are retained. The pre-existing, unrelated accumulation lemma contains its original sorry, but collectAxioms proves it is not a dependency of ExpectedType or its referenced equidistribution definitions.

Version: Lean 4.27.0, x86_64-unknown-linux-gnu, compiler commit db93fe1608548721853390a10cd40580fe7d22ae. Dependency pins: FormalConjectures 233a10e857ef78e79fd9fe661d37db724089170a; Mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900.

Golden Target SHA256: `ad404c2c6883380dbd8c3e7918ec96ba87242db5baca280ab95accb3caa6c3c0`.
Spec olean SHA256: `1b300bdfe2f6e1cdcd249973088a2866be6045eb91c04315cf1b1ca3b5ce7441`.
Manifest SHA256 pinned in both checkers: `6d769d097e1b1391c169faa877d47569923828846041bf72ec5aa9612bf92de3`.
Full source, code and product hashes are in both synchronized `trusted_spec/manifest.json`. ExpectedType has zero outer binders and no universe parameters. Its value and both referenced prefix definitions were transitively audited to use only propext, Classical.choice and Quot.sound.

## Final local Harbor acceptance

Read `harbor --help`, `harbor run --help`, and Docker backend source to select local path, nop, no-delete, and keep_containers options. In this Harbor version no-delete preserves images but still removes containers unless keep_containers is set; keep_containers stops the container at trial completion. It was explicitly restarted for supplementary tests.

Final command (exit 0, one trial, no exception):

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/books-uniformdistributionofsequences-equidistribution-isequidistributedmoduloone-three-halves-pow-prove --agent nop --env docker --job-name fcb-three-halves-prove-finalok-20261104 --jobs-dir /tmp/fcb-three-halves-prove/harbor --no-delete --ek keep_containers=true --extra-docker-compose /tmp/fcb-three-halves-prove/compose-final-subnet.yaml -n 1
```

Only a unique explicit subnet (`10.194.67.0/28`) is supplied by the Compose overlay; no mounts, socket access or elevated permissions. Earlier attempts encountered exhausted default Docker network address pools and then a conflicting explicit subnet; inspected subnets, selected an unused subnet and retried successfully. No existing/other-agent networks were removed. Earlier local Harbor build also succeeded (`gml2pay`) and received the same supplementary validation; final acceptance after metadata updates is `lfj2uzy`.

Final image: `books-uniformdistributionofseque__lfj2uzy__env-main:latest`, ID `sha256:8be9f2e283710472a2d455767fc09512cf765d34b03bc419af637884f9232b63`.
Final container ID: `3062db3e41c1f05b6b1eba5f3b0641c1fe255cb5a7bc81e3bf779f40025affcb`.

Inside that same Harbor child:

- `bash /tests/test.sh`: exit **1**, reward **0**, expected original sorry rejection.
- `docker exec --user ubuntu ... bash /app/check.sh`: exit **1**, same expected sorry rejection.
- Independent `/tmp/fcb-three-halves-supplement.py` imports the **actual** `/tests/test_target.py`: exit **0**.
- Same program as ubuntu with `FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker`, importing that actual checker: exit **0**.
- Host/container hash audit: exit **0**, AST parse of both checkers, identical packages and all **35** checker/Spec/golden/entry/public Target file hashes matched.

Dockerfile installs only the local checker in `/opt`; Harbor verifier upload populated `/tests`. The unchanged test.sh explicitly exports `FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests`. The unchanged check.sh exports the corresponding `/opt` path. Container mount list was empty: no hidden host dependency/socket was attached. The checker takes Spec only from TESTS_DIR/trusted_spec and validates the pinned manifest, golden inputs, artifact hashes, exact compiler version, architecture and dependency manifest before import. It uses fixed compiler/dependency paths, with trusted paths before the candidate temporary project, not candidate Lake configuration/caches. It never invokes the repair generator or recompiles the Spec at runtime.

## Supplementary coverage (both entry layouts)

Actual checker functions covered:

- `load_trusted_spec`, independent `check_trusted_type`: audited ExpectedType's value, binders/universes and referenced definitions.
- `make_fresh_golden_project`: temporary Target imports Spec before helper, reuses the same prefix constants and restores namespace/scoped context.
- `check_build`: real compiler runs as ubuntu; inspected compiled target ownership. Placeholder **only in isolated downstream fixture** permitted reaching later paths.
- `check_golden_theorem_import`: original candidate full type matches the fixed ExpectedType without reparsing the proposition.
- `check_axioms`: rejects the placeholder target's sorryAx. No audit was disabled or weakened.
- `check_sorry_canary`: succeeds in detecting sorryAx.
- Frozen prefix/header/assignment mutations, frozen project changes, out-of-subtree Lean source and editable symlink: rejected.
- Frozen target **byte-identical**, helper adds a permitted high-priority `HDiv ℝ ℝ ℝ` instance returning 0: candidate compiles, complete type comparison rejects with **Type mismatch**. The type check, not an earlier source/header failure, is the observed rejection.
- Candidate same-name FCBTrustedSpec source, invalid olean, invalid build-cache module and LEAN_PATH override: cannot replace the fixed trusted import. Same-name candidate Mathlib cache cannot replace trusted dependency resolution. Independent Spec audit still succeeds.
- Missing compiled artifact, altered artifact and altered manifest in isolated trusted-package fixtures: explicit failures, no runtime regeneration/fallback.

Source bans, confinement, frozen checks, target axiom audit and sorry canary remain in main's call path. The actual original theorem is intentionally unproved and was not expected to receive reward 1. No claim is made about untested general plugin/initializer security or arbitrary external dependencies; that is outside this repair's scope.

## Other checks and cleanup

Instruction's three-path rg command successfully found package definitions such as Mathlib/Analysis/Asymptotics/AsymptoticEquivalent.lean `IsEquivalent` (exit 0). Unicode script case `no_issue`, initial and final verification passed without changing headers.

Docker baseline and exact task-owned resources are saved in docker-before-* and resources-created.json. Only resource identities derived from this task's own named Spec container and Harbor trial results are eligible for cleanup. First Harbor container was auto-removed; exact project/name absence was verified. Cleanup is performed after saving the report and evidence, with results in docker-cleanup.json/log. Shared bases/caches and all pre-existing/other-agent resources are excluded.
