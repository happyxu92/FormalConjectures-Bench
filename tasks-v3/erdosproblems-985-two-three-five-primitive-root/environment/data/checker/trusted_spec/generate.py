"""Repair-time extraction: read only this task's immutable golden input."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop the doc comment that belongs to the target; retain the original prefix.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos985')].strip()
source = prefix + '''
-- Elaborate the complete golden declaration in an isolated environment, retain
-- its full type and level parameters, then discard the temporary declaration.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos985.erdos_985.variants.two_three_five_primitive_root
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
end Erdos985
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
