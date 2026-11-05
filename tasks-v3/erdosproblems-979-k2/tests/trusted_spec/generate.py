"""Repair-time generator; trusted golden only, no candidate/Lake configuration."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Keep imports, namespace and the exact solutionSet definition. The unrelated
# open research theorem erdos_979 is not a dependency of this variant.
prefix = prefix[:prefix.index('/--')]
target = rest[:rest.rindex('end Erdos979')].strip()
source = prefix + '''
-- Elaborate the entire golden declaration, including every binder/universe.
-- Restore the pre-target environment before exporting only its type value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos979.erdos_979.variants.k2
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
end Erdos979
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
