from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The sole preceding declaration is the independent, weaker density theorem.
# Elaborate it and the target inside a disposable environment, keeping every
# original prefix name during elaboration, but export neither sorry proof.
imports, declarations = prefix.split('namespace Erdos298', 1)
declarations = declarations[:declarations.rindex('/--')]
target = rest[:rest.rindex('end Erdos298')].strip()
source = imports + '''
namespace Erdos298
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let prefixStx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(declarations.strip(), ensure_ascii=False) + '''
  elabCommand prefixStx
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos298.erdos_298.variants.upper_density
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
end Erdos298
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
