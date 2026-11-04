#!/usr/bin/env bash
# Repair-time only. Run in the matching task Docker toolchain, not the verifier.
set -euo pipefail
PKG="$(cd "$(dirname "$0")" && pwd)"
python3 "$PKG/generate.py"
cd "$PKG"
DEPS=/opt/formal-conjectures
TOOLCHAIN=/opt/elan/toolchains/leanprover--lean4---v4.27.0
export LEAN_PATH="$PKG:$DEPS/.lake/build/lib/lean:$TOOLCHAIN/lib/lean"
for name in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  export LEAN_PATH="$LEAN_PATH:$DEPS/.lake/packages/$name/.lake/build/lib/lean"
done
LEAN="$TOOLCHAIN/bin/lean"
"$LEAN" -DautoImplicit=false -DrelaxedAutoImplicit=false -DmaxHeartbeats=0 -DmaxRecDepth=4000 -DsynthInstance.maxHeartbeats=20000 -DsynthInstance.maxSize=128 -o "$PKG/FCBTrustedSpec.olean" -i "$PKG/FCBTrustedSpec.ilean" "$PKG/FCBTrustedSpec.lean"
"$LEAN" "$PKG/AuditSpec.lean" > "$PKG/audit.log"
"$LEAN" --version > "$PKG/lean-version.txt"
uname -m > "$PKG/platform.txt"
sha256sum /opt/formal-conjectures/lake-manifest.json > "$PKG/dependency-manifest.sha256"
