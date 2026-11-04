# Statement and public-proof review (2026-11-04)

## Actual task / statement

Task: `erdosproblems-247-erdos-247-refute`.
Pinned upstream read in full:
https://raw.githubusercontent.com/google-deepmind/formal-conjectures/233a10e857ef78e79fd9fe661d37db724089170a/FormalConjectures/ErdosProblems/247.lean

Public Target lines 39–53 negate exactly the universally quantified RHS of
`Erdos247.erdos_247`, not its stronger-condition variant. There are no task-local
prefix definitions. The domain is increasing natural exponents; the denominator
is k+1, and the quotient is in EReal (confirmed by independently printing the
compiled Spec). The sum is over all natural indices in R; this is a normal
zero-based transcription. Strict monotonicity gives n(k)>=k and hence geometric
summability, so there is no nonsummable-tsum-to-zero flaw. Finite index and
integer-origin shifts are harmless to this transcendence question.

Sources read:
- pinned upstream above;
- https://firsching.ch/formal-conjectures/src/FormalConjectures/ErdosProblems/%C2%AB247%C2%BB/ (complete transcription and stronger-condition reference Erdos–Graham 1980);
- https://cairn-commons.com/topics/irrationality (original question);
- https://www.jig.so/p/54?s=2 (complete canonical statement matching this underlying universal proposition).

https://www.erdosproblems.com/247 and /history/247 returned Cloudflare/HTTP 403
including no-www and query-string retries. Search indexing agrees on the original
question and its open status. No concrete defect or contradiction was found.
`statement_status=consistent` means fidelity/no evident defect, NOT that this
open negative direction is known true. Mathematical inputs were not changed.

## Public complete Lean4 proof search

First: exact task-column match in
`/root/FormalConjectures-Bench/skills/lean-task-repair/references/public-lean4-proofs.csv`:
zero rows. The positive paired task was not used to infer this result.

Search groups actually run (web_search, OpenAI provider):
1. `Erdos problem 247 limsup transcendental sum 2 n k`; `site:erdosproblems.com/247 transcendental`.
2. `"Erdos247" "Lean" proof`; `"erdos_247" proof Lean4 -site:firsching.ch`; `"Erdős" "247" Lean counterexample transcendental`.
3. `"erdos_247" site:github.com proof`; `"Erdos247" site:github.com -google-deepmind/formal-conjectures`; `"247" "transcendental" "Lean" proof counterexample`; `"Erdos" "247" "Mathlib"`.
4. `"Erdos 247" counterexample quadratic`; `"Erdős problem 247" disproof formalization`; `"sparse binary" "Lean" transcendental`; `"erdos_247" "refutation"`.

Sources / candidate exclusion:
- Current upstream `main` 247.lean was read: universal theorem and stronger-condition variant both still have sorry. Neither is a complete proof of the refutation.
- GitHub PR search https://github.com/google-deepmind/formal-conjectures/pulls?q=247 exposed #2540 and #3065. Both files API patches were read; each only changes the strong_condition category attribute. The #3065 commit source `be85167dd0b136b031ab0d717c7e16a5f7413770` was fetched. Not a proof and not this direction.
- https://www.jig.so/p/54?s=2 has an OPEN universal target, plus two checked partial statements: summability and existence of a growing sequence. Both actual Lean sources were read at artifact IDs `d8b23928-54ba-4d71-8d2c-e9cb945acebd` and `84bad9e7-640c-49d5-8481-50d6f64e3c40`. They do not prove failure of transcendence. A search summary suggesting a quadratic counterexample was disproved by this source inspection: the quadratic sequence only witnesses the hypotheses.
- A registry search hit PALOMAR-2026-10-11-000014 was followed through its dynamic page to https://data.palomar-registry.org/entries/PALOMAR-2026-10-11-000014-v1.json . It concerns Egyptian-fraction problem 206, not 247. Excluded by its complete statement/metadata.
- Cairn's irrationality topic and problem page, Mathlib-specific searches, upstream history API, AlphaProof Nexus README and attempted-theorem list were fetched/reviewed as indexes, not treated as complete proofs.
- problems.science/247/sources returned HTTP 500; search index says statement-only/no proof. An edisonymy/erdos-lean-research campaign-dossier search hit could not be retrieved on main or master (404), so no proof claim from it was accepted.

Result: `public_lean4_proof=unknown`, status `blocked`, conservatively, because
problem/discussion source access remains blocked and one research-repository
search lead is unavailable. Multiple major sources and concrete plausible leads
were checked and no complete proof of this NEGATIVE target was verified. This is
not a claim that no public proof exists. No external solution was copied into
this task or image and no external proof was compiled.

Web result IDs: mw1t0rwghzer8j, mw1t1gaz1tzr39, mw1t1pprjvgm2t,
mw1t26vvud9qqe, mw1t2ejt049h79, mw1t2vwen9l6xq, mw1t3i43dwwirn,
mw1t46z60mi958, mw1t4eaf65vfen, mw1t4ox1udyk2d, mw1t5jrjf9sdrk,
mw1t65iipqxjq4.
