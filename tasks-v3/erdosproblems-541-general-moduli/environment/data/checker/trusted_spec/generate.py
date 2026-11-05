"""Repair-time extraction from this task's immutable golden, never a candidate."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# There are no mathematical prefix definitions in this task. The earlier,
# distinct prime-modulus theorem is a golden placeholder, not a dependency of
# the general-modulus proposition; do not export that unrelated sorry theorem.
prefix = prefix[:prefix.index('/--\nLet')]
target = rest[:rest.rindex('end Erdos541')].strip()
source = prefix + '''
-- Elaborate the entire original declaration, retain its type and universes,
-- then restore the pre-declaration environment before kernel-checking a def.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos541.erdos_541.variants.general_moduli
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
end Erdos541
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
