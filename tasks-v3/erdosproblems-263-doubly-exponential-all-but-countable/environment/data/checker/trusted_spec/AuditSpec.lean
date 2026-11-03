import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos263.erdos_263.variants.doubly_exponential_all_but_countable then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Erdos263.erdos_263.variants.doubly_exponential_all_but_countable).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos263.IsIrrationalitySequence] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType

open Filter
example : FCBTrustedSpec.ExpectedType = (∀ᶠ (α : ℝ) in .cocountable, α > 1 → Erdos263.IsIrrationalitySequence (fun n : ℕ => ⌊α ^ 2 ^ n⌋₊)) := rfl
