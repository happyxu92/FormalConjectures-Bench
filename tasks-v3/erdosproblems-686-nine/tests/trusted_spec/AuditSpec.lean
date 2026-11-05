import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos686.erdos_686.variants.nine).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  -- This target is closed; all its quantifiers are inside the iff's RHS.
  match info.value with
  | .forallE .. => throwError "unexpected outer binder"
  | _ => pure ()
  -- Earlier research statements in the immutable prefix use sorry, but none
  -- may enter the expected proposition's transitive dependency graph.
  let rec visit (name : Name) (seen : NameSet) : CommandElabM NameSet := do
    if seen.contains name then return seen
    let seen := seen.insert name
    let some ci := (← getEnv).find? name | throwError "unknown constant {name}"
    if (`Erdos686).isPrefixOf name then
      throwError "unexpected task-local dependency in this closed product proposition: {name}"
    let mut seen := seen
    let refs := ci.type.getUsedConstants ++ (ci.value?.map Expr.getUsedConstants).getD #[]
    for ref in refs do
      seen ← visit ref seen
    return seen
  let mut seen : NameSet := {}
  for ref in info.value.getUsedConstants do
    seen ← visit ref seen
  logInfo m!"audited entire ExpectedType dependency graph ({seen.size} constants): {axioms}"
  logInfo m!"universe parameters (ordered): {info.levelParams}; complete outer binder count: 0"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
