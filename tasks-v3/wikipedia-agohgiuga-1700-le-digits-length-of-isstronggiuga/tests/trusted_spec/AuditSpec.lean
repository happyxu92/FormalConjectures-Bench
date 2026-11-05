import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `AgohGiuga.agoh_giuga.variants._1700_le_digits_length_of_isStrongGiuga
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `AgohGiuga.IsStrongGiuga] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun binders body => do
      unless binders.size == 2 do throwError "expected all two target binders"
      unless (← Meta.inferType binders[0]!) == mkConst `Nat do
        throwError "first binder is not Nat"
      let hypothesisType ← Meta.inferType binders[1]!
      unless hypothesisType == mkApp (mkConst `AgohGiuga.IsStrongGiuga) binders[0]! do
        throwError "second binder is not IsStrongGiuga a"
      logInfo m!"complete binder count: {binders.size}; conclusion: {body}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print AgohGiuga.IsStrongGiuga
#print axioms AgohGiuga.IsStrongGiuga
#print axioms FCBTrustedSpec.ExpectedType
