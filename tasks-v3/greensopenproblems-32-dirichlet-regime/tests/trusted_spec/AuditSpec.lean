import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green32.green_32.variants.dirichlet_regime).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  if info.value.hasSorry then throwError "sorry in expected expression"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green32.HasGap, `Green32.HasLargeGapDilate] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder (golden is a closed existential)"
  | .app (.app (.const `Exists _) _) _ => pure ()
  | _ => throwError "expected closed existential expression"
  logInfo "complete outer binder count: 0; quantified binders retained in the original elaborated expression"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Green32.HasGap
#print Green32.HasLargeGapDilate
#print axioms FCBTrustedSpec.ExpectedType
