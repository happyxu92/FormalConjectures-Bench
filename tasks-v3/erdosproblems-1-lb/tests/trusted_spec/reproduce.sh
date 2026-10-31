#!/usr/bin/env bash
# Repair-time generation only. Never invoked by the verifier.
set -euo pipefail
cd "$(dirname "$0")"
python3 generate.py
export LEAN_PATH="$(find /opt/formal-conjectures/.lake/packages -path '*/.lake/build/lib/lean' -type d | sort | paste -sd:):/opt/formal-conjectures/.lake/build/lib/lean:$PWD"
lean_bin=/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean
"$lean_bin" -DautoImplicit=false -DrelaxedAutoImplicit=false -Dpp.unicode.fun=true -DmaxHeartbeats=0 -DmaxRecDepth=4000 -DsynthInstance.maxHeartbeats=20000 -DsynthInstance.maxSize=128 -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
"$lean_bin" AuditSpec.lean
# Regenerating artifacts requires regenerating and pinning the manifest hashes.
