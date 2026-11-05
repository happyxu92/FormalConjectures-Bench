import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`ModularityConjecture.modularity_conjecture).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType,
      `ModularityConjecture.modularFormAn, `ModularityConjecture.ratRed,
      `ModularityConjecture.setOfPointsModN, `ModularityConjecture.apFintype,
      `ModularityConjecture.WeierstrassCurve.ap,
      `ModularityConjecture.IsNormalisedEigenform,
      `ModularityConjecture.modularityConjecture] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args body => do
      unless args.size == 2 do throwError "expected E and IsElliptic instance binders"
      let e ← args[0]!.fvarId!.getDecl
      let inst ← args[1]!.fvarId!.getDecl
      unless e.binderInfo == .default && inst.binderInfo == .instImplicit do
        throwError "incorrect binder information"
      logInfo m!"complete binder 0: {e.userName}, explicit, {e.type}"
      logInfo m!"complete binder 1: {inst.userName}, instance-implicit, {inst.type}"
      logInfo m!"complete result: {body}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
