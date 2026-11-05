"""Repair-time extraction from this task's immutable golden, not candidate sources."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the target's trailing documentation, not mathematical declarations.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Green38')].strip()
source = prefix + '''
-- Elaborate the complete trusted target, retain its full type and ordered
-- universe parameters, then discard the temporary theorem and its proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green38.green_38.variants.best_upper
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted full type: {expected}; universes: {levels}"
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
end Green38
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
