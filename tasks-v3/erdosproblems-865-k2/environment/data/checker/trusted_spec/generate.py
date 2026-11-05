"""Repair-time extraction from this task's immutable golden, never candidate input."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# A declaration doc comment cannot attach to the extraction command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos865')].strip()
source = prefix + '''
-- Elaborate the entire trusted declaration, then discard its temporary proof.
-- Only its kernel-checked type expression and original universe order survive.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos865.erdos_865.variants.k2
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted universe parameters: {levels}"
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
end Erdos865
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
