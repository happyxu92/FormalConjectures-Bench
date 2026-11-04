# Infrastructure validation (not a solution of Erdős 11)

## Generation and identity

- `docker run -d --network none --name fcb-erdos11-prove-spec-20261104 --entrypoint sleep fcb-local/erdosproblems-1-least-n-5:cache-smoke infinity` created container `6d7f2290c1df267ee9a221b3bfc4a286ac9a33ec62737d92e115d82565cb4fbc` from a pre-existing trusted cached image, not a newly claimed image. No host mounts/socket.
- Copied this task's immutable `tests/golden_env` and new `tests/trusted_spec` into `/tmp/erdos11-bundle` and ran `docker exec -u root fcb-erdos11-prove-spec-20261104 bash /tmp/erdos11-bundle/trusted_spec/reproduce.sh` (exit 0). This invokes the pinned Lean binary with explicit trusted dependency paths and no Lake/candidate configuration, after removing the Submission import from the trusted input.
- Golden Target SHA256: `d5075820fd0d6d2016384da11d3f80ceb676978f4c545623c8d499a7e04f5c2c`. Both golden directories, public Target, and both GoldenCheck files remain byte-identical to repository HEAD. Original frozen hash and EXPECTED_HEADER unchanged.
- Lean 4.27.0 x86_64 Linux, commit `db93fe1608548721853390a10cd40580fe7d22ae`; FormalConjectures revision `233a10e857ef78e79fd9fe661d37db724089170a`; Mathlib revision `a3a10db0e9d66acbebf76c5e6a135066525ac900`.
- `tests/trusted_spec/manifest.json` (SHA256 `4ddd9430b5132367cc6085a4d826fb0e377f23ff6badd9322975a1a74a852930`) pins every source, generator, audit log and compiled artifact, all golden inputs, all dependency revisions, platform/version, and ordered universe parameters (empty). Both delivered packages are byte-identical.
- Independent Lean audit confirms ExpectedType is a definition whose VALUE is `∀ n : ℕ, Odd n → 1 < n → ∃ k l : ℕ, Squarefree k ∧ n = k + 2 ^ l`. Its transitive axiom set is `[propext]`; the placeholder target was rolled out of the environment and is absent from the delivered module. All original parameters are retained; no new axiom or proof of the problem is exported. See `trusted_spec/audit.log`.

## Checker changes and static checks

- Both checker ASTs parse and are identical. Both Spec package trees match by bytes.
- Spec manifest/artifacts/golden/version/dependency manifest checked before fixed precompiled loading; no runtime generation/recompilation or fallback. Sanitized Lean process environment and fixed Spec/dependency-first import paths, with ordinary helper source imports after trusted roots. No candidate Lake configuration is executed.
- Only the verification copy of Target imports Spec before Submission, preserving `namespace Erdos11` and using the Spec prefix. No mathematical prefix definitions need duplication for this target.
- Comparison imports both compiled modules and assigns `@_root_.Erdos11.erdos_11` to `_root_.FCBTrustedSpec.ExpectedType`, checking the entire type including assumptions. No original proposition is re-parsed in the candidate environment.
- Frozen/source/banned-syntax checks, theorem-axiom audit, and sorry canary remain on their main execution paths. No generic dependency whitelist/sandbox was added. Existing helper `def`/`lemma`/`instance` rules remain.
- Dockerfile's last build step remains `RUN lake build +FormalConjecturesBench.Target`, under `USER ubuntu`, after copy/cleanup/permissions. Target has no extra imports requiring extra upstream build targets. Image history and Harbor build transcript confirm that layer. Trusted dependencies were not made writable.

## Current-local-task Harbor acceptance

Harbor CLI help was independently consulted. First trial used `--no-delete` but DockerEnvironment removed the container; discovered its separate `keep_containers` setting and reran successfully using `--environment-kwarg keep_containers=true`.

Final command (executed from the task root):

```bash
harbor trials start \
  --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-11-erdos-11-prove \
  --trial-name fcb-erdos11-prove-final-20261104 \
  --trials-dir /tmp/erdos11-prove-harbor-final-retry \
  --agent nop --env docker --no-delete --force-build \
  --environment-kwarg keep_containers=true \
  --extra-docker-compose /tmp/erdos11-prove-own-network.yaml
```

The final local Docker build succeeded. One intermediate final attempt hit Docker subnet-pool exhaustion after building successfully. It was resolved without touching any other task/user resource: `own-network.yaml` reused only this task's already-created `fcb-erdos11-prove-20261104__env_default` network. No extra host dependencies, socket mounts, capabilities, or relaxed permissions were used.

Final Harbor image: `fcb-erdos11-prove-final-20261104__env-main:latest`, ID `sha256:b47d487da6c02607b7ff6eb1e46352616213e229c0a6011af14d5bde4358285a`. Final Harbor child container: `668b6f47fc6479baf6d84e616f0716b038a08851ba8a0761a1dbec4a4cfe5a93`. The stopped retained child was restarted for manual entry/supplemental runs. Mount list is empty. Harbor uploaded `/tests` and supplied `/logs/verifier`; all `/tests` and `/opt/formal-conjectures-bench-checker` checker/Spec/golden file hashes match the host (`container-hashes.json`). These are not registry task images.

- `docker exec fcb-erdos11-prove-final-20261104__env-main-1 bash /tests/test.sh`: exit 1, reward 0, expected original `sorry` rejection.
- `docker exec -u ubuntu fcb-erdos11-prove-final-20261104__env-main-1 /app/check.sh`: exit 1, same expected `sorry` rejection.
- `entrypoints.log` confirms formal FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests, and local FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker.
- Since those exits occur before loading Spec, the actual checker functions were exercised independently in isolated fixtures by `supplement.py`, without changing the official Target/checker/golden or relaxing any official checks.
- Formal-path supplement: `docker exec -e FCB_TASK_DIR=/app -e FCB_TESTS_DIR=/tests ... python3 /tmp/erdos11-prove-supplement.py`, exit 0.
- Local-path supplement: `docker exec -u ubuntu -e FCB_TASK_DIR=/app -e FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker ... python3 /tmp/erdos11-prove-supplement.py`, exit 0. Each log prints its actual Spec directory.

Supplemental coverage (all actually reached):

1. Manifest/artifact validation, independent precompiled ExpectedType/transitive dependency audit; original candidate compiled as ubuntu; complete type matches; original candidate rejected by axiom audit for `sorryAx`; sorry canary detects `sorryAx`.
2. A helper `def Erdos11.Odd (_ : ℕ) : Prop := False`, with the frozen Target prefix/header unchanged and proof `cases hn`, passes source rules and ubuntu compilation and has no forbidden axioms. The actual full-type check rejects it with a Lean type mismatch (genuine `Odd` versus helper `Erdos11.Odd`).
3. Frozen prefix change and added out-of-bounds Lean source are rejected by actual checker functions.
4. A compiled same-name fake FCBTrustedSpec in candidate source/artifact and `.lake` cache, plus ambient LEAN_PATH override, does not replace the trusted import. `--deps` resolves `/tests/trusted_spec/FCBTrustedSpec.olean` (or local `/opt` path); actual independent audit and full-type comparison still pass.
5. Missing compiled artifact, corrupted artifact hash, and corrupted manifest explicitly fail. No artifact is regenerated; no source fallback occurs.

The successful-proof/reward-1 branch is deliberately not tested: no proof of the open target was constructed or included. Placeholder fixtures are used only to cover the downstream checks and are correctly rejected by theorem axiom audit. No remaining infrastructure path required by the skill was left blocked.

## Other checks and cleanup

- Search-path command was run on the final container with all three specified roots; exit 0, located the package definition of `Squarefree`. See `search-path.log`.
- Skill Unicode script: final `no_issue`, both checkers verified original and malformed-header cases (`unicode.json`).
- Statement and public-proof research are recorded separately in `research.md`; only metadata was marked, not mathematics.
- Existing containers/images were recorded before creating resources. Cleanup is performed after report/artifacts are saved, on explicitly recorded own IDs/tags/network only; see `docker-cleanup.log` and final report note. The pre-existing generation base image and all other task/user resources are retained; no prune/cache deletion.
