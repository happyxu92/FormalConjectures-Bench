"""Repair-time only: extract the complete type from this task's trusted golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos48')].strip()
source = prefix + '''
-- Elaborate the trusted complete declaration, discard the temporary theorem,
-- and export only its elaborated type and ordered universe parameters.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos48.erdos_48
    | throwError "missing temporary target"
  -- Pattern binders in the set-builder elaborate to a temporary matcher.
  -- Delta-expand only newly generated declarations before discarding them;
  -- original prefix constants and the complete proposition remain intact.
  let expected ← liftTermElabM <| Meta.deltaExpand info.type (fun n => !original.contains n)
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
end Erdos48
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
