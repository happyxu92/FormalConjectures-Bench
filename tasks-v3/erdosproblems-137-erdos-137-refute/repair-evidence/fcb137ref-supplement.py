import importlib.util, os, hashlib, json, shutil, tempfile
from pathlib import Path
p=Path(os.environ.get('FCB_TESTS_DIR','/tests'))/'test_target.py'
s=importlib.util.spec_from_file_location('checker',p); c=importlib.util.module_from_spec(s); s.loader.exec_module(c)
def rejected(label,f):
    try: f()
    except SystemExit as e:
        assert e.code==1
        print('EXPECTED REJECTION:',label,flush=True)
    else: raise AssertionError('unexpected acceptance '+label)

def hashes(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '__pycache__' not in str(p)}
assert hashes(Path('/tests/trusted_spec'))==hashes(Path('/opt/formal-conjectures-bench-checker/trusted_spec'))
assert Path('/tests/test_target.py').read_bytes()==Path('/opt/formal-conjectures-bench-checker/test_target.py').read_bytes()
assert hashes(Path('/tests/golden_env'))==hashes(Path('/opt/formal-conjectures-bench-checker/golden_env'))
print('Both uploaded/preinstalled checker, golden and Spec packages match',flush=True)
c.load_trusted_spec()
with c.make_fresh_golden_project() as tmp:
    root=Path(tmp)
    c.check_trusted_type(root)
    # The proof is only an isolated fixture, never accepted or placed in /app.
    c.check_build(root)
    c.check_golden_theorem_import(root)
    rejected('placeholder target axiom audit',lambda:c.check_axioms(root))
    c.check_sorry_canary(root)
    print('sorry canary detected sorryAx',flush=True)
    # Candidate source and cached modules cannot replace the fixed import.
    (root/'FCBTrustedSpec.olean').write_bytes(b'forged candidate cache')
    forged=root/'.lake/build/lib/lean'; forged.mkdir(parents=True)
    (forged/'FCBTrustedSpec.olean').write_bytes(b'forged Lake cache')
    (root/'FCBTrustedSpec.lean').write_text('def ExpectedType := True\n')
    os.environ['LEAN_PATH']=str(forged)
    os.environ['LEAN_SYSROOT']=str(forged)
    c.check_trusted_type(root)
    c.check_golden_theorem_import(root)
    print('Candidate same-name module, Lake cache and environment cannot shadow Spec',flush=True)
# Test source restrictions through actual checker functions.
text=c.target_text()
c.check_frozen_prefix_and_header(text)
rejected('changed frozen prefix',lambda:c.check_frozen_prefix_and_header('--changed\n'+text))
rejected('changed theorem header',lambda:c.check_frozen_prefix_and_header(text.replace('∀ k ≥ 3','∀ k ≥ 4')))
rejected('missing assignment',lambda:c.check_frozen_prefix_and_header(text.replace(') := by',') by')))
for keyword in ['sorry','axiom bad : False','unsafe def bad := 0','notation "bad" => True']:
    rejected('source rule '+keyword,lambda k=keyword:c.check_banned_patterns(k))
original_task=c.TASK_DIR
with tempfile.TemporaryDirectory(prefix='fcb137ref-boundary-') as tmp:
    root=Path(tmp); shutil.copytree('/app/FormalConjecturesBench',root/'FormalConjecturesBench')
    c.TASK_DIR=root
    (root/'Outside.lean').write_text('def bad := 0')
    rejected('out-of-bounds Lean source',c.check_extra_lean_files_confined)
    (root/'FormalConjecturesBench/extra.txt').write_text('bad')
    rejected('non-Lean editable file',c.check_editable_tree_shape)
c.TASK_DIR=original_task
# Frozen text is identical, but helper name resolution changes the proposition.
with c.make_fresh_golden_project() as tmp:
    root=Path(tmp)
    helper=root/'FormalConjecturesBench/Submission.lean'
    helper.write_text('import FormalConjectures.Util.ProblemImports\ninstance (priority := 2000) : LE ℕ := ⟨fun _ _ => True⟩\n')
    candidate=text.replace('  sorry','  intro h\n  have hbad := h 0 True.intro 0\n  exact hbad (by simp [Nat.Powerful, Nat.Full])')
    body=c.check_frozen_prefix_and_header(candidate); c.check_banned_patterns(body)
    c.check_banned_patterns(helper.read_text())
    target=root/c.TARGET_REL
    target.write_text('import FCBTrustedSpec\nimport FormalConjecturesBench.Submission\nnamespace Erdos137\n'+c.MARKER+candidate.split(c.MARKER,1)[1])
    c.check_build(root)
    c.check_axioms(root)
    rejected('unchanged frozen text with instance-shadowed target type',lambda:c.check_golden_theorem_import(root))
# Corrupt and missing precompiled artifacts must fail, never regenerate.
original_spec=c.SPEC_DIR
for kind in ['missing','corrupt']:
    with tempfile.TemporaryDirectory(prefix='fcb137ref-artifact-') as tmp:
        q=Path(tmp)/'trusted_spec'; shutil.copytree(original_spec,q)
        artifact=q/'FCBTrustedSpec.olean'
        if kind=='missing': artifact.unlink()
        else: artifact.write_bytes(b'corrupt')
        before=set(q.iterdir()); c.SPEC_DIR=q
        rejected(kind+' precompiled artifact',c.load_trusted_spec)
        assert set(q.iterdir())==before
c.SPEC_DIR=original_spec
print('ALL SUPPLEMENTAL PATHS PASSED',flush=True)
