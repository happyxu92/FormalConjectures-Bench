import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `ArtinPrimitiveRootsConjecture.artin_primitive_roots.variants.part_ii_square_or_minus_one
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `ArtinPrimitiveRootsConjecture.S] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec outerBinders : Expr → List Name
    | .forallE name _ body _ => name :: outerBinders body
    | _ => []
  let binders := outerBinders info.value
  unless binders == [`a, `ha] do
    throwError "unexpected complete binders: {binders}"
  logInfo m!"complete outer binders: {binders}"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print ArtinPrimitiveRootsConjecture.S
#print axioms FCBTrustedSpec.ExpectedType
