from pathlib import Path
import json

# Repair-time only: inputs are the immutable golden tree, not /app or candidate caches.
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The trailing target doc-comment must not attach to the generation command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos399')].strip()
source = prefix + '''
-- Elaborate the complete trusted declaration, retain its type and universes,
-- then restore the pre-target environment before exporting the definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos399.erdos_399.variants.erdos_oblath
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
end Erdos399
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
