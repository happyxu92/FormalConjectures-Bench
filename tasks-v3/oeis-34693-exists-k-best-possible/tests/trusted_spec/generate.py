"""Repair-time only: elaborate this task's immutable golden without Submission."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the dangling target doc-comment, not any prefix declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end OeisA34693')].strip()
source = prefix + '''
-- The temporary declaration is elaborated only to extract its complete type.
-- Restore the original environment before compiling the retained definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `OeisA34693.exists_k_best_possible
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
end OeisA34693
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
