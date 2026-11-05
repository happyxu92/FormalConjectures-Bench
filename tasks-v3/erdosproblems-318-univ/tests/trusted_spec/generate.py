"""Repair-time extraction from this task's trusted golden; no candidate inputs."""
from pathlib import Path
import hashlib, json
pkg = Path(__file__).resolve().parent
golden_path = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
golden = golden_path.read_text()
assert hashlib.sha256(golden_path.read_bytes()).hexdigest() == '3c1fc722bc2ab5b231cbecdbc37a98a8b1b6feaeef2c5e9b67d8236f7b9cdc34'
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos318')].strip()
source = prefix + '''
-- Elaborate the complete trusted declaration, save its type and universes,
-- then restore the environment so the placeholder theorem is never exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos318.erdos_318.variants.univ
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
end Erdos318
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
