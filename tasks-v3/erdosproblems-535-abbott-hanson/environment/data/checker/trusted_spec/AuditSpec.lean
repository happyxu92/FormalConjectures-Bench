import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos535.erdos_535.variants.abbott_hanson).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos535.f,
                `Erdos535.AllBigOmega, `Erdos535.NoConstantPairwiseGcdCoprimeSubsets] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  -- The complete type starts with the implicit natural r and the hypothesis
  -- hr : 3 ≤ r, not just the proposition elaborated with r as a free variable.
  match info.value with
  | .forallE r rType (.forallE hr _ _ hrBI) rBI =>
    unless r == `r && hr == `hr && rType == .const `Nat [] &&
        rBI == .implicit && hrBI == .default do
      throwError "missing original r/hr parameters"
  | _ => throwError "missing full outer binders"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos535.f
#print axioms FCBTrustedSpec.ExpectedType
