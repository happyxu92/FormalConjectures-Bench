"""Repair-time generation from the original golden input; never called by verifier."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final theorem doc-comment cannot attach to a metaprogram command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end FermatCatalanConjecture')].strip()
source = prefix + '''
-- Elaborate the original declaration, then discard it and export only its full type.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `FermatCatalanConjecture.fermat_catalan
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
end FermatCatalanConjecture
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
