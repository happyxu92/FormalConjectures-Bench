"""Repair-time only; run after reproduce.sh in the pinned Docker environment."""
import hashlib
import json
import platform
import subprocess
from pathlib import Path

pkg = Path(__file__).resolve().parent
golden = pkg.parent / 'golden_env'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = {
    'task_id': 'erdosproblems-1-erdos-1-prove',
    'target_name': 'Erdos1.erdos_1',
    'universe_params': [],
    'platform': platform.machine(),
    'lean_version': subprocess.check_output(['/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean', '--version'], text=True).strip(),
    'formal_conjectures_commit': '233a10e857ef78e79fd9fe661d37db724089170a',
    'mathlib_commit': 'a3a10db0e9d66acbebf76c5e6a135066525ac900',
    'dependency_manifest_sha256': sha(Path('/opt/formal-conjectures/lake-manifest.json')),
    'golden_files': {str(p.relative_to(golden)): sha(p) for p in sorted(golden.rglob('*')) if p.is_file()},
    'files': {p.name: sha(p) for p in sorted(pkg.iterdir()) if p.is_file() and p.name != 'manifest.json'},
}
(pkg / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
