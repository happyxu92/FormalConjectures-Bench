#!/usr/bin/env bash
# Repair-time generation only. Never invoked by the verifier.
set -euo pipefail
cd "$(dirname "$0")"
python3 generate.py
export LEAN_PATH="$PWD:/opt/formal-conjectures/.lake/build/lib/lean"
for dependency in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  export LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$dependency/.lake/build/lib/lean"
done
lean_bin=/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean
"$lean_bin" -DautoImplicit=false -DrelaxedAutoImplicit=false -Dpp.unicode.fun=true -DmaxHeartbeats=0 -DmaxRecDepth=4000 -DsynthInstance.maxHeartbeats=20000 -DsynthInstance.maxSize=128 -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
"$lean_bin" AuditSpec.lean
# Regenerating artifacts requires regenerating and pinning the manifest hashes.
