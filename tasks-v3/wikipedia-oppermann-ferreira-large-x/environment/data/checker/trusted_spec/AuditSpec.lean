import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Oppermann.oppermann_conjecture.ferreira_large_x).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  -- There are no outer theorem binders; x is bound inside Filter.Eventually.
  match info.value with
  | .forallE .. => throwError "unexpected outer theorem binder"
  | _ => pure ()
  logInfo m!"audited ExpectedType and all transitive dependencies: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}; outer binders: 0"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
