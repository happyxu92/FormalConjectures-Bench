import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos245.erdos_245 then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Erdos245.erdos_245).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 0 do throwError "expected zero target binders"
      logInfo m!"complete binder count: {args.size}"
      let some (_, rhs) := info.value.app2? ``Iff | throwError "expected iff"
      Meta.forallTelescope rhs fun rhsArgs _ => do
        unless rhsArgs.size == 3 do throwError "expected A, infinitude and density-zero binders on RHS"
        logInfo m!"RHS binder count: {rhsArgs.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
