import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos851.erdos_851 then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Erdos851.erdos_851).isPrefixOf name && name != `Erdos851.erdos_851.variants.romanoff then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos851.TwoPowAddSet] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec countBinders : Expr → Nat
    | .forallE _ _ b _ => countBinders b + 1
    | _ => 0
  unless countBinders info.value == 2 do
    throwError "expected both original explicit parameters ε and hε"
  logInfo "complete outer binder count: 2 (ε : ℝ) (hε : ε ∈ Set.Ioo 0 1)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos851.TwoPowAddSet
#print axioms Erdos851.TwoPowAddSet
#print axioms FCBTrustedSpec.ExpectedType
