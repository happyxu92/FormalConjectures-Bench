"""Repair-time extraction from this task's trusted golden, never the candidate."""
from pathlib import Path
import json

pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
assert prefix.count('import FormalConjecturesBench.Submission\n') == 1
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The trailing doc comment annotates the target, not the generated run_cmd.
# Preserve every preceding declaration; remove this comment only.
assert prefix[prefix.rindex('/--'):].rstrip().endswith('-/')
prefix = prefix[:prefix.rindex('/--')]
target = rest[:rest.rindex('end Erdos36')].strip()
source = prefix + '''
-- Elaborate the complete trusted declaration, capture its type and universes,
-- then restore the environment so no temporary target proof is exported.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos36.minimum_overlap.variants.lower.swierczkowski_1958
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
end Erdos36
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
