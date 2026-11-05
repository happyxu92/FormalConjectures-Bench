"""Repair-time only: elaborate the entire trusted declaration in isolation."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The trailing target doc-comment must not attach to run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos269')].strip()
source = prefix + '''
-- Capture the full elaborated type and universes, then discard the temporary
-- theorem and its proof environment before exporting the definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos269.erdos_269.variants.infinite
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
end Erdos269
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
