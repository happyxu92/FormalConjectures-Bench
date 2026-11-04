# Infrastructure validation

## Steps 1–3

- Instruction search now explicitly covers /app, /opt/formal-conjectures, and
  /opt/formal-conjectures/.lake/packages. Running the exact command (substituting
  `def totient`) as ubuntu in the final Harbor container returned 0 and found the
  package definition; see search-validation.log.
- Target has only ProblemImports and local Submission imports; no additional
  upstream module needed. Dockerfile now ends with ubuntu/HOME and
  `RUN lake build +FormalConjecturesBench.Target`. Image build succeeded, and the
  same command was rerun as ubuntu in the final container (exit 0;
  ubuntu-lake-build.log). Trusted dependency permissions were not relaxed.
- Skill check_unicode_header.py ran before semantic edits and again afterward:
  case no_issue, original header accepted, altered header and missing assignment
  rejected. Both checker copies agree. See unicode*.json.

## Repair-time Spec

Original golden Target SHA256:
34d076cea0fc7cd3fc1720c11164370f61b6bfbdf4a89b65dd722881474a7fd8.
Manifest SHA256:
214a9d926c721fa4d02465738cc0806bcc19e1d1428473df2a6483a4584be646.
All source/compiled-artifact hashes, pinned Lean version, platform, dependency
manifest hash, revisions, and ordered universes are in both trusted_spec/manifest.json
files. Ordered target universe parameters: []. The full proposition retains the
implicit n parameter. No proof of the conjecture is exported or delivered.

The Spec dependency image was built from this task's Dockerfile stages preceding
COPY data, with a task-unique tag:

```sh
docker build --progress=plain -t fcb-carmichael-prove-spec:20261104 \
  -f /tmp/carmichael-prove-spec.Dockerfile \
  /root/FormalConjectures-Bench/tasks-v3/wikipedia-carmichaeltotient-charmichaeltotient-prove/environment
```

Image ID: sha256:257e2c7b8a9602fa785193d0321a59663019f2753979a6c5ac69a27abb5d111a.
Spec generation used a fresh second container and the exact direct compiler and
fixed dependency paths in trusted_spec/README.md. Generation and independent
AuditSpec import exited 0; generation2.log audits all three task-prefix
constants and ExpectedType transitively, allowing only standard axioms. The
placeholder declaration is absent, ExpectedType is a definition with proposition
value, not an axiom/string, and no sorryAx is reachable.

An initial attempt used `lake env` in /opt: because the image removes .git, Lake
recloned packages in that disposable container; invoking elan outside a project
also lacked a default toolchain. No shared filesystem was touched. This attempt
was discarded, not used for artifacts, and fixed with a fresh container and direct
pinned compiler/precompiled imports (generation.log versus generation2.log).

## Current local-task Harbor build and entry points

Read `harbor --help` and `harbor run --help` independently. Builds used the actual
local task, not a registry task/image. Final retained build command:

```sh
harbor run -p /root/FormalConjectures-Bench/tasks-v3/wikipedia-carmichaeltotient-charmichaeltotient-prove \
  --agent nop --env docker --no-delete --ek keep_containers=true \
  --job-name fcb-carmichael-prove-keep-20261104 \
  --jobs-dir /tmp/carmichael-prove-harbor -n 1 \
  --extra-docker-compose /tmp/carmichael-prove-compose.yaml
```

The first build succeeded but default network allocation failed because the host
address pools were exhausted. Inspected existing networks without deleting any;
an overlay used a free task-specific subnet 10.249.137.0/24. No socket/extra host
dependencies or elevated permissions were added. A second completed trial showed
that --no-delete alone still removes containers in this Harbor version; reading
its Docker backend identified keep_containers=true. The final trial retained its
container, which was restarted for supplemental tests.

Final local-build image:
`wikipedia-carmichaeltotient-char__p9kcfm7__env-main:latest`,
sha256:d619bc3d04745a7a4e14294a2a9b9562eb5aea9b9fa248e1d5dfd8521b1ddb1d.
Final Harbor child: b6d28e4fe769 (full identity in resources.json).
Harbor supplied /tests (including the compiled package) and /logs/verifier.
Container bytes for both checkers, both complete Spec packages, both golden trees,
GoldenCheck files and entry scripts matched host files (31 files); public Target
also matched. See container-hashes.json. /tests/test.sh explicitly supplies
FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests. Local /app/check.sh supplies /opt's
checker path; neither checker nor Spec source was placed into the submission tree.

Actual commands in this same child:

- `docker exec -u root b6d28e4fe769 bash /tests/test.sh`: exit 1, reward 0,
  solely the expected original proof-region sorry rejection.
- `docker exec -u ubuntu b6d28e4fe769 bash /app/check.sh`: exit 1, same expected
  sorry rejection. See official-entry.log and local-entry.log.
- `docker exec -u root b6d28e4fe769 python3 /tmp/carmichael-prove-coverage.py`:
  exit 0, all 17 tests, fixed Spec loaded from /tests/trusted_spec.
- `docker exec -u ubuntu -e CARMICHAEL_COVERAGE_TESTS=/opt/formal-conjectures-bench-checker b6d28e4fe769 python3 /tmp/carmichael-prove-coverage.py`:
  exit 0, all 17 tests, fixed Spec loaded from /opt's package.

The delivered supplemental.py calls the actual checker functions in independent
/tmp fixtures; it never alters official checker, public Target, or golden, and
does not disable any formal-entry check. Logs and per-test JSON are included.
Coverage includes trusted Spec identity/value/universes/transitive axiom audit;
ubuntu candidate compilation; matching complete-type comparison on a placeholder
fixture; rejection of that fixture's sorryAx by the actual target axiom audit;
sorry canary; unchanged-frozen-text LT-instance semantic attack, which compiles,
is axiom-clean, and is rejected specifically by complete-type comparison (also by
full checker main); changed frozen-prefix rejection; out-of-tree source rejection;
invalid same-name candidate compiled module/cache and injected environment cannot
replace Spec; missing and corrupted artifacts fail without regenerating anything.

Both Python ASTs parse; checker bytes and Spec package bytes agree. Original
frozen-prefix/header checks, bans, tree checks, axiom audit and canary calls remain
in main. No runtime Spec generation or GoldenCheck execution remains. Only the
verification copy of Target is transformed, importing Spec before Submission and
using Spec's original-named prefix definitions. Normal editable helper definitions,
instances, and imports remain supported. The compiler uses trusted fixed paths
before the fresh candidate project; candidate Lake configuration/caches do not
supply Spec or its dependencies.

No complete proof was requested, supplied, or accepted for the open conjecture.
The original formal entry stops early as designed; all mandated later paths were
covered separately, not inferred from that early failure. General compiler/plugin
sandboxing and arbitrary initializer execution are outside this repair's scope.

Resource ownership, initial inventory, task-specific image identifiers, network,
and cleanup verification are recorded alongside this document. Only the explicitly
recorded resources created by this task are eligible for cleanup.
