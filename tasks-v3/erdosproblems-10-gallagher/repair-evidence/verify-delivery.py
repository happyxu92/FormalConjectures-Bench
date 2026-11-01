from pathlib import Path
import hashlib,json,subprocess
root=Path('/root/FormalConjectures-Bench/tasks-v3/erdosproblems-10-gallagher')
container='erdosproblems-10-gallagher__pkg6avm__env-main-1'
results={}
def command(args):
 r=subprocess.run(['docker','exec',*args],capture_output=True,text=True)
 return {'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
# Record official and local process exits explicitly.
for label,user,args in [('official','root',['bash','/tests/test.sh']),('local','ubuntu',['/app/check.sh'])]:
 results[label]=command(['-u',user,container,*args])
 assert results[label]['exit_code']==1 and 'Banned Lean feature' in results[label]['stderr']
for base,local in [('/tests',root/'tests'),('/opt/formal-conjectures-bench-checker',root/'environment/data/checker')]:
 hashes={}
 for p in sorted(local.rglob('*')):
  if not p.is_file() or '__pycache__' in p.parts:continue
  name=str(p.relative_to(local))
  r=command(['-u','ubuntu',container,'sha256sum',base+'/'+name])
  expected=hashlib.sha256(p.read_bytes()).hexdigest()
  assert r['exit_code']==0 and r['stdout'].split()[0]==expected,(base,name,r)
  hashes[name]=expected
 results[base]=hashes
results['reward']=command([container,'cat','/logs/verifier/reward.txt'])
assert results['reward']['stdout'].strip()=='0'
results['search']=command(['-u','ubuntu',container,'rg','--glob','*.lean','^theorem card_powerset','/app','/opt/formal-conjectures','/opt/formal-conjectures/.lake/packages'])
assert results['search']['exit_code']==0 and '/.lake/packages/mathlib/' in results['search']['stdout']
results['image']=subprocess.run(['docker','image','inspect','erdosproblems-10-gallagher__pkg6avm__env-main','--format','{{.Id}}'],capture_output=True,text=True,check=True).stdout.strip()
results['test_entry']=command([container,'cat','/tests/test.sh'])
assert 'FCB_TASK_DIR=/app FCB_TESTS_DIR=/tests python3 /tests/test_target.py' in results['test_entry']['stdout']
results['target_sha256']=command([container,'sha256sum','/app/FormalConjecturesBench/Target.lean'])
assert results['target_sha256']['stdout'].split()[0]==hashlib.sha256((root/'environment/data/FormalConjecturesBench/Target.lean').read_bytes()).hexdigest()
(root/'repair-evidence/delivery.json').write_text(json.dumps(results,indent=2)+'\n')
print('Harbor-uploaded /tests, installed /opt checker/Spec/golden, entries, original Target, package search: passed')
