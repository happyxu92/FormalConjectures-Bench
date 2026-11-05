"""Repair-time extraction from this task's immutable golden; never used by checker."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the dangling documentation comment of the temporary declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos346')].strip()
source = prefix + '''
-- Elaborate in a candidate-free environment, extract the complete type and
-- ordered universes, restore the environment (discarding the temporary proof),
-- and kernel-check the resulting definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos346.erdos_346.variants.f_isAddStronglyCompleteNatSeq
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
end Erdos346
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
