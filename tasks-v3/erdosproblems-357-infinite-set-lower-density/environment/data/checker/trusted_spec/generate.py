"""Repair-time extraction from this task's unmodified golden (never a candidate)."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the target doc comment; all preceding original definitions remain.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos357')].strip()
source = prefix + '''
-- Elaborate the complete original declaration in isolation, retain its type
-- and universe parameters, then restore the environment before exporting.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos357.erdos_357.variants.infinite_set_lower_density
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
end Erdos357
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
