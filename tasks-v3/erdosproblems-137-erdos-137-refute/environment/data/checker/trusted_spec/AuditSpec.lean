import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Erdos137.formal_conjectures_bench_refutation then
    throwError "temporary theorem exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType must be a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive dependency {ax}"
  logInfo m!"audited full value and transitive dependencies: {axioms}"
  logInfo m!"universe parameters (ordered): {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
