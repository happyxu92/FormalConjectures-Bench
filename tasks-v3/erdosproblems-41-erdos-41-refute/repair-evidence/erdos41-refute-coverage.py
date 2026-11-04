import os, importlib.util, tempfile, shutil
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
os.environ['FCB_TESTS_DIR']='/tests'
spec=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
def rejects(label, f):
    try: f()
    except SystemExit as e:
        assert e.code==1
        print('EXPECTED REJECT:',label,flush=True)
    else: raise AssertionError('unexpected accept: '+label)
c.check_frozen_prefix_and_header(c.target_text())
rejects('frozen prefix',lambda:c.check_frozen_prefix_and_header('--changed\n'+c.target_text()))
rejects('header mutation',lambda:c.check_frozen_prefix_and_header(c.target_text().replace('¬ (','( ',1)))
rejects('missing assignment',lambda:c.check_frozen_prefix_and_header(c.target_text().replace(') := by',') by')))
rejects('formal sorry source rule',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(c.target_text())))
c.check_editable_tree_shape(); c.check_extra_lean_files_confined(); c.check_frozen_files_unchanged()
with tempfile.TemporaryDirectory(prefix='erdos41-refute-confinement-') as t:
    old=c.TASK_DIR; c.TASK_DIR=Path(t)
    (c.TASK_DIR/'escape.lean').write_text('def escape := True')
    rejects('out of subtree Lean source',c.check_extra_lean_files_confined)
    c.TASK_DIR=old
c.load_trusted_spec()
with c.make_fresh_golden_project() as t:
    p=Path(t)
    c.check_trusted_type(p)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    rejects('target sorryAx audit',lambda:c.check_axioms(p))
    c.check_sorry_canary(p)
    print('PASS sorry canary',flush=True)
    os.environ['LEAN_PATH']='/app/.lake/build/lib/lean'
    os.environ['LEAN_SYSROOT']='/app/forged-toolchain'
    (p/'FCBTrustedSpec.lean').write_text('def forgedSpec : True := True.intro\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'forged candidate cache')
    q=p/'FormalConjectures/Util'; q.mkdir(parents=True)
    (q/'ProblemImports.olean').write_bytes(b'forged dependency cache')
    dep=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
    assert dep.returncode==0,dep.stdout
    assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in dep.stdout,dep.stdout
    assert str(p/'FCBTrustedSpec.olean') not in dep.stdout,dep.stdout
    print('PASS trusted Spec wins candidate module/cache and environment overrides',flush=True)
    c.check_build(p); c.check_golden_theorem_import(p)
    # An allowed ordinary helper def changes only qualified-name resolution.
    helper=p/'FormalConjecturesBench/Submission.lean'
    helper.write_text('import FormalConjectures.Util.ProblemImports\nnamespace Erdos41.Filter\ndef atTop : _root_.Filter ℕ := ⊥\nend Erdos41.Filter\n')
    c.check_banned_patterns(helper.read_text())
    target=p/c.TARGET_REL
    assert c.EXPECTED_HEADER in target.read_text()
    c.check_build(p)
    rejects('complete type mismatch: Erdos41.Filter.atTop shadows Filter.atTop; frozen header unchanged',lambda:c.check_golden_theorem_import(p))
    c.check_sorry_canary(p)
    print('PASS semantic negative compiled; complete type comparison actually rejected',flush=True)
with tempfile.TemporaryDirectory(prefix='erdos41-refute-broken-spec-') as t:
    p=Path(t); shutil.copytree(c.SPEC_DIR,p/'spec')
    old=c.SPEC_DIR; c.SPEC_DIR=p/'spec'
    artifact=c.SPEC_DIR/'FCBTrustedSpec.olean'; original=artifact.read_bytes()
    artifact.unlink()
    rejects('missing precompiled artifact, no runtime fallback',c.load_trusted_spec)
    assert not artifact.exists()
    artifact.write_bytes(original+b'corruption')
    rejects('corrupt precompiled artifact hash',c.load_trusted_spec)
    (c.SPEC_DIR/'manifest.json').write_text('{}')
    rejects('corrupt manifest hash',c.load_trusted_spec)
    c.SPEC_DIR=old
c.load_trusted_spec()
# Independently exercise the local entry's fixed /opt Spec location too.
c.SPEC_DIR=Path('/opt/formal-conjectures-bench-checker/trusted_spec')
c.GOLDEN_ENV_DIR=Path('/opt/formal-conjectures-bench-checker/golden_env')
c.load_trusted_spec()
with c.make_fresh_golden_project() as t:
    p=Path(t); c.check_trusted_type(p); c.check_build(p); c.check_golden_theorem_import(p)
    rejects('local target sorryAx audit',lambda:c.check_axioms(p)); c.check_sorry_canary(p)
print('ALL REQUIRED SUPPLEMENTAL PATHS COVERED',flush=True)
