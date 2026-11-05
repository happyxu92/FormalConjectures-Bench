"""Repair-time extraction from this task's immutable golden input, not candidate code."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the trailing doc comment for the target; retain all original definitions.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end CongruentNumber')].strip()
source = prefix + '''
-- Elaborate the entire original target in an isolated environment, extract its
-- full type and ordered universe parameters, then discard the temporary proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `CongruentNumber.Tunnell_even
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
end CongruentNumber
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
