import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos264.erdos_264.variants.ko_tao_neg then
    throwError "temporary theorem was exported"
  for (name, _) in env.constants.toList do
    if (`Erdos264.erdos_264.variants.ko_tao_neg).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos264.IsIrrationalitySequence] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType

open Filter
example : FCBTrustedSpec.ExpectedType = (∀ {a : ℕ → ℕ}, StrictMono a → 0 ∉ Set.range a →
    Summable ((1 : ℝ) / a ·) →
    (0 < atTop.liminf fun n ↦ a n ^ 2 * ∑' k : Set.Ioi n, (1 : ℝ) / a k ^ 2) →
    ¬Erdos264.IsIrrationalitySequence a) := rfl
