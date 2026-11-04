import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos41.formal_conjectures_bench_refutation then
    throwError "temporary target theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos41.NtupleCondition] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 0 do throwError "unexpected outer binders"
    unless info.value.isAppOfArity ``Not 1 do throwError "expected negation"
    Meta.forallTelescope info.value.appArg! fun args _ => do
      unless args.size == 5 do throwError "lost implicit, instance, set or hypothesis binders"
      logInfo m!"negated universal binder count: {args.size} (implicit type, instance, set, two hypotheses)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
