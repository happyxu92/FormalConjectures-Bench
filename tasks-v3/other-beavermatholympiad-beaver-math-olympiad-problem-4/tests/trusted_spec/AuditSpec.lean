import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`BeaverMathOlympiad.beaver_math_olympiad_problem_4).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType transitive dependencies: {axioms}"
  let mut value := info.value
  let mut names : Array Name := #[]
  while value.isForall do
    match value with
    | .forallE name _ body _ =>
      names := names.push name
      value := body
    | _ => pure ()
  unless names == #[`a, `a_ini, `a_rec] do
    throwError "unexpected complete binders: {names}"
  logInfo m!"complete outer binders: {names}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
