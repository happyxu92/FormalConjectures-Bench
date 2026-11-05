import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `Erdos707.erdos_707.variants.counterexample_hall
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  let mut expr := info.value
  let mut count : Nat := 0
  while expr.isForall do
    count := count + 1
    expr := expr.bindingBody!
  unless count == 2 do throwError "expected full A and hA binders; got {count}"
  logInfo m!"complete outer binder count: {count}; universe parameters: {info.levelParams}"
  logInfo m!"transitive ExpectedType axioms: {axioms}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
