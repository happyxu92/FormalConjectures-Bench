import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos392.erdos_392.variants.implication).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let rec countBinders : Expr → Nat
    | .forallE _ _ body _ => 1 + countBinders body
    | _ => 0
  unless countBinders info.value == 3 do
    throwError "expected full h, A and hA binders"
  -- collectAxioms recursively visits ExpectedType's value and every referenced
  -- prefix definition. Frozen prefix placeholder theorems must NOT be used.
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType transitively: {axioms}"
  logInfo m!"complete outer binder count: {countBinders info.value}"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.all true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
