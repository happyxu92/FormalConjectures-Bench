import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`CongruentNumber.Tunnell_odd).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let rec binders : Expr → Nat
    | .forallE _ _ b _ => 1 + binders b
    | _ => 0
  unless binders info.value == 4 do throwError "expected n, hsqf, hodd and congruence hypothesis"
  for name in #[`FCBTrustedSpec.ExpectedType, `CongruentNumber.congruentNumber,
      `CongruentNumber.A, `CongruentNumber.B, `CongruentNumber.C, `CongruentNumber.D] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"complete outer binders: 4; universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print CongruentNumber.congruentNumber
#print CongruentNumber.A
#print CongruentNumber.B
#print axioms FCBTrustedSpec.ExpectedType
