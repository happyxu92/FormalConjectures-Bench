import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`SierpinskiNumber.selfridge_78557).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let expected := mkApp (mkConst `Nat.IsSierpinskiNumber) (mkNatLit 78557)
  unless info.value == expected do throwError "unexpected complete expression: {info.value}"
  for name in #[`FCBTrustedSpec.ExpectedType, `Nat.IsSierpinskiNumber] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"complete outer binder count: 0; universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Nat.IsSierpinskiNumber
#print axioms FCBTrustedSpec.ExpectedType
