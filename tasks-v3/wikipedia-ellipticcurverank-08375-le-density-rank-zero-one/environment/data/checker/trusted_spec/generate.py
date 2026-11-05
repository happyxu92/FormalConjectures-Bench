"""Repair-time extraction from this task's immutable golden, without candidates."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Only remove the target documentation, not mathematical declarations.
prefix = prefix[:prefix.rindex('/-- Theorem 4 of [BS2013]:')]
ending = '\nend RatEllipticCurve\nend EllipticCurveRank\n'
assert rest.endswith(ending)
target = rest[:-len(ending)].strip()
name = 'EllipticCurveRank.RatEllipticCurve._08375_le_density_rank_zero_one'
source = prefix + '''
-- Elaborate the entire trusted declaration; preserve its full type and levels.
-- Restore the prefix environment so neither target nor proof is exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `''' + name + '''
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
end RatEllipticCurve
end EllipticCurveRank
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
