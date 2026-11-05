import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos939.erdos_939.variants.euler then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Erdos939.erdos_939.variants.euler).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos939.Erdos939Sums] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    unless info.value.isAppOfArity `Not 1 do
      throwError "expected negation of the complete universal statement"
    Meta.forallTelescope info.value.getAppArgs[0]! fun args _ => do
      unless args.size == 4 do throwError "expected k, k ≥ 4, S, and cardinality equality"
      logInfo m!"complete universal binder count under Not: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
