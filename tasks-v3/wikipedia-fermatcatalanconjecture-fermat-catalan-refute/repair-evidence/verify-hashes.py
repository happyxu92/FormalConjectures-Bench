from pathlib import Path
import subprocess,hashlib,json,ast,tomllib
r=Path('/root/FormalConjectures-Bench/tasks-v3/wikipedia-fermatcatalanconjecture-fermat-catalan-refute')
c='2b0be845ce5659d4732a3a343a543582b662f586e55ae5df0f0227092af98a74'
sha=lambda b:hashlib.sha256(b).hexdigest()
remote_code='''from pathlib import Path
import hashlib,json
roots=['/tests','/opt/formal-conjectures-bench-checker']
data={}
for root in roots:
 for p in Path(root).rglob('*'):
  if p.is_file() and '__pycache__' not in str(p):data[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
print(json.dumps(data))
'''
remote=json.loads(subprocess.check_output(['docker','exec',c,'python3','-c',remote_code]))
checks={}
for local,remote_root in [(r/'tests','/tests'),(r/'environment/data/checker','/opt/formal-conjectures-bench-checker')]:
 for p in local.rglob('*'):
  if p.is_file() and '__pycache__' not in str(p):
   key=remote_root+'/'+str(p.relative_to(local))
   assert remote[key]==sha(p.read_bytes()),key
   checks[key]=remote[key]
assert (r/'tests/test_target.py').read_bytes()==(r/'environment/data/checker/test_target.py').read_bytes()
for p in (r/'tests/trusted_spec').iterdir():
 assert p.read_bytes()==(r/'environment/data/checker/trusted_spec'/p.name).read_bytes()
for p in [r/'tests/test_target.py',r/'environment/data/checker/test_target.py']:ast.parse(p.read_text())
for rel in ['environment/data/FormalConjecturesBench/Target.lean','tests/GoldenCheck.lean','environment/data/checker/GoldenCheck.lean']:
 original=subprocess.check_output(['git','-C',str(r.parents[1]),'show','HEAD:'+str((r/rel).relative_to(r.parents[1]))])
 assert original==(r/rel).read_bytes(),rel
m=tomllib.loads((r/'task.toml').read_text())
assert m['metadata']['statement_status']=='consistent'
print(json.dumps({'container':c,'status':'all hashes match; both ASTs parse; public Target and GoldenChecks unchanged','files':checks},indent=2))
