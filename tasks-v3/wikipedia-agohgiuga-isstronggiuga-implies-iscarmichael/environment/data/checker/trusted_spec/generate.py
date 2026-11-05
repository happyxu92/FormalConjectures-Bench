from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
# Only trusted golden input is read. No Submission, candidate Lake or caches.
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The last doc-comment belongs to the removed target, not a prefix declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end AgohGiuga')].strip()
source = prefix + '''
-- Elaborate all binders/universes with Lean, then discard the temporary theorem.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `AgohGiuga.agoh_giuga.variants.isStrongGiuga_implies_isCarmichael
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
end AgohGiuga
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
