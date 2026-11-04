from pathlib import Path
import ast,hashlib,subprocess,tomllib
r=Path('/root/FormalConjectures-Bench/tasks-v3/erdosproblems-137-erdos-137-prove')
a=r/'tests';b=r/'environment/data/checker'
for f in [Path('test_target.py'),Path('GoldenCheck.lean'),*map(lambda x:Path('trusted_spec')/x.name,(a/'trusted_spec').iterdir()),*map(lambda x:Path('golden_env')/x.relative_to(a/'golden_env'),(a/'golden_env').rglob('*'))]:
 if not (a/f).is_file():continue
 h=hashlib.sha256((a/f).read_bytes()).hexdigest();assert (a/f).read_bytes()==(b/f).read_bytes(),f
 for d in ['/tests','/opt/formal-conjectures-bench-checker']:
  result=subprocess.check_output(['docker','exec','15f5c18424c0','sha256sum',str(Path(d)/f)],text=True)
  assert result.split()[0]==h,(f,d,result)
 print(h,str(f))
for p in [a/'test_target.py',b/'test_target.py']:ast.parse(p.read_text())
tomllib.loads((r/'task.toml').read_text())
f=(r/'environment/Dockerfile').read_text();assert f.rstrip().endswith('RUN lake build +FormalConjecturesBench.Target');assert f.rindex('USER ubuntu')<f.rindex('RUN lake build +FormalConjecturesBench.Target')
for p in ['environment/data/FormalConjecturesBench/Target.lean','tests/golden_env/FormalConjecturesBench/Target.lean','environment/data/checker/golden_env/FormalConjecturesBench/Target.lean','tests/GoldenCheck.lean','environment/data/checker/GoldenCheck.lean']:
 orig=subprocess.check_output(['git','-C','/root/FormalConjectures-Bench','show','HEAD:tasks-v3/'+r.name+'/'+p])
 assert orig==(r/p).read_bytes(),p
print('All golden/Target/GoldenCheck files unchanged. AST/TOML/Dockerfile static checks pass. Complete host and final Harbor /tests + /opt package hashes match.')
