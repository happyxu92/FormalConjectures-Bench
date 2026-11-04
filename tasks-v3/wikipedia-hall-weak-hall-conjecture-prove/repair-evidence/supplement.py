import importlib.util, os, tempfile, shutil, json, hashlib
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
os.environ.setdefault('FCB_TESTS_DIR','/tests')
s=importlib.util.spec_from_file_location('checker',str(Path(os.environ['FCB_TESTS_DIR'])/'test_target.py'))
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
results=[]
def exercise(name, f, reject=False, contains=None):
    import contextlib,io
    out=io.StringIO()
    try:
        with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out): f()
        rejected=False
    except SystemExit as e:
        assert e.code==1,(name,e)
        rejected=True
    message=out.getvalue()
    print('===',name,'===\n',message,flush=True)
    assert rejected==reject,(name,rejected,reject)
    if contains: assert contains in message,(name,message,contains)
    results.append({'name':name,'rejected':rejected,'log':message})

exercise('fixed_spec_manifest_and_artifacts',m.load_trusted_spec)
text=m.target_text()
exercise('original_frozen_header',lambda:m.check_frozen_prefix_and_header(text))
exercise('frozen_edit',lambda:m.check_frozen_prefix_and_header(text.replace('open Real','open Real -- changed')),True,'above')
exercise('header_edit',lambda:m.check_frozen_prefix_and_header(text.replace('theorem weak_hall_conjecture','theorem wrong')),True,'header')
exercise('sorry_source',lambda:m.check_banned_patterns(m.check_frozen_prefix_and_header(text)),True,'Banned')
exercise('original_frozen_files',m.check_frozen_files_unchanged)
exercise('original_tree',m.check_editable_tree_shape)
exercise('original_source_confinement',m.check_extra_lean_files_confined)
with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    exercise('trusted_type_transitive_audit',lambda:m.check_trusted_type(p))
    # Original sorry is intentionally retained only in this isolated fixture.
    exercise('ubuntu_candidate_compile',lambda:m.check_build(p))
    exercise('full_type_match',lambda:m.check_golden_theorem_import(p))
    exercise('target_sorry_axiom_rejected',lambda:m.check_axioms(p),True,'sorryAx')
    exercise('sorry_canary',lambda:m.check_sorry_canary(p))
    # A same-name candidate cache/module cannot replace the trusted .olean.
    (p/'FCBTrustedSpec.olean').write_bytes(b'not a Lean module')
    (p/'FCBTrustedSpec.lean').write_text('def malicious : True := True.intro\n')
    (p/'.lake/build/lib/lean').mkdir(parents=True)
    (p/'.lake/build/lib/lean/FCBTrustedSpec.olean').write_bytes(b'not a Lean module')
    os.environ['LEAN_PATH']=str(p)
    os.environ['LEAN_SYSROOT']=str(p)
    dep=m.run_lean(p,['--deps',str(p/m.TARGET_REL)])
    assert dep.returncode==0,dep.stdout
    resolved=str(m.SPEC_DIR/'FCBTrustedSpec.olean')
    assert resolved in dep.stdout,dep.stdout
    print('fixed_spec_resolution:\n'+dep.stdout,flush=True)
    exercise('same_name_module_cache_environment_cannot_shadow',lambda:m.check_golden_theorem_import(p))

with m.make_fresh_golden_project() as tmp:
    p=Path(tmp)
    sub=p/'FormalConjecturesBench/Submission.lean'
    sub.write_text('import FormalConjectures.Util.ProblemImports\n'
        'instance (priority := 1000000) : HSub ℝ ℝ ℝ := ⟨fun _ _ => 0⟩\n')
    # All frozen text, including the theorem header, remains byte-for-byte original.
    exercise('semantic_attack_original_header_unchanged',lambda:m.check_frozen_prefix_and_header(text))
    exercise('semantic_attack_allowed_source_syntax',lambda:m.check_banned_patterns(sub.read_text()))
    exercise('semantic_attack_compiles',lambda:m.check_build(p))
    exercise('semantic_instance_full_type_rejected',lambda:m.check_golden_theorem_import(p),True,'Type mismatch')

original_task=m.TASK_DIR
with tempfile.TemporaryDirectory(prefix='hall-prove-confinement-') as tmp:
    m.TASK_DIR=Path(tmp)
    (m.TASK_DIR/'Escape.lean').write_text('theorem escape : True := by trivial\n')
    exercise('out_of_tree_lean_rejected',m.check_extra_lean_files_confined,True,'outside editable')
m.TASK_DIR=original_task
original_spec=m.SPEC_DIR
for mode in ['missing','corrupt']:
    with tempfile.TemporaryDirectory(prefix='hall-prove-artifact-') as tmp:
        m.SPEC_DIR=Path(tmp)/'trusted_spec'
        shutil.copytree(original_spec,m.SPEC_DIR)
        olean=m.SPEC_DIR/'FCBTrustedSpec.olean'
        if mode=='missing': olean.unlink()
        else: olean.write_bytes(b'corrupt')
        exercise('spec_'+mode+'_fails_without_regeneration',m.load_trusted_spec,True,
                 'Missing trusted Spec artifact' if mode=='missing' else 'artifact hash mismatch')
        assert (not olean.exists()) if mode=='missing' else olean.read_bytes()==b'corrupt'
m.SPEC_DIR=original_spec
suffix='local' if str(m.TESTS_DIR).startswith('/opt') else 'official'
Path(f'/tmp/hall-prove-supplement-{suffix}-results.json').write_text(json.dumps(results,indent=2))
print('ALL SUPPLEMENTAL ASSERTIONS PASSED',flush=True)
