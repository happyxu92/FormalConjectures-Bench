"""Repair-time only: extract the complete elaborated type from trusted golden."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final docstring belongs to the target, not the extraction command.
assert prefix[prefix.rindex('/--'):].strip() == '/-- Is `5n` the complexity of `5^n` for `0 < n`? Answer: No. -/'
prefix = prefix[:prefix.rindex('/--')]
target, tail = rest.rsplit('end Mathoverflow75792', 1)
assert not tail.strip()
source = prefix + '''
-- Elaborate in an isolated trusted environment; retain the entire type and
-- ordered universe parameters, then discard the temporary theorem environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Mathoverflow75792.complexity_five_pow
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted universe parameters: {levels}"
  logInfo m!"complete elaborated type: {expected}"
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
end Mathoverflow75792
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
