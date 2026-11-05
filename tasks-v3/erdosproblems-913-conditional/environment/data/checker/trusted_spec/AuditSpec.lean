import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos913.erdos_913.variants.conditional).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  match info.value with
  | .forallE _ _ body .default =>
    if body.isForall then throwError "unexpected additional outer binder"
  | _ => throwError "expected one explicit hypothesis binder"
  logInfo m!"complete outer binder count: 1 (explicit hypothesis h)"
  logInfo m!"universe parameters: {info.levelParams}"
  logInfo m!"ExpectedType transitive axioms: {axioms}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
