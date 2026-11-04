import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos137.erdos_137 then
    throwError "temporary theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType and all transitive dependencies: {axioms}"
  logInfo m!"universe parameters (ordered): {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
