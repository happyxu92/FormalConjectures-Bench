import hashlib, json, subprocess
from pathlib import Path
root = Path('/root/FormalConjectures-Bench/tasks-v3/wikipedia-gausscircleproblem-error-isbigo-refute')
pkg = root/'tests/trusted_spec'
container='fcb-gauss-refute-spec-nt40-20261104'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def cmd(*args): return subprocess.check_output(['docker','exec',container,*args],text=True).strip()
(pkg/'audit.log').write_bytes(Path('/tmp/gauss-refute-spec-generation.log').read_bytes())
deps=json.loads(cmd('python3','-c',"from pathlib import Path; print(Path('/opt/formal-conjectures/lake-manifest.json').read_text())"))
manifest={
 'task_id':root.name,'target_name':'GaussCircleProblem.formal_conjectures_bench_refutation',
 'lean_version':cmd('/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean','--version'),
 'platform':'x86_64','universe_params':[],
 'formal_conjectures_commit':'233a10e857ef78e79fd9fe661d37db724089170a',
 'dependency_revisions':{x['name']:x['rev'] for x in deps['packages']},
 'dependency_manifest_sha256':cmd('sha256sum','/opt/formal-conjectures/lake-manifest.json').split()[0],
 'golden_files':{str(p.relative_to(root/'tests/golden_env')):sha(p) for p in sorted((root/'tests/golden_env').rglob('*')) if p.is_file()},
 'files':{p.name:sha(p) for p in sorted(pkg.iterdir()) if p.is_file() and p.name!='manifest.json'},
 'generation_image':subprocess.check_output(['docker','inspect',container,'--format','{{.Image}}'],text=True).strip(),
 'generation_command':'docker run -d --network none --name fcb-gauss-refute-spec-nt40-20261104 --user root --workdir /tmp erdos1062-import-20261102__env-main:latest sleep infinity; docker cp trusted golden and generation sources to /tmp/fcb-gauss-refute-generation; docker exec fcb-gauss-refute-spec-nt40-20261104 bash /tmp/fcb-gauss-refute-generation/trusted_spec/reproduce.sh',
 'audit':'Independent import audited complete negated existential, empty universe list, ExpectedType/N/E transitive allowed axioms only. Temporary target and children absent. Original prefix solved theorem placeholders not in expected type dependencies.'
}
(pkg/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(sha(pkg/'manifest.json'))
