import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green32.green_32.variants.finite_field).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green32.HasCosetHole,
                `Green32.HasGap, `Green32.HasLargeGapDilate] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  -- The eventual quantifier is the head constant Filter.Eventually, not a Pi.
  match info.value with
  | .forallE .. => throwError "unexpected outer Pi binder"
  | _ => logInfo "complete outer Pi binder count: 0; eventual quantifier retained in expression"
  unless info.value.getAppFn.isConstOf `Filter.Eventually do
    throwError "expected full eventual proposition"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print Green32.HasCosetHole
#print axioms FCBTrustedSpec.ExpectedType
