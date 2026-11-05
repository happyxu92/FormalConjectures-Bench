"""Repair-time only: elaborate the whole trusted target, discard its proof environment."""
from pathlib import Path
import hashlib
import json
pkg = Path(__file__).resolve().parent
golden_path = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
golden = golden_path.read_text()
assert hashlib.sha256(golden_path.read_bytes()).hexdigest() == '1f556400727e1fe9f6a6fa6d631538d79d7db337a00aff87f1b6df122aa254de'
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the target's trailing documentation comment, which cannot attach
# to the repair-time command. All mathematical prefix declarations remain.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Andrica')].strip()
source = prefix + '''
-- Repair-time elaboration in a candidate-free environment. Keep every binder
-- and universe parameter from the actual declaration; discard its proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Andrica.andrica_conjecture.ferreira_large_n
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted complete type: {expected}"
  logInfo m!"extracted universes in declaration order: {levels}"
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
end Andrica
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
