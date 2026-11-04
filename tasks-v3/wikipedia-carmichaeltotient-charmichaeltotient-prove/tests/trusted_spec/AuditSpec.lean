import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `CarmichaelTotient.charmichaelTotient then
    throwError "temporary theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  -- This traverses types and definition values, including the trusted prefix.
  for name in #[`FCBTrustedSpec.ExpectedType, `CarmichaelTotient.CarmichaelTotientFor,
                `CarmichaelTotient.carchimichealTotientFor_zero,
                `CarmichaelTotient.carmichealTotientFor_odd] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters (ordered): {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
