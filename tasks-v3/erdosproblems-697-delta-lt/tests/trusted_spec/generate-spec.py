from pathlib import Path
import json, hashlib
E=Path(__file__).resolve().parent
R=Path('/root/FormalConjectures-Bench/tasks-v3/erdosproblems-697-delta-lt')
P=E/'generated-spec';P.mkdir(exist_ok=True)
golden=(R/'tests/golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix,rest=golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN',1)
assert prefix.count('  sorry')==1
assert prefix.count('import FormalConjecturesBench.Submission\n')==1
prefix=prefix.replace('import FormalConjecturesBench.Submission\n','')
helper=(E/'DensityProof.lean').read_text().removeprefix('import FormalConjectures.Util.ProblemImports\n')
proof=(E/'ProveDensityExists.lean').read_text().split(' := by\n',1)[1].split('\n#print axioms density_exists',1)[0]
prefix=prefix.replace('  sorry',proof.rstrip())
prefix=prefix.replace('import FormalConjectures.Util.ProblemImports\n','import FormalConjectures.Util.ProblemImports\n\n'+helper+'\n',1)
# Remove only the trailing documentation for the temporary target command.
prefix=prefix[:prefix.rindex('/--')]
target=rest[:rest.rindex('end Erdos697')].strip()
source=prefix+'''
-- Repair-time extraction; no candidate module, Lake config, or cache is loaded.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command '''+json.dumps(target,ensure_ascii=False)+'''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos697.erdos_697.variants.delta_lt
    | throwError "missing temporary target"
  let expected := info.type
  let levels := info.levelParams
  setEnv original
  liftTermElabM do
    addAndCompile <| .defnDecl {
      name := `FCBTrustedSpec.ExpectedType
      levelParams := levels
      type := ← Meta.inferType expected
      value := expected
      hints := .abbrev
      safety := .safe
    }
end Erdos697
'''
(P/'FCBTrustedSpec.lean').write_text(source)
(P/'AuditSpec.lean').write_text('''import FCBTrustedSpec
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for (name, _) in env.constants.toList do
    if (`Erdos697.erdos_697.variants.delta_lt).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not a proposition"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 2 do throwError "expected complete binders m and α"
      let mType ← Meta.inferType args[0]!
      let aType ← Meta.inferType args[1]!
      unless ← Meta.isDefEq mType (mkConst ``Nat) do throwError "m is not Nat"
      unless ← Meta.isDefEq aType (mkConst ``Real) do throwError "α is not Real"
      logInfo m!"complete binder count: {args.size} (m : Nat) (α : Real)"
  logInfo m!"universe parameters: {info.levelParams}"
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos697.δ, `Erdos697.density_exists] do
    let axioms ← collectAxioms name
    logInfo m!"audit {name}: {axioms}"
    for ax in axioms do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "untrusted axiom {ax} in {name}"
#print FCBTrustedSpec.ExpectedType
#print Erdos697.density_exists
#print axioms FCBTrustedSpec.ExpectedType
#print axioms Erdos697.δ
#print axioms Erdos697.density_exists
''')
# Repair-time ONLY original-type audit, never compiled into Spec or loaded by verifier.
original=golden.replace('import FormalConjectures.Util.ProblemImports\n','').replace('import FormalConjecturesBench.Submission\n','')
(E/'AuditTypeIdentity.lean').write_text('import FCBTrustedSpec\nnamespace OriginalGolden\n'+original+'\nend OriginalGolden\n'+'''open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let originalDensity := (env.find? `OriginalGolden.Erdos697.density_exists).get!
  let repairedDensity := (env.find? `Erdos697.density_exists).get!
  unless originalDensity.levelParams == repairedDensity.levelParams do
    throwError "density_exists universe parameters changed"
  let originalTarget := (env.find? `OriginalGolden.Erdos697.erdos_697.variants.delta_lt).get!
  let expected := (env.find? `FCBTrustedSpec.ExpectedType).get!.value!
  unless originalTarget.levelParams == (env.find? `FCBTrustedSpec.ExpectedType).get!.levelParams do
    throwError "target universe parameters changed"
  liftTermElabM do
    unless ← Meta.isDefEq originalDensity.type repairedDensity.type do
      throwError "density_exists complete type changed"
    unless ← Meta.isDefEq originalTarget.type expected do
      throwError "original target complete type changed"
  logInfo "Original golden density_exists and target complete types/universes match repaired Spec"
-- Kernel checks, including proof-irrelevance for the unchanged choose definition.
example (m : ℕ) (α : ℝ) : OriginalGolden.Erdos697.δ m α = Erdos697.δ m α := rfl
example : FCBTrustedSpec.ExpectedType := @OriginalGolden.Erdos697.erdos_697.variants.delta_lt
''')
(P/'reproduce.sh').write_text((E/'research-lean.sh').read_text().replace('/tmp/retry7', '$(cd "$(dirname "$0")" && pwd)').replace('cd $(cd "$(dirname "$0")" && pwd)','cd "$(dirname "$0")"').replace('"$@"','-o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean\n/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean AuditSpec.lean'))
(P/'generate-spec.py').write_text(Path(__file__).read_text())
(P/'DensityProof.lean').write_text((E/'DensityProof.lean').read_text())
(P/'ProveDensityExists.lean').write_text((E/'ProveDensityExists.lean').read_text())
print('Generated from this task golden, replacing only density_exists proof; δ unchanged.')
