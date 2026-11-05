import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`OeisA358684.oeis_358684_conjecture_0).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  match info.value with
  | .forallE n domain body bi =>
    unless n == `n && domain == .const `Nat [] && bi == .default do
      throwError "lost original explicit n : Nat binder"
    if body.hasLooseBVars == false then throwError "lost dependent body"
    match body with
    | .forallE .. => throwError "unexpected extra outer binder"
    | _ => pure ()
  | _ => throwError "missing complete forall n : Nat binder"
  for name in #[`FCBTrustedSpec.ExpectedType, `OeisA358684.a, `OeisA358684.log2_minFac_le] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo "complete outer binders: (n : Nat), explicit, dependent"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.fullNames true in
#print FCBTrustedSpec.ExpectedType
#print OeisA358684.a
#print axioms OeisA358684.a
#print axioms FCBTrustedSpec.ExpectedType
