"""Repair-time generator: use only this task's trusted golden input."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the dangling target doc comment (the preceding declarations remain).
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Constant1a')].strip()
source = prefix + '''
-- Elaborate the full original declaration, extract type and universes, then
-- restore the prior environment so the temporary target is never exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Constant1a.c1a_upper_bound
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
end Constant1a
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
