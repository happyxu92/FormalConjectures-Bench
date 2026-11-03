from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
pkg.mkdir(exist_ok=True)
golden = (pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final documentation comment originally attaches to the target declaration.
# Keep its text as an ordinary comment before the extraction command.
last_doc = prefix.rfind('/--')
if last_doc >= 0:
    prefix = prefix[:last_doc] + prefix[last_doc:].replace('/--', '/-', 1)
target = rest[:rest.rindex('end Erdos266')].strip()
source = prefix + '''
-- Generated from the trusted golden Target, without candidate imports.
-- Elaborate the complete declaration, retain its type, then discard the
-- temporary theorem environment before exporting the kernel-checked definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos266.erdos_266.variants.all_rationals
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
end Erdos266
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
