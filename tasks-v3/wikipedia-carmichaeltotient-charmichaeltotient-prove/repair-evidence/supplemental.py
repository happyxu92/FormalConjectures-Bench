import contextlib, importlib.util, io, json, os, shutil, tempfile
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
tests=os.environ.get('CARMICHAEL_COVERAGE_TESTS','/tests')
os.environ['FCB_TESTS_DIR']=tests
spec=importlib.util.spec_from_file_location('actual_checker',str(Path(tests)/'test_target.py'))
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
results=[]
def test(name, action, reject=None):
    out=io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            action()
        except SystemExit as e:
            if reject is None or e.code!=1 or reject not in out.getvalue():
                print(out.getvalue(),file=__import__('sys').__stdout__,flush=True);raise
        else:
            if reject is not None:raise AssertionError('accepted negative '+name)
    print('PASS',name,flush=True)
    print(out.getvalue(),flush=True)
    results.append({'name':name,'expected_rejection':reject,'output':out.getvalue()})

original=c.target_text()
test('fixed Spec load',c.load_trusted_spec)
with c.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    test('trusted Spec import/value/universes/transitive axiom audit',lambda:c.check_trusted_type(p))
    test('ubuntu candidate compile (original placeholder fixture)',lambda:c.check_build(p))
    test('complete theorem type comparison (matching placeholder fixture)',lambda:c.check_golden_theorem_import(p))
    test('target axiom audit rejects placeholder',lambda:c.check_axioms(p),'sorryAx')
    test('sorry canary',lambda:c.check_sorry_canary(p))
    # An invalid same-name compiled cache and source must not shadow the fixed Spec.
    (p/'FCBTrustedSpec.olean').write_bytes(b'invalid candidate replacement')
    (p/'FCBTrustedSpec.lean').write_text('def replacement : Prop := True\n')
    cache=p/'.lake/build/lib/lean';cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'candidate cache')
    os.environ['LEAN_PATH']=str(cache)
    os.environ['FCB_DEPENDENCY_PACKAGES']=str(cache)
    def identity():
        r=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
        assert r.returncode==0,r.stdout
        assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in r.stdout,r.stdout
        assert str(p/'FCBTrustedSpec.olean') not in r.stdout,r.stdout
        c.check_trusted_type(p)
    test('same-name candidate module/cache and environment cannot replace Spec',identity)

saved_task,saved_target=c.TASK_DIR,c.TARGET
with tempfile.TemporaryDirectory(prefix='carmichael_prove_negative_') as d:
    d=Path(d);shutil.copytree(c.GOLDEN_ENV_DIR,d,dirs_exist_ok=True)
    c.TASK_DIR=d;c.TARGET=d/c.TARGET_REL
    test('changed frozen prefix',lambda:c.check_frozen_prefix_and_header('\n'+original),'Code above')
    (d/'Outside.lean').write_text('theorem benign : True := True.intro\n')
    test('out-of-tree source',c.check_extra_lean_files_confined,'outside editable subtree')
    (d/'Outside.lean').unlink()
    # Keep the entire frozen text and theorem header unchanged; only legal
    # instance and proof declarations change the meaning of 0 < n.
    (d/'FormalConjecturesBench/Submission.lean').write_text(
      'import FormalConjectures.Util.ProblemImports\n'
      'instance (priority := 2000) fcbFalseLT : LT Nat := ⟨fun _ _ => False⟩\n')
    c.TARGET.write_text(original.replace('  sorry\n','  intro n h\n  cases h\n'))
    test('semantic fixture frozen/header check',lambda:c.check_frozen_prefix_and_header(c.target_text()))
    test('semantic fixture source restrictions',c.check_no_banned_patterns_in_editable_sources)
    with c.make_fresh_golden_project() as tmp:
        p=Path(tmp)
        test('semantic replacement compiles as ubuntu',lambda:c.check_build(p))
        test('semantic replacement is axiom-clean',lambda:c.check_axioms(p))
        test('complete type rejects altered LT instance',lambda:c.check_golden_theorem_import(p),'Type mismatch')
    test('full actual checker rejects legal-syntax instance attack',c.main,'Type mismatch')
c.TASK_DIR,c.TARGET=saved_task,saved_target
saved_spec=c.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='carmichael_prove_artifact_') as d:
    p=Path(d)/'trusted_spec';shutil.copytree(saved_spec,p)
    c.SPEC_DIR=p
    art=p/'FCBTrustedSpec.olean';original_art=art.read_bytes();art.unlink()
    test('missing precompiled artifact fails without regeneration',c.load_trusted_spec,'Missing trusted Spec artifact')
    assert not art.exists()
    art.write_bytes(original_art+b'corrupt')
    test('artifact hash mismatch fails without regeneration',c.load_trusted_spec,'artifact hash mismatch')
    assert art.read_bytes()==original_art+b'corrupt'
c.SPEC_DIR=saved_spec
Path('/tmp/carmichael-prove-coverage-results-'+('official' if tests=='/tests' else 'local')+'.json').write_text(json.dumps(results,indent=2))
print('ALL',len(results),'SUPPLEMENTAL CHECKS PASSED',flush=True)
