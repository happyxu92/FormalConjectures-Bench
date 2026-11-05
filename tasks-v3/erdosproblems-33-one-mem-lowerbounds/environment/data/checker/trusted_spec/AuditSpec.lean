import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos33.erdos_33).isPrefixOf name then
      throwError "temporary or unrelated theorem exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos33.AdditiveBasisCondition] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in closed existential proposition"
  | _ => logInfo "complete outer binder count: 0; full existential retained"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos33.AdditiveBasisCondition
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos33.AdditiveBasisCondition
