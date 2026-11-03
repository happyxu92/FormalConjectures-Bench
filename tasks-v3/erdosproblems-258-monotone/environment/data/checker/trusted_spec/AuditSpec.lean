import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos258.erdos_258.variants.Monotone).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted axiom {ax} in ExpectedType or its transitive dependencies"
  logInfo m!"audited ExpectedType and transitive dependencies: {axioms}"
  liftTermElabM do
    let value ← Meta.whnf info.value
    unless value.isAppOfArity ``Iff 2 do throwError "expected the complete answer equivalence"
    let rhs := value.appArg!
    Meta.forallTelescope rhs fun args _ => do
      unless args.size == 4 do throwError "expected a and all three hypotheses"
      logInfo m!"complete RHS binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
