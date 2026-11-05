import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green38.green_38.variants.best_upper).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let mut body := info.value
  let mut binders := 0
  while body matches .forallE .. do
    let .forallE _ _ next _ := body | unreachable!
    binders := binders + 1
    body := next
  unless binders == 2 do throwError "unexpected full binder count: {binders}"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green38.𝔽₇,
      `Green38.IntersectsOnlyAtZero, `Green38.ValidCardinalities,
      `Green38.LargestAdmissibleCardinality, `Green38.C₁, `Green38.C₂] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"complete outer binders: {binders}; ordered universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
