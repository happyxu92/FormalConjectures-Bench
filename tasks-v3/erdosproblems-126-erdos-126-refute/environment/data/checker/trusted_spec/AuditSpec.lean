import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos126.formal_conjectures_bench_refutation).isPrefixOf name then
      throwError "temporary theorem or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos126.IsMaximalAddFactorsCard] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.isEmpty do throwError "unexpected outer binders on negation"
      logInfo m!"complete outer binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos126.IsMaximalAddFactorsCard
#print axioms FCBTrustedSpec.ExpectedType
