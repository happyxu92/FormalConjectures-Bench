# Infrastructure validation

All original mathematical inputs, public Target, golden copies, GoldenCheck.lean, frozen header and prefix hash are unchanged.

## Steps 1-3

- instruction.md now explicitly searches /app, /opt/formal-conjectures and /opt/formal-conjectures/.lake/packages. Real rg command found `def IsCoprime` in mathlib/Mathlib/RingTheory/Coprime/Basic.lean:43, exit 0 (fcb137ref-search-validation.log).
- Target has only ProblemImports and local Submission imports; no extra upstream precompilation was needed. Dockerfile ends with `WORKDIR /app`, HOME ubuntu, USER ubuntu and `RUN lake build +FormalConjecturesBench.Target`. Current Harbor image build succeeded; see docker-history.txt.
- Skill Unicode checker returned no_issue and exercised baseline, changed header and removed assignment. Both checker copies agree.

## Repair-time Spec

Created container fcb137ref-spec-20261104 (9bc7da32aee831e01a1af21067482556568c6817b425cdef742317bba5d4ed38) from pre-existing trusted matching base image sha256:0824de0f16475f1f619701869e59de4e4ce3229bfce229a5fd16f88072c37e8f, network none. Copied only this task's golden_env and extraction/audit tools into /tmp/fcb137ref-bundle.

Generation command: `docker exec -u root fcb137ref-spec-20261104 bash /tmp/fcb137ref-bundle/trusted_spec/reproduce.sh`.

The extraction elaborates the full original declaration without Submission, captures its type and ordered universe parameters, restores the original Lean environment and exports only a definition ExpectedType. Independent import asserts temporary theorem absence and audits all transitive type/value dependencies; only propext, Classical.choice and Quot.sound occur. There are no universe parameters or omitted outer binders. The initial dangling doc-comment parser error was corrected before successful generation; no failed artifact was delivered.

Manifest SHA256: e9457971cd54443630a73ca0e3d73ba6527d8a79874553e4a4525958e3acecf7.
Spec olean SHA256: 6368e51a8f756b919be8b7211e036debd7c41a98e1bf039a9227260d60a96c56.
Golden Target SHA256: 42ea40cbd254abd516690686dd198bcbe887d30cf2c8c7e8c0404a9a1fbbcc87.
Lean version, platform, dependency revisions and hashes of all original golden inputs and delivered files are pinned in both identical manifests. The generator/reproduce.sh are repair-time tools only, never called by the verifier.

## Current local Harbor build and entrypoints

Read `harbor --help` and `harbor run --help` before selecting options. Commands:

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-137-erdos-137-refute --agent nop --env docker --no-delete --force-build --ek keep_containers=true --extra-docker-compose /tmp/fcb137ref-compose.yaml --job-name fcb137ref-retained-20261104 --jobs-dir /tmp/fcb137ref-harbor -n 1
```

The first build succeeded but container startup failed because existing Docker networks exhausted predefined pools. No existing networks were removed. A task-exclusive 10.247.137.0/24 compose overlay resolved that. A second run completed but --no-delete retains only images; inspecting Harbor implementation showed `keep_containers=true` is needed to retain a stopped container. The third/current run retained the exact Harbor child for supplements.

Current acceptance image: sha256:4ac7a4024fc6fb6b8d00144d96a795dae8675e2b436871cd758783f11e68485d, tag erdosproblems-137-erdos-137-refu__3udnqd7__env-main:latest.
Harbor child: 21b5b26394d2568020b0e4551bcee39b8e0069f7444444d3f112be49258235be.

Harbor uploaded /tests at verification, with /logs/verifier provided by Harbor (inspect log and retained config). All uploaded Spec/golden/checker contents matched the preinstalled /opt package and host hashes. No registry task image was substituted for the local task build.

- Harbor actual verification: completed, reward 0 (expected original sorry rejection).
- Restarted retained child, `docker exec -u root 21b5b26394d2 bash /tests/test.sh`: exit 1, original sorry banned, reward 0.
- `docker exec -u ubuntu 21b5b26394d2 bash /app/check.sh`: exit 1, same expected rejection.

The entrypoints set FCB_TASK_DIR=/app and respectively FCB_TESTS_DIR=/tests or /opt/formal-conjectures-bench-checker. The formal verifier does not read the preinstalled /opt Spec instead of the uploaded package.

## Supplemental coverage in that SAME Harbor child

`docker exec -u root 21b5b26394d2 python3 /tmp/fcb137ref-supplement.py`: exit 0.
Repeated with FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker: exit 0.

Actual checker functions exercised, without changing formal checker or public/golden inputs:
- Fixed-package validation, independent Spec loading and transitive type audit.
- Candidate compilation after dropping to ubuntu, fixed compiler and trusted imports, no candidate Lake configuration.
- Full expected-type comparison succeeded for isolated original placeholder fixture.
- Actual target axiom audit rejected sorryAx; canary independently detected sorryAx.
- Forged same-name module/source, .lake module cache and poisoned LEAN_PATH/LEAN_SYSROOT did not replace Spec.
- Frozen prefix/header changes, missing assignment, banned syntax, outside-tree Lean file and non-Lean editable file rejected.
- A high-priority LE Nat instance changed the meaning of the unchanged target header. The isolated candidate compiled without sorry, passed its own axiom audit, and was rejected by the actual full-type comparison. This is a real semantic negative, not an inferred rejection at an earlier stage.
- Missing/corrupt precompiled olean explicitly rejected without creating files or runtime regeneration.

Python AST, frozen-input comparisons, pinned manifest/artifact hashes, and both trusted package contents verified statically as well. This validates infrastructure, not a proof of Erdős 137; original proof remains intentionally unfinished. No original full proof is claimed and no answer is bundled.
