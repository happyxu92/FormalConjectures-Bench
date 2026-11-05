"""Repair-time extraction from this task's immutable golden; never a verifier fallback."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final documentation comment belongs to the temporary target, not run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end RiemannZetaValues')].strip()
source = prefix + '''
-- Elaborate all binders and universes in a candidate-free environment, then
-- discard the temporary target and its proof before exporting ExpectedType.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `RiemannZetaValues.exists_irrational_of_five_seven_nine_eleven
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted universes in order: {levels}"
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
end RiemannZetaValues
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
