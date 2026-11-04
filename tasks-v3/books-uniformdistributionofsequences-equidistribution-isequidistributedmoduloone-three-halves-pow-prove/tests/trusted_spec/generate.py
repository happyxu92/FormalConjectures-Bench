"""Repair-time only: elaborate trusted declaration, export its full type, not its proof."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target docstring must attach to the temporary declaration, not run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Equidistribution')].strip()
source = prefix + '''
-- Repair-time extraction in a candidate-free environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Equidistribution.isEquidistributedModuloOne_three_halves_pow
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
end Equidistribution
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
