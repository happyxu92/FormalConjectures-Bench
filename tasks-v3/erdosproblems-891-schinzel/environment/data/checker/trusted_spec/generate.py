"""Repair-time extraction from this task's immutable golden, never a candidate."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Only remove the trailing explanatory doc comment, not mathematical declarations.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos891')].strip()
source = prefix + '''
-- Elaborate the full golden declaration in isolation, save its type and levels,
-- and restore the preceding environment before adding the definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos891.erdos_891.variants.schinzel
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
end Erdos891
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
