"""Repair-time only; consume this task's trusted golden, never a candidate."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove the dangling target doc comment, keeping all preceding definitions.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos454')].strip()
source = prefix + '''
-- Elaborate the entire trusted declaration, capture type and ordered universes,
-- then restore the environment so no temporary proof or child is exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos454.erdos_454.variants.two_le_limsup
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
end Erdos454
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
