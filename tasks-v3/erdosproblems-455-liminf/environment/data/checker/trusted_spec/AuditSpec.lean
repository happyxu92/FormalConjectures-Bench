import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos455.erdos_455.variants.liminf).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  let rec countBinders : Expr → Nat
    | .forallE _ _ next _ => 1 + countBinders next
    | _ => 0
  let binders := countBinders info.value
  unless binders == 3 do throwError "incomplete outer parameters: {binders}"
  logInfo m!"audited ExpectedType and all transitive references: {axioms}"
  logInfo m!"complete outer binder count: {binders} (q, StrictMono q, prime/convexity hypothesis)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
