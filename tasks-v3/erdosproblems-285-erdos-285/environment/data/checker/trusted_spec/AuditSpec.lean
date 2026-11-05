import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos285.erdos_285).isPrefixOf name then
      throwError "temporary theorem or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom: {ax}"
  logInfo m!"audited ExpectedType and transitive dependencies: {axioms}"
  unless info.value.isAppOfArity `Iff 2 do throwError "expected complete iff"
  liftTermElabM do
    Meta.forallTelescope info.value.getAppArgs[1]! fun args body => do
      unless args.size == 4 do throwError "expected f, S, hS and h"
      logInfo m!"complete RHS binder count: {args.size}; conclusion: {body}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
