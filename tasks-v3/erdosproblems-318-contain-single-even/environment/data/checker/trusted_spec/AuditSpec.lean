import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `Erdos318.erdos_318.variants.contain_single_even
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos318.P₁] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE n _ (.forallE h _ body biH) biA =>
    unless n == `A && h == `hA && biA == .implicit && biH == .default do
      throwError "full parameter names/binder kinds changed"
    match body with
    | .forallE .. => throwError "unexpected extra binder"
    | _ => logInfo "complete outer binders: {A : Set ℕ} (hA : {n | n ∈ A ∧ Even n}.ncard = 1)"
  | _ => throwError "missing full implicit A and explicit hA parameters"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos318.P₁
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos318.P₁
