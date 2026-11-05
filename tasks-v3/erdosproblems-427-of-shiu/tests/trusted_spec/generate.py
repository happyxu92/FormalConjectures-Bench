"""Repair-time extraction from this task's immutable golden; never run by verifier."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the final documentation comment; preserve the original prefix definitions.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos427')].strip()
source = prefix + '''
-- Elaborate the COMPLETE golden declaration in a disposable environment.
-- Export only its kernel-checked type expression, including all parameters.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos427.erdos_427.variants.of_shiu
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
end Erdos427
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
