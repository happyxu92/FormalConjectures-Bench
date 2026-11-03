import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `FermatCatalanConjecture.fermat_catalan.variants.darmon_granville then
    throwError "temporary theorem was exported"
  if env.contains `FermatCatalanConjecture.FCBExtractionTarget then
    throwError "temporary extraction proof was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `FermatCatalanConjecture.FermatCatalanSet', `FermatCatalanConjecture.FermatCatalanSet, `FermatCatalanConjecture.fermatCatalanConjecture] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec binderNames : Expr → List Name
    | .forallE n _ body _ => n :: binderNames body
    | _ => []
  let names := binderNames info.value
  unless names == [`m, `n, `k, `hm, `hn, `hk, `H] do
    throwError "incomplete binders: {names}"
  logInfo m!"complete binder order: {names}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
