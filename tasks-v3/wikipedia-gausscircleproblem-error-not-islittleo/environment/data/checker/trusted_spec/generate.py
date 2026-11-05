"""Repair-time extraction from this task's trusted golden; never run by verifier."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target's doc comment cannot attach to a run_cmd; preserve it as a plain comment.
pos = prefix.rindex('/--')
prefix = prefix[:pos] + prefix[pos:].replace('/--', '/-', 1)
target = rest[:rest.rindex('end GaussCircleProblem')].strip()
source = prefix + '''
-- Elaborate the entire trusted declaration with Lean's parser/elaborator,
-- retain its full type and universe order, discard the placeholder environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `GaussCircleProblem.error_not_isLittleO
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
end GaussCircleProblem
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
