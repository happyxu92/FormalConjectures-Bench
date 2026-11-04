# Infrastructure repair validation

Only this task directory was modified. No mathematical statement, public Target, golden file, frozen hash/header, GoldenCheck, shared generator/skill or other task was changed. Git HEAD byte comparisons verified all protected files. AST comparisons verified BANNED_PATTERNS and ALLOWED_AXIOMS were retained verbatim.

## Changes and inputs

1. instruction.md source-search command now explicitly lists `/app`, `/opt/formal-conjectures`, and `/opt/formal-conjectures/.lake/packages`. Actual container search for `def totient` found `mathlib/Mathlib/Data/Nat/Totient.lean` without path/permission errors.
2. Target imports only ProblemImports and local Submission: no additional upstream build target needed. Dockerfile now ends in `USER ubuntu` and `RUN lake build +FormalConjecturesBench.Target`. The pinned cached dependency build and actual ubuntu target build succeeded (warning about the original sorry is expected).
3. Skill Unicode script returned `case=no_issue`, both original headers accepted, changed headers and missing assignment rejected. No Unicode repair was necessary.
4. Trusted Spec comes only from the immutable golden input copied to a clean temporary directory in our task's matching Docker image. It excludes Submission and candidate Lake settings/caches. `generate.py` elaborates the entire original target, captures info.type and ordered levelParams, restores the original environment and exports only ExpectedType as a definition value. Independent AuditSpec verifies no temporary theorem survives and traverses the type and prefix dependencies for disallowed axioms. Ordered universe parameters are empty. Generation and audits succeeded with only propext/Classical.choice/Quot.sound.

Golden Target SHA256: `bf9a89b3f65158c76b914232d6839d7dc47076b2f1ecd94cc06dfdeebfae2e92`.
Trusted package manifest SHA256: `d38a43a04762fbbad9f5399753b64aa958eda886c601c48edddb72211cb8fc37`.
Manifest records source/generation/audit/artifact/golden hashes, Lean version, Linux x86_64 platform, FC/mathlib revisions, dependency manifest hash, target and universes. Both trusted packages are byte-identical. The compiled artifact was produced with pinned Lean 4.27.0, not a host compiler. Successful independent import confirms this toolchain needs the delivered `.olean`; no absent auxiliary artifact was masked by a build fallback.

Reproducible generation commands are in trusted_spec/README.md. The first attempt using Lake from the upstream root rewrote only our disposable container's cleaned dependency checkout and rejected a source outside its root. We discarded/recreated that container and used the absolute pinned Lean compiler with explicit trusted precompiled paths; the delivered generation/audit succeeded in the pristine replacement. No host/shared dependency was modified.

## Verifier behavior

- `SPEC_DIR=TESTS_DIR/trusted_spec`: `/tests` for Harbor, `/opt/formal-conjectures-bench-checker` for check.sh.
- Manifest hash pinned in both checkers; validates task/target/universes/platform/version/golden and file hashes/dependency manifest before import.
- Absolute pinned compiler; sanitized environment and fixed Spec/dependency search paths before candidate paths. No candidate Lake config is run and Spec never recompiles at verification time.
- Temporary Target imports Spec before Submission and takes all original prefix declarations from Spec. Only the temporary copy is transformed.
- Actual candidate compilation runs as ubuntu (drops uid/gid if official checker is root). Normal helper imports/defs/lemmas/instances and dependency modules remain available. No broad import whitelist or unrelated sandbox hardening was introduced.
- Full target type is checked against the **value** of the pre-elaborated ExpectedType. The original GoldenCheck files remain unchanged but are no longer used to reparse the expected proposition in candidate context.
- Original frozen/source rules, target axiom audit and sorry canary remain in the main path.

## Actual Harbor builds and entry points

Read `harbor --help` and `harbor trial start --help` independently (saved CLI help). Built from the current local task, never an old registry task.

Initial precompile build:
`docker build -t fcb-ctrefute-spec:20261104 <absolute-task>/environment`

Final acceptance:
`harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/wikipedia-carmichaeltotient-charmichaeltotient-refute --trial-name fcb-ctrefute-final-20261104 --trials-dir /tmp/ctrefute-harbor --agent nop --env docker --no-delete --environment-kwarg keep_containers=true --extra-docker-compose /tmp/ctrefute-compose-final.yaml`

No LLM agent was started (`nop`). Docker socket or extra host dependencies were not mounted. The compose override only gives this task a checked-unused `10.249.139.0/24` subnet: the initial attempt exhausted Docker's predefined pool. No other networks or resources were removed. A preliminary successful Harbor run revealed that this installed Harbor's `--no-delete` still downs containers; inspecting Harbor's Docker backend showed `keep_containers=true` is required for supplemental verification. Subsequent kept runs succeeded.

Final Harbor image: `fcb-ctrefute-final-20261104__env-main:latest`, ID `sha256:25c7ddd08bef61309de840efd37e0a4b1d8d035c26ea8db2e4cd56276bedb502`.
Final container: `fcb-ctrefute-final-20261104__env-main-1`, ID prefix `1f76837fdfbb`.

Harbor supplied `/tests` and `/logs/verifier`. Both container checkers, complete golden trees and both Spec packages were compared file-by-file with current local hashes (all match). Spec/checker sources were not added to `/app`.

Executed in that actual Harbor child:
- `docker exec <container> bash /tests/test.sh`: exit 1, reward 0, **expected original sorry rejection**, not an infrastructure failure.
- `docker exec --user ubuntu <container> bash /app/check.sh`: exit 1, same expected rejection.

These early rejections do not themselves cover Spec loading. The independent `/tmp/ctrefute-coverage.py` imports and calls the actual unmodified checker's functions inside that same container, once using `/tests` and once as ubuntu using `/opt`.

Each of the 17 supplemental checks covers:
- fixed precompiled Spec load, independent value/universe/transitive-axiom audit;
- ubuntu compile of isolated original placeholder fixture;
- matching complete-type check; explicit axiom-audit rejection of its sorryAx; sorry canary;
- invalid candidate same-name Spec source/olean/cache and hostile LEAN_PATH/dependency env cannot substitute Spec (verified resolved import path and audit);
- frozen prefix modification and out-of-tree Lean source rejection;
- legal-syntax priority LT Nat instance changing `<` to True, with byte-identical frozen prefix/header: source restrictions pass, altered candidate compiles and is axiom-clean, but actual full-type comparison rejects it with Type mismatch; the full actual checker also rejects it;
- missing precompiled Spec and corrupted artifact fail explicitly without regenerating them.

The semantic negative fixture is deliberately NOT a proof of the task: it makes n=0 satisfy the positivity premise under a replacement order. Neither public Target nor golden was edited for these tests. No full proof of the open refutation was required or supplied. General external initializer/plugin security is outside this repair's scope; no claim of broad compiler sandboxing is made.

Logs/results are in this evidence directory and `/tmp/ctrefute-*`. The final Docker resource list and cleanup verification are recorded separately; existing resource snapshots were taken before creation and only explicit task-created IDs/tags/projects were cleaned.
