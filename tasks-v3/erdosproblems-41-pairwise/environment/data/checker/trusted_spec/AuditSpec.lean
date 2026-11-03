import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos41.erdos_41.variants.pairwise).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let mut binders : Nat := 0
  let mut body := info.value
  while body.isForall do
    let .forallE name type value binderInfo := body | unreachable!
    logInfo m!"binder {binders}: {name}, {repr binderInfo}, {type}"
    binders := binders + 1
    body := value
  unless binders == 3 do throwError "expected complete A, hA₂, hA binders"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos41.NtupleCondition] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
