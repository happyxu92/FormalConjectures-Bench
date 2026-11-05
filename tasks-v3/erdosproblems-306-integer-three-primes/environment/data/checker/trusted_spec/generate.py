"""Repair-time only: elaborate this task's golden declaration in isolation."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos306')].strip()
source = prefix + '''
-- Extract the complete elaborated type and universes, discard the placeholder.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos306.erdos_306.variants.integer_three_primes
    | throwError "missing temporary target"
  let temporary ← getEnv
  let mut expected := info.type
  -- Index bounds proved by omega produce private auxiliary proof constants.
  -- Inline their checked values, not the placeholder theorem, before rollback.
  for _ in [:100] do
    expected := expected.replace fun e => do
      let .const name levels := e | none
      if !(`Erdos306.erdos_306.variants.integer_three_primes).isPrefixOf name then none
      else do
        let ci ← temporary.find? name
        let value ← ci.value? (allowOpaque := true)
        return value.instantiateLevelParams ci.levelParams levels
  for name in expected.getUsedConstants do
    if (`Erdos306.erdos_306.variants.integer_three_primes).isPrefixOf name then
      throwError "unexpanded temporary reference {name}"
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
end Erdos306
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
