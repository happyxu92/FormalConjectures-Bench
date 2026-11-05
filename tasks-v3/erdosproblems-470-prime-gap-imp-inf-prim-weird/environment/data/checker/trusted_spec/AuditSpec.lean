import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `Erdos470.erdos_470.variants.prime_gap_imp_inf_prim_weird
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos470.PrimitiveWeird,
                 `Erdos470.AbundancyIndex] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.isEmpty do throwError "unexpected outer parameters"
      logInfo m!"complete outer binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.all true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
