from pathlib import Path
import ast, subprocess,hashlib,json,tomllib
r=Path('/root/FormalConjectures-Bench/tasks-v3/erdosproblems-17-erdos-17-refute')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
a=r/'tests/test_target.py';b=r/'environment/data/checker/test_target.py'
assert a.read_bytes()==b.read_bytes()
new=ast.parse(a.read_text())
base=ast.parse(subprocess.check_output(['git','-C','/root/FormalConjectures-Bench','show','HEAD:tasks-v3/erdosproblems-17-erdos-17-refute/tests/test_target.py'],text=True))
def constants(tree):return {n.targets[0].id:ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['EXPECTED_HEADER','EXPECTED_PREFIX_SHA256','BANNED_PATTERNS']}
assert constants(base)==constants(new)
for name in ['check_frozen_prefix_and_header','check_banned_patterns','check_editable_tree_shape','check_no_banned_patterns_in_editable_sources','check_extra_lean_files_confined','check_frozen_files_unchanged','check_axioms','check_sorry_canary']:
    get=lambda t:ast.dump(next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==name))
    assert get(base)==get(new),name
for p in (r/'tests/golden_env').rglob('*'):
    if p.is_file():
        rel=p.relative_to(r/'tests/golden_env')
        assert p.read_bytes()==(r/'environment/data/checker/golden_env'/rel).read_bytes()
        tracked='tasks-v3/'+r.name+'/tests/golden_env/'+str(rel)
        assert p.read_bytes()==subprocess.check_output(['git','-C','/root/FormalConjectures-Bench','show','HEAD:'+tracked])
for relative in ['environment/data/FormalConjecturesBench/Target.lean','tests/GoldenCheck.lean','environment/data/checker/GoldenCheck.lean']:
    assert (r/relative).read_bytes()==subprocess.check_output(['git','-C','/root/FormalConjectures-Bench','show','HEAD:tasks-v3/'+r.name+'/'+relative])
for p in (r/'tests/trusted_spec').iterdir():assert p.read_bytes()==(r/'environment/data/checker/trusted_spec'/p.name).read_bytes()
m=json.loads((r/'tests/trusted_spec/manifest.json').read_text())
for k,v in m['files'].items():assert sha(r/'tests/trusted_spec'/k)==v
assert r.joinpath('environment/Dockerfile').read_text().rstrip().endswith('RUN lake build +FormalConjecturesBench.Target')
assert tomllib.loads((r/'task.toml').read_text())['metadata']['statement_status']=='consistent'
hashes={str(p.relative_to(r/'tests')):sha(p) for p in (r/'tests').rglob('*') if p.is_file()}
Path('/tmp/ep17r-local-test-hashes.json').write_text(json.dumps(hashes))
print('PASS AST, synchronized checker/Spec, original restrictions/frozen baselines/golden/GoldenCheck/public Target unchanged, manifest hashes, Dockerfile final ubuntu build, TOML parse')
