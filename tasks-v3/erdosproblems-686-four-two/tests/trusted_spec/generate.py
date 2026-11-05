"""Repair-time only: extract the complete type from this task's trusted golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment belongs to the temporary target, not to run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos686')].strip()
source = prefix + '''
-- Elaborate without candidates, retain the full type and universes, then discard
-- the temporary theorem environment before exporting ExpectedType.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos686.erdos_686.variants.four_two
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
