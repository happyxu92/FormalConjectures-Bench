import importlib.util, os, sys, shutil, tempfile, contextlib, io
from pathlib import Path
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('checker', sys.argv[1])
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

def rejects(label, fn, contains):
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        try:
            fn()
        except SystemExit as exc:
            assert exc.code == 1
        else:
            raise AssertionError('Unexpected acceptance: ' + label)
    assert contains in buf.getvalue(), buf.getvalue()
    print('PASS expected rejection:', label, '\n' + buf.getvalue(), flush=True)

assert c.SPEC_DIR == c.TESTS_DIR / 'trusted_spec'
print('Checker:', spec.origin, 'Spec:', c.SPEC_DIR, 'uid:', os.getuid(), flush=True)
assert c.TASK_DIR == Path('/app')
text = c.target_text()
c.check_frozen_prefix_and_header(text)
c.check_editable_tree_shape(); c.check_extra_lean_files_confined(); c.check_frozen_files_unchanged()
rejects('frozen prefix', lambda: c.check_frozen_prefix_and_header(text.replace('open Filter', 'open Filter\n-- changed', 1)), 'Code above')
rejects('header', lambda: c.check_frozen_prefix_and_header(text.replace('theorem formal_conjectures_bench_refutation :', 'theorem wrong_name :', 1)), 'header changed')
rejects('assignment', lambda: c.check_frozen_prefix_and_header(text.replace(') := by\n  sorry', ') by\n  sorry', 1)), 'proof assignment')
rejects('source sorry', lambda: c.check_banned_patterns('by\n sorry'), 'Banned Lean feature')
with tempfile.TemporaryDirectory(prefix='green2refute-confined-') as td:
    old = c.TASK_DIR
    c.TASK_DIR = Path(td)
    shutil.copytree(c.GOLDEN_ENV_DIR, td, dirs_exist_ok=True)
    (Path(td) / 'Outside.lean').write_text('def outside := 1\n')
    rejects('out-of-tree source', c.check_extra_lean_files_confined, 'outside editable subtree')
    c.TASK_DIR = old

c.load_trusted_spec()
with c.make_fresh_golden_project() as td:
    p = Path(td)
    c.check_trusted_type(p)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    rejects('target sorryAx', lambda: c.check_axioms(p), 'sorryAx')
    c.check_sorry_canary(p)
    print('PASS sorry canary', flush=True)
    (p/'FCBTrustedSpec.lean').write_text('THIS IS NOT VALID LEAN\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'candidate module poison')
    cache = p/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'candidate cached module poison')
    # Also try shadowing a trusted dependency at the candidate root.
    dep = p/'FormalConjectures/Util/ProblemImports.olean'; dep.parent.mkdir(parents=True)
    dep.write_bytes(b'candidate dependency poison')
    os.environ['LEAN_PATH'] = str(cache)
    os.environ['LEAN_SYSROOT'] = '/tmp/not-a-toolchain'
    os.environ['ELAN_TOOLCHAIN'] = 'not-a-toolchain'
    deps = c.run_lean(p, ['--deps', str(p/c.TARGET_REL)])
    assert deps.returncode == 0, deps.stdout
    assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout, deps.stdout
    assert str(cache/'FCBTrustedSpec.olean') not in deps.stdout
    c.check_build(p); c.check_golden_theorem_import(p)
    c.check_trusted_type(p)
    print('PASS fixed Spec/dependency origin despite same-name candidate module/cache and environment', flush=True)

with c.make_fresh_golden_project() as td:
    p = Path(td)
    helper = 'import FormalConjectures.Util.ProblemImports\nnamespace Green2.Real\ndef log (_ : ℝ) : ℝ := 0\nend Green2.Real\n'
    c.check_banned_patterns(helper)
    (p/'FormalConjecturesBench/Submission.lean').write_text(helper)
    c.check_frozen_prefix_and_header(text)
    c.check_build(p)
    rejects('name shadowing: unchanged frozen text/header', lambda: c.check_golden_theorem_import(p), 'Type mismatch')
    print('PASS semantic negative compiled and reached full type comparison', flush=True)

old = c.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='green2refute-spec-negative-') as td:
    p = Path(td)
    shutil.copytree(old, p, dirs_exist_ok=True)
    c.SPEC_DIR = p
    artifact = p/'FCBTrustedSpec.olean'
    original = artifact.read_bytes(); artifact.unlink()
    rejects('missing artifact', c.load_trusted_spec, 'Missing trusted Spec artifact')
    assert not artifact.exists(), 'runtime regenerated missing Spec'
    artifact.write_bytes(original + b'corrupted')
    rejects('corrupt artifact', c.load_trusted_spec, 'artifact hash mismatch')
    (p/'manifest.json').write_text('{}')
    rejects('corrupt manifest', c.load_trusted_spec, 'manifest hash mismatch')
    c.SPEC_DIR = old
c.load_trusted_spec()
print('ALL SUPPLEMENTARY CHECKS PASSED; original theorem remains unproved.', flush=True)
