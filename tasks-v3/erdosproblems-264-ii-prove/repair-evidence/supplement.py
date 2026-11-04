from pathlib import Path
import importlib.util, os, shutil, tempfile, hashlib, json


def load(path, name):
    os.environ['FCB_TASK_DIR']='/app'
    os.environ['FCB_TESTS_DIR']=str(path.parent)
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def rejected(label,fn):
    try: fn()
    except SystemExit as e:
        assert e.code == 1
        print('EXPECTED REJECTION:',label,flush=True)
    else: raise AssertionError('Accepted '+label)

for name,path in [('official',Path('/tests/test_target.py')),('local',Path('/opt/formal-conjectures-bench-checker/test_target.py'))]:
    c=load(path,name)
    print('ENTRY PACKAGE',name,c.SPEC_DIR,flush=True)
    c.check_frozen_files_unchanged()
    c.check_editable_tree_shape(); c.check_extra_lean_files_confined()
    text=c.target_text()
    c.check_frozen_prefix_and_header(text)
    rejected('original sorry source gate',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(text)))
    rejected('frozen change',lambda:c.check_frozen_prefix_and_header(text.replace('namespace Erdos264','namespace Broken',1)))
    rejected('header change',lambda:c.check_frozen_prefix_and_header(text.replace(c.EXPECTED_HEADER,c.EXPECTED_HEADER+'X',1)))
    with tempfile.TemporaryDirectory(prefix='264ii-outside-') as f:
        fake=Path(f); shutil.copytree('/app',fake,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.lake'))
        (fake/'Outside.lean').write_text('def outside := 1\n')
        old=c.TASK_DIR;c.TASK_DIR=fake
        rejected('outside source',c.check_extra_lean_files_confined)
        c.TASK_DIR=old
    c.load_trusted_spec()
    with c.make_fresh_golden_project() as f:
        p=Path(f)
        c.check_trusted_type(p)
        c.check_build(p)
        c.check_golden_theorem_import(p)
        rejected('target sorryAx audit',lambda:c.check_axioms(p))
        c.check_sorry_canary(p); print('CANARY PASSED',flush=True)
        # Candidate-controlled same-name root module and cache must not replace Spec.
        fake=p/'FCBTrustedSpec.lean'
        fake.write_text('def FCBTrustedSpec.ExpectedType : Prop := True\n')
        res=c.run_lean(p,['-o',str(fake.with_suffix('.olean')),str(fake)])
        assert res.returncode==0,res.stdout
        cache=p/'.lake/build/lib/lean';cache.mkdir(parents=True)
        shutil.copy2(fake.with_suffix('.olean'),cache/'FCBTrustedSpec.olean')
        os.environ['LEAN_PATH']=str(cache)
        os.environ['LEAN_SYSROOT']=str(p)
        os.environ['ELAN_TOOLCHAIN']='candidate-toolchain'
        res=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
        print('fixed Spec deps:',res.stdout,flush=True)
        assert res.returncode==0 and str(c.SPEC_DIR/'FCBTrustedSpec.olean') in res.stdout
        c.check_golden_theorem_import(p)
        print('SAME-NAME MODULE/CACHE/ENV SHADOW REJECTED',flush=True)
        # Keep ordinary external imports usable after fixed trusted paths.
        import pwd
        external=p/'external'; external.mkdir()
        os.chown(external,pwd.getpwnam('ubuntu').pw_uid,pwd.getpwnam('ubuntu').pw_gid)
        ext=external/'ExternalAllowed.lean'
        ext.write_text('theorem external_allowed : True := True.intro\n')
        result=c.run_lean(p,['-o',str(ext.with_suffix('.olean')),str(ext)])
        assert result.returncode==0,result.stdout
        os.environ['LEAN_PATH']=str(external)
        c.lean_output(p,'import ExternalAllowed\nexample : True := external_allowed\n')
        print('NORMAL EXTERNAL PRECOMPILED IMPORT PASSED',flush=True)
        # Reach complete-type comparison with unchanged public header/prefix,
        # but with a helper-provided name changing Nat.factorial's meaning.
        helper=p/'FormalConjecturesBench/Submission.lean'
        helper.write_text('import FormalConjectures.Util.ProblemImports\nnamespace Erdos264.Nat\ndef factorial (_ : ℕ) : ℕ := 1\nend Erdos264.Nat\n')
        c.check_banned_patterns(helper.read_text())
        assert c.check_frozen_prefix_and_header(text)
        c.check_build(p)
        print(c.lean_output(p,'import FormalConjecturesBench.Target\nset_option pp.fullNames true in\n#check @Erdos264.erdos_264.parts.ii\n'),flush=True)
        rejected('same frozen header, helper name changes complete type',lambda:c.check_golden_theorem_import(p))
    original=c.SPEC_DIR
    for defect in ['missing','corrupt']:
        with tempfile.TemporaryDirectory(prefix='264ii-spec-negative-') as f:
            pkg=Path(f)/'spec';shutil.copytree(original,pkg)
            artifact=pkg/'FCBTrustedSpec.olean'
            if defect=='missing': artifact.unlink()
            else: artifact.write_bytes(artifact.read_bytes()+b'corrupt')
            c.SPEC_DIR=pkg
            rejected(defect+' precompiled Spec (no regenerate)',c.load_trusted_spec)
            assert (not artifact.exists()) if defect=='missing' else artifact.read_bytes().endswith(b'corrupt')
            c.SPEC_DIR=original
    print('ALL PATHS PASSED:',name,flush=True)
print('SUPPLEMENT COMPLETE',flush=True)
