"""Exercise the delivered checker's functions, leaving production inputs untouched."""
import ast, contextlib, hashlib, importlib.util, io, json, os, shutil, tempfile
from pathlib import Path

checker_path=Path(os.environ.get('FCB_TESTS_DIR','/tests'))/'test_target.py'
spec=importlib.util.spec_from_file_location('checker',checker_path)
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
results=[]
def passed(label,fn):
 fn();results.append({'case':label,'result':'passed'});print('PASS',label,flush=True)
def reject(label,fn,needle):
 err=io.StringIO()
 try:
  with contextlib.redirect_stderr(err): fn()
 except SystemExit as e:
  assert e.code==1,(label,e.code)
  assert needle.lower() in err.getvalue().lower(),(label,err.getvalue())
 else: raise AssertionError('Accepted: '+label)
 results.append({'case':label,'result':'rejected','message':err.getvalue().strip()})
 print('PASS rejection:',label,flush=True)

assert c.SPEC_DIR==checker_path.parent/'trusted_spec'
ast.parse(checker_path.read_text())
passed('fixed artifact hash/version/dependency validation',c.load_trusted_spec)
with tempfile.TemporaryDirectory(prefix='fcb_validation_') as tmp:
 root=Path(tmp);root.chmod(0o755)
 fixture=root/'input';shutil.copytree(c.GOLDEN_ENV_DIR,fixture)
 c.TASK_DIR=fixture;c.TARGET=fixture/c.TARGET_REL
 original=c.target_text()
 passed('original frozen prefix and header',lambda:c.check_frozen_prefix_and_header(original))
 reject('frozen prefix mutation',lambda:c.check_frozen_prefix_and_header('-- mutation\n'+original),'Code above')
 reject('header mutation',lambda:c.check_frozen_prefix_and_header(original.replace('∃ k, 1 - ε ≤', '∃ k, 2 - ε ≤')),'header changed')
 reject('missing assignment',lambda:c.check_frozen_prefix_and_header(original.replace('.lowerDensity := by', '.lowerDensity by')),'proof assignment')
 reject('original sorry source policy',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(original)),'Banned Lean feature')
 passed('valid tree shape',c.check_editable_tree_shape)
 bad=fixture/'Outside.lean';bad.write_text('example : True := True.intro')
 reject('unconfined Lean file',c.check_extra_lean_files_confined,'outside editable subtree');bad.unlink()
 bad=fixture/c.EDITABLE_REL/'bad.txt';bad.write_text('bad')
 reject('non-Lean editable file',c.check_editable_tree_shape,'non-Lean');bad.unlink()
 bad=fixture/c.EDITABLE_REL/'bad.lean';bad.symlink_to(c.TARGET)
 reject('symlink',c.check_editable_tree_shape,'Symlinks');bad.unlink()
 passed('frozen files',c.check_frozen_files_unchanged)
 bad=fixture/'lean-toolchain';saved=bad.read_bytes();bad.write_text('bad')
 reject('changed frozen config',c.check_frozen_files_unchanged,'Trusted benchmark file was modified');bad.write_bytes(saved)
 helper=fixture/c.EDITABLE_REL/'Submission.lean';saved_helper=helper.read_text()
 helper.write_text('axiom bad : True')
 reject('helper axiom source ban',c.check_no_banned_patterns_in_editable_sources,'pattern');helper.write_text(saved_helper)
 # Ordinary helper declarations stay legal. Exclude the target placeholder only
 # for this direct source-policy test; the production check is unmodified.
 helper.write_text(saved_helper+'\nnamespace Fixture\ndef value : Nat := 0\nlemma value_eq : value = 0 := rfl\nstructure Box where\n  n : Nat\ninstance : Inhabited Box := ⟨⟨0⟩⟩\nend Fixture\n')
 c.TARGET.write_text(original.rsplit('  sorry',1)[0]+'  exact missing_proof\nend Erdos10\n')
 passed('ordinary def lemma and instance accepted',c.check_no_banned_patterns_in_editable_sources)
 c.TARGET.write_text(original)
 # Candidate caches and same-named sources cannot precede the fixed package.
 cache=fixture/'.lake/build/lib/lean';cache.mkdir(parents=True)
 (cache/'FCBTrustedSpec.olean').write_bytes(b'poison')
 (fixture/c.EDITABLE_REL/'FCBTrustedSpec.lean').write_text('def FCBTrustedSpec.ExpectedType : Prop := True\n')
 os.environ['LEAN_PATH']=str(cache)
 os.environ['LEAN_SYSROOT']='/invalid';os.environ['ELAN_TOOLCHAIN']='invalid'
 with c.make_fresh_golden_project() as temp_project:
  project=Path(temp_project)
  assert not (project/'.lake').exists()
  (project/'FCBTrustedSpec.olean').write_bytes(b'poison')
  passed('Spec import audit despite module/cache/env shadowing',lambda:c.check_trusted_type(project))
  passed('candidate compiled as ubuntu',lambda:c.check_build(project))
  passed('complete type comparison of placeholder fixture',lambda:c.check_golden_theorem_import(project))
  reject('placeholder theorem axiom audit',lambda:c.check_axioms(project),'sorryAx')
  passed('sorry canary',lambda:c.check_sorry_canary(project))
 helper.write_text('import FormalConjectures.Util.ProblemImports\ninstance (priority := 2000) : LE ℝ := ⟨fun _ _ => True⟩\n')
 passed('semantic attack keeps frozen text',lambda:c.check_frozen_prefix_and_header(c.target_text()))
 passed('semantic instance is source legal',lambda:c.check_banned_patterns(helper.read_text()))
 with c.make_fresh_golden_project() as temp_project:
  project=Path(temp_project)
  passed('semantic instance attack compiles',lambda:c.check_build(project))
  reject('semantic LE attack type mismatch',lambda:c.check_golden_theorem_import(project),'type mismatch')
 original_spec=c.SPEC_DIR
 for kind in ['missing','tampered','manifest']:
  package=root/kind;shutil.copytree(original_spec,package)
  if kind=='missing':(package/'FCBTrustedSpec.olean').unlink();needle='Missing trusted Spec artifact'
  elif kind=='tampered':(package/'FCBTrustedSpec.olean').write_bytes(b'bad');needle='artifact hash mismatch'
  else:(package/'manifest.json').write_text('{}');needle='manifest hash mismatch'
  before={str(p.relative_to(package)):p.read_bytes() for p in package.rglob('*') if p.is_file()}
  c.SPEC_DIR=package
  reject(kind+' precompiled package',c.load_trusted_spec,needle)
  after={str(p.relative_to(package)):p.read_bytes() for p in package.rglob('*') if p.is_file()}
  assert before==after,'Runtime changed package'
 c.SPEC_DIR=original_spec
 passed('original package restored',c.load_trusted_spec)
print(json.dumps({'uid':os.geteuid(),'checker':str(checker_path),'spec':str(c.SPEC_DIR),'results':results},indent=2),flush=True)
print('ALL CHECKS PASSED',flush=True)
