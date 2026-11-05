"""Repair-time generation from this task's immutable golden; never used by verifier."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final target doc comment cannot decorate the extraction command.
# Keep all mathematical declarations and their original names unchanged.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos350')].strip()
source = prefix + '''
-- Generated independently of candidate sources, configuration and caches.
-- Elaborate the whole declaration, save its complete type and universes, and
-- restore the original environment before exporting the definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos350.erdos_350.variants.strengthening
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
end Erdos350
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
