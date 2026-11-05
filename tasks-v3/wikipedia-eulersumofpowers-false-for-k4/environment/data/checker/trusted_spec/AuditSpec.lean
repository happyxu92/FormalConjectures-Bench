import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let target := `EulerSumOfPowers.eulers_sum_of_powers_conjecture.false_for_k4
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
  -- The expected value is the entire closed negation, with its forall binders
  -- inside Not. In particular, it contains no reference to the earlier open
  -- conjecture's placeholder proof retained in the immutable prefix.
  unless info.value.getAppFn == .const `Not [] do
    throwError "unexpected outer type expression"
  logInfo m!"audited ExpectedType transitive axioms: {axioms}"
  logInfo m!"ordered universe parameters: {info.levelParams}"
  logInfo "outer binders: 0; entire negated universal proposition preserved"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
