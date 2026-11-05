"""Repair-time extraction from this task's trusted golden, never a verifier fallback."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# This final docstring belongs to the extracted target; it cannot attach to
# the extraction command. All preceding declarations remain verbatim.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos267')].strip()
source = prefix + '''
-- Elaborate the entire golden target in an isolated environment, save its
-- full type and universes, then discard the temporary theorem and proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos267.erdos_267.variants.fibonacci_inverse_sum
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
end Erdos267
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
