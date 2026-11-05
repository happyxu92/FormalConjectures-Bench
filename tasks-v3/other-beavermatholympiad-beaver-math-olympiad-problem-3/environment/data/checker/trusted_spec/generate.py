"""Repair-time extraction from this task's trusted golden; never used at verification."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the trailing documentation comment; keep all mathematical prefix declarations.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end BeaverMathOlympiad')].strip()
source = prefix + '''
-- Elaborate the entire trusted declaration in a temporary environment, extracting
-- its complete type and ordered universe parameters. Export no temporary proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `BeaverMathOlympiad.beaver_math_olympiad_problem_3
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted ordered universe parameters: {levels}"
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
end BeaverMathOlympiad
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
