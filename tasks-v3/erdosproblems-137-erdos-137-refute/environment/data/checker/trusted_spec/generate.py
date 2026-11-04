"""Repair-time only: elaborate the immutable golden declaration, save its full type."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
source = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = source.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment describes the temporary theorem, not the extraction command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos137')].strip()
(pkg / 'FCBTrustedSpec.lean').write_text(prefix + '''
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos137.formal_conjectures_bench_refutation
    | throwError "temporary declaration missing"
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
end Erdos137
''')
