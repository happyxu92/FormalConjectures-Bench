"""Repair-time generator: only reads this task's trusted golden Target."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final documentation comment belongs to the target, not to a command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Green27')].strip()
source = prefix + '''
-- Elaborate the entire original target in an isolated temporary environment.
-- Retain its full type and universe list, then discard the temporary theorem.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green27.green_27.variants.previous_lower
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
end Green27
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
