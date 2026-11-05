import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Brocard.brocard_conjecture.ferreira_large_n).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted axiom {ax} in ExpectedType"
  -- The unrelated open Brocard conjecture remains in the frozen prefix.
  -- It must NOT be referenced by the expected proposition.
  -- collectAxioms traverses all transitive dependencies, including prefix ones.
  logInfo m!"audited ExpectedType transitive axioms: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in closed eventuality proposition"
  | _ => logInfo "complete outer binder count: 0; eventual variable is internal to Filter.Eventually"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
