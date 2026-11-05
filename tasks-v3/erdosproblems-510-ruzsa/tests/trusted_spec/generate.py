"""Repair-time only: elaborate the trusted complete declaration in isolation."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# A declaration doc-comment cannot annotate the repair-time run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos510')].strip()
source = prefix + '''
-- Elaborate all binders and universes before any candidate can be imported.
-- Restore the environment so the temporary proof and its children are not exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos510.erdos_510.variants.ruzsa
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
end Erdos510
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
