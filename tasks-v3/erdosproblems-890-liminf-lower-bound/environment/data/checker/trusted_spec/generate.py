"""Repair-time only: derive the complete kernel type from immutable golden input."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The preceding open research questions are not definitions and are not needed
# by this target. Exclude their placeholder proofs, retaining omegaGt verbatim.
prefix = prefix[:prefix.index('/--\nIf $')]
target = rest[:rest.rindex('end Erdos890')].strip()
source = prefix + '''
-- Elaborate in isolation, retain ALL binders and universes, discard the
-- temporary declaration and its proof before exporting the type definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos890.erdos_890.variants.liminf_lower_bound
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
end Erdos890
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
