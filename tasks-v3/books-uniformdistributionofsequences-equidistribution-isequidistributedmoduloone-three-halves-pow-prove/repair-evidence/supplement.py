import importlib.util, os, shutil, tempfile, pwd
from pathlib import Path
checker_dir=Path(os.environ.get('FCB_TESTS_DIR','/tests'))
spec=importlib.util.spec_from_file_location('checker', checker_dir/'test_target.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

def reject(label, fn, needle):
    import contextlib, io
    buf=io.StringIO()
    with contextlib.redirect_stderr(buf):
        try: fn()
        except SystemExit as e:
            assert e.code == 1
        else: raise AssertionError(label+' was accepted')
    output=buf.getvalue()
    assert needle in output, (label, output)
    print('REJECTED',label,output.strip(),flush=True)

manifest=m.load_trusted_spec()
with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    m.check_trusted_type(p)
    m.check_build(p)
    assert (p/m.TARGET_REL.with_suffix('.olean')).stat().st_uid == pwd.getpwnam('ubuntu').pw_uid
    m.check_golden_theorem_import(p)
    reject('placeholder target axiom audit',lambda:m.check_axioms(p),'sorryAx')
    m.check_sorry_canary(p); print('PASS sorry canary',flush=True)
    # Candidate same-name source, olean, build cache and environment cannot win.
    (p/'FCBTrustedSpec.lean').write_text('invalid candidate replacement')
    (p/'FCBTrustedSpec.olean').write_bytes(b'invalid candidate artifact')
    cache=p/'.lake/build/lib/lean';cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'invalid cache artifact')
    (cache/'Mathlib.olean').write_bytes(b'invalid dependency cache artifact')
    os.environ['LEAN_PATH']=str(cache)
    result=m.run_lean(p,['--deps',str(p/m.TARGET_REL)])
    assert result.returncode == 0, result.stdout
    assert str(m.SPEC_DIR/'FCBTrustedSpec.olean') in result.stdout, result.stdout
    assert str(p/'FCBTrustedSpec.olean') not in result.stdout, result.stdout
    m.check_golden_theorem_import(p)
    m.check_trusted_type(p)
    print('PASS candidate same-name modules/cache/environment did not replace trusted Spec/dependencies',flush=True)

original=m.target_text()
reject('frozen prefix edit',lambda:m.check_frozen_prefix_and_header('--changed\n'+original),'above the benchmark')
reject('header edit',lambda:m.check_frozen_prefix_and_header(original.replace('theorem isEquidistributed','theorem alteredIsEquidistributed',1)),'header changed')
reject('removed assignment',lambda:m.check_frozen_prefix_and_header(original.replace(m.EXPECTED_HEADER+' :=',m.EXPECTED_HEADER+' --',1)),'proof assignment')
reject('original sorry source',lambda:m.check_banned_patterns(m.check_frozen_prefix_and_header(original)),'Banned Lean feature')

with tempfile.TemporaryDirectory(prefix='fcb-boundary-') as tmp:
    p=Path(tmp);shutil.copytree(m.GOLDEN_ENV_DIR,p,dirs_exist_ok=True)
    saved=m.TASK_DIR;m.TASK_DIR=p
    try:
        (p/'Escape.lean').write_text('import Mathlib\n')
        reject('out of subtree Lean source',m.check_extra_lean_files_confined,'outside editable subtree')
        (p/'Escape.lean').unlink()
        (p/'lakefile.toml').write_text('changed')
        reject('frozen project configuration',m.check_frozen_files_unchanged,'modified')
        (p/m.EDITABLE_REL/'link.lean').symlink_to(p/m.TARGET_REL)
        reject('editable symlink',m.check_editable_tree_shape,'Symlinks')
    finally:m.TASK_DIR=saved

# Unchanged frozen target text, but a legal helper instance changes division meaning.
with tempfile.TemporaryDirectory(prefix='fcb-instance-fixture-') as tmp:
    fixture=Path(tmp);shutil.copytree(m.GOLDEN_ENV_DIR,fixture,dirs_exist_ok=True)
    helper=fixture/m.EDITABLE_REL/'Submission.lean'
    helper.write_text('import FormalConjectures.Util.ProblemImports\ninstance (priority := 1000000) : HDiv ℝ ℝ ℝ where\n  hDiv _ _ := 0\n')
    m.check_banned_patterns(helper.read_text())
    assert (fixture/m.TARGET_REL).read_text() == original
    m.check_frozen_prefix_and_header((fixture/m.TARGET_REL).read_text())
    saved=m.TASK_DIR;m.TASK_DIR=fixture
    try:
        m.check_editable_tree_shape();m.check_extra_lean_files_confined();m.check_frozen_files_unchanged()
        with m.make_fresh_golden_project() as project:
            p=Path(project)
            m.check_build(p)
            reject('unchanged header but helper HDiv semantic substitution',lambda:m.check_golden_theorem_import(p),'Type mismatch')
    finally:m.TASK_DIR=saved

saved=m.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='fcb-broken-spec-') as tmp:
    p=Path(tmp);shutil.copytree(saved,p,dirs_exist_ok=True);m.SPEC_DIR=p
    try:
        o=p/'FCBTrustedSpec.olean';data=o.read_bytes();o.unlink()
        reject('missing precompiled Spec',m.load_trusted_spec,'Missing trusted Spec artifact')
        assert not o.exists()
        o.write_bytes(data+b'corrupt')
        reject('corrupt precompiled Spec',m.load_trusted_spec,'artifact hash mismatch')
        assert o.read_bytes()==data+b'corrupt'
        o.write_bytes(data)
        (p/'manifest.json').write_text('{}')
        reject('manifest tamper',m.load_trusted_spec,'manifest hash mismatch')
    finally:m.SPEC_DIR=saved
print('PASS all supplementary stages; original theorem remains unproved',flush=True)
