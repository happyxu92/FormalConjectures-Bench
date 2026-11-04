# Infrastructure validation

Only this task was modified. Public Target, both golden trees, frozen hash and
header, and both GoldenCheck.lean files were preserved.

## Commands / generation

- Step 1: the three-path rg command with `def TendstoLocallyUniformlyOn` ran as ubuntu in the final Harbor container, exit 0; see accept-search.log.
- Step 2: no extra upstream import exists. Added the final `RUN lake build +FormalConjecturesBench.Target` after `USER ubuntu`, HOME and permissions. First actual local Docker build succeeded (spec-build.log); final Harbor image uses the same Dockerfile and precompiled dependencies. Original sorry warning is expected, not suppressed.
- Step 3: `cd /root/FormalConjectures-Bench/skills/lean-task-repair && python3 /root/FormalConjectures-Bench/skills/lean-task-repair/scripts/check_unicode_header.py /root/FormalConjectures-Bench/tasks-v3/erdosproblems-247-erdos-247-refute`: exit 0, case no_issue; original/changed headers and missing assignment boundary tested by supplied script.
- Generation: `docker build -t fcb-247-refute:spec-20261104 -f /root/FormalConjectures-Bench/tasks-v3/erdosproblems-247-erdos-247-refute/environment/Dockerfile /root/FormalConjectures-Bench/tasks-v3/erdosproblems-247-erdos-247-refute/environment`; run the named network-none Spec container, copy trusted tests into /tmp/247refute-bundle, execute trusted_spec/reproduce.sh. The first attempt exposed a trailing declaration doc-comment attached to run_cmd; the generator was fixed and generation/audit rerun successfully. No candidate source/config/cache participated.
- The generator elaborates the entire trusted theorem in a temporary environment, retains info.type and info.levelParams, restores the original environment, and exports a definition with the complete type as value. No axiom or string-defined proposition. Independent audit checks the exported definition, zero universe parameters, absence of temporary theorem/children, and transitive standard-axiom dependencies. There are no task-local prefix definitions. Lean version, platform, dependency revisions, golden/source/artifact hashes are in both identical manifests.

## Final current-task Harbor acceptance

```
harbor run -p /root/FormalConjectures-Bench/tasks-v3/erdosproblems-247-erdos-247-refute \
  -a nop -e docker --no-delete --force-build --ek keep_containers=true \
  --extra-docker-compose /tmp/247refute-network-final.yaml \
  --job-name fcb-247-refute-harbor-accept-20261104 \
  --jobs-dir /tmp/247refute-harbor-jobs --n-concurrent 1
```

Harbor CLI help was read independently (harbor-run-help.txt). Its `--no-delete`
still removes containers in this installation; `keep_containers=true` preserves
and stops them, allowing the required same-container supplemental checks. An
initial network creation failed because Docker default address pools were
exhausted. Only this task's compose overlay added explicit subnets; no existing
network or container was deleted to make room. No socket or extra host dependency
mounts, privilege escalation or old registry task image were used.

Final image: sha256:3afa52552535260f8855308cb4f3a5cea78012a0eccdb66a68de55faaeb1da0f.
Final Harbor container: 19efd808f0ae22adff44cd6ec5fb3d725c3c7cab036c384184c7a61823fc47cd.
Harbor trial: erdosproblems-247-erdos-247-refu__6hDmByQ.
Harbor ran the verifier and reported reward 0, with no environment exception.
After restarting its retained container:

- `docker exec -u root 19efd808f0ae bash /tests/test.sh`: exit 1, reward=0, expected banned sorry. test.sh explicitly sets FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests.
- `docker exec -u ubuntu 19efd808f0ae bash /app/check.sh`: exit 1, expected banned sorry, using /opt/formal-conjectures-bench-checker.
- `/tests` did not exist in the image's agent-stage /app copy: Harbor provides it in verifier stage by upload; the retained container had no host bind mounts. All 33 hashes for checker, golden trees, GoldenCheck, Target, and both Spec packages were compared to local files (accept-hashes.log), and matched. Checker AST and TOML parsed; both checker files and all package bytes matched.

## Supplemental coverage (same final Harbor container)

`docker cp repair-evidence/supplement.py 19efd808f0ae:/tmp/247refute-supplement.py`
then run as root against `/tests`, and independently as ubuntu with argument
`/opt/formal-conjectures-bench-checker`. Both exit 0. Earlier local fixture output
used a root-owned results filename and failed after all checks; that test-only
output path was corrected to include uid and both entire suites rerun to exit 0.

The supplemental driver calls actual checker functions, without modifying or
relaxing official checks:
- fixed package hash/version/input validation and independent type/axiom audit;
- ubuntu candidate compilation with original sorry confined to a temporary fixture;
- complete type equality against the compiled ExpectedType value;
- target axiom audit rejects sorryAx;
- sorry canary detects sorryAx;
- changed frozen prefix rejected;
- original sorry syntax rejected;
- outside-editable source rejected in isolated checkout;
- normal helper definitions/imports still compile;
- identical frozen target text with a helper defining Erdos247.Transcendental compiles, but full-type comparison rejects the changed meaning (actual Lean type mismatch logged);
- fake candidate FCBTrustedSpec source/olean and .lake cache plus inherited LEAN_PATH do not change actual --deps resolution or imported Spec identity;
- missing/corrupted precompiled artifact copies fail explicitly and their files remain unchanged (no runtime generation).

The public proof is unfinished, so official entry never reaches later proof
checks; these paths were actually exercised separately, not inferred. No complete
original proof is claimed. Ordinary external import/initializer sandboxing is
outside the requested scope and was not tested.

See resources.json and cleanup.json for explicitly owned resource identities and
post-report cleanup, without attributing concurrent resources by global diff.
