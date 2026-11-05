"""Repair-time only: elaborate the trusted golden declaration, save its full type."""
from pathlib import Path
import hashlib
import json

pkg = Path(__file__).resolve().parent
golden_path = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
golden = golden_path.read_text()
assert hashlib.sha256(golden_path.read_bytes()).hexdigest() == 'd420a9e397df2ecdd099acf073c73cdef2a8d3b766c5446398580e2c9f29c9cd'
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment belongs to the target, not the generator command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos939')].strip()
source = prefix + '''
-- Elaborate before any candidate exists. Discard the temporary theorem and its
-- proof environment, retaining only the complete type and universe parameters.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos939.erdos_939.variants.eight
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
end Erdos939
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
