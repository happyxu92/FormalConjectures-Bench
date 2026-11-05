import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green24.variants.upper_trivial).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  match info.value with
  | .forallE n ty body bi =>
    unless n == `n && ty == .const `Nat [] && bi == .implicit do
      throwError "wrong implicit natural parameter"
    match body with
    | .forallE .. => throwError "unexpected extra outer parameter"
    | _ => pure ()
  | _ => throwError "missing full implicit parameter n"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green24.max013AffineTranslates] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters in order: {info.levelParams}"
  logInfo "complete outer parameter: {n : Nat} (implicit)"
#print FCBTrustedSpec.ExpectedType
#print Green24.max013AffineTranslates
#print axioms FCBTrustedSpec.ExpectedType
