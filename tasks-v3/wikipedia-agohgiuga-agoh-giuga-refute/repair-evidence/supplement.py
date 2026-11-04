import importlib.util, os, shutil, tempfile, hashlib
from pathlib import Path
os.environ['FCB_TESTS_DIR']='/tests'
s=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)

def reject(label,fn):
 try: fn()
 except SystemExit as e:
  assert e.code==1
  print('EXPECTED REJECTION:',label,flush=True)
 else: raise AssertionError('accepted '+label)

assert os.getuid()==1000
print('actual supplemental user uid:',os.getuid(),flush=True)
c.check_frozen_prefix_and_header(c.target_text())
c.check_editable_tree_shape();c.check_extra_lean_files_confined();c.check_frozen_files_unchanged()
reject('original sorry source',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(c.target_text())))
reject('changed frozen prefix',lambda:c.check_frozen_prefix_and_header('changed\n'+c.target_text()))
reject('changed target header',lambda:c.check_frozen_prefix_and_header(c.target_text().replace('¬ (','True ∧ (')))
reject('axiom source restriction',lambda:c.check_banned_patterns('by trivial\naxiom bad : False'))
c.load_trusted_spec()
with c.make_fresh_golden_project() as tmp:
 p=Path(tmp)
 c.check_trusted_type(p)
 c.check_build(p)
 c.check_golden_theorem_import(p)
 reject('placeholder theorem sorryAx audit',lambda:c.check_axioms(p))
 c.check_sorry_canary(p)
 print('SORRY CANARY PASS',flush=True)
 # Fixture-only local-name shadowing: retain the exact frozen theorem header.
 # Not a proposed solution; no changes to /app or trusted golden inputs.
 target=p/c.TARGET_REL
 baseline=target.read_text()
 target.write_text(baseline.replace('namespace AgohGiuga\n','namespace AgohGiuga\nvariable (AgohGiugaCongr : Prop)\n'))
 assert c.EXPECTED_HEADER in target.read_text()
 c.check_build(p)
 reject('unchanged header, locally shadowed AgohGiugaCongr has an extra full-type parameter',lambda:c.check_golden_theorem_import(p))
 target.write_text(baseline)
 c.check_build(p)
 # Same-name candidate source/cache plus hostile environment cannot mask the trusted Spec.
 (p/'FCBTrustedSpec.lean').write_text('def bogus : Prop := True\n')
 fake=p/'.lake/build/lib/lean';fake.mkdir(parents=True)
 (fake/'FCBTrustedSpec.olean').write_bytes(b'not a trusted module')
 os.environ['LEAN_PATH']=str(fake)
 os.environ['LEAN_SYSROOT']=str(p)
 result=c.run_lean(p,['--deps',str(target)])
 assert result.returncode==0,result.stdout
 assert str(c.SPEC_DIR/'FCBTrustedSpec.olean') in result.stdout,result.stdout
 assert str(fake/'FCBTrustedSpec.olean') not in result.stdout
 c.check_golden_theorem_import(p)
 print('SAME-NAME SOURCE/CACHE AND ENV OVERRIDE TEST PASS\n'+result.stdout,flush=True)
 # Actual source confinement function, isolated candidate checkout.
 original_task=c.TASK_DIR
 c.TASK_DIR=p
 reject('extra source outside editable subtree',c.check_extra_lean_files_confined)
 c.TASK_DIR=original_task
original_spec=c.SPEC_DIR
with tempfile.TemporaryDirectory(prefix='agoh_refute_corrupt_') as t:
 q=Path(t)/'spec';shutil.copytree(original_spec,q)
 c.SPEC_DIR=q
 artifact=q/'FCBTrustedSpec.olean'
 artifact.unlink()
 reject('missing precompiled Spec fails closed',c.load_trusted_spec)
 assert not artifact.exists(),'runtime regenerated Spec'
 artifact.write_bytes(b'corrupt')
 reject('corrupt precompiled Spec hash fails closed',c.load_trusted_spec)
 assert artifact.read_bytes()==b'corrupt','runtime regenerated Spec'
 c.SPEC_DIR=original_spec
c.load_trusted_spec()
print('ALL SUPPLEMENTAL PATHS PASS',flush=True)
