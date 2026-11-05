"""Repair-time only: elaborate the complete trusted declaration in isolation."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the target's unattached doc comment; retain every prefix declaration.
prefix = prefix[:prefix.rindex('/-- Theorem 3 of [BS2013]')]
target = rest[:rest.rindex('end RatEllipticCurve')].strip()
# The complete declaration is parsed by Lean, not reconstructed from its header.
source = prefix + '''
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `EllipticCurveRank.RatEllipticCurve.avg_rank_lt_0885
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
