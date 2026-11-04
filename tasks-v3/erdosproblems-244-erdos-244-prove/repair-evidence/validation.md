# Infrastructure validation

## Commands and environments

- Before creation: `docker ps -a --no-trunc` and `docker images --no-trunc`, saved to `/tmp/fcb244-existing-containers.txt` and `/tmp/fcb244-existing-images.txt`.
- Read `harbor --help`, `harbor run --help`, `harbor trial start --help`; inspected Docker environment's `keep_containers` option after discovering `--no-delete` alone still removes the container. No task or verifier privileges were widened.
- Precompile image: `docker build -t fcb-erdos244-prove:spec-20261104 /root/FormalConjectures-Bench/tasks-v3/erdosproblems-244-erdos-244-prove/environment`. Build passed, including final `USER ubuntu` `lake build +FormalConjecturesBench.Target`. No extra imports beyond the standard pair were present.
- Generation: create task-owned `fcb244-spec-20261104`; copy the task's tests/golden_env and repair-time trusted_spec scripts into `/tmp/fcb244-generation/`; run `bash /tmp/fcb244-generation/trusted_spec/reproduce.sh`. Exit 0. No candidate code or Lake project was loaded. Absolute locked Lean compiler and pinned dependency paths were used. Generation logs correctly warn about the *temporary* sorry theorem. Audit proves it was not exported and does not appear in ExpectedType's transitive dependencies. ExpectedType has no universe parameters and is the complete forall proposition.
- Both `.olean`/`.ilean` and reproducible generator/auditor source are synchronized under `tests/trusted_spec` and `environment/data/checker/trusted_spec`. Manifest records original golden hashes, artifact hashes, exact Lean version/platform/revisions/image ID. Its fixed checker anchor is `b6da3ea235cbefcdc3eabb839581055e44df06f285a557ddc4cf3e5ff33eceb2`.
- Final delivered image is built by Harbor from this **local task**, not a registry image:
  `harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-244-erdos-244-prove --agent nop --env docker --no-delete --ek keep_containers=true --job-name fcb244-harbor-retain-20261104 --jobs-dir /tmp/fcb244-harbor-jobs --n-concurrent 1`.
  Exit 0, no Harbor exceptions; reward 0. Unique image `erdosproblems-244-erdos-244-prov__xak79y8__env-main`, child `erdosproblems-244-erdos-244-prov__xak79y8__env-main-1`. Exact IDs retained in the ID/resource files. An initial Harbor run without `keep_containers` also built and verified this task, then automatically removed its child; its image and result records are retained for cleanup accounting.
- Harbor uploads `/tests/` for verifier execution and provides `/logs/verifier`. All 33 files in the container's `/tests` and `/opt/formal-conjectures-bench-checker` were hashed and matched the host checker/Spec/golden packages (`delivery-hashes.json`). No tests/Spec were put into the editable submission tree.
- Restarted the retained Harbor child (Harbor had stopped it). Executed `docker exec --user root <child> bash /tests/test.sh`: exit 1, reward 0, expected original proof-region `sorry` rejection. The script explicitly sets `FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests`. Executed `docker exec --user ubuntu <child> bash /app/check.sh`: exit 1 for the same expected reason. These are proof-placeholder failures, not infrastructure errors, and do not themselves cover subsequent Lean checks.

## Supplementary reachability tests in the same Harbor child

The independent `/tmp/fcb244-supplement.py` loads the actual `/tests/test_target.py` functions without modifying official checker, public Target or golden. Full output: `supplement-final.log`, exit 0. Reproducible script: `supplement.py`.

1. `load_trusted_spec`: validated `/tests/trusted_spec`; independent ExpectedType audit passed, no exported temporary target, only propext/Quot.sound/Classical.choice.
2. `make_fresh_golden_project` and `check_build`: original isolated sorry fixture compiled as ubuntu, using Spec before Submission, exact namespace Erdos244, fixed absolute Lean compiler/path/options. Candidate Lake config/caches/environment are not used for trusted dependency resolution.
3. `check_golden_theorem_import`: complete candidate type matches the already elaborated ExpectedType value. No GoldenCheck file is copied/executed and no expected proposition is reparsed.
4. `check_axioms`: original fixture rejected with actual `sorryAx`. `check_sorry_canary`: passed.
5. Same-name candidate `FCBTrustedSpec.lean`, invalid `.olean`, and `.lake/build/lib/lean/FCBTrustedSpec.olean` cannot override the verified Spec; audit still passed with the fixed search path.
6. Frozen-prefix mutation and added outside-subtree Lean source were rejected by the original restrictions.
7. Semantic negative: ordinary high-priority `LT ℝ` instance in Submission replaces `<` with True. The frozen public prefix and theorem header are byte-identical, proof is `intro C hC; trivial`, with **no placeholder**, and source-ban checks pass. The candidate compiles, its axiom audit passes, but the actual full-type comparison rejects it with Lean `Type mismatch`. This covers a real meaning change, not merely the earlier sorry rejection.
8. Missing and corrupted `.olean` each explicitly fail the manifest/artifact gate without invoking a generator or fallback compilation.

Additionally ran the actual checker load/audit/build/type-compare/canary functions as **ubuntu** with `FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker`: exit 0; `ubuntu-local-supplement.log` shows that the local route directly imports the packaged precompiled Spec.

## Final static checks

Python AST for both checkers, byte synchronization of both checker files and all Spec files, task.toml parse, original Target SHA256 `1a2cf2aa395b59abf263bc31219d97aa291b80536b10f8834f7b75c582babdfc`, unchanged public/golden equality, preserved frozen hash/header and unchanged GoldenCheck were checked. The Unicode skill script passed before and after changes with `case=no_issue`. Dockerfile still ends with ordinary-user Target dependency validation. Search command executed without path/permission errors and found `class Group` in hidden package sources (`package-search.log`).

No complete proof of the original mathematical target was supplied, built or claimed. Acceptance here concerns infrastructure and the explicitly covered rejection paths, not reward 1 or resolution of Erdős 244. General compiler/plugin security and arbitrary external module behavior are outside this repair's scope.
