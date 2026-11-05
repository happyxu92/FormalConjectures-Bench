import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `BeaverMathOlympiad.beaver_math_olympiad_problem_3
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType and its transitive references: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun binders body => do
      unless binders.size == 3 do throwError "lost full theorem parameters"
      for binder in binders do
        logInfo m!"complete binder: {binder} : {← Meta.inferType binder}"
      logInfo m!"complete conclusion: {body}"
  logInfo m!"ordered universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
