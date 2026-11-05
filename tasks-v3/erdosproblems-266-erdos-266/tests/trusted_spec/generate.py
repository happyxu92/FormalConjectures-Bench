"""Repair-time only: elaborate this task's complete trusted declaration."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The target's doc-comment cannot attach to a metaprogram command.
prefix = prefix[:prefix.rindex('/--')]
target, closing = rest.rsplit('end Erdos266', 1)
assert not closing.strip()
source = prefix + '''
-- Elaborate the complete original declaration, retaining only its type and
-- ordered universe parameters. Discard the temporary theorem environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos266.erdos_266
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted complete type: {expected}; universe parameters: {levels}"
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
end Erdos266
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
