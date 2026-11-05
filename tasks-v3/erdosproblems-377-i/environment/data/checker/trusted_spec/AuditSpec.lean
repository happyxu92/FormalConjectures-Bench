import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos377.erdos_377.variants.limit.i).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos377.sumInvPrimesNotDvdCentralBinom] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let mut value := info.value
  let mut binders := #[]
  repeat
    match value with
    | .forallE name _ body binderInfo =>
      binders := binders.push (name, binderInfo)
      value := body
    | _ => break
  unless binders.size == 2 do throwError "expected both gamma and equality binders"
  logInfo m!"complete outer binders (name, binderInfo): {reprStr binders}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos377.sumInvPrimesNotDvdCentralBinom
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos377.sumInvPrimesNotDvdCentralBinom
