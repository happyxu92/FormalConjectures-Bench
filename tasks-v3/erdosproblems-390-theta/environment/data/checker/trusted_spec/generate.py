"""Repair-time extraction from this task's immutable golden, never run by verifier."""
from pathlib import Path
import hashlib, json
pkg = Path(__file__).resolve().parent
golden = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
assert hashlib.sha256(golden.read_bytes()).hexdigest() == '3505b32daca4bb26b618a83df3d96cfd59314b87ef2722281d8584b3bb141fad'
prefix, rest = golden.read_text().split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment belongs to the temporary theorem, not run_cmd.
prefix = prefix[:prefix.rindex('/--')]
# Keep all original definitions and scoped/open context. Only the final theorem
# is temporarily elaborated, then removed by restoring the prior environment.
target = rest[:rest.rindex('end Erdos390')].strip()
source = prefix + '''
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos390.erdos_390.variants.theta
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
end Erdos390
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
