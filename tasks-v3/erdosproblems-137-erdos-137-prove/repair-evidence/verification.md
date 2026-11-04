# Verification and scope

Task: erdosproblems-137-erdos-137-prove. No public Target, golden, frozen hash,
original theorem header, or GoldenCheck.lean was changed; final byte comparison
against repository HEAD passed (`final-static-and-hashes.log`). No answer added.

## Ordered repairs

1. instruction.md source-search command now explicitly includes the packages
   path. Final container ran the same three-root command using `def IsSquare`:
   exit 0, matching Mathlib/Algebra/Group/Even.lean (`final-package-search.log`).
2. Target imports only ProblemImports and local Submission: no extra upstream
   precompile imports needed. Dockerfile now ends with HOME=/home/ubuntu,
   USER ubuntu, RUN lake build +FormalConjecturesBench.Target after copying,
   cleaning and permission setup. Local Harbor builds succeeded. Independent
   final-container ubuntu Lake build exit 0, original sorry warning only.
3. Skill unicode script executed in skill directory with the absolute task
   argument: exit 0, case no_issue; both headers, frozen baselines and `:=`
   negative checks passed, no header changes (`unicode.json`).
4. Repair-time-only Spec generation uses golden without Submission, Lean parser
   and elaborator, stores info.type plus ordered info.levelParams, restores the
   environment before emitting ExpectedType. Original temporary theorem absent
   on independent import. Definition value has both Nat quantifiers and k≥3.
   No universes or local prefix definitions for this target. Transitive audit
   allows only propext, Classical.choice and Quot.sound; no sorryAx dependency.
   The transient elaboration warning about sorry is not an exported proof.
   All generation input/artifact/version/revision hashes are pinned in the two
   identical trusted_spec/manifest.json packages.
5–6. See research.md; statement consistent, public proof status unknown/blocked.

## Repair-time compilation

Reused trusted pre-existing image
`fcb-local/erdosproblems-1-least-n-5:cache-smoke`,
sha256:0824de0f16475f1f619701869e59de4e4ce3229bfce229a5fd16f88072c37e8f.
This image is a dependency cache, NOT the final task build.

```
docker run -d --network none --name fcb-ep137-prove-spec-20261104 \
  --entrypoint sleep fcb-local/erdosproblems-1-least-n-5:cache-smoke infinity
# copy this task's tests/golden_env and tests/trusted_spec into /tmp/ep137-bundle/
docker exec -u root fcb-ep137-prove-spec-20261104 \
  bash /tmp/ep137-bundle/trusted_spec/reproduce.sh
```

Generation and audit exit 0. Toolchain is pinned v4.27.0, x86_64 Linux; upstream
commit 233a10e857ef78e79fd9fe661d37db724089170a, Mathlib
 a3a10db0e9d66acbebf76c5e6a135066525ac900; dependency manifest hash
5b99b5f4f807cbba67bbcd22e5e486c17d6a8d970ea218de08d05830ab350c26.
Trusted manifest hash
2c72f975cd7f0da2fd41d279e67e35771b06e1f1ecc6055c01844e6ab0f7c28c.

## Final current-local-task Harbor build and entry tests

Read Harbor run/trials CLI help independently. The first run showed that
--no-delete alone retains images but removes containers; source inspection
confirmed that --ek keep_containers=true is needed for supplemental testing.
No Docker socket or extra host mount was supplied.

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-137-erdos-137-prove \
  --agent nop --env docker --force-build --no-delete --ek keep_containers=true \
  --n-concurrent 1 --debug --jobs-dir /tmp/ep137-harbor \
  --job-name ep137-prove-final-20261104
```

Harbor exit 0; no exceptions, reward 0. Final image:
`erdosproblems-137-erdos-137-prov__ezpnn5h__env-main:latest`,
sha256:e2547c42bf4dee18b9926adad3f510ed616a4d5204330522e1acab3fac801b19.
Final child: 15f5c18424c07129b6bf479d39e1304cbbaf6e858e6bc75e919abd143285a70d.
Restarted this same retained Harbor child for all final additional tests.

- `/tests/test.sh`: exit 1, reward.txt=0, expected banned sorry rejection.
- `docker exec -u ubuntu ... bash -c 'cd /app && ./check.sh'`: exit 1,
  same expected rejection. No theorem-success claim.
- Harbor supplied /logs/verifier and uploaded /tests; docker diff shows /tests
  added after image creation; no volume mounts. Official entry explicitly sets
  FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests. Local check.sh uses the /opt package.
- Both checker copies, every trusted_spec file, every golden file and
  GoldenCheck hashes match host and final Harbor copies exactly.
- AST, TOML, package synchronization and Dockerfile-tail checks passed.

## Supplemental actual-function coverage in the same final child

`python3 /tmp/ep137-supplement.py` (formal /tests) and
`docker exec -u ubuntu -e FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker ...`
both exited 0; see final-supplement.log and final-ubuntu-supplement.log.
The script imports the delivered checker and calls its real functions; no
formal checker, public Target or golden edits and no rule disabling.

Covered:
- Fixed manifest, artifact and dependency/version validation; independent
  ExpectedType value/universe/transitive axiom audit.
- Original complete type compiled as ubuntu in a fresh isolated fixture (its
  placeholder intentionally retained solely for path coverage), type comparison
  passed; target axiom audit detected and rejected sorryAx.
- Sorry canary successfully detected sorryAx.
- Frozen-prefix changes, theorem-header changes, missing `:=`, and out-of-tree
  Lean sources explicitly rejected; tree/frozen-file checks also invoked.
- Same frozen header with Submission defining Erdos137.Finset.Ioc: candidate
  compilation succeeded, full type comparison actually failed with the
  shadowed constant visible in the type mismatch. Not just a source-ban failure.
- Compiled same-name FCBTrustedSpec.olean put in candidate root, candidate Lake
  cache and ambient LEAN_PATH; --deps and printed ExpectedType confirmed the
  fixed /tests or /opt artifact won, and full comparison still passed.
- Missing .olean and corrupt .olean rejected before invoking compiler/generator;
  no regeneration fallback and absent artifact stayed absent.

No original complete proof was attempted. Positive no-sorry acceptance of this
open theorem is intentionally not covered. Generic compiler/plugin execution
security and unrelated external-import sandboxing are outside this repair.

## Resources

Existing resources were recorded before creation in /tmp/ep137-before-containers.txt
and /tmp/ep137-before-images.txt. Only explicit task-owned IDs/tags are cleaned;
no global diff ownership inference and no prune. Created-image IDs/tags are in
created-images.log. Containers: generation 6f3a87ab2ada; first Harbor
e99bdb518f9a (auto-removed); retained intermediate 17a794a46908; final
15f5c18424c0. Shared base image and build cache are retained intentionally.
Cleanup results are recorded separately in cleanup.log after report persistence.
