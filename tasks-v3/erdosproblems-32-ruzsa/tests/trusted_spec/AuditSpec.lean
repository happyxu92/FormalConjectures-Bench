import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos32.erdos_32.variants.ruzsa).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not Prop-valued"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos32.IsAdditiveComplementToPrimes] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let .forallE _ domain body binder := info.value
    | throwError "missing complete explicit set binder"
  unless binder == .default do throwError "set binder is not explicit"
  unless domain == (mkApp (mkConst `Set [.zero]) (mkConst `Nat)) do
    throwError "set binder domain changed: {domain}"
  let .forallE _ _ conclusion implicationBinder := body
    | throwError "missing additive complement assumption"
  unless implicationBinder == .default do throwError "assumption binder changed"
  match conclusion with
  | .forallE .. => throwError "unexpected additional outer binder"
  | _ => pure ()
  logInfo "complete outer binder count: 2 (A : Set Nat; additive-complement implication)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos32.IsAdditiveComplementToPrimes
#print axioms Erdos32.IsAdditiveComplementToPrimes
#print axioms FCBTrustedSpec.ExpectedType
