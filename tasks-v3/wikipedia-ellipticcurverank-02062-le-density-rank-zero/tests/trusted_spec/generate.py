"""Repair-time only: elaborate the trusted golden declaration, export its full type."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final target doc-comment must not attach to the generation command.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end RatEllipticCurve')].strip()
source = prefix + '''
-- Capture the elaborated full type, not the parsed header. Discard the temporary
-- theorem and all generated children before exporting the kernel-checked value.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `EllipticCurveRank.RatEllipticCurve._02062_le_density_rank_zero
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
