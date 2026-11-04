# Infrastructure validation

All commands used this task's absolute path. Initial Docker inventories are
`before-containers.txt` / `before-images.txt`; no resources were claimed by
global before/after differences. Only the explicit task-specific names below
are owned by this repair.

## 1–3

- instruction search now includes /app, /opt/formal-conjectures and its hidden
  .lake/packages explicitly. Executed the actual command as ubuntu in the
  final Harbor container with `def sqrt`: exit 0, known Mathlib definitions
  found, no permission/path errors (search-validation.log).
- No additional upstream Target imports beyond ProblemImports and the local
  Submission. Added final Docker `USER ubuntu` / `RUN lake build
  +FormalConjecturesBench.Target`. Build succeeded (7992 jobs); original
  placeholder warnings are expected. No dependency permissions relaxed.
- Executed skill check_unicode_header.py: no_issue, both heads match; original
  passes and altered/missing-assignment heads are rejected (unicode.json).

## Spec generation

Precompile image was locally built from this task Dockerfile:

```
docker build -t fcb-hall-prove-spec:nt40-20261104 \
  -f <task>/environment/Dockerfile <task>/environment
```

Image index ID: sha256:6c08268fca51ddfcdc0957423511ff4f4d1bfaf4da5639cd4748aee0be0117b7.
Container: fcb-hall-prove-spec-nt40 (final generation ID d2a0a9c56b5b).
Copied the trusted tests/golden_env and extraction scripts, ran
`bash /tmp/hall-prove-trusted-tests/trusted_spec/reproduce.sh`, copied artifacts
back. The generator has no candidate inputs, excludes Submission import,
elaborates the entire original theorem, keeps its type/universe parameters,
and resets the environment before defining ExpectedType. Earlier extraction
attempts found a trailing doc-comment parser error and a Lake invocation that
wanted to reclone stripped dependencies; these were fixed by removing only
the target's orphaned doc-comment in generated source and invoking the pinned
Lean directly with fixed trusted dependency paths in a fresh container.
Final compilation and independent audit succeeded; no runtime generation.

The original prefix retains preexisting statements with placeholders. They
are not transitive dependencies of ExpectedType. Independent audit checks
ExpectedType, HallIneq and HallConjectureExp and their transitive axioms:
only propext, Quot.sound, Classical.choice. The temporary target is absent.
ExpectedType is a definition whose value is `forall epsilon>0,
HallConjectureExp (1/2-epsilon)`; ordered universe parameters are [].

Manifest SHA256: faa551851c0df81996c5df1d3e1845507f896308cc37b55cc4605e2a3289b893.
Golden Target SHA256: 63ea370df28c534cd8f00dcea79f0dbf4035abc437defb763a661c421f1bd21b.
Spec .olean SHA256: 824511371adf56342cc0aaee185adb6201d29179272875693a4623210167302d.
All source/artifact hashes, exact Lean/platform/revisions and all golden input
hashes are in both identical trusted_spec/manifest.json files.

## Current local Harbor Docker build and actual entries

Read Harbor CLI --help, run --help and task start-env --help independently.
Initial `harbor run --agent nop --env docker --no-delete --force-build`
built and verified, but --no-delete alone still removes the container on this
Harbor version. A retry with `--ek keep_containers=true` encountered exhausted
Docker automatic subnet pools. Did not delete any existing networks. Inspected
IPAM, selected a non-overlapping explicit task-only subnet via the CLI-supported
compose overlay (compose-network.yaml). Successful retained run:

```
harbor run --path <absolute task> --agent nop --env docker \
  --no-delete --ek keep_containers=true --force-build \
  --extra-docker-compose /tmp/hall-prove-compose-network.yaml \
  --n-concurrent 1 --job-name hall-prove-nt40-network \
  --jobs-dir /tmp/hall-prove-harbor-jobs
```

Job had no exceptions and reward 0. The environment is built from the current
local Dockerfile; no registry task/image was substituted. Spec precompile
container was not used for final acceptance.
Final image: wikipedia-hall-weak-hall-conject__uxs83dv__env-main:latest,
sha256:216c9df3fe8ecbac80cf0fa72fdaae6a407ea42acd50047be16979327941cd22.
Final Harbor container:
451b3444077d906bd6ea8f98bf25dc0eb2704c7033c742262289ccb3e6bba60e.
Harbor stopped it on completion; restarted it for actual supplemental checks.
No Docker socket, host mounts, or widened permissions (Mounts=[]).

Harbor supplied /tests and /logs/verifier. Container hashes of both checkers,
both entire Spec packages, both golden trees and GoldenCheck files match host
(container-hashes.json). /tests/test.sh sets FCB_TASK_DIR=/app and
FCB_TESTS_DIR=/tests. Explicit docker exec `bash /tests/test.sh`: exit 1,
reward.txt = 0; `--user ubuntu bash /app/check.sh`: exit 1. Both reject the
unmodified placeholder at the original source check, an expected proof failure,
not an infrastructure pass or a solved conjecture.

## Same-container supplements

`docker exec --user ubuntu <final-container> python3 /tmp/hall-prove-supplement.py`
and the same with `-e FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker`
both exit 0, ALL SUPPLEMENTAL ASSERTIONS PASSED. Saved source and per-entry
logs/results. The driver imports and calls the actual unmodified checker
functions, not a replacement verifier. Fixtures live only in disposable /tmp
projects; original public Target and golden were not changed.

Covered on each path (/tests official package and /opt local package):
- fixed manifest/hash/input/toolchain/platform validation;
- original header passes, changed frozen prefix and header rejected;
- banned sorry and out-of-tree source rejected;
- independent Spec value/prefix transitive axiom audit passes;
- temporary candidate compiled by the pinned Lean as ubuntu;
- complete candidate theorem type matches ExpectedType for original fixture;
- target's sorryAx is detected and rejected by real axiom audit;
- sorry canary detects sorryAx;
- same-name candidate module/cache and forged LEAN_PATH/LEAN_SYSROOT cannot
  replace the fixed Spec (actual --deps resolves the trusted package);
- high-priority HSub real instance in Submission compiles while frozen text
  and header remain byte-identical, but complete type comparison rejects it;
- missing and corrupt .olean fail explicitly, with no regeneration/fallback.

All formal checker rules remain present, including editable source checks,
frozen checks, axiom checks and canary. Normal helper/import compilation is
retained with trusted Spec/dependencies ordered before candidate paths.
Static AST, package consistency, manifest hashes, final Docker validation
position and original immutable files were rechecked (static-validation.json).
No complete mathematical proof fixture is required or provided. The only
uncovered success is an axiom-clean proof of the actual open conjecture.

## Resource cleanup

Four explicitly owned image tags/IDs are listed in owned-images.txt, including
the initial Harbor run and the failed-network build. The only retained
containers were the Spec generation container and the final Harbor container.
An earlier same-name Spec container was explicitly stopped/removed when
resetting the failed generation environment; the first Harbor run was
reclaimed by Harbor. The final task-only network is
fcb-hall-prove-nt40-20261104 (10.251.73.0/24).

Report and evidence were saved before cleanup. See cleanup.log for actual
stop/rm/image rm/network rm and inspect verification. No shared images,
user containers, other-agent containers/networks or build caches were pruned.
