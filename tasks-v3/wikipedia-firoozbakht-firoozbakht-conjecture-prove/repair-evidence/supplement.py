from pathlib import Path
import os, importlib.util, tempfile, shutil, json, hashlib
os.environ['FCB_TASK_DIR']='/app'
os.environ['FCB_TESTS_DIR']='/tests'
spec=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
results=[]
def ok(name):
    print('PASS '+name,flush=True); results.append(name)
def reject(name,fn,expected):
    try: fn()
    except SystemExit as e:
        assert e.code==1
        ok(name+' (rejected: '+expected+')')
    else: raise AssertionError(name+' accepted')

m.load_trusted_spec(); ok('fixed package hash/version/golden validation')
text=m.target_text()
m.check_frozen_prefix_and_header(text); ok('original header/frozen prefix')
reject('frozen edit',lambda:m.check_frozen_prefix_and_header(text.replace('open Real','open Nat')), 'frozen prefix')
prefix,rest=text.split(m.MARKER,1)
reject('header edit',lambda:m.check_frozen_prefix_and_header(prefix+m.MARKER+rest.replace('(n : ℕ)', '(n : ℤ)')), 'header')
reject('missing assignment',lambda:m.check_frozen_prefix_and_header(text.replace(':= by\n  sorry','by\n  sorry')), ':=')
reject('banned placeholder',lambda:m.check_banned_patterns(m.check_frozen_prefix_and_header(text)), 'sorry')
original_task=m.TASK_DIR
with tempfile.TemporaryDirectory(prefix='fcb-firooz-outside-') as t:
    root=Path(t); shutil.copytree(m.GOLDEN_ENV_DIR,root,dirs_exist_ok=True)
    (root/'Outside.lean').write_text('def outside := True\n')
    m.TASK_DIR=root
    reject('out-of-bounds source',m.check_extra_lean_files_confined,'outside editable subtree')
m.TASK_DIR=original_task

with m.make_fresh_golden_project() as t:
    p=Path(t)
    m.check_trusted_type(p); ok('trusted expected value/prefix transitive axiom audit')
    # Same-name candidate source, build cache and ambient LEAN_PATH cannot replace fixed Spec.
    (p/'FCBTrustedSpec.lean').write_text('def FCBTrustedSpec.ExpectedType : Prop := True\n')
    result=m.run_lean(p,['-o',str(p/'FCBTrustedSpec.olean'),str(p/'FCBTrustedSpec.lean')])
    assert result.returncode==0,result.stdout
    cache=p/'.lake/build/lib/lean';cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'not a Lean artifact')
    os.environ['LEAN_PATH']=str(cache)
    dep=m.run_lean(p,['--deps',str(p/m.TARGET_REL)])
    assert dep.returncode==0,dep.stdout
    assert '/tests/trusted_spec/FCBTrustedSpec.olean' in dep.stdout,dep.stdout
    m.check_build(p); ok('ubuntu candidate compilation; same-name module/cache cannot replace Spec')
    m.check_golden_theorem_import(p); ok('complete baseline forall type comparison')
    reject('baseline axiom audit',lambda:m.check_axioms(p),'sorryAx')
    m.check_sorry_canary(p); ok('sorry canary detects sorryAx')

with m.make_fresh_golden_project() as t:
    p=Path(t)
    target=p/m.TARGET_REL
    target.write_text(target.read_text().replace('  sorry','  trivial'))
    helper=p/m.EDITABLE_REL/'Submission.lean'
    helper.write_text('import FormalConjectures.Util.ProblemImports\ninstance (priority := 1000000) : LT ℝ := ⟨fun _ _ => True⟩\n')
    m.check_banned_patterns('by trivial')
    # The original frozen text/header is unchanged in this semantic counterexample.
    m.check_frozen_prefix_and_header(text.replace('  sorry','  trivial'))
    m.check_build(p); ok('semantic LT-instance swap compiles with unchanged frozen text')
    reject('complete type comparison rejects semantic swap',lambda:m.check_golden_theorem_import(p),'type mismatch')
    m.check_axioms(p); ok('semantic negative has no forbidden axioms; rejection is type comparison')

original_spec=m.SPEC_DIR
for kind in ('missing','corrupt','manifest'):
    with tempfile.TemporaryDirectory(prefix='fcb-firooz-artifact-') as t:
        p=Path(t);shutil.copytree(original_spec,p,dirs_exist_ok=True)
        if kind=='missing': (p/'FCBTrustedSpec.olean').unlink()
        elif kind=='corrupt': (p/'FCBTrustedSpec.olean').write_bytes(b'corrupt')
        else: (p/'manifest.json').write_text('{}')
        before={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.is_file()}
        m.SPEC_DIR=p
        reject('artifact '+kind, m.load_trusted_spec, 'trusted hash/artifact validation')
        after={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.is_file()}
        assert before==after,'runtime regenerated artifact'
m.SPEC_DIR=original_spec
m.load_trusted_spec()
print(json.dumps({'passed':results,'count':len(results)},ensure_ascii=False,indent=2))
