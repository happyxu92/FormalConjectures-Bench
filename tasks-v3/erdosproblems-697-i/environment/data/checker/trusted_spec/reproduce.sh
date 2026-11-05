#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export LEAN_PATH="$PWD:/opt/formal-conjectures/.lake/build/lib/lean"
for dep in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
 export LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$dep/.lake/build/lib/lean"
done
LEAN=/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean
"$LEAN" --version
"$LEAN" -DautoImplicit=false -DrelaxedAutoImplicit=false -DmaxHeartbeats=0 -DmaxRecDepth=4000 -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
"$LEAN" AuditSpec.lean
