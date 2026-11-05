"""Repair-time extraction from this task's immutable golden, never a candidate."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The trailing doc comment belongs to the temporary target, not run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos931')].strip()
source = prefix + '''
-- Elaborate the complete original declaration, then discard its proof and
-- auxiliary declarations before compiling the extracted type expression.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos931.erdos_931.variants.additional_condition_nonempty
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
end Erdos931
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
