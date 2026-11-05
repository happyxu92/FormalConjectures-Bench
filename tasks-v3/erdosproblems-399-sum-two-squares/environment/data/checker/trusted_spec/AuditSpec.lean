import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos399.erdos_399.variants.sum_two_squares).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom: {ax}"
  logInfo m!"audited ExpectedType and transitive dependencies: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 5 do throwError "expected n, x, y and both complete hypotheses"
      for i in [:3] do
        let decl ← args[i]!.fvarId!.getDecl
        unless decl.binderInfo == .implicit do throwError "implicit binder lost"
        unless decl.type == mkConst `Nat do throwError "expected natural number binder"
      logInfo m!"complete binder count: {args.size} (n x y implicit, two hypotheses)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
