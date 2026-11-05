import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green14.W_3_14).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let expected := mkApp3 (mkConst ``Eq [Level.succ Level.zero]) (mkConst ``Nat)
    (mkApp2 (mkConst `Green14.W) (mkNatLit 3) (mkNatLit 14)) (mkNatLit 186)
  unless info.value == expected do throwError "unexpected complete type expression"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green14.W, `Green14.mixedMonoAPGuaranteeSet] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo "complete outer binder count: 0"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Green14.W
#print Green14.mixedMonoAPGuaranteeSet
#print axioms FCBTrustedSpec.ExpectedType
