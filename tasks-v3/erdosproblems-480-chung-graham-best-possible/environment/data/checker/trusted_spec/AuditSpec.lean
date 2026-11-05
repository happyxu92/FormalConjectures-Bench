import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `Erdos480.erdos_480.variants.chung_graham_best_possible
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  logInfo m!"audited ExpectedType and its transitive references: {axioms}"
  -- The original type has a let-bound c, then epsilon and its positivity proof.
  match info.value with
  | .letE name _ _ (.forallE eps epsType (.forallE positive positiveType body _) _) _ =>
      unless body.isAppOf ``Not do throwError "expected negated uniform bound"
      logInfo m!"outer let binder: {name}; explicit complete binders: {eps} : {epsType}, {positive} : {positiveType}"
  | _ => throwError "missing original let/epsilon/positivity structure"
  logInfo m!"universe parameters (ordered): {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
