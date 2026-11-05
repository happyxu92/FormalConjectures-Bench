import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`RiemannZetaValues.infinite_irrational_at_odd).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  -- collectAxioms traverses the definition value and every referenced prefix
  -- declaration transitively. Unrelated original prefix theorems are not used.
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType and transitive dependencies: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 0 do throwError "unexpected outer forall parameters"
      logInfo m!"complete outer binder count: {args.size}"
  logInfo m!"ordered universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
