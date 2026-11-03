from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
pkg.mkdir(exist_ok=True)
golden = (pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos264')].strip()
source = prefix + '''
-- Generated from the trusted golden Target, without candidate imports.
-- Elaborate the complete declaration, retain its type, then discard the
-- temporary theorem environment before exporting the kernel-checked definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos264.erdos_264.variants.ko_tao_pos
    | throwError "missing temporary target"
  -- Inline only fresh definitions referenced by the type (e.g. pair matchers).
  -- Never retain the temporary theorem or its proof, and preserve prefix names.
  let expected ← liftCoreM <| Core.transform info.type (pre := fun e => do
    if let .const name levels := e then
      unless original.contains name do
        let ci ← getConstInfo name
        match ci with
        | .defnInfo _ =>
          logInfo m!"inlined fresh target-type auxiliary {name}"
          return .visit (← Core.instantiateValueLevelParams ci levels)
        | _ => throwError "non-definition fresh dependency {name}"
    return .continue)
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
end Erdos264
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
