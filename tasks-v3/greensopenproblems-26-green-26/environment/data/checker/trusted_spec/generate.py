"""Repair-time extraction from this task's immutable golden input only."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
original = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
golden = original.read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Green26')].strip()
source = prefix + '''
-- Generated from the immutable golden Target, without candidate imports.
-- Elaborate the entire declaration, save its full type and universes, then
-- restore the pre-declaration environment before compiling ExpectedType.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green26.green_26
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
end Green26
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
