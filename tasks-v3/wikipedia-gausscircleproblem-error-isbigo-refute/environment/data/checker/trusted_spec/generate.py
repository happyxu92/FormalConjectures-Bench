"""Repair-time generator. Input is the unmodified trusted golden, not Submission."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target docstring annotates a theorem, not the following generation command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end GaussCircleProblem')].strip()
source = prefix + '''
-- Elaborate the complete declaration in a clean environment. Export only its
-- type, not the temporary proof or any generated auxiliary declarations.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `GaussCircleProblem.formal_conjectures_bench_refutation
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
