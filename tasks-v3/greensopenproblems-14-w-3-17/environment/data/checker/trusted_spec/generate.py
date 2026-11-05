"""Repair-time only: elaborate the complete trusted golden target in isolation."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final documentation comment belongs to the target, not the metacommand.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Green14')].strip()
source = prefix + '''
-- Elaborate the full original declaration, capture all binders and universes,
-- then restore the environment before exporting only the expected type value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green14.W_3_17
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
end Green14
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
