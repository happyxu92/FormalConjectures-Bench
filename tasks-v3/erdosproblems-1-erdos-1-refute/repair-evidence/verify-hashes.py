from pathlib import Path
import subprocess,hashlib,json
root=Path('/root/FormalConjectures-Bench/tasks-v3/erdosproblems-1-erdos-1-refute')
container='fcb-erdos1-refute-final2-20261104__env-main-1'
script='''from pathlib import Path
import hashlib,json
out={}
for root in [Path('/tests'),Path('/opt/formal-conjectures-bench-checker')]:
 for p in root.rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:out[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
print(json.dumps(out))
'''
p=subprocess.run(['docker','exec','-i',container,'python3','-'],input=script,text=True,capture_output=True,check=True)
remote=json.loads(p.stdout);result={}
for local_rel,dest in [('tests','/tests'),('environment/data/checker','/opt/formal-conjectures-bench-checker')]:
 local=root/local_rel
 for file in local.rglob('*'):
  if not file.is_file() or '__pycache__' in file.parts:continue
  name=dest+'/'+str(file.relative_to(local))
  digest=hashlib.sha256(file.read_bytes()).hexdigest()
  assert remote.get(name)==digest,(name,remote.get(name),digest)
  result[name]=digest
print(json.dumps({'status':'PASS','container':container,'files':result},indent=2))
