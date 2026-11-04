# Infrastructure validation

## Generation / identity

- Shared trusted generation image reused read-only as base: `sha256:6b765e0c2f2503ee3818b3da5a0fdf24070a4773338acda6948d090217a7065a`. No registry task image used for final acceptance.
- Own generation container: `10968617906f00841fc1259a5da5de036c796aba95d3ac588530ab0af950dfa9` (`fcb32-refute-spec-20261104`), network none; only this task's golden and generator copied to `/tmp/erdos32-refute-bundle`.
- Command: `docker exec -u root fcb32-refute-spec-20261104 bash /tmp/erdos32-refute-bundle/trusted_spec/reproduce.sh`, exit 0.
- Generator uses Lean parser/elaborator, restores pre-target environment, exports only the entire target type as definition value. No temporary target theorem is exported. Full prefix is trusted golden minus Submission import; existing variant placeholders are not dependencies of ExpectedType or the prefix definition.
- Lean 4.27.0 x86_64; locked FormalConjectures and Mathlib revisions recorded in trusted_spec/manifest.json. Universe parameter list `[]`, outer forall binder count 0; full negation/existential/conjunction/little-o expression retained. Audit permits only propext/Classical.choice/Quot.sound.
- Manifest SHA256 `e01636d250888961bdfc2548ce96c0a1ec90a27803b9a691e4e92d6c246addf0`; input/source/artifact hashes in both identical manifests. Original Target SHA256 `35decaf5cc34cbda9abe246ba6aecda5982fe4bf9b5952d0eaeddf2cc81f7899`.

## Harbor acceptance

CLI help was read independently (`harbor --help`, `harbor trial start --help`).

```
harbor trial start --path /root/FormalConjectures-Bench/tasks-v3/erdosproblems-32-erdos-32-refute --trial-name fcb32-refute-accept2-20261104 --trials-dir /tmp/erdos32-refute-harbor --agent nop --env docker --no-delete --force-build --environment-kwarg keep_containers=true
```

Exit 0, Harbor exception_info null; image built from current task's environment/Dockerfile. Final image `sha256:d36cc2556744523219ca9feea8abf79d9ef868a64fd0f067ab4f5cc8e54d2a98`, tag `fcb32-refute-accept2-20261104__env-main:latest`. Actual retained Harbor container `5baa51b300f42a2c69b74b9d9f07481699bcf972beb43b393392ba3daa1f0553`. Harbor stops it on completion; explicitly restarted the same container for supplementary checks. No socket mounts, no extra host dependencies, no permission relaxation. A first attempt with only --no-delete auto-removed its container; its own image tag is `fcb32-refute-accept-20261104__env-main:latest`, ID `sha256:5990fd2abd6ec56a03485d107b721cb735b0ed02f24c398a46ecd77148d72db0`.

- `/tests` uploaded by Harbor verifier, not part of submission. `test.sh` sets FCB_TASK_DIR=/app and FCB_TESTS_DIR=/tests. `/logs/verifier` provided by Harbor.
- Re-executed `docker exec <id> bash /tests/test.sh`: exit 1, reward 0, expected source-rule rejection of original sorry.
- Re-executed `docker exec -u ubuntu <id> bash -lc 'cd /app && ./check.sh'`: exit 1, same expected rejection; check.sh uses FCB_TESTS_DIR=/opt/formal-conjectures-bench-checker.
- Byte-for-byte checker, Spec package, golden and test script comparisons against local files passed; `container-hashes.json` records hashes from `/tests` and `/opt`.
- Dockerfile ends in USER ubuntu and `RUN lake build +FormalConjecturesBench.Target`. Re-ran same dependency build as ubuntu: exit 0. No extra upstream imports in Target.
- Instruction command actually finds package `Mathlib/Analysis/Asymptotics/Defs.lean: irreducible_def IsBigOWith`; exit 0, no missing paths/permissions.

## Supplemental actual-function coverage

`docker exec <same Harbor id> python3 /tmp/erdos32-refute-coverage.py`, exit 0, full log in `erdos32-refute-coverage.log`, reproducible fixture in `coverage.py`. It imports the unchanged actual checker functions. Fixture alone permits existing placeholder body; it never bypasses production rules or claims a proof.

Covered paths:
- validated fixed precompiled Spec and independent trusted type/dependency axiom audit;
- candidate helper/Target compiled as ubuntu, trusted-type comparison passes for original complete statement;
- target axiom audit actually detects and rejects sorryAx;
- sorry canary succeeds;
- frozen prefix/header and missing := rejected;
- out-of-subtree Lean source rejected;
- semantic negative with identical frozen header and ordinary `Erdos32.Real.log` helper definition: candidate compiles, then complete trusted type comparison rejects the changed proposition (actual Lean mismatch in log constant);
- same-name candidate Spec source and corrupt cache plus environment override cannot replace loaded trusted Spec; subsequent candidate compile and type compare still succeed with original statement;
- missing compiled Spec explicitly fails, does not regenerate; corrupted artifact explicitly hash-fails.

No full original proof was attempted or supplied. Normal successful theorem-axiom-audit branch has no full theorem proof fixture; the actual rejection branch and canary were reached. Acceptance is infrastructure/type-isolation acceptance, not reward=1.

## Static final checks

Both checker ASTs parse and are identical. Both trusted package trees and every manifest digest agree. Original golden, public Target, frozen hash/header, and GoldenCheck are unchanged. See unicode JSON for original/header-negative verification. Runtime no longer uses GoldenCheck or parses the expected proposition in a candidate environment; it loads fixed ExpectedType instead.
