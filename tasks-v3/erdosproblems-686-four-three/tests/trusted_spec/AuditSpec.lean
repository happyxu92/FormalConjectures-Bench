import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos686.erdos_686.variants.four_three).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax} in ExpectedType"
  logInfo m!"audited ExpectedType and all transitive dependencies: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 0 do throwError "expected no outer binders on negated existence"
      logInfo m!"complete outer binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.all true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
