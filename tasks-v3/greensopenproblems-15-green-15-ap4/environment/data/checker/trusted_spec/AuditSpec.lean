import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green15.green_15_ap4).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  -- The other frozen conjecture has a placeholder, but must not contribute to
  -- this target type, either directly or through any prefix dependency.
  if axioms.contains `sorryAx then throwError "placeholder reached ExpectedType"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in this closed existential proposition"
  | _ => logInfo "complete outer binder count: 0; full existential proposition retained"
  logInfo m!"audited ExpectedType transitive axioms: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
