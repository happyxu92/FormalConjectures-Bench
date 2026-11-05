"""Repair-time only: elaborate the original golden declaration without Submission."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop the final documentation comment so it does not annotate run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Green32')].strip()
source = prefix + '''
-- Elaborate in a temporary environment, retain the FULL type and level parameters,
-- restore the original environment, then kernel-check the exported definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green32.green_32.variants.szemeredi_regime
    | throwError "temporary target missing"
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
end Green32
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
