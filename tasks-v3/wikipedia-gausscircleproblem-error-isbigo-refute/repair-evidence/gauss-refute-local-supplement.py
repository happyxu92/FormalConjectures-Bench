import os, importlib.util
from pathlib import Path
os.environ['FCB_TASK_DIR']='/app'
os.environ['FCB_TESTS_DIR']='/opt/formal-conjectures-bench-checker'
s=importlib.util.spec_from_file_location('local_checker','/opt/formal-conjectures-bench-checker/test_target.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
assert str(c.SPEC_DIR)=='/opt/formal-conjectures-bench-checker/trusted_spec'
c.load_trusted_spec()
with c.make_fresh_golden_project() as tmp:
 p=Path(tmp)
 c.check_trusted_type(p)
 c.check_build(p)
 c.check_golden_theorem_import(p)
 try:c.check_axioms(p)
 except SystemExit as e:assert e.code==1
 else:raise AssertionError('sorryAx audit accepted')
 c.check_sorry_canary(p)
print('LOCAL /opt fixed package: actual ubuntu compile, full type comparison, rejecting axiom audit and canary covered')
