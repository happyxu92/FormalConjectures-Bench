"""Repair-time only: elaborate the trusted golden declaration, not candidate text."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final docstring documents the removed temporary theorem, not run_cmd.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end ArtinPrimitiveRootsConjecture')].strip()
source = prefix + '''
-- Extract all binders and universe parameters before discarding the temporary theorem.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `ArtinPrimitiveRootsConjecture.conditional_artin_primitive_roots.parts.i
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
end ArtinPrimitiveRootsConjecture
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
