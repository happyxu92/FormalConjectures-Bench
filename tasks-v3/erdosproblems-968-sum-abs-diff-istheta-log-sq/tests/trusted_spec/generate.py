"""Repair-time extraction from this task's immutable golden; never run by checker."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the dangling target docstring, retaining all mathematical prefix definitions.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos968')].strip()
source = prefix + '''
-- Elaborate the entire original target in isolation. Restore the pre-target
-- environment before adding the definition, so the placeholder is not exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos968.erdos_968.variants.sum_abs_diff_isTheta_log_sq
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
end Erdos968
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
