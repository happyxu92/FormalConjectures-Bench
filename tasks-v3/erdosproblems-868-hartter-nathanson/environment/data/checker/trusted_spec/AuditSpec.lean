import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos868.erdos_868.variants.Hartter_Nathanson).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  let rec binders : Expr → Nat
    | .forallE _ _ body _ => binders body + 1
    | _ => 0
  unless binders info.value == 2 do
    throwError "complete expected type lost binders (o, ho)"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive dependency: {ax}"
  logInfo m!"audited ExpectedType and all referenced prefix dependencies: {axioms}"
  logInfo m!"complete outer binder count: {binders info.value}"
  logInfo m!"universe parameters (in order): {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
