import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green32.green_32.variants.szemeredi_regime).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universe parameters"
  unless info.type == .sort .zero do throwError "ExpectedType must define a proposition"
  let mut count : Nat := 0
  let mut body := info.value
  while body.isForall do
    count := count + 1
    body := body.bindingBody!
  unless count == 4 do throwError "expected full binders c, hc, omega, asymptotics, not a fragment: got {count}"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green32.HasLargeGapDilate, `Green32.HasGap] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}; full outer forall count: {count}"
#print FCBTrustedSpec.ExpectedType
#print Green32.HasLargeGapDilate
#print Green32.HasGap
#print axioms FCBTrustedSpec.ExpectedType
