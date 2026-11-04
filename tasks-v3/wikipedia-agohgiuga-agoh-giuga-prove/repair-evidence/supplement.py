import os, sys, json, shutil, tempfile, importlib.util
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
tests_dir=sys.argv[1] if len(sys.argv)>1 else '/tests'
os.environ['FCB_TESTS_DIR']=tests_dir
os.environ['LEAN_PATH']='/tmp/agohgiuga-prove-candidate-cache'
os.environ['LEAN_SYSROOT']='/tmp/agohgiuga-prove-candidate-cache'
spec=importlib.util.spec_from_file_location('checker',str(Path(tests_dir)/'test_target.py'))
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
results=[]
def ok(name, fn):
    print('\nSTAGE',name,flush=True)
    fn(); results.append({'stage':name,'result':'passed'})
def rejected(name, fn):
    print('\nNEGATIVE',name,flush=True)
    try: fn()
    except SystemExit as e:
        assert e.code==1
        results.append({'stage':name,'result':'rejected'}); return
    raise AssertionError('Negative unexpectedly accepted: '+name)
ok('fixed package validation ignoring candidate env',c.load_trusted_spec)
with c.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    ok('independent expected type and prefix transitive axiom audit',lambda:c.check_trusted_type(p))
    ok('original placeholder isolated fixture compiles as ubuntu',lambda:c.check_build(p))
    ok('complete original theorem type comparison',lambda:c.check_golden_theorem_import(p))
    rejected('placeholder target sorryAx audit',lambda:c.check_axioms(p))
    ok('sorry canary',lambda:c.check_sorry_canary(p))
    (p/'FCBTrustedSpec.olean').write_text('not a Lean artifact')
    cache=p/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_text('candidate cache shadow')
    os.environ['LEAN_PATH']=str(cache)
    deps=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
    print(deps.stdout,flush=True); assert deps.returncode==0
    assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout
    assert str(p/'FCBTrustedSpec.olean') not in deps.stdout
    ok('candidate same-name module/cache cannot replace Spec',lambda:c.check_golden_theorem_import(p))

with tempfile.TemporaryDirectory(prefix='agohgiuga-prove-negative-') as tmp:
    root=Path(tmp)
    shutil.copytree(c.GOLDEN_ENV_DIR,root,dirs_exist_ok=True)
    c.TASK_DIR=root; c.TARGET=root/c.TARGET_REL
    golden=c.TARGET.read_text()
    rejected('frozen prefix modification',lambda:c.check_frozen_prefix_and_header(golden.replace('open scoped Nat','open scoped Nat\n-- changed',1)))
    extra=root/'OutOfBounds.lean';extra.write_text('theorem harmless : True := by trivial\n')
    rejected('out of bounds source',c.check_extra_lean_files_confined); extra.unlink()
    helper=root/'FormalConjecturesBench/Submission.lean'
    helper.write_text('''import FormalConjectures.Util.ProblemImports
namespace AgohGiuga
def bernoulli' (_ : ℕ) : ℚ := 0
end AgohGiuga
''')
    ok('prefix semantic shadow frozen/header unchanged',lambda:c.check_frozen_prefix_and_header(c.target_text()))
    ok('prefix semantic shadow allowed helper source',lambda:c.check_banned_patterns(helper.read_text()))
    with c.make_fresh_golden_project() as fresh:
        p=Path(fresh)
        ok('prefix semantic shadow compiles as ubuntu',lambda:c.check_build(p))
        ok('shared trusted prefix prevents helper bernoulli reinterpretation',lambda:c.check_golden_theorem_import(p))

    # Actual frozen-text semantic negative via an ordinary external precompiled
    # dependency. Its scoped name notation changes the candidate type to True;
    # the already elaborated Spec must remain the original Bernoulli property.
    # This is a test-only module, not a trusted dependency modification or a
    # runtime Spec generator. Keep the original rules for normal imports.
    with tempfile.TemporaryDirectory(prefix='agohgiuga-name-fixture-') as external:
        module_dir=Path(external)
        os.chmod(module_dir,0o777)  # allow the ubuntu compiler to emit fixture .olean
        module=module_dir/'NameFixture.lean'
        module.write_text('import FormalConjectures.Util.ProblemImports\nscoped[Nat] notation "AgohGiugaCongr" => True\n')
        compiled=c.run_lean(module_dir,['-o',str(module.with_suffix('.olean')),str(module)])
        assert compiled.returncode==0,compiled.stdout
        c.TARGET.write_text(golden.replace('  sorry','  trivial'))
        helper.write_text('import «'+str(module.with_suffix(''))+'»\n')
        ok('scoped-name hijack unchanged complete frozen text/header',lambda:c.check_frozen_prefix_and_header(c.target_text()))
        ok('scoped-name hijack passes original source restrictions',c.check_no_banned_patterns_in_editable_sources)
        ok('scoped-name hijack passes tree shape',c.check_editable_tree_shape)
        ok('scoped-name hijack passes source confinement',c.check_extra_lean_files_confined)
        ok('scoped-name hijack passes frozen files',c.check_frozen_files_unchanged)
        with c.make_fresh_golden_project() as fresh:
            p=Path(fresh)
            ok('scoped-name hijack actually compiles as ubuntu',lambda:c.check_build(p))
            ok('scoped-name hijack target has no extra axioms',lambda:c.check_axioms(p))
            probe=p/'MismatchProbe.lean'
            probe.write_text('import FCBTrustedSpec\nimport FormalConjecturesBench.Target\nexample : _root_.FCBTrustedSpec.ExpectedType := @_root_.AgohGiuga.agoh_giuga\n')
            mismatch=c.run_lean(p,[str(probe)])
            assert mismatch.returncode != 0 and 'Type mismatch' in mismatch.stdout and 'True' in mismatch.stdout, mismatch.stdout
            probe.unlink()
            rejected('scoped-name hijack complete type mismatch',lambda:c.check_golden_theorem_import(p))

trusted=c.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='agohgiuga-prove-corrupt-spec-') as tmp:
    d=Path(tmp)/'trusted_spec';shutil.copytree(trusted,d)
    c.SPEC_DIR=d
    artifact=d/'FCBTrustedSpec.olean';original=artifact.read_bytes();artifact.unlink()
    rejected('missing precompiled artifact',c.load_trusted_spec)
    assert not artifact.exists(), 'runtime generation happened'
    artifact.write_bytes(original+b'corrupt')
    rejected('corrupt precompiled artifact',c.load_trusted_spec)
    c.SPEC_DIR=trusted
print('\nRESULTS_JSON='+json.dumps(results,ensure_ascii=False),flush=True)
