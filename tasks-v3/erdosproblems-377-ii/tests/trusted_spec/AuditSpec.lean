import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos377.erdos_377.variants.limit.ii).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos377.sumInvPrimesNotDvdCentralBinom] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec countBinders : Expr → Nat
    | .forallE _ _ body _ => 1 + countBinders body
    | _ => 0
  unless countBinders info.value == 2 do
    throwError "expected both gamma and its defining equality binders"
  logInfo "complete outer binder count: 2 (gamma and its defining equality)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos377.sumInvPrimesNotDvdCentralBinom
#print axioms Erdos377.sumInvPrimesNotDvdCentralBinom
#print axioms FCBTrustedSpec.ExpectedType
