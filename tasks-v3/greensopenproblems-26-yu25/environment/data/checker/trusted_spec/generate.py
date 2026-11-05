"""Repair-time only: elaborate the trusted complete target, export only its type."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final target docstring now precedes a meta command, not a declaration.
last_doc = prefix.rfind('/--')
if last_doc >= 0 and prefix[last_doc:].strip().endswith('-/'):
    prefix = prefix[:last_doc] + prefix[last_doc:].replace('/--', '/-', 1)
target = rest[:rest.rindex('end Green26')].strip()
source = prefix + '''
-- No candidate source, project configuration or cache participates here.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green26.green_26.variants.yu25
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
end Green26
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
