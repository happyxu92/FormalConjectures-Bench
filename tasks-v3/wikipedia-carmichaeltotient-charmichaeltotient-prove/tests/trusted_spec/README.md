# Repair-time trusted Spec (not a proof)

Input: this task's unchanged `golden_env/FormalConjecturesBench/Target.lean`.
`generate.py` removes only Submission's import and the final target doc comment,
asks Lean's command parser/elaborator for the full declaration type and ordered
universes, then restores the environment before exporting ExpectedType's value.
The temporary target and its placeholder proof are not exported. AuditSpec checks
this and recursively audits ExpectedType and every task prefix declaration.

Generation was performed in a fresh Docker container built from the dependency
stages of this task's Dockerfile (Ubuntu 24.04, Linux x86_64), using the pinned
v4.27.0 compiler directly, without a candidate project, Lake config, or cache.

Reproduction at repair time only:

```sh
python3 generate.py
export LEAN_PATH="$(pwd):/opt/formal-conjectures/.lake/build/lib/lean"
for n in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  export LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$n/.lake/build/lib/lean"
done
LEAN=/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean
"$LEAN" -o FCBTrustedSpec.olean FCBTrustedSpec.lean
"$LEAN" AuditSpec.lean
```

The verifier validates the pinned manifest and artifacts, loads only the compiled
module, and never invokes generate.py or recompiles Spec. No proof of the open
conjecture is included. ExpectedType has no universe parameters.
