#!/bin/bash
# Repair-time only. Run in a clean matching Docker image, after copying this
# package and the original golden_env to /tmp/green2-spec/tests/.
set -euo pipefail
cd /tmp/green2-spec/tests/trusted_spec
python3 generate.py
export PATH=/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin:/usr/bin:/bin
export LEAN_PATH="$PWD:/opt/formal-conjectures/.lake/build/lib/lean"
for p in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  export LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$p/.lake/build/lib/lean"
done
lean -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
lean AuditSpec.lean
lean --version
uname -m
sha256sum /opt/formal-conjectures/lake-manifest.json
