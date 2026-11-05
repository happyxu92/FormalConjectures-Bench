"""Repair-time extraction from this task's immutable golden, never a candidate."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
prefix, rest = golden.read_text().split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Keep the original prefix declarations/names, and discard only the final doc comment.
prefix = prefix[:prefix.rindex('/-- Pollack and Shapiro')]
target = rest[:rest.rindex('end Erdos399')].strip()
assert target.startswith('theorem erdos_399.variants.pollack_shapiro (n x : ℕ)')
source = prefix + '''
-- Repair-time only: elaborate the whole golden declaration without Submission.
-- Restore the pre-declaration environment, exporting only its complete type.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory original `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos399.erdos_399.variants.pollack_shapiro
    | throwError "missing trusted extraction target"
  let expected := info.type
  let universes := info.levelParams
  setEnv original
  liftTermElabM do
    addAndCompile <| .defnDecl {
      name := `FCBTrustedSpec.ExpectedType
      levelParams := universes
      type := ← Meta.inferType expected
      value := expected
      hints := .abbrev
      safety := .safe
    }
end Erdos399
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
