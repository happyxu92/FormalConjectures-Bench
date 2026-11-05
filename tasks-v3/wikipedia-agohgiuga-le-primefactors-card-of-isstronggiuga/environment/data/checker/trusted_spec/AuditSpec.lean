import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `AgohGiuga.agoh_giuga.variants.le_primeFactors_card_of_isStrongGiuga
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
    Meta.forallTelescope info.value fun args body => do
      unless args.size == 2 do throwError "expected full binders a and ha"
      let aType ← Meta.inferType args[0]!
      let haType ← Meta.inferType args[1]!
      unless ← Meta.isDefEq aType (mkConst `Nat) do
        throwError "first binder is not Nat"
      unless ← Meta.isDefEq haType (mkApp (mkConst `AgohGiuga.IsStrongGiuga) args[0]!) do
        throwError "hypothesis type changed"
      logInfo m!"complete binder count: {args.size}; conclusion: {body}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
