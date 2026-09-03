---
title: OdontoFlow — Synthetic Clinic Contribution Map
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning) — fan-in synthesis; evidence in .audit/contributions/synthetic-clinic/
donor_repo: https://github.com/AlejandroMarceloCh/odontoflow
donor_head: b57f7bc6b1eca84a132b61a11ca687bbd5b5e58e
---

# Synthetic Clinic — Contribution Map

One synthesis over `AlejandroMarceloCh/odontoflow`. **No implementation.
Nothing promoted, nothing ported, no product code changed.**

Living brief: [docs/handoffs/plans/2026-09-02-synthetic-clinic-contributor-intake.md](docs/handoffs/plans/2026-09-02-synthetic-clinic-contributor-intake.md)
Credit: [CONTRIBUTIONS.md](CONTRIBUTIONS.md) · Raw runs: `.audit/contributions/synthetic-clinic/`

---

## 1 · WHAT ALEJANDRO ALREADY BUILT

A complete, working **clinic operations simulator**. Not a mockup — a
deterministic discrete-event simulation with a pure domain core, a virtual
clock, a reversible timeline and 98 passing tests.

`master` @ `b57f7bc` · 7 commits · 55 files · ~6 200 lines of source.

**Provenance note that must not be lost:** 6 of the 7 commits are Alejandro's;
**one is Leonardo Panduro's** (`333af34`, "feat: ampliar demo operativa"). This
is a shared codebase.

**The layers, in the author's own order of importance:**

- **`src/domain/` — pure, no I/O, no clock.** A rules engine (`evaluate()`), an explicit state machine, a risk heuristic, message drafting, a waitlist matcher, a rescheduling proposer, a deterministic seed and a patient-behaviour simulator.
- **`src/runtime/` — the world.** `reproducir(catalog, events, rules, target)` rebuilds the clinic from the seed and replays history to any instant; `buildSnapshot()` produces the paint-ready state; `horario.ts` keeps the virtual clock inside opening hours.
- **`src/store/` + `src/components/` — the operations centre.** Operations queue, agenda board by state, patients, doctors, laboratories, activity feed and an editable rules screen.
- **`scripts/verificar.ts`** — the author's own eight-step end-to-end walkthrough, run from the console against the pure runtime.

**Two design decisions that carry the whole thing:**

1. **The engine is a pure function** — no effects, and it never reads the system clock. There is a dedicated test (`reloj-sentinel.test.ts`, 32 assertions) that fails if *any* file under `src/` reads real time. The author's reasoning: if someone uses the real clock, advancing the virtual clock silently stops working and the simulation breaks without an error.
2. **The past is rebuilt, never undone.** Dragging the timeline backwards re-runs history from the seed. That is what makes the simulation reproducible — and it is exactly the property a ground-truth engine needs.

## 2 · WHAT WE WERE ABOUT TO REBUILD

Repo 0's `NEXT_ACTIVITY` read: *"V2 — Synthetic Clinic Configuration."* The plan
assumed we would build the synthetic clinic.

**We would have rebuilt, badly and slower, work that already exists and passes
98 tests:**

| We were going to build | He already built it |
|---|---|
| A synthetic clinic with patients, doctors, treatments and appointments | Deterministic seed: 28 patients, 4 doctors, 10 treatments, 60 appointments |
| A way to advance time to see the funnel happen | Virtual clock with a **reversible** timeline and a real replay engine |
| Appointment lifecycle states | A 9-state machine with **illegal transitions raising errors**, not corrupting data |
| Reminder / confirmation / no-response logic | A pure, **idempotent** rules engine with duplicate-send protection as its most-tested property |
| Something to model no-shows | A deterministic patient-behaviour simulator, ~62/13/25 split, weighted by prior no-shows |
| A configuration surface for the scenario | An editable rules screen with cross-field validation, already wired |

**And two things we had not even thought to build:** a **waitlist with slot
recovery** (cancel → offer → accept → `recovered`), and a **laboratory
tracking** module with automatic overdue alerts.

That is the finding of this activity. V2 is now an **integration** problem, not
a construction problem.

## 3 · WHAT SHOULD BE REUSED

Classification of every major asset.

### `REUSE_AS_IS` — pure, tested, no dependencies to untangle

| Asset | Lines | Why |
|---|---|---|
| `domain/engine.ts` | 135 | Pure, idempotent, 13 tests. The product's logic, and it reads no clock. |
| `domain/transitions.ts` | 42 | The 9-state machine. Refuses illegal transitions instead of corrupting state. 6 tests. |
| `domain/risk.ts` | 60 | Explainable heuristic with a one-sentence reason string — deliberately *not* a statistical model, which is the right call for something a clinic owner has to trust. |
| `domain/lista-espera.ts` | 62 | Deterministic candidate matching by treatment/dentist/time window, ordered by seniority. 5 tests. |
| `domain/reprogramacion.ts` | 92 | Deterministic non-overlapping slot proposals. |
| `domain/channel.ts` | 68 | Message drafting in neutral Peruvian Spanish. Text only, no transport. |
| `domain/paciente-sim.ts` | 105 | Deterministic behaviour from a hashed id — no `Math.random`, no dates. **This is what makes ground truth reproducible.** |
| `runtime/horario.ts` | ~60 | Clock clamping to opening hours. |
| `tests/reloj-sentinel.test.ts` | 32 assertions | **Carry this over verbatim.** It is the guard that keeps the whole property alive. |

### `PORT_WITH_ADAPTER`

| Asset | Adaptation needed |
|---|---|
| `runtime/mundo.ts` (693) | The replay engine. Sound as-is, but it currently replays **into its own world**. As a ground-truth engine it must also **emit intents** for the adapter. Add an output, do not change the replay. |
| `runtime/snapshot.ts` (555) | Paint-ready projection. Reusable, but today it is shaped for *this* UI; the evaluator will want a comparable projection of *canonical observed* state beside it. |
| `store/OdontoStore.tsx` (202) | React + `localStorage`. Fine for a lab; the scenario itself should become a named, shareable configuration rather than a browser-local blob. |
| `domain/seed.ts` (288) | Deterministic and excellent, but **hard-coded**. Becomes the default scenario; the values become editable configuration (see §6). |

### `GROUND_TRUTH_ONLY` — must never become canonical business authority

| Asset | Why it stays simulation-side |
|---|---|
| The whole `runtime/` replay | It knows what "really happened" in a fictional clinic. Canonical OdontoFlow must only ever learn things through the adapter, like it would from a real clinic. |
| `paciente-sim.ts` outcomes | The simulated patient's decision *is* the ground truth the evaluator scores against. If canonical could read it, the measurement would be circular. |
| Simulated WhatsApp sends and inbound replies | In-memory messages. No transport, and none should be added here — the voice repo already owns the real-channel question. |
| Lab jobs and overdue alerts | No canonical counterpart exists at all (see §5/§7). |

### `UX_REFERENCE`

| Asset | Why |
|---|---|
| `VistaOperacion.tsx` (224) | The **operations centre** — "what needs attention today?" as a prioritised queue with metrics kept secondary. This is a genuinely good product idea and OdontoFlow has no equivalent. |
| `VistaAgenda.tsx` (288) | Agenda as a board by state, with the conversation and available actions beside the selected appointment. |
| `VistaDoctores.tsx` (164) | Cancellation impact on a specific dentist's day; highlights day-restricted dentists. |
| `VistaLaboratorios.tsx` (137) | Simple, legible external-work tracking. |
| `Timeline.tsx` (160) · `Estacion.tsx` (329) | The virtual-clock control and the workstation shell. **Different visual lineage** from Leonardo's baseline (dark header, monospace numerics) — see [VISUAL_BASELINE.md](VISUAL_BASELINE.md). Reconciling the two is a design decision, not a merge. |

### `DOMAIN_CONCEPT` — ideas worth adopting even if no code moves

- **Waitlist + slot recovery.** Cancel → offer → accept → `recovered`. This is revenue recovery, and it is precisely candidate #2 in the M5 leakage list ("late cancellations not refilled"). OdontoFlow has no waitlist at all.
- **Exposure ordering** (`risk × price`): rank the work queue by *money actually at stake*, not by risk alone.
- **`accionHumana`** — the activity feed distinguishes what the system did by itself from what it created as a task for a human. That distinction is what would let us measure automation value later.
- **Laboratories as an operational domain.** Out of current scope; a real clinic need.

### `DEFER`

- The real WhatsApp adapter (the voice repo already owns that question, and V1 closed with it unverified).
- Authentication and roles — the author lists this as blocking for production, and it is a platform decision.
- Waitlist editing from the UI (his own stated limitation: candidates come from the seed).
- Mobile polish (his own stated limitation: desktop-optimised).

### `OBSOLETE`

**None.** Nothing in this repository is obsolete. The one thing to *not* carry
forward is the HEAD commit's removal of the synthetic-data labels (§7) — and
that is a decision to reverse, not dead code.

---

## 4 · SYNTHETIC ENGINE — how it becomes ground truth without becoming authority

Target concept, restated:

```
scenario → donor pure simulator → synthetic ground truth
                                          ↓
                                FastAPI intent adapter
                                          ↓
                                 canonical OdontoFlow
                                          ↓
                                   observed state → evaluator
```

**Why the donor's simulator can hold this role**, and this is not a lucky
accident — it is a consequence of choices he made and tested:

1. **It is pure.** No database, no network, no system clock. It can be run headless, in a script, in CI.
2. **It is deterministic.** Behaviour derives from hashed ids, never from randomness. The same scenario always produces the same ground truth — which is the *definition* of a usable measurement baseline.
3. **It is reversible.** `reproducir(...)` rebuilds from the seed to any instant, so ground truth at any point in time is recomputable rather than stored.
4. **It already separates decision from effect.** `evaluate()` returns *actions*; the runtime applies them. Actions are one short step from **intents**.

**The one boundary that keeps it honest.** The simulator must never write to,
read from, or be consulted by canonical OdontoFlow. The only permitted flow is:
the simulator emits an intent → the adapter translates it into an ordinary
canonical command (`POST /appointments`, `/visits`, `/charges`, …) with a real
principal and an idempotency key → canonical does whatever it would do with a
real clinic's request. Canonical never learns that the request came from a
simulation, and never sees ground truth.

**The evaluator is then the actual product of this architecture:** it compares
what the simulator knows happened against what canonical observed, and the gap
*is* the measurement. Concretely, it is the instrument that could finally answer
M5.1's unmeasurable question — feed it a scenario with a known no-show rate and
check whether canonical can detect it. If canonical cannot, that is proof the
instrumentation gap (M5.1 backlog item I1) is real, measured rather than argued.

**Not implemented in this activity**, per the brief. What it needs when
authorised: an intent vocabulary, a principal for the simulator, idempotency
keys per simulated action, and a comparison projection. All of that is V2+ work.

---

## 5 · STATE COMPATIBILITY

Donor appointment vocabulary against canonical FastAPI semantics, verified
against the live schema and services at backend `23527c2` — **not** against docs.

**The canonical baseline, stated first because everything below depends on it:**
`appointments.state` is `CHECK (state IN ('confirmed', 'cancelled'))`. Booking
creates a row **already `confirmed`**. There is **no** reminder, waitlist or
no-show concept anywhere in `app/` or `alembic/` (exhaustive search: zero hits).

| Donor state | Canonical reality | Verdict |
|---|---|---|
| `scheduled` | Collapses with `confirmed`: a canonical appointment is born `confirmed`. **The word means different things on each side** — canonical `confirmed` = "booked", donor `confirmed` = "the patient confirmed". | **CANONICAL_NOW** (as "booked") — but the semantic collision must be documented, not glossed over |
| `reminded` | Nothing. No reminder table, field, or audit action. | **GROUND_TRUTH_ONLY** |
| `confirmed` (patient assent) | Not representable. Canonical cannot distinguish a booked appointment from one the patient acknowledged. | **REQUIRES_FUTURE_INSTRUMENTATION** |
| `reschedule_requested` | Canonical has `appointment.rescheduled` in `audit_events` — the *completed act*, mutating the row in place. It has no notion of a **pending request**. | **GROUND_TRUTH_ONLY** |
| `no_response` | Nothing. | **GROUND_TRUTH_ONLY** |
| `no_show` | Nothing — and **not derivable**: M5.1 established that the absence of a `visits` row on a past confirmed appointment conflates no-show, unrecorded visit and still-pending. | **REQUIRES_FUTURE_INSTRUMENTATION** (M5.1 backlog **I1**) |
| `cancelled` | `state='cancelled'`, CHECK-constrained, terminal (`_require_confirmed` blocks re-cancel); the instant is recoverable from `audit_events`. | **CANONICAL_NOW** |
| `recovered` | Not a state. **Partially derivable**: a cancelled appointment whose freed interval later holds a new confirmed appointment for the same practitioner. But the *causal link* to a waitlist offer is unrecoverable — canonical has no waitlist. | **DERIVED** (the refill), **GROUND_TRUTH_ONLY** (the causation) |
| `completed` | Not a state. **Derivable and sound**: a `visits` row exists for the appointment. Attendance is provable in the positive direction. | **DERIVED** |

**Verdict: 2 canonical now, 2 derived, 3 ground-truth-only, 2 requiring
instrumentation.** The donor's vocabulary is **richer than canonical's**, and
the gap is not an oversight on either side — canonical models *what the clinic
committed to and what it did*, while the donor models *the conversation that
decides whether it happens*.

**No database state is added in this activity.** The temptation to import these
nine states into the `CHECK` constraint should be resisted until an evaluator
proves which of them the business actually needs — that is the whole point of
building the measuring instrument first.

---

## 6 · DATA INVENTORY — all synthetic

Every dataset below is **SYNTHETIC**. None is real clinic evidence, and none may
ever be recorded as such.

| Dataset | Volume | Nature | Editable as Scenario Configuration? |
|---|---|---|---|
| Patients | 28 (invented Peruvian names) | SYNTHETIC | **Yes** — count, names, phones, prior-no-show counts |
| Doctors | 4, with `diasAtiende` and specialties | SYNTHETIC | **Yes** — and this maps cleanly onto canonical `practitioners` + `availability_rules.day_of_week` |
| Treatments | 10, with duration and price in cents | SYNTHETIC | **Yes** — the natural join point to a real tariff later |
| Appointments | 60 around a fixed start instant | SYNTHETIC | **Yes** — volume, spread, and the fixed demo window |
| Waitlist | 5 candidates (`w1`–`w5`) with windows and preferences | SYNTHETIC | **Yes** |
| Laboratories | 3, with contact numbers | SYNTHETIC | **Yes** |
| Lab jobs | 6, with promised dates and owners | SYNTHETIC | **Yes** |
| Rules | 5 (`firstReminderHours` 24, `secondReminderHours` 2, `alertAfterHours` 6, open 8, close 20) | CONFIGURATION | **Already editable in the UI**, with cross-field validation |
| Behaviour probabilities | ~62 % confirm / 13 % reschedule / 25 % silence, plus a prior-no-show weighting | SYNTHETIC **ASSUMPTION** | **Yes — and these are the most valuable knobs in the whole system** |
| Scenario roles | 4 fixed patients (`p10` confirms, `p17` reschedules, `p23` goes silent, `p24` cancels) | SYNTHETIC, deliberate | **Yes** — this is how a demo is made rehearsable |

**Two findings worth calling out:**

1. **A configuration surface already exists.** `VistaReglas.tsx` edits the five rules live, with validation (close > open, second < first). V2 does not start from zero on configuration — it extends a working pattern.
2. **The behaviour probabilities are the real scenario dial.** Being able to say *"run a clinic with a 40 % silence rate"* and then ask whether canonical can detect it is exactly the experiment M5.1 could not run for lack of data. The author labels these an assumption, not a measurement — and that honesty is what makes them safe to use as a dial.

**The prices are in cents on purpose** (`priceCents`), to avoid floating-point
drift — the same discipline canonical uses with `Numeric(12,2)`.

---

## 7 · DOCUMENTATION DRIFT — verified, and it is real

The contradiction the brief flagged is **confirmed at HEAD**.

**README claims** (still, at `b57f7bc`):

> *"Esta distinción importa, así que va primero. Toda la interfaz lleva la
> etiqueta visible **«Datos ficticios de demostración»**."*

**HEAD commit `b57f7bc` is literally titled** *"quitar etiquetas de 'datos
ficticios de demostración' de la UI"* and removes **14 lines across 3
components**, insertions: zero.

| Removed from | What went |
|---|---|
| `Bienvenida.tsx` | the bordered pill on the welcome screen |
| `Estacion.tsx` | the persistent header badge — **desktop and mobile variants** |
| `VistaActividad.tsx` | the caption under the activity feed |

**Current HEAD behaviour, measured not assumed.** The *always-visible* boundary
marker is **gone**. What survives is three scattered, view-specific mentions:

- `Bienvenida.tsx:41` — "Esta es una demostración con datos ficticios." — body text on the **pre-start** screen only, seen once and then never again.
- `VistaLaboratorios.tsx:133` — a caption on that one view.
- `VistaAgenda.tsx:233` — "reglas ficticias de demostración", inside a specific waitlist panel.

So the README's claim that the **whole** interface carries the label is now
**false**. Once you press "Iniciar demostración", you can use the agenda,
patients, doctors and operations centre with **no synthetic-data marker in
sight**.

**No judgement of intent.** Removing a demo watermark before a presentation is
an entirely ordinary thing to do, and the author may simply not have updated the
README. But the consequence is what matters: **screenshots taken from HEAD are
indistinguishable from screenshots of a real clinic.**

**Binding requirement for the canonical Synthetic Lab:** it must carry a
**visible, persistent, non-dismissible** synthetic-data boundary — present on
every view, not only before you start. Anything less and someone eventually
pastes a synthetic number into a real decision. This is the same rule already
recorded for the voice catalog in `odontoflow-voice/CANONICAL.md`, and the same
rule that keeps `DOMINANT_LEAKAGE = UNKNOWN` honest in M5.

---

## 8 · WHAT SHOULD STAY SIMULATION-ONLY

1. The replay engine and everything it knows about "what really happened".
2. Simulated patient decisions — the evaluator's answer key.
3. Simulated messaging (in-memory sends and inbound replies).
4. `localStorage` persistence — a lab convenience, never a system of record.
5. The synthetic seed itself: names, phones, prices, lab contacts. **They must never enter `patients`, `practitioners`, `services` or `products` as canonical rows.**
6. The behaviour probabilities, permanently labelled assumptions.

## 9 · WHAT SHOULD ENTER THE CANONICAL FRONTEND

Nothing yet — and when it does, as **a Synthetic Lab route behind a flag**,
exactly the pattern V1 established for voice (`VITE_ENABLE_VOICE` → an opt-in
route, mock-safe, no live calls unless explicitly enabled).

Candidates, in value order: the **operations-centre queue** (the strongest
product idea, and OdontoFlow has no equivalent), the **agenda-by-state board**,
the **timeline control**, and the **cancellation-impact view**. Each must be
reconciled with Leonardo's visual baseline rather than importing a second
design language wholesale.

## 10 · WHAT SHOULD ENTER THE CANONICAL BACKEND

**Nothing in V2.** Explicitly:

- **No new appointment states.** §5 is a map, not a migration.
- **No waitlist table** until the evaluator shows the recovery loop is worth persisting.
- **No lab tables** — a separate vertical, not this one.
- **No reminder scheduling.** That is real automation touching real patients; it does not belong in a measurement instrument.

The only backend work this activity even suggests is the **intent adapter**, and
it is deliberately unbuilt. Its first requirement is not code: the simulator
needs a **principal** (PF2/PF3) before it can be permitted to send a single
command.

## 11 · WHAT SHOULD NOT BE BUILT YET

| Not yet | Why |
|---|---|
| The intent adapter | Needs an intent vocabulary and a simulator principal first. |
| The evaluator | Needs the adapter to have something to compare. |
| Any database state change | Would bake in a vocabulary no measurement has justified. |
| Reminder automation | Real messages to real people. Out of scope, and the voice repo already owns the channel question. |
| Merging the two design languages | A design decision for the Owner and Leonardo, not a refactor. |
| Waitlist / lab persistence | Both are good ideas with no measured demand yet. |

---

## 12 · REVISED V2 IMPLEMENTATION ORDER

V2 was *"connect the voice alias vocabulary to an editable Synthetic Clinic
configuration."* That framing is now too small: **the Synthetic Clinic exists.**

Revised, each step independently valuable and abandonable. **None authorised yet.**

| # | Step | Why here | Risk |
|---|---|---|---|
| **0** | **Decide promotion** (§13) and the visual-language question. Owner decisions, no code. | Everything downstream sits in a repo that either exists or does not. | none |
| **1** | **Reinstate the persistent synthetic-data boundary** (§7) as the first change after promotion. | It is the smallest change with the largest downside if skipped, and the README already promises it. | none |
| **2** | **Turn the seed into a named Scenario Configuration** — extend the working rules screen to patients/doctors/appointments/waitlist and, above all, the **behaviour probabilities**. Keep the seed as the default scenario. | This *is* the original V2 goal, and it starts from a working pattern rather than zero. | low — simulation-side only |
| **3** | **Join the voice alias vocabulary to the scenario catalog** — the original V2 sentence, now a small step: both sides are synthetic catalogs of the same clinic. | Cheap once step 2 exists; closes the loop with V1. | low |
| **4** | **Define the intent vocabulary** — map simulator actions to canonical commands on paper, and give the simulator a principal. | The gate for every write. No code writes anything before this. | medium — touches PF2/PF3 |
| **5** | **Build the intent adapter** (read-only rehearsal first: log the intents it *would* send, send nothing). | Proves the mapping before any state moves. | medium |
| **6** | **Turn the adapter on** against a scratch database, never the pilot one. | First real writes, isolated. | high |
| **7** | **Build the evaluator** — compare ground truth against canonical observed state. | **The actual prize:** an instrument that can measure what M5.1 could not. | medium |
| **8** | **Run the no-show experiment**: a scenario with a known silence rate, and check whether canonical can detect it. | Turns M5.1's backlog item **I1** from an argument into a measurement. | low |
| **9** | Surface the operations-centre queue in the canonical frontend, behind a flag. | Highest-value UX idea, but it should follow the measurement, not precede it. | medium |

**Do not reorder 6 before 4.** And note what step 8 buys: the reason M5 stalled
was no real clinic data. A calibrated simulator does not replace that data — but
it *can* prove whether our instrumentation would have caught the problem if we
had it. That is a legitimate, cheap, and previously unavailable move.

---

## 13 · PROMOTION RECOMMENDATION

**Fan-in verdict: PASS.**

- Baseline **fully green** on the donor's own contract: typecheck clean, **98 tests passing** in 11 files, build passing, and the author's eight-step walkthrough finishing *"Recorrido completo sin fallos"*.
- The simulator is not merely valuable — it is **most of V2**, already built and tested.
- History is clean, authorship is intact, and there is no licence or dependency obstacle (React + Vite + Vitest, two runtime dependencies).

**Recommendation: promote the same git repository** — by moving it, never by
copying files — to `odontoflow-sim/`, with `origin` → `MiguelAAR10/odontoflow-sim`
and `alejandro` → `AlejandroMarceloCh/odontoflow`. Never rewrite history.

**Not performed in this activity.** Two reasons, and the second is the real one:

1. The brief authorises promotion only if the fan-in concludes PASS — which it does, but the conclusion and the act are separate steps by design.
2. **Repository visibility is an Owner decision, and publishing is irreversible.** The voice repo was created private for exactly this reason and that call is still open. Making the same choice twice unasked would be assuming a pattern rather than confirming one.

Also to settle before promotion: the repo's own name collides conceptually with
the product (`AlejandroMarceloCh/odontoflow` is a *simulator*, not the product),
which is precisely why `odontoflow-sim` is the right canonical name.

---

## 14 · What this map does not claim

- It does not claim the simulator is production software — its author lists the gaps himself (no auth, no persistence, desktop-only, no real messaging channel).
- It does not treat any donor data as real clinic evidence. **`DOMINANT_LEAKAGE` remains `UNKNOWN`**; a simulator is not a clinic.
- It does not authorise any step in §12, or the promotion in §13.
- It changed no product code and no donor file.
