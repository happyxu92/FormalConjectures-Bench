import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`AgohGiuga.isWeakGiuga_iff_sum_primeFactors).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  let rec countBinders : Expr → Nat
    | .forallE _ _ body _ => countBinders body + 1
    | _ => 0
  unless countBinders info.value == 2 do throwError "lost full n/hn binders"
  match info.value with
  | .forallE `n (.const `Nat []) (.forallE `hn _ _ .default) .implicit => pure ()
  | _ => throwError "incorrect binder names, types or explicitness"
  for name in #[`FCBTrustedSpec.ExpectedType, `AgohGiuga.AgohGiugaCongr,
      `AgohGiuga.AgohGiugaSum, `AgohGiuga.IsWeakGiuga, `AgohGiuga.IsStrongGiuga] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"complete outer binders: 2 (implicit n : Nat, explicit hn : n.Composite)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print AgohGiuga.IsWeakGiuga
#print axioms FCBTrustedSpec.ExpectedType
