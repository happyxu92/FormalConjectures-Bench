import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos697.erdos_697.parts.i).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not a proposition"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 2 do throwError "expected complete binders α and hα"
      let aType ← Meta.inferType args[0]!
      let hType ← Meta.inferType args[1]!
      unless ← Meta.isDefEq aType (mkConst ``Real) do throwError "α is not Real"
      unless ← Meta.isProp hType do throwError "hα is not a proposition"
      let aInfo ← args[0]!.fvarId!.getDecl
      let hInfo ← args[1]!.fvarId!.getDecl
      unless aInfo.binderInfo == .implicit && hInfo.binderInfo == .default do
        throwError "binder visibility changed"
      logInfo m!"complete binders: implicit α : {aType}; explicit hα : {hType}"
  logInfo m!"universe parameters: {info.levelParams}"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos697.δ, `Erdos697.density_exists] do
    let axioms ← collectAxioms name
    logInfo m!"audit {name}: {axioms}"
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
#print FCBTrustedSpec.ExpectedType
#print Erdos697.density_exists
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos697.δ
#print axioms Erdos697.density_exists
-- Unreferenced frozen auxiliary: not in ExpectedType's dependency closure.
#print axioms Erdos697.erdos_697.variants.delta_lt
