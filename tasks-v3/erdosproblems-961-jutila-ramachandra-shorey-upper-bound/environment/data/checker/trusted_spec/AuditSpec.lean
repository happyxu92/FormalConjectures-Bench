import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos961.erdos_961.variants.jutila_ramachandra_shorey_upper_bound then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Erdos961.erdos_961.variants.jutila_ramachandra_shorey_upper_bound).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos961.f,
      `Erdos961.erdos_961.variants.well_defined] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 0 do throwError "expected no outer binders"
      logInfo m!"complete binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos961.erdos_961.variants.well_defined
-- This original, unused theorem remains unproved, but is outside the audited closure.
#print axioms Erdos961.erdos_961.sylvester_schur
