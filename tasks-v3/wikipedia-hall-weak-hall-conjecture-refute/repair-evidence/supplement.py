import importlib.util, os, shutil, tempfile, json
from pathlib import Path
spec=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
results=[]
def rejected(label, fn):
    try: fn()
    except SystemExit as e:
        assert e.code==1
        results.append(label+': rejected')
    else: raise AssertionError(label+' unexpectedly accepted')
def passed(label, fn):
    fn(); results.append(label+': passed')
passed('fixed /tests Spec manifest artifacts version inputs',m.load_trusted_spec)
with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    passed('independent type and transitive prefix axiom audit',lambda:m.check_trusted_type(p))
    passed('ubuntu candidate build (isolated sorry fixture only)',lambda:m.check_build(p))
    passed('complete original type comparison',lambda:m.check_golden_theorem_import(p))
    rejected('target axiom audit detects fixture sorryAx',lambda:m.check_axioms(p))
    passed('sorry canary',lambda:m.check_sorry_canary(p))
    # Candidate lookalike module/cache plus hostile environment overrides cannot replace Spec.
    (p/'FCBTrustedSpec.lean').write_text('def FCBTrustedSpec.ExpectedType := True\n')
    (p/'FCBTrustedSpec.olean').write_bytes(b'not a Lean module')
    (p/'.lake/build/lib/lean').mkdir(parents=True)
    (p/'.lake/build/lib/lean/FCBTrustedSpec.olean').write_bytes(b'not a Lean module')
    os.environ['LEAN_PATH']=str(p); os.environ['LEAN_SYSROOT']=str(p)
    deps=m.run_lean(p,['--deps',str(p/m.TARGET_REL)])
    assert deps.returncode==0 and str(m.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout
    passed('candidate same-name source/cache and environment cannot replace fixed Spec',lambda:m.check_golden_theorem_import(p))
    # Ordinary helper import remains usable.
    helper=p/'FormalConjecturesBench/Submission.lean'
    helper.write_text('import Mathlib.Data.Real.Basic\nnoncomputable instance (priority := 2000) : Inv ℝ := ⟨fun _ => 0⟩\n')
    m.check_banned_patterns(helper.read_text())
    # Frozen public text remains byte-identical in this semantic attack.
    public=Path('/app/FormalConjecturesBench/Target.lean').read_text()
    m.check_frozen_prefix_and_header(public)
    passed('semantic instance attack fixture compiles',lambda:m.check_build(p))
    rejected('full type comparison rejects changed inverse instance with unchanged frozen text',lambda:m.check_golden_theorem_import(p))
with tempfile.TemporaryDirectory(prefix='hall-refute-negative-') as tmp:
    p=Path(tmp); shutil.copytree('/app',p,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.lake'))
    old_task,old_target=m.TASK_DIR,m.TARGET
    m.TASK_DIR=p;m.TARGET=p/m.TARGET_REL
    text=m.target_text()
    rejected('frozen prefix mutation',lambda:m.check_frozen_prefix_and_header(text.replace('open Real','open Real\n-- changed',1)))
    rejected('header mutation',lambda:m.check_frozen_prefix_and_header(text.replace('¬ (','( ',1)))
    (p/'Outside.lean').write_text('example : True := True.intro\n')
    rejected('out-of-tree Lean source',m.check_extra_lean_files_confined)
    (p/'Outside.lean').unlink()
    (p/'FormalConjecturesBench/Submission.lean').write_text('axiom hacked : False\n')
    rejected('banned helper axiom',m.check_no_banned_patterns_in_editable_sources)
    m.TASK_DIR,m.TARGET=old_task,old_target
for corruption in ['missing','hash']:
    with tempfile.TemporaryDirectory(prefix='hall-refute-package-') as tmp:
        p=Path(tmp);shutil.copytree(m.SPEC_DIR,p,dirs_exist_ok=True)
        if corruption=='missing':(p/'FCBTrustedSpec.olean').unlink()
        else:(p/'FCBTrustedSpec.olean').write_bytes(b'corrupt')
        old=m.SPEC_DIR;m.SPEC_DIR=p
        rejected('precompiled artifact '+corruption+' fails without regeneration',m.load_trusted_spec)
        assert (p/'FCBTrustedSpec.olean').exists()==(corruption!='missing')
        m.SPEC_DIR=old
m.SPEC_DIR=Path('/opt/formal-conjectures-bench-checker/trusted_spec')
m.GOLDEN_ENV_DIR=Path('/opt/formal-conjectures-bench-checker/golden_env')
passed('local /opt package fixed artifact load',m.load_trusted_spec)
print(json.dumps(results,ensure_ascii=False,indent=2))
