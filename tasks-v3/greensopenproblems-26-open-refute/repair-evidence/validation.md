# Infrastructure repair validation

Only `greensopenproblems-26-open-refute` was edited. No public proof was added.
Public Target, golden inputs, GoldenCheck.lean, frozen prefix hash and target
header mathematical text remain unchanged. See Unicode logs for the encoding fix.

## Changes

1. Added explicit `.lake/packages` to instruction's `rg` command. Ran the full
   three-path command as ubuntu in the final container; `^theorem card_union_le`
   matched Mathlib package files and exited 0 (`search-final.log`).
2. Target imports only ProblemImports and local Submission; no extra upstream
   precompile module was required. Added final `USER ubuntu` build validation.
   Current Harbor build passed; a direct final ubuntu `lake build
   +FormalConjecturesBench.Target` also exited 0 (`ubuntu-build-final.log`).
3. Skill's exact Unicode script repaired the surrogate pair for 𝔽 in both
   EXPECTED_HEADER constants. It checked both golden inputs, frozen hash, original
   header, changed header and missing `:=`. Final run reports `no_issue`.
4. Independently elaborated and compiled a trusted Spec from this task's golden
   Target without Submission. Temporary target declaration is erased before
   adding ExpectedType; independent audit checks it was not exported. The
   ExpectedType value is the **negated** all-prime proposition, with all nested
   binders; universe list is empty. Transitive audits of ExpectedType and prefix
   definitions find only propext, Classical.choice and Quot.sound. Original
   prefix's unrelated sorry lemmas remain, but none is a dependency of
   ExpectedType. No candidate input participated in generation.

Generation environment: reused pre-existing local image
`greensopenproblems-26-open-prove__jsmyxgx__env-main:latest`,
sha256:c528d69a700cd44b3f9f2f1b590d3308b3e6507fc9ab3c8ce25c6f621bb3dca7,
only for its pinned toolchain/dependencies. No paired task was edited. Container
`fcb-green26-refute-spec-20261104` / caf1e8e4a5e377a9bb386850cfa263a08042bba2c0593b70b3e382f9d393ddd7.
Copied **this task's** golden_env and generation files into
`/tmp/fcb-green26-refute-spec/` and ran
`bash /tmp/fcb-green26-refute-spec/trusted_spec/reproduce.sh` (exit 0).
The reproducible generator, exact Lean flags, source, artifacts, audit and
manifest are in both synchronized trusted_spec packages. Lean 4.27.0,
x86_64-unknown-linux-gnu, compiler commit db93fe1608548721853390a10cd40580fe7d22ae.
FormalConjectures 233a10e857ef78e79fd9fe661d37db724089170a;
Mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900.
Golden Target SHA256:
6f4ab977c9ed15acbb48663aa67a81c187976d708aa322c95402bdf9ad72e558.
Manifest SHA256:
008c3c6cbfd57855c8980c0bec6d03c14dc4e4f423b5dfa454a555774aa25d00.
All source/artifact/input hashes are in that pinned manifest.

## Harbor acceptance (current local task, not registry)

Read `harbor --help`, `harbor run --help`, and `harbor task start-env --help`.
Initial `harbor task start-env --path <absolute-task> --env docker
--non-interactive` successfully built the task, but Docker's default address
pools were exhausted. Harbor automatically removed that failed attempt's image
`greensopenproblems-26-open-refute__27a3aecb4e10__env-main:latest`.
No existing network was deleted. An external temporary Compose overlay supplied
only an explicit unused subnet, 10.249.226.0/24 (no extra mounts/permissions).

Successful CLI command:

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/greensopenproblems-26-open-refute \
  --agent nop --env docker --job-name fcb-green26-refute-keep-20261104 \
  --jobs-dir /tmp/green26-refute-harbor-jobs --no-delete --ek keep_containers=true \
  --extra-docker-compose /tmp/green26-refute-network.yaml
```

A preceding successful `fcb-green26-refute-accept-20261104` run omitted
keep_containers (Harbor automatically removed its container). Both jobs had
zero exceptions and reward 0, the expected unfinished-proof outcome.
Final image: `greensopenproblems-26-open-refut__vjwzlp5__env-main:latest`,
sha256:3adf35b8e93a957e82c9ab0169f294f9f237cbe6bdf4cdf40a12b947c7de8df3.
Previous successful image: `greensopenproblems-26-open-refut__e4wfw5e__env-main:latest`,
sha256:2f7d0673ae054e9fd196b06d14d698440fe4eb60d368a8e328b9be19ebe42a3c.
Final container: 11909060d4200e5d2e876864c3c672995461857878677fc7de20421f068714e3,
`greensopenproblems-26-open-refut__vjwzlp5__env-main-1`.
Harbor stops the retained container; it was restarted for supplementary tests.

Harbor uploaded `/tests` in the verifier phase and supplied `/logs/verifier`.
All local checker, Spec, golden and entry-script hashes matched their `/tests`
and `/opt/formal-conjectures-bench-checker` counterparts (`hashes.log`).
Official `docker exec <container> bash /tests/test.sh`: exit 1, reward.txt=0,
original sorry banned. Local `docker exec -u ubuntu <container> bash -lc
'cd /app && ./check.sh'`: exit 1, same expected rejection. No Python exception
or dependency failure occurred. Entry scripts record exact FCB_TASK_DIR and
FCB_TESTS_DIR settings (`entry-scripts.log`).

## Downstream path coverage

The independent `supplement.py` imports and calls the production checker's
actual functions in the **same Harbor container**. It does not modify checker,
/app, golden or trusted artifacts. Placeholder proofs are used only in temporary
fixtures to reach paths blocked by the original sorry syntax check. Runs:

```
docker exec <container> python3 /tmp/green26-refute-supplement.py
docker exec -u ubuntu -e FCB_TASK_DIR=/app \
  -e FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker \
  <container> python3 /tmp/green26-refute-supplement.py
```

Both exited 0 with `ALL SUPPLEMENTAL PATHS PASSED`:
- fixed precompiled Spec hash/version/input loading and transitive type audit;
- ubuntu candidate compilation using trusted dependency paths and golden options;
- complete unchanged theorem type comparison;
- target axiom audit detected/rejected sorryAx;
- independent sorry canary detected sorryAx;
- frozen prefix and changed header rejected;
- added outside-subtree Lean source rejected;
- candidate same-name Spec source, invalid olean/cache and LEAN_PATH override
  did not replace the trusted module; independent audit/type comparison passed;
- missing and corrupt Spec artifacts explicitly rejected without regeneration;
- a helper defines `Green26.Fin` as Empty: the **unchanged frozen target/header**
  still passes textual matching and the temporary target compiles, but its full
  type differs (A is indexed by Green26.Fin), and production full-type comparison
  rejects it with an actual Lean Type mismatch.

The formal theorem was not proved, and reward 1 / successful proof axiom audit
was not claimed. Ordinary helper definitions, instances and imports remain
allowed; this is not a general code-execution sandbox.

## Static checks and resource handling

Python ASTs parse; checker copies and all package files compare byte-identical.
TOML parses; final Dockerfile still ends in ubuntu Target build validation.
Git diff confirms only this task was modified, and no GoldenCheck/golden/Target
file changed. Metadata was marked only after source verification and proof
search. Resources present before this repair are in docker-before.txt and
images-before.txt. Only explicit IDs/tags created by this task will be cleaned;
see cleanup.log for final commands/results. Shared base images/build cache are
not removed.
