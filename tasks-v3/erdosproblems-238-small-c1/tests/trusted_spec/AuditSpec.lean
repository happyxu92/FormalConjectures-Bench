import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos238.erdos_238.variants.small_c1).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType does not define a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `primeGap] do
    unless env.contains name do throwError "missing audited constant {name}"
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  liftTermElabM do
    Meta.forallTelescope info.value fun args body => do
      unless args.size == 2 do throwError "expected natural c2 and its positivity hypothesis"
      for arg in args do
        let decl ← arg.fvarId!.getDecl
        logInfo m!"binder {decl.userName}, info {repr decl.binderInfo}: {decl.type}"
      logInfo m!"complete binder count: {args.size}"
      logInfo m!"remaining proposition: {body}"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
