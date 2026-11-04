#!/bin/bash
# Repair time only: matched v4.27.0 Linux container, no candidate inputs.
set -euo pipefail
cd "$(dirname "$0")"
python3 generate.py
ROOT=/opt/formal-conjectures
TOOLCHAIN=/opt/elan/toolchains/leanprover--lean4---v4.27.0
export LEAN_PATH="$PWD:$ROOT/.lake/build/lib/lean:$TOOLCHAIN/lib/lean"
for pkg in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  export LEAN_PATH="$LEAN_PATH:$ROOT/.lake/packages/$pkg/.lake/build/lib/lean"
done
"$TOOLCHAIN/bin/lean" -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
"$TOOLCHAIN/bin/lean" AuditSpec.lean > audit.log
cat audit.log
