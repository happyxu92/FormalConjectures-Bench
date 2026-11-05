from pathlib import Path
import json
pkg=Path(__file__).resolve().parent
golden=(pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix,rest=golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN',1)
prefix=prefix.replace('import FormalConjecturesBench.Submission\n','')
# Remove only the target doc-comment (not any prefix definition).
prefix=prefix[:prefix.rindex('/--')]
target=rest[:rest.rindex('end Erdos357')].strip()
source=prefix+'\n-- Repair-time only: elaborate the trusted complete declaration, capture its\n-- entire type and level parameters, then discard all temporary declarations.\nopen Lean Elab Command in\nrun_cmd do\n  let original ← getEnv\n  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command '+json.dumps(target,ensure_ascii=False)+'\n  elabCommand stx\n  let some info := (← getEnv).find? `Erdos357.erdos_357.variants.weisenberg\n    | throwError "missing temporary target"\n  let expected := info.type\n  let levels := info.levelParams\n  setEnv original\n  liftTermElabM do\n    addAndCompile <| .defnDecl {\n      name := `FCBTrustedSpec.ExpectedType\n      levelParams := levels\n      type := ← Meta.inferType expected\n      value := expected\n      hints := .abbrev\n      safety := .safe\n    }\nend Erdos357\n'
(pkg/'FCBTrustedSpec.lean').write_text(source)
