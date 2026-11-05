import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`AgohGiuga.agoh_giuga.variants.isStrongGiuga_growth).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `AgohGiuga.IsStrongGiuga] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"transitively audited {name}: {axioms}"
  let rec countBinders : Expr → Nat
    | .forallE _ _ body _ => 1 + countBinders body
    | _ => 0
  unless countBinders info.value == 2 do throwError "expected G and hG binders"
  logInfo m!"complete outer binders: 2; ordered universes: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print AgohGiuga.IsStrongGiuga
#print axioms FCBTrustedSpec.ExpectedType
#print axioms AgohGiuga.IsStrongGiuga
