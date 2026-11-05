import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Andrica.andrica_conjecture.ferreira_large_n).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  -- The entire closed eventual proposition has no outer forall binders.
  -- Its n binder occurs inside Filter.Eventually, retained in info.value.
  match info.value with
  | .forallE .. => throwError "unexpected outer forall binder"
  | _ => pure ()
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited entire ExpectedType value and referenced prefix definitions: {axioms}"
  logInfo m!"universe parameters in order: {info.levelParams}"
  logInfo "complete outer binder count: 0; n : Nat is bound inside Filter.Eventually"
set_option pp.all true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
