#!/bin/bash
# Repair-time only. Use the matching Docker toolchain and original golden_env.
set -euo pipefail
cd "$(dirname "$0")"
python3 generate.py
TC=/opt/elan/toolchains/leanprover--lean4---v4.27.0
DEP=/opt/formal-conjectures
export LEAN_PATH="$PWD"
for pkg in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  LEAN_PATH="$LEAN_PATH:$DEP/.lake/packages/$pkg/.lake/build/lib/lean"
done
export LEAN_PATH="$LEAN_PATH:$DEP/.lake/build/lib/lean:$TC/lib/lean"
"$TC/bin/lean" -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
"$TC/bin/lean" AuditSpec.lean | tee audit.log
