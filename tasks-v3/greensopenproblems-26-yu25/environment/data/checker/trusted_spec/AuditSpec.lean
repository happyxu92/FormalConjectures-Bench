import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Green26.green_26.variants.yu25).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green26.𝔽, `Green26.𝔽₃,
                `Green26.StandardCube, `Green26.IsCube] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec countBinders : Expr → Nat
    | .forallE _ _ body _ => 1 + countBinders body
    | _ => 0
  let count := countBinders info.value
  unless count == 3 do throwError "expected complete n, A, cube-hypothesis binders"
  logInfo m!"complete outer binder count: {count} (n, A, cube hypothesis)"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print Green26.𝔽
#print Green26.𝔽₃
#print Green26.StandardCube
#print Green26.IsCube
#print axioms FCBTrustedSpec.ExpectedType
