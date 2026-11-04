# Infrastructure validation

## Changes
- instruction.md explicitly searches `/app`, `/opt/formal-conjectures`, and
  `/opt/formal-conjectures/.lake/packages`. Real-container `rg` found
  `mathlib/Mathlib/Data/PNat/Prime.lean:def Coprime`, exit 0.
- Target has only ProblemImports and local Submission imports. Dockerfile now
  ends with `USER ubuntu` and `RUN lake build +FormalConjecturesBench.Target`.
  Spec-stage local Docker build exercised this (7992 jobs, exit 0; original
  sorry warning expected). Final Harbor builds use the same validated layer.
- Skill Unicode script returned `case=no_issue`; original header passes,
  changed header and removed assignment are rejected. No header or frozen hash
  was refreshed.
- Both checkers load the same repair-time precompiled Spec. The manifest SHA256
  is pinned in the checkers, which validate golden inputs, every delivered
  artifact hash, platform, Lean version, dependency manifest, target and task.
- Direct locked Lean compilation preserves the original Lean options and normal
  dependency library paths, including optional Cli. The trusted Spec and trusted
  dependency libraries precede the fresh candidate project and ordinary
  candidate compiled-module cache. Candidate Lake configuration, caches and
  inherited Lean variables cannot override the trusted Spec. Ordinary helper
  definitions and imports, including an external precompiled fixture, remain
  accepted; no generic external-module whitelist was introduced.
- Temporary Target imports the trusted Spec first, then Submission, and keeps
  the original target text/namespace/scoped Function context, using the exact
  prefix definitions compiled in Spec. Complete type comparison refers only to
  ExpectedType and the root-qualified candidate constant. GoldenCheck files
  were not modified or executed by the new type-comparison path.

## Trusted generation and audit

Command: `docker build -t fcb-fermat-refute-spec:nt40-20261104 <task>/environment`.
A uniquely named, network-disabled container from that locally built image
received only golden_env and generation tools under
`/tmp/fcb-fermat-refute-generation`. Its `trusted_spec/reproduce.sh` generates
and compiles FCBTrustedSpec and independently imports AuditSpec.

The Lean command parser elaborates the complete original golden target after
removing Submission. It captures ConstantInfo.type and levelParams, restores
the environment before the temporary declaration, and exports a definition
whose value is the full expression. Independent audit confirms the temporary
target is absent, universes are empty, the complete expression is Not applied
to the original conjecture, with no syntactic forall binders, and all prefix
definitions and ExpectedType transitively use only allowed standard axioms.
The initial audit expected one syntactic binder for Not; actual Lean
forallTelescope showed zero. That audit assertion was corrected and generation
and independent audit were rerun successfully before manifesting delivery.
This was an audit-fixture issue, not a change to the proposition.

Versions, revisions, full input/source/artifact hashes, generation image ID and
command are recorded in both identical `trusted_spec/manifest.json` files.
FCBTrustedSpec source/olean/ilean and reproduction tools are delivered in both
packages. The verifier never calls the generator or rebuilds missing artifacts.

## Actual Harbor acceptance

CLI help was read independently (`harbor --help`, `harbor run --help`,
`harbor trial start --help`). Current local task path, not a registry image,
was used with nop agent. Latest accepted build:

```
harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/wikipedia-fermatcatalanconjecture-fermat-catalan-refute --trial-name fcb-fermat-refute-delivery3-nt40-20261104 --trials-dir /tmp/fcb-fermat-refute-harbor --agent nop --env docker --no-delete --force-build --environment-kwarg keep_containers=true --extra-docker-compose /tmp/fcb-fermat-refute-compose-delivery3.yaml
```

The overlay only selects unique subnet 10.247.201.0/24. No socket mount,
privilege escalation or external host dependency was added. Earlier attempts
hit exhausted default address pools; one unique-network attempt collided with
another agent's newly selected subnet. The final unused subnet succeeded.
`--no-delete` alone removes containers in this installed Harbor release;
`keep_containers=true` was needed to retain the acceptance container for
supplemental tests. No shared network was removed to work around these errors.

Latest container:
`2b0be845ce5659d4732a3a343a543582b662f586e55ae5df0f0227092af98a74`.
Image tag: `fcb-fermat-refute-delivery3-nt40-20261104__env-main:latest`.
Full image ID and all creation tags are in `docker-resources.json`.

Harbor supplied `/tests` and `/logs/verifier`; test.sh sets FCB_TASK_DIR=/app,
FCB_TESTS_DIR=/tests. All files in both container checker/golden/Spec trees
were hash-compared to the host delivery (`delivery-hashes.json`).
AST parse and both package-copy comparisons pass. Public Target, both
GoldenCheck files and golden files remain byte-for-byte unchanged.

In the same Harbor child container:
- `bash /tests/test.sh`: exit 1, reward 0, source sorry rejected as expected.
- `docker exec -u ubuntu ... bash /app/check.sh`: exit 1, same expected sorry
  rejection. This entry sets FCB_TESTS_DIR to the installed `/opt` checker.
- Independent supplemental program invokes the checker's actual functions;
  official `/tests` program as root (compiler explicitly drops to ubuntu): 0.
- Same program as ubuntu with installed `/opt` checker/Spec: 0.

Both supplemental executions actually cover:
1. Manifest validation and independent trusted-type/transitive axiom audit.
2. ubuntu build of an isolated placeholder fixture with the original type.
3. Successful complete type comparison against the actual negated conjecture.
4. Target axiom audit rejects `sorryAx`, then sorry canary detects it.
5. Ordinary helper/import compilation and external precompiled-module import.
6. Counterfeit same-name source/olean/cache and inherited LEAN_PATH cannot
   replace Spec; `lean --deps` resolves the validated trusted artifact.
7. Unchanged frozen prefix/header plus scoped name hijack makes candidate type
   `¬False`. The candidate compiles with a real proof of that changed type;
   complete type comparison actually rejects it. Preserved syntax ban also
   independently rejects that notation. The isolated diagnostic invokes later
   functions explicitly; it does not bypass or weaken the formal checker.
8. Frozen prefix, changed header, missing `:=`, and out-of-tree source rejected.
9. Missing and corrupt precompiled artifacts explicitly fail and are not
   regenerated. The normal helper declaration remains accepted.

The external-import supplemental fixture initially used Mathlib-only `lemma`
syntax without importing Mathlib. It was corrected to core `theorem` and both
supplemental runs were repeated to completion. No checker rule was relaxed.

No proof of the open mathematical target was attempted or delivered. There is
no positive full-checker fixture for that target; original source rejection
and explicit isolated later-stage tests are separately documented, not
misrepresented as a reward-1 result.
