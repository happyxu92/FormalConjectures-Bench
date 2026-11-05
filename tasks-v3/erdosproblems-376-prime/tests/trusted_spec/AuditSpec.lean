import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos376.erdos_376.variants.prime).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType and all referenced definitions transitively: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun binders _ => do
      unless binders.size == 6 do
        throwError "expected p q and four hypotheses, got {binders.size}"
      for binder in binders do
        let decl ← binder.fvarId!.getDecl
        logInfo m!"binder {decl.userName}, {repr decl.binderInfo}, type {decl.type}"
      logInfo m!"complete outer binder count: {binders.size}; universes: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
