"""Repair-time generator: only sibling golden_env, never candidate sources."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Drop only the target's doc comment, retaining every original prefix definition.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end LehmerMahlerMeasureProblem')].strip()
source = prefix + '''
-- Elaborate in the trusted environment; retain the complete type and universe
-- parameters, restore the environment, then kernel-check the resulting def.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `LehmerMahlerMeasureProblem.lehmer_mahler_measure_problem.variants.not_reciprocal
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
end LehmerMahlerMeasureProblem
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
