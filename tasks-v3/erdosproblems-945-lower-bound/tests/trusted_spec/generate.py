"""Repair-time only: extract the complete elaborated target type from trusted golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the final doc comment, which belongs to the target declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos945')].strip()
source = prefix + '''
-- Trusted repair-time elaboration. Discard the temporary target environment
-- before exporting the complete kernel-checked type as a definition value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos945.erdos_945.variants.lower_bound
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
end Erdos945
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
