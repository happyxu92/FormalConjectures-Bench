from pathlib import Path
import hashlib, json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
assert hashlib.sha256(golden.encode()).hexdigest() == '1aa089665df4d47a8a0050bab81666ad054a41b75126f6662db86ece0bc01640'
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# Retain the original prefix, including its unrelated original open problem.
# Only the target's attached doc comment is omitted from this generated module.
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos455')].strip()
source = prefix + '''
-- Repair-time elaboration of the entire trusted declaration, without candidates.
-- Restore the environment before exporting, so the temporary target and its
-- placeholder never become dependencies of ExpectedType.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos455.erdos_455.variants.liminf
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
end Erdos455
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
