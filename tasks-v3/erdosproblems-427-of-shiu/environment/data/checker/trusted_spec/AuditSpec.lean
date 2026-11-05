import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos427.erdos_427.variants.of_shiu).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos427.erdos427, `Erdos427.ShiuTheorem] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    let .forallE _ domain body binder := info.value
      | throwError "missing complete H binder"
    unless domain == .const `Erdos427.ShiuTheorem [] do
      throwError "wrong hypothesis type"
    unless body == .const `Erdos427.erdos427 [] do
      throwError "wrong conclusion"
    unless binder == .default do throwError "wrong binder visibility"
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 1 do throwError "expected exactly the explicit H binder"
      logInfo m!"complete binder count: {args.size}; explicit H : Erdos427.ShiuTheorem"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
