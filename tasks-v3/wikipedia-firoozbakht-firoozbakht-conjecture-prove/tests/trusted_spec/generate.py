"""Repair-time only: extract the complete type from the immutable golden input."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final docstring belongs to the temporary theorem, not the extraction command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Firoozbakht')].strip()
source = prefix + '''
-- Elaborate without candidate imports; discard the temporary placeholder theorem.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Firoozbakht.firoozbakht_conjecture
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
end Firoozbakht
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
