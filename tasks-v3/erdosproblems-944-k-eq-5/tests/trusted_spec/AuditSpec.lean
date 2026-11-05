import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos944.erdos_944.variants.dirac_conjecture.k_eq_5).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams == [`u] do throwError "unexpected universes: {info.levelParams}"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos944.SimpleGraph.IsErdos944] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer forall binder"
  | _ => logInfo "complete outer forall binder count: 0; existential V : Type u and graph retained"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos944.SimpleGraph.IsErdos944
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos944.SimpleGraph.IsErdos944
