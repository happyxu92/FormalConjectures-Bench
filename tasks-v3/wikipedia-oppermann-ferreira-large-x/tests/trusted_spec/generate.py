"""Repair-time only: elaborate this task's immutable golden, no candidate inputs."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Remove only the final target doc comment, not any mathematical declaration.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Oppermann')].strip()
source = prefix + '''
-- Extract the entire kernel type and universe list, then discard the temporary
-- theorem and its proof environment before compiling ExpectedType.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Oppermann.oppermann_conjecture.ferreira_large_x
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted universe parameters: {levels}"
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
end Oppermann
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
