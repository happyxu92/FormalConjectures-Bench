import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `ArtinPrimitiveRootsConjecture.conditional_artin_primitive_roots.variants.part_ii_power_squarefreePart_not_modeq_one
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType,
      `ArtinPrimitiveRootsConjecture.S, `ArtinPrimitiveRootsConjecture.ArtinConstant,
      `ArtinPrimitiveRootsConjecture.powCorrectionFactor,
      `ArtinPrimitiveRootsConjecture.entanglementFactor] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 9 do throwError "expected a m b ha hb hm₁ hm₂ hb' h"
      for arg in args do
        logInfo m!"binder {arg}: {← Meta.inferType arg}"
      logInfo m!"complete binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
