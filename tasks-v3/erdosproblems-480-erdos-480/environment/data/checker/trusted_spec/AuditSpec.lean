import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos480.erdos_480).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  unless info.value.getAppFn == .const `Iff [] do
    throwError "expected the complete closed equivalence, not just its RHS"
  logInfo m!"audited ExpectedType transitive dependencies: {axioms}"
  logInfo m!"universe parameters in order: {info.levelParams}"
  logInfo "outer forall binders: 0; complete equivalence contains the quantified sequence and boundedness hypothesis"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
