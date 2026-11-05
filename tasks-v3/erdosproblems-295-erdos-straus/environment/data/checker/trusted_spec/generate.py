from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
pkg.mkdir(exist_ok=True)
golden = (pkg.parent/'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
prefix = prefix[:prefix.rindex('/--')]
# Repair only the proof of the prerequisite; its original declaration/type and
# the mathematical definition k remain unchanged. The target is not proved here.
proof_source = (pkg / 'ExistsKProof.lean').read_text()
body = proof_source.split('namespace Erdos295\n', 1)[1].split('\n#print axioms exists_k', 1)[0]
helpers, replacement = body.split('lemma exists_k', 1)
replacement = 'lemma exists_k' + replacement.rstrip()
original_start = prefix.index('lemma exists_k')
original_end = prefix.index('\n\n/--', original_start)
original = prefix[original_start:original_end]
assert original.split(':= by', 1)[0] == replacement.split(':= by', 1)[0]
assert original.endswith(':= by\n  sorry')
prefix = prefix[:original_start] + replacement + prefix[original_end:]
helper_doc = prefix.index('/--\nHelper lemma:')
prefix = prefix[:helper_doc] + helpers + '\n' + prefix[helper_doc:]
target = rest[:rest.rindex('end Erdos295')].strip()
source = prefix + '''
-- Generated from the trusted golden Target, without candidate imports.
-- Elaborate the complete declaration, retain its type, then discard the
-- temporary theorem environment before exporting the kernel-checked definition.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos295.erdos_295.variants.erdos_straus
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
end Erdos295
'''
(pkg/'FCBTrustedSpec.lean').write_text(source)
