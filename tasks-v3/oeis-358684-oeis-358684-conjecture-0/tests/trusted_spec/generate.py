"""Repair-time only: elaborate this task's immutable golden, without helpers."""
from pathlib import Path
import json
p = Path(__file__).resolve().parent
golden = (p.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The final doc comment annotates the temporary theorem, not the run_cmd.
prefix = prefix[:prefix.rindex('/--')]
# Imported private aliases are not available in the temporary Target. Preserve
# the original user-facing helper name and its exact statement/proof, changing
# visibility only in this generated evaluator artifact (never the golden).
assert prefix.count('private lemma log2_minFac_le') == 1
prefix = prefix.replace('private lemma log2_minFac_le', 'lemma log2_minFac_le')
target = rest[:rest.rindex('end OeisA358684')].strip()
source = prefix + '''
-- Elaborate the complete declaration in a temporary environment; export only
-- its complete type and ordered universes, never the placeholder theorem.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `OeisA358684.oeis_358684_conjecture_0
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
end OeisA358684
'''
(p / 'FCBTrustedSpec.lean').write_text(source)
