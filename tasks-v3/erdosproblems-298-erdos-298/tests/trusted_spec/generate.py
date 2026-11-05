"""Repair-time only: elaborate the trusted golden declaration, not a candidate."""
from pathlib import Path
import json, hashlib
pkg = Path(__file__).resolve().parent
source = pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean'
golden = source.read_text(encoding='utf-8')
assert hashlib.sha256(source.read_bytes()).hexdigest() == '0545efeab904f02057f3c6fdec94ef681dda0ead4814fa79204a1e5d7af89fc5'
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment belongs to the temporary theorem, not run_cmd.
# This target has no prefix declarations after that comment.
prefix = prefix[:prefix.rindex('/--')]
target, tail = rest.rsplit('end Erdos298', 1)
assert not tail.strip()
(pkg/'FCBTrustedSpec.lean').write_text(prefix + '''
-- Elaborate the entire original declaration; discard the temporary theorem
-- environment before exporting only its full type expression and universes.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target.strip(), ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos298.erdos_298
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  logInfo m!"extracted universes in order: {levels}"
  logInfo m!"extracted complete type: {expected}"
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
end Erdos298
''', encoding='utf-8')
