import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `Erdos69.erdos_69.variants.specialisation_of_erdos_257
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
  match info.value with
  | .letE .. => logInfo "complete type starts with original let A; no outer forall binders"
  | _ => throwError "unexpected full type shape"
  logInfo m!"universe parameters: {info.levelParams}"
  logInfo m!"ExpectedType transitive axioms: {axioms}"
  -- The unrelated original prefix theorem erdos_69 has a baseline placeholder;
  -- it must not occur in this target type or any of its dependencies.
  unless !(axioms.contains `sorryAx) do throwError "placeholder dependency"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
