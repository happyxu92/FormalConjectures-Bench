-- Repair-time only: not run by the verifier. Compare the generated f against
-- the exact original proof argument, using kernel proof irrelevance.
import FCBTrustedSpec
open Classical Filter Real
namespace Erdos961
example (k : ℕ) : f k =
    (if hk : 0 < k then Nat.find (show ∃ n, Erdos961Prop k n from by
      use k
      exact erdos_961.sylvester_schur k hk) else 0) := rfl
example : FCBTrustedSpec.ExpectedType =
    (∀ᶠ k in atTop, f k < 3 * k / log k) := rfl
end Erdos961
