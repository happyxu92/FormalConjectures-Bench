# Repair-time trusted Spec

Input: immutable `../golden_env`, Lean v4.27.0, Formal Conjectures 233a10e857ef78e79fd9fe661d37db724089170a, mathlib a3a10db0e9d66acbebf76c5e6a135066525ac900, Linux x86_64.

Reproduce in the task Docker image, with no candidate modules or caches loaded:

```
python3 /tmp/ctrefute-input/trusted_spec/generate.py
cd /tmp/ctrefute-input/trusted_spec
export LEAN_PATH=$PWD:/opt/formal-conjectures/.lake/build/lib/lean
for name in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  export LEAN_PATH=$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$name/.lake/build/lib/lean
done
/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean -o FCBTrustedSpec.olean FCBTrustedSpec.lean
/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean AuditSpec.lean
```

The generation restores the environment before exporting ExpectedType; no temporary theorem or proof is exported. Audit traverses the resulting type and all original prefix declarations. The verifier only imports the fixed compiled artifact, never regenerates it. See manifest and generation-audit.log.
