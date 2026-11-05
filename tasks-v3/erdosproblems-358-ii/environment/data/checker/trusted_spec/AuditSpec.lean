import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos358.erdos_358.parts.ii).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType,
      `Erdos358.intervalRepresentations, `Erdos358.f,
      `Erdos358.intervalRepresentationsNonTrivial, `Erdos358.g] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  -- The original target has no declaration binders; its entire iff/existential
  -- proposition is the value, not just a consequent or the type Prop itself.
  unless info.value.isAppOfArity ``Iff 2 do
    throwError "expected a complete outer iff proposition"
  logInfo "complete outer binder count: 0; complete iff proposition retained"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos358.intervalRepresentations
#print Erdos358.f
#print axioms FCBTrustedSpec.ExpectedType
