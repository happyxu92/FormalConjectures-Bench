"""Repair-time only: elaborate the full trusted declaration, discard its proof."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the documentation for the temporary target.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos377')].strip()
source = prefix + '''
-- Generate ExpectedType from the complete elaborated declaration and its universes.
-- Restore the original environment before exporting: no placeholder target survives.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos377.erdos_377.variants.limit.i
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
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
end Erdos377
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
