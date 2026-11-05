import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos304.erdos_304.variants.upper_1950).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for (name, _) in env.constants.toList do
    if name == `FCBTrustedSpec.ExpectedType || (`Erdos304).isPrefixOf name then
      let axioms ← collectAxioms name
      for ax in axioms do
        unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
          throwError "untrusted axiom {ax} in {name}"
      logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in this closed asymptotic proposition"
  | _ => logInfo "complete outer binder count: 0 (function arguments are inside IsBigO)"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.all true in
#print FCBTrustedSpec.ExpectedType
#print Erdos304.unitFractionExpressible
#print Erdos304.smallestCollection
#print Erdos304.smallestCollectionTo
#print axioms FCBTrustedSpec.ExpectedType
