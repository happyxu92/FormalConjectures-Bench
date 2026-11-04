import importlib.util, pathlib, tempfile, shutil, os, json, contextlib, io
P=pathlib.Path
s=importlib.util.spec_from_file_location('checker',os.environ.get('CHECKER_PATH','/tests/test_target.py'))
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
results={}
def reject(label,fn,contains):
    stream=io.StringIO()
    with contextlib.redirect_stderr(stream):
        try:fn()
        except SystemExit as e: assert e.code==1
        else:raise AssertionError(label+' was accepted')
    output=stream.getvalue();assert contains in output, output
    print(label+': REJECTED: '+output,flush=True);results[label]='rejected as expected'
def source_rules():
    t=c.target_text();c.check_banned_patterns(c.check_frozen_prefix_and_header(t))
    c.check_editable_tree_shape();c.check_no_banned_patterns_in_editable_sources()
    c.check_extra_lean_files_confined();c.check_frozen_files_unchanged()
c.load_trusted_spec()
with tempfile.TemporaryDirectory(prefix='fcb-firooz-refute-fixture-') as d:
    fixture=P(d);shutil.copytree(c.GOLDEN_ENV_DIR,fixture,dirs_exist_ok=True)
    c.TASK_DIR=fixture;c.TARGET=fixture/c.TARGET_REL
    original=c.TARGET.read_text()
    c.TARGET.write_text(original.replace('open Real','open Nat'))
    reject('frozen prefix',lambda:c.check_frozen_prefix_and_header(c.target_text()),'Code above')
    c.TARGET.write_text(original)
    (fixture/'Outside.lean').write_text('def outside : Nat := 0\n')
    reject('outside source',c.check_extra_lean_files_confined,'outside editable')
    (fixture/'Outside.lean').unlink()
    reject('original sorry source',source_rules,'Banned Lean feature')
    # Isolated placeholder fixture: deliberately bypass ONLY source gating to reach downstream functions.
    with c.make_fresh_golden_project() as tmp:
        q=P(tmp);c.check_trusted_type(q);results['trusted type audit']='passed'
        c.check_build(q);results['ubuntu candidate build']='passed'
        c.check_golden_theorem_import(q);results['complete original type']='passed'
        reject('target sorryAx audit',lambda:c.check_axioms(q),'sorryAx')
        c.check_sorry_canary(q);results['sorry canary']='passed'
        out=c.lean_output(q,'import FCBTrustedSpec\n#eval do\n  let r ← IO.Process.output {cmd := "/usr/bin/id", args := #["-un"]}\n  IO.println r.stdout\n')
        assert 'ubuntu' in out,out;results['compiler uid']='ubuntu'
    # Frozen text unchanged: a legal helper instance replaces real strict comparison.
    helper=fixture/'FormalConjecturesBench/Submission.lean'
    helper.write_text('import FormalConjectures.Util.ProblemImports\ninstance (priority := 1000000) refuteLt : LT ℝ := ⟨fun _ _ => False⟩\n')
    c.TARGET.write_text(original.replace('  sorry','  intro h\n  exact h 0'))
    source_rules();results['semantic negative source rules']='passed with frozen text unchanged'
    with c.make_fresh_golden_project() as tmp:
        q=P(tmp);c.check_build(q)
        c.check_axioms(q);results['semantic negative axiom audit']='passed (no sorry or new axioms)'
        reject('semantic instance type substitution',lambda:c.check_golden_theorem_import(q),'Type mismatch')
    # Same-named candidate artifacts and environment variables cannot replace the fixed Spec.
    cache=fixture/'.lake/build/lib/lean';cache.mkdir(parents=True)
    (cache/'FCBTrustedSpec.olean').write_bytes(b'forged candidate cache')
    (fixture/'FCBTrustedSpec.lean').write_text('def counterfeit : Nat := 42\n')
    os.environ['LEAN_PATH']=str(cache)
    os.environ['LEAN_SYSROOT']=str(cache)
    with c.make_fresh_golden_project() as tmp:
        q=P(tmp);(q/'FCBTrustedSpec.olean').write_bytes(b'forged same-name module')
        deps=c.run_lean(q,['--deps',str(q/c.TARGET_REL)])
        assert deps.returncode==0,deps.stdout
        assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in deps.stdout,deps.stdout
        assert str(cache) not in deps.stdout,deps.stdout
        c.check_trusted_type(q);results['candidate module/cache/environment shadow']='fixed Spec selected and audited'
    old=c.SPEC_DIR
    with tempfile.TemporaryDirectory(prefix='fcb-firooz-refute-bad-spec-') as b:
        bad=P(b);shutil.copytree(old,bad,dirs_exist_ok=True);c.SPEC_DIR=bad
        (bad/'FCBTrustedSpec.olean').unlink()
        reject('missing precompiled Spec',c.load_trusted_spec,'Missing trusted Spec artifact')
        assert not (bad/'FCBTrustedSpec.olean').exists()
        (bad/'FCBTrustedSpec.olean').write_bytes(b'corrupt')
        reject('corrupt precompiled Spec',c.load_trusted_spec,'hash mismatch')
        assert (bad/'FCBTrustedSpec.olean').read_bytes()==b'corrupt'
        c.SPEC_DIR=old
    c.load_trusted_spec()
print(json.dumps(results,indent=2),flush=True)
P('/tmp/fcb-firooz-refute-supplement-results.json').write_text(json.dumps(results,indent=2)+'\n')
