"""Repair-time only: elaborate the trusted golden declaration then discard it."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the dangling documentation comment preceding the marker.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos975')].strip()
source = prefix + '''
-- No candidate source, Lake configuration, or cache is loaded here.
run_cmd do
  let original ← Lean.getEnv
  let stx ← Lean.ofExcept <| Lean.Parser.runParserCategory (← Lean.getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  Lean.Elab.Command.elabCommand stx
  let some info := (← Lean.getEnv).find? `Erdos975.erdos_975.variants.lower_bound
    | Lean.throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  Lean.setEnv original
  Lean.Elab.Command.liftTermElabM do
    Lean.addAndCompile <| .defnDecl {
      name := `FCBTrustedSpec.ExpectedType
      levelParams := levels
      type := ← Lean.Meta.inferType expected
      value := expected
      hints := .abbrev
      safety := .safe
    }
end Erdos975
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
