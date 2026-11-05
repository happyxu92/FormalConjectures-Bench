"""Repair-time only: elaborate this task's trusted golden, not candidate code."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the unfinished documentation immediately preceding the marker.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos346')].strip()
source = prefix + '''
-- Elaborate the complete trusted declaration, extract type and universes,
-- then discard its temporary environment (including all proof auxiliaries).
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos346.erdos_346.variants.f_not_isAddComplete
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
end Erdos346
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
