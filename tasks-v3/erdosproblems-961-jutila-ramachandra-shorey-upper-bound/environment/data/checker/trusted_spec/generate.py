from pathlib import Path
import json, shutil
pkg=Path(__file__).resolve().parent
golden=(pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix,rest=golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN',1)
prefix=prefix.replace('import FormalConjecturesBench.Submission\n','')
prefix=prefix[:prefix.rindex('/--')]
target=rest[:rest.rindex('end Erdos961')].strip()
# Replace only the proof of the existence lemma, not its name or complete type.
# Elaborate the original and replacement in turn from the same environment;
# reject any change of type or universes before retaining the real proof.
old = '''theorem erdos_961.variants.well_defined (k : ℕ) (hk : 0 < k): ∃ n, Erdos961Prop k n := by
  use k
  exact erdos_961.sylvester_schur k hk'''
new = '''theorem erdos_961.variants.well_defined (k : ℕ) (hk : 0 < k): ∃ n, Erdos961Prop k n := by
  obtain ⟨p, hkp, hp⟩ := Nat.exists_infinite_primes (k + 1)
  refine ⟨p + 1, ?_⟩
  intro m hm
  refine ⟨(m / p + 1) * p, ?_, ?_⟩
  · have hmod := Nat.mod_lt m hp.pos
    have hdiv := Nat.mod_add_div m p
    rw [Nat.mul_comm p (m / p)] at hdiv
    simp only [Nat.add_mul, Nat.one_mul]
    constructor <;> omega
  · intro hs
    have hlt := Nat.mem_smoothNumbers'.mp hs p hp (by exact dvd_mul_left p (m / p + 1))
    omega'''
assert prefix.count(old) == 1
# The attribute is applied inside both elaborations; it must not apply to run_cmd.
attribute = '@[category research solved, AMS 11]\n'
assert prefix.count(attribute + old) == 1
transform = '''open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let originalSyntax ← ofExcept <| Parser.runParserCategory original `command ''' + json.dumps(attribute + old, ensure_ascii=False) + '''
  elabCommand originalSyntax
  let some before := (← getEnv).find? `Erdos961.erdos_961.variants.well_defined
    | throwError "missing original auxiliary"
  setEnv original
  let replacementSyntax ← ofExcept <| Parser.runParserCategory original `command ''' + json.dumps(attribute + new, ensure_ascii=False) + '''
  elabCommand replacementSyntax
  let some after := (← getEnv).find? `Erdos961.erdos_961.variants.well_defined
    | throwError "missing proved auxiliary"
  unless before.type == after.type && before.levelParams == after.levelParams do
    throwError "auxiliary type/universe mismatch"
  let axioms ← collectAxioms after.name
  for ax in axioms do
    unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
      throwError "untrusted auxiliary axiom {ax}"
  logInfo m!"auxiliary full type/universes unchanged; kernel-checked axioms: {axioms}"
'''
prefix = prefix.replace(attribute + old, transform)
# A doc comment cannot attach to a run_cmd; retain it as an ordinary comment.
prefix = prefix.replace('/-- There exists $n$ such that `Erdos961Prop k n` holds. -/',
                        '/- There exists $n$ such that `Erdos961Prop k n` holds. -/')
source=prefix+'''
-- Repair-time extraction from the complete trusted declaration.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command '''+json.dumps(target,ensure_ascii=False)+'''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos961.erdos_961.variants.jutila_ramachandra_shorey_upper_bound
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
end Erdos961
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
