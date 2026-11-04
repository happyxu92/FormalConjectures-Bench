import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Hall.weak_hall_conjecture then
    throwError "temporary theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Hall.HallIneq, `Hall.HallConjectureExp] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted transitive axiom {ax}"
    logInfo m!"audited {name} and all transitive dependencies: {axioms}"
  logInfo m!"universe parameters (ordered): {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Hall.HallIneq
#print Hall.HallConjectureExp
#print axioms FCBTrustedSpec.ExpectedType
