"""Repair-time extraction from this task's immutable golden, without candidates."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the target documentation comment; retain every original declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end RiemannZetaValues')].strip()
source = prefix + '''
-- Extract the complete elaborated type and its ordered universe parameters.
-- Restore the original environment before adding the definition: the temporary
-- target and its placeholder proof are never exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `RiemannZetaValues.infinite_irrational_at_odd
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
end RiemannZetaValues
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
