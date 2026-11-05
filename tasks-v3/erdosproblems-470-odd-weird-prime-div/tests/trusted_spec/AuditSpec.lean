import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos470.erdos_470.variants.odd_weird_prime_div).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos470.PrimitiveWeird,
      `Erdos470.AbundancyIndex] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let count := (let rec go : Expr → Nat
    | .forallE _ _ body _ => 1 + go body
    | _ => 0
    go info.value)
  unless count == 3 do throwError "expected all three binders (n, Odd n, n.Weird), got {count}"
  logInfo m!"complete outer binder count: {count}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos470.PrimitiveWeird
#print Erdos470.AbundancyIndex
#print axioms FCBTrustedSpec.ExpectedType
