# Infrastructure validation

Task: `erdosproblems-264-ii-prove`. No mathematical answer was supplied.

## Repair-time Spec

Created container `697c7c330f24cf6cdaa4e153e3c26f1e7bfe4e70128193fec8aec17fd011b9ba` (`fcb-264ii-spec-20261104`) from already-present trusted image `sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`. This base was reused, not created by this task and must not be removed. Checked its Lean 4.27.0 version and dependency-manifest hash against the task locks. Copied only golden inputs and repair-time generator to `/tmp/264ii-generation/`; no candidate or Lake config/cache was loaded during generation.

Command: `docker exec -u root fcb-264ii-spec-20261104 bash /tmp/264ii-generation/trusted_spec/reproduce.sh` (exit 0). Reproducible generator and command are delivered in both `trusted_spec/` packages. The parser/elaborator elaborates the complete trusted theorem, saves its type and universe parameters, rolls back the temporary theorem environment, and installs the definition `FCBTrustedSpec.ExpectedType`. No universe parameters exist for this target. The original named prefix definition is preserved. The earlier frozen `parts.i` placeholder remains in the prefix but is not a transitive dependency of ExpectedType or the relevant prefix definition. `AuditSpec.lean` independently imports the compiled module, checks definition/Prop identity, absence of the temporary target/children, full-proposition `rfl`, and transitive axioms. Only `propext`, `Classical.choice`, `Quot.sound` were found. See `tests/trusted_spec/audit.log` and its manifest for all input/source/artifact hashes, versions and dependency revisions.

Original golden Target SHA256: `98e49c1111792caaa667f3881b4b03b0e0ce3a5c6f5a95c61f60648afe06f142`.
Spec `.olean` SHA256: `ad6af205bc71be1809100c7bae5031ecbbb0cad4446a527a39e1bed0454efabb`.
Pinned manifest SHA256: `f3262c5ba4d34267b4d1a18d3db2e1f0fe5c372958c24e177de0ec1c326ca686`.

## Final local Harbor build and entries

Independently read Harbor CLI help. Final command:

```
harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-264-ii-prove --agent nop --env docker --trial-name fcb-264ii-final2-20261104 --trials-dir /tmp/264ii-harbor-trials --no-delete --environment-kwarg keep_containers=true --extra-docker-compose /tmp/264ii-compose-final-network.yaml
```

Harbor built from the **current local task**, not a registry task. Final image `fcb-264ii-final2-20261104__env-main:latest`, ID `sha256:30c8bcd3d12714a1b972ecebda3d7eb65abf79ea594c0590ecca16a97f88b748`; container `8b1d12ecd60f` (full ID recorded in `final-container.txt`). The Dockerfile ends in `USER ubuntu` and `RUN lake build +FormalConjecturesBench.Target`; successful cached build layers retained this validation. No extra upstream import was present.

Initial Harbor networking failed because Docker's automatic pools were exhausted. Used task-owned explicit subnets without deleting existing networks. A later final rebuild initially tried to reuse the older task-owned subnet while its retained container existed and got overlap; the final successful trial uses its own `10.204.65.0/24`. `--no-delete` alone still removes containers in this Harbor version; discovered and used `keep_containers=true`, which retains a stopped container. Restarted that same final Harbor container for additional checks. No extra capabilities, Docker socket, or host dependency mounts were added.

Harbor supplied `/tests` at verification and `/logs/verifier`. `integrity.json` confirms every uploaded tests file, both checker copies, both Spec packages and golden hashes match the local task; original Target/golden/GoldenCheck remain unchanged. `entrypoints.log` records `/tests/test.sh` setting `FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests`, and `/app/check.sh` using `/opt/formal-conjectures-bench-checker`. The two package paths are verified independently, not runtime cross-compared.

`docker exec -u root 8b1d12ecd60f bash /tests/test.sh`: exit **1**, reward **0**, original `sorry` rejected at the source gate.
`docker exec -u ubuntu 8b1d12ecd60f bash /app/check.sh`: exit **1**, same expected source rejection.

These are expected incomplete-proof results, not a successful proof of the theorem.

## Supplemental actual-checker coverage

`docker exec -u root 8b1d12ecd60f python3 /tmp/erdosproblems-264-ii-prove-supplement.py`: exit **0**; retained reproducible harness `supplement.py` and output `supplement.log`.

For **each** actual checker package (`/tests` and `/opt`), called its real functions without changing the official checker or public task:

- Frozen files/tree/ordinary source checks pass; frozen-prefix change, altered header and an outside-subtree source are rejected.
- Original `sorry` is rejected by the source gate.
- Manifest/artifact/golden/toolchain/dependency validation loads the fixed precompiled Spec; independent type/value/universe/axiom audit succeeds.
- A fresh isolated fixture retaining the original placeholder compiles through the real candidate build as ubuntu; complete type comparison succeeds; actual target axiom audit then detects and rejects `sorryAx`.
- Sorry canary executes and detects `sorryAx`.
- A competing `FCBTrustedSpec.olean` in candidate root and `.lake/build/lib/lean`, plus candidate `LEAN_PATH`, `LEAN_SYSROOT`, and `ELAN_TOOLCHAIN`, cannot replace the trusted Spec. Actual `--deps` reports the trusted package location; complete comparison continues to succeed.
- A benign external precompiled module still imports normally after fixed trusted paths. No general dependency whitelist was introduced.
- Legal helper `Erdos264.Nat.factorial` shadows the unmodified header's `Nat.factorial`. The temporary target successfully compiles with the changed type, but actual full type comparison rejects it. Printed candidate type is `Erdos264.IsIrrationalitySequence Erdos264.Nat.factorial`, not the pre-elaborated expected proposition.
- Removing or corrupting the compiled Spec fails explicitly before loading. No runtime regeneration or source-compilation fallback occurs.

The fixture's placeholder is deliberately not a submitted proof: the axiom audit rejects it. No original full proof was constructed; the accepted-final-proof path is not claimed. All required later infrastructure paths were independently reached rather than inferred from the original early exit.

## Static and other checks

`integrity.json`: two checker ASTs parse; synchronized packages identical; all delivered package and uploaded tests hashes match. `unicode.json`: skill script reports `no_issue` for this exact task, including baseline checks and negative header tests. `instruction-search.log`: the explicit three-path rg command found Mathlib's factorial definition (exit 0). `research.md`: steps 5 and 6 source review and searches. Docker resource inventory/cleanup is recorded separately; only explicitly created task resources are owned by this repair.
