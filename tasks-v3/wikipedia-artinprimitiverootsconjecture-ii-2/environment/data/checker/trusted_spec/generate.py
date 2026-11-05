from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the dangling doc comment attached to the target command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end ArtinPrimitiveRootsConjecture')].strip()
source = prefix + '''
-- Extract the elaborated complete type in a candidate-free golden environment.
-- Restore that environment before exporting: no placeholder theorem is saved.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `ArtinPrimitiveRootsConjecture.conditional_artin_primitive_roots.parts.ii
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
