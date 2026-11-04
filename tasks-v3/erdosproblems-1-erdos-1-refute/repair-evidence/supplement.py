from pathlib import Path
import importlib.util, tempfile, shutil, os, hashlib
checker_path=Path(os.environ.get('FCB_TESTS_DIR','/tests'))/'test_target.py'
spec=importlib.util.spec_from_file_location('checker',checker_path)
print('CHECKER:',checker_path,flush=True)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

def reject(label,fn):
    try: fn()
    except SystemExit as e:
        assert e.code==1
        print('EXPECTED REJECTION:',label,flush=True)
    else: raise AssertionError('accepted '+label)

def fixture(root):
    c.TASK_DIR=root;c.TARGET=root/c.TARGET_REL
    shutil.copytree(c.GOLDEN_ENV_DIR,root,dirs_exist_ok=True)

with tempfile.TemporaryDirectory(prefix='erdos1-refute-supplement-') as t:
    root=Path(t); fixture(root)
    c.load_trusted_spec()
    with c.make_fresh_golden_project() as d:
        p=Path(d)
        c.check_trusted_type(p)
        c.check_build(p)
        c.check_golden_theorem_import(p)
        reject('placeholder target axiom audit',lambda:c.check_axioms(p))
        c.check_sorry_canary(p)
        print('PASS: fixed Spec audit, ubuntu build, full type equality, sorryAx rejection, canary',flush=True)
    original=c.target_text()
    reject('frozen text mutation',lambda:c.check_frozen_prefix_and_header(original.replace('namespace Erdos1','namespace Bad',1)))
    extra=root/'Outside.lean';extra.write_text('def x := 1\n')
    reject('out-of-bounds source',c.check_extra_lean_files_confined);extra.unlink()
    # All frozen text stays byte-identical. An allowed high-priority instance
    # changes the meaning of > and < in the freshly elaborated candidate header.
    (root/c.EDITABLE_REL/'Submission.lean').write_text('import FormalConjectures.Util.ProblemImports\nnoncomputable instance (priority := 100000) : LT ℝ := ⟨fun _ _ => False⟩\n')
    c.TARGET.write_text(original.replace('by\n  sorry','by\n  rintro ⟨C, hC, _⟩\n  exact hC'))
    c.check_frozen_prefix_and_header(c.target_text());c.check_editable_tree_shape()
    c.check_no_banned_patterns_in_editable_sources();c.check_extra_lean_files_confined();c.check_frozen_files_unchanged()
    with c.make_fresh_golden_project() as d:
        p=Path(d);c.check_build(p)
        reject('instance semantic substitution with unchanged frozen header',lambda:c.check_golden_theorem_import(p))
        c.check_axioms(p)
        print('PASS: semantic substitution has no forbidden axioms, but complete type comparison rejects',flush=True)
    # Same-name candidate source and compiled cache are searched after fixed Spec.
    (root/c.EDITABLE_REL/'Submission.lean').write_bytes((c.GOLDEN_ENV_DIR/c.EDITABLE_REL/'Submission.lean').read_bytes())
    c.TARGET.write_text(original)
    with c.make_fresh_golden_project() as d:
        p=Path(d)
        (p/'FCBTrustedSpec.lean').write_text('invalid candidate Spec\n')
        (p/'FCBTrustedSpec.olean').write_bytes(b'corrupt candidate Spec')
        cache=p/'.lake/build/lib/lean';cache.mkdir(parents=True)
        (cache/'FCBTrustedSpec.olean').write_bytes(b'corrupt candidate cache')
        os.environ['LEAN_PATH']=str(cache)
        os.environ['LEAN_SYSROOT']=str(p)
        c.check_trusted_type(p);c.check_build(p);c.check_golden_theorem_import(p)
        print('PASS: candidate same-name source/olean/cache/environment cannot replace fixed Spec',flush=True)
    real_spec=c.SPEC_DIR
    copied=root/'spec-missing';shutil.copytree(real_spec,copied)
    c.SPEC_DIR=copied
    (copied/'FCBTrustedSpec.olean').unlink()
    reject('missing precompiled artifact',c.load_trusted_spec)
    assert not (copied/'FCBTrustedSpec.olean').exists()
    shutil.copy2(real_spec/'FCBTrustedSpec.olean',copied/'FCBTrustedSpec.olean')
    with (copied/'FCBTrustedSpec.olean').open('ab') as f:f.write(b'x')
    reject('corrupt artifact hash',c.load_trusted_spec)
    c.SPEC_DIR=real_spec
print('ALL SUPPLEMENTARY PATHS PASSED',flush=True)
