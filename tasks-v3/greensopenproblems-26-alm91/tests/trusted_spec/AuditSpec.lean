import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Green26.green_26.variants.alm91 then
    throwError "temporary theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 2 do throwError "expected p and the prime Fact instance"
      logInfo m!"complete forall telescope: {args.size} parameters (p, Fact p.Prime)"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green26.𝔽, `Green26.𝔽₃, `Green26.StandardCube, `Green26.IsCube] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
