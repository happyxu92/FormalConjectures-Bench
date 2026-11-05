"""Repair-time only: extract this task's complete elaborated type from golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the immediately preceding target documentation comment.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos686')].strip()
source = prefix + '''
-- Generated solely from this task's trusted golden, with no candidate import.
-- Keep the complete type and universes, discard the temporary theorem and its
-- proof environment, then export a kernel-checked definition of the type.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos686.erdos_686.variants.four_three
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
end Erdos686
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
