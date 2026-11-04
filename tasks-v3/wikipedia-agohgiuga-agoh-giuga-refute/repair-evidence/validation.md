# Infrastructure verification

No proof of the open mathematical target is claimed or supplied.

## Repair-time generation

- Recorded pre-existing Docker containers/images before creating resources;
  copies: `existing-containers.txt`, `existing-images.txt`.
- Built from this task's Dockerfile:
  `docker build --progress=plain -t fcb-agoh-refute-spec:20261104 <task>/environment`.
  Cached trusted upstream layers were reused. The final `USER ubuntu` build
  succeeded; there are no additional upstream Target imports.
- Created `fcb-agoh-refute-spec-20261104` from that image and copied trusted
  `tests/golden_env` plus generation tools into an isolated `/tmp` project.
  Ran `bash trusted_spec/reproduce.sh` as ubuntu. No candidate sources, Lake
  configuration or caches participated in extraction. It elaborates the full
  golden declaration, restores the pre-declaration environment, and exports
  only its type value. `AuditSpec.lean` confirms the temporary theorem is
  absent, there are no universe/outer parameters, and ExpectedType plus both
  prefix definitions transitively use only approved standard axioms.
- The compilation warning about the temporary `sorry` is expected; the
  independent import audit verifies that the placeholder proof is not in
  ExpectedType or its transitive dependencies.
- Two identical bundles, including Lean source, generation code, `.olean`,
  `.ilean`, audit log and manifest, are in `tests/trusted_spec` and
  `environment/data/checker/trusted_spec`.
- Manifest SHA256 pinned in both checkers:
  `df4346a78e8dd655bb5d11acbb9bf5ca50e84937956dee6ea4f8136de4eac536`.
  Input/artifact hashes, platform, toolchain and dependency revisions are
  recorded there. Golden Target SHA256:
  `819ba9cb9e88ec077f31b79e218c2a73047e700b6715c89f1ddcea996a383f2c`.
- Toolchain: Lean 4.27.0, commit
  `db93fe1608548721853390a10cd40580fe7d22ae`, x86_64-unknown-linux-gnu.

## Actual Harbor build and entrypoints

Read `harbor --help` and `harbor run --help` locally. Command family:

```
harbor run --path <absolute-task> --agent nop --env docker \
  --no-delete --force-build --ek keep_containers=true \
  --extra-docker-compose /tmp/agoh-refute-compose-network.yaml \
  --n-concurrent 1 --job-name agoh-refute-repair-accept-20261104 \
  --jobs-dir /tmp/agoh-refute-harbor --debug
```

Initial attempt could build but network creation failed because the daemon's
predefined address pools were fully subnetted. Existing resources were NOT
removed. Read existing network subnets and used an unoccupied task-specific
`10.249.183.0/24` via a temporary Compose IPAM overlay. No socket mounts,
privilege changes or extra host dependencies. A retry verified the formal
entry; the final retained trial used `keep_containers=true` (on this Harbor
version `--no-delete` alone still removes the container while retaining the
image).

Final Harbor trial: `wikipedia-agohgiuga-agoh-giuga-r__YAeioH8`.
Final image:
`wikipedia-agohgiuga-agoh-giuga-r__yaeioh8__env-main:latest`, ID
`sha256:e2ffddc500f20c5d005c6d942f96a7e75740710fba784ea9a3ee72b427cd431a`.
Final child container: `1a009cd80ef8` (full ID in resource evidence).

Harbor uploaded `/tests`, provisioned `/logs/verifier`, and invoked
`/tests/test.sh`. It exited 1, reward 0, explicitly rejecting the original
`sorry` before Spec loading. Independently reran `bash /tests/test.sh` in the
same child (exit 1), then `bash /app/check.sh` as ubuntu (exit 1, same reason).
Inspected entrypoints: formal sets FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests;
local sets FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker. Complete hashes
of both checker copies, all bundle files, and both golden trees match the
host (`full-hashes.json`). No checker or bundle was placed in the candidate
editable source tree.

## Supplemental coverage in the SAME Harbor child

`python3 /tmp/agoh-refute-supplement.py` as ubuntu: exit 0. It imports and
calls the actual uploaded checker functions, without editing or relaxing the
checker. All fixture edits occur in disposable projects, never `/app` or
trusted golden inputs.

- Frozen baseline accepted; frozen-prefix change and header change rejected.
- Original banned sorry, new axiom syntax, out-of-tree Lean file rejected.
- Fixed `/tests/trusted_spec` manifest, artifacts, dependency revision,
  toolchain/platform checked; independent trustworthy type audit succeeds.
- Original placeholder fixture compiled as ubuntu; full type comparison
  succeeds and theorem axiom audit explicitly rejects `sorryAx`.
- Actual sorry canary succeeds, detecting `sorryAx`.
- A fixture-only local variable named `AgohGiugaCongr` leaves the entire
  original target header text unchanged but produces full type
  `∀ (AgohGiugaCongr : Prop), ¬ AgohGiugaCongr`. The actual complete-type
  check fails with Lean's Type mismatch against fixed ExpectedType. This is
  a deliberate transient context test, not an accepted public submission.
- Same-name candidate `FCBTrustedSpec.lean`, fake `.lake/.../FCBTrustedSpec.olean`,
  and hostile LEAN_PATH/LEAN_SYSROOT do not mask `/tests/trusted_spec`:
  actual Lean `--deps` resolves the uploaded Spec; complete comparison passes
  again after restoring the baseline fixture.
- Missing `.olean` and corrupt `.olean` in isolated trusted-package fixtures
  fail explicitly before Lean compilation and are not regenerated.

`python3 /tmp/agoh-refute-local-supplement.py` as ubuntu: exit 0. It repeats
fixed-package load, trusted type audit, ubuntu compilation, complete-type
comparison, expected sorryAx rejection and canary using the actual local
checker and `/opt/.../trusted_spec`, rather than the uploaded package.

Additional `lake build +FormalConjecturesBench.Target` in /app as ubuntu:
exit 0. Package-source search for `^def bernoulli` through the corrected
three-path command: exit 0 and a Mathlib package source match.

Static verification: both checker ASTs parse; original banned patterns,
frozen hash, target name and header are unchanged; public Target, golden and
GoldenCheck are byte-identical to repository originals; packages/checkers
are synchronized; Dockerfile ends with the ubuntu dependency build.
Unicode script run twice: `case=no_issue`, both checkers passed.

## Coverage boundaries

The full mathematical proof success/reward-1 branch was not exercised:
the unchanged public target remains a placeholder. Positive type acceptance,
negative type mismatch, target sorryAx rejection and canary were actually
executed, not inferred from early exits. The semantic repair concerns the
identity/source of fixed Spec and full-type comparison, not arbitrary
compiler execution or universal import sandboxing.

Resources were saved before cleanup. `cleanup.log` records cleanup of only
this task's containers, four tagged images and retained network, followed
by inspect-based absence checks. Existing/shared images and build caches
were not pruned.
