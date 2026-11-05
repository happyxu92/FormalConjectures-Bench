import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Mathoverflow75792.complexity_five_pow).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  for (name, _) in env.constants.toList do
    if (`Mathoverflow75792).isPrefixOf name || name == `FCBTrustedSpec.ExpectedType then
      let axioms ← collectAxioms name
      for ax in axioms do
        unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
          throwError "untrusted axiom {ax} in {name}"
      logInfo m!"audited {name}: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected outer binder in the closed iff proposition"
  | _ => logInfo "complete outer binder count: 0; all nested quantifiers retained"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.all true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
#print Mathoverflow75792.complexity
#print axioms Mathoverflow75792.complexity
