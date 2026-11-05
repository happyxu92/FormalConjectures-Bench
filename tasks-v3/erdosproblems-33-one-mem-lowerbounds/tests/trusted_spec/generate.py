"""Repair-time generation from this task's immutable golden, without candidates."""
from pathlib import Path
import json
pkg = Path(__file__).resolve().parent
golden = (pkg.parent / 'golden_env/FormalConjecturesBench/Target.lean').read_text()
prefix, rest = golden.split('-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN', 1)
prefix = prefix.replace('import FormalConjecturesBench.Submission\n', '')
# The earlier open research theorem is not a definition or a dependency of this
# target. Exclude its placeholder (and answer command) from the exported module.
prefix = prefix[:prefix.index('/-- Let `A ⊆ ℕ` be a set such that every integer can be written as `n^2 + a`\n')]
target = rest[:rest.rindex('end Erdos33')].strip()
source = prefix + '''
-- Elaborate the entire original declaration in an isolated temporary environment.
open Lean Elab Command in
run_cmd do
  let original ← getEnv
  let stx ← ofExcept <| Parser.runParserCategory (← getEnv) `command ''' + json.dumps(target, ensure_ascii=False) + '''
  elabCommand stx
  let some info := (← getEnv).find? `Erdos33.erdos_33.variants.one_mem_lowerBounds
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
end Erdos33
'''
(pkg / 'FCBTrustedSpec.lean').write_text(source)
