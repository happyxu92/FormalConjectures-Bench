"""Repair-time only: elaborate this task's trusted golden, with no candidate imports."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The original existence proof calls a frozen theorem with sorry. Substitute
# only this proof term (same declaration/type); all mathematical definitions
# remain byte-for-byte unchanged. Proof irrelevance preserves f's meaning.
old = '''  use k
  exact erdos_961.sylvester_schur k hk'''
assert prefix.count(old) == 1
proof = (pkg / 'WellDefinedProof.lean').read_text().split(':= by\n', 1)[1].split('\nend Erdos961', 1)[0]
prefix = prefix.replace(old, proof)
# Drop the final target doc-comment, which cannot attach to a command block.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos961')].strip()
source = prefix + '''
-- Elaborate the complete target, then restore the environment so that the
-- placeholder theorem and its proof cannot be exported or become dependencies.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos961.erdos_961.variants.erdos_upper_bound
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
end Erdos961
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
