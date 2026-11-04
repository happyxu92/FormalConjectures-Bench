# Infrastructure acceptance

## Repair-time Spec

- Resource baseline: `/tmp/erdos1-prove-existing-{containers,images}.txt` (also saved here).
- Reused pre-existing trusted cache image `fcb-local/erdosproblems-1-least-n-5:cache-smoke`
  (`0824de0f1647`); did not alter or delete it. Generator reads only this task's
  golden source; the compiler's import path excludes `/app` and the cached checker.
- Created container `erdos1-prove-spec-20261104`, ID
  `6bcd8f485a2d23318338981ac7b177d683ae55b9ab277b74a5bff653609ab5b2`.
- Copied this task's tests to `/tmp/erdos1-prove-build` inside that container.
  Executed `docker exec -u root erdos1-prove-spec-20261104 bash /tmp/erdos1-prove-build/trusted_spec/reproduce.sh` (exit 0),
  then `python3 .../trusted_spec/make_manifest.py` (exit 0).
  Initial generation under the image's default ubuntu user failed to write the
  root-owned copied directory; rerunning repair-time generation as root fixed
  this without changing any delivered permissions or candidate execution user.
- Lean 4.27.0, x86_64; pinned upstream commit `233a10e857ef78e79fd9fe661d37db724089170a`;
  Mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`.
- Golden Target SHA256 `dcf555b05172a3390e0af4035232a11319845ebcac0977d8d3332aac5c8a211b`.
  Spec olean SHA256 `17fca04efbf81a2c355188da7020c1df4f8eaed9af0ffe9afa2423fb2d9c8fe1`.
  Pinned manifest SHA256 `abe93840c98d1c0831caf5f6f700870d0496ab500da21d3cb57f677ac81486c7`.
- Generator elaborates the entire trusted declaration, extracts `ConstantInfo.type`
  and ordered level parameters, then restores the environment before exporting
  `FCBTrustedSpec.ExpectedType`. Ordered universes: `[]`. The target placeholder
  is absent from the delivered environment. Recursive audits of ExpectedType and
  IsSumDistinctSet allow only propext/Classical.choice/Quot.sound, never sorryAx.
  `trusted_spec/audit.log` records the complete expected proposition.

## Actual local Harbor build and entries

Independently inspected `harbor --help`, `harbor trial start --help` and
`harbor run --help`. All trials use the current local task path, not a registry.
Initial successful trial: `erdos1-prove-repair-20261104`, nop, docker, --no-delete.
Harbor removes containers with --no-delete unless `keep_containers=true`; the
first container `d855e424b6958bfa9ec9ce249d85914f14ab25825685fb8fce9e442d468d8902`
was automatically removed. Repeated using the documented environment-kwarg hook:
`erdos1-prove-accept-20261104`, --environment-kwarg keep_containers=true;
container `7b40a2211a7123c66be8066d9eaadbe7b66178b635911fedc9c51a0c4720a03a`.

After metadata updates, repeated local Harbor build. Trial
`erdos1-prove-final-20261104` built successfully but could not allocate a default
Docker subnet (predefined address pool exhausted). No other agent/user network
was removed. Retried reusing only our already-created acceptance network through
`/tmp/erdos1-prove-network-overlay.yaml` (external default network named
`erdos1-prove-accept-20261104__env_default`), without new mounts, privileges or
host dependencies:

```
harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-1-erdos-1-prove --trial-name erdos1-prove-final-net-20261104 --trials-dir /tmp/erdos1-prove-harbor --agent nop --env docker --no-delete --environment-kwarg keep_containers=true --extra-docker-compose /tmp/erdos1-prove-network-overlay.yaml
```

Final container `c80886711f9374ad9f4002f25dced0593c9fa9708690239ef55c6983f4e893fe`;
image `erdos1-prove-final-net-20261104__env-main:latest`, ID
`28aef9acd14a2fd32509c6a590a83b996943fcfda982fe3a472587a5c50ef3e8`.
Dockerfile retains its final ubuntu `RUN lake build +FormalConjecturesBench.Target`;
no extra upstream imports exist. After Harbor stopped the retained container,
restarted it with `docker start` for checks in the same child container.

- `/tests` was uploaded by Harbor. All local/remote golden files, both checkers,
  both Spec packages and pinned hashes matched (final-static log, exit 0).
- `docker exec ... bash /tests/test.sh`: exit 1, reward 0, expected original sorry rejection.
- `docker exec -u ubuntu ... bash /app/check.sh`: exit 1, same expected rejection.
- Formal script sets FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests; local script uses
  /opt/formal-conjectures-bench-checker. Neither regenerates/recompiles the Spec.
- Independent `supplement.py` imports the actual checker functions and executes
  them with an isolated original placeholder fixture. Root invocation with
  FCB_TESTS_DIR=/tests: exit 0. Ubuntu invocation using the /opt local package:
  exit 0. Both cover trusted loading and recursive audit, ubuntu candidate
  compilation, full type match, rejection of target sorryAx, and sorry canary.
- Negative tests: frozen prefix mutation, outside-subtree Lean source, unchanged
  header with a high-priority real multiplication instance (candidate compiles,
  complete type check rejects), same-name candidate Spec/cache and ambient
  LEAN_PATH (trusted module wins), missing olean and corrupted olean (explicit
  failure; no regeneration).
- Three-path package source search (`rg --glob '*.lean' '^def sum ' /app
  /opt/formal-conjectures /opt/formal-conjectures/.lake/packages`): exit 0,
  finds Mathlib/Data/Fin/Tuple/Reflection.lean and other package definitions,
  no permission/path errors. The instructional multiline command is valid bash.
- Static AST/package equality and Unicode skill script pass. Frozen golden,
  public Target, original header/prefix hash, and GoldenCheck.lean unchanged.

This verifies infrastructure, not a proof of the mathematical target. No completed
original-proof/reward-1 branch is claimed. Logs are retained alongside this file.

Own image tags (all deleted after report was saved; absence verified):
- erdos1-prove-repair-20261104__env-main:latest / ccd56fa04eb01c09d996aa7eebf8545c20d6818874c020192bc253cb87cccedc
- erdos1-prove-accept-20261104__env-main:latest / 868cd1d046f89c7e9ac70443ece3220c8a009dd6ba95da0b3546fbef81c21e90
- erdos1-prove-final-20261104__env-main:latest / 963dc74d24fcdc701ef891cd7a30eb7850609db853225620e6fc11839e1a8635
- erdos1-prove-final-net-20261104__env-main:latest / 28aef9acd14a2fd32509c6a590a83b996943fcfda982fe3a472587a5c50ef3e8

Cleanup completed: all three retained/temporary containers stopped and removed,
the first Harbor container already absent, all four image IDs absent on inspect,
and the task-owned acceptance network removed. No task containers/networks remain.
The pre-existing cache image is still present, and no shared image/cache or user
container was deleted. See `docker-cleanup.log`.
