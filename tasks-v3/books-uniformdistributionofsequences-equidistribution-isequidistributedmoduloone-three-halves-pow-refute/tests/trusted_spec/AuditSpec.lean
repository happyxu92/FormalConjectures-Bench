import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Equidistribution.formal_conjectures_bench_refutation then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Equidistribution.formal_conjectures_bench_refutation).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Equidistribution.IsEquidistributed, `Equidistribution.IsEquidistributedModuloOne] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 0 do throwError "expected no outer binders"
      logInfo m!"complete binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
