import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos346.erdos_346.variants.f_not_isAddComplete).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos346.f] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let .forallE nB _ (.forallE nh _ (.forallE nhB _ body ihB) ih) iB := info.value
    | throwError "expected complete B, h, hB telescope"
  unless nB == `B && nh == `h && nhB == `hB do
    throwError "unexpected binder names"
  unless iB == .implicit && ih == .default && ihB == .default do
    throwError "unexpected binder implicitness"
  if body.isForall then throwError "unexpected additional binders"
  logInfo "complete outer binder count: 3; B implicit, h and hB explicit"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print Erdos346.f
#print axioms Erdos346.f
#print axioms FCBTrustedSpec.ExpectedType
