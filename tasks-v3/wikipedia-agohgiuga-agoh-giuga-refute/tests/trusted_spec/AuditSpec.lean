import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `AgohGiuga.formal_conjectures_bench_refutation then
    throwError "temporary theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `AgohGiuga.AgohGiugaCongr, `AgohGiuga.AgohGiugaSum] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 0 do throwError "unexpected outer parameters"
      logInfo m!"complete outer parameter count: {args.size}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
