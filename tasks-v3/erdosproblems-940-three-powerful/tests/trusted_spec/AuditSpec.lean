import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos940.erdos_940.variants.three_powerful).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  -- This task's complete target is an Eventually expression, not an outer Pi.
  match info.value with
  | .forallE .. => throwError "unexpected outer binder"
  | _ => pure ()
  logInfo m!"ExpectedType transitive axioms: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}; outer binder count: 0"
  logInfo m!"complete raw expression: {repr info.value}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
