# Infrastructure verification

This is not a proof of the conjecture. Public Target, both golden trees, GoldenCheck.lean and frozen prefix/header were preserved. Existing source bans, confinement, frozen-file audit, target axiom audit and sorry canary remain called by `main`.

## Generation

- `docker build -t fcb-fermatcatalan-spec:20261104 /root/FormalConjectures-Bench/tasks-v3/wikipedia-fermatcatalanconjecture-fermat-catalan-prove/environment` (exit 0). Final Dockerfile command builds Target as ubuntu; no extra upstream imports exist.
- `docker run -d --network none --name fcb-fermatcatalan-spec-20261104 fcb-fermatcatalan-spec:20261104 sleep infinity`; container `57490cb48b32055261cf8019c5b83d6c4f89924dd56cec18c378911d956c9729`.
- Copied original `tests/golden_env` and generation sources to `/tmp/fermatcatalan-generation/` in this container. Ran `docker exec -u root ... bash /tmp/fermatcatalan-generation/trusted_spec/reproduce.sh` (final exit 0).
- Generation uses the locked Lean binary directly, with only trusted upstream precompiled libraries and the generation directory in LEAN_PATH. No candidate Submission, Lake configuration or cache is loaded. A first attempt exposed a Lean doc-comment attaching to `open` rather than a theorem; generation now omits that final theorem documentation comment (not any definitions), and was rerun successfully.
- Lean: 4.27.0 / db93fe1608548721853390a10cd40580fe7d22ae, x86_64 Linux. Upstream 233a10e857ef78e79fd9fe661d37db724089170a, Mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900.
- `tests/trusted_spec/manifest.json` records original golden hashes, all artifact/source hashes and dependency revisions. Its pinned SHA256 is `8e2e068b60a50b79e705d61f9eeb28d16b94595111950ffac2a1c521dbe16d09`.
- The parser/elaborator extracts the original declaration's **type**, restores the previous environment, and exports a definition value `FCBTrustedSpec.ExpectedType`. No target theorem or placeholder proof is exported. Audit checks exact value, Prop sort, zero binders, empty universe list, and transitive axioms of ExpectedType plus all three prefix definitions. Only propext/Classical.choice/Quot.sound occur. See package `audit.log`.
- Both package directories contain identical source, generation code, `.olean`, `.ilean`, audit and manifest. They are repair-time products; verifier never runs generation or invokes a Spec source fallback.

## Fixed verifier loading

Formal entry loads `SPEC_DIR = /tests/trusted_spec`; local `/app/check.sh` loads `/opt/formal-conjectures-bench-checker/trusted_spec`. Each validates its pinned manifest, golden input, artifact hashes, version, architecture and dependency revision manifest. Locked LEAN_PATH puts that fixed package and trusted dependencies before the fresh candidate project; caller environment and candidate Lake configuration/cache do not select trusted modules. The unused, nonexistent Cli build path from Lake is not needed; all existing dependency libraries and ordinary editable Lean helper imports remain available. No new general dependency whitelist or compiler/plugin sandbox was introduced.

Only the temporary Target imports Spec before Submission, reuses Spec's original prefix definitions and restores the original `open scoped Function` / namespace context. Complete type comparison references the already-elaborated ExpectedType value, not a re-parsed proposition string. GoldenCheck remains untouched and is no longer executed for type comparison.

## Actual local Harbor acceptance

Read Harbor top-level/run/trial help and inspected the DockerEnvironment `keep_containers` option. Used `nop`, never a second pi agent.

Final successful command:

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/wikipedia-fermatcatalanconjecture-fermat-catalan-prove --agent nop --env docker --no-delete --force-build --ek keep_containers=true --extra-docker-compose /tmp/fcb-fermatcatalan-compose-final.yaml --job-name fcb-fermatcatalan-final2-20261104 --jobs-dir /tmp/fcb-fermatcatalan-harbor -n 1 --debug
```

Final trial `wikipedia-fermatcatalanconjectur__QNL3U4m`; container `06d7d99367f6`, image `wikipedia-fermatcatalanconjectur__qnl3u4m__env-main:latest`, ID `sha256:7a604efb0e6d8ba4ca94e77942eee2387bf40a4489d3473347d3b0ca37e807b9`. This is built from the current local task environment, not a registry replacement. Image history retains the final ubuntu `lake build +FormalConjecturesBench.Target`. Harbor uploaded `/tests`, including Spec, and provided `/logs/verifier`.

After Harbor stopped the retained container, started this same child again and ran:
- `docker exec 06d7d99367f6 bash /tests/test.sh`: exit 1, reward 0, original `sorry` rejected by source checks (expected).
- `docker exec -u ubuntu 06d7d99367f6 /app/check.sh`: exit 1 for the same expected reason.
- Hashes of **all** delivered tests/checker/Spec/golden files match local files at both container locations (`container-hashes.json`). Entry source and reward are in `entry-evidence.txt`.
- Exact instruction search (`rg --glob '*.lean' '^def IsEvenlyCovered' /app /opt/formal-conjectures /opt/formal-conjectures/.lake/packages`) exits 0 and finds Mathlib's definition (`package-search.log`).

### Supplemental paths after expected early exit

`repair-evidence/supplement.py` imports the actual unmodified checker module and calls its actual functions. It ran in the **same final Harbor child**, once against `/tests` and once entirely as ubuntu against `/opt/...-checker`, both exit 0:

```
docker exec -e FCB_TASK_DIR=/app -e FCB_TESTS_DIR=/tests 06d7d99367f6 python3 /tmp/fcb-fermatcatalan-supplement.py
docker exec -u ubuntu -e FCB_TASK_DIR=/app -e FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker 06d7d99367f6 python3 /tmp/fcb-fermatcatalan-supplement.py
```

Covered stages:
1. Fixed Spec validation and independent full-type/prefix transitive axiom audit pass.
2. Original placeholder fixture compiles as ubuntu and passes complete type comparison.
3. Target axiom audit actually rejects `sorryAx`; separate sorry canary passes.
4. Candidate same-name `.lean`/bogus `.olean` and `.lake/build/lib/lean/FCBTrustedSpec.olean`, plus an injected LEAN_PATH, cannot replace Spec. `--deps` resolves the fixed validated artifact and full-type comparison still passes.
5. Semantic negative retains exact frozen prefix and theorem header in the fixture. A scoped helper notation in namespace Function changes the candidate proposition to True; candidate compilation succeeds, `#check` shows True, and the **actual full-type comparator rejects** it against ExpectedType. The preserved source ban independently rejects this notation. The deeper-stage fixture intentionally tests that comparator separately; no formal check was disabled or modified.
6. Frozen prefix modification and an added out-of-tree Lean file are rejected.
7. Missing and corrupt precompiled Spec `.olean` files fail hash/artifact validation without regeneration; tests assert the artifact is not recreated or altered.

See `formal-supplement.log` and `local-supplement.log`; both end `ALL SUPPLEMENTAL CASES PASSED`. No proof-dependent success/reward=1 path is claimed or required. Final AST/package equality, TOML/JSON validation and unchanged Target/golden checks pass.

## Build/retention obstacles and resource scope

Before creation, recorded `docker-before.txt`. No existing user or other task resources were claimed by a global diff.

- First Harbor image `...rfssgfr...` built, but Docker's default address pools were exhausted. Read existing subnets and used an explicit task-owned subnet, without changing daemon configuration, privileges or mounts.
- Retry `...ghptzwu...` built and ran the formal verifier (reward 0), but `--no-delete` alone removed its container. Added the supported `keep_containers=true` option. The removed retry container ID was not captured before Harbor removed it; no container with that project remains (event history no longer retained those events).
- Retained acceptance `...cehkusy...` used 10.249.174.0/24 and passed both supplemental runs.
- A final rerun after metadata marking first collided with that still-retained **own** subnet (`...twksdgf...`, no container created). The final successful child uses separately checked, nonoverlapping 10.248.174.0/24. Other agents' networks were not removed.
- `created-images.txt` records all six task-created image IDs/tags. Three retained task containers were created: Spec `57490cb48b32`, first retained acceptance `899350249b68`, final acceptance `06d7d99367f6`. Cleanup happens only after this evidence and the report have been saved; results are in `docker-cleanup.log` and repair-report.json.
