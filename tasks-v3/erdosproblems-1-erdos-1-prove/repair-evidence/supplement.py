import importlib.util
import os
import shutil
import tempfile
from pathlib import Path

s = importlib.util.spec_from_file_location('checker', os.environ.get('FCB_TESTS_DIR', '/tests') + '/test_target.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)

def rejected(label, action):
    try:
        action()
    except SystemExit as e:
        assert e.code == 1
        print('PASS rejection:', label, flush=True)
    else:
        raise AssertionError('accepted ' + label)

text=m.target_text()
m.check_frozen_prefix_and_header(text)
m.check_editable_tree_shape()
m.check_extra_lean_files_confined()
m.check_frozen_files_unchanged()
rejected('original sorry', lambda: m.check_banned_patterns(m.check_frozen_prefix_and_header(text)))
rejected('frozen text modification', lambda: m.check_frozen_prefix_and_header('--changed\n'+text))
with tempfile.TemporaryDirectory(prefix='erdos1-prove-outside-') as tmp:
    tmp=Path(tmp)
    shutil.copytree(m.GOLDEN_ENV_DIR, tmp, dirs_exist_ok=True)
    (tmp/'Outside.lean').write_text('theorem outside : True := by trivial\n')
    old=m.TASK_DIR
    m.TASK_DIR=tmp
    rejected('out-of-subtree source', m.check_extra_lean_files_confined)
    m.TASK_DIR=old

m.load_trusted_spec()
with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    m.check_trusted_type(p)
    m.check_build(p)
    m.check_golden_theorem_import(p)
    rejected('target sorryAx audit', lambda: m.check_axioms(p))
    m.check_sorry_canary(p)
    print('PASS sorry canary', flush=True)
    # Candidate modules, .lake caches and ambient path cannot replace Spec.
    (p/'FCBTrustedSpec.lean').write_text('def forged := True\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'forged cache')
    (p/'.lake/build/lib/lean').mkdir(parents=True)
    (p/'.lake/build/lib/lean/FCBTrustedSpec.olean').write_bytes(b'forged lake cache')
    os.environ['LEAN_PATH']=str(p)
    deps=m.run_lean(p, ['--deps', str(p/m.TARGET_REL)])
    assert deps.returncode==0, deps.stdout
    assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout, deps.stdout
    m.check_golden_theorem_import(p)
    print('PASS fixed Spec wins candidate name/cache/environment shadow', flush=True)

with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    (p/'FormalConjecturesBench/Submission.lean').write_text('''import FormalConjectures.Util.ProblemImports
namespace Erdos1
instance (priority := 1000000) : HMul ℝ ℝ ℝ := ⟨fun _ _ => 0⟩
end Erdos1
''')
    # Original Target text/header/prefix are byte-identical. The isolated fixture
    # keeps its original placeholder only to exercise the subsequent comparator.
    m.check_build(p)
    rejected('unchanged header with multiplication-instance semantic substitution', lambda: m.check_golden_theorem_import(p))

old=m.SPEC_DIR
for corrupt in ('missing','hash'):
    with tempfile.TemporaryDirectory(prefix='erdos1-prove-spec-negative-') as tmp:
        pkg=Path(tmp)/'trusted_spec'
        shutil.copytree(old,pkg)
        artifact=pkg/'FCBTrustedSpec.olean'
        if corrupt=='missing': artifact.unlink()
        else: artifact.write_bytes(b'bad artifact')
        m.SPEC_DIR=pkg
        rejected('Spec artifact '+corrupt, m.load_trusted_spec)
        if corrupt=='missing': assert not artifact.exists(), 'runtime regenerated Spec'
        else: assert artifact.read_bytes()==b'bad artifact', 'runtime regenerated Spec'
        m.SPEC_DIR=old
print('ALL SUPPLEMENTAL CHECKS PASSED', flush=True)
