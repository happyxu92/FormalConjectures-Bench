import importlib.util, os, json, hashlib, shutil, tempfile
from pathlib import Path
sp=importlib.util.spec_from_file_location('checker',os.environ.get('FCB_TESTS_DIR','/tests')+'/test_target.py')
m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
results=[]
def ok(name, f):
    f(); results.append({'case':name,'result':'passed'})
def reject(name, f, contains):
    try: f()
    except SystemExit as e:
        assert e.code==1
        results.append({'case':name,'result':'rejected','expected_stage':contains})
    else: raise AssertionError('accepted '+name)

m.load_trusted_spec()
with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    ok('independent trusted type and prefix transitive axiom audit',lambda:m.check_trusted_type(p))
    ok('ubuntu build original placeholder fixture',lambda:m.check_build(p))
    ok('full type agrees for original fixture',lambda:m.check_golden_theorem_import(p))
    reject('placeholder target axiom audit',lambda:m.check_axioms(p),'sorryAx')
    ok('sorry canary',lambda:m.check_sorry_canary(p))
    # Candidate module/cache and environment variables must not shadow fixed artifact.
    (p/'FCBTrustedSpec.lean').write_text('def counterfeit : Prop := True\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'counterfeit')
    cache=p/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'counterfeit cache')
    old=os.environ.get('LEAN_PATH'); os.environ['LEAN_PATH']=str(cache)
    deps=m.run_lean(p,['--deps',str(p/m.TARGET_REL)])
    assert deps.returncode==0, deps.stdout
    assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout, deps.stdout
    assert str(cache) not in deps.stdout, deps.stdout
    ok('same-name module/cache/env cannot replace Spec',lambda:m.check_golden_theorem_import(p))
    if old is None: os.environ.pop('LEAN_PATH',None)
    else: os.environ['LEAN_PATH']=old

# All frozen text and the target header remain unchanged in this semantic fixture.
# Scoped name/notation hijack intentionally tests the deeper comparator separately
# from the preserved syntax ban, which also rejects this submission.
with tempfile.TemporaryDirectory(prefix='fermatcatalan-negative-') as tmp:
    candidate=Path(tmp); shutil.copytree(m.TASK_DIR,candidate,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.lake'))
    target=candidate/m.TARGET_REL
    original=target.read_text(); target.write_text(original.replace('  sorry','  trivial'))
    original_task,original_target=m.TASK_DIR,m.TARGET
    m.TASK_DIR,m.TARGET=candidate,target
    try:
        ok('semantic fixture frozen prefix/header unchanged',lambda:m.check_frozen_prefix_and_header(target.read_text()))
        helper=candidate/'FormalConjecturesBench/Submission.lean'
        helper.write_text('namespace Function\nscoped notation "fermatCatalanConjecture" => True\nend Function\n')
        reject('semantic hijack also rejected by preserved source ban',m.check_no_banned_patterns_in_editable_sources,'banned syntax')
        with m.make_fresh_golden_project() as fresh:
            p=Path(fresh)
            ok('semantic hijack candidate compiles with unchanged theorem header',lambda:m.check_build(p))
            out=m.lean_output(p,'import FormalConjecturesBench.Target\n#check @FermatCatalanConjecture.fermat_catalan\n')
            print('HIJACK TYPE:',out)
            assert 'True' in out
            reject('full type comparator rejects semantic hijack',lambda:m.check_golden_theorem_import(p),'type mismatch')
        reject('frozen text modification',lambda:m.check_frozen_prefix_and_header('-- altered\n'+original),'prefix hash')
        (candidate/'Outside.lean').write_text('theorem unrelated : True := by trivial\n')
        reject('out-of-tree source',m.check_extra_lean_files_confined,'outside editable subtree')
    finally: m.TASK_DIR,m.TARGET=original_task,original_target

spec=m.SPEC_DIR
for mode in ['missing','corrupt']:
    with tempfile.TemporaryDirectory(prefix='fermatcatalan-spec-negative-') as tmp:
        s=Path(tmp)/'trusted_spec'; shutil.copytree(spec,s)
        artifact=s/'FCBTrustedSpec.olean'
        if mode=='missing': artifact.unlink()
        else: artifact.write_bytes(b'corrupt')
        m.SPEC_DIR=s
        try: reject(mode+' precompiled artifact: fail closed without regeneration',m.load_trusted_spec,'artifact validation')
        finally: m.SPEC_DIR=spec
        if mode=='missing': assert not artifact.exists()
        else: assert artifact.read_bytes()==b'corrupt'
print(json.dumps(results,indent=2))
print('ALL SUPPLEMENTAL CASES PASSED')
