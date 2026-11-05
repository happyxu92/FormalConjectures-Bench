# Fixed trusted Spec: Erdős 961 Jutila–Ramachandra–Shorey upper bound

Generated only at repair time from this task's immutable golden Target, with
Submission removed. `generate.py` extracts the complete target type and ordered
universe parameters with Lean elaboration, then restores the environment before
adding ExpectedType. The temporary target and its children are not exported.

The only mathematical proof transformation is the proof body of
`Erdos961.erdos_961.variants.well_defined`. Its original complete type and universe
parameters are elaborated in a temporary environment and compared exactly with
the independent replacement. For a prime p ≥ k+1, choose interval length p+1;
(m/p+1)*p lies in [m,m+p+1), and its prime divisor p precludes (k+1)-smoothness.
This proves the SAME existence proposition without the unproved optimal
Sylvester–Schur bound. No definition, target, hypothesis or allowed axiom changes.
The definition f (including its Nat.find argument) keeps its original source.
Proof irrelevance makes the existence-proof replacement definitionally harmless.

`reproduce.sh` uses the locked Linux x86_64 Lean 4.27.0 dependency environment;
never run it in the verifier. The generated module still contains unrelated
original sorry declarations, but AuditSpec checks that ExpectedType, f and
well_defined transitively use only propext/Classical.choice/Quot.sound. The
original sylvester_schur is deliberately printed separately to document that its
sorry is not silently approved. Both trusted packages contain the same artifacts.
Manifest hashes must be regenerated and pinned in both checkers after generation.
