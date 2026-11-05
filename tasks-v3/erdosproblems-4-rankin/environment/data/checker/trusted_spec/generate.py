"""Repair-time only: elaborate the isolated original golden declaration."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target's doc comment must not attach to the extraction command.
prefix = prefix[:prefix.rindex('/-- Rankin')]
target = rest[:rest.rindex('end Erdos4')].strip()
source = prefix + '''
-- Elaborate the full declaration including all binders/universes. Restore the
-- original environment before exporting only its kernel-checked type value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos4.erdos_4.variants.rankin
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
end Erdos4
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
