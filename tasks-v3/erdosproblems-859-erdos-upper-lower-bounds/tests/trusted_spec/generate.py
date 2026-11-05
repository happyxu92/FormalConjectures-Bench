"""Repair-time extraction from this task's immutable golden, not a candidate."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The last documentation block belongs to the target, not the prefix definition.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos859')].strip()
source = prefix + '''
-- Elaborate the entire golden declaration and preserve its type and universes.
-- Restore the prefix environment so the placeholder and children are not exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos859.erdos_859.variants.erdos_upper_lower_bounds
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
end Erdos859
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
