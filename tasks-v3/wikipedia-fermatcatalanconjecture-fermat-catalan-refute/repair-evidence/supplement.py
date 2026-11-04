import importlib.util, os, json, shutil, tempfile, io, contextlib
from pathlib import Path
sp=importlib.util.spec_from_file_location('checker',os.environ.get('FCB_TESTS_DIR','/tests')+'/test_target.py')
m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
results=[]
def ok(name, f):
    f(); results.append({'case':name,'result':'passed'})
def reject(name, f, contains):
    out=io.StringIO()
    try:
        with contextlib.redirect_stderr(out): f()
    except SystemExit as e:
        assert e.code==1
        message=out.getvalue()
        assert contains in message, (name, message)
        print('EXPECTED REJECTION:',name,'\n',message)
        results.append({'case':name,'result':'rejected','actual_message':message})
    else: raise AssertionError('accepted '+name)

m.load_trusted_spec()
with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    ok('independent precompiled Spec and prefix transitive axiom audit',lambda:m.check_trusted_type(p))
    ok('ubuntu build original placeholder fixture',lambda:m.check_build(p))
    ok('full type agrees for original refutation fixture',lambda:m.check_golden_theorem_import(p))
    reject('placeholder target axiom audit',lambda:m.check_axioms(p),'sorryAx')
    ok('sorry canary',lambda:m.check_sorry_canary(p))
    # Normal imports and helper declarations remain usable.
    helper=p/'FormalConjecturesBench/Submission.lean'
    helper.write_text('import Mathlib.Tactic\nlemma ordinary_helper : True := by trivial\n')
    ok('ordinary external import and helper lemma',lambda:m.check_build(p))
    # Ignore candidate same-name module, caches and inherited environment overrides.
    (p/'FCBTrustedSpec.lean').write_text('def counterfeit : Prop := True\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'counterfeit')
    cache=p/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'counterfeit cache')
    original_task=m.TASK_DIR
    m.TASK_DIR=p
    external=p/'ExternalFixture.lean'
    external.write_text('namespace ExternalFixture\ntheorem helper : True := by trivial\nend ExternalFixture\n')
    compiled=m.run_lean(p,['-o',str(cache/'ExternalFixture.olean'),str(external)])
    assert compiled.returncode==0, compiled.stdout
    external.unlink()
    ok('ordinary external precompiled module still importable',lambda:m.lean_output(p,'import ExternalFixture\nexample : True := ExternalFixture.helper\n'))
    old=os.environ.get('LEAN_PATH'); os.environ['LEAN_PATH']=str(cache)
    deps=m.run_lean(p,['--deps',str(p/m.TARGET_REL)])
    assert deps.returncode==0, deps.stdout
    assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout, deps.stdout
    assert str(cache) not in deps.stdout, deps.stdout
    print('FIXED RESOLUTION:',deps.stdout)
    ok('same-name module/cache/env cannot replace Spec',lambda:m.check_golden_theorem_import(p))
    if old is None: os.environ.pop('LEAN_PATH',None)
    else: os.environ['LEAN_PATH']=old
    m.TASK_DIR=original_task

with tempfile.TemporaryDirectory(prefix='fermat-refute-negative-') as tmp:
    candidate=Path(tmp); shutil.copytree(m.TASK_DIR,candidate,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.lake'))
    target=candidate/m.TARGET_REL
    original=target.read_text(); target.write_text(original.replace('  sorry','  intro h\n  exact h'))
    original_task,original_target=m.TASK_DIR,m.TARGET
    m.TASK_DIR,m.TARGET=candidate,target
    try:
        ok('semantic fixture frozen prefix/header unchanged',lambda:m.check_frozen_prefix_and_header(target.read_text()))
        helper=candidate/'FormalConjecturesBench/Submission.lean'
        helper.write_text('namespace Function\nscoped notation "fermatCatalanConjecture" => False\nend Function\n')
        reject('semantic hijack rejected by preserved source ban',m.check_no_banned_patterns_in_editable_sources,'Found banned Lean syntax')
        with m.make_fresh_golden_project() as fresh:
            p=Path(fresh)
            ok('semantic hijack compiles with frozen text unchanged',lambda:m.check_build(p))
            out=m.lean_output(p,'import FormalConjecturesBench.Target\n#check @FermatCatalanConjecture.formal_conjectures_bench_refutation\n')
            print('HIJACK TYPE:',out)
            assert 'False' in out
            reject('full type comparator rejects Not False semantic hijack',lambda:m.check_golden_theorem_import(p),'Type mismatch')
        reject('frozen prefix modification',lambda:m.check_frozen_prefix_and_header('-- altered\n'+original),'Code above the benchmark target marker changed')
        reject('header modification',lambda:m.check_frozen_prefix_and_header(original.replace('¬ (','( ',1)),'Target theorem header changed')
        reject('proof assignment removed',lambda:m.check_frozen_prefix_and_header(original.replace(') := by',') by',1)),'proof assignment')
        (candidate/'Outside.lean').write_text('theorem unrelated : True := by trivial\n')
        reject('out-of-tree source',m.check_extra_lean_files_confined,'outside editable subtree')
        (candidate/'Outside.lean').unlink()
        target.write_text(original)
        helper.write_text('lemma ordinary_helper : True := by trivial\n')
        ok('normal helper allowed by syntax restrictions',lambda:m.check_banned_patterns(helper.read_text()))
    finally: m.TASK_DIR,m.TARGET=original_task,original_target

spec=m.SPEC_DIR
for mode in ['missing','corrupt']:
    with tempfile.TemporaryDirectory(prefix='fermat-refute-spec-negative-') as tmp:
        s=Path(tmp)/'trusted_spec'; shutil.copytree(spec,s)
        artifact=s/'FCBTrustedSpec.olean'
        if mode=='missing': artifact.unlink()
        else: artifact.write_bytes(b'corrupt')
        m.SPEC_DIR=s
        try: reject(mode+' precompiled artifact fails closed',m.load_trusted_spec,'trusted Spec artifact' if mode=='missing' else 'artifact hash mismatch')
        finally: m.SPEC_DIR=spec
        if mode=='missing': assert not artifact.exists()
        else: assert artifact.read_bytes()==b'corrupt'
print(json.dumps(results,indent=2))
print('ALL SUPPLEMENTAL CASES PASSED')
