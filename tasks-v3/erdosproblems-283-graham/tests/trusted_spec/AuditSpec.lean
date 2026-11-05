import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos283.erdos_283.variants.graham).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  match info.value.getAppFn with
  | .const name levels =>
    unless name == `Erdos283.Condition && levels.isEmpty && info.value.getAppNumArgs == 1 do
      throwError "ExpectedType does not contain the complete closed Condition proposition"
  | _ => throwError "unexpected complete type expression"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos283.Condition] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted transitive axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}; outer binders: 0; one polynomial argument"
#print FCBTrustedSpec.ExpectedType
#print Erdos283.Condition
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos283.Condition
