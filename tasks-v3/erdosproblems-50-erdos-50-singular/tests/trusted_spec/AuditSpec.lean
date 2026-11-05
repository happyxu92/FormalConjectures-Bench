import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos50.erdos_50_singular).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos50.IsDistributionOfPhiRatio,
                `Erdos50.IsPurelySingular] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args body => do
      unless args.size == 2 do throwError "expected f and the complete distribution hypothesis"
      let f := args[0]!
      let hf := args[1]!
      unless ← Meta.isDefEq (← Meta.inferType f)
          (← Elab.Term.elabTerm (← `(Real → Real)) none) do
        throwError "incorrect f binder type"
      unless ← Meta.isDefEq (← Meta.inferType hf)
          (mkApp (.const `Erdos50.IsDistributionOfPhiRatio []) f) do
        throwError "incorrect distribution hypothesis"
      unless ← Meta.isDefEq body
          (mkApp (.const `Erdos50.IsPurelySingular []) f) do
        throwError "incorrect conclusion"
      logInfo m!"complete binder count: {args.size}; f : Real → Real; hf : IsDistributionOfPhiRatio f"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
