"""Repair-time generator. Input is only this task's immutable golden Target."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final documentation comment annotates the target declaration, not run_cmd.
# Remove only that documentation block; all prefix declarations stay unchanged.
prefix = prefix[:prefix.rindex('/--')]
target, tail = rest.rsplit('end Erdos373', 1)
assert not tail.strip()
source = prefix + '''
-- Elaborate the entire trusted declaration, including every binder. Discard
-- its temporary proof/environment before exporting the checked type value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos373.erdos_373.variants.of_lower_bound
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  setEnv original
  liftTermElabM do
    addAndCompile <| .defnDecl {
      name := `FCBTrustedSpec.ExpectedType
      levelParams := levels
      type := ← Meta.inferType expected
      value := expected
      hints := .abbrev
      safety := .safe
    }
end Erdos373
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
