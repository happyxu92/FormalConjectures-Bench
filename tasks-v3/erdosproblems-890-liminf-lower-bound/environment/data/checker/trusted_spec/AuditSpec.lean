import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos890.erdos_890).isPrefixOf name then
      throwError "temporary theorem or research placeholder exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  match info.value with
  | .forallE name domain body binder =>
    unless name == `k && domain == .const `Nat [] && binder == .default do
      throwError "expected one explicit Nat binder k"
    if body.isForall then throwError "unexpected extra outer binder"
    logInfo "complete outer binders: (k : Nat), explicit; universes: []"
  | _ => throwError "missing complete Nat binder"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos890.omegaGt] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
#print FCBTrustedSpec.ExpectedType
#print Erdos890.omegaGt
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos890.omegaGt
