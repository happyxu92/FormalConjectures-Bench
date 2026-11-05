"""Repair-time only: python3 generate-spec.py GOLDEN_TARGET OUTPUT_DIRECTORY.
Only density_exists's proof is replaced. No candidate source is an input.
Periodic proof adapted read-only from the sibling delta-lt research; all ii
elaboration, type identity checks, compilation and dependency audits are local.
"""
from pathlib import Path
import json, sys, shutil
E = Path(__file__).resolve().parent
G = Path(sys.argv[1]).resolve()
P = Path(sys.argv[2]).resolve(); P.mkdir(parents=True, exist_ok=True)
golden = G.read_text()
helper = (E/'DensityProof.lean').read_text()
proof_source = (E/'ProveDensityExists.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('  sorry') == 3
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
proof = proof_source.split(' := by\n', 1)[1].split('\n#print axioms density_exists', 1)[0].rstrip()
prefix = prefix.replace('  sorry', proof, 1)
prefix = prefix.replace('import FormalConjectures.Util.ProblemImports\n',
    'import FormalConjectures.Util.ProblemImports\n\n' + helper.removeprefix('import FormalConjectures.Util.ProblemImports\n') + '\n', 1)
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos697')].strip()
source = prefix + '''
-- Repair-time elaboration in a candidate-free environment. Discard the
-- temporary target and all its auxiliary declarations before export.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos697.erdos_697.parts.ii
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
    if (`Erdos697.erdos_697.parts.ii).isPrefixOf name then
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
  for name in #[`FCBTrustedSpec.ExpectedType, `Erdos697.δ, `Erdos697.density_exists,
                 `FCBRepair697.periodic_density] do
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
-- These unchanged frozen auxiliaries are NOT in ExpectedType's closure.
#print axioms Erdos697.erdos_697.variants.delta_lt
#print axioms Erdos697.erdos_697.parts.i
''')
original = golden.replace('import FormalConjectures.Util.ProblemImports\n', '').replace('import FormalConjecturesBench.Submission\n', '')
(P/'AuditTypeIdentity.lean').write_text('import FCBTrustedSpec\nnamespace OriginalGolden\n' + original + '\nend OriginalGolden\n' + '''open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let od := (env.find? `OriginalGolden.Erdos697.density_exists).get!
  let rd := (env.find? `Erdos697.density_exists).get!
  let ot := (env.find? `OriginalGolden.Erdos697.erdos_697.parts.ii).get!
  let et := (env.find? `FCBTrustedSpec.ExpectedType).get!
  unless od.levelParams == rd.levelParams && ot.levelParams == et.levelParams do
    throwError "original universe parameters changed"
  liftTermElabM do
    unless ← Meta.isDefEq od.type rd.type do throwError "density_exists complete type changed"
    unless ← Meta.isDefEq ot.type et.value! do throwError "target complete type changed"
  logInfo "Original ii golden density_exists and target complete types/universes match repaired Spec"
example (m : ℕ) (α : ℝ) : OriginalGolden.Erdos697.δ m α = Erdos697.δ m α := rfl
example : FCBTrustedSpec.ExpectedType := @OriginalGolden.Erdos697.erdos_697.parts.ii
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
"$LEAN" AuditTypeIdentity.lean
''')
for name in ('generate-spec.py', 'DensityProof.lean', 'ProveDensityExists.lean'):
    if (E/name).resolve() != (P/name).resolve(): shutil.copy2(E/name, P/name)
print('Generated only from ii golden:', G, '; output:', P)
