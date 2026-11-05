"""Repair-time only: elaborate the complete trusted declaration, not a regex type."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment describes the removed target, not the extraction command.
prefix = prefix[:prefix.rindex('/--')]
target, closing = rest.rsplit('end Erdos470', 1)
assert not closing.strip()
target = target.strip()
source = prefix + '''
-- Repair-time extraction from golden, with no candidate imports or Lake cache.
-- Discard the temporary theorem environment, export only its complete type.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos470.erdos_470.variants.prime_gap_imp_inf_prim_weird
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
end Erdos470
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
