import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green18.green_18.bmz_corners).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams == [`u_1] do throwError "unexpected universes: {info.levelParams}"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green18.numBmzCorners, `Green18.numNaiveCorners] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 2 do throwError "expected alpha and its positivity hypothesis"
      logInfo m!"complete outer binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.universes true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
