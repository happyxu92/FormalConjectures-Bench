"""Repair-time only: elaborate this task's trusted golden declaration in isolation."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc-comment belongs to the temporary theorem, not run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos727')].strip()
source = prefix + '''
-- Extract all binders and universe parameters using Lean's elaborator.
-- Discard the temporary declaration (and its proof) before exporting Spec.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos727.erdos_727.variants.k_1
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
end Erdos727
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
