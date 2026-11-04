import importlib.util, os, pathlib, tempfile, shutil, json, hashlib
os.environ['FCB_TASK_DIR']='/app'; os.environ['FCB_TESTS_DIR']='/tests'
s=importlib.util.spec_from_file_location('checker','/tests/test_target.py'); c=importlib.util.module_from_spec(s); s.loader.exec_module(c)
results={}
def expect_reject(name, fn):
    try: fn()
    except SystemExit as e:
        assert e.code==1, (name,e.code)
        results[name]='rejected as expected'; print('PASS REJECTION',name,flush=True)
    else: raise AssertionError('accepted '+name)
c.load_trusted_spec(); results['spec_load']='passed'
with c.make_fresh_golden_project() as tmp:
    p=pathlib.Path(tmp)
    c.check_trusted_type(p); results['spec_type_audit']='passed'
    c.check_build(p); results['ubuntu_candidate_compile']='passed (isolated original sorry fixture)'
    c.check_golden_theorem_import(p); results['complete_type_comparison']='passed'
    expect_reject('target_sorry_axiom_audit',lambda:c.check_axioms(p))
    c.check_sorry_canary(p); results['sorry_canary']='passed'

original=c.target_text()
expect_reject('frozen_prefix',lambda:c.check_frozen_prefix_and_header(original.replace('namespace Erdos244','namespace Erdos244 -- altered',1)))
expect_reject('header',lambda:c.check_frozen_prefix_and_header(original.replace('∀ C >','∀ C ≥',1)))
with tempfile.TemporaryDirectory(prefix='244-refute-fixture-') as td:
    fixture=pathlib.Path(td)
    shutil.copytree(c.GOLDEN_ENV_DIR,fixture,dirs_exist_ok=True)
    c.TASK_DIR=fixture; c.TARGET=fixture/c.TARGET_REL
    (fixture/'Extra.lean').write_text('')
    expect_reject('outside_editable_source',c.check_extra_lean_files_confined)
    (fixture/'Extra.lean').unlink()
    target=c.TARGET
    text=original.replace('  sorry','  intro h\n  have bad : (0 : ℝ) ≠ 0 := h 2 (show (1 : ℝ) ≠ 0 from one_ne_zero)\n  exact bad rfl')
    target.write_text(text)
    (fixture/c.EDITABLE_REL/'Submission.lean').write_text('import FormalConjectures.Util.ProblemImports\ninstance : LT ℝ := ⟨fun x _ => x ≠ 0⟩\n')
    # Same frozen bytes/header, no banned syntax; candidate LT changes both inequalities.
    c.check_frozen_prefix_and_header(text); c.check_no_banned_patterns_in_editable_sources()
    with c.make_fresh_golden_project() as tmp:
        p=pathlib.Path(tmp)
        c.check_build(p)
        expect_reject('semantic_shadow_LT_complete_type',lambda:c.check_golden_theorem_import(p))
    # A same-named candidate Spec module and .lake cache must never be used.
    (fixture/c.EDITABLE_REL/'Submission.lean').write_bytes((c.GOLDEN_ENV_DIR/c.EDITABLE_REL/'Submission.lean').read_bytes())
    target.write_text(original)
    (fixture/c.EDITABLE_REL/'FCBTrustedSpec.lean').write_text('def maliciousReplacement : True := True.intro\n')
    cache=fixture/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'invalid candidate replacement')
    with c.make_fresh_golden_project() as tmp:
        p=pathlib.Path(tmp)
        (p/'FCBTrustedSpec.lean').write_text('invalid candidate replacement')
        (p/'FCBTrustedSpec.olean').write_bytes(b'invalid candidate replacement')
        out=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
        assert out.returncode==0 and str(c.SPEC_DIR/'FCBTrustedSpec.olean') in out.stdout,out.stdout
        c.check_trusted_type(p); c.check_build(p); c.check_golden_theorem_import(p)
        results['candidate_named_module_cache']='fixed trusted olean selected; compile/audit/type passed'

# Isolated damaged package; no modification of official artifacts/checker.
with tempfile.TemporaryDirectory(prefix='244-refute-bad-spec-') as td:
    package=pathlib.Path(td)/'trusted_spec'; shutil.copytree(c.SPEC_DIR,package)
    c.SPEC_DIR=package
    art=package/'FCBTrustedSpec.olean'; saved=art.read_bytes(); art.unlink()
    expect_reject('missing_precompiled_artifact',c.load_trusted_spec)
    assert not art.exists(), 'unexpected regeneration'
    art.write_bytes(saved+b'corruption')
    expect_reject('corrupt_precompiled_artifact',c.load_trusted_spec)
print('COVERAGE_RESULTS '+json.dumps(results,sort_keys=True),flush=True)
