"""Repair-time extraction from this task's immutable golden; never run by verifier."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final documentation comment describes the target, not the extraction command.
pos = prefix.rindex('/--')
prefix = prefix[:pos] + prefix[pos:].replace('/--', '/-', 1)
target, closing = rest.rsplit('end SumOfThreeCubes', 1)
assert not closing.strip()
source = prefix + '''
-- Elaborate the original declaration in an isolated trusted environment. Retain
-- its complete type/universes, then restore the environment before exporting.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `SumOfThreeCubes.isSumOfThreeCubesRat_any
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted complete type: {expected}"
  logInfo m!"extracted universe parameters: {levels}"
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
end SumOfThreeCubes
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
