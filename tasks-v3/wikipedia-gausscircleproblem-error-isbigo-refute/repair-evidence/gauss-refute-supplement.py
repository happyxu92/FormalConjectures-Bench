"""Isolated fixture tests calling the delivered checker's actual functions."""
import importlib.util, os, json, shutil, tempfile, hashlib
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
os.environ['FCB_TESTS_DIR']='/tests'
# Inherited candidate hints must be ignored even when present at checker import.
os.environ['LEAN_PATH']='/tmp/fcb-gauss-untrusted-before-import'
os.environ['LEAN_SYSROOT']='/tmp/fcb-gauss-untrusted-before-import'
os.environ['ELAN_TOOLCHAIN']='fcb-gauss-nonexistent-toolchain'
spec=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
results={}
def ok(name, fn):
    fn(); results[name]='passed'; print('PASS',name,flush=True)
def rejects(name, fn):
    try: fn()
    except SystemExit as e:
        assert e.code != 0
        results[name]='rejected'; print('REJECTED',name,flush=True)
    else: raise AssertionError('unexpected acceptance: '+name)
# Hash parity for uploaded /tests and image-installed local checker inputs.
local=Path('/opt/formal-conjectures-bench-checker')
assert (Path('/tests/test_target.py').read_bytes()==(local/'test_target.py').read_bytes())
for base in ['trusted_spec','golden_env']:
    for p in (Path('/tests')/base).rglob('*'):
        if p.is_file(): assert p.read_bytes()==(local/base/p.relative_to(Path('/tests')/base)).read_bytes(),p
print('PASS /tests and /opt byte parity',flush=True)
original=c.target_text()
ok('original frozen header',lambda:c.check_frozen_prefix_and_header(original))
rejects('frozen prefix mutation',lambda:c.check_frozen_prefix_and_header('-- changed\n'+original))
rejects('header mutation',lambda:c.check_frozen_prefix_and_header(original.replace('theorem formal_conjectures_bench_refutation','theorem bad')))
rejects('missing assignment',lambda:c.check_frozen_prefix_and_header(original.replace(':= by\n  sorry\n\nend GaussCircleProblem', 'by\n  sorry\n\nend GaussCircleProblem')))
ok('manifest/artifact/version validation',c.load_trusted_spec)
with c.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    ok('precompiled Spec independent import and transitive type audit',lambda:c.check_trusted_type(p))
    ok('baseline ubuntu build (isolated original sorry fixture)',lambda:c.check_build(p))
    ok('baseline complete type comparison',lambda:c.check_golden_theorem_import(p))
    rejects('baseline target sorryAx audit',lambda:c.check_axioms(p))
    ok('sorry canary',lambda:c.check_sorry_canary(p))
    # A candidate cache and root module with the same name must not replace Spec.
    shutil.copy2('/tests/trusted_spec/FCBTrustedSpec.olean',p/'FCBTrustedSpec.olean')
    (p/'FCBTrustedSpec.olean').write_bytes(b'corrupt candidate shadow')
    (p/'FCBTrustedSpec.lean').write_text('axiom forged : False\n')
    (p/'.lake/build/lib/lean').mkdir(parents=True)
    (p/'.lake/build/lib/lean/FCBTrustedSpec.olean').write_bytes(b'candidate cache')
    os.environ['LEAN_PATH']=str(p)
    os.environ['LEAN_SYSROOT']=str(p)
    ok('same-name candidate module/cache and environment cannot shadow trusted Spec',lambda:c.check_trusted_type(p))
    ok('same-name shadow cannot change full comparison',lambda:c.check_golden_theorem_import(p))
# Ordinary external precompiled imports are still allowed, without a directory whitelist.
with tempfile.TemporaryDirectory(prefix='fcb-gauss-refute-external-') as tmp:
    ext=Path(tmp)
    if os.geteuid()==0:
        import pwd
        u=pwd.getpwnam('ubuntu'); os.chown(ext,u.pw_uid,u.pw_gid)
    (ext/'NormalExtra.lean').write_text('def normalExtra : Nat := 7\n')
    result=c.run_lean(ext,['-o',str(ext/'NormalExtra.olean'),str(ext/'NormalExtra.lean')])
    assert result.returncode==0,result.stdout
    saved_paths=c.CANDIDATE_IMPORT_PATHS
    c.CANDIDATE_IMPORT_PATHS=str(ext)
    with c.make_fresh_golden_project() as tmp_project:
        ok('normal external precompiled import remains allowed',lambda:c.lean_output(Path(tmp_project),'import FCBTrustedSpec\nimport NormalExtra\nexample : normalExtra = 7 := rfl\n'))
    c.CANDIDATE_IMPORT_PATHS=saved_paths
# Isolate source-rule checks without modifying /app.
with tempfile.TemporaryDirectory(prefix='fcb-gauss-rules-') as fixture:
    task=Path(fixture)
    shutil.copytree('/tests/golden_env',task,dirs_exist_ok=True)
    saved_task,saved_target=c.TASK_DIR,c.TARGET
    c.TASK_DIR=task; c.TARGET=task/c.TARGET_REL
    (task/'Outside.lean').write_text('def x := 1\n')
    rejects('out-of-scope source',c.check_extra_lean_files_confined)
    (task/'Outside.lean').unlink()
    (task/'FormalConjecturesBench/Submission.lean').write_text('axiom forged : False\n')
    rejects('banned helper declaration',c.check_no_banned_patterns_in_editable_sources)
    # The public prefix/header is byte-for-byte unchanged. Normal helper def
    # changes name resolution of Tendsto. A sorry fixture is used only to reach
    # the type check; no source guard or axiom audit is disabled in production.
    helper='''import FormalConjectures.Util.ProblemImports
namespace GaussCircleProblem
def Tendsto (_ : ℝ → ℝ) (_ _ : Filter ℝ) : Prop := True
end GaussCircleProblem
'''
    (task/'FormalConjecturesBench/Submission.lean').write_text(helper)
    ok('semantic fixture helper passes original syntax rules',lambda:c.check_banned_patterns(helper))
    ok('semantic fixture frozen header unchanged',lambda:c.check_frozen_prefix_and_header(c.target_text()))
    with c.make_fresh_golden_project() as tmp:
        p=Path(tmp)
        ok('semantic fixture ubuntu compile',lambda:c.check_build(p))
        rejects('semantic Tendsto shadow full-type comparison',lambda:c.check_golden_theorem_import(p))
    c.TASK_DIR,c.TARGET=saved_task,saved_target
# Missing/corrupt artifacts fail, with no rebuild or source fallback.
saved=c.SPEC_DIR
for case in ['missing','corrupt']:
    with tempfile.TemporaryDirectory(prefix='fcb-gauss-spec-negative-') as tmp:
        p=Path(tmp); shutil.copytree(saved,p,dirs_exist_ok=True)
        artifact=p/'FCBTrustedSpec.olean'
        if case=='missing': artifact.unlink()
        else: artifact.write_bytes(b'corrupt')
        c.SPEC_DIR=p
        rejects(case+' precompiled artifact',c.load_trusted_spec)
        if case=='missing': assert not artifact.exists()
        else: assert artifact.read_bytes()==b'corrupt'
c.SPEC_DIR=saved
Path('/tmp/fcb-gauss-refute-supplement-result.json').write_text(json.dumps(results,indent=2)+'\n')
print('ALL SUPPLEMENTAL PATHS COVERED',flush=True)
