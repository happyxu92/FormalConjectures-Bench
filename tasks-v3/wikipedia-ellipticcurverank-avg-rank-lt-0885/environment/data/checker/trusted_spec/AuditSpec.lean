import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `EllipticCurveRank.RatEllipticCurve.avg_rank_lt_0885
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType,
      `EllipticCurveRank.RatEllipticCurve.rank,
      `EllipticCurveRank.RatEllipticCurve.toWeierstrass,
      `EllipticCurveRank.RatEllipticCurve.naiveHeight,
      `EllipticCurveRank.RatEllipticCurve.heightLE] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in this closed average-rank proposition"
  | _ => logInfo "complete outer binder count: 0 (original elaborated expression)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print EllipticCurveRank.RatEllipticCurve.rank
#print EllipticCurveRank.RatEllipticCurve.heightLE
#print axioms FCBTrustedSpec.ExpectedType
