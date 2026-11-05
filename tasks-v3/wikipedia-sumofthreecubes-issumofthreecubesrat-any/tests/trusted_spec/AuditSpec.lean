import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`SumOfThreeCubes.isSumOfThreeCubesRat_any).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  match info.value with
  | .forallE name domain body binderInfo =>
    unless name == `r && domain == .const `Rat [] && binderInfo == .default do
      throwError "incorrect complete outer binder"
    if body.isForall then throwError "unexpected extra binder"
    logInfo m!"complete outer binder: {name} : {domain}, explicit; body: {body}"
  | _ => throwError "missing rational argument"
  for name in #[`FCBTrustedSpec.ExpectedType, `SumOfThreeCubes.IsSumOfThreeCubes,
      `SumOfThreeCubes.isSumOfThreeCubes_2, `SumOfThreeCubes.isSumOfThreeCubes_33,
      `SumOfThreeCubes.isSumOfThreeCubes_42, `SumOfThreeCubes.mod_9_of_isSumOfThreeCubes] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.all true in
#print FCBTrustedSpec.ExpectedType
#print SumOfThreeCubes.IsSumOfThreeCubes
#print axioms FCBTrustedSpec.ExpectedType
