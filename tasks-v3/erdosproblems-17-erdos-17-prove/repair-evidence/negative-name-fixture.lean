import FCBTrustedSpec
namespace Hacker
def IsClusterPrime (_ : ℕ) : Prop := True
-- Deliberately adversarial name-resolution fixture, never a submitted proof.
@[term_elab Mathlib.Meta.setBuilder]
meta def shadowName : Lean.Elab.Term.TermElab := fun _ _ => do
  return Lean.mkApp2 (Lean.mkConst ``setOf [.zero]) (Lean.mkConst ``Nat)
    (Lean.mkConst ``Hacker.IsClusterPrime)
end Hacker
