import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Firoozbakht.formal_conjectures_bench_refutation then
    throwError "temporary theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let .app (.const `Not []) (.forallE _ dom body .default) := info.value
    | throwError "expected negated universal type"
  unless dom == .const `Nat [] do throwError "unexpected quantified domain"
  unless body.getAppFn == .const `LT.lt [.zero] do
    throwError "unexpected inequality head"
  for name in #[`FCBTrustedSpec.ExpectedType, `Firoozbakht.firoozbakhtSeq] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}; one Nat binder within Not"
#print FCBTrustedSpec.ExpectedType
#print Firoozbakht.firoozbakhtSeq
#print axioms FCBTrustedSpec.ExpectedType
