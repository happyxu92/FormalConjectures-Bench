import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `EulerSumOfPowers.eulers_sum_of_powers_conjecture.false_for_k5
  for (name, _) in env.constants.toList do
    if target.isPrefixOf name then
      throwError "temporary target or child was exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom: {ax}"
  logInfo m!"ExpectedType transitive axiom audit: {axioms}"
  match info.value with
  | .forallE .. => throwError "unexpected external binder on closed negation"
  | .app (.const ``Not _) _ => pure ()
  | _ => throwError "expected the full closed negation expression"
  logInfo m!"complete outer binder count: 0; full quantifiers remain inside negation"
  logInfo m!"universe parameters (ordered): {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
