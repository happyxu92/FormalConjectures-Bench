import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `PerfectNumbers.odd_perfect_number_conjecture then
    throwError "temporary theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not a proposition"
  let .forallE _ nType body _ := info.value | throwError "missing n binder"
  unless nType == .const `Nat [] do throwError "incorrect domain"
  let .forallE _ _ _ _ := body | throwError "missing perfectness hypothesis"
  -- This traverses all value/type dependencies, including referenced prefix
  -- definitions. The unrelated prefix placeholder theorems are not reachable.
  for name in #[`FCBTrustedSpec.ExpectedType, `Nat.Perfect] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters (ordered): {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
