# Infrastructure validation

Task root: `/root/FormalConjectures-Bench/tasks-v3/erdosproblems-17-erdos-17-refute`.
All task mathematical inputs, public Target, golden trees, GoldenCheck files, frozen prefix SHA256 and header are unchanged (checked against git HEAD, not reset).

## 1–3

- Instruction search now explicitly includes `/app`, `/opt/formal-conjectures`, `/opt/formal-conjectures/.lake/packages`. Executed the search in matching Docker environment with pattern `^def IsCompact`; rg returned 0 and found `mathlib/Mathlib/Topology/Defs/Filter.lean` inside packages.
- Target imports only ProblemImports and Submission. No additional upstream module needed. Dockerfile now ends with `WORKDIR /app`, HOME, `USER ubuntu`, and `RUN lake build +FormalConjecturesBench.Target`. Spec-preparation image built successfully; final build uses current local task and compatible cache. Original sorry produces a build warning, not a missing dependency failure.
- Ran the skill Unicode script both before and after checker changes. Both report `case=no_issue`, unchanged original header passes; modified header and missing assignment rejected. No header/frozen baseline change.

## Trusted Spec

Repair-time preparation:
```
docker build -t fcb-erdos17-refute:spec-20261104 <task>/environment
docker run -d --name fcb-erdos17-refute-spec-20261104 --user root fcb-erdos17-refute:spec-20261104 sleep infinity
# Copy ONLY this task's original golden_env plus generator/auditor into /tmp/ep17r-clean.
docker exec -w /tmp/ep17r-clean fcb-erdos17-refute-spec-20261104 bash /tmp/ep17r-clean/trusted_spec/reproduce.sh
```
Both build and generation/audit exited 0. Generation does not load candidate sources/config/cache. The generator removes Submission import, elaborates the entire original target, extracts `ConstantInfo.type` and ordered universe parameters, restores the environment, then adds a definition with that expression as its value. The temporary theorem is not exported. Prefix IsClusterPrime remains under its original name.

Lean: 4.27.0, commit db93fe1608548721853390a10cd40580fe7d22ae, x86_64 Linux. Upstream 233a10e857ef78e79fd9fe661d37db724089170a; Mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900. Audit independently imports the precompiled module, verifies ExpectedType is a proposition-valued definition, no temporary theorem, no universes, and transitive axioms of ExpectedType and IsClusterPrime are only `[propext]`. It displays the negative infinitude expression. Manifest records complete input, source/code and artifact hashes and exact versions. Identical package copies are in `tests/trusted_spec` and `environment/data/checker/trusted_spec`.

Manifest SHA256: `521212f438cc82e5f4665052b1ccd6c0495f7081a428fbd8d66485e8a431eb87`.
Other artifact hashes: see trusted manifest. Resource IDs: `resources.json`.

Checker loads only the manifest-validated precompiled module, never generates/rebuilds it. Fixed Lean executable and LEAN_PATH order are Spec, pinned dependency libraries, then fresh temporary candidate sources. Candidate Lake config and caches are not used. Local helper sources are compiled in dependency order using Lean's own `--deps`; normal imports remain supported. Candidate compilation runs as ubuntu. Only temporary Target is rewritten to import the Spec's original prefix definitions and retain namespace/open settings. Complete target type is checked using the root-qualified theorem at the already elaborated ExpectedType. Original source restrictions, frozen checks, axiom audit and canary are preserved; static AST comparison confirms this.

## Actual local Harbor build and runtime

Read `harbor --help`, `harbor run --help`, and `harbor trial --help`. Used nop, not a proof-producing agent or old registry image:
```
harbor run -p <task> -a nop --env docker --no-delete --ek keep_containers=true \
  --force-build --extra-docker-compose /tmp/ep17r-network.yaml \
  --job-name ep17r-repair-finalnet-20261104 --jobs-dir /tmp/ep17r-harbor-jobs
```
`--no-delete` alone retained image but Harbor removed the first container. Read installed Harbor stop handling; `keep_containers=true` preserves it. A subsequent final attempt hit Docker's exhausted default network address pools (build itself succeeded); inspected existing subnets and supplied a nonoverlapping task-local subnet 10.231.217.0/24 through the supported compose option. No permissions, mounts or Docker socket were added; no other resources removed.

Final successful trial: `erdosproblems-17-erdos-17-refute__3RRMBqB`, container `896afda880d4`, image `erdosproblems-17-erdos-17-refute__3rrmbqb__env-main:latest` (full image ID in logs/resources). Harbor: one trial, no exceptions, reward 0. Started its retained container and ran:
```
docker exec 896afda880d4 bash /tests/test.sh                       # rc 1
# /tests/test.sh explicitly sets FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests.
docker exec -u ubuntu 896afda880d4 bash /app/check.sh              # rc 1
# check.sh explicitly loads the preinstalled /opt checker package.
```
Both reject the original proof's literal sorry at the source check, as expected; reward file is 0. This is not an infrastructure exception or a proof of the mathematical problem. Harbor itself uploaded /tests, including the fixed Spec. Every local tests file was hash-compared to /tests; both checker, all Spec artifacts and all golden files were also compared against /opt. All matched.

## Supplementary paths reached in that same final Harbor container

Ran `repair-evidence/supplement.py` copied into `/tmp` as ubuntu, first with `/tests`, then with `FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker`. Both runs exited **0**; no formal checker or task inputs were modified. Actual imported checker functions were called in isolated fixtures:

- Load manifest/artifacts and independently audit precompiled ExpectedType: pass for both locations.
- Compile fresh original placeholder candidate as ubuntu: pass.
- Full type comparison for placeholder candidate: pass (type only).
- Target axiom audit: **rejects sorryAx**, expected.
- Sorry canary: detects sorryAx, pass.
- Frozen prefix mutation, header mutation, source sorry, out-of-tree source and non-Lean editable file: reject.
- Same-name candidate `FCBTrustedSpec.lean`, root `.olean`, and `.lake/build/lib/lean/FCBTrustedSpec.olean`: cannot replace fixed module; Lean `--deps` resolves the verified Spec, audit and type comparison still pass.
- Semantic substitution with unchanged public prefix/header: a candidate meta-def attribute redirects set-builder elaboration to `Hacker.fakeSet`, using a different named `Hacker.IsClusterPrime`. Original source scanner accepts this syntax; the fixture compiles an axiom-clean proof of `¬ Hacker.fakeSet.Infinite`. **Actual complete type comparison rejects it** as not ExpectedType. Printed types and Lean error are retained in logs. No new blanket ban was added.
- Missing `.olean` and corrupt `.olean`: explicit load-time failure; before/after package bytes show no generation/fallback.

Uncovered: no genuine proof of the open negative target was supplied, hence no authentic reward-1 proof path is claimed. Isolated placeholders were retained only to test later checks and correctly fail the axiom audit. The semantic negative itself uses no placeholder and passes candidate axiom audit before rejection by the full type comparison. No unrelated external-module initializer/security sandbox tests were added.

## Evidence

`logs/` includes spec build/audit, Unicode JSONs, search sample, static result, entrypoint source/output, final Harbor result, hash checks, full supplementary output from each package location, network failure/resolution context, and initial Docker resources. `resources.json` records only resource names/IDs directly attributable to our exact build tags and Harbor trial projects, not a concurrent global diff. Report is saved before cleanup, then updated with actual cleanup results.
