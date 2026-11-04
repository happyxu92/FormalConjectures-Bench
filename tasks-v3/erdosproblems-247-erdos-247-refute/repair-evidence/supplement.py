import importlib.util, os, json, shutil, tempfile, hashlib, sys
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
tests=sys.argv[1] if len(sys.argv)>1 else '/tests'
os.environ['FCB_TESTS_DIR']=tests
spec=importlib.util.spec_from_file_location('checker',tests+'/test_target.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
results={}
def passed(name, f):
    f(); results[name]='passed'; print('PASS',name,flush=True)
def rejected(name, f):
    try: f()
    except SystemExit as e:
        assert e.code == 1
        results[name]='rejected as expected'; print('PASS reject',name,flush=True)
    else: raise AssertionError('unexpected acceptance: '+name)
text=m.target_text()
passed('unchanged frozen prefix/header', lambda:m.check_frozen_prefix_and_header(text))
rejected('modified frozen prefix', lambda:m.check_frozen_prefix_and_header('-- changed\n'+text))
rejected('original sorry source restriction',lambda:m.check_banned_patterns(m.check_frozen_prefix_and_header(text)))
passed('frozen files',m.check_frozen_files_unchanged)
passed('load official precompiled package',m.load_trusted_spec)
with m.make_fresh_golden_project() as tmp:
    project=Path(tmp)
    passed('trusted type independent import and axiom audit',lambda:m.check_trusted_type(project))
    passed('ubuntu candidate compilation with isolated sorry fixture',lambda:m.check_build(project))
    passed('complete type equality',lambda:m.check_golden_theorem_import(project))
    rejected('target axiom audit catches sorryAx',lambda:m.check_axioms(project))
    passed('sorry canary',lambda:m.check_sorry_canary(project))
    # A normal helper definition/import is not globally forbidden.
    sub=project/'FormalConjecturesBench/Submission.lean'
    sub.write_text('import FormalConjectures.Util.ProblemImports\nimport Mathlib.Data.Nat.Basic\nnamespace Erdos247\ndef Transcendental (_ : Type) (_ : ℝ) : Prop := True\nend Erdos247\n')
    passed('semantic shadow candidate compiled',lambda:m.check_build(project))
    rejected('unchanged header name-shadow full-type mismatch',lambda:m.check_golden_theorem_import(project))
    # Candidate names/caches and inherited Lean environment cannot replace Spec.
    (project/'FCBTrustedSpec.lean').write_text('def fake : True := True.intro\n')
    (project/'FCBTrustedSpec.olean').write_bytes(b'FAKE')
    cache=project/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'FAKE CACHE')
    os.environ['LEAN_PATH']=str(cache)
    r=m.run_lean(project,['--deps',str(project/m.TARGET_REL)])
    assert r.returncode==0, r.stdout
    assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in r.stdout, r.stdout
    assert str(cache) not in r.stdout, r.stdout
    passed('candidate same-name module/cache cannot replace fixed Spec',lambda:m.check_trusted_type(project))
    assert not (project/'FCBTrustedSpec.ilean').exists()
# Source outside editable tree is rejected in an isolated candidate checkout.
with tempfile.TemporaryDirectory(prefix='247refute-source-') as tmp:
    fixture=Path(tmp); shutil.copytree('/app/FormalConjecturesBench',fixture/'FormalConjecturesBench')
    (fixture/'Outside.lean').write_text('def outside := 1\n')
    old=m.TASK_DIR; m.TASK_DIR=fixture
    rejected('out-of-bounds source',m.check_extra_lean_files_confined)
    m.TASK_DIR=old
# Fail closed, without runtime regeneration, using copies only.
original=m.SPEC_DIR
for kind in ('missing','corrupt'):
    with tempfile.TemporaryDirectory(prefix='247refute-package-') as tmp:
        copy=Path(tmp)/'trusted_spec'; shutil.copytree(original,copy); m.SPEC_DIR=copy
        artifact=copy/'FCBTrustedSpec.olean'
        if kind=='missing': artifact.unlink()
        else: artifact.write_bytes(artifact.read_bytes()+b'bad')
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in copy.iterdir() if p.is_file()}
        rejected(kind+' precompiled artifact',m.load_trusted_spec)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in copy.iterdir() if p.is_file()}
        assert before==after, 'runtime regenerated package'
        m.SPEC_DIR=original
Path('/tmp/247refute-supplement-results-'+str(os.getuid())+'.json').write_text(json.dumps(results,indent=2)+'\n')
print('ALL SUPPLEMENTARY CHECKS PASSED',flush=True)
