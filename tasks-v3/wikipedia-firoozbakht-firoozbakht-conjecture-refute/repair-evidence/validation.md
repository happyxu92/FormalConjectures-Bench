# Infrastructure validation

## Repair-time compilation

```
docker build -t fcb-firooz-refute-spec:nt40-20261104 /root/FormalConjectures-Bench/tasks-v3/wikipedia-firoozbakht-firoozbakht-conjecture-refute/environment
docker create --name fcb-firooz-refute-spec-nt40 --user root fcb-firooz-refute-spec:nt40-20261104 sleep infinity
# Copy tests/golden_env and tests/trusted_spec to a clean /tmp/firooz-refute-clean directory.
docker exec fcb-firooz-refute-spec-nt40 bash /tmp/firooz-refute-clean/trusted_spec/reproduce.sh
```

Build and generation/audit exit 0. Image `sha256:91d45e5a355023ce73339416ac86a78751cfa2b744dbcb6309cad03018f4f4c8`.
No candidate import, Lake configuration or cache participates in Spec compilation: only original golden input, locked Lean, and fixed upstream libraries are searched. The temporary theorem environment is discarded before exporting ExpectedType. `AuditSpec.lean` verifies target absence, definition value shape, zero universe parameters, the nested Nat binder and transitive axioms of ExpectedType and the retained sequence definition. Output shows the full original negated universal inequality and only standard axioms. Generation warning about the temporary placeholder is expected; no placeholder theorem or sorryAx reaches the delivered module.

See both identical `trusted_spec/manifest.json` packages for input/source/artifact hashes, exact Lean version, platform and pinned dependency revisions. Manifest hash pinned in both checkers: `5c64c388fa0066f2bceb0e53149c727693cfc9b97f4e44e91dcfad5e8cd5f77d`.

## Actual local Harbor acceptance

Independently read `harbor --help`, `harbor run --help`, `harbor trials start --help`, and inspected the installed Docker backend to establish `keep_containers` behavior.

```
harbor run -p /root/FormalConjectures-Bench/tasks-v3/wikipedia-firoozbakht-firoozbakht-conjecture-refute -a nop -e docker --force-build --no-delete --ek keep_containers=true --job-name fcb-firooz-refute-accept-nt40-20261104 --jobs-dir /tmp/fcb-firooz-refute-harbor -n 1
```

Harbor exit 0, no trial exceptions, reward 0 (expected original unfinished proof). This builds the current local environment; there is no registry task replacement. Final Harbor image `wikipedia-firoozbakht-firoozbakh__opjhcps__env-main`, ID `sha256:48003e433b526d71428a53ffa7121d194179af19efe85ddca85fc3abb3f3db47`. Retained child `6c4a3fb8b2363faa0f11912d7ebd90bd33df8ac7cfa71149fa8fa94fb93de493` was restarted for supplemental testing. No extra host mounts or Docker socket were used (`Mounts: []`).

An initial Harbor run with `--no-delete` but without `keep_containers=true` also built and verified successfully, then automatically removed its child (backend semantics). Its image is `wikipedia-firoozbakht-firoozbakh__e4rgxik__env-main`, ID `sha256:41ea8625a189bae0c1c6da5ce39edbc88351fccef285a5ce014b8e9ce6e9ba3f`. Its container ID was not retained before automatic removal; the exact trial/project name is recorded, and subsequent Docker inspection confirmed absence. No other agents' containers/images were claimed by a resource diff.

```
docker exec wikipedia-firoozbakht-firoozbakh__opjhcps__env-main-1 bash /tests/test.sh
docker exec --user ubuntu wikipedia-firoozbakht-firoozbakh__opjhcps__env-main-1 bash /app/check.sh
```

Both exit 1 solely on the original banned `sorry`; formal reward file is 0. Harbor uploaded `/tests` at verification time. `/tests/test.sh` sets FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests; check.sh sets the latter to /opt/formal-conjectures-bench-checker. A complete host/container hash comparison confirmed both checkers, both Spec packages, all golden files, entry scripts and the public Target match this local task (`container-hashes.json`). No inference about downstream correctness was drawn from these early exits.

## Supplemental downstream coverage in the same Harbor child

Run the saved `supplement.py` against the actual checker functions, first with the formal `/tests` package and then, as ubuntu, with CHECKER_PATH and FCB_TESTS_DIR selecting the installed `/opt` package. Both final runs exit 0. An initial assertion matched lower-case `type mismatch` against Lean's capitalized diagnostic; that fixture assertion alone was corrected and all tests rerun. Formal checker was not loosened.

- Original frozen header passes; prefix modification and out-of-subtree source rejected.
- Original sorry is rejected by source restrictions.
- In an isolated placeholder fixture, independently reach trusted Spec load/audit, actual ubuntu compilation, successful full original type comparison, target sorryAx rejection, and successful sorry canary. Compiler identity independently prints `ubuntu`.
- Semantic negative: unchanged original prefix and theorem header; helper defines a high-priority `LT Real` instance returning False. The candidate compiles and its proof has no extra axioms, yet full comparison against compiled ExpectedType rejects it with a Lean type mismatch. Thus the frozen text and axiom audit alone are insufficient, and the new comparison actually runs.
- A forged same-name FCBTrustedSpec.olean in candidate project/cache, plus hostile LEAN_PATH and LEAN_SYSROOT environment values, cannot replace the trusted module. Actual `lean --deps` resolves the validated fixed Spec path; independently importing it still passes the trusted audit.
- Missing and corrupt precompiled artifacts fail explicitly before compilation; neither is regenerated or repaired at runtime.

The placeholder fixture deliberately calls downstream functions directly, without weakening formal source checks. This is coverage of infrastructure, not a proof or acceptance of the open mathematics task. There is no completed real proof/reward-1 test.

## Other checks

- Instruction search now explicitly includes the hidden package directory; the real ubuntu rg command found Mathlib `add_comm` definitions, exit 0, with no path/permission errors.
- Public Target imports only ProblemImports and Submission; no extra upstream precompile needed. Dockerfile ends with the required actual ubuntu `lake build +FormalConjecturesBench.Target`, successful in the build. No dependency permissions were widened.
- Skill Unicode script returned `case=no_issue`, both headers and frozen inputs pass; no header changes.
- AST parsing, exact two-checker/package equality, manifest hashes, TOML parsing and final Dockerfile-tail checks pass. Banned-pattern list, frozen prefix hash and EXPECTED_HEADER are byte-for-value unchanged from git HEAD. Public Target, both golden trees and both GoldenCheck files are unchanged (`immutable-inputs.json`).
- Research-only metadata marks the mathematical statement consistent and proof search searched/no known proof. See research.md; no statement, golden, or public answer changes.

Resource cleanup is recorded in `docker-cleanup.log`, `resources.json` and the root repair report. Only exact task-owned resource identities were used; shared bases/caches and other agents' resources were untouched.
