from pathlib import Path
import json, hashlib
E=Path(__file__).resolve().parent
R=Path('/root/FormalConjectures-Bench/tasks-v3/erdosproblems-697-i')
P=E/'generated-spec'; P.mkdir(exist_ok=True)
# Read-only reference: a general periodic-set proof, independently compiled here.
ref=Path('/root/FormalConjectures-Bench/jobs/number-theory-informal-repair/retry-seven-20261105/tasks/erdosproblems-697-delta-lt/attempt-001')
helper=(ref/'DensityProof.lean').read_text()
proof_source=(ref/'ProveDensityExists.lean').read_text()
(E/'DensityProof.lean').write_text(helper)
(E/'ProveDensityExists.lean').write_text(proof_source)
golden=(R/'tests/golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix,rest=golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN',1)
assert prefix.count('  sorry')==2
prefix=prefix.replace('import FormalConjecturesBench.Submission\n','')
proof=proof_source.split(' := by\n',1)[1].split('\n#print axioms density_exists',1)[0].rstrip()
# Only density_exists proof is transformed. delta_lt is unreferenced by ExpectedType.
prefix=prefix.replace('  sorry',proof,1)
prefix=prefix.replace('import FormalConjectures.Util.ProblemImports\n','import FormalConjectures.Util.ProblemImports\n\n'+helper.removeprefix('import FormalConjectures.Util.ProblemImports\n')+'\n',1)
prefix=prefix[:prefix.rindex('/--')]
target=rest[:rest.rindex('end Erdos697')].strip()
source=prefix+'''\n-- Repair-time elaboration only, isolated from every candidate input.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command '''+json.dumps(target,ensure_ascii=False)+'''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos697.erdos_697.parts.i
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
    if (`Erdos697.erdos_697.parts.i).isPrefixOf name then
      throwError "temporary target or child exported: {name}"
  let some (.defnInfo info) := env.find? `FCBTrustedSpec.ExpectedType
    | throwError "ExpectedType is not a definition"
  unless info.levelParams.isEmpty do throwError "unexpected universes"
  unless info.type == .sort .zero do throwError "ExpectedType is not a proposition"
  liftTermElabM do
    Meta.forallTelescope info.value fun args _ => do
      unless args.size == 2 do throwError "expected complete binders α and hα"
      let aType ← Meta.inferType args[0]!
      let hType ← Meta.inferType args[1]!
      unless ← Meta.isDefEq aType (mkConst ``Real) do throwError "α is not Real"
      unless ← Meta.isProp hType do throwError "hα is not a proposition"
      let aInfo ← args[0]!.fvarId!.getDecl
      let hInfo ← args[1]!.fvarId!.getDecl
      unless aInfo.binderInfo == .implicit && hInfo.binderInfo == .default do
        throwError "binder visibility changed"
      logInfo m!"complete binders: implicit α : {aType}; explicit hα : {hType}"
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
-- Unreferenced frozen auxiliary: not in ExpectedType's dependency closure.
#print axioms Erdos697.erdos_697.variants.delta_lt
''')
original=golden.replace('import FormalConjectures.Util.ProblemImports\n','').replace('import FormalConjecturesBench.Submission\n','')
(E/'AuditTypeIdentity.lean').write_text('import FCBTrustedSpec\nnamespace OriginalGolden\n'+original+'\nend OriginalGolden\n'+'''open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let od := (env.find? `OriginalGolden.Erdos697.density_exists).get!
  let rd := (env.find? `Erdos697.density_exists).get!
  let ot := (env.find? `OriginalGolden.Erdos697.erdos_697.parts.i).get!
  let et := (env.find? `FCBTrustedSpec.ExpectedType).get!
  unless od.levelParams == rd.levelParams && ot.levelParams == et.levelParams do
    throwError "original universe parameters changed"
  liftTermElabM do
    unless ← Meta.isDefEq od.type rd.type do throwError "density_exists complete type changed"
    unless ← Meta.isDefEq ot.type et.value! do throwError "target complete type changed"
  logInfo "Original golden density_exists and target complete types/universes match repaired Spec"
example (m : ℕ) (α : ℝ) : OriginalGolden.Erdos697.δ m α = Erdos697.δ m α := rfl
example : FCBTrustedSpec.ExpectedType := @OriginalGolden.Erdos697.erdos_697.parts.i
''')
(P/'reproduce.sh').write_text('''#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export LEAN_PATH="$PWD:/opt/formal-conjectures/.lake/build/lib/lean"
for dep in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
 export LEAN_PATH="$LEAN_PATH:/opt/formal-conjectures/.lake/packages/$dep/.lake/build/lib/lean"
done
LEAN=/opt/elan/toolchains/leanprover--lean4---v4.27.0/bin/lean
"$LEAN" --version
"$LEAN" -DautoImplicit=false -DrelaxedAutoImplicit=false -DmaxHeartbeats=0 -DmaxRecDepth=4000 -o FCBTrustedSpec.olean -i FCBTrustedSpec.ilean FCBTrustedSpec.lean
"$LEAN" AuditSpec.lean
''')
(P/'generate-spec.py').write_text(Path(__file__).read_text())
print('Generated from erdosproblems-697-i golden; only density_exists proof transformed; δ and all types unchanged.')
