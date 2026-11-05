import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos683.erdos_683.variant.sylvester_schur).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos683.P] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec countBinders : Expr → Nat
    | .forallE _ _ body _ => 1 + countBinders body
    | _ => 0
  let binders := countBinders info.value
  unless binders == 3 do throwError "expected all n, k, and hypothesis binders; got {binders}"
  logInfo m!"complete outer binder count: {binders}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos683.P
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos683.P
