import os, sys, json, hashlib, shutil, tempfile, importlib.util
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
tests_dir=sys.argv[1] if len(sys.argv)>1 else '/tests'
os.environ['FCB_TESTS_DIR']=tests_dir
os.environ['LEAN_PATH']='/tmp/erdos41-candidate-cache'
os.environ['LEAN_SYSROOT']='/tmp/erdos41-candidate-cache'
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
    (p/'FCBTrustedSpec.olean').unlink()

with tempfile.TemporaryDirectory(prefix='erdos41-negative-') as tmp:
    root=Path(tmp)
    shutil.copytree(c.GOLDEN_ENV_DIR,root,dirs_exist_ok=True)
    c.TASK_DIR=root; c.TARGET=root/c.TARGET_REL
    golden=c.TARGET.read_text()
    rejected('frozen prefix modification',lambda:c.check_frozen_prefix_and_header(golden.replace('open Filter Set','open Filter Set\n-- modified',1)))
    extra=root/'OutOfBounds.lean';extra.write_text('theorem harmless : True := by trivial\n')
    rejected('out of bounds source',c.check_extra_lean_files_confined); extra.unlink()
    helper=root/'FormalConjecturesBench/Submission.lean'
    helper.write_text('''import FormalConjectures.Util.ProblemImports
namespace Erdos41.Filter
def atTop : Unit := ()
end Erdos41.Filter
def Unit.liminf (_ : Unit) (_ : ℕ → ℝ) : ℝ := 0
''')
    # Identical frozen text and theorem header, no proof placeholders or banned syntax.
    c.TARGET.write_text(golden.replace('  sorry','  rfl'))
    ok('semantic shadow frozen/header unchanged',lambda:c.check_frozen_prefix_and_header(c.target_text()))
    ok('semantic shadow allowed source syntax',c.check_no_banned_patterns_in_editable_sources)
    ok('semantic shadow tree shape',c.check_editable_tree_shape)
    ok('semantic shadow source confinement',c.check_extra_lean_files_confined)
    ok('semantic shadow frozen files',c.check_frozen_files_unchanged)
    with c.make_fresh_golden_project() as fresh:
        p=Path(fresh)
        ok('semantic shadow candidate actually compiles as ubuntu',lambda:c.check_build(p))
        ok('semantic shadow has only allowed axioms',lambda:c.check_axioms(p))
        rejected('semantic shadow complete type mismatch',lambda:c.check_golden_theorem_import(p))

trusted=c.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='erdos41-corrupt-spec-') as tmp:
    d=Path(tmp)/'trusted_spec';shutil.copytree(trusted,d)
    c.SPEC_DIR=d
    artifact=d/'FCBTrustedSpec.olean';original=artifact.read_bytes();artifact.unlink()
    rejected('missing precompiled artifact',c.load_trusted_spec)
    assert not artifact.exists(), 'runtime generation happened'
    artifact.write_bytes(original+b'corrupt')
    rejected('corrupt precompiled artifact',c.load_trusted_spec)
    c.SPEC_DIR=trusted
print('\nRESULTS_JSON='+json.dumps(results,ensure_ascii=False),flush=True)
