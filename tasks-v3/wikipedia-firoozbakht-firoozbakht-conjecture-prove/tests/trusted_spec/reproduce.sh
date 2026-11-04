#!/bin/bash
# Repair-time only. Run from this directory in the pinned Linux task image.
set -euo pipefail
python3 ./generate.py
TC=/opt/elan/toolchains/leanprover--lean4---v4.27.0
export PATH="$TC/bin:/usr/bin:/bin"
export LEAN_PATH="$PWD"
for p in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$p/.lake/build/lib/lean"
done
export LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/build/lib/lean:$TC/lib/lean"
lean -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
lean AuditSpec.lean | tee audit.log
lean --version > lean-version.txt
uname -m > platform.txt
sha256sum /opt/formal-conjectures/lake-manifest.json > dependency-manifest.sha256
