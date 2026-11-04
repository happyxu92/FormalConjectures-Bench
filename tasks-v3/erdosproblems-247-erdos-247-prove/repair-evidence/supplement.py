import contextlib, hashlib, importlib.util, io, json, os, shutil, sys, tempfile
from pathlib import Path
checker_path=Path(sys.argv[1])
s=importlib.util.spec_from_file_location('actual_checker', checker_path)
c=importlib.util.module_from_spec(s); s.loader.exec_module(c)
results=[]
def record(label, action):
    action(); results.append({'test':label,'result':'pass'}); print('PASS:',label,flush=True)
def rejects(label, action, message):
    out=io.StringIO()
    with contextlib.redirect_stderr(out):
        try: action()
        except SystemExit as e:
            assert e.code==1
        else: raise AssertionError('unexpected acceptance: '+label)
    text=out.getvalue(); assert message in text,(label,text)
    results.append({'test':label,'result':'rejected','diagnostic':text})
    print('REJECTED:',label, text[:1000],flush=True)
record('load precompiled Spec', c.load_trusted_spec)
original_spec=c.SPEC_DIR
original_task=c.TASK_DIR
original_target=c.TARGET
with c.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    record('independent transitive trusted type audit',lambda:c.check_trusted_type(p))
    record('placeholder candidate compiles with actual ubuntu compiler',lambda:c.check_build(p))
    assert (p/c.TARGET_REL.with_suffix('.olean')).stat().st_uid==1000
    record('complete correct type comparison (placeholder fixture only)',lambda:c.check_golden_theorem_import(p))
    rejects('target axiom audit rejects placeholder',lambda:c.check_axioms(p),'sorryAx')
    record('sorry detection canary',lambda:c.check_sorry_canary(p))
    # Ordinary extra imports and local helper modules remain permitted.
    helper=p/'FormalConjecturesBench/Helper.lean'
    helper.write_text('import Mathlib.NumberTheory.Transcendental.Liouville.Basic\ndef ordinaryHelper (n : ℕ) : ℕ := n\nlemma ordinaryHelper_id (n : ℕ) : ordinaryHelper n = n := rfl\n')
    submission=p/'FormalConjecturesBench/Submission.lean'
    submission.write_text('import FormalConjecturesBench.Helper\n')
    if os.geteuid()==0:
        os.chown(helper,1000,1000)
    record('normal Mathlib and local helper imports still compile',lambda:c.check_build(p))
    record('ordinary helper does not change expected type',lambda:c.check_golden_theorem_import(p))
    # Same-named candidate modules and .lake caches cannot override first fixed path.
    (p/'FCBTrustedSpec.lean').write_text('def fakeSpec : True := True.intro\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'candidate invalid cache')
    cache=p/'.lake/build/lib/lean'; cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'candidate invalid lake cache')
    os.environ['LEAN_PATH']=str(cache)
    os.environ['LEAN_SYSROOT']=str(p)
    os.environ['ELAN_TOOLCHAIN']='candidate'
    deps=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
    assert deps.returncode==0 and str(original_spec/'FCBTrustedSpec.olean') in deps.stdout,deps.stdout
    record('same-name source/cache/environment cannot replace fixed Spec',lambda:c.check_golden_theorem_import(p))
# No production source is edited: all attacks live in isolated golden copies.
with tempfile.TemporaryDirectory(prefix='ep247-fixtures-') as base:
    base=Path(base); base.chmod(0o755)
    fixture=base/'task'; shutil.copytree(c.GOLDEN_ENV_DIR,fixture)
    c.TASK_DIR=fixture; c.TARGET=fixture/c.TARGET_REL
    text=c.TARGET.read_text()
    rejects('frozen prefix modification',lambda:c.check_frozen_prefix_and_header('-- changed\n'+text),'above the benchmark target marker changed')
    (fixture/'Outside.lean').write_text('theorem outside : True := True.intro\n')
    rejects('out-of-bounds added source',c.check_extra_lean_files_confined,'outside editable subtree')
    (fixture/'Outside.lean').unlink()
    (fixture/'FormalConjecturesBench/bad.bin').write_bytes(b'bad')
    rejects('non-Lean editable entry',c.check_editable_tree_shape,'non-Lean')
    (fixture/'FormalConjecturesBench/bad.bin').unlink()
    rejects('unchanged original sorry still banned',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(text)),'Banned Lean feature')
    # Frozen prefix/header unchanged, but a permitted ordinary helper def
    # changes resolution of Transcendental inside namespace Erdos247.
    (fixture/'FormalConjecturesBench/Submission.lean').write_text('import FormalConjectures.Util.ProblemImports\nnamespace Erdos247\ndef Transcendental (_K : Type) (_x : ℝ) : Prop := True\nend Erdos247\n')
    c.TARGET.write_text(text.replace('  sorry','  intro n hn h\n  trivial'))
    record('semantic attack retains exact frozen prefix and theorem header',lambda:c.check_frozen_prefix_and_header(c.TARGET.read_text()))
    record('semantic attack uses allowed source syntax',c.check_no_banned_patterns_in_editable_sources)
    record('semantic attack passes original shape/confined/frozen-file rules',lambda:(c.check_editable_tree_shape(),c.check_extra_lean_files_confined(),c.check_frozen_files_unchanged()))
    with c.make_fresh_golden_project() as tmp:
        p=Path(tmp)
        record('semantically shadowed theorem compiles',lambda:c.check_build(p))
        rejects('full type comparison rejects frozen-text name-shadow attack',lambda:c.check_golden_theorem_import(p),'Lean audit command failed')
        record('shadow attack itself has allowed axioms',lambda:c.check_axioms(p))
    rejects('actual main rejects semantic attack',c.main,'Lean audit command failed')
    c.TASK_DIR=original_task; c.TARGET=original_target
    # Only copies of the Spec are damaged. Neither can fall back to generation.
    for kind in ['missing','artifact_hash','manifest_hash']:
        bad=base/kind; shutil.copytree(original_spec,bad)
        c.SPEC_DIR=bad
        if kind=='missing': (bad/'FCBTrustedSpec.olean').unlink(); expected='Missing trusted Spec artifact'
        elif kind=='artifact_hash': (bad/'FCBTrustedSpec.olean').write_bytes(b'bad'); expected='artifact hash mismatch'
        else: (bad/'manifest.json').write_text('{}'); expected='manifest hash mismatch'
        before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in bad.iterdir()}
        rejects('fixed Spec '+kind+' fails closed',c.load_trusted_spec,expected)
        after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in bad.iterdir()}
        assert before==after,'runtime regenerated damaged Spec'
    c.SPEC_DIR=original_spec
print('ALL SUPPLEMENTAL TESTS PASSED',flush=True)
print(json.dumps({'checker':str(checker_path),'tests':results},indent=2),flush=True)
