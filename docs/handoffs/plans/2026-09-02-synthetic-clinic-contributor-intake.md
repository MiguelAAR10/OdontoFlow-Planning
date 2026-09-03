# Synthetic Clinic — Contributor Intake #2 — FOREMAN living brief

> Written for the Architect. Self-contained: readable without opening code.
> **Live document** — opened at intake, updated as decisions are made.

## Executive status

**Phase: INTAKE COMPLETE.** Verdict: **PASS.**

A second, previously unknown contributor repository has surfaced:
`AlejandroMarceloCh/odontoflow`. It is **not** the voice module. It is a
complete, pure-frontend **clinic operations simulator** — the very thing V2 was
about to start building.

**The question this activity must answer before V2 writes a single line:** how
much of V2 already exists, and in whose hands.

**Active gate: an Owner decision on promotion.** The fan-in concluded PASS, so
promotion is *authorised by the brief's own condition* — but it is deliberately
**not performed**, because repository visibility is irreversible and that call
has not been made. See "Next approval".

**The finding that changes V2:** the simulator is not a component we could reuse.
**It is most of V2, already built and passing 98 tests.** V2 stops being a
construction problem and becomes an integration problem.

**First finding, and it changes the provenance record:** this repository is
**not solely Alejandro's**. Of its 7 commits, **one is authored by Leonardo
Panduro** (`333af34`, "feat: ampliar demo operativa de OdontoFlow"). The two
contributors worked on the same codebase. The intake must therefore credit both
here, not just in the visual baseline.

## Objective and success criteria

**Objective.** Preserve, run and map **all** remaining contributor work before
V2 starts, so V2 builds on what exists instead of unknowingly re-creating it.

**Constraints set by the brief:**

- No product behaviour changes. Voice V1 is closed and must not be reopened.
- Clone the complete repository; do not copy files into the canonical repos.
- Run the donor's **own** contract; do not repair failures during the baseline.
- Do not implement the adapter. Do not add database states. No product implementation.
- Never rewrite donor history.
- Promotion only if the fan-in concludes PASS.
- Everything donor-side is **synthetic** and must never be recorded as real clinic evidence.

**Acceptance criteria:**

| Criterion | Status |
|---|---|
| Complete repo cloned, history and origin preserved | **DONE** — 7 commits, `master`, 55 files, HEAD `b57f7bc` |
| Bundle + checksums under the contributor preservation root | **DONE** — complete history bundle; **20/20 checksums OK** |
| Donor baseline run on its own contract, unrepaired | **DONE — fully green**, nothing repaired |
| Every major asset classified | **DONE** — §3 of the contribution map |
| Appointment-state vocabulary mapped against canonical semantics | **DONE** — verified against the live schema, not docs |
| All donor data classified synthetic | **DONE** — 10 datasets, all synthetic |
| Documentation-drift contradiction verified at HEAD | **DONE — the contradiction is real** |
| Leonardo's visual baseline preserved with hashes and credited | **DONE** — 7 originals from the git object store, blob hashes match GitHub |
| Provenance recorded **separately** from the voice contribution | **DONE** — Contributions 3 and 4, never collapsed |
| Fan-in map with a revised V2 order | **DONE** — 9-step revised order |
| Promotion recommendation (not execution) | **DONE — recommend PASS**, execution withheld for the Owner |

## Repository reality

**Canonical state at intake, verified by git, all four repos clean and synced:**
planning `c723e33` · backend `23527c2` · frontend `a967b24` · voice `4149a3e`.

**Where V2 stood before this discovery.** Repo 0's `NEXT_ACTIVITY` was
*"V2 — Synthetic Clinic Configuration: connect the preserved alias vocabulary
to an editable Synthetic Clinic configuration."* The plan assumed we would
build the synthetic clinic ourselves.

**What the donor repository actually contains** (first read, ~6 200 lines of
source excluding the lockfile):

- `src/domain/` — a **pure** domain layer: an engine, explicit state
  transitions, a patient-behaviour simulator, a waitlist, rescheduling, a risk
  model, channel handling, and a seed. No database, no framework.
- `src/runtime/` — a simulated **world** with a schedule, a next-event loop and
  snapshots. This is a virtual-clock discrete-event simulator.
- `src/store/`, `src/components/` — a React operations centre with agenda,
  patients, doctors, laboratories, activity, rules and an operations view.
- `tests/` — **11 test files**, including a clock sentinel and a render smoke test.
- `scripts/verificar.ts` — the donor's own verification harness, plus a
  `VERIFICACION.md` describing it.

**The tension the brief already spotted**, and which I must verify rather than
assume: the README claims demo data is visibly labelled fictitious, while the
**HEAD commit is literally** *"quitar etiquetas de 'datos ficticios de
demostración' de la UI"* — remove the fictitious-data labels from the UI.
**Verified at HEAD: the contradiction is real** — the persistent marker is gone
(14 deletions across 3 components) and the README's claim is now false. Detail
in the decision log below.

**Protected surfaces:** backend, frontend, voice, MediStock (legacy,
read-only), and the donor's files and history.

## Authority and evidence used

- **Repo 0** read first, per protocol: `STATUS.md`, `PLAN.md`, `CAVELOG.md`, `HANDOFFS.md`.
- **The donor's own contract** (`README.md`, `VERIFICACION.md`, `package.json`) as the baseline definition — not a harness of my own invention.
- **The live canonical schema and services** for the state-compatibility question, because the workspace rule is that the schema outranks the models and the docs.
- **Prior activities' primary documents**, reused not duplicated: `VOICE_CONTRIBUTION_INTEGRATION_MAP.md`, `M5_REVENUE_LEAKAGE_BASELINE.md`, `CONTRIBUTIONS.md`.

**Originality boundary:** everything in the donor repository is the work of
**Alejandro Marcelo** and **Leonardo Panduro**. My contribution to this
activity is preservation, verification, classification and this record.

## What we will build and how

**Nothing, in this activity.** This is intake: preserve, run, map, decide.

The **target architecture** the mapping must serve — stated so the
classification has something to be right or wrong about:

```
scenario  →  donor pure simulator  →  synthetic ground truth
                                              ↓
                                    FastAPI intent adapter
                                              ↓
                                     canonical OdontoFlow
                                              ↓
                                       observed state  →  evaluator
```

The load-bearing idea: the simulator generates **ground truth** — what really
happened in a fictional clinic — while canonical OdontoFlow only ever sees
**intents** through an adapter, and an evaluator compares what the system
observed against what actually happened. That is what makes it a measurement
instrument rather than a second source of business truth.

**Deliberately not built here:** the intent adapter, any database state, any
canonical UI change.

## Execution model

**Solo.** The work is a dependency chain — clone, preserve, run the baseline,
read, classify, decide — where each step consumes the previous step's output.
The repository is ~6 200 lines, small enough to read directly and too
interconnected to split without two workers contending on the same files.
No competing approaches need comparing before committing.

## Risks, conflicts, and protected surfaces

| Risk | Standing at intake |
|---|---|
| **We were about to rebuild work that already exists** | The whole reason for this activity. Severity depends on the baseline: a green simulator makes V2 mostly an integration problem instead of a construction problem. |
| **A simulator becoming a second business authority** | The central architectural risk. Synthetic ground truth and canonical state must never merge; the adapter boundary is what keeps them apart, and it is exactly what is *not* being implemented yet. |
| **Synthetic data mistaken for clinic evidence** | Sharpened by the HEAD commit removing the fictitious-data labels. Whatever the reason, the canonical Synthetic Lab must keep a **visible** synthetic-data boundary. |
| **Provenance collapse** | Two distinct contributions from the same person, plus a Leonardo commit inside an "Alejandro" repo. The brief is explicit: do not collapse them. |
| **State-vocabulary temptation** | The donor's appointment states include exactly what M5.1 found unmeasurable (`no_show`, `no_response`, `recovered`). It will be tempting to adopt them into the database. This activity must map, not migrate. |

## Evidence and validation

**The donor's own contract, run unrepaired.** Node v24.12.0 / npm 11.6.2.

| Check | Result |
|---|---|
| `npm install` | clean |
| `npm run typecheck` | **clean** |
| `npm test` | **98 passed / 11 files / 1.31 s** |
| `npm run build` | **PASS** (57 modules, 1.49 s) |
| `npm run verificar` | **"Recorrido completo sin fallos"** — all 8 steps ok |

The walkthrough is worth reading as evidence in its own right: it advances the
virtual clock, watches reminders send themselves, cancels an appointment, sees
the waitlist recover the slot, **rewinds time and confirms the world rebuilds
identically**, and asserts no reminder was ever sent twice.

**Preservation.** Complete-history bundle plus commit log with authorship;
Leonardo's 7 screenshots extracted from the git object store as originals
(blob hashes match what GitHub reports). Master checksums: **20 of 20 OK**.

**Known limitations, the author's own and not hidden:** no authentication,
`localStorage` persistence only, desktop-optimised design, no real messaging
channel, and the waitlist not editable from the UI.

Evidence paths: `.audit/contributions/synthetic-clinic/donor-baseline-raw.txt` ·
`_preservation/odontoflow-contributors-2026-09-02/`.

## Decision and progress log

| Date | Entry |
|---|---|
| 2026-09-02 | **Intake opened.** Canonical state verified clean and synced across all four repos before touching anything. |
| 2026-09-02 | Repository cloned complete: HEAD `b57f7bc`, branch `master`, 7 commits, 55 files, no tags, original `origin` preserved. Nothing copied into any canonical repo. |
| 2026-09-02 | **Provenance correction at intake:** one of the 7 commits (`333af34`) is authored by **Leonardo Panduro**, not Alejandro. This is a shared codebase and will be credited as such. |
| 2026-09-02 | **This brief was opened at intake, not after completion** — the explicit instruction, and the correction of the previous activity's failure. |

### Decisions taken during execution

| Date | Entry |
|---|---|
| 2026-09-02 | Baseline run on the donor's contract and **fully green**. Nothing repaired, per the brief. |
| 2026-09-02 | **Documentation drift confirmed, and characterised precisely.** The README claims the whole interface is labelled synthetic; HEAD removes exactly those labels (14 deletions, 3 components, zero insertions). At HEAD the claim is **false** — the persistent marker is gone, three scattered mentions survive, and after pressing "start" there is no marker in sight. No judgement of intent; the consequence is that HEAD screenshots are indistinguishable from a real clinic's. Binding requirement recorded: the canonical Synthetic Lab must carry a **visible, persistent, non-dismissible** boundary. |
| 2026-09-02 | **State vocabulary mapped, not migrated.** Verified against the live schema: canonical admits only `confirmed`/`cancelled`, appointments are born `confirmed`, and there is **no** reminder, waitlist or no-show concept anywhere. Result: 2 canonical now, 2 derived, 3 ground-truth-only, 2 requiring instrumentation. **No database state added**, per the brief — importing nine states before an evaluator justifies them would bake in a vocabulary nothing has measured. |
| 2026-09-02 | Found a **semantic collision** worth flagging rather than smoothing over: canonical `confirmed` means *"booked"*, donor `confirmed` means *"the patient confirmed"*. Same word, different fact. |
| 2026-09-02 | **Configuration surface already exists**: the donor's rules screen edits five parameters live with cross-field validation. V2's original goal does not start from zero — it extends a working pattern. And the **behaviour probabilities** turn out to be the most valuable dial in the system. |
| 2026-09-02 | **Promotion recommended (PASS) but not performed.** Two reasons: the brief separates the conclusion from the act, and repository visibility is an irreversible Owner decision — the voice repo was created private for that reason and the call is still open. Assuming the same answer twice unasked would be inventing a policy. |
| 2026-09-02 | Recorded that `AlejandroMarceloCh/odontoflow` is a **simulator**, not the product, despite the name — which is exactly why `odontoflow-sim` is the right canonical name if promotion is approved. |

## Next approval / next step

**Three decisions are yours, and nothing proceeds without them:**

1. **Promote the simulator to `odontoflow-sim`?** Fan-in says PASS. If yes, also say **public or private** — the voice repo is private and I did not assume the same answer here.
2. **The visual-language question.** The simulator carries its own design (dark workstation, monospace numerics), a different lineage from Leonardo's baseline. Reconciling them is a design decision for you and Leonardo, not a refactor for me.
3. **Whether V2 keeps its original scope** or adopts the revised 9-step order, which now starts by *restoring the synthetic-data boundary* rather than by building configuration.

**Then, in order:** restore the boundary → turn the seed into a named Scenario
Configuration → join the voice alias vocabulary → define the intent vocabulary
and give the simulator a principal → build the adapter (rehearsal first) → turn
it on against a scratch database → **build the evaluator** → run the no-show
experiment.

**Why that last step matters more than it looks.** M5 stalled for lack of real
clinic data, and a simulator does not replace it. But a calibrated simulator
*can* answer a question we could not touch before: **if the clinic did have a
20 % no-show rate, would OdontoFlow detect it?** M5.1 argued the answer is no.
Step 8 would measure it instead of arguing — turning backlog item **I1** from an
opinion into evidence.

**Unchanged:** this contribution supplies **no real clinic data**.
`DOMINANT_LEAKAGE` remains `UNKNOWN`. A simulator is not a clinic.
