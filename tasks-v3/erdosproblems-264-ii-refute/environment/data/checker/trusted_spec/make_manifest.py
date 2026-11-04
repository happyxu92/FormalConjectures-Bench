"""Repair-time only: run after reproduce.sh in the locked clean image.
After regeneration, manually pin the resulting manifest hash in both checkers.
"""
import hashlib
import json
import platform
import subprocess
from pathlib import Path

pkg = Path(__file__).resolve().parent
root = Path('/opt/formal-conjectures')
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
manifest = {
    'task_id': 'erdosproblems-264-ii-refute',
    'target_name': 'Erdos264.formal_conjectures_bench_refutation',
    'universe_params': [],
    'platform': platform.machine(),
    'lean_version': subprocess.check_output([
        '/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean', '--version'
    ], text=True).strip(),
    'formal_conjectures_commit': '233a10e857ef78e79fd9fe661d37db724089170a',
    'mathlib_commit': 'a3a10db0e9d66acbebf76c5e6a135066525ac900',
    'dependency_manifest_sha256': sha(root / 'lake-manifest.json'),
    'golden_files': {str(p.relative_to(pkg.parent / 'golden_env')): sha(p)
                     for p in sorted((pkg.parent / 'golden_env').rglob('*')) if p.is_file()},
    'files': {p.name: sha(p) for p in sorted(pkg.iterdir())
              if p.is_file() and p.name != 'manifest.json'},
}
(pkg / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
print(sha(pkg / 'manifest.json'))
