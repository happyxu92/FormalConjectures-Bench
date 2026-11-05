import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos672.erdos_672.variants.euler).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos672.Erdos672With] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    unless info.value == (mkApp2 (mkConst `Erdos672.Erdos672With) (mkNatLit 4) (mkNatLit 2)) do
      throwError "unexpected complete target type expression"
    Meta.withTransparency .all <| Meta.forallTelescopeReducing info.value fun args _ => do
      -- Nine explicit/hypothesis binders plus the negated equality's premise.
      unless args.size == 10 do throwError "expected ten reduced binders, got {args.size}"
      logInfo m!"complete expanded binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos672.Erdos672With
#print axioms FCBTrustedSpec.ExpectedType
