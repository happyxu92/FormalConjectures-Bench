# Infrastructure validation

Only this task was modified. Original public Target, three golden/public Target copies, both GoldenCheck files, frozen header and prefix hash remain unchanged (also compared byte-for-byte to git HEAD). No mathematical proof was supplied.

## Steps 1–3

- Instruction search now explicitly includes `/app`, `/opt/formal-conjectures`, and `/opt/formal-conjectures/.lake/packages`. Ran as ubuntu in final Harbor child: `rg --glob '*.lean' 'def ncard' /app /opt/formal-conjectures /opt/formal-conjectures/.lake/packages` -> exit 0, actual `Set.ncard` definition found under Mathlib; see search-path.log.
- Only imports are ProblemImports and local Submission. No extra upstream build target is necessary. Dockerfile now ends with `WORKDIR /app`, HOME, `USER ubuntu`, and `RUN lake build +FormalConjecturesBench.Target`. This build succeeded in current local Harbor builds (cached trusted base layers allowed).
- Ran the skill's `check_unicode_header.py` before and after repair: both `case=no_issue`, exit 0. Headers remain identical. See unicode.json.

## Trusted Spec generation and identity

- Container `fcb41-prove-spec-20261104`, ID `4167d1beb0e15aa9d2844dd2c666221e7e9798e686c41bbf83b7b10b39a228b6`, created with network none from pre-existing compatible base image `erdos1062-import-20261102__env-main:latest`, ID `sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`. This shared pre-existing image will not be removed.
- Copied only trusted golden and new generator to `/tmp/erdos41-bundle`. Ran `docker exec -u root fcb41-prove-spec-20261104 bash /tmp/erdos41-bundle/trusted_spec/reproduce.sh`. Generation environment excludes candidate source/config/cache paths from LEAN_PATH. First audit encountered a BinderInfo pretty-print instance error; corrected the audit to `repr`, reran successfully (exit 0). The complete declaration is parsed/elaborated by Lean; environment is restored before exporting only the type expression as a definition. The temporary theorem is checked absent by independent import.
- Full original prefix `Erdos41.NtupleCondition` retained with original name; Submission import removed for generation. ExpectedType has all three explicit binders (`A`, `h_triple`, `h_infinite`), no universe parameters. Independent AuditSpec checks ExpectedType is a definition of a proposition, binder count, temporary target absence, and transitive axioms of ExpectedType and NtupleCondition. Only propext/Classical.choice/Quot.sound; no sorryAx or task axiom. Generator's temporary placeholder warning is not an exported proof or dependency.
- Same generated source, .olean, .ilean, code, audit and manifest copied to both packages. Manifest SHA256 `37a4507355ccece019e795a8d8f15b30c63917ac2d70dda2428b53a814fb1820`, .olean SHA256 `261d468e480ff5913b4d1c6063f903f7ba0d034201e4870f73542f3f2e88482d`, original Target SHA256 `e60390817c9307e576d3c3556a45db83abd33c058186289e1dbd06cb9bb417d4`. Full input/artifact hashes, platform, exact Lean version and dependency revisions are in each trusted manifest.
- Checker pins manifest hash and verifies all artifacts and original golden inputs, toolchain version, platform and upstream dependency manifest. Uses SPEC_DIR from trusted tests location, fixed Lean executable and trusted library paths before temporary project. Does not use candidate Lake configuration or environment overrides to load Spec/dependencies. No runtime generation or source fallback. Candidate ordinary imports and allowed defs/lemmas/instances remain allowed. No new generic external-module whitelist/sandbox was added.
- Temporary candidate imports compiled Spec first and takes prefix definition from it; reconstructs original namespace/open/variable context without duplicating the prefix definition. Only temporary candidate copy changes. Full type check references `_root_.FCBTrustedSpec.ExpectedType` and `@_root_.Erdos41.erdos_41`, not GoldenCheck or a reparsed expected proposition. Existing freeze, source restrictions, axiom audit and canary remain on main's path.

## Current local Harbor builds and entrances

CLI help read independently (`harbor --help`, `harbor run --help`, `harbor trials start --help`). No registry task replacement, socket mount, elevated permissions or additional host dependency mounts.

1. `harbor run --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-41-erdos-41-prove --agent nop --env docker --force-build --no-delete --n-concurrent 1 --job-name fcb41-prove-accept-20261104 --jobs-dir /tmp/erdos41-harbor-jobs` succeeded. Harbor removed its container despite no-delete: this option retains images, not containers. Container `bed61d11e90f8576e35bcd6462fe77e369ab5fc8b58298bceb267357f7be60cd` was observed and subsequently confirmed absent.
2. Repeated with `harbor trials start ... --trial-name fcb41-prove-accept2-20261104 --trials-dir /tmp/erdos41-harbor-trials --agent nop --env docker --force-build --no-delete --environment-kwarg keep_containers=true`. Build, official entry and all supplemental tests succeeded with expected proof rejection. Restarted the retained Harbor child after Harbor stopped it. No public proof changed.
3. After metadata marking, final build `fcb41-prove-final-20261104` succeeded, but creating its bridge failed: Docker predefined address pools fully subnetted. Did not delete any pre-existing/shared network. Retried using this task's own #2 bridge as an external network via the minimal own-network.yaml. This repairs the operational obstacle without host mounts or permission changes.
4. Final acceptance command: `harbor trials start --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-41-erdos-41-prove --trial-name fcb41-prove-final2-20261104 --trials-dir /tmp/erdos41-harbor-final2 --agent nop --env docker --force-build --no-delete --environment-kwarg keep_containers=true --extra-docker-compose /tmp/erdos41-own-network.yaml`. Exit 0; final task image `sha256:3ce9405070228591903d9c1d2abeaf1c970768e4acb2d92f72fd8b44b93f77d1`. Child `3a49572e998e891187979796cbc5c1441093d7537fa60fa2457cdf9d987bb3e7` / `fcb41-prove-final2-20261104__env-main-1`. See harbor-config.json, harbor-result.json and harbor-final.log. The failed network attempt's successful build log is saved separately.

Harbor uploaded current `/tests` and provided `/logs/verifier`. Restarted its retained final child, not a manually created substitute. Both checker/Spec/golden trees in that child match all host hashes (container-hashes.json). Inspected `/tests/test.sh` supplies FCB_TASK_DIR=/app, FCB_TESTS_DIR=/tests. Local `/app/check.sh` supplies `/opt/formal-conjectures-bench-checker`.

- `docker exec <final-child> bash /tests/test.sh`: exit 1, reward 0, expected original sorry source-ban rejection.
- `docker exec -u ubuntu <final-child> /app/check.sh`: exit 1, same expected source-ban rejection.
- No claim that the original mathematical theorem was proved or the submission passed.

## Downstream coverage in the same final Harbor child

Copied independent supplement.py to `/tmp/erdos41-supplement.py`, not /app. Ran `docker exec -u ubuntu <final-child> python3 /tmp/erdos41-supplement.py` and again with argument `/opt/formal-conjectures-bench-checker`; both exit 0. This imports each actual checker, calls its real functions and uses isolated fixtures only. See formal-supplement.log and local-supplement.log.

Covered for **both fixed package locations**:

- validated and loaded compiled Spec, independent full-type/prefix axiom audit;
- compiled original placeholder fixture as ubuntu, full theorem type matched ExpectedType;
- target axiom audit actually rejected sorryAx; canary detected sorryAx;
- frozen prefix change and out-of-bounds added Lean source rejected;
- allowed-definition semantic attack (`Erdos41.Filter.atTop : Unit`, `Unit.liminf := 0`) passes unchanged frozen text/header, source syntax/tree/confinement and frozen file checks; candidate compiles with rfl and passes allowed-axiom audit; **actual complete type comparison rejects its changed proposition**;
- corrupt project-root same-name FCBTrustedSpec.olean and candidate .lake cache, plus malicious LEAN_PATH/LEAN_SYSROOT: actual --deps resolves verified trusted Spec, full-type check still passes;
- isolated package with missing .olean explicitly fails, does not regenerate; hash-corrupt .olean explicitly fails.

Static AST, checker equality, trusted-package equality/hashes, TOML and untouched mathematical inputs were checked. No unexplained infrastructure failures remain. Full proof-success branch is not covered because no proof was provided; all required downstream infrastructure paths were exercised separately without weakening official checks.

## Resources

Baseline resources recorded before any creation in `/tmp/erdos41-existing-containers.txt` and `/tmp/erdos41-existing-images.txt`. Ownership is by explicit names/IDs, not concurrent inventory diffs. Own images are listed in owned-images.txt; own containers above plus #2 `dbb5efec74d408a756811d5ec389dc365d8d894362e1c891f1f68689a1de2c48`. Own bridge ID `0147055520aafcc531fc444c01e49a19f2eb485628fba6fc78e0ff3201b7ebd8`. Cleanup is performed after report/evidence persistence and recorded in docker-cleanup.log and the final report. No shared base image or build cache is removed.
