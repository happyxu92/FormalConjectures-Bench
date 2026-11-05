import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos375.erdos_375.variants.le_two).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos375.Erdos375Prop] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let mut binders := #[]
  let mut e := info.value
  while e.isForall do
    match e with
    | .forallE name _ body bi =>
      binders := binders.push (name, bi)
      e := body
    | _ => throwError "unreachable"
  unless binders.size == 5 do throwError "expected complete five outer binders"
  logInfo m!"complete outer binders (names, binder kinds): {reprStr binders}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Erdos375.Erdos375Prop
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos375.Erdos375Prop
