from pathlib import Path
import importlib.util, os, tempfile, shutil, hashlib, json
spec = importlib.util.spec_from_file_location('checker', '/tests/test_target.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
def reject(label, f):
    try: f()
    except SystemExit as e:
        assert e.code != 0
        print('EXPECTED REJECTION:', label, flush=True)
    else: raise AssertionError('unexpected acceptance: ' + label)
print('SPEC_DIR:', c.SPEC_DIR, flush=True)
c.load_trusted_spec()
with c.make_fresh_golden_project() as tmp:
    p = Path(tmp)
    c.check_trusted_type(p)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    reject('target sorryAx audit', lambda: c.check_axioms(p))
    c.check_sorry_canary(p)
    print('SORRY CANARY PASSED', flush=True)
    # Candidates and their caches must not replace the trusted module.
    fake = p / 'FCBTrustedSpec.lean'
    fake.write_text('def FCBTrustedSpec.ExpectedType : Prop := True\n')
    cache = p / '.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache / 'FCBTrustedSpec.olean').write_bytes(b'candidate-invalid-olean')
    os.environ['LEAN_PATH'] = str(cache)
    os.environ['LEAN_SYSROOT'] = str(p)
    os.environ['ELAN_TOOLCHAIN'] = 'candidate'
    result = c.run_lean(p, ['--deps', str(p / c.TARGET_REL)])
    assert result.returncode == 0, result.stdout
    assert str(c.SPEC_DIR / 'FCBTrustedSpec.olean') in result.stdout, result.stdout
    assert str(cache / 'FCBTrustedSpec.olean') not in result.stdout
    c.check_trusted_type(p)
    print('CANDIDATE SAME-NAME SOURCE/CACHE/ENV CANNOT SHADOW SPEC', flush=True)
    # Allowed instance changes meaning without touching frozen text/header.
    submission = p / 'FormalConjecturesBench/Submission.lean'
    submission.write_text('import FormalConjectures.Util.ProblemImports\nnamespace Equidistribution\nnoncomputable instance (priority := 2000) : HDiv ℝ ℝ ℝ := ⟨fun _ _ => 0⟩\nend Equidistribution\n')
    import pwd
    account = pwd.getpwnam('ubuntu')
    os.chown(submission, account.pw_uid, account.pw_gid)
    original = c.target_text()
    c.check_frozen_prefix_and_header(original)
    c.check_banned_patterns(submission.read_text())
    c.check_build(p)
    reject('unchanged-header semantic instance substitution at full type comparison', lambda: c.check_golden_theorem_import(p))
    c.check_trusted_type(p)
text = c.target_text()
reject('frozen prefix', lambda: c.check_frozen_prefix_and_header(text.replace('namespace Equidistribution', 'namespace Changed', 1)))
reject('changed header', lambda: c.check_frozen_prefix_and_header(text.replace(c.EXPECTED_HEADER, c.EXPECTED_HEADER + ' → False')))
# A disposable candidate checkout exercises actual confinement checks.
with tempfile.TemporaryDirectory(prefix='three-halves-refute-boundary-') as d:
    p = Path(d); shutil.copytree(c.GOLDEN_ENV_DIR, p, dirs_exist_ok=True)
    old = c.TASK_DIR; c.TASK_DIR = p
    (p / 'Outside.lean').write_text('def outside := 1\n')
    reject('out of subtree Lean source', c.check_extra_lean_files_confined)
    (p / 'Outside.lean').unlink()
    c.check_extra_lean_files_confined()
    c.check_frozen_files_unchanged()
    (p / 'lakefile.toml').write_text('changed')
    reject('frozen project file', c.check_frozen_files_unchanged)
    c.TASK_DIR = old
# Missing/corrupt fixed products fail loading rather than invoking generation.
old = c.SPEC_DIR
for mode in ['missing', 'corrupt']:
    with tempfile.TemporaryDirectory(prefix='three-halves-refute-products-') as d:
        p = Path(d); shutil.copytree(old, p, dirs_exist_ok=True)
        olean = p / 'FCBTrustedSpec.olean'
        if mode == 'missing': olean.unlink()
        else: olean.write_bytes(b'corrupt')
        before = {f.name for f in p.iterdir()}
        c.SPEC_DIR = p
        reject(mode + ' Spec artifact (no runtime generation)', c.load_trusted_spec)
        assert {f.name for f in p.iterdir()} == before
        if mode == 'missing': assert not olean.exists()
        else: assert olean.read_bytes() == b'corrupt'
        c.SPEC_DIR = old
print('ALL SUPPLEMENTAL PATHS PASSED', flush=True)
