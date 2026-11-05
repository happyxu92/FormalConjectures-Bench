#!/usr/bin/env bash
# Repair time only; verifier never generates or compiles a Spec.
set -euo pipefail
cd "$(dirname "$0")"
python3 generate.py
export LEAN_PATH="$PWD:/opt/formal-conjectures/.lake/build/lib/lean"
for dep in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  export LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$dep/.lake/build/lib/lean"
done
lean=/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean
"$lean" --version
"$lean" -DautoImplicit=false -DrelaxedAutoImplicit=false -Dpp.unicode.fun=true -DmaxHeartbeats=0 -DmaxRecDepth=4000 -DsynthInstance.maxHeartbeats=20000 -DsynthInstance.maxSize=128 -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
"$lean" AuditSpec.lean
