# Infrastructure validation

## Edits and invariants
- instruction.md now explicitly searches /app, /opt/formal-conjectures and /opt/formal-conjectures/.lake/packages. As ubuntu, the exact three-root search finds `def fract` in Mathlib/Algebra/Order/Floor/Defs.lean (exit 0).
- Target has no extra upstream imports. Dockerfile now ends, after copying/permissions, with `WORKDIR /app`, `HOME=/home/ubuntu`, `USER ubuntu`, `RUN lake build +FormalConjecturesBench.Target`. Actual ubuntu Lake build also exited 0, reporting the expected original sorry warnings. This is dependency verification, not proof acceptance.
- Skill Unicode script ran before semantic edits: `case=no_issue`, both original headers pass and modified headers/removal of := are rejected; no Unicode change was made.
- Original public Target, both golden Target copies and both GoldenCheck.lean files were compared against git HEAD and remain byte-identical. Frozen prefix digest and EXPECTED_HEADER values remain unchanged.

## Repair-time Spec generation
Trusted source: tests/golden_env, original Target SHA256 `694ff3c9fcb1b2b7e4153b265e54d4f278b04b9300a3ad397ac0d0af50ea1117`.

Reused preexisting compatible dependency image `erdos1062-import-20261102__env-main:latest`, ID `sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`. Created isolated network-none container `three-halves-refute-spec-nt40-143048` (`ad1816648a88488b4153ee8bf7d5304d9ec3b6349d86e81fa924efd1777a83e9`), copied only trusted golden_env and the repair-time generator into `/tmp/three-halves-refute-bundle`, then executed `bash /tmp/three-halves-refute-bundle/trusted_spec/reproduce.sh` as root, exit 0. This does not load candidate source, candidate Lake configuration or caches.

The parser/elaborator temporarily elaborates the whole original target declaration, extracts its `ConstantInfo.type` and ordered `levelParams`, restores the original environment, then kernel-checks and compiles a definition with that expression as value. Thus no regex-built proposition or new axiom is used. An independent AuditSpec import checks that the temporary target/children are absent, ExpectedType is a definition of a Prop, there are zero outer binders and zero universe parameters, and the expected type plus its two referenced task definitions have only allowed standard axioms transitively. The unrelated frozen subsequence lemma retains its original sorry, but is not a dependency of ExpectedType; the audit verifies this rather than rejecting all prefix declarations indiscriminately.

Lean: v4.27.0, commit db93fe1608548721853390a10cd40580fe7d22ae, x86_64-unknown-linux-gnu. Upstream Formal Conjectures: 233a10e857ef78e79fd9fe661d37db724089170a. Mathlib: a3a10db0e9d66acbebf76c5e6a135066525ac900. Dependency manifest SHA256: 5b99b5f4f807cbba67bbcd22e5e486c17d6a8d970ea218de08d05830ab350c26.

Same generated source, .olean, .ilean, audit source/log and reproducible generator/script are delivered under both trusted_spec paths. Manifest SHA256 `442df4804252367413f86b941b6afe4d6f9984b711217f8cd854d8cf5ab62c8b` is pinned in both identical checkers. Artifact hashes and all dependency revisions are recorded in that manifest.

## Checker behavior
Only trusted Spec loading, temporary verification assembly and full type checking/build support were changed. Original freeze, tree confinement, banned-source checks, target axiom audit and sorry canary remain called. Normal helper declarations/instances and ordinary dependency imports remain allowed.

SPEC_DIR is TESTS_DIR/trusted_spec, not /app. The pinned toolchain runs with explicit search order: verified Spec, trusted precompiled dependency libraries and finally the disposable candidate project. Candidate Lake configurations, inherited LEAN_PATH/LEAN_SYSROOT/ELAN_TOOLCHAIN and .lake caches are not consulted for Spec identity. Missing/hash-mismatched artifacts fail rather than recompile or generate. Candidate compilation drops to ubuntu even when the official checker starts as root. Temporary Target imports Spec before Submission and reuses its prefix constants under the original namespace/scoped context. GoldenCheck.lean is retained untouched but no longer copied/executed; complete type comparison references only compiled ExpectedType.

## Actual local Harbor builds and entries
Read `harbor --help`, `harbor run --help` and `harbor trial start --help` independently. Command family:

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/books-uniformdistributionofsequences-equidistribution-isequidistributedmoduloone-three-halves-pow-refute --agent nop --env docker --no-delete --ek keep_containers=true --job-name three-halves-refute-nt40-final-net --jobs-dir /tmp/three-halves-refute-harbor-jobs --n-concurrent 1 --extra-docker-compose /tmp/three-halves-refute-network-compose.yaml
```

`nop` is not another pi agent and supplies no solution. The environment is built from this local task, not a registry task image. BuildKit reused trusted dependency/cache layers. The Docker history/build transcript includes the final ubuntu dependency-validation RUN.

Initial Harbor attempt `SjudFHe` built successfully and ran verifier (reward 0); --no-delete still removes containers on this Harbor version. Read the local Harbor implementation to find `keep_containers=true`, then ran retained trial `3d6QyPA`, built image `sha256:d5c191dd5177fe1548640cc551446ecc1f7674603eeac469a3cc0c4efe194e37`, restarted its stopped container and completed both entrypoints and all supplemental tests there.

After metadata marking, an additional build `VEopKXD` succeeded but container startup hit exhausted Docker default address pools. No unrelated network was removed. Inspected existing subnets, supplied a task-only Compose IPAM override for 10.247.195.0/28, and reran current local task successfully as `DTTT9Np`.

Final image: `books-uniformdistributionofseque__dttt9np__env-main:latest`, `sha256:47eccb4a04fc87aa4725469fa8a203b87b677418079e16d089cfaf3434574e14`.
Final container: `c553fe101d69099fb1328992359919288492ba8c57d55ba6011d10f4b5cbd5ea`.
Final task-only network: `8868770806ab9cc45cac37439d0e6c473d41bd75adae8bcc62873d1045155c62`.

Harbor uploaded /tests and supplied /logs/verifier. Repeated in that same final Harbor container:
- `docker exec <id> bash /tests/test.sh`: exit 1, reward.txt 0, original target sorry banned (expected).
- `docker exec -u ubuntu <id> bash /app/check.sh`: exit 1, same expected sorry rejection.
- Independent supplemental script importing /tests/test_target.py's actual functions: exit 0.
- Independent local supplemental script as ubuntu importing /opt/.../test_target.py: exit 0.
- All /tests files and all /opt checker files, including every Spec artifact, golden and GoldenCheck, hash-match the local final files. Checker AST parses, checker copies and Spec package copies are byte-identical.

## Supplemental coverage after expected early exit
In isolated temporary projects, without altering official checker, public Target or golden:
1. Validate fixed precompiled Spec and execute its independent trusted-type audit.
2. Compile candidate as ubuntu; compare whole theorem type successfully for original sorry fixture.
3. Target axiom audit rejects actual sorryAx, not an assumed/predicted result.
4. Sorry canary actually detects sorryAx.
5. Add candidate same-name FCBTrustedSpec source and corrupt .lake cached module; set hostile LEAN_PATH, LEAN_SYSROOT and ELAN_TOOLCHAIN. `lean --deps` resolves the verified /tests product; independent Spec audit still passes.
6. Keep all original frozen text/header unchanged; add an allowed high-priority HDiv ℝ ℝ ℝ instance in Submission that returns 0. Candidate compiles, full type comparison actually rejects its changed type. Spec audit remains unchanged. The fixture uses an isolated placeholder solely to cover type checking, not a delivered proof.
7. Frozen prefix/header changes, out-of-subtree source, and changed frozen lakefile are rejected by actual checker functions.
8. Missing .olean and corrupted .olean in disposable package copies cause explicit load failures with no regeneration/recompilation.
9. Local /opt entry loads the same delivered package; ordinary `import Mathlib.Data.Nat.Basic` and helper lemma remain buildable.

No full mathematical proof was attempted or delivered. The official theorem-success/reward-1 branch is not claimed covered; all required downstream infrastructure branches are covered independently. Exact output and replay helper programs are stored alongside this note. Docker cleanup is recorded in cleanup.log and repair-report.json after artifacts/report were saved.
