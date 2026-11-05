"""Repair-time only: elaborate the trusted golden declaration and capture its full type."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment annotates the theorem, not the extraction command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end GaussCircleProblem')].strip()
source = prefix + '''
-- No candidate imports, sources, Lake configuration or caches participate.
-- The complete declaration is elaborated, then its temporary environment is discarded.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `GaussCircleProblem.exact_form_floor
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
