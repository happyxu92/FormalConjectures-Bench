import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`EllipticCurveRank.RatEllipticCurve._02062_le_density_rank_zero).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType,
      `EllipticCurveRank.RatEllipticCurve,
      `EllipticCurveRank.RatEllipticCurve.toWeierstrass,
      `EllipticCurveRank.RatEllipticCurve.rank,
      `EllipticCurveRank.RatEllipticCurve.naiveHeight,
      `EllipticCurveRank.RatEllipticCurve.heightLE] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in this closed density proposition"
  | _ => logInfo "complete outer binder count: 0; H and E are internal bound variables"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
#print EllipticCurveRank.RatEllipticCurve.rank
#print EllipticCurveRank.RatEllipticCurve.heightLE
