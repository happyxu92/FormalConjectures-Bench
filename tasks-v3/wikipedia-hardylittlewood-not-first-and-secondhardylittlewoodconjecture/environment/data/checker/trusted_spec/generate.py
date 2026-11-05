"""Repair-time only: derive a closed elaborated type from this task's golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Omit the two unrelated, pre-existing placeholder proofs, not any definitions.
for name, ending in [
    ('first_hardy_littlewood_conjecture', '    FirstHardyLittlewoodConjectureFor m := by\n  sorry'),
    ('second_hardy_littlewood_conjecture', '    SecondHardyLittlewoodConjectureFor x y := by\n  sorry'),
]:
    declaration = prefix.index('@[category research open, AMS 11]\ntheorem ' + name)
    start = prefix.rindex('/--', 0, declaration)
    stop = prefix.index(ending, declaration) + len(ending)
    prefix = prefix[:start] + prefix[stop:]
# The final doc comment annotates the target, not the generation command.
prefix = prefix[:prefix.rindex('/-- Richards')]
target = rest[:rest.rindex('end HardyLittlewood')].strip()
source = prefix + '''
-- Elaborate in isolation, retain complete type/levelParams, discard theorem.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `HardyLittlewood.not_first_and_secondHardyLittlewoodConjecture
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
end HardyLittlewood
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
