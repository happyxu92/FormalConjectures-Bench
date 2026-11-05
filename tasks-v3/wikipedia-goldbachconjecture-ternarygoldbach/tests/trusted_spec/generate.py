"""Repair-time generator; reads this task's trusted golden, never candidate files."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The pending target doc comment cannot attach to a run_cmd command.
prefix = prefix[:prefix.rindex('/--')]
target, ending = rest.rsplit('end TernaryGoldbachConjecture', 1)
assert not ending.strip()
source = prefix + '''
-- Elaborate all binders using Lean, then discard the temporary declaration.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `TernaryGoldbachConjecture.ternaryGoldbach
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
end TernaryGoldbachConjecture
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
