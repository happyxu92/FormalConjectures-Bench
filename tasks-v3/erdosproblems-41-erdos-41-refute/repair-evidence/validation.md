# Infrastructure validation

Only this task was edited. No public Target, golden input, GoldenCheck.lean, frozen prefix hash, or theorem header was changed.

## Trusted generation

- Existing-resource inventory saved before creation: `/tmp/erdos41-refute-resources-before-containers.txt`, `/tmp/erdos41-refute-resources-before-images.txt`.
- Generation container `erdos41-refute-spec-20261104`, ID `4b4cda875bc120db4295c09013df75dc493c06c000b84de13d4b7b22f288e111`, network none, existing trusted image `sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`. No new generation image.
- Commands recorded in `trusted_spec/manifest.json`; repair-time `generate.py` extracts the complete elaborated declaration type and levelParams, restores the environment before exporting ExpectedType. Generation loads golden input with Submission import removed, not candidate source/Lake/cache.
- Generation/independent audit exit 0. Temporary target absent; ExpectedType and NtupleCondition transitive axioms allowed; no sorryAx dependency. Audit counts 5 universal binders inside Not, preserving the unused implicit type/instance and all hypotheses. Universe order `[]`.
- Lean 4.27.0, x86_64 Linux, formal-conjectures revision `233a10e857ef78e79fd9fe661d37db724089170a`, Mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`; input/source/artifact hashes and dependency revisions in manifest. Manifest SHA256 `11950479c32012913773bc4efe744d068cd048d6dd90d1c5316cd51ec4cdf933` pinned in both checkers.
- Both trusted packages byte-identical. Compiler artifacts successfully imported in final Harbor container from each delivered package location, not just in generation environment.

## Local Harbor builds and entries

Read `harbor --help`, `harbor run --help`, `harbor trial start --help`; inspected DockerEnvironment constructor for `keep_containers` option.

1. `harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-41-erdos-41-refute --agent nop --env docker --force-build --no-delete --job-name erdos41-refute-accept-20261104 --jobs-dir /tmp/erdos41-refute-harbor-jobs --n-concurrent 1`.
   Local image `erdosproblems-41-erdos-41-refute__jfbmxhw__env-main:latest`, ID `sha256:4418728046af95a6fa22b9581412aacc9b6f6e16d907b51185a05b59d117a4c0`. Harbor removed its container despite delete=false because keep_containers was not set.
2. `harbor trial start --config /tmp/erdos41-refute-harbor-config.json`, explicit task-local trial `erdos41-refute-accept2-20261104`, nop, force_build=true, keep_containers=true.
   Final local image `erdos41-refute-accept2-20261104__env-main:latest`, ID `sha256:58ec15ff9d66c27fbc9dbe688c58af99c6933d889cf3248b09cc2997d4bbfa59`; container `dfad47997b9b3f295eb36ae1da74b66f97ae3376bf1e749496ab6cb72e362447`. No old registry task substituted. Build used ordinary cached trusted base layers plus this task's current Dockerfile/data/checker/Spec.

Harbor stopped the kept container at trial end. Restarted that same container with `docker start` for supplemental checks (no socket or extra dependency mounts). Both entries then actually executed:
- `docker exec erdos41-refute-accept2-20261104__env-main-1 bash /tests/test.sh`: exit 1; `/logs/verifier/reward.txt` = 0; expected source rejection of original sorry.
- `docker exec -u ubuntu erdos41-refute-accept2-20261104__env-main-1 bash -lc 'cd /app && ./check.sh'`: exit 1; same expected sorry rejection.
- Formal shell sets FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests. Local shell sets /opt/formal-conjectures-bench-checker. `/tests` was uploaded by Harbor at verifier time.
- Container hashes compared to host: checker, Spec package and golden in both locations exactly match local task. `/tests` additionally contains only the verified formal-only test.sh. See `erdos41-refute-container-hashes.json`.
- Docker history confirms final `RUN lake build +FormalConjecturesBench.Target` after COPY/cleanup/permissions and USER ubuntu. Independently repeated as ubuntu: exit 0 (`erdos41-refute-ubuntu-build.log`). No additional upstream imports needed beyond ProblemImports.

## Supplemental paths in the SAME final container

`docker exec -u ubuntu erdos41-refute-accept2-20261104__env-main-1 python3 /tmp/erdos41-refute-coverage.py`, exit 0. Delivered evidence contains this standalone fixture driver and complete output. It imports the actual /tests checker and directly calls its actual functions; it does not patch/disable formal checks.

Covered:
- fixed Spec manifest/version/input/artifact checks and independent transitive type audit;
- isolated candidate compilation as ubuntu, full type comparison passes for the original placeholder type;
- actual target axiom audit rejects sorryAx, and actual sorry canary detects sorryAx;
- frozen prefix/header/assignment mutation rejection and out-of-subtree source rejection;
- semantic negative with unchanged frozen header: allowed helper `Erdos41.Filter.atTop := ⊥` compiles, changes the theorem's type, and the full type comparison actually rejects it;
- candidate same-name FCBTrustedSpec source/garbage olean, forged dependency cache, LEAN_PATH and LEAN_SYSROOT cannot override fixed trusted module/dependency lookup; original candidate still compiles and type-checks against Spec;
- missing olean, corrupt olean and corrupt manifest explicitly rejected without regeneration/fallback;
- repeat trusted audit, ubuntu compile, full type comparison, target sorryAx rejection and canary using local /opt package too.

The placeholder is retained ONLY in isolated verification fixtures to reach later stages; formal source restrictions remain active and reject it. No claim of solving the open/refutation target or reward 1. The successful-proof/allowed-axioms branch for this unsolved target is not covered, as no answer was constructed. All infrastructure paths required by the skill were exercised.

AST parses, two checker/package copies match, unchanged Target/golden bytes and TOML metadata verified. Unicode helper rerun passes no_issue. Source-search command as ubuntu found package Mathlib's Real.log with exit 0 and no path/permission errors. Frozen checks, source restrictions, target axiom audit and canary remain on the main path. Runtime invokes fixed Lean directly (trusted search paths first), does not build Spec/dependencies or use candidate Lake configuration.

Docker cleanup is recorded separately after saving the report and these artifacts.
