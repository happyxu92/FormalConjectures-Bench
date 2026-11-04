"""Isolated path coverage, not a proof submission; public/golden inputs untouched."""
from pathlib import Path
import importlib.util, shutil, os, tempfile
checker = os.environ.get('FCB_SUPPLEMENT_CHECKER', '/tests/test_target.py')
spec = importlib.util.spec_from_file_location('checker', checker)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

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
    reject('original placeholder axiom audit detects sorryAx', lambda: m.check_axioms(p))
    m.check_sorry_canary(p)
    print('PASS: Spec audit, ubuntu build, complete type, axiom rejection, canary', flush=True)
    fake = p / 'FCBTrustedSpec.lean'
    fake.write_text('def FCBTrustedSpec.ExpectedType : Prop := False\n')
    r = m.run_lean(p, ['-o', str(p/'FCBTrustedSpec.olean'), str(fake)])
    assert r.returncode == 0, r.stdout
    cache = p / '.lake/build/lib/lean'
    cache.mkdir(parents=True)
    shutil.copy2(p/'FCBTrustedSpec.olean', cache/'FCBTrustedSpec.olean')
    os.environ['LEAN_PATH'] = str(cache)
    os.environ['LEAN_SYSROOT'] = '/nonexistent/candidate-sysroot'
    r = m.run_lean(p, ['--deps', str(p/m.TARGET_REL)])
    assert r.returncode == 0, r.stdout
    assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in r.stdout, r.stdout
    assert str(p/'FCBTrustedSpec.olean') not in r.stdout, r.stdout
    m.check_golden_theorem_import(p)
    m.check_trusted_type(p)
    print('PASS: fixed Spec wins over candidate same-name source/artifact/cache/environment', flush=True)

# Preserve frozen Target text, change only a normal helper name. A placeholder
# proof is intentional in this isolated fixture to reach type comparison without
# constructing either mathematical direction. The real source checker stays on.
with tempfile.TemporaryDirectory(prefix='erdos126-refute-fixture-') as td:
    task = Path(td)
    shutil.copytree(m.GOLDEN_ENV_DIR, task, dirs_exist_ok=True)
    target = task / m.TARGET_REL
    original = target.read_text()
    (task/'FormalConjecturesBench/Submission.lean').write_text(
        'import FormalConjectures.Util.ProblemImports\n'
        'namespace Erdos126\n'
        'def Tendsto {α β : Type*} (_ : α → β) (_ : Filter α) (_ : Filter β) : Prop := False\n'
        'end Erdos126\n')
    m.TASK_DIR = task
    m.TARGET = target
    proof = m.check_frozen_prefix_and_header(m.target_text())
    m.check_editable_tree_shape()
    m.check_extra_lean_files_confined()
    m.check_frozen_files_unchanged()
    reject('unchanged formal fixture placeholder still banned', lambda: m.check_banned_patterns(proof))
    # Helper itself is permitted ordinary Lean, without syntax or new axioms.
    m.check_banned_patterns((task/'FormalConjecturesBench/Submission.lean').read_text())
    with m.make_fresh_golden_project() as tmp:
        p = Path(tmp)
        m.check_trusted_type(p)
        m.check_build(p)
        reject('frozen-text name shadowing Tendsto := False, full type mismatch',
               lambda: m.check_golden_theorem_import(p))
        reject('shadow fixture placeholder is also detected by axiom audit', lambda: m.check_axioms(p))
        m.check_sorry_canary(p)
    target.write_text(original.replace('namespace Erdos126', 'namespace Erdos126\n-- changed frozen prefix'))
    reject('frozen prefix mutation', lambda: m.check_frozen_prefix_and_header(m.target_text()))
    target.write_text(original)
    (task/'OutOfBounds.lean').write_text('theorem x : True := trivial\n')
    reject('Lean source outside editable tree', m.check_extra_lean_files_confined)

real = m.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='erdos126-refute-spec-negative-') as td:
    damaged = Path(td)/'trusted_spec'
    shutil.copytree(real, damaged)
    m.SPEC_DIR = damaged
    artifact = damaged/'FCBTrustedSpec.olean'
    saved = artifact.read_bytes()
    artifact.unlink()
    reject('missing precompiled Spec; no fallback', m.load_trusted_spec)
    assert not artifact.exists()
    artifact.write_bytes(saved+b'corrupt')
    reject('corrupt artifact; no regeneration', m.load_trusted_spec)
    assert artifact.read_bytes() == saved+b'corrupt'
    (damaged/'manifest.json').write_text('{}')
    reject('manifest hash mismatch', m.load_trusted_spec)
m.SPEC_DIR = real
print('ALL SUPPLEMENTAL PATHS PASSED', flush=True)
