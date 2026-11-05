import FCBTrustedSpec
open Classical
open scoped Real
namespace Erdos295
lemma fcbOriginalExistsK (N : ℕ) : ∃ (k : ℕ) (n : Fin k.succ → ℕ),
    (∀ i, N ≤ n i) ∧ StrictMono n ∧ ∑ i, (1 / n i : ℝ) = 1 := by
  sorry
noncomputable abbrev fcbOriginalK (N : ℕ) : ℕ := Nat.find (fcbOriginalExistsK N)
theorem erdos_295.variants.erdos_straus :
    ∃ᵉ (C > 0) (O > 0), ∀ᶠ (N : ℕ) in Filter.atTop,
      (k N - (rexp 1 - 1)*N) ∈ Set.Ioc (-C) (O * N / (N : ℝ).log) := by
  sorry
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let some original := env.find? `Erdos295.fcbOriginalExistsK | throwError "original helper absent"
  let some repaired := env.find? `Erdos295.exists_k | throwError "repaired helper absent"
  unless original.levelParams == repaired.levelParams do throwError "helper universes changed"
  liftTermElabM do
    unless ← Meta.isDefEq original.type repaired.type do throwError "helper complete type changed"
    let some (.defnInfo oldK) := env.find? `Erdos295.fcbOriginalK | throwError "original k absent"
    let some (.defnInfo newK) := env.find? `Erdos295.k | throwError "repaired k absent"
    unless oldK.levelParams == newK.levelParams do throwError "k universes changed"
    unless ← Meta.isDefEq oldK.type newK.type do throwError "k complete type changed"
    unless ← Meta.isDefEq oldK.value newK.value do throwError "k definition meaning changed"
    let some goal := env.find? `Erdos295.erdos_295.variants.erdos_straus | throwError "original target absent"
    let some (.defnInfo expected) := env.find? `FCBTrustedSpec.ExpectedType | throwError "ExpectedType absent"
    unless goal.levelParams == expected.levelParams do throwError "target universes changed"
    unless ← Meta.isDefEq goal.type expected.value do throwError "full target type changed"
  logInfo "ORIGINAL COMPLETE HELPER TYPE, K TYPE/VALUE, TARGET TYPE AND UNIVERSES MATCH"
end Erdos295
