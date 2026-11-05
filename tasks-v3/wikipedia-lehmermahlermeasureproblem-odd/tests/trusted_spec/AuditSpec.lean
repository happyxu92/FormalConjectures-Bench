import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`LehmerMahlerMeasureProblem.lehmer_mahler_measure_problem.variants.odd).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType,
      `LehmerMahlerMeasureProblem.mahlerMeasure,
      `LehmerMahlerMeasureProblem.mahlerMeasureZ,
      `LehmerMahlerMeasureProblem.Polynomial.HasOddCoeffs] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec binderCount : Expr → Nat
    | .forallE _ _ body _ => 1 + binderCount body
    | _ => 0
  let count := binderCount info.value
  unless count == 3 do throwError "expected full three binders f, hf, hf'"
  logInfo m!"complete outer binder count: {count}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print LehmerMahlerMeasureProblem.mahlerMeasure
#print LehmerMahlerMeasureProblem.mahlerMeasureZ
#print LehmerMahlerMeasureProblem.Polynomial.HasOddCoeffs
#print axioms FCBTrustedSpec.ExpectedType
