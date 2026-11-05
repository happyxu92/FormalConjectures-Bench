import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos427.erdos_427.variants.shiu).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  unless info.value == mkConst `Erdos427.ShiuTheorem do
    throwError "ExpectedType is not the original ShiuTheorem definition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos427.ShiuTheorem, `Erdos427.erdos427] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    let full ← Meta.whnf info.value
    Meta.forallTelescope full fun args _ => do
      unless args.size == 6 do
        throwError "expected all six binders: k, a, q, positive k, positive q, coprimality"
      logInfo m!"complete unfolded binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos427.ShiuTheorem
#print axioms FCBTrustedSpec.ExpectedType
