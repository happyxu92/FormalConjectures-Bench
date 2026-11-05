import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos346.erdos_346.variants.f_isAddStronglyCompleteNatSeq).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  -- Independently compare the saved value against the original closed type.
  -- This repair-time audit is compiled without any candidate in scope.
  liftTermElabM do
    let expected ← Term.elabTerm (← `(IsAddStronglyCompleteNatSeq Erdos346.f)) none
    unless ← Meta.isDefEq info.value expected do
      throwError "unexpected complete definition value"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos346.f] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in this closed sequence-completeness proposition"
  | _ => logInfo "complete outer binder count: 0"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos346.f
#print axioms Erdos346.f
#print axioms FCBTrustedSpec.ExpectedType
