import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos299.erdos_299.variants.density).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType and all referenced prefix dependencies: {axioms}"
  let countBinders : Expr → Nat := fun e => Id.run do
    let mut e := e
    let mut n := 0
    repeat
      match e with
      | .forallE _ _ body _ => n := n + 1; e := body
      | _ => break
    return n
  unless countBinders info.value == 3 do
    throwError "expected three complete outer binders (A, zero exclusion, positive upper density)"
  logInfo m!"complete outer binder count: {countBinders info.value}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
