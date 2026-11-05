import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos975.erdos_975.variants.lower_bound).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos975.Erdos975Sum] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  let rec collectBinders : Expr → Array Name
    | .forallE name _ body _ => #[name] ++ collectBinders body
    | _ => #[]
  let binders := collectBinders info.value
  unless binders == #[`f, `hf, `hfdeg, `hf_pos] do
    throwError "incomplete or unexpected binders: {binders}"
  logInfo m!"complete outer binders: {binders}"
  logInfo m!"universe parameters: {info.levelParams}"
set_option pp.explicit true in
#print FCBTrustedSpec.ExpectedType
#print Erdos975.Erdos975Sum
#print axioms Erdos975.Erdos975Sum
#print axioms FCBTrustedSpec.ExpectedType
