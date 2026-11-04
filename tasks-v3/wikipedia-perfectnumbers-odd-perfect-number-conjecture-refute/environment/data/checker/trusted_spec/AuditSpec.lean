import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `PerfectNumbers.formal_conjectures_bench_refutation then
    throwError "temporary target theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType is not a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Nat.Perfect] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted transitive axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  unless info.value.isAppOfArity `Not 1 do throwError "missing outer negation"
  liftTermElabM do
    Meta.forallTelescope info.value.appArg! fun args _ => do
      unless args.size == 2 do throwError "lost quantified arguments"
      logInfo m!"quantified arguments: {args}"
  logInfo m!"universe parameters: {info.levelParams}; all quantified arguments retained"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
