# Infrastructure validation

## Generation

- Trusted input: `tests/golden_env/FormalConjecturesBench/Target.lean`, SHA256 `11464783ef6a12908c00b310e0f113cee4ce85fc681d99163eef9d8425720025`.
- Full input/file/compiled-artifact hashes, ordered universe list (empty), Lean version, x86_64 platform and dependency revisions are recorded in `tests/trusted_spec/manifest.json`. Manifest SHA256: `a240d84a70b9908dbd6da241fc64a8b76daf2bc8a2e6d6f8050f48c55b38947d`, pinned in both checkers.
- Reused existing matching dependency image `sha256:0824de0f16475f1f619701869e59de4e4ce3229bfce229a5fd16f88072c37e8f` (not owned, must not delete). Own network-disabled generator container: `fcb-oddperfect-prove-spec-nt40-143048`, ID `a570c93e2eb31d28e94a946730e6628be32542a41dbe0a74ad300df345e25282`.
- Copied only trusted golden input and generator/audit source into `/tmp/oddperfect-bundle`; ran `docker exec -u root fcb-oddperfect-prove-spec-nt40-143048 bash /tmp/oddperfect-bundle/trusted_spec/reproduce.sh`: exit 0. No candidate imports/configuration/cache entered generation. Lean 4.27.0 and dependency manifest SHA256 `5b99b5f4f807cbba67bbcd22e5e486c17d6a8d970ea218de08d05830ab350c26` matched.
- Lean parser/elaborator creates a temporary full declaration, extracts `ConstantInfo.type` and `levelParams`, restores the original environment, then exports only the new ExpectedType definition. Full prefix retained except candidate Submission import and trailing documentation. Independent `AuditSpec.lean` checks no temporary target was exported, definition value and two forall binders, Nat domain, empty universes, and transitive allowed-axiom closure of ExpectedType and Nat.Perfect. Output: `∀ (n : ℕ), n.Perfect → Even n`. Earlier unrelated frozen conjectures contain placeholders but are not in that closure. See package `audit.log`.
- Same generated `.lean`, `.olean`, `.ilean`, generator, reproducibility command, audit source/log and manifest copied byte-for-byte into both trusted packages. The verifier never runs generation or recompilation of Spec.

## Static checks

Both checker ASTs parse and bytes match. Both package file maps match. Golden/public Target and GoldenCheck remain unchanged. Frozen hashes, theorem header, banned-pattern rules, editable-tree rules, allowed-axiom audit and sorry canary retained. No ordinary def/lemma/instance ban added. Target imports no additional upstream module, so no extra prebuild modules needed. Dockerfile now ends with `USER ubuntu` and `RUN lake build +FormalConjecturesBench.Target`; final image history records that successful build.

Trusted Spec is fixed at `TESTS_DIR/trusted_spec`. Compiler executable and precompiled trusted dependency roots are fixed and precede candidate imports; normal extra LEAN_PATH imports are retained after those roots. Candidate Lean sources are compiled recursively in a fresh copy as ubuntu, using original golden Lean options, not candidate Lake configuration or old caches. Only temporary Target is transformed to import Spec before Submission and reuse the trusted prefix and original `namespace PerfectNumbers; open Nat` context. Complete type check references the pre-elaborated ExpectedType value, not a re-parsed proposition. Runtime audits use precompiled Spec. Missing or corrupt package/version/input fails without fallback.

## Current local Harbor build and real entry points

CLI help read first; `--no-delete` alone actually tears down containers in this installed Harbor, so the first successful trial auto-removed its container. Read the implementation and repeated with the supported Docker kwarg `keep_containers=true`.

Commands:

```
harbor run --path /root/FormalConjectures-Bench/tasks-v3/wikipedia-perfectnumbers-odd-perfect-number-conjecture-prove --agent nop --env docker --no-delete --job-name oddperfect-prove-nt40-143048 --jobs-dir /tmp/oddperfect-harbor-jobs --n-concurrent 1
harbor run --path /root/FormalConjectures-Bench/tasks-v3/wikipedia-perfectnumbers-odd-perfect-number-conjecture-prove --agent nop --env docker --no-delete --ek keep_containers=true --job-name oddperfect-prove-retain-nt40-143048 --jobs-dir /tmp/oddperfect-harbor-jobs --n-concurrent 1
```

Both jobs completed with zero exceptions, reward 0 (original sorry). No registry task used, no socket or extra host dependency mount. First own image `wikipedia-perfectnumbers-odd-per__4mdnf88__env-main:latest`, ID `sha256:742e3dc92c926fe896934f941fbf680b3223f48cb581ddd5ac104670febdad44`; container short ID `f858935fe863` was automatically removed by Harbor. Retained trial uses own image `wikipedia-perfectnumbers-odd-per__rhsrbnr__env-main:latest`, ID `sha256:9d2d435c8354be87d18a7298731ddb24e8ccf22e24ccb5b0893a2b6836e39021`; container identity in `oddperfect-harbor-resource.txt`.

Harbor uploaded `/tests` at verifier time and provided `/logs/verifier`. Restarted retained child container after Harbor stopped it. Actual commands in that same child:

- `docker exec wikipedia-perfectnumbers-odd-per__rhsrbnr__env-main-1 bash /tests/test.sh`: exit 1, `/logs/verifier/reward.txt` = 0. Script sets `FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests` (its unchanged bytes verified). Expected failure: banned original `sorry`.
- `docker exec -u ubuntu ... bash -c 'cd /app && ./check.sh'`: exit 1 for the same expected original sorry.
- Compared host hashes against container `/tests` (17 files) and `/opt/formal-conjectures-bench-checker` (16 files), including both checkers, all Spec artifacts and golden inputs: every file matches (`oddperfect-container-hashes.json`).
- Executed instruction search in final container; `rg --glob '*.lean' '^def Perfect \(' /app /opt/formal-conjectures /opt/formal-conjectures/.lake/packages`: exit 0, finds package `Mathlib/NumberTheory/Divisors.lean`.

## Supplemental coverage in the same Harbor child

Production entry stops before compilation because original Target has sorry. `oddperfect-supplement.py` calls the actual checker functions on isolated temporary fixtures, without modifying production checker, Target or golden, or relaxing a production check. It was run twice as ubuntu: `FCB_TESTS_DIR=/tests` and `FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker`, both exit **0**. Logs explicitly show the different fixed package paths. Code imported from `/tests` and both checker copies were byte-verified identical.

Actually covered:

1. Original header accepted; original sorry syntax rejected.
2. Frozen prefix modification rejected; extra Lean source outside editable tree rejected; original frozen file/tree rules accepted on valid fixture.
3. Fixed package validation and independent complete trusted-type/public-axiom audit succeed.
4. Ubuntu compilation of isolated original placeholder fixture succeeds; full candidate type matches ExpectedType; target axiom audit explicitly rejects `sorryAx`; sorry canary succeeds.
5. Semantic negative fixture keeps prefix and header **byte-identical**, adds normal `PerfectNumbers.Even (_ : Nat) : Prop := True` to Submission and uses a trivial proof. Syntax/frozen/tree checks and ubuntu compilation pass; target has allowed axioms; **complete type comparison fails with Lean Type mismatch** between `n.Perfect → PerfectNumbers.Even n` and ExpectedType.
6. Compiled fake same-name `FCBTrustedSpec.olean` placed in candidate cache, external LEAN_PATH and temporary project. `--deps` still resolves `/tests/trusted_spec/FCBTrustedSpec.olean` (or the `/opt` fixed package in local run); trusted audit still prints original full proposition.
7. Temporarily copied package with missing .olean fails explicitly, leaves artifact missing; corrupt .olean fails hash; changed manifest fails pinned hash. No runtime regeneration occurs. Real package restored only by restoring the independent test variable; production files were never changed.

These are infrastructure tests, **not** a proof of the conjecture. The honest theorem-proof success/reward-1 branch remains untested because no full mathematical proof was supplied or sought as a deliverable.
