import importlib.util, os, shutil, tempfile, json, hashlib, sys
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
base=sys.argv[1] if len(sys.argv)>1 else '/tests'
os.environ['FCB_TESTS_DIR']=base
spec=importlib.util.spec_from_file_location('checker',str(Path(base)/'test_target.py'))
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

def rejected(label, f):
    try: f()
    except SystemExit as e:
        assert e.code == 1
        print('PASS expected rejection:',label,flush=True)
    else: raise AssertionError('Accepted '+label)

print('Supplement uid',os.getuid(),flush=True)
c.load_trusted_spec()
original=c.target_text()
c.check_frozen_prefix_and_header(original)
rejected('frozen prefix',lambda:c.check_frozen_prefix_and_header(original.replace('open Filter','open Set')))
rejected('header',lambda:c.check_frozen_prefix_and_header(original.replace('¬ (','(True ∧ ¬ (',1)))
c.check_editable_tree_shape(); c.check_extra_lean_files_confined(); c.check_frozen_files_unchanged()
rejected('original sorry source',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(original)))
with tempfile.TemporaryDirectory(prefix='264ii-fixture-') as td:
    fixture=Path(td); shutil.copytree(c.TASK_DIR,fixture,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.lake'))
    old=c.TASK_DIR; c.TASK_DIR=fixture
    (fixture/'Outside.lean').write_text('theorem outsider : True := by trivial\n')
    rejected('outside source',c.check_extra_lean_files_confined)
    (fixture/'Outside.lean').unlink(); c.TASK_DIR=old

with c.make_fresh_golden_project() as td:
    p=Path(td)
    c.check_trusted_type(p)
    # Fixed artifact wins over candidate same-name module/cache and hostile env.
    (p/'FCBTrustedSpec.lean').write_text('def FCBTrustedSpec.ExpectedType := True\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'not a trusted module')
    os.environ['LEAN_PATH']=str(p)
    os.environ['LEAN_SYSROOT']=str(p)
    deps=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
    assert deps.returncode==0, deps.stdout
    assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout,deps.stdout
    assert str(p/'FCBTrustedSpec.olean') not in deps.stdout,deps.stdout
    print('PASS fixed Spec resolution over candidate and env',flush=True)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    rejected('sorryAx target audit',lambda:c.check_axioms(p))
    c.check_sorry_canary(p); print('PASS sorry canary',flush=True)
    # Source is legal. The public frozen text remains byte-for-byte unchanged.
    helper=p/'FormalConjecturesBench/Submission.lean'
    helper.write_text('import FormalConjectures.Util.ProblemImports\nnamespace Erdos264.Nat\ndef factorial (_ : ℕ) : ℕ := 0\nend Erdos264.Nat\n')
    c.check_banned_patterns(helper.read_text())
    assert c.check_frozen_prefix_and_header(original)
    c.check_build(p)
    rejected('factorial name shadow complete type',lambda:c.check_golden_theorem_import(p))

real=c.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='264ii-bad-spec-') as td:
    bad=Path(td); shutil.copytree(real,bad,dirs_exist_ok=True)
    c.SPEC_DIR=bad
    artifact=bad/'FCBTrustedSpec.olean'; data=artifact.read_bytes(); artifact.unlink()
    rejected('missing precompiled Spec',c.load_trusted_spec)
    assert not artifact.exists()
    artifact.write_bytes(data+b'corrupt')
    rejected('corrupt precompiled Spec',c.load_trusted_spec)
    artifact.write_bytes(data)
    (bad/'manifest.json').write_text('{}')
    rejected('corrupt manifest',c.load_trusted_spec)
c.SPEC_DIR=real
c.load_trusted_spec()
print('ALL SUPPLEMENTAL PATHS PASS',flush=True)
