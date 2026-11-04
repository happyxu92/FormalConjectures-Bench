from pathlib import Path
import importlib.util, os, tempfile, shutil, hashlib, json
spec=importlib.util.spec_from_file_location('checker',str(Path(os.environ.get('FCB_TESTS_DIR','/tests'))/'test_target.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def reject(label, f, contains):
    try: f()
    except SystemExit as e:
        assert e.code==1
        print('PASS rejection:',label,flush=True)
    else: raise AssertionError('not rejected: '+label)

print('TESTS_DIR',m.TESTS_DIR,'SPEC_DIR',m.SPEC_DIR,flush=True)
m.load_trusted_spec()
original=m.target_text()
m.check_frozen_prefix_and_header(original)
reject('original sorry syntax',lambda:m.check_banned_patterns(m.check_frozen_prefix_and_header(original)), 'Banned')
reject('frozen text',lambda:m.check_frozen_prefix_and_header('-- changed\n'+original),'above')
reject('changed header',lambda:m.check_frozen_prefix_and_header(original.replace('¬ (','True ∧ (',1)),'header')

with m.make_fresh_golden_project() as d:
    p=Path(d)
    m.check_trusted_type(p)
    m.check_build(p)
    m.check_golden_theorem_import(p)
    reject('target axiom sorryAx',lambda:m.check_axioms(p),'axioms')
    m.check_sorry_canary(p)
    print('PASS sorry canary',flush=True)
    # Same-name source and candidate cache cannot substitute the precompiled Spec.
    (p/'FCBTrustedSpec.lean').write_text('def FCBTrustedSpec.ExpectedType : Prop := True\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'invalid candidate module')
    (p/'.lake/build/lib/lean').mkdir(parents=True)
    (p/'.lake/build/lib/lean/FCBTrustedSpec.olean').write_bytes(b'invalid candidate cache')
    os.environ['LEAN_PATH']=str(p)
    m.check_trusted_type(p)
    m.check_golden_theorem_import(p)
    print('PASS candidate same-name source/cache and environment cannot replace trusted module',flush=True)

with tempfile.TemporaryDirectory(prefix='green26-refute-invalid-spec-') as d:
    q=Path(d)/'trusted_spec';shutil.copytree(m.SPEC_DIR,q)
    previous=m.SPEC_DIR;m.SPEC_DIR=q
    artifact=q/'FCBTrustedSpec.olean';saved=artifact.read_bytes();artifact.unlink()
    reject('missing artifact (no regeneration)',m.load_trusted_spec,'missing')
    assert not artifact.exists()
    artifact.write_bytes(saved+b'corrupt')
    reject('corrupt artifact (no regeneration)',m.load_trusted_spec,'hash')
    assert artifact.read_bytes()==saved+b'corrupt'
    m.SPEC_DIR=previous
m.load_trusted_spec()

# All source mutations below exist only in an isolated fixture, never /app or golden.
with tempfile.TemporaryDirectory(prefix='green26-refute-candidate-') as d:
    fixture=Path(d);shutil.copytree('/tests/golden_env',fixture,dirs_exist_ok=True)
    previous_dir,previous_target=m.TASK_DIR,m.TARGET
    m.TASK_DIR=fixture;m.TARGET=fixture/m.TARGET_REL
    try:
        (fixture/'Outside.lean').write_text('theorem harmless : True := trivial\n')
        reject('out-of-subtree Lean source',m.check_extra_lean_files_confined,'outside')
        (fixture/'Outside.lean').unlink()
        submission=fixture/'FormalConjecturesBench/Submission.lean'
        submission.write_text('import FormalConjectures.Util.ProblemImports\nnamespace Green26\nabbrev Fin (_ : ℕ) := Empty\nend Green26\n')
        m.check_frozen_prefix_and_header(m.target_text())
        m.check_banned_patterns(submission.read_text())
        # The isolated placeholder target intentionally bypasses only source prechecks
        # by calling the production downstream functions directly; axiom rejection
        # above demonstrates it cannot pass the official verifier.
        with m.make_fresh_golden_project() as p:
            p=Path(p)
            m.check_build(p)
            reject('unchanged frozen header but shadowed Fin changes complete type',lambda:m.check_golden_theorem_import(p),'type')
        print('PASS semantic shadowing reached and failed complete type comparison',flush=True)
    finally:
        m.TASK_DIR,m.TARGET=previous_dir,previous_target
print('ALL SUPPLEMENTAL PATHS PASSED',flush=True)
