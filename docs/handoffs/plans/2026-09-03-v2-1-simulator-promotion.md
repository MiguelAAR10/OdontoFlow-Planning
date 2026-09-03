# V2.1 — Simulator Promotion & Synthetic Boundary — FOREMAN living brief

> Written for the Architect. Self-contained: readable without opening code.
> **Live document** — opened before any change, updated as decisions are made.

## Executive status

**Phase: COMPLETE.** Verdict: **PASS.**

V2.1 does two things and nothing else: bring Alejandro and Leonardo's clinic
simulator into canonical OdontoFlow **without touching its history**, and make
its synthetic-data boundary **structurally obvious** before anyone builds on it.

**The Owner decision that was blocking this is now answered:** promote, and
**private**. Intake #2 recommended promotion but withheld the act because
visibility is irreversible. That gate is closed.

**Active gate:** none. Nothing is waiting on you.

**One design question is open and deliberately not mine to settle:** the
simulator carries its own visual language (dark workstation, monospace
numerics), a different lineage from Leonardo's baseline. Reconciling them is a
conversation for you and Leonardo, not a refactor for me.

**The one judgement call worth your scrutiny:** how far a "non-dismissible
boundary" may reach into a contributor's interface. The brief asked for
unmissable *and* for no redesign of their UI, and those pull against each other.
I resolved it by putting the band in the **shell** rather than in the pages —
structurally present everywhere, while their views are untouched. Five lines of
their code changed. If you would rather it looked different, that is a style
change on top of a guarantee that now holds.

## Objective and success criteria

**Objective.** A canonical `odontoflow-sim` repository whose donor history is
byte-identical to what the contributors wrote, and whose interface can never be
mistaken for a real clinic.

**Constraints set by the brief:**

- Move the repository; **never** copy files, `git init`, squash, rebase or force.
- HEAD must remain exactly `b57f7bc`; `git fsck` must pass.
- Preserve all 7 donor commits — 6 Alejandro, 1 Leonardo.
- Run the donor contract **unchanged** as the baseline; fix nothing unrelated.
- Update the README only enough to match reality; **do not** rewrite it for style.
- Add only tests needed to prove the boundary.
- **Determinism and the clock sentinel must survive untouched.**
- **No integration of any kind** — no FastAPI, no adapter, no new states, no
  waitlist or lab tables, no voice vocabulary, no UI port, no agents, no WhatsApp.
- Never claim authorship of donor code.

**Acceptance criteria:**

| Criterion | Status |
|---|---|
| All repos verified clean and synced before touching anything | **DONE** |
| Repository moved, not copied; HEAD still `b57f7bc`; `fsck` passes | **DONE** — exact match, `fsck` clean, 0 tracked files modified |
| 7 donor commits intact, both authors preserved | **DONE** — 6 Alejandro + 1 Leonardo, verified **on the remote** |
| `MiguelAAR10/odontoflow-sim` created **private**; remotes set | **DONE** — `origin` canonical, `alejandro` upstream |
| Donor commits visible on the remote with original authorship | **DONE** — checked via the API, not just locally |
| Baseline reproduced before modification (98 tests, 11 files, clean walkthrough) | **DONE** — exactly as expected |
| Persistent, non-dismissible synthetic boundary on **every** view, desktop and mobile | **DONE** — in the shell's sticky header, outside the view switch |
| README matches actual HEAD behaviour, contributor terminology preserved | **DONE** — one paragraph corrected, voice preserved |
| Focused tests prove the boundary | **DONE** — 10 sentinel-style tests |
| Full suite, typecheck, build and walkthrough still green after the change | **DONE** — 109 tests, build PASS, walkthrough clean |
| Clock sentinel intact; determinism unchanged | **DONE** — sentinel grew 32→33 on its own |
| Zero canonical product change (backend / frontend / voice) | **DONE** — all three unchanged, 0 files modified |

## Repository reality

**Canonical state before the activity**, verified by git — all four repos clean
and synced: planning `04acfc1` · backend `23527c2` · frontend `a967b24` · voice
`4149a3e`. The contributor simulator is clean at `b57f7bc` on `master`, with 0
tracked files modified.

**What is being promoted** (established in intake #2, not re-audited here): a
pure, deterministic clinic operations simulator — ~6 200 lines, 55 files, a
virtual clock with a reversible timeline, a 9-state appointment machine, a
waitlist with slot recovery, a risk heuristic and a React operations centre.
Baseline was green on its own contract: 98 tests, build passing, and the
author's own 8-step walkthrough finishing clean.

**The defect being repaired.** The donor's README states that the whole
interface carries a visible *"Datos ficticios de demostración"* label. The HEAD
commit is titled *"quitar etiquetas…"* and removes exactly those labels — 14
deletions across the welcome screen, the workstation shell (desktop **and**
mobile) and the activity view, with zero insertions. So at HEAD the README's
claim is **false**: once you press "Iniciar demostración" there is no persistent
marker anywhere. Three scattered, view-specific mentions survive, none of them
always visible.

Why that matters more than a documentation nit: **screenshots taken from HEAD
are indistinguishable from a real clinic's.** This repository is about to become
canonical, and its whole purpose is to produce numbers that must never be
mistaken for evidence.

**Protected surfaces:** backend, frontend, voice, MediStock (legacy,
read-only), the donor's commit history, and the determinism guarantees —
specifically `tests/reloj-sentinel.test.ts`, the 32-assertion guard that fails
if any source file reads real time.

**A pre-existing worktree condition worth noting:** `node_modules/` and `dist/`
from the intake baseline are present and git-ignored. They survive the move and
make the baseline immediately re-runnable, which is convenient — but the move
will break the installed binaries' absolute paths, exactly as it did with the
voice repo's Python venv. Expect a reinstall.

## Authority and evidence used

- **Repo 0** first, per protocol: `STATUS.md`, `PLAN.md`, `CAVELOG.md`, `HANDOFFS.md`, `REPOSITORIES.md`.
- **The intake #2 primary documents**, reused and **not re-audited**: `SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md`, `CONTRIBUTIONS.md`, `VISUAL_BASELINE.md`, and the intake living brief. The brief is explicit that intake is closed.
- **The donor's own contract** (`package.json`, `README.md`, `VERIFICACION.md`) as the definition of the baseline — not a harness of my own.
- **The voice promotion precedent** (`odontoflow-voice`, V1): move-not-copy, verify HEAD and `fsck`, rename the donor remote to the author's name, add a canonical `origin`, and put all canonical metadata in **one** new file so the contributor's tree stays untouched. Following a precedent that already worked beats inventing a second pattern.

**Originality boundary.** Everything being promoted is the work of **Alejandro
Marcelo** and **Leonardo Panduro**. My contribution here is the promotion
mechanics, the synthetic boundary, its tests, the documentation alignment and
this record. Their code is not mine and the commit will say so.

## What we will build and how

**Promotion** follows the voice precedent exactly: `mv` on the same filesystem
so `.git` survives whole, then verify HEAD and `fsck` before trusting anything.
Remotes become `origin` → canonical and `alejandro` → the contributors' upstream.
Push normally.

**The synthetic boundary — and the tension I have to resolve.** The brief wants
it unmissable, on every view, undismissable, on both form factors, not styled
like an error, and *without redesigning the contributor's interface*.

My approach: put it in the **shell**, not in the pages. The donor already has a
single workstation component that wraps every view; a boundary rendered there is
structurally present on every route by construction, rather than by remembering
to add it to each page. That is also what makes it testable as a property rather
than as seven separate assertions.

Two consequences I am choosing deliberately:

- **Not dismissible means no dismiss affordance at all** — no close button, no
  state, nothing to persist. The cheapest way to guarantee something cannot be
  turned off is to give it no mechanism for being turned off.
- **Not styled like an error** — this is a standing fact about the data, not a
  fault. It should read as a label, not an alarm, so it survives familiarity
  without either being ignored or looking broken.

I will restore the boundary the contributor originally had, in the place he had
it, and extend it to hold on every view and both form factors. **Not a
redesign** — closer to reinstating his own decision with the coverage the README
already promised.

**Documentation** gets the minimum: make the README's claim true again, keep his
words and his terminology, and put canonical/provenance metadata in a separate
new file rather than editing his prose to talk about ownership.

**Deliberately not built:** everything in §8 of the brief. V2.1 is promotion
plus safety boundary, full stop. Anything that connects the simulator to
canonical OdontoFlow is V2.2 and later, and the first requirement there is not
code — it is giving the simulator a principal.

## Execution model

**Solo.** A strict dependency chain: verify → move → verify → remote → baseline
→ repair → test → verify again. Every step consumes the previous step's output,
and the repair touches shared files. There are no independent pieces and no
competing approaches worth comparing. Orchestration would add coordination cost
for no wall-clock saving and no better decision.

## Risks, conflicts, and protected surfaces

| Risk | Mitigation |
|---|---|
| **Losing donor authorship in the move** | `mv`, never copy. HEAD and `fsck` verified immediately after, and both authors confirmed on the remote — not just locally. |
| **Breaking determinism while touching the UI** | The change is confined to the shell's presentation. The clock sentinel and the full 98-test suite are re-run afterwards; if determinism moved, they fail. |
| **Over-reaching into the contributor's design** | Restore what he had, extend its coverage, change nothing else. Any further design change is an Owner/Leonardo conversation, not mine. |
| **A boundary that technically exists but nobody sees** | Placed in the shell so it cannot be omitted per-page; tested as a property, not per-view. |
| **Rewriting his README voice** | Only the false claim is corrected. Canonical metadata goes in its own file. |
| **Scope creep into integration** | §8 is a hard stop; the brief enumerates it and so does this document. |

## Evidence and validation

**Baseline, before touching anything** — the contributors' contract, unchanged:
typecheck clean · **98 tests / 11 files** · build PASS · `npm run verificar`
*"Recorrido completo sin fallos"* across all 8 steps.

**After the boundary repair** — same contract plus the new tests:

| Check | Result |
|---|---|
| `npm run typecheck` | **clean** |
| `npm test` | **109 passed / 12 files** |
| `npm run build` | **PASS** (58 modules) |
| `npm run verificar` | **"Recorrido completo sin fallos"** |

The arithmetic is worth stating: 98 baseline + 10 new boundary tests + **1 the
clock sentinel generated by itself**, because it scans every file under `src/`
and picked up the new component. The sentinel doing its job unprompted is the
best evidence that determinism is still guarded.

The walkthrough still asserts the two properties that matter most — *"ir y
volver reproduce el mismo mundo"* (the timeline rebuilds identically) and
*"ningún recordatorio se envió dos veces"* (idempotency). Neither moved.

**Scope of the change, precisely:** two new files (`BandaSintetica.tsx`, its
test), one new documentation file (`CANONICAL.md`), **+5 lines** in the
contributors' shell, and **one paragraph** of their README. Their
`package-lock.json` was rewritten by `npm install` twice and reverted both
times — a lockfile churn is none of the three things the brief permits in the
first canonical commit.

Evidence paths: `.audit/contributions/synthetic-clinic/v21-baseline-pre.txt` ·
`.audit/contributions/synthetic-clinic/v21-final-post.txt` ·
`odontoflow-sim/CANONICAL.md`.

**Known limitations, unchanged and the authors' own:** no authentication,
`localStorage` persistence only, desktop-optimised, no real messaging channel,
waitlist not editable from the UI.

## Decision and progress log

| Date | Entry |
|---|---|
| 2026-09-03 | **Brief opened before any change**, per the instruction and as the standing correction of the V1 failure. |
| 2026-09-03 | Canonical state verified clean and synced across all four repos; contributor simulator clean at `b57f7bc` with 0 tracked modifications. MediStock untouched. |
| 2026-09-03 | **Owner decisions received and recorded:** promote, visibility **private**. This closes the gate intake #2 left open. |
| 2026-09-03 | Chose to follow the **voice promotion precedent** rather than invent a second pattern: move-not-copy, verify HEAD + `fsck`, donor remote renamed to the author's name, all canonical metadata in one new file. |

### Decisions taken during execution

| Date | Entry |
|---|---|
| 2026-09-03 | Moved by `mv`, verified HEAD `b57f7bc` and `fsck` **before trusting anything**. The move broke `node_modules` binary paths (same as the voice venv) — reinstalled; git-ignored build state, not contributor code. |
| 2026-09-03 | Had to switch `gh` accounts again to create the repository (`MigueAriasNEO` was active, not `MiguelAAR10`) and **restored the original account afterwards**. Verified authorship on the remote via the API rather than trusting the local log. |
| 2026-09-03 | **Resolved the boundary tension by placing it in the shell.** The brief wanted it unmissable on every view *and* no redesign of the contributors' UI. A band in the station shell's sticky header, outside the view switch, is present on every route and at every scroll position **by construction** — not by remembering to add it per page. Three deliberate choices: no dismiss affordance at all (the safest way to make something unturnoffable is to give it no switch); the authors' own `wait` tokens so it reads as a standing label, not an alarm; and one single text with **no responsive variants**, because a label that changes meaning with viewport width is a label you cannot trust. |
| 2026-09-03 | **Tests guard the property, not the pixels.** The original labels were deleted and no test complained — that is *why* the README could assert something false. The new tests therefore also assert that the band is mounted unconditionally, outside the view switch, inside the sticky header, with no dismiss control, no display toggles, and that no view is rendered by a parallel shell that would escape it. Written in the spirit of the authors' own clock sentinel. |
| 2026-09-03 | **Fixed my own test, not their component.** A first assertion banned the substring `hidden`, which wrongly matched the legitimate `aria-hidden` on a decorative dot. Narrowed to inspect `class` attributes only. The component was right; the assertion was sloppy. |
| 2026-09-03 | README corrected **only where it was false**, with a maintenance note explaining the history. Their voice and terminology preserved; no stylistic rewrite. All canonical/provenance metadata went into a **separate** file rather than editing their prose to talk about ownership. |
| 2026-09-03 | **No integration, deliberately.** Nothing connects to FastAPI, no adapter, no canonical states, no waitlist or lab tables, no voice vocabulary, no UI port, no agents, no WhatsApp. Canonical backend, frontend and voice verified unchanged. |

## Next approval / next step

**Nothing is blocked.** V2.1 is complete and pushed.

**Next activity: V2.2 — Named Scenario Configuration.** Turn the contributors'
hard-coded seed into named, editable scenarios, starting from the surface that
already works — their rules screen edits five parameters live with cross-field
validation. The highest-value dial is the **behaviour probabilities**, because
they are what would eventually let us ask *"if the clinic had a 20 % silence
rate, would OdontoFlow detect it?"*

**One constraint carries forward as a precondition, not a feature:** the
synthetic-data boundary is in place, and V2.2 must not weaken it while making
the scenario editable. Making data editable is exactly the moment when
someone is tempted to make the "demo" label conditional.

**Unchanged, and worth restating because a working simulator makes it easy to
forget:** real M5 validation is **BLOCKED_EXTERNAL** and
`DOMINANT_LEAKAGE = UNKNOWN`. This activity contributed **no real clinic data**.
A simulator is not a clinic — it can eventually prove whether our
instrumentation *would* catch a problem, but it cannot tell us whether the
clinic has one.
