"""Repair-time only: derive this task's full elaborated type from trusted golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target's doc comment must attach to the parsed temporary theorem, not run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target, endings = rest.split('\nend variants', 1)
assert endings.strip() == 'end Green24'
source = prefix + '''
-- Elaborate the entire original target in an isolated trusted environment.
-- Discard the temporary declaration before exporting only its complete type.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green24.variants.upper_trivial
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
end variants
end Green24
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
