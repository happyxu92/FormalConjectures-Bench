"""Repair-time only: elaborate the complete golden declaration in isolation."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the target's trailing documentation comment, preserving all definitions.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end EulerSumOfPowers')].strip()
source = prefix + '''
-- Elaborate the full declaration with Lean, then restore the original environment
-- before exporting only its closed type expression and ordered universe parameters.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `EulerSumOfPowers.eulers_sum_of_powers_conjecture.false_for_k5
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
end EulerSumOfPowers
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
