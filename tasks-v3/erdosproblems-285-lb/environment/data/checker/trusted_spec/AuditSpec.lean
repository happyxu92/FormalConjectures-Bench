import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos285.erdos_285).isPrefixOf name then
      throwError "temporary or unrelated placeholder theorem exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  if info.value.hasMVar || info.value.hasFVar then throwError "ExpectedType is not closed"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted axiom {ax}"
  logInfo m!"audited ExpectedType and transitive dependencies: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 4 do throwError "expected the complete f, S, hS, h binders"
      for arg in args do
        let decl ← arg.fvarId!.getDecl
        logInfo m!"complete binder: {decl.userName}, {reprStr decl.binderInfo}, type: {decl.type}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
