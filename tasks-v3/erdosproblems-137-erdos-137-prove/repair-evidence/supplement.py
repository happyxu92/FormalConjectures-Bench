from pathlib import Path
import importlib.util, tempfile, shutil, os, traceback
s=importlib.util.spec_from_file_location('checker','/tests/test_target.py'); c=importlib.util.module_from_spec(s); s.loader.exec_module(c)

def rejected(label, fn):
    try: fn()
    except SystemExit as ex:
        assert ex.code == 1
        print('PASS rejected:', label, flush=True)
    else: raise AssertionError('accepted '+label)

c.load_trusted_spec()
text=c.target_text()
assert c.check_frozen_prefix_and_header(text)
rejected('frozen prefix',lambda:c.check_frozen_prefix_and_header(text.replace('namespace Erdos137','namespace Erdos137\n-- tamper',1)))
rejected('changed header',lambda:c.check_frozen_prefix_and_header(text.replace('∀ k ≥ 3','∀ k ≥ 4',1)))
rejected('missing assignment',lambda:c.check_frozen_prefix_and_header(text.replace(':= by','by',1)))
c.check_editable_tree_shape(); c.check_extra_lean_files_confined(); c.check_frozen_files_unchanged()
with tempfile.TemporaryDirectory(prefix='ep137-confined-') as d:
    original=c.TASK_DIR;c.TASK_DIR=Path(d)
    (Path(d)/'Outside.lean').write_text('example : True := True.intro')
    rejected('out of subtree',c.check_extra_lean_files_confined)
    c.TASK_DIR=original
with c.make_fresh_golden_project() as d:
    p=Path(d)
    c.check_trusted_type(p)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    rejected('target sorryAx audit',lambda:c.check_axioms(p))
    c.check_sorry_canary(p); print('PASS sorry canary',flush=True)
    # A precompiled candidate namesake in source, build cache and ambient paths.
    with tempfile.TemporaryDirectory(prefix='ep137-impostor-') as imp:
        q=Path(imp); q.chmod(0o755)
        (q/'FCBTrustedSpec.lean').write_text('namespace FCBTrustedSpec\ndef ExpectedType : Prop := True\nend FCBTrustedSpec\n')
        os.chmod(q/'FCBTrustedSpec.lean',0o644)
        import pwd
        a=pwd.getpwnam('ubuntu');os.chown(q,a.pw_uid,a.pw_gid)
        r=c.run_lean(q,['-o',str(q/'FCBTrustedSpec.olean'),str(q/'FCBTrustedSpec.lean')]); assert r.returncode==0,r.stdout
        for dest in [p,p/'.lake/build/lib/lean']:
            dest.mkdir(parents=True,exist_ok=True)
            shutil.copy2(q/'FCBTrustedSpec.olean',dest/'FCBTrustedSpec.olean')
        (p/'FCBTrustedSpec.lean').write_text((q/'FCBTrustedSpec.lean').read_text())
        os.environ['LEAN_PATH']=str(q)
        output=c.lean_output(p,'import FCBTrustedSpec\n#print FCBTrustedSpec.ExpectedType\n')
        assert 'Finset.Ioc' in output and '∀ k ≥ 3' in output,output
        deps=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
        assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout,deps.stdout
        c.check_golden_theorem_import(p)
        print('PASS candidate module/cache/ambient LEAN_PATH cannot replace Spec',flush=True)
    # The exact frozen header now resolves Finset.Ioc differently through Submission.
    (p/'FormalConjecturesBench/Submission.lean').write_text('import FormalConjectures.Util.ProblemImports\nnamespace Erdos137\ndef Finset.Ioc (_ _ : ℕ) : _root_.Finset ℕ := ∅\nend Erdos137\n')
    c.check_build(p)
    rejected('semantic shadow with unchanged header',lambda:c.check_golden_theorem_import(p))
    print('PASS shadowed candidate compiled; full type comparison rejected',flush=True)
# Fixed package failure tests never call a compiler or generator.
original=c.SPEC_DIR
for label,kind in [('missing artifact','missing'),('corrupt artifact','corrupt')]:
    with tempfile.TemporaryDirectory(prefix='ep137-bad-spec-') as d:
        q=Path(d);shutil.copytree(original,q,dirs_exist_ok=True);c.SPEC_DIR=q
        artifact=q/'FCBTrustedSpec.olean'
        if kind=='missing': artifact.unlink()
        else: artifact.write_bytes(artifact.read_bytes()+b'corrupt')
        original_run=c.run
        c.run=lambda *a,**kw: (_ for _ in ()).throw(AssertionError('unexpected compiler/generator call'))
        rejected(label,c.load_trusted_spec)
        c.run=original_run
        if kind=='missing': assert not artifact.exists()
c.SPEC_DIR=original
print('ALL SUPPLEMENTAL CHECKS PASSED',flush=True)
