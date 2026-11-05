from pathlib import Path
import hashlib
import json

# Repair-time only: the sole mathematical input is this task's trusted golden.
pkg = Path(__file__).resolve().parent
golden_path = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
golden = golden_path.read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the final documentation comment attached to the target.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Green14')].strip()
source = prefix + '''
-- Elaborate the full trusted declaration in a temporary environment, retain
-- its complete type and universes, then discard the placeholder declaration.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Green14.W_3_11
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
end Green14
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
print('golden Target sha256:', hashlib.sha256(golden_path.read_bytes()).hexdigest())
