from pathlib import Path
import importlib.util, tempfile, shutil, os, pwd
s=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)

def rejected(label, fn):
    try: fn()
    except SystemExit as ex:
        assert ex.code==1
        print('PASS rejected: '+label, flush=True)
    else: raise AssertionError('accepted '+label)

def own(path):
    a=pwd.getpwnam('ubuntu')
    for p in (path,*path.rglob('*')): os.chown(p,a.pw_uid,a.pw_gid)

c.load_trusted_spec()
text=c.target_text()
c.check_frozen_prefix_and_header(text)
rejected('frozen prefix',lambda:c.check_frozen_prefix_and_header(text.replace('namespace Erdos17','namespace Erdos17\n-- tamper',1)))
rejected('changed header',lambda:c.check_frozen_prefix_and_header(text.replace('theorem erdos_17 :','theorem erdos_18 :',1)))
rejected('missing proof assignment',lambda:c.check_frozen_prefix_and_header(text.replace(':= by','by',1)))
rejected('source sorry ban',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(text)))
c.check_editable_tree_shape();c.check_extra_lean_files_confined();c.check_frozen_files_unchanged()
with tempfile.TemporaryDirectory(prefix='erdos17-confined-') as d:
    original=c.TASK_DIR;c.TASK_DIR=Path(d)
    (Path(d)/'Outside.lean').write_text('example : True := True.intro')
    rejected('source outside editable subtree',c.check_extra_lean_files_confined)
    c.TASK_DIR=original
with c.make_fresh_golden_project() as d:
    p=Path(d)
    c.check_trusted_type(p)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    rejected('original placeholder target sorryAx audit',lambda:c.check_axioms(p))
    c.check_sorry_canary(p);print('PASS sorry canary',flush=True)
    with tempfile.TemporaryDirectory(prefix='erdos17-impostor-') as imp:
        q=Path(imp);q.chmod(0o755)
        (q/'FCBTrustedSpec.lean').write_text('namespace FCBTrustedSpec\ndef ExpectedType : Prop := True\nend FCBTrustedSpec\n')
        own(q)
        r=c.run_lean(q,['-o',str(q/'FCBTrustedSpec.olean'),str(q/'FCBTrustedSpec.lean')]);assert r.returncode==0,r.stdout
        for dest in [p,p/'.lake/build/lib/lean']:
            dest.mkdir(parents=True,exist_ok=True)
            shutil.copy2(q/'FCBTrustedSpec.olean',dest/'FCBTrustedSpec.olean')
        (p/'FCBTrustedSpec.lean').write_text((q/'FCBTrustedSpec.lean').read_text())
        old=os.environ.get('LEAN_PATH');os.environ['LEAN_PATH']=str(q)
        output=c.lean_output(p,'import FCBTrustedSpec\n#print FCBTrustedSpec.ExpectedType\n')
        assert 'Erdos17.IsClusterPrime' in output,output
        deps=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
        assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout,deps.stdout
        assert str(q/'FCBTrustedSpec.olean') not in deps.stdout
        print(deps.stdout,flush=True)
        c.check_golden_theorem_import(p)
        if old is None: os.environ.pop('LEAN_PATH')
        else: os.environ['LEAN_PATH']=old
        print('PASS candidate namesake source/cache/ambient LEAN_PATH cannot replace Spec',flush=True)

# Adversarial existing-syntax elaboration redirects the IsClusterPrime name to
# Hacker.IsClusterPrime, leaving the ENTIRE original Target prefix/header intact.
# This is only an isolated negative test, not an answer or allowed proof technique.
with tempfile.TemporaryDirectory(prefix='erdos17-name-shadow-') as d:
    task=Path(d);shutil.copytree(c.GOLDEN_ENV_DIR,task,dirs_exist_ok=True)
    target=task/c.TARGET_REL
    target.write_text(text.replace('  sorry','  change Set.Infinite (Set.univ : Set ℕ)\n  exact Set.infinite_univ'))
    (task/'FormalConjecturesBench/Submission.lean').write_text(Path('/tmp/erdos17-name-helper4.lean').read_text())
    original=c.TASK_DIR;original_target=c.TARGET
    c.TASK_DIR=task;c.TARGET=target
    proof=c.check_frozen_prefix_and_header(c.target_text());c.check_banned_patterns(proof)
    c.check_editable_tree_shape();c.check_no_banned_patterns_in_editable_sources()
    c.check_extra_lean_files_confined();c.check_frozen_files_unchanged()
    with c.make_fresh_golden_project() as fresh:
        p=Path(fresh)
        c.check_trusted_type(p);c.check_build(p)
        c.check_axioms(p)
        print(c.lean_output(p,'import FormalConjecturesBench.Target\n#print Erdos17.erdos_17\n'),flush=True)
        rejected('name redirection; identical frozen text; compiled altered candidate full type',lambda:c.check_golden_theorem_import(p))
    c.TASK_DIR=original;c.TARGET=original_target

original=c.SPEC_DIR
for label,kind in [('missing Spec artifact','missing'),('corrupt Spec artifact','corrupt')]:
    with tempfile.TemporaryDirectory(prefix='erdos17-bad-spec-') as d:
        q=Path(d);shutil.copytree(original,q,dirs_exist_ok=True);c.SPEC_DIR=q
        artifact=q/'FCBTrustedSpec.olean'
        if kind=='missing':artifact.unlink()
        else:artifact.write_bytes(artifact.read_bytes()+b'corrupt')
        original_run=c.run
        c.run=lambda *a,**kw: (_ for _ in ()).throw(AssertionError('unexpected compiler/generator call'))
        rejected(label,c.load_trusted_spec)
        c.run=original_run
        if kind=='missing':assert not artifact.exists()
c.SPEC_DIR=original
print('ALL SUPPLEMENTAL CHECKS PASSED',flush=True)
