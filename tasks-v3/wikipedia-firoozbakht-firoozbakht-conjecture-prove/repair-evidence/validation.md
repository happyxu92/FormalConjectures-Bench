# Infrastructure validation

All commands target only this task. Docker resources existing before work were
recorded in `docker-before-containers.txt`, `docker-before-images.txt`, and
`docker-before-networks.txt`; these are inventory only, not ownership inference.
No shared cache or existing resource was deleted.

## Generation

```
docker build -t fcb-firoozbakht-prove-spec:nt40-20261104 /root/FormalConjectures-Bench/tasks-v3/wikipedia-firoozbakht-firoozbakht-conjecture-prove/environment
docker run -d --name fcb-firoozbakht-prove-spec-nt40-20261104 --user root fcb-firoozbakht-prove-spec:nt40-20261104 sleep infinity
```

Image build exit 0, including the final `USER ubuntu` Target build. Only the two
standard imports occur in Target, so no extra upstream module was required.
Golden and repair-time generator inputs were copied to an isolated container
`/tmp/fcb-firoozbakht-prove/tests/`, then `bash ./reproduce.sh` ran in its
`trusted_spec/`. No candidate source, config or cache participated in extraction.
An initial Lean failure caused by a theorem docstring preceding the extraction
command was fixed by removing only that trailing docstring from generated input;
the successful generation/audit exit was 0. The temporary theorem is explicitly
removed from the environment before ExpectedType is exported. Its placeholder
warning is not a delivered axiom dependency: independent audit finds only
`propext`, `Classical.choice`, `Quot.sound` for ExpectedType and the prefix
`Firoozbakht.firoozbakhtSeq`, and verifies the temporary target is absent.

Artifacts/source/generator/audit and ordered universe list `[]` are in both
`trusted_spec/` packages. `manifest.json` records all hashes, toolchain/platform,
original golden files and pinned dependency revisions. Manifest SHA-256:
`9ed1030bd3d6e53f0d9aede14b2b5acf55a986209c2e1ef5f026337865ffb446`.
Original public and both golden Target SHA-256 remained:
`1cd75ed262e15fe969fa88eff1d7f1c80d0ebe3ff362a8e4d24d0c0cabce96b9`.

## Harbor current-local-task acceptance

CLI help was independently read (`harbor --help`, `harbor run --help`,
`harbor task start-env --help`). Runs used local `-p`, `-a nop`, no registry task,
no Docker socket or additional host dependency mounts.

The first local Harbor build succeeded but container startup failed because
Docker's predefined address pools were exhausted. Existing networks were
inspected, not pruned. A task-only Compose overlay selected the unused
`10.249.176.0/24` subnet and task-only image tag. A second run completed normally;
Harbor's `--no-delete` still removes containers unless `keep_containers` is set,
so the final acceptance used:

```
harbor run -p /root/FormalConjectures-Bench/tasks-v3/wikipedia-firoozbakht-firoozbakht-conjecture-prove -a nop --env docker --no-delete --ek keep_containers=true --extra-docker-compose /tmp/fcb-firoozbakht-prove-compose.json --job-name fcb-firoozbakht-prove-covered-20261104 --jobs-dir /tmp/fcb-firoozbakht-prove-harbor -n 1
```

Harbor exit 0, no trial exception, expected reward 0. Final local image:
`fcb-firoozbakht-prove-final:nt40-20261104`, ID
`sha256:ee2fb94774129850481fcdadb0175fd56b4d7ab4c012f2355b90a24a9c6ea5ff`.
Retained Harbor child:
`04fe2660756fad122355f262212184120d1a3ef9b20a27ee7e2fdfc3cc915c2a`,
`wikipedia-firoozbakht-firoozbakh__nrqmq2s__env-main-1`.
It was restarted after Harbor stopped it, for the following checks in the same
child. Harbor provided `/tests` by upload and `/logs/verifier` via its normal
mount. Hashes of 39 checker, Spec and golden files match local files in both
`/tests` and `/opt/formal-conjectures-bench-checker` (see container-hashes.json).

- `docker exec CHILD bash /tests/test.sh`: exit 1, reward.txt `0`, original
  `sorry` source rejected. Verified test.sh explicitly selects `/app` and `/tests`.
- `docker exec --user ubuntu -w /app CHILD /app/check.sh`: exit 1, same expected
  `sorry` rejection, selecting the `/opt` checker/Spec path.
- Supplemental local-checker calls under ubuntu: exit 0, explicitly loaded
  `/opt/.../trusted_spec`, audited it, compiled the temporary candidate,
  compared the full type and ran the sorry canary.
- Supplemental actual `/tests/test_target.py` functions: exit 0, 18 assertions,
  in `supplement.log` / `supplement.py`. No formal checks were disabled or edited
  to make the placeholders pass. Fixtures only call downstream functions
  independently to cover paths unreachable after the source-level rejection.

Covered paths: fixed Spec hashes/version/golden; expected-value and prefix
transitive axiom audit; true ubuntu compilation; correct full forall-type match;
original placeholder's axiom rejection (`sorryAx`); canary detection; frozen
prefix/header/assignment rejection; out-of-subtree source rejection; and an
unchanged-header semantic counterexample. The latter introduces only an allowed
`LT Real` instance with relation `True`, uses `by trivial`, compiles without
forbidden axioms, and is rejected specifically by complete type comparison.
Candidate same-name FCBTrustedSpec source/compiled module, fake `.lake` cached
module and ambient LEAN_PATH cannot redirect the fixed Spec import. Missing
olean, corrupt olean and changed manifest all fail explicitly without runtime
artifact generation. Normal helper declarations/import rules remain available;
this is not a general plugin or code-execution hardening claim.

No complete proof of the open conjecture was constructed or accepted. The main
entry's post-source-check success branch remains unavailable on the original
unfinished Target; its substantive later functions were actually exercised as
above, not inferred from the early failure.

## Static and other checks

Both checker ASTs parse; checker bytes and both Spec packages agree. Original
Target, golden trees and GoldenCheck.lean were not modified. Unicode script ran
before and after repair: exit 0 / `no_issue`, original headers pass, changed
headers and absent `:=` are rejected. Instruction search command now explicitly
covers `.lake/packages`; the actual command finds Mathlib's `Nat.nth` in
`Mathlib/Data/Nat/Nth.lean` with no path/permission error. Dockerfile still ends
with ordinary-user `lake build +FormalConjecturesBench.Target`.

See research.md for the separate statement/proof-source review. Cleanup is
performed only after artifacts/logs and repair-report.json have been saved;
its observed outcome is recorded in cleanup.log and the report.
