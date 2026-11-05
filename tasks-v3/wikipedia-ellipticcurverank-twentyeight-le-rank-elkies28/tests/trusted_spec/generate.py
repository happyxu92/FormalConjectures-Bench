"""Repair-time only: elaborate this task's complete trusted golden declaration."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
target, suffix = rest.rsplit('\nend WeierstrassCurve', 1)
assert suffix.strip() == 'end EllipticCurveRank'
source = prefix + '''
-- Elaborate the full golden declaration in isolation, retain its complete type
-- and ordered universes, then discard the temporary theorem environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `EllipticCurveRank.WeierstrassCurve.twentyeight_le_rank_elkies28
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
end WeierstrassCurve
end EllipticCurveRank
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
