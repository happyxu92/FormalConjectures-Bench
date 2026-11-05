import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos402.erdos_402).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  let axioms ← collectAxioms `FCBTrustedSpec.ExpectedType
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted transitive axiom {ax}"
  let mut count : Nat := 0
  let mut body := info.value
  while body.isForall do
    count := count + 1
    body := body.bindingBody!
  unless count == 3 do throwError "expected all 3 binders (A, h₁, h₂), got {count}"
  logInfo m!"complete outer binders: {count}; universe parameters: {info.levelParams}"
  logInfo m!"transitive ExpectedType axioms: {axioms}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
