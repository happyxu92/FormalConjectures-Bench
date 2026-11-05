"""Repair-time generator: only trusted golden input, never candidate sources."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The doc comment immediately before the marker belongs to the target, not
# the generation command. All prefix declarations remain unchanged.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos325')].strip()
source = prefix + '''
-- Elaborate the entire trusted target declaration, extract its full type and
-- universe parameters, and restore the environment before exporting the value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos325.erdos_325.variants.wooley
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
end Erdos325
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
