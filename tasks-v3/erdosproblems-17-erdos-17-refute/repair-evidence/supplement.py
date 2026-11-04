from pathlib import Path
import importlib.util, os, shutil, tempfile, contextlib, io
os.environ.setdefault('FCB_TASK_DIR','/app')
os.environ.setdefault('FCB_TESTS_DIR','/tests')
s=importlib.util.spec_from_file_location('checker',str(Path(os.environ['FCB_TESTS_DIR'])/'test_target.py')); c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
def reject(label,fn,part):
    out=io.StringIO()
    with contextlib.redirect_stderr(out):
        try:fn()
        except SystemExit as e:assert e.code==1
        else:raise AssertionError(label+' accepted')
    assert part in out.getvalue(),out.getvalue()
    print('PASS expected rejection',label,':',out.getvalue().strip(),flush=True)
c.load_trusted_spec()
text=c.target_text()
c.check_frozen_prefix_and_header(text)
reject('frozen prefix',lambda:c.check_frozen_prefix_and_header('-- changed\n'+text),'above the benchmark')
reject('header',lambda:c.check_frozen_prefix_and_header(text.replace(c.EXPECTED_HEADER,c.EXPECTED_HEADER+' → True')),'proof assignment')
reject('source sorry',lambda:c.check_banned_patterns(' by sorry'),'Banned Lean feature')
with c.make_fresh_golden_project() as t:
    p=Path(t)
    c.check_trusted_type(p)
    c.check_build(p)
    c.check_golden_theorem_import(p)
    reject('target sorry axiom audit',lambda:c.check_axioms(p),'sorryAx')
    c.check_sorry_canary(p)
    print('PASS sorry canary',flush=True)
    # Neither a same-name source nor a candidate build cache can replace Spec.
    (p/'FCBTrustedSpec.lean').write_text('def hacked := True\n')
    cache=p/'.lake/build/lib/lean';cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'not a trusted module')
    (p/'FCBTrustedSpec.olean').write_bytes(b'not a trusted module')
    r=c.run_lean(p,['--deps',str(p/c.TARGET_REL)])
    assert r.returncode==0,r.stdout
    assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in r.stdout,r.stdout
    assert str(cache/'FCBTrustedSpec.olean') not in r.stdout
    c.check_trusted_type(p)
    c.check_golden_theorem_import(p)
    print('PASS same-name candidate source/cache cannot shadow fixed Spec',flush=True)
# Confinement against isolated copies, never edit /app or formal inputs.
with tempfile.TemporaryDirectory(prefix='ep17r-fixture-') as t:
    p=Path(t);shutil.copytree('/app/FormalConjecturesBench',p/'FormalConjecturesBench')
    saved=c.TASK_DIR;c.TASK_DIR=p
    (p/'Outside.lean').write_text('def x := True\n')
    reject('out-of-tree source',c.check_extra_lean_files_confined,'outside editable')
    (p/'Outside.lean').unlink()
    (p/'FormalConjecturesBench/x.txt').write_text('x')
    reject('non-Lean editable file',c.check_editable_tree_shape,'non-Lean file')
    c.TASK_DIR=saved
# Semantic attack: a meta-def attribute hooks set-builder elaboration,
# substituting a named predicate (Hacker.IsClusterPrime) without changing text.
# Frozen prefix and exact header remain unchanged; only helper/proof change.
with tempfile.TemporaryDirectory(prefix='ep17r-semantic-') as t:
    fixture=Path(t);shutil.copytree('/app/FormalConjecturesBench',fixture/'FormalConjecturesBench')
    target=fixture/c.TARGET_REL
    target.write_text(text.replace('by\n  sorry','by\n  change ¬ Set.Infinite (∅ : Set ℕ)\n  exact Set.finite_empty.not_infinite'))
    (fixture/'FormalConjecturesBench/Submission.lean').write_text('''import FCBTrustedSpec
namespace Hacker
def IsClusterPrime (_ : ℕ) : Prop := False
def fakeSet : Set ℕ := fun p => IsClusterPrime p
@[term_elab Mathlib.Meta.setBuilder]
meta def shadowName : Lean.Elab.Term.TermElab := fun _ _ => do
  return Lean.mkConst `Hacker.fakeSet
end Hacker
''')
    saved=c.TASK_DIR;c.TASK_DIR=fixture
    c.check_frozen_prefix_and_header(target.read_text())
    c.check_no_banned_patterns_in_editable_sources()
    with c.make_fresh_golden_project() as t2:
        p=Path(t2);c.check_build(p)
        # Type actually changed, with no placeholder proof.
        print(c.lean_output(p,'import FormalConjecturesBench.Target\n#print '+c.THEOREM_NAME+'\n'))
        c.check_axioms(p)
        reject('semantic name substitution full type check',lambda:c.check_golden_theorem_import(p),'Lean audit command failed')
    c.TASK_DIR=saved
# Missing/corrupt package must fail before Lean, without refreshing anything.
original=c.SPEC_DIR
for damage in ['missing','corrupt']:
    with tempfile.TemporaryDirectory(prefix='ep17r-damage-') as t:
        pkg=Path(t)/'trusted_spec';shutil.copytree(original,pkg)
        f=pkg/'FCBTrustedSpec.olean'
        if damage=='missing':f.unlink()
        else:f.write_bytes(b'corrupted')
        before={str(x.relative_to(pkg)):x.read_bytes() for x in pkg.rglob('*') if x.is_file()}
        c.SPEC_DIR=pkg
        reject(damage+' Spec',c.load_trusted_spec,'Spec artifact')
        after={str(x.relative_to(pkg)):x.read_bytes() for x in pkg.rglob('*') if x.is_file()}
        assert before==after
c.SPEC_DIR=original
print('ALL SUPPLEMENTARY CHECKS PASSED',flush=True)
