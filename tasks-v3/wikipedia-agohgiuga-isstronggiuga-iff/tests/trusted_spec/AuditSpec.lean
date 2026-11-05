import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`AgohGiuga.isStrongGiuga_iff).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  -- Both implicit a and explicit ha must be retained, in their original order.
  match info.value with
  | .forallE a _ (.forallE ha _ _ .default) .implicit =>
    unless a == `a && ha == `ha do throwError "incorrect complete binder names"
  | _ => throwError "missing implicit a or explicit Composite hypothesis"
  for name in #[`FCBTrustedSpec.ExpectedType, `AgohGiuga.IsStrongGiuga,
      `AgohGiuga.IsCarmichael] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted transitive axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo "complete outer binders: {a : Nat} (ha : Nat.Composite a)"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print AgohGiuga.IsStrongGiuga
#print AgohGiuga.IsCarmichael
#print axioms FCBTrustedSpec.ExpectedType
