import ast
import hashlib
import json
import subprocess
from pathlib import Path
r=Path('/root/FormalConjectures-Bench/tasks-v3/erdosproblems-1-erdos-1-prove')
c='erdos1-prove-final-net-20261104__env-main-1'
sha=lambda b:hashlib.sha256(b).hexdigest()
for left,right in [('tests/test_target.py','environment/data/checker/test_target.py')]:
    assert (r/left).read_bytes()==(r/right).read_bytes()
    ast.parse((r/left).read_text())
pkg=r/'tests/trusted_spec'
other=r/'environment/data/checker/trusted_spec'
assert sorted(x.name for x in pkg.iterdir())==sorted(x.name for x in other.iterdir())
for p in pkg.iterdir(): assert p.read_bytes()==(other/p.name).read_bytes()
manifest=json.loads((pkg/'manifest.json').read_text())
for name,digest in manifest['files'].items(): assert sha((pkg/name).read_bytes())==digest
for name,digest in manifest['golden_files'].items():
    assert sha((r/'tests/golden_env'/name).read_bytes())==digest
    assert sha((r/'environment/data/checker/golden_env'/name).read_bytes())==digest
    assert sha((r/'environment/data'/name).read_bytes())==digest
for local,remote in [('tests','/tests'),('environment/data/checker','/opt/formal-conjectures-bench-checker')]:
    for sub in ['test_target.py','test.sh','GoldenCheck.lean']:
        p=r/local/sub
        if p.exists():
            result=subprocess.check_output(['docker','exec',c,'sha256sum',remote+'/'+sub],text=True)
            assert result.split()[0]==sha(p.read_bytes()),result
    for subroot in ['golden_env','trusted_spec']:
        for p in (r/local/subroot).rglob('*'):
            if not p.is_file(): continue
            rel=p.relative_to(r/local)
            result=subprocess.check_output(['docker','exec',c,'sha256sum',remote+'/'+str(rel)],text=True)
            assert result.split()[0]==sha(p.read_bytes()),result
print('PASS: AST, synchronized checkers/packages, all pinned artifact/golden hashes, and final Harbor /tests + /opt hashes')
