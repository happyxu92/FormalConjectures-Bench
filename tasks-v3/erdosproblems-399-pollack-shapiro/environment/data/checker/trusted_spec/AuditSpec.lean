import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos399.erdos_399.variants.pollack_shapiro).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType must be a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args body => do
      unless args.size == 2 do throwError "missing complete n/x binders"
      for arg in args do
        unless (← Meta.inferType arg) == .const `Nat [] do
          throwError "expected Nat parameter"
        unless (← arg.fvarId!.getDecl).binderInfo == .default do
          throwError "expected explicit binder"
      unless (← Meta.inferType body) == .sort .zero do
        throwError "expected proposition body"
      logInfo m!"complete explicit Nat binder count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
  logInfo m!"transitive ExpectedType axioms: {axioms}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
