# Infrastructure verification

Root: /root/FormalConjectures-Bench/tasks-v3/erdosproblems-126-erdos-126-refute

## Repair and Spec generation

- Instruction search now explicitly includes /app, /opt/formal-conjectures and hidden .lake/packages. Actual final-container rg found `def Ordinal.toNimber` in Mathlib/SetTheory/Nimber/Basic.lean, exit 0, no path/permission errors (final-search.log).
- Target has only ProblemImports and local Submission imports: no extra upstream build targets needed. Dockerfile now ends in `RUN lake build +FormalConjecturesBench.Target`, after WORKDIR /app, HOME ubuntu and USER ubuntu. It succeeded (original sorry produces a warning, not a dependency error).
- Unicode skill script was run before and after changes; both returned 0, case=no_issue. Expected header, frozen prefix and := checks passed; constants not changed.
- Original Target, both golden copies, frozen prefix/hash and both GoldenCheck.lean files were not modified.

Spec precompile command:
`docker build -t fcb-erdos126-refute:spec-20261104 /root/FormalConjectures-Bench/tasks-v3/erdosproblems-126-erdos-126-refute/environment`

Created container `fcb-erdos126-refute-spec-20261104`, ID 3b8ce3afd35e..., from that image. Copied only original trusted golden inputs plus newly written generator/auditor into /tmp/erdos126-refute-generation. Executed `bash /tmp/erdos126-refute-generation/trusted_spec/reproduce.sh`. Direct locked Lean binary, working directory outside /app, and explicit trusted LEAN_PATH: no candidate Lake config, source or cache participated. Generator removes Submission import, elaborates the full original declaration, captures type and level parameters, restores the pre-target environment and adds a checked definition of the type expression. Audit rejects exported temporary target and its children. The transient elaboration warning about sorry is expected; independent audit proves no sorryAx dependency survives in ExpectedType or the prefix definition.

Generation/audit exit 0. Manifest: tests/trusted_spec/manifest.json, SHA256 e73fb3ee0291c7043d94db82e014a9835e2ff4d1b119e5c165989532ca6d9645. Original golden Target SHA256 4414a59b82e82a4e2cb564fb37b676b5b86e4f6ca4c0ead617e299a61b980c4e. Olean SHA256 51afccaacae794a5b0158621cb7c91f96af136c0fd73c97224155e80fd6973b6. Full source, artifact and input hashes are in manifest; its identity is pinned in both checkers. Lean v4.27.0 commit db93fe1608548721853390a10cd40580fe7d22ae, x86_64-linux, FC 233a10e857ef78e79fd9fe661d37db724089170a, Mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900. Universe parameters [], outer binder count 0 (the complete proposition is a negation containing the full quantification). Audit prints the actual full ExpectedType value and prefix definition; transitive axioms are only propext, Classical.choice, Quot.sound. Both trusted packages are byte-identical.

## Checker

Actual checker functions retain frozen files/header, editable-source confinement, banned syntax, target axiom checks and sorry canary. Only temporary Target is transformed: import fixed Spec first, import Submission, restore open Filter/namespace Erdos126, keep target declaration and proof suffix. Prefix definition comes from Spec, not candidate re-elaboration. Fixed LEAN_PATH places Spec and locked precompiled dependencies before fresh candidate modules; ignores candidate Lake/cache and ambient Lean variables. Direct compiler recursively builds normal candidate imports and drops to ubuntu even from the official root verifier. Does not introduce a general external-module whitelist. No runtime generator or fallback compilation of Spec.

Type check invokes the actual `check_golden_theorem_import` function: a temporary Lean check imports compiled ExpectedType and candidate theorem and checks `example : _root_.FCBTrustedSpec.ExpectedType := @_root_.Erdos126.formal_conjectures_bench_refutation`. GoldenCheck.lean is left untouched and no longer copied/executed for expected-type checking.

## Harbor and entrypoints

CLI help read independently: harbor --help, task --help, task start-env --help and run --help. `--no-delete` alone does not retain the stopped container; explicit `--ek keep_containers=true` was used after diagnosis.

Successful retained local build command (before metadata-only review):
`harbor run -p <root> -a nop --job-name erdos126-refute-retain-20261104 --jobs-dir /tmp/erdos126-refute-harbor --env docker --no-delete --ek keep_containers=true --force-build --n-concurrent 1`

A final metadata-inclusive repeat built successfully but failed network creation because the host's predefined Docker address pools were fully subnetted. No unrelated network was removed. Retried with the SAME local build, adding `--extra-docker-compose /tmp/erdos126-refute-own-network.yaml`, which merely reuses this task's own already-created network `erdosproblems-126-erdos-126-refu__dgp2la9__env_default` (external:true). The overlay grants no extra privileges/mounts and is saved with evidence. Retry job: erdos126-refute-final-retry-20261104, trial JNmda6d, exception_info=null. Final container ID 0efb0b63ace780d156df92cd39c6518b3a1f2277042dc4bdd217e41a7d3161ec, final image sha256:f271f02a3f76a07551c2fc00e0a43a475729773fefbb65b13007557901360178. This is Harbor's current local environment/Dockerfile build, NOT an old registry task image.

Harbor uploaded /tests and provided /logs/verifier. After restarting its retained stopped container, ran:
- `docker exec <final> bash /tests/test.sh` => 1, reward.txt=0, expected original sorry syntax rejection.
- `docker exec --user ubuntu <final> bash /app/check.sh` => 1, same expected rejection.
- `docker exec <final> python3 /tmp/erdos126-refute-supplement.py` => 0.
- `docker exec --user ubuntu -e FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker -e FCB_SUPPLEMENT_CHECKER=/opt/formal-conjectures-bench-checker/test_target.py <final> python3 /tmp/erdos126-refute-supplement.py` => 0.

Official wrapper explicitly supplies FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests. Local wrapper supplies /opt/formal-conjectures-bench-checker. Final hashes prove container's two checkers, Spec packages and golden copies equal the local delivery; no source/checker package was placed under submission /app/FormalConjecturesBench. No Docker socket or privileged container used.

## Actual supplemental coverage, in BOTH official and ubuntu local contexts

The separate isolated program calls the checker functions, without modifying them or bypassing formal rules:
- Trusted manifest/version/dependency/input/artifact validation and independent full value/prefix transitive axiom audit: pass.
- Fresh candidate compilation as ubuntu: pass; unchanged placeholder type matches full ExpectedType.
- Target axiom audit: rejects sorryAx; sorry canary: detects sorryAx.
- Same-name candidate Spec source, compiled olean and .lake cache plus ambient LEAN_PATH/LEAN_SYSROOT: cannot replace fixed Spec; --deps names trusted package, full type/audit still pass.
- Frozen target text unchanged, helper defines Erdos126.Tendsto := False: temporary target compiles but ACTUAL full type comparison rejects changed Erdos126.Tendsto versus Filter.Tendsto. This isolated negative deliberately retains a placeholder solely to exercise type comparison without solving math. Its sorry is separately rejected by both source and axiom checks; formal checker was not relaxed.
- Frozen-prefix mutation: rejected. Source outside editable subtree: rejected.
- Missing artifact, corrupted olean and corrupted manifest: rejected before Lean use, no fallback generation/recompilation.

No claim is made that a real proof of this negative mathematical statement passed; no complete proof was constructed. The formal entries intentionally exit at original sorry; supplemental functions independently cover the later paths rather than inferring their behavior. Only the all-checks-success branch for a genuine complete target proof remains unexercised. All required infrastructure paths were actually reached.

Static AST/TOML/package equality and final Dockerfile-user ordering validations pass. Exact IDs and cleanup evidence are in created-resources and cleanup logs. Resource cleanup is performed only after report, source artifacts and logs are saved.
