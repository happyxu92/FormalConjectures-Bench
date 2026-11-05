"""Repair-time generation from this task's frozen golden input, without candidates."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final target doc comment must not attach to the metaprogram command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end RegularPrimes')].strip()
source = prefix + '''
-- Elaborate the complete declaration in a temporary environment, extract its
-- kernel type and universe parameters, then restore the environment. Neither
-- its placeholder proof nor any generated child declaration is exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `RegularPrimes.infinitude_of_irregularprimes
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
end RegularPrimes
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
