# Infrastructure validation

## Scope

No public Target, golden input, frozen prefix hash, theorem header, or
GoldenCheck.lean was changed. `final-validation.json` compares these inputs
against repository HEAD. Two checkers and both trusted bundles are identical.
The original restrictions remain: frozen files/header, editable-tree checks,
source bans, allowed-axiom audit and sorry canary. Normal helper definitions,
lemmas, instances and ordinary imports are not blanket-banned.

## Trusted Spec

Generation used the existing matching dependency image
`sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`
in a new task-owned container `fcb-green26-open-spec-20261104` (network none).
Its /app, Lake config and candidate caches are not on generation LEAN_PATH.
Only the original golden Target supplies mathematical input; Submission import
is removed. `generate.py` asks Lean's parser/elaborator for the entire temporary
target declaration, reads its type and level parameters, resets the environment,
and exports the type as the value of `FCBTrustedSpec.ExpectedType`.
The temporary theorem/proof is not exported. Existing unrelated prefix theorem
placeholders are not dependencies of ExpectedType or the cube definitions.

Reproduce at repair time using `tests/trusted_spec/reproduce.sh` in a matching
image with sibling golden_env. The verifier never runs this generator or
compiles the Spec. Source, generator, .olean/.ilean, audit, input hashes,
compiler version, x86_64 platform, revisions and universe parameter order are
recorded in `tests/trusted_spec/manifest.json` (SHA256
`84fb9f3b33b495b7cf85f76016c73c366c6ffd5f79f46aca2f2d8c1fb3ba8bdf`).
The complete type has no universe parameters; it retains p and the implicit
Fact p.Prime binder, followed by the full existential C and all nested binders.
Independent import audit succeeded, standard axioms only (exit 0).

## Final current-task Harbor build

CLI help was read independently. Final command:

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/greensopenproblems-26-open-prove --agent nop --env docker --force-build --no-delete --ek keep_containers=true --extra-docker-compose /tmp/green26-repair/network-final-overlay.yaml --job-name fcb-green26-open-final2-20261104 --jobs-dir /tmp/green26-repair/jobs --n-concurrent 1
```

The overlay only assigns a task-specific subnet, 10.249.126.0/24. Docker's
predefined subnet pools were exhausted; no existing networks/resources were
removed. A prior retry retained a container on 10.249.26.0/24, so the final run
used a different unused subnet. `--no-delete` alone in this Harbor version
removes containers; `keep_containers=true` preserves them stopped for supplement
coverage. They were restarted with docker start.

Final local build image:
`greensopenproblems-26-open-prove__zjl4wwf__env-main:latest`, ID
`sha256:a171f407ede3d13167336a1a091cfe2ac319f1b44a15d5843647b4a3425e8d93`.
Final Harbor child:
`6eadd2ca82006fe7caaad6a8c24d49d46fadf2762e0e47f5d0471e513d8bac8b`.
It has no host mounts/socket or extra host dependencies. Dockerfile remains
FROM ubuntu:24.04 with pinned dependency checkout and ends with the ubuntu
`RUN lake build +FormalConjecturesBench.Target`. The final child also ran that
Lake build directly as ubuntu: exit 0. Cached trusted build layers were reused;
no registry task image replaced this task's build.

Harbor uploaded /tests at verifier stage. Hashes of all 33 files in /tests and
/opt/formal-conjectures-bench-checker match the local checker, golden and Spec
packages (`final-validation.json`). The official /tests/test.sh sets
FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests. Local /app/check.sh uses the /opt
package. Spec is always TESTS_DIR/trusted_spec; only its verified compiled
module and fixed dependency/toolchain paths precede the fresh candidate path.
No candidate Lake configuration or .lake cache is copied/used to load Spec.

## Entry points and actual-function supplements

In that same Harbor child:

* `docker exec <child> bash /tests/test.sh`: exit 1, reward 0, expected rejection
  of the original target's sorry. Harbor's nop trial had no infrastructure
  exception and reward 0.
* `docker exec -u ubuntu -w /app <child> /app/check.sh`: exit 1, same expected
  source-ban rejection. Neither is claimed to prove the open theorem.
* Independent `supplement.py` imports the delivered checker and calls its real
  functions, without changing the official checker, Target or golden. Formal
  /tests supplement exit 0; local /opt supplement as ubuntu exit 0. Their logs
  record:
  - fixed package validation and full-type/prefix dependency audit;
  - fresh candidate compilation as ubuntu (isolated placeholder fixture);
  - successful full type comparison for the original complete type;
  - rejection of that fixture's sorryAx by target axiom audit;
  - successful sorry canary detection;
  - prefix/header mutations and missing := rejected;
  - extra source outside editable subtree rejected;
  - unchanged frozen text plus helper `Green26.univ := ∅` compiled, then
    failed the actual full-type comparison against the pre-elaborated Spec;
  - invalid same-name candidate source/cache and LEAN_PATH/LEAN_SYSROOT
    overrides did not replace Spec (actual --deps source path checked);
  - missing/corrupt precompiled artifacts rejected before build; no fallback
    generation or Spec compilation exists.

No complete candidate proof was constructed or required. The proof-success
exit-0 branch is not covered by a proof of this open problem; the infrastructure
paths that the original sorry would skip were covered independently.

Other checks: package source search for `^def IsOpen` succeeded as ubuntu with
all three instruction paths (exit 0); Unicode script repaired the non-BMP F
header in both checkers and checked original/changed/missing-assignment cases.
Python AST and TOML parsing pass. Immutable mathematical inputs are unchanged.

Resource identities and cleanup are recorded in `resources.json`,
`cleanup.log`, and the report. Only these task-owned resources are removed.
