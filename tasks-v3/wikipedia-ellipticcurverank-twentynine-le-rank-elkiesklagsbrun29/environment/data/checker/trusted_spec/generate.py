"""Repair-time only: extract the full elaborated target, never candidate input."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the trailing documentation comment, whose declaration is temporary.
prefix = prefix[:prefix.rindex('/--')]
closing = 'end WeierstrassCurve\nend EllipticCurveRank'
target = rest[:rest.rindex(closing)].strip()
source = prefix + '''
-- Generated from trusted golden; no Submission, candidate Lake or cache.
-- Restore the environment before exporting the elaborated complete type.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `EllipticCurveRank.WeierstrassCurve.twentynine_le_rank_elkiesKlagsbrun29
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
