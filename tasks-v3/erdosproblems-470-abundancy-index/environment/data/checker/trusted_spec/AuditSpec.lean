import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos470.erdos_470.variants.abundancy_index).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos470.AbundancyIndex, `Erdos470.PrimitiveWeird] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun xs body => do
      unless xs.size == 3 do throwError "unexpected complete binder count: {xs.size}"
      for x in xs do
        logInfo m!"complete binder: {x} : {← Meta.inferType x}"
      logInfo m!"complete body: {body}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos470.AbundancyIndex
#print Erdos470.PrimitiveWeird
#print axioms FCBTrustedSpec.ExpectedType
