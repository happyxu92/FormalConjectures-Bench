import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  if env.contains `Green26.formal_conjectures_bench_refutation then
    throwError "temporary target theorem was exported"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not a proposition"
  for name in #[`FCBTrustedSpec.ExpectedType, `Green26.𝔽, `Green26.𝔽₃,
                `Green26.StandardCube, `Green26.IsCube] do
    let axioms ← collectAxioms name
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
    logInfo m!"audited {name}: {axioms}"
  unless info.value.isAppOf ``Not do throwError "missing outer negation"
  liftTermElabM do
    Meta.forallTelescope info.value.appArg! fun args body => do
      unless args.size == 2 do throwError "unexpected negated outer binders"
      unless body.isAppOf ``Exists do throwError "missing existential constant bound"
      for arg in args do
        let decl ← arg.fvarId!.getDecl
        logInfo m!"binder: {decl.userName}, {repr decl.binderInfo}, type {decl.type}"
      logInfo m!"negated binder count: {args.size}; existential C and all nested binders retained"
  logInfo m!"universe parameters: {info.levelParams}"
#print FCBTrustedSpec.ExpectedType
#print axioms FCBTrustedSpec.ExpectedType
