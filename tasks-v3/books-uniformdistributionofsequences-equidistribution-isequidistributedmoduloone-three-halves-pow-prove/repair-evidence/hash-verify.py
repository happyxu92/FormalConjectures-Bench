from pathlib import Path
import subprocess,hashlib,json,ast
T=Path('/root/FormalConjectures-Bench/tasks-v3/books-uniformdistributionofsequences-equidistribution-isequidistributedmoduloone-three-halves-pow-prove')
C='books-uniformdistributionofseque__lfj2uzy__env-main-1'
paths={}
for f in (T/'tests').rglob('*'):
    if f.is_file():paths['/tests/'+str(f.relative_to(T/'tests'))]=f
for f in (T/'environment/data/checker').rglob('*'):
    if f.is_file():paths['/opt/formal-conjectures-bench-checker/'+str(f.relative_to(T/'environment/data/checker'))]=f
paths['/app/FormalConjecturesBench/Target.lean']=T/'environment/data/FormalConjecturesBench/Target.lean'
paths['/app/check.sh']=T/'environment/data/check.sh'
outputs=subprocess.check_output(['docker','exec',C,'sha256sum',*paths],text=True)
for line in outputs.splitlines():
    sha,path=line.split(maxsplit=1)
    assert sha==hashlib.sha256(paths[path].read_bytes()).hexdigest(),path
    print(line)
a=T/'tests/test_target.py'; b=T/'environment/data/checker/test_target.py'
assert a.read_bytes()==b.read_bytes()
ast.parse(a.read_text());ast.parse(b.read_text())
for f in (T/'tests/trusted_spec').iterdir():
    assert f.read_bytes()==(T/'environment/data/checker/trusted_spec'/f.name).read_bytes()
assert (T/'tests/golden_env/FormalConjecturesBench/Target.lean').read_bytes()==(T/'environment/data/FormalConjecturesBench/Target.lean').read_bytes()
print('PASS AST, checker/package synchronization, public Target unchanged, and all '+str(len(paths))+' container file hashes')
