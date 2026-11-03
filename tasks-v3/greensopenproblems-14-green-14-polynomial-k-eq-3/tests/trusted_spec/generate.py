"""Repair-time extraction from the immutable golden input; never used by verifier."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target's doc comment would otherwise attach to the extraction command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Green14')].strip()
# All original prefix definitions retain their names. The unrelated original
# open-question placeholder stays in the prefix but is audited NOT to occur in
# the expected type's transitive dependencies. The temporary target is discarded.
source = prefix + '''
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green14.green_14_polynomial_k_eq_3
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
end Green14
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
