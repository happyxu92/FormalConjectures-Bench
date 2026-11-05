"""Repair-time extraction from this task's trusted golden; not used by checker."""
from pathlib import Path
import hashlib
import json

pkg = Path(__file__).resolve().parent
golden_path = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
golden = golden_path.read_text()
assert hashlib.sha256(golden_path.read_bytes()).hexdigest() == 'e518b86bbe3c2b454f2cc43229e5b235d71e1606ba71c785c6a0365eb1dc73f7'
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos470')].strip()
source = prefix + '''
-- Elaborate the complete trusted declaration in isolation. Restore the original
-- environment before exporting the definition, discarding the temporary proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos470.erdos_470.variants.abundancy_index
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
