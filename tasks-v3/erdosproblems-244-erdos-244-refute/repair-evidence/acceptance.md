# erdosproblems-244-erdos-244-refute repair acceptance

Only this task was changed. Public Target, golden copies, GoldenCheck.lean, expected header and frozen prefix hash remain unchanged. No mathematical answer is bundled.

## Steps 1–3

- Instruction now explicitly searches `/app`, `/opt/formal-conjectures`, and `/opt/formal-conjectures/.lake/packages`. Actual rg package test (exit 0) found `def Prime` in Mathlib; see `244-refute-package-search.log`.
- Target imports only ProblemImports and local Submission; no extra upstream build target needed. Dockerfile ends with `USER ubuntu` and `RUN lake build +FormalConjecturesBench.Target` after all copy/cleanup/permissions. Actual ubuntu build exit 0 (`ubuntu-build.log`).
- Skill Unicode script exit 0, case `no_issue`; original header accepted, changed header/missing assignment rejected; see `244-refute-unicode.json`.

## Spec generation and identity

Existing resources were recorded in `/tmp/244-refute-docker-before.txt` and `/tmp/244-refute-images-before.txt`. Reused the trusted pinned base image `erdos1062-import-20261102__env-main:latest`, ID `6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`, without altering it. Its history records the exact Formal Conjectures commit and ProblemImports build (`244-refute-base-history.txt`).

Commands:

```
docker run -d --network none --name fcb-244-refute-spec-20261104 erdos1062-import-20261102__env-main:latest sleep infinity
docker cp <task>/tests fcb-244-refute-spec-20261104:/tmp/244-refute-generation
docker exec -u root fcb-244-refute-spec-20261104 bash /tmp/244-refute-generation/trusted_spec/reproduce.sh
```

Generation/audit exit 0. Container ID `b749a299e47c` (full ID in cleanup evidence). Generation uses only golden prefix/type and pinned dependencies, with Submission import removed. It elaborates the complete temporary declaration, saves its `ConstantInfo.type` and ordered level parameters, restores the original environment, then kernel-checks a safe definition. Audit confirms temporary target/children absent, ExpectedType is a closed proposition (universe parameters `[]`), and transitive axioms are exactly propext/Classical.choice/Quot.sound, not sorryAx. The generation warning refers only to the temporary declaration, not exported ExpectedType. No task-local prefix definitions exist for this target.

Both trusted packages are from the same generation. `manifest.json` pins every artifact/generator/audit hash, all golden inputs, versions and dependency revisions. Manifest SHA256: `4917df2acc39ebbc5cf987dd617e16f68ee55dc6377d76d351f61695501407ac`. Original golden Target SHA256: `5d4cd04ee920b1184e4caafc419d3a2b7e30f1bc3d65e17ba92fd588cd55fa36`. Lean 4.27.0 (db93fe1608548721853390a10cd40580fe7d22ae), x86_64 Linux; formal-conjectures 233a10e857ef78e79fd9fe661d37db724089170a; mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900.

## Actual current-task Harbor builds and entrypoints

CLI help was read independently. Commands (absolute local task path in place of `<task>`):

```
harbor run --path <task> --agent nop --env docker --force-build --no-delete --job-name fcb-244-refute-20261104 --jobs-dir /tmp/244-refute-harbor --n-concurrent 1
harbor run --path <task> --agent nop --env docker --force-build --no-delete --ek keep_containers=true --job-name fcb-244-refute-accept-20261104 --jobs-dir /tmp/244-refute-harbor --n-concurrent 1
```

Both trials finished without infrastructure exceptions, reward 0. First trial's `--no-delete` retains its image but this Harbor version still removes its container; therefore the second trial additionally sets `keep_containers=true`. This is not a registry task: local environment COPY and final ubuntu build layers are in `harbor-image-history.txt`.

- First image tag: `erdosproblems-244-erdos-244-refu__uqadwt5__env-main:latest`, ID `09724b6fce6ada92af0fb44bdbd2ac0ca7c8d2702321fc7adca5aba48caafbb1`.
- Accepted image tag: `erdosproblems-244-erdos-244-refu__zq2nbzk__env-main:latest`, ID `f03f89685ed9a48e9a4dee7f2719539e10ba654bba95db52ed5fea501f3c28d1`.
- Accepted Harbor child: `38b907a70f7b`, named `erdosproblems-244-erdos-244-refu__zq2nbzk__env-main-1`. Harbor initially stopped it; `docker start 38b907a70f7b` resumed the same child for supplementary checks.
- `docker exec 38b907a70f7b bash /tests/test.sh`: exit 1, reward.txt 0, expected original sorry syntax rejection.
- `docker exec -u ubuntu 38b907a70f7b bash /app/check.sh`: exit 1, same expected rejection.
- `/tests/test.sh` explicitly uses FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests. Local check.sh uses /opt/formal-conjectures-bench-checker. Harbor supplied /tests and /logs/verifier; no Docker socket or extra host dependency mounts.
- Recursive hashes confirmed both container packages and golden copies match both host copies (`package-comparison.log`, `244-refute-container-hashes.txt`).

## Supplementary coverage in the same Harbor child

```
docker cp /tmp/244-refute-coverage.py 38b907a70f7b:/tmp/244-refute-coverage.py
docker exec 38b907a70f7b python3 /tmp/244-refute-coverage.py
```

Final exit 0; actual checker functions are imported, never patched or relaxed. Isolated fixtures, not public Target/golden, contain the original placeholder for later-stage coverage. `coverage.py` and `244-refute-coverage.log` retain reproducible tests/results:

- Fixed manifest/artifact/version/input loading and independent trusted type/transitive axiom audit pass.
- Original fixture compiles as ubuntu; full type matches ExpectedType; target axiom audit rejects sorryAx; sorry canary detects it.
- Modified frozen prefix/header and added out-of-scope Lean source are rejected.
- Frozen-text-preserving semantic negative defines an ordinary LT Real instance in Submission. A proof of that altered proposition compiles without sorry, but the checker rejects its COMPLETE type against fixed ExpectedType. This proves actual comparison was reached, not merely source rejection. Initial exploratory fixture attempts that did not compile were corrected; only the final exit-0 coverage is used for acceptance.
- Same-named candidate Spec source/olean and candidate .lake cache cannot replace trusted Spec: --deps selects /tests/trusted_spec/FCBTrustedSpec.olean and independent audit/build/full type still pass.
- Missing precompiled olean and mismatched artifact hashes fail explicitly. Missing olean remains absent: no runtime regeneration/fallback.

Runtime uses fixed toolchain and fixed trusted library paths, with validated Spec first and isolated candidate project last. It never invokes candidate Lake config or loads candidate .lake cache. Normal helper declarations/imports and original source/frozen/axiom/canary restrictions are retained; no generic external module security policy was added.

No complete mathematical proof was tested or claimed; successful proof reward=1 is intentionally not covered. The later-stage validation uses isolated placeholders with demonstrated sorryAx rejection, as required.

## Steps 5–6

See `research.json`. Statement status consistent (open refutation direction, no obvious formalization error); exact CSV lookup missed, then multiple independent web keyword groups and upstream/author/PR sources were followed. No public complete Lean4 proof of this NEGATION found. Romanoff positive/base-2/analytic-hypothesis proofs and category-only sorry PRs are specifically excluded. Direct source website had Cloudflare/403; original paper, source wiki and upstream code/issues were accessible.
