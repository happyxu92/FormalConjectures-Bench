# erdosproblems-126-erdos-126-prove infrastructure repair

## 1–3
- instruction search explicitly includes `/app`, `/opt/formal-conjectures`, and `/opt/formal-conjectures/.lake/packages`. Tested as ubuntu with `rg --glob '*.lean' 'def primeFactors'` against all three paths: exit 0, including Mathlib/Data/Nat/PrimeFin.lean.
- Target has only the two standard imports; no additional upstream precompile needed. Dockerfile now ends in ubuntu `RUN lake build +FormalConjecturesBench.Target`. Both local Harbor builds succeeded; same build separately repeated in final container as ubuntu, exit 0 (7992 jobs).
- Required Unicode script: `case=no_issue`, both before and after repair. All original Targets still SHA256 `dc811b12220e1a3f0d473228a071f19357f69aa94e7f846c62236a0a145979b8`.

## 4: generation and audit
- Clean repair-time directory `/tmp/erdos126-generation` in container `fcb-erdos126-spec-20261104`, ID `4fd8037ad9ce41262f12e16a2842656e93ee518a94ebad8d7d48ba7892e3bee7`.
- Reused pre-existing pinned dependency image `fcb-local/erdosproblems-1-least-n-5:cache-smoke`, ID `0824de0f16475f1f619701869e59de4e4ce3229bfce229a5fd16f88072c37e8f`. Only this task's golden and generator were copied into the generation directory. Candidate source, configuration and caches were not loaded.
- Command: `bash /tmp/erdos126-generation/trusted_spec/reproduce.sh`. Initial generation failed because the target doc-comment preceded `run_cmd`; generator was corrected to omit only that documentation comment, then succeeded (exit 0).
- Generator elaborates the complete golden declaration, extracts `ConstantInfo.type` and ordered level parameters, restores the pre-declaration environment, and exports only the type expression as a definition. Placeholder theorem is not exported. Generator warning is expected; the independently imported delivered Spec has no `sorryAx` dependency.
- Full type has one universal function binder and the maximality implication; universe list is empty. `collectAxioms` recursively audits ExpectedType and IsMaximalAddFactorsCard; only propext, Classical.choice, Quot.sound occur.
- Both `trusted_spec` packages are byte-identical, including .olean/.ilean, generation source/commands, audit code/log, and manifest. Manifest SHA256 `dbb12505cae410aa6d3d896baaeb7465b64384008f3b08a433487835e8a2579c`; all input/artifact hashes, exact Lean version, platform and dependency revisions are in that manifest.
- Checker validates fixed manifest and all files, golden input, toolchain version, platform, universes, dependency revision manifest. Direct pinned Lean uses Spec then trusted dependencies then fresh candidate source outputs; does not use candidate Lake configuration or search environment. Only temporary Target is transformed to share prefix constants from Spec, preserving namespace/open context.
- Existing frozen, banned syntax, editable tree, extra-source, axiom and canary checks remain. GoldenCheck.lean is unchanged and no longer used for type comparison. The type comparison uses `example : _root_.FCBTrustedSpec.ExpectedType := @_root_.Erdos126.erdos_126`.

## Local Harbor acceptance
Help was read for `harbor run`; retention additionally requires Docker environment kwarg `keep_containers=true` (plain `--no-delete` removes containers but keeps images in this installed version).

Commands:
```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-126-erdos-126-prove --agent nop --env docker --force-build --no-delete --job-name fcb-erdos126-20261104 --jobs-dir /tmp/erdos126-harbor-jobs -n 1
harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-126-erdos-126-prove --agent nop --env docker --force-build --no-delete --ek keep_containers=true --job-name fcb-erdos126-final-20261104 --jobs-dir /tmp/erdos126-harbor-jobs -n 1
```
- First build tag `erdosproblems-126-erdos-126-prov__za8tz4p__env-main:latest`, image `8e232d5d9b0da3b66198cf4120f25b5e2adfb31687327f738db865cf2865be2b`; container `3cfb5a999c60674d2b14daac2684bff72ef07365080b85288541ef1d0b74d389` automatically removed by Harbor.
- Final tag `erdosproblems-126-erdos-126-prov__qvgpman__env-main:latest`, image `a97d90bc74a460ed87e9f9e104344df1801480160814debe8393553cbe3a8cbf`; container `25241b3328e2528aebe51df5f242a6605fc416ed25f8185b5636e28e37a776f7` retained/stopped, then restarted for tests.
- Harbor uploaded `/tests` and created `/logs/verifier`. Final container file hashes match local checker, both trusted packages and both golden trees (see hash log).
- `docker exec <final container> bash /tests/test.sh`: exit 1, reward 0, expected original `sorry` source rejection. `/tests/test.sh` uses FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests.
- `docker exec --user ubuntu <final container> bash /app/check.sh`: exit 1, same expected rejection. Local script uses `/opt/formal-conjectures-bench-checker`.
- Independent supplemental script invokes the actual checker functions in the same Harbor container, both as root (compiler drops to ubuntu) and ubuntu: exit 0. Each Spec path independently passed loading, trusted type audit, ubuntu candidate build, full type comparison, target sorryAx rejection, and sorry canary. No formal checks were weakened. Original Target/golden were never replaced.
- Semantic negative: allowed helper `def Erdos126.Tendsto ... := True`; frozen prefix/header unchanged, source restrictions passed, candidate compiled and had only allowed axioms. Complete type comparison rejected the resulting different proposition.
- Other negatives: frozen prefix/header mutation, missing :=, outside-subtree source, missing/corrupt .olean all rejected. A real same-name compiled candidate cache and hostile LEAN_PATH/dependency environment could not replace the fixed Spec; `--deps` resolved `/tests/trusted_spec/FCBTrustedSpec.olean`. Missing/corrupt artifacts were not regenerated.
- This is infrastructure acceptance, not a proof of the target. No complete positive target proof was constructed, installed or claimed. Full success (reward 1) for a genuine target proof was not tested.

## 5: statement fidelity (mark only)
- Read pinned upstream `https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/126.lean` in full. This task retains the positive proposition under its `answer(sorry) ↔ ...`, not the negative paired task or the weaker IsBigO variant.
- Read Erdős and Turán, *On a Problem in the Elementary Theory of Numbers*, Amer. Math. Monthly 41 (1934), pp. 608–611: `https://static.renyi.hu/~p_erdos/1934-03.pdf`. It discusses pairwise sums with a fixed finite prime support, logarithmic lower bounds and stronger growth questions. Problem page `https://www.erdosproblems.com/126` and non-www variant returned HTTP 403; web search supplied corroborating indexed formulation. Searches: `Erdos problem 126 f(n) prime factors a+b logarithm`; `Erdos Turan 1934 On a Problem in the Elementary Theory of Numbers distinct prime factors sums 126`.
- Checked full IsMaximalAddFactorsCard definition: IsGreatest over universal lower bounds for n-element Finset naturals; product over offDiag and primeFactors.card; real quotient and atTop convergence. Ordered pairs double multiplicities without changing distinct prime support. For distinct naturals each sum is positive. Allowing zero can delete at most one element, so is harmless asymptotically compared with positive naturals. Empty/singleton products and Real.log 0/1 do not affect atTop. No evident false-statement defect. Marked consistent; no mathematical changes.

## 6: public proof collection
Exact full task ID match in `/root/FormalConjectures-Bench/skills/lean-task-repair/references/public-lean4-proofs.csv`:
- task: erdosproblems-126-erdos-126-prove
- proof_urls: https://github.com/tadamcz/erdos126/blob/2516785fe6bbc43e979cf6029c976d9f998a7fba/Erdos126/Resolutions/Erdos126_132usd_25h.lean#L3053

Per skill, this trusted exact match establishes public_lean4_proof=true without further proof search. No public Lean answer source was copied or compiled. The result is specific to this positive task ID.

Docker resource cleanup is recorded in cleanup.log and the final report; pre-existing shared base images, build cache and all other task/user resources are excluded.
