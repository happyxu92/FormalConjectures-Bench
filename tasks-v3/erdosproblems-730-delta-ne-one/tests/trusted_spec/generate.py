"""Repair-time only: elaborate the task's isolated golden declaration."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the trailing documentation comment before the marker.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos730')].strip()
source = prefix + '''
-- Extract the kernel expression, not a pretty-printed/reparsed proposition.
-- Restore the original environment before exporting ExpectedType so that the
-- temporary target and its placeholder proof are not present in this module.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos730.erdos_730.variants.delta_ne_one
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
end Erdos730
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
