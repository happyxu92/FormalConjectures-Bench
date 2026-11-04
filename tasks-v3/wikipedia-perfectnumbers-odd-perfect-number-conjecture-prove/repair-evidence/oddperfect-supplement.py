from pathlib import Path
import importlib.util, tempfile, shutil, os, hashlib, subprocess
spec = importlib.util.spec_from_file_location('checker', '/tests/test_target.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def rejected(name, fn):
    try:
        fn()
    except SystemExit as e:
        assert e.code == 1
        print('PASS expected rejection:', name, flush=True)
    else:
        raise AssertionError('accepted: ' + name)

def point(root):
    m.TASK_DIR = root
    m.TARGET = root / m.TARGET_REL

print('uid', os.geteuid(), 'SPEC_DIR', m.SPEC_DIR, flush=True)
m.load_trusted_spec()
with tempfile.TemporaryDirectory(prefix='oddperfect-fixtures-') as td:
    root = Path(td)
    task = root/'task'
    shutil.copytree(m.GOLDEN_ENV_DIR, task)
    point(task)
    text = m.target_text()
    m.check_frozen_prefix_and_header(text)
    rejected('original sorry syntax', lambda: m.check_banned_patterns(m.check_frozen_prefix_and_header(text)))
    rejected('frozen prefix modification', lambda: m.check_frozen_prefix_and_header(text.replace('open Nat', 'open Nat\n-- changed')))
    extra = task/'Outside.lean'; extra.write_text('example : True := True.intro\n')
    rejected('source outside editable tree', m.check_extra_lean_files_confined); extra.unlink()
    m.check_editable_tree_shape(); m.check_extra_lean_files_confined(); m.check_frozen_files_unchanged()
    # Isolated placeholder fixture covers post-syntax paths without changing or
    # relaxing the production checker, candidate, golden or dependency files.
    with m.make_fresh_golden_project() as p:
        project = Path(p)
        m.check_trusted_type(project)
        m.check_build(project)
        m.check_golden_theorem_import(project)
        rejected('target sorryAx audit', lambda: m.check_axioms(project))
        m.check_sorry_canary(project)
        print('PASS canary and matching complete forall type', flush=True)
        deps = m.run_lean(project, ['--deps', str(project/m.TARGET_REL)])
        assert deps.returncode == 0 and str(m.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout
        print('PASS trusted import path:', deps.stdout, flush=True)
    # Frozen text unchanged; an ordinary def in editable Submission shadows Even.
    prefix, rest = text.split(m.MARKER, 1)
    rest = rest.replace(':= by\n  sorry', ':= by\n  trivial', 1)
    m.TARGET.write_text(prefix + m.MARKER + rest)
    (task/'FormalConjecturesBench/Submission.lean').write_text('namespace PerfectNumbers\ndef Even (_ : Nat) : Prop := True\nend PerfectNumbers\n')
    m.check_frozen_prefix_and_header(m.target_text())
    m.check_banned_patterns(m.check_frozen_prefix_and_header(m.target_text()))
    m.check_no_banned_patterns_in_editable_sources(); m.check_frozen_files_unchanged()
    m.check_extra_lean_files_confined(); m.check_editable_tree_shape()
    with m.make_fresh_golden_project() as p:
        project = Path(p)
        m.check_trusted_type(project)
        m.check_build(project)
        m.check_axioms(project)
        rejected('semantic Even shadow with unchanged frozen text', lambda: m.check_golden_theorem_import(project))
    # A same-name precompiled candidate module, in cache and an ordinary external
    # LEAN_PATH, must not take the place of the fixed trusted module.
    fake = root/'fake'; fake.mkdir()
    (fake/'FCBTrustedSpec.lean').write_text('def FCBTrustedSpec.ExpectedType : Prop := True\n')
    cp = subprocess.run([str(m.LEAN), '-o', str(fake/'FCBTrustedSpec.olean'), str(fake/'FCBTrustedSpec.lean')], cwd=fake, env=m.ENV, capture_output=True,text=True)
    assert cp.returncode == 0, cp.stdout+cp.stderr
    cache = task/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    shutil.copy2(fake/'FCBTrustedSpec.olean', cache/'FCBTrustedSpec.olean')
    os.environ['LEAN_PATH'] = str(fake)+':'+str(cache)
    with m.make_fresh_golden_project() as p:
        project=Path(p)
        shutil.copy2(fake/'FCBTrustedSpec.olean', project/'FCBTrustedSpec.olean')
        m.check_trusted_type(project)
        deps = m.run_lean(project, ['--deps', str(project/m.TARGET_REL)])
        assert deps.returncode == 0, deps.stdout
        assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout, deps.stdout
        assert str(fake/'FCBTrustedSpec.olean') not in deps.stdout, deps.stdout
        print('PASS same-name candidate module, cache and LEAN_PATH cannot replace Spec', flush=True)
    del os.environ['LEAN_PATH']
    fixed=m.SPEC_DIR
    broken=root/'broken-spec'; shutil.copytree(fixed,broken); m.SPEC_DIR=broken
    artifact=broken/'FCBTrustedSpec.olean'; original=artifact.read_bytes(); artifact.unlink()
    rejected('missing precompiled artifact', m.load_trusted_spec)
    assert not artifact.exists(), 'runtime regeneration occurred'
    artifact.write_bytes(original+b'corrupted')
    rejected('precompiled artifact hash mismatch', m.load_trusted_spec)
    assert artifact.read_bytes()==original+b'corrupted', 'runtime regenerated artifact'
    (broken/'manifest.json').write_text('{}')
    rejected('manifest hash mismatch', m.load_trusted_spec)
    m.SPEC_DIR=fixed
    m.load_trusted_spec()
print('ALL SUPPLEMENTARY CHECKS PASSED', flush=True)
