import importlib.util, pathlib, tempfile, shutil, os, contextlib, io, json
spec=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
results=[]
def test(name, fn, reject=False):
    try:
        fn()
    except SystemExit as e:
        if not reject: raise
        results.append((name,'expected rejection',e.code))
    else:
        if reject: raise RuntimeError(name+' unexpectedly passed')
        results.append((name,'passed'))
    print('RESULT',results[-1],flush=True)

c.load_trusted_spec()
with c.make_fresh_golden_project() as tmp:
    p=pathlib.Path(tmp)
    test('independent trusted type audit',lambda:c.check_trusted_type(p))
    test('ubuntu original candidate build (isolated sorry fixture)',lambda:c.check_build(p))
    test('full original type matches Spec',lambda:c.check_golden_theorem_import(p))
    test('target sorryAx audit',lambda:c.check_axioms(p),True)
    test('sorry canary',lambda:c.check_sorry_canary(p))
    # A candidate module/cache cannot precede the verified Spec or its dependencies.
    (p/'FCBTrustedSpec.lean').write_text('def forged : True := True.intro\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'forged candidate cache')
    (p/'.lake/build/lib/lean').mkdir(parents=True)
    (p/'.lake/build/lib/lean/FCBTrustedSpec.olean').write_bytes(b'forged cache')
    test('same-name candidate source and caches cannot replace fixed Spec',lambda:c.check_trusted_type(p))

text=c.target_text()
test('frozen prefix change',lambda:c.check_frozen_prefix_and_header('-- changed\n'+text),True)
# Confined, isolated copy: no formal /app file is edited.
with tempfile.TemporaryDirectory(prefix='fcb244-fixture-') as tmp:
    p=pathlib.Path(tmp); shutil.copytree(c.GOLDEN_ENV_DIR,p,dirs_exist_ok=True)
    old=c.TASK_DIR; c.TASK_DIR=p
    (p/'Outside.lean').write_text('theorem outside : True := by trivial\n')
    test('out-of-scope Lean source',c.check_extra_lean_files_confined,True)
    c.TASK_DIR=old

# Shadow the ordinary LT instance on Real, while leaving frozen Target bytes intact.
# Keep sorry only in this isolated fixture so full type mismatch, not proof search,
# is the rejection criterion.
with c.make_fresh_golden_project() as tmp:
    p=pathlib.Path(tmp)
    (p/'FormalConjecturesBench/Submission.lean').write_text('import FormalConjectures.Util.ProblemImports\ninstance (priority := 100000) : LT ℝ := ⟨fun _ _ => True⟩\n')
    original = c.target_text().replace('  sorry', '  intro C hC\n  trivial')
    test('semantic shadow retains frozen prefix and header', lambda:c.check_frozen_prefix_and_header(original))
    test('semantic proof obeys source bans',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(original)))
    target=p/'FormalConjecturesBench/Target.lean'
    target.write_text(target.read_text().replace('  sorry','  intro C hC\n  trivial'))
    test('semantic shadow candidate builds without placeholder',lambda:c.check_build(p))
    test('semantic shadow has only allowed axioms',lambda:c.check_axioms(p))
    test('semantic shadow rejected by full type comparison',lambda:c.check_golden_theorem_import(p),True)

# Corruption/missing precompiled artifact fail before any Lean build; no fallback.
for mode in ('missing','corrupt'):
    with tempfile.TemporaryDirectory(prefix='fcb244-spec-negative-') as tmp:
        p=pathlib.Path(tmp); shutil.copytree(c.SPEC_DIR,p,dirs_exist_ok=True)
        if mode=='missing': (p/'FCBTrustedSpec.olean').unlink()
        else: (p/'FCBTrustedSpec.olean').write_bytes(b'corrupt')
        old=c.SPEC_DIR;c.SPEC_DIR=p
        test(mode+' precompiled Spec',c.load_trusted_spec,True)
        c.SPEC_DIR=old
print(json.dumps(results,indent=2))
