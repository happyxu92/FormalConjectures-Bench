import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos442.erdos_442).isPrefixOf name then
      throwError "temporary theorem or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  -- collectAxioms traverses the stored value and all referenced prefix definitions.
  let mut names := #[`FCBTrustedSpec.ExpectedType]
  for (name, _) in env.constants.toList do
    if (`Erdos442).isPrefixOf name then names := names.push name
  for name in names do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in closed iff proposition"
  | _ => logInfo "complete outer binder count: 0; quantified A and implication stored inside iff"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos442.Real.maxLogOne
#print Erdos442.Set.bddProdUpper
#print axioms FCBTrustedSpec.ExpectedType
