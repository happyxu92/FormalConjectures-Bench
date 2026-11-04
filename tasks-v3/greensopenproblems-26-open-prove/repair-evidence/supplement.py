"""Independent coverage fixture: call the delivered checker, never modify public Target."""
import importlib.util
import os
from pathlib import Path
import tempfile
import shutil
import json

spec = importlib.util.spec_from_file_location('checker', str(Path(os.environ.get('FCB_TESTS_DIR', '/tests')) / 'test_target.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
results = {}

def reject(label, call):
    try:
        call()
    except SystemExit as e:
        assert e.code == 1
        results[label] = 'rejected as expected'
    else:
        raise AssertionError(label + ' unexpectedly passed')

text = m.target_text()
m.check_frozen_prefix_and_header(text)
results['original_frozen_header'] = 'passed'
reject('frozen_prefix_mutation', lambda: m.check_frozen_prefix_and_header('-- change\n' + text))
reject('header_mutation', lambda: m.check_frozen_prefix_and_header(text.replace('theorem green_26.variants.open :', 'theorem green_26.variants.openX :')))
reject('missing_assignment', lambda: m.check_frozen_prefix_and_header(text.replace('= univ) := by', '= univ) by')))
reject('placeholder_source_rule', lambda: m.check_banned_patterns(m.check_frozen_prefix_and_header(text)))

with tempfile.TemporaryDirectory(prefix='green26-outside-') as temp:
    candidate = Path(temp)
    shutil.copytree(m.GOLDEN_ENV_DIR, candidate, dirs_exist_ok=True)
    (candidate / 'Outside.lean').write_text('def outside : Nat := 0\n')
    old = m.TASK_DIR
    m.TASK_DIR = candidate
    reject('out_of_bounds_source', m.check_extra_lean_files_confined)
    m.TASK_DIR = old

m.load_trusted_spec()
with m.make_fresh_golden_project() as temp:
    project = Path(temp)
    m.check_trusted_type(project)
    results['trusted_spec_audit'] = 'passed'
    m.check_build(project)
    results['ubuntu_candidate_compilation'] = 'passed (isolated placeholder fixture)'
    m.check_golden_theorem_import(project)
    results['complete_type_comparison'] = 'passed for original full type'
    reject('target_axioms_sorryAx', lambda: m.check_axioms(project))
    m.check_sorry_canary(project)
    results['sorry_canary'] = 'detected sorryAx'

    # Neither candidate same-name source/caches nor inherited search paths replace Spec.
    for p in [project / 'FCBTrustedSpec.olean', project / '.lake/build/lib/lean/FCBTrustedSpec.olean']:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b'invalid candidate replacement')
    (project / 'FCBTrustedSpec.lean').write_text('def malicious : True := True.intro\n')
    os.environ['LEAN_PATH'] = str(project)
    os.environ['LEAN_SYSROOT'] = str(project)
    dep = m.run_lean(project, ['--deps', str(project / m.TARGET_REL)])
    assert dep.returncode == 0, dep.stdout
    fixed = str(m.SPEC_DIR / 'FCBTrustedSpec.olean')
    assert fixed in dep.stdout, dep.stdout
    m.check_golden_theorem_import(project)
    m.check_trusted_type(project)
    results['same_name_source_cache_environment'] = 'fixed trusted olean selected; audit and complete type still pass'

# Header and frozen text remain byte-for-byte unchanged. Only Submission shadows univ.
with m.make_fresh_golden_project() as temp:
    project = Path(temp)
    submission = project / 'FormalConjecturesBench/Submission.lean'
    submission.write_text('import FormalConjectures.Util.ProblemImports\nnamespace Green26\ndef univ {α : Type*} : Set α := ∅\nend Green26\n')
    m.check_banned_patterns(submission.read_text())
    m.check_frozen_prefix_and_header(text)
    m.check_build(project)
    reject('semantic_univ_shadow_full_type', lambda: m.check_golden_theorem_import(project))
    results['semantic_shadow_frozen_text'] = 'original frozen prefix/header unchanged; altered type compiles and full comparison rejects'

# Corrupt/missing artifacts must fail before any compile or generation can run.
for mode in ('missing', 'corrupt'):
    with tempfile.TemporaryDirectory(prefix='green26-spec-') as temp:
        package = Path(temp) / 'trusted_spec'
        shutil.copytree(m.SPEC_DIR, package)
        artifact = package / 'FCBTrustedSpec.olean'
        if mode == 'missing': artifact.unlink()
        else: artifact.write_bytes(b'corrupt')
        old = m.SPEC_DIR
        m.SPEC_DIR = package
        reject(mode + '_artifact', m.load_trusted_spec)
        m.SPEC_DIR = old

print('COVERAGE_JSON=' + json.dumps(results, ensure_ascii=False, indent=2))
