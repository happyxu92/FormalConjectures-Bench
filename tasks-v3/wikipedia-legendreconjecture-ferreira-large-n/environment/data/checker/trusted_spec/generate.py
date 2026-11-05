"""Repair-time only: elaborate the original complete declaration, save its type."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove the target's pending doc comment, not any mathematical declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end LegendreConjecture')].strip()
source = prefix + '''
-- Elaborate in a temporary environment, then discard the proof and children.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `LegendreConjecture.legendre_conjecture.ferreira_large_n
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
end LegendreConjecture
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
