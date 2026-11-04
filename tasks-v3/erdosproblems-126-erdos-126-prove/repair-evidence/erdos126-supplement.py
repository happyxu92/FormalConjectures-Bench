import importlib.util, os, shutil, tempfile, hashlib, json
from pathlib import Path
os.environ['FCB_TESTS_DIR']='/tests'
os.environ['FCB_TASK_DIR']='/app'
spec=importlib.util.spec_from_file_location('checker','/tests/test_target.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
def reject(label, fn):
    try: fn()
    except SystemExit as e:
        assert e.code == 1
        print('PASS rejected:',label,flush=True)
    else: raise AssertionError('accepted '+label)
c.load_trusted_spec()
original=c.target_text()
c.check_frozen_prefix_and_header(original)
reject('frozen prefix',lambda:c.check_frozen_prefix_and_header(original.replace('open Filter','open Set')))
reject('changed header',lambda:c.check_frozen_prefix_and_header(original.replace('theorem erdos_126','theorem bad')))
reject('missing assignment',lambda:c.check_frozen_prefix_and_header(original.replace(':= by\n  sorry', 'by\n  sorry')))
reject('original sorry source',lambda:c.check_banned_patterns(c.check_frozen_prefix_and_header(original)))
for local in ['/tests','/opt/formal-conjectures-bench-checker']:
    c.SPEC_DIR=Path(local)/'trusted_spec'; c.GOLDEN_ENV_DIR=Path(local)/'golden_env'
    c.load_trusted_spec()
    with c.make_fresh_golden_project() as name:
        p=Path(name)
        c.check_trusted_type(p)
        c.check_build(p)
        c.check_golden_theorem_import(p)
        reject(local+' target sorryAx',lambda:c.check_axioms(p))
        c.check_sorry_canary(p)
        print('PASS',local,'Spec audit, ubuntu build, full type, sorryAx rejection, canary',flush=True)
c.SPEC_DIR=Path('/tests/trusted_spec');c.GOLDEN_ENV_DIR=Path('/tests/golden_env')
# Fully source-compliant semantic attack: only a normal helper definition;
# target's frozen prefix and literal theorem header remain byte-for-byte.
with tempfile.TemporaryDirectory(prefix='erdos126-negative-') as d:
    candidate=Path(d)
    shutil.copytree('/app/FormalConjecturesBench',candidate/'FormalConjecturesBench')
    for rel in c.FROZEN_FILES:
        (candidate/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(c.GOLDEN_ENV_DIR/rel,candidate/rel)
    helper=candidate/'FormalConjecturesBench/Submission.lean'
    helper.write_text('import FormalConjectures.Util.ProblemImports\nnamespace Erdos126\ndef Tendsto {α β : Type*} (_ : α → β) (_ : Filter α) (_ : Filter β) : Prop := True\nend Erdos126\n')
    target=candidate/c.TARGET_REL
    attack=original.replace('by\n  sorry','by\n  intro f hf\n  trivial')
    target.write_text(attack)
    c.TASK_DIR=candidate;c.TARGET=target
    c.check_frozen_prefix_and_header(attack)
    c.check_banned_patterns(c.check_frozen_prefix_and_header(attack))
    c.check_editable_tree_shape();c.check_no_banned_patterns_in_editable_sources()
    c.check_extra_lean_files_confined();c.check_frozen_files_unchanged()
    print('PASS semantic negative unchanged frozen text and allowed syntax',flush=True)
    with c.make_fresh_golden_project() as name:
        p=Path(name);c.check_build(p)
        # Attack theorem is genuinely proved without sorry/new axioms.
        c.check_axioms(p)
        reject('shadowed Tendsto full theorem type',lambda:c.check_golden_theorem_import(p))
    (candidate/'Outside.lean').write_text('def outside := 1\n')
    reject('out-of-bounds Lean source',c.check_extra_lean_files_confined)
    (candidate/'Outside.lean').unlink()
    # A same-name compiled candidate cache cannot replace fixed Spec.
    with c.make_fresh_golden_project() as name:
        p=Path(name)
        fake=p/'.lake/build/lib/lean';fake.mkdir(parents=True)
        source=fake/'FCBTrustedSpec.lean';source.write_text('def FCBTrustedSpec.ExpectedType : Prop := True\n')
        import pwd
        u=pwd.getpwnam('ubuntu')
        for f in [p/'.lake',p/'.lake/build',p/'.lake/build/lib',fake,source]:os.chown(f,u.pw_uid,u.pw_gid)
        r=c.run_lean(fake,['-o',str(fake/'FCBTrustedSpec.olean'),str(source)])
        assert r.returncode==0,r.stdout
        os.environ['LEAN_PATH']=str(fake)
        os.environ['FCB_DEPENDENCY_PACKAGES']=str(fake)
        probe=p/'Probe.lean';probe.write_text('import FCBTrustedSpec\n')
        r=c.run_lean(p,['--deps',str(probe)])
        assert r.returncode==0,r.stdout
        assert '/tests/trusted_spec/FCBTrustedSpec.olean' in r.stdout,r.stdout
        assert str(fake/'FCBTrustedSpec.olean') not in r.stdout,r.stdout
        c.check_trusted_type(p)
        print('PASS same-name candidate cache and hostile env cannot replace Spec',flush=True)
c.TASK_DIR=Path('/app');c.TARGET=Path('/app')/c.TARGET_REL
# Corruption and absence never invoke generation, even with source still there.
with tempfile.TemporaryDirectory(prefix='erdos126-spec-fail-') as d:
    p=Path(d);shutil.copytree('/tests/trusted_spec',p/'trusted_spec')
    c.SPEC_DIR=p/'trusted_spec'
    artifact=c.SPEC_DIR/'FCBTrustedSpec.olean';saved=artifact.read_bytes()
    artifact.unlink();reject('missing precompiled artifact',c.load_trusted_spec)
    assert not artifact.exists()
    artifact.write_bytes(saved+b'corrupt');reject('corrupt artifact',c.load_trusted_spec)
    assert artifact.read_bytes()==saved+b'corrupt'
print('ALL SUPPLEMENTAL PATHS PASSED',flush=True)
