import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos387.erdos_387.variants.easy).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType and all referenced definitions: {axioms}"
  let expectedBinders := #[(`n, BinderInfo.implicit), (`k, BinderInfo.implicit),
                           (`hn, BinderInfo.default), (`hk, BinderInfo.default)]
  let mut value := info.value
  for (name, kind) in expectedBinders do
    match value with
    | .forallE actual _ body binderKind =>
      unless actual == name && binderKind == kind do
        throwError "wrong full binder: {actual}"
      value := body
    | _ => throwError "missing full binder {name}"
  match value with
  | .forallE .. => throwError "unexpected extra outer binder"
  | _ => pure ()
  logInfo "complete outer binders: {n : Nat} {k : Nat} (hn : 1 ≤ n) (hk : k ≤ n)"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
