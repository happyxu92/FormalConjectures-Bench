import importlib.util, os, sys, shutil, tempfile, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('checker', sys.argv[1] if len(sys.argv) > 1 else '/tests/test_target.py')
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)

def rejects(label, fn, contains):
    try:
        fn()
    except SystemExit as exc:
        assert exc.code == 1
        print('PASS expected rejection:', label, flush=True)
        return
    raise AssertionError('Unexpected acceptance: ' + label)

assert c.SPEC_DIR == c.TESTS_DIR / 'trusted_spec'
print('Validated checker path:', spec.origin, 'Spec path:', c.SPEC_DIR, 'test uid:', os.getuid(), flush=True)
assert c.TASK_DIR == Path('/app')
text = c.target_text()
c.check_frozen_prefix_and_header(text)
c.check_editable_tree_shape(); c.check_extra_lean_files_confined(); c.check_frozen_files_unchanged()
rejects('frozen prefix changed', lambda: c.check_frozen_prefix_and_header(text.replace('open Classical', 'open Classical\n-- changed', 1)), '')
rejects('header changed', lambda: c.check_frozen_prefix_and_header(text.replace('theorem erdos_32 :', 'theorem erdos_32_bad :', 1)), '')
rejects('assignment removed', lambda: c.check_frozen_prefix_and_header(text.replace('^ 2 := by\n  sorry\n\nend Erdos32', '^ 2 by\n  sorry\n\nend Erdos32')), '')
rejects('proof placeholder source', lambda: c.check_banned_patterns('by\n sorry'), '')
with tempfile.TemporaryDirectory(prefix='fcb32-confined-') as td:
    old = c.TASK_DIR
    c.TASK_DIR = Path(td)
    shutil.copytree(c.GOLDEN_ENV_DIR, td, dirs_exist_ok=True)
    (Path(td) / 'Outside.lean').write_text('def outside := 1\n')
    rejects('out-of-tree source', c.check_extra_lean_files_confined, '')
    c.TASK_DIR = old

c.load_trusted_spec()
with c.make_fresh_golden_project() as td:
    p = Path(td)
    c.check_trusted_type(p)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    rejects('target axiom audit detects sorryAx', lambda: c.check_axioms(p), '')
    c.check_sorry_canary(p)
    print('PASS sorry canary', flush=True)
    # Candidate roots/caches must not replace the fixed module.
    (p/'FCBTrustedSpec.lean').write_text('THIS IS NOT VALID LEAN\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'candidate module poison')
    cache = p/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'candidate cached module poison')
    os.environ['LEAN_PATH'] = str(cache)
    os.environ['LEAN_SYSROOT'] = '/tmp/not-a-toolchain'
    os.environ['ELAN_TOOLCHAIN'] = 'not-a-toolchain'
    deps = c.run_lean(p, ['--deps', str(p/c.TARGET_REL)])
    assert deps.returncode == 0, deps.stdout
    assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout, deps.stdout
    assert str(cache/'FCBTrustedSpec.olean') not in deps.stdout
    print('fixed Spec dependency resolution:\n'+deps.stdout, flush=True)
    c.check_build(p); c.check_golden_theorem_import(p)
    print('PASS same-name candidate module/cache and environment cannot replace Spec', flush=True)

# Freeze text and theorem header remain byte-for-byte unchanged. Only normal helper def changes.
with c.make_fresh_golden_project() as td:
    p = Path(td)
    helper = 'import FormalConjectures.Util.ProblemImports\nnamespace Erdos32.Real\ndef log (_ : ℝ) : ℝ := 0\nend Erdos32.Real\n'
    c.check_banned_patterns(helper)
    (p/'FormalConjecturesBench/Submission.lean').write_text(helper)
    c.check_frozen_prefix_and_header(text)
    c.check_build(p)
    rejects('name shadowing changes full target type', lambda: c.check_golden_theorem_import(p), '')
    print('PASS semantic shadowing reaches and fails complete type comparison', flush=True)

old = c.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='fcb32-spec-negative-') as td:
    p = Path(td)
    shutil.copytree(old, p, dirs_exist_ok=True)
    c.SPEC_DIR = p
    artifact = p/'FCBTrustedSpec.olean'
    original = artifact.read_bytes(); artifact.unlink()
    rejects('missing precompiled artifact', c.load_trusted_spec, '')
    assert not artifact.exists(), 'runtime regenerated missing Spec'
    artifact.write_bytes(original + b'corrupted')
    rejects('corrupt precompiled artifact', c.load_trusted_spec, '')
    (p/'manifest.json').write_text('{}')
    rejects('corrupt manifest', c.load_trusted_spec, '')
    c.SPEC_DIR = old
c.load_trusted_spec()
print('ALL SUPPLEMENTARY CHECKS PASSED; no proof of the open theorem was supplied.', flush=True)
