"""Repair-time extraction from this task's trusted golden; never run by checker."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Omit only the trailing target doc-comment (it must attach to a declaration).
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos36')].strip()
source = prefix + '''
-- Elaborate the entire trusted declaration, retain its type and universes,
-- restore the pre-target environment, then export only the checked definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos36.minimum_overlap.variants.lower.scherk_1955
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
end Erdos36
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
