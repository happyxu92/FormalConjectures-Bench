"""Repair-time only: derive the complete type from this task's trusted golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# This task has no prefix mathematical definitions. The unrelated upstream
# erdos_285 theorem is an unproved placeholder, not a dependency of the bound.
# Omit that theorem (and its documentation), rather than exporting its sorry.
prefix = prefix[:prefix.index('/--\nLet $f(k)$')]
target = rest[:rest.rindex('end Erdos285')].strip()
source = prefix + '''
-- Generated from the trusted golden Target without any candidate input.
-- Elaborate the entire declaration, retain its complete type and universes,
-- then restore the environment to discard the temporary placeholder proof.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos285.erdos_285.variants.lb
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
end Erdos285
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
