"""Repair-time extraction from immutable golden; retain type-only generated matchers."""
from pathlib import Path
import json
pkg=Path(__file__).resolve().parent
golden=(pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix,rest=golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN',1)
prefix=prefix.replace('import FormalConjecturesBench.Submission\n','')
prefix=prefix[:prefix.rindex('/--')]
target=rest[:rest.rindex('end FermatCatalanConjecture')].strip()
target=target.replace('theorem fermat_catalan.variants.darmon_granville','theorem FCBExtractionTarget',1)
source=prefix+'''
-- Elaborate in the pristine golden environment; export only the complete type
-- and the auxiliary definitions transitively referenced by that type.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory original `command '''+json.dumps(target,ensure_ascii=False)+'''
  elabCommand stx
  let elaborated ← getEnv
  let some info := elaborated.find? `FermatCatalanConjecture.FCBExtractionTarget
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  setEnv original
  liftTermElabM do
    let rec retain (fuel : Nat) (name : Name) : Term.TermElabM Unit := do
      if (← getEnv).contains name then return
      match fuel with
      | 0 => throwError "type dependency recursion exhausted"
      | fuel + 1 =>
        if name == `FermatCatalanConjecture.FCBExtractionTarget then
          throwError "temporary proof entered expected type"
        let some ci := elaborated.find? name | throwError "missing dependency {name}"
        let decl ← match ci with
          | .defnInfo value => pure (Declaration.defnDecl value)
          | .thmInfo value => pure (Declaration.thmDecl value)
          | _ => throwError "unexpected generated dependency {name}"
        for dep in ci.type.getUsedConstants do retain fuel dep
        if let some value := ci.value? then
          for dep in value.getUsedConstants do retain fuel dep
        addAndCompile decl
    for dep in expected.getUsedConstants do retain 10000 dep
    addAndCompile <| .defnDecl {
      name := `FCBTrustedSpec.ExpectedType
      levelParams := levels
      type := ← Meta.inferType expected
      value := expected
      hints := .abbrev
      safety := .safe
    }
end FermatCatalanConjecture
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
