"""Repair-time only: extract the elaborated complete type from this task's golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the final unattached documentation comment, not any declarations.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos535')].strip()
source = prefix + '''
-- Generated only from trusted golden, without any candidate import or cache.
-- The temporary theorem is elaborated to recover all binders and universes,
-- then its entire environment extension is discarded before export.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos535.erdos_535.variants.sunflower_erdos_rado
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
end Erdos535
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
