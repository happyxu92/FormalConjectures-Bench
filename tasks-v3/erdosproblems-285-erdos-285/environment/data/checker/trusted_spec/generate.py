from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment describes the target; it must not attach to run_cmd.
doc = prefix.rfind('/--')
if doc >= 0:
    prefix = prefix[:doc] + prefix[doc:].replace('/--', '/-', 1)
target = rest[:rest.rindex('end Erdos285')].strip()
source = prefix + '''
-- Repair-time extraction in a candidate-free environment. Do not export the
-- temporary theorem or its placeholder proof: restore the original environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos285.erdos_285
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
end Erdos285
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
