"""Repair-time extraction from this task's immutable golden, without candidates."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the final target documentation, retaining all original definitions.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos416')].strip()
source = prefix + '''
-- Elaborate the full declaration in isolation. Restore the original environment
-- before adding the type expression as a kernel-checked definition value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos416.erdos_416.variants.Pillai
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
end Erdos416
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
