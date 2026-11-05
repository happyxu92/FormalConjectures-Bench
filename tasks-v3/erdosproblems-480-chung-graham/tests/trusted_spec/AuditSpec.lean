import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos480.erdos_480.variants.chung_graham).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"ExpectedType transitive axioms (including referenced prefix): {axioms}"
  liftTermElabM do
    Meta.forallTelescopeReducing info.value fun xs _ => do
      unless xs.size == 2 do throwError "expected complete x and interval-hypothesis binders"
      for x in xs do
        logInfo m!"complete binder: {x} : {← Meta.inferType x}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
