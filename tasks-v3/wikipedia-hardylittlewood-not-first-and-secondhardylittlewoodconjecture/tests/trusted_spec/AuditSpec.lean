import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`HardyLittlewood.not_first_and_secondHardyLittlewoodConjecture).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  for name in #[`FCBTrustedSpec.ExpectedType,
      `HardyLittlewood.IsPrimeConstellation,
      `HardyLittlewood.IsAdmissiblePrimeConstellation,
      `HardyLittlewood.Nat.numResidues,
      `HardyLittlewood.Nat.primeTupleCounting,
      `HardyLittlewood.FirstHardyLittlewoodConjectureFor,
      `HardyLittlewood.SecondHardyLittlewoodConjectureFor] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let .forallE _ first _ _ := info.value
    | throwError "missing full implication binder"
  let .forallE _ _ tail binder := first
    | throwError "missing implicit k binder"
  unless binder == .implicit do throwError "k binder not implicit"
  let .forallE _ _ _ binder := tail
    | throwError "missing explicit m binder"
  unless binder == .default do throwError "m binder not explicit"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
