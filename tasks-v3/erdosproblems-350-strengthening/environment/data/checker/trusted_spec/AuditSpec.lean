import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos350.erdos_350.variants.strengthening).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos350.DecidableDistinctSubsetSums,
                `Erdos350.DistinctSubsetSums] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let mut value := info.value
  let mut binders := #[]
  while value.isForall do
    match value with
    | .forallE name _ body _ =>
      binders := binders.push name
      value := body
    | _ => break
  unless binders == #[`A, `hA, `s, `hs] do
    throwError "incorrect complete binders: {binders}"
  logInfo m!"complete binders: {binders}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos350.DecidableDistinctSubsetSums
#print Erdos350.DistinctSubsetSums
#print axioms FCBTrustedSpec.ExpectedType
