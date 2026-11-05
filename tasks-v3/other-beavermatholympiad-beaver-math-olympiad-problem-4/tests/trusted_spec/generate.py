"""Repair-time extraction from this task's immutable golden input only."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
source = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = source.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the final unattached doc comment; retain the original prefix declarations.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end BeaverMathOlympiad')].strip()
(pkg / 'FCBTrustedSpec.lean').write_text(prefix + '''
-- Elaborate in an isolated trusted environment, retain ALL type binders and levels,
-- then discard the placeholder declaration and its children before exporting.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `BeaverMathOlympiad.beaver_math_olympiad_problem_4
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
end BeaverMathOlympiad
''')
