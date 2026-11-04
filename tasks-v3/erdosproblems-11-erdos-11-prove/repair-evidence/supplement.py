from pathlib import Path
import importlib.util, shutil, os, json, hashlib, tempfile
spec = importlib.util.spec_from_file_location('checker', '/tests/test_target.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def reject(label, fn):
    try:
        fn()
    except SystemExit as e:
        assert e.code == 1, (label, e.code)
        print('EXPECTED REJECTION:', label, flush=True)
    else:
        raise AssertionError('accepted: ' + label)

m.load_trusted_spec()
with m.make_fresh_golden_project() as td:
    p = Path(td)
    m.check_trusted_type(p)
    m.check_build(p)
    m.check_golden_theorem_import(p)
    reject('original placeholder theorem axiom audit (sorryAx)', lambda: m.check_axioms(p))
    m.check_sorry_canary(p)
    print('PASS: independent Spec audit, ubuntu build, full type, sorry rejection, canary', flush=True)
    # Neither a same-named candidate source/olean nor its ordinary Lake cache
    # nor ambient path can replace the first fixed precompiled module.
    fake = p / 'FCBTrustedSpec.lean'
    fake.write_text('def FCBTrustedSpec.ExpectedType : Prop := False\n')
    r = m.run_lean(p, ['-o', str(p / 'FCBTrustedSpec.olean'), str(fake)])
    assert r.returncode == 0, r.stdout
    cache = p / '.lake/build/lib/lean'; cache.mkdir(parents=True)
    shutil.copy2(p/'FCBTrustedSpec.olean', cache/'FCBTrustedSpec.olean')
    os.environ['LEAN_PATH'] = str(cache)
    r = m.run_lean(p, ['--deps', str(p/m.TARGET_REL)])
    assert r.returncode == 0, r.stdout
    assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in r.stdout, r.stdout
    assert str(p/'FCBTrustedSpec.olean') not in r.stdout, r.stdout
    m.check_golden_theorem_import(p)
    m.check_trusted_type(p)
    print('PASS: same-name candidate source/artifact/cache and ambient LEAN_PATH cannot replace Spec', flush=True)

# An isolated candidate fixture with frozen Target text intact, but a normal
# helper def that changes the meaning of the unqualified assumption Odd.
with tempfile.TemporaryDirectory(prefix='erdos11-fixture-') as td:
    task = Path(td)
    shutil.copytree(m.GOLDEN_ENV_DIR, task, dirs_exist_ok=True)
    target = task / m.TARGET_REL
    original = target.read_text()
    target.write_text(original.replace('by\n  sorry', 'by\n  cases hn'))
    (task/'FormalConjecturesBench/Submission.lean').write_text(
        'import FormalConjectures.Util.ProblemImports\nnamespace Erdos11\ndef Odd (_ : ℕ) : Prop := False\nend Erdos11\n')
    m.TASK_DIR = task; m.TARGET = target
    proof = m.check_frozen_prefix_and_header(m.target_text())
    m.check_banned_patterns(proof); m.check_editable_tree_shape()
    m.check_no_banned_patterns_in_editable_sources(); m.check_extra_lean_files_confined()
    m.check_frozen_files_unchanged()
    with m.make_fresh_golden_project() as tmp:
        p = Path(tmp)
        m.check_trusted_type(p); m.check_build(p)
        m.check_axioms(p) # a genuine proof of the WRONG type, no sorry
        reject('frozen-header semantic name-shadowing (Erdos11.Odd := False)', lambda: m.check_golden_theorem_import(p))
        m.check_sorry_canary(p)
    target.write_text(original.replace('namespace Erdos11', 'namespace Erdos11\n-- frozen change'))
    reject('frozen-prefix mutation', lambda: m.check_frozen_prefix_and_header(m.target_text()))
    target.write_text(original.replace('by\n  sorry', 'by\n  cases hn'))
    (task/'OutOfBounds.lean').write_text('theorem x : True := trivial\n')
    reject('Lean source outside editable subtree', m.check_extra_lean_files_confined)

# Never change the actual trusted package: make damaged isolated copies.
real = m.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='erdos11-spec-negative-') as td:
    damaged = Path(td)/'trusted_spec'
    shutil.copytree(real, damaged)
    m.SPEC_DIR = damaged
    artifact = damaged/'FCBTrustedSpec.olean'; saved = artifact.read_bytes()
    artifact.unlink()
    reject('missing precompiled Spec; no fallback compile', m.load_trusted_spec)
    assert not artifact.exists()
    artifact.write_bytes(saved+b'corrupt')
    reject('artifact hash mismatch; no regeneration', m.load_trusted_spec)
    assert artifact.read_bytes() == saved+b'corrupt'
    (damaged/'manifest.json').write_text('{}')
    reject('manifest hash mismatch', m.load_trusted_spec)
m.SPEC_DIR = real
print('ALL SUPPLEMENTAL PATHS PASSED', flush=True)
