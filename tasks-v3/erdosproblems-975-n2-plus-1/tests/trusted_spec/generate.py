"""Repair-time extraction from this task's immutable golden, without candidate input."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove the final unattached doc comment, but retain all original declarations.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos975')].strip()
source = prefix + '''
-- Elaborate in a temporary environment, retain the COMPLETE type and universes,
-- restore the original environment, then compile only its definition value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos975.erdos_975.variants.n2_plus_1
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
end Erdos975
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
