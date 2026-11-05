import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`GaussCircleProblem.exact_form_floor).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `GaussCircleProblem.N, `GaussCircleProblem.E] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec names : Expr → List Name
    | .forallE name _ body _ => name :: names body
    | _ => []
  let binders := (names info.value).toArray
  unless binders == #[`r, `hr] do
    throwError "incorrect complete binders: {binders}"
  logInfo m!"complete binders: {binders}; universe parameters: {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print GaussCircleProblem.N
#print GaussCircleProblem.E
#print axioms FCBTrustedSpec.ExpectedType
