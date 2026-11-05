"""Repair-time extraction only; the verifier never executes this generator."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target's doc comment cannot attach to a metaprogramming command.
# All actual prefix declarations remain byte-for-byte unchanged.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end RamanujanTau')].strip()
source = prefix + '''
-- Elaborate the entire trusted declaration (including all implicit binders),
-- save its complete type/universes, and discard the temporary proof environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `RamanujanTau.ramanujan_petersson
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
end RamanujanTau
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
