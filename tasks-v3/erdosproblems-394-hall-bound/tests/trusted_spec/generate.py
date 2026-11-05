"""Repair-time only: elaborate the trusted complete declaration and save its type."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target doc-comment precedes a generation command, not a declaration.
start = prefix.rindex('/--')
prefix = prefix[:start] + prefix[start:].replace('/--', '/-', 1)
target = rest[:rest.rindex('end Erdos394')].strip()
source = prefix + '''
-- No candidate modules, configuration, or caches participate in generation.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos394.erdos_394.variants.hall_bound
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
end Erdos394
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
