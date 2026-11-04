from pathlib import Path
import importlib.util
s=importlib.util.spec_from_file_location('c','/opt/formal-conjectures-bench-checker/test_target.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
assert str(c.SPEC_DIR)=='/opt/formal-conjectures-bench-checker/trusted_spec'
c.load_trusted_spec()
with c.make_fresh_golden_project() as d:
 p=Path(d)
 c.check_trusted_type(p)
 c.check_build(p)
 c.check_golden_theorem_import(p)
 try:c.check_axioms(p)
 except SystemExit as e: assert e.code==1
 else:raise AssertionError('sorry audit must reject')
 c.check_sorry_canary(p)
 # Ordinary standard dependency imports and helper declarations remain allowed.
 helper=p/'FormalConjecturesBench/Submission.lean'
 helper.write_text('import Mathlib.Data.Nat.Basic\nlemma ordinary_helper : (1 : ℕ) = 1 := rfl\n')
 c.check_banned_patterns(helper.read_text())
 c.check_build(p)
 c.check_golden_theorem_import(p)
print('LOCAL FIXED SPEC AND NORMAL IMPORT PATHS PASSED')
