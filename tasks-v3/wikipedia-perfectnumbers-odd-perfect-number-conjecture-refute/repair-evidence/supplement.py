import importlib.util, os, shutil, tempfile, hashlib, json
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
os.environ['FCB_TESTS_DIR']='/tests'
s=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
c=importlib.util.module_from_spec(s); s.loader.exec_module(c)
results=[]
def good(label,fn):
    fn(); results.append({'case':label,'result':'passed'}); print('PASS',label,flush=True)
def reject(label,fn):
    try: fn()
    except SystemExit as e:
        assert e.code != 0
        results.append({'case':label,'result':'rejected'}); print('REJECTED',label,flush=True)
    else: raise AssertionError('unexpected acceptance: '+label)
good('fixed manifest, inputs, toolchain and artifact verification', c.load_trusted_spec)
with c.make_fresh_golden_project() as t:
    p=Path(t)
    good('precompiled ExpectedType complete value and transitive axiom audit',lambda:c.check_trusted_type(p))
    good('ubuntu candidate compilation (isolated original sorry fixture)',lambda:c.check_build(p))
    good('original complete theorem type comparison',lambda:c.check_golden_theorem_import(p))
    reject('target axiom audit detects sorryAx',lambda:c.check_axioms(p))
    good('sorry canary',lambda:c.check_sorry_canary(p))
    # Corrupt candidate homonyms cannot replace fixed Spec or trusted imports.
    (p/'FCBTrustedSpec.olean').write_bytes(b'candidate counterfeit')
    fake=p/'.lake/build/lib/lean'; fake.mkdir(parents=True)
    (fake/'FCBTrustedSpec.olean').write_bytes(b'candidate cache counterfeit')
    dep=p/'FormalConjectures/Util'; dep.mkdir(parents=True)
    (dep/'ProblemImports.olean').write_bytes(b'candidate dependency counterfeit')
    os.environ['LEAN_PATH']=str(fake)
    good('Spec and dependency homonyms/cache/environment do not shadow fixed modules',lambda:c.check_golden_theorem_import(p))
    deps=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
    assert deps.returncode==0 and str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout
    print('FIXED IMPORT RESOLUTION\n'+deps.stdout,flush=True)
    good('trusted type audit still identical after counterfeit modules',lambda:c.check_trusted_type(p))
text=c.target_text()
reject('frozen prefix mutation',lambda:c.check_frozen_prefix_and_header('-- altered\n'+text))
reject('changed theorem header',lambda:c.check_frozen_prefix_and_header(text.replace('¬ (','(')))
reject('missing proof assignment',lambda:c.check_frozen_prefix_and_header(text.replace(') := by',') by')))
reject('original placeholder syntax',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(text)))
with tempfile.TemporaryDirectory(prefix='odd-perfect-refute-fixture-') as t:
    p=Path(t); shutil.copytree('/tests/golden_env',p,dirs_exist_ok=True)
    old_task,old_target=c.TASK_DIR,c.TARGET
    c.TASK_DIR=p; c.TARGET=p/c.TARGET_REL
    c.TARGET.write_text(text.replace('  sorry\n\nend PerfectNumbers','  intro h\n  exact h 0 True.intro\n\nend PerfectNumbers'))
    (p/'FormalConjecturesBench/Submission.lean').write_text('import FormalConjectures.Util.ProblemImports\nnamespace PerfectNumbers\ndef Perfect (_ : ℕ) : Prop := True\ndef Even (_ : ℕ) : Prop := False\nend PerfectNumbers\n')
    good('semantic attack preserves original frozen prefix/header',lambda:c.check_frozen_prefix_and_header(c.target_text()))
    good('semantic attack obeys source restrictions',lambda:(c.check_editable_tree_shape(),c.check_extra_lean_files_confined(),c.check_frozen_files_unchanged(),c.check_no_banned_patterns_in_editable_sources()))
    with c.make_fresh_golden_project() as inner:
        q=Path(inner)
        good('semantic attack compiles as ubuntu without placeholders',lambda:c.check_build(q))
        good('semantic attack itself passes axiom audit',lambda:c.check_axioms(q))
        reject('semantic attack rejected by complete trusted type comparison',lambda:c.check_golden_theorem_import(q))
    reject('actual checker main rejects unchanged-text semantic attack',c.main)
    (p/'Forbidden.lean').write_text('def forbidden := 1\n')
    reject('out-of-bounds Lean source',c.check_extra_lean_files_confined)
    (p/'Forbidden.lean').unlink()
    (p/'FormalConjecturesBench/bad.txt').write_text('x')
    reject('non-Lean editable source',c.check_editable_tree_shape)
    c.TASK_DIR,c.TARGET=old_task,old_target
old_spec=c.SPEC_DIR
for mode in ['missing','corrupt']:
    with tempfile.TemporaryDirectory(prefix='odd-perfect-refute-artifact-') as t:
        d=Path(t)/'spec'; shutil.copytree(old_spec,d); c.SPEC_DIR=d
        f=d/'FCBTrustedSpec.olean'
        if mode=='missing': f.unlink()
        else: f.write_bytes(b'bad artifact')
        before={str(x.relative_to(d)):hashlib.sha256(x.read_bytes()).hexdigest() for x in d.rglob('*') if x.is_file()}
        reject(mode+' Spec precompiled artifact fails closed',c.load_trusted_spec)
        after={str(x.relative_to(d)):hashlib.sha256(x.read_bytes()).hexdigest() for x in d.rglob('*') if x.is_file()}
        assert before==after, 'runtime regenerated Spec'
        print('NO RUNTIME REGENERATION',mode,flush=True)
c.SPEC_DIR=old_spec
for rel in ['test_target.py','GoldenCheck.lean','golden_env/FormalConjecturesBench/Target.lean']:
    assert Path('/tests',rel).read_bytes()==Path('/opt/formal-conjectures-bench-checker',rel).read_bytes()
for f in old_spec.iterdir():
    assert f.read_bytes()==(Path('/opt/formal-conjectures-bench-checker/trusted_spec')/f.name).read_bytes()
print('ALL CHECKER/GOLDEN/SPEC COPIES IDENTICAL',flush=True)
Path('/tmp/odd-perfect-refute.supplement-results.json').write_text(json.dumps(results,indent=2))
