"""Repair-time extraction from immutable golden; no candidate files are loaded."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# A doc comment immediately before a metaprogram is not a Lean declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end EulerSumOfPowers')].strip()
source = prefix + '''
-- Elaborate the entire original target in a disposable environment, extracting
-- its kernel Expr and ordered level parameters, never its placeholder proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `EulerSumOfPowers.eulers_sum_of_powers_conjecture.false_for_k4
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
end EulerSumOfPowers
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
