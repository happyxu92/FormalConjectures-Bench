import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos888.erdos_888.variants.primes then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Erdos888.erdos_888.variants.primes).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos888.p, `Erdos888.RequiredCondition] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in this closed asymptotic proposition"
  | _ => logInfo "complete outer binder count: 0 (original elaborated expression)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos888.p
#print axioms Erdos888.p
#print axioms FCBTrustedSpec.ExpectedType
