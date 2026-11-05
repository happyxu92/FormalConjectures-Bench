import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos36.erdos_36.variants.exists).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos36.MinOverlapQuotient,
                 `Erdos36.M, `Erdos36.MaxOverlap, `Erdos36.Overlap] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in closed existential proposition"
  | _ => logInfo "complete outer binder count: 0; existential witness retained inside expression"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos36.MinOverlapQuotient
#print Erdos36.M
#print Erdos36.MaxOverlap
#print Erdos36.Overlap
#print axioms FCBTrustedSpec.ExpectedType
