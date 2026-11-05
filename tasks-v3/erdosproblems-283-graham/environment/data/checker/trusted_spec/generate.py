"""Repair-time extraction from this task's immutable golden (never verifier-time)."""
from pathlib import Path
import hashlib
import json

pkg = Path(__file__).resolve().parent
golden = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
raw = golden.read_text()
assert hashlib.sha256(golden.read_bytes()).hexdigest() == 'f8e689e65f7ba61d210865c1190aaf1afc2287341ba3fb95b3b3ee3f20d4627d'
prefix, rest = raw.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# A declaration doc comment cannot attach to the extraction command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos283')].strip()
source = prefix + '''
-- Elaborate the entire original declaration in an isolated environment, retain
-- its full type and universes, then roll back the temporary proof environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos283.erdos_283.variants.graham
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted complete type: {expected}; universes: {levels}"
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
end Erdos283
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
