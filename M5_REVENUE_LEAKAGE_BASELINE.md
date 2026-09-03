---
title: OdontoFlow — M5.1 Revenue Leakage Baseline Contract
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning) — classifications derived by read-only inspection of backend HEAD 23527c2 and the live schema at migration 0008
milestone: M5 — First Measured Value
---

# M5.1 — Revenue Leakage Measurability Baseline

**Purpose.** Establish, before any intervention, exactly which economic
transitions OdontoFlow can *prove* from committed data, which it can only
partially prove, and which it cannot prove at all. Nothing in this document
infers a business state the data cannot demonstrate.

**Method.** Read-only inspection of the domain at backend `23527c2`
(migration `0008`), plus the live PostgreSQL schema and row census in the
`odontoflow-db-1` container (port 5434). No code was written and no
migration was created.

---

## 1. The funnel and its authoritative tables

```
Lead ──(appointments.lead_id)──► Appointment ──(visits.appointment_id)──► Visit
                                                                            │
                                                        (service_executions.visit_id)
                                                                            ▼
Payment ◄──(payments.charge_id)── Charge ◄──(charges.service_execution_id)── ServiceExecution
```

| Stage | Table | Module | Own timestamps | Own state field |
|---|---|---|---|---|
| Lead | `leads` | `app/commercial/models.py` | `created_at` | `commercial_status` (inert — see §3.T2) |
| Appointment | `appointments` | `app/scheduling/models.py` | `created_at`, `start_utc`, `end_utc` | `state ∈ {confirmed, cancelled}` |
| Visit | `visits` | `app/clinical/models.py` | `started_at`, `created_at` | *none* |
| ServiceExecution | `service_executions` | `app/clinical/models.py` | `executed_at` | *none* |
| Charge | `charges` | `app/economics/models.py` | `created_at` | *none* (derived) |
| Payment | `payments` | `app/economics/models.py` | `paid_at` | *none* |
| Provenance | `audit_events` | `app/audit/models.py` | `occurred_at` | `action` + `before_state`/`after_state` JSONB |
| Command log | `command_receipts` | `app/idempotency/models.py` | `created_at` | `outcome_json` JSONB |

**Structural note that governs every join below.** Every child table carries
`organization_id` and reaches its parent through a *composite* tenant foreign
key (`(organization_id, parent_id)`). Therefore **every join in this document
must include `organization_id` on both sides.** A join on the bare id is not
merely sloppy here — it is the one way to produce a cross-tenant number.

**The provenance seam.** `audit_events` is the only place transition *history*
exists. It carries `occurred_at`, the acting principal, and full JSONB
before/after snapshots, and every state-changing command stages its audit row
*inside the same transaction* as the mutation (`app/audit/service.py`:
"an audit row lands exactly when — and only when — the state transition it
describes is committed"). This makes several otherwise-unmeasurable timings
recoverable. Two cautions: `audit_events.entity_id` is `String(100)`, so joins
to integer ids require an explicit cast; and audit is append-only history with
no retention policy declared — if it is ever pruned, these measures die with it.

---

## 2. Verified audit action vocabulary

Emitted today (grepped from `app/`, confirmed live in `odontoflow_e2e`):

`organization.created` · `patient.created` · `appointment.created` ·
`appointment.cancelled` · `appointment.rescheduled` · `visit.created` ·
`service_execution.created` · `service_consumption.created` ·
`charge.created` · `payment.created` · `product.created` ·
`inventory_entry.created` · `inventory_adjustment.created` ·
`inventory_transfer.created`

**Not emitted:** anything about a Lead. `app/commercial/service.py` contains no
`record_event` call — lead creation and lead reads are unaudited. Lead
`created_at` is the only lead timestamp in existence.

---

## 3. Transition-by-transition classification

### T1 · Lead created — **MEASURABLE**

- **Model/table:** `leads`
- **Join:** none required
- **Timestamps:** `leads.created_at`
- **State:** `acquisition_source ∈ {promotion, referral, direct}` (CHECK-constrained)
- **Formula:** `SELECT acquisition_source, date_trunc('day', created_at), count(*) FROM leads WHERE organization_id = :org GROUP BY 1,2`
- **Ambiguity:** none. Demand *arrival* is well instrumented.
- **Missing:** nothing.

### T2 · Lead → Appointment (conversion) — **PARTIALLY_MEASURABLE**

- **Model/table:** `appointments.lead_id` → `leads.id` (NOT NULL — every appointment has a lead)
- **Exact join:**
  ```sql
  FROM leads l
  LEFT JOIN appointments a
    ON a.organization_id = l.organization_id
   AND a.lead_id         = l.id
  ```
- **Timestamps:** `l.created_at` (arrival), `a.created_at` (booking instant)
- **Usable state:** existence of `a` — nothing else
- **Formula (booked rate):**
  `count(DISTINCT l.id) FILTER (WHERE a.id IS NOT NULL) / count(DISTINCT l.id)`
  **Formula (time to book):** `a.created_at - l.created_at`, first appointment per lead
- **Ambiguity — the significant one.** `leads.commercial_status` is a
  `varchar(30)` defaulted to `'new'` with **no CHECK constraint and no
  transition code anywhere**. `app/commercial/service.py` only ever *filters*
  on it; nothing ever writes a different value. The design handoff of
  2026-08-13 states this explicitly: *"No state machine invented (spec defers
  exact progression to a later vertical)."* Verified live: every lead row in
  the workspace reads `new`. Consequently a lead with no appointment is
  indistinguishable between *still being worked*, *unreachable*, *disqualified*,
  *price-lost*, and *duplicate entry*.
- **Second ambiguity.** There is **no identity bridge between `Lead` and
  `Patient`** — no `patient_id` on leads, no `lead_id` on patients (verified by
  grep across `app/`). So "the lead became a paying patient" is not expressible.
  Conversion can only ever mean "this lead was booked at least once", and a
  walk-in visit can never be attributed back to any lead or acquisition source.
- **Minimum missing instrumentation:** a lead outcome — either a real
  `commercial_status` transition with a `status_changed_at`, or (cheaper) a
  `lead.status_changed` audit action. Separately, a `lead_id` on `patients`
  would close acquisition→revenue attribution.

### T3 · Appointment → cancelled — **MEASURABLE** (state) / **PARTIALLY** (circumstance)

- **Model/table:** `appointments.state`, CHECK-constrained to `('confirmed','cancelled')`
- **Timestamps:** `appointments` has **no `cancelled_at` column**. The instant is
  recoverable from audit:
  ```sql
  FROM appointments a
  LEFT JOIN audit_events e
    ON e.organization_id = a.organization_id
   AND e.entity_type     = 'appointment'
   AND e.entity_id       = a.id::text     -- entity_id is varchar(100)
   AND e.action          = 'appointment.cancelled'
  ```
- **Usable state:** `cancelled` is **terminal and provable**. `_require_confirmed()`
  in `app/scheduling/service.py` rejects any transition out of a non-confirmed
  appointment, so there is no cancel→reinstate path and no double-cancel.
- **Formulas:**
  - cancellation rate = `count(*) FILTER (WHERE a.state='cancelled') / count(*)`
  - **cancellation lead time** = `a.start_utc - e.occurred_at` (negative ⇒ cancelled after the slot had passed)
  - late-cancellation bucket = lead time `< 24h`
- **Ambiguity:** no cancellation **reason** and no **initiating party**. `audit_events.actor_id`
  is the API principal (the staff member or system that executed the command),
  which is *not* who decided to cancel. Patient-initiated and clinic-initiated
  cancellations are indistinguishable — and they are economically opposite.
- **Minimum missing instrumentation:** a reason + initiating party on the cancel
  command, carried into the audit `after_state`. **No migration needed** — the
  JSONB column already exists.

### T3b · Appointment rescheduled (churn) — **PARTIALLY_MEASURABLE**

- **Model/table:** `appointments` (mutated **in place**)
- Reschedule updates the *same row*: per `app/scheduling/service.py`, *"there
  is no new appointment, no temporary cancellation and therefore no visible
  old-cancelled + new-confirmed transition."* The table therefore retains
  **only the final interval**.
- **Recovery is audit-only:** `action = 'appointment.rescheduled'`, with
  `before_state`/`after_state` each carrying `start_utc`/`end_utc`. Verified
  live in `odontoflow_e2e` (event id 15: `14:00 → 14:45`).
- **Formulas:** reschedules per appointment = count of those events;
  originally-booked interval = the `appointment.created` event's
  `after_state->>'start_utc'`; churn days = `(final start_utc) - (original start_utc)`.
- **Ambiguity:** no reason, no initiating party (same gap as T3). And the
  entire history is audit-dependent.
- **Minimum missing instrumentation:** same reason/party field as T3.

### T4 · Appointment → Visit (attendance) — **PARTIALLY_MEASURABLE**

> This is the weakest link in the funnel, and it sits exactly where the largest
> suspected leakage lives.

- **Exact join:**
  ```sql
  FROM appointments a
  LEFT JOIN visits v
    ON v.organization_id = a.organization_id
   AND v.appointment_id  = a.id
  ```
- **Timestamps:** `a.start_utc` (scheduled), `v.started_at` (server-owned
  attendance instant — never client-supplied)
- **Usable state:** existence of `v`. Nothing else.
- **What IS provable:**
  - **Attendance** (positive direction): `v.id IS NOT NULL` ⇒ the patient attended. Sound.
  - **Punctuality:** `v.started_at - a.start_utc`.
  - **Realization integrity:** `create_visit` validates that the originating
    appointment is `confirmed`, so a cancelled appointment can never carry a
    visit. The two sets are clean.
- **What is NOT provable — the core finding.** The absence of a visit row on a
  past confirmed appointment has at least three causes that the data cannot
  separate:
  1. the patient did not show up (**no-show** — real leakage);
  2. the patient attended but staff never recorded the visit (**data-entry gap** — no leakage, pure measurement error);
  3. the appointment simply has not been resolved yet (**unresolved** — clinic closed, still pending).
  There is **no no-show state anywhere in the system** (verified: no
  `no_show` / `noshow` / `inasistencia` token in `app/`, `alembic/`, or
  `docs/api/`), and `appointments.state` has **no terminal "completed" or
  "resolved" value** — a confirmed appointment from two weeks ago still reads
  `confirmed` forever. Absence of evidence is therefore not evidence of a
  no-show, and any no-show rate computed today would be a fabrication.
- **Structural caution:** there is **no UNIQUE constraint on
  `visits.appointment_id`** (confirmed against the live schema). Two visits may
  legally point at one appointment. Every per-appointment aggregation must use
  `EXISTS` / `count(DISTINCT a.id)` — never `count(v.id)`, which would silently
  over-count attendance.
- **Minimum missing instrumentation:** an **appointment resolution** —
  `attended | no_show | cancelled`, with `resolved_at` and the resolving actor.
  This is the single highest-value missing field in the entire domain.

### T5 · Visit → ServiceExecution — **MEASURABLE**

- **Exact join:**
  ```sql
  FROM visits v
  LEFT JOIN service_executions se
    ON se.organization_id = v.organization_id
   AND se.visit_id        = v.id
  ```
- **Timestamps:** `v.started_at`, `se.executed_at`
- **Formula (visit with no execution):** `NOT EXISTS (SELECT 1 FROM service_executions se WHERE se.organization_id = v.organization_id AND se.visit_id = v.id)`
- **Ambiguity:** structurally exact, semantically open — a visit with no
  execution may be a legitimate free consultation *or* an unrecorded procedure.
  Only a clinic rule can settle which; the data cannot.
- **Related gap:** `visits` has **no `ended_at`**. Chair-time, visit duration,
  and every capacity/productivity leakage measure are therefore
  **NOT_MEASURABLE**. Out of scope for M5.1; recorded here so it is not
  rediscovered later.

### T6 · ServiceExecution → Charge — **MEASURABLE**

- **Exact join:**
  ```sql
  FROM service_executions se
  LEFT JOIN charges c
    ON c.organization_id      = se.organization_id
   AND c.service_execution_id = se.id
  ```
- **Cardinality is guaranteed 1:1** by `uq_charges_org_execution`. This makes
  `c.id IS NULL` an **unambiguous, provable** "service performed but never
  charged" — no interpretation required.
- **Timestamps:** `se.executed_at`, `c.created_at`
- **Formulas:**
  - **unbilled value** = `SUM(se.executed_price) WHERE c.id IS NULL`
  - **billing lag** = `c.created_at - se.executed_at`
  - **under-charge value** = `SUM(se.executed_price - c.amount) WHERE c.id IS NOT NULL AND c.amount < se.executed_price`
- **Ambiguity:** `charges.amount` defaults to the execution's price snapshot but
  is a separate column and may legitimately differ. An *intentional discount*
  and a *mis-keyed amount* are indistinguishable (no discount reason field).
  The aggregate is exact; its attribution is not.
- **Minimum missing instrumentation:** none for the headline number. A discount
  reason would split intentional from accidental.

### T7 · Charge → Payment (collection) — **MEASURABLE**

> The strongest measurement surface in the domain. Exact, unambiguous, no new
> instrumentation required.

- **Exact join:**
  ```sql
  FROM charges c
  LEFT JOIN payments p
    ON p.organization_id = c.organization_id
   AND p.charge_id       = c.id
  ```
- **Timestamps:** `c.created_at`, `p.paid_at`
- **Formulas** (outstanding is derived by contract, never stored):
  - `paid(c)        = COALESCE(SUM(p.amount), 0)`
  - `outstanding(c) = c.amount - paid(c)`
  - `unpaid  ⇔ paid = 0`
  - `partial ⇔ 0 < paid < c.amount`
  - `full    ⇔ paid = c.amount`
  - `aging          = now() - c.created_at`
  - `days_to_collect = MAX(p.paid_at) - c.created_at` (fully-paid charges only)
- **Invariant, not assumption:** `paid ≤ amount` always holds. The application
  serializes payments per charge with a row lock and rejects overpayment
  deterministically (`INVALID_INPUT`); `CHECK (amount > 0)` on both tables
  forbids negative entries. So the three payment states are exhaustive and
  mutually exclusive.
- **Ambiguity:** there is **no reversal, refund, or write-off model**. Payments
  are append-only ("reversal, never delete" is stated as contract, but no
  reversal row type exists). An uncollectible charge therefore stays
  "outstanding" indefinitely and cannot be distinguished from a genuinely
  pending one. This inflates aged receivables over time.
- **Minimum missing instrumentation:** a charge write-off / bad-debt marker.
  Not needed for a first 90-day baseline; needed before receivables are
  reported as a standing KPI.

### T8 · Outstanding money (portfolio) — **MEASURABLE**

- **Join chain:** `payments → charges → service_executions → visits → locations`
  (and `→ practitioners`, `→ services`), every hop tenant-qualified.
- **Formula:** `SUM(c.amount - COALESCE(paid, 0))` sliced by location,
  practitioner, service, and age bucket.
- **Ambiguity:** only the write-off gap above.

---

## 4. Required distinguishability — verdict table

| Question | Verdict | Basis |
|---|---|---|
| Lead still open vs abandoned | **NOT_MEASURABLE** | `commercial_status` frozen at `'new'`; no transition code; no lead audit event; no lost/disqualified marker |
| Lead converted vs not converted | **PARTIALLY_MEASURABLE** | "ever booked" provable via `appointments.lead_id`; "became a paying patient" impossible — no Lead↔Patient bridge |
| Appointment cancelled | **MEASURABLE** | `state='cancelled'`, CHECK-constrained, terminal; instant via `audit_events`; **reason and initiating party NOT_MEASURABLE** |
| Appointment without visit | **MEASURABLE (as a set)** | `LEFT JOIN visits … IS NULL` — but see next row for what the set *means* |
| No-show vs unresolved | **NOT_MEASURABLE** | no no-show state, no appointment resolution state, no terminal "completed"; no-show / data-entry gap / still-pending are one indistinguishable set |
| Visit without execution | **MEASURABLE** (structurally) | `NOT EXISTS` on `service_executions`; business meaning needs a clinic rule |
| Execution without charge | **MEASURABLE** | 1:1 enforced by `uq_charges_org_execution`; `c.id IS NULL` is unambiguous |
| Unpaid / partial / full charge | **MEASURABLE** | derived from `SUM(payments.amount)` vs `charges.amount`; overpayment structurally excluded |
| Outstanding money | **MEASURABLE** | exact, derivable, sliceable by location/practitioner/service/age |

**The pattern.** Instrumentation quality *increases* monotonically down the
funnel. Money is exactly measurable; demand and attendance are not. OdontoFlow
can today prove what it *failed to collect*, but not what it *never got the
chance to earn*.

---

## 5. Data availability — real data check

Live census taken 2026-09-02 from container `odontoflow-db-1` (PostgreSQL 15,
`127.0.0.1:5434`):

| Database | Migration | Contents | Classification |
|---|---|---|---|
| `odontoflow_e2e` | `0008` | 1 lead · 2 appointments · 2 patients · 1 visit · 1 execution · 1 charge · 2 payments · 1 consumption · 16 audit events · 12 command receipts | **TEST/FIXTURE DATA** |
| `odontoflow` (dev) | `0001` | 10 tables, **0 leads**, no clinical/economic tables at all | EMPTY |
| `odontoflow_test_*` (≈40 databases) | per-run | pytest scaffolding, dropped/recreated per run | TEST/FIXTURE DATA |
| `odontoflow-frontend/db/seeds/001_simulated.sql` | n/a | "Sede Simulada Aurora", "Paciente Alfa Ficticio", phones in the reserved fictional `555-01xx` range; file header declares *"solo contiene identidades inventadas"* | **SYNTHETIC DATA** |

Provenance of the `odontoflow_e2e` rows is unambiguous: the lead is literally
named `Lead E2E Piloto`, the patients `Paciente E2E Piloto` / `Paciente E2E`,
the organization `Bootstrap Clinic`, all inserted 2026-08-17T16:55:32Z within a
43-second window by `.audit/accelerator/seed_e2e.py` — the M4.4 pilot harness.

### Verdict

**REAL_CLINIC_DATA = NONE.** No database, export, spreadsheet, or dump anywhere
in the canonical workspace contains operational data from an actual clinic.

**DOMINANT_LEAKAGE = UNKNOWN.**

Any leakage figure computed from what is currently on disk would describe the
behaviour of a test fixture, not of a business. It is stated here so that no
later reader mistakes the M4.4 harness numbers for a baseline.

---

## 6. Minimum clinic data sample required

To compute a defensible Revenue Leakage Baseline we need the clinic's own
operating history — **not** OdontoFlow data, and it does not need to be
migrated into OdontoFlow first. A CSV/Excel export from whatever the clinic
uses today (including a transcribed paper agenda) is sufficient.

**Window:** 90 consecutive days, closed and settled (i.e. ending at least 30
days ago, so the collection cycle on those charges has had time to complete).

**Scope:** one location minimum; two if the multi-branch question matters to
the first decision.

**Volume floor:** **≥ 300 appointments** and **≥ 200 charges** in the window.
Rationale: the headline candidate is a rate (no-show %, uncollected %). Below
roughly 300 appointments the confidence interval on a rate near 15–25% is wide
enough (±5 pp or worse) that it cannot distinguish a real problem from noise,
and an intervention sized against it would be unjustified.

**Required fields:**

| Dataset | Fields |
|---|---|
| Appointments | scheduled datetime, service, practitioner, location, booking datetime, current status **as the clinic records it**, and — critically — **whether the patient showed up** |
| Cancellations | date/time the cancellation was communicated, **who cancelled** (patient or clinic), reason if the clinic captures one |
| Visits | date, patient reference, services actually performed, practitioner, location |
| Charges / invoices | amount, issue date, linked service |
| Payments | amount, date, method, linked charge |
| Tariff | current service price list |

**Privacy:** direct identifiers are **not required**. A stable pseudonymous
patient reference (`P001`, `P002`, …) is enough for every measure in this
document. Request the export without names, DNI, phones, or email.

**Also request (5 minutes of conversation, not data):** which of these the
clinic *believes* is its biggest money loss. Their prior is not evidence, but
it tells us which measure to compute first and where a disagreement between
belief and data would be most valuable.

---

## 7. Candidate leakages

Ranked by (prior likelihood × economic size), with today's measurability
stated separately — the two do not correlate, and that tension is the whole
content of M5.1.

| # | Candidate | Prior | Measurable **today** | Formula (once data exists) |
|---|---|---|---|---|
| 1 | **No-show / unattended confirmed appointments** — lost chair time | High | **NO** | `count(a) WHERE state='confirmed' AND start_utc < now() AND NOT EXISTS(visit)` × average service price — **blocked: the set conflates no-show with data-entry gap** |
| 2 | **Late cancellations not refilled** | Medium-high | **PARTIAL** | cancels with `start_utc - occurred_at < 24h`, minus those whose freed interval was rebooked (derivable from other appointments in the interval) |
| 3 | **Performed but never charged** | Medium | **YES — exact** | `SUM(se.executed_price) WHERE charge IS NULL` |
| 4 | **Charged below executed price** (discount / keying) | Medium | **YES — exact** | `SUM(se.executed_price - c.amount) WHERE c.amount < se.executed_price` |
| 5 | **Uncollected receivables** (aged outstanding) | Medium | **YES — exact** | `SUM(c.amount - paid)` by age bucket |
| 6 | **Leads that never book** | Unknown | **SET only** | `count(l) WHERE NOT EXISTS(appointment)` — no outcome state, so the set is uninterpretable as loss |
| 7 | **Chair-time / capacity underuse** | Unknown | **NO** | blocked: no `visits.ended_at` |

**The asymmetry worth stating plainly:** candidates 3, 4 and 5 can be proven
today with zero new code. Candidates 1 and 2 are the ones most likely to be
large. M5 must not quietly substitute the measurable for the important — it
must measure 3/4/5 *now* and instrument 1 *deliberately*.

---

## 8. Confidence

| Claim | Confidence | Basis |
|---|---|---|
| Funnel joins and cardinalities as documented | **High** | read from models, migrations, **and** the live `information_schema` / `\d` output |
| Money-side measures (T6, T7, T8) are exact | **High** | uniqueness and CHECK constraints verified in the live schema; overpayment rejection verified in `app/economics/service.py` |
| Cancellation instant recoverable from audit | **High** | verified live — `appointment.cancelled` and `appointment.rescheduled` events present with full before/after JSONB in `odontoflow_e2e` |
| No-show is not measurable | **High** | exhaustive token search across `app/`, `alembic/`, `docs/api/` returned nothing; `state` CHECK admits only two values |
| Lead status is inert | **High** | no writer exists in code; every live row reads `'new'`; the 2026-08-13 handoff documents the deferral by design |
| No real clinic data exists | **High** | full workspace file sweep + live row census in every database on the instance |
| Which leakage dominates | **NONE — UNKNOWN** | no real data; not estimated, not guessed |

---

## 9. Minimum instrumentation backlog

Ordered smallest-first. Only **I1** is on the M5 critical path.

| # | Instrumentation | Unblocks | Migration? | Priority |
|---|---|---|---|---|
| **I1** | **Appointment resolution**: `attended \| no_show \| cancelled` + `resolved_at` + resolving actor. Cheapest honest form: a new `appointment.no_show` command emitting a new audit action — `audit_events` already carries action, timestamp, actor and JSONB, so **no schema change is required**. | Candidate 1 (no-show), and the denominator for candidate 2 | **No** (audit-only form) | **Critical** |
| I2 | Cancellation **reason + initiating party**, carried into the cancel command and stored in the audit `after_state` | Splits patient-driven from clinic-driven cancellation | **No** | High |
| I3 | Real `commercial_status` transitions (`new → contacted → booked → lost`) + `lead.status_changed` audit action | Candidate 6; lead open-vs-abandoned | No (audit form) / small (column form) | Medium |
| I4 | `lead_id` on `patients` | Acquisition-source → revenue attribution | Yes | Medium |
| I5 | `visits.ended_at` | Candidate 7 (chair time) | Yes | Low |
| I6 | Charge write-off / bad-debt marker | Separates uncollectible from pending in aged receivables | Yes | Low |

---

## 10. Code required?

**Not for the first baseline.** Candidates 3, 4 and 5 — the entire measurable
money surface — are computable from existing domain state with read-only SQL.
No endpoint, no migration, no application change.

**Yes, eventually, for the no-show measurement, and only for that.** This meets
the bar of "a genuinely necessary measurement that cannot be obtained from
existing domain state": the absence of a visit row is *provably* ambiguous, and
no query over current data can disambiguate it. That work (I1) should be
authorized only once real clinic data confirms that unattended appointments are
in fact material — measuring first, instrumenting second.

**CODE_REQUIRED (M5.1) = NO.**
**CODE_REQUIRED (M5.2, conditional on real data) = YES — I1 only.**

---

## 11. Recommended next experiment — exactly one

Evidence does **not** permit an intervention experiment: with no real data,
there is nothing to intervene on and no baseline to measure against. Evidence
**does** permit exactly one *measurement* experiment.

> ### EXPERIMENT M5.1-E1 — Revenue Leakage Baseline Extract
>
> **Hypothesis.** The clinic's measurable economic leakage (unbilled
> executions + under-charged executions + aged receivables) is materially
> greater than zero and concentrated in one of those three buckets.
>
> **Input.** The 90-day clinic export specified in §6, loaded into a scratch
> database. Nothing is written to the product databases.
>
> **Method.** A read-only SQL query pack — seven queries, one per measurable
> transition (T1, T2, T3, T5, T6, T7, T8) — using the exact joins in §3. No
> application code, no migration, no intervention.
>
> **Outputs.**
> 1. Funnel volumes and conversion rates at each measurable stage.
> 2. Unbilled value (candidate 3), in currency.
> 3. Under-charge value (candidate 4), in currency.
> 4. Aged outstanding (candidate 5), in currency, by bucket.
> 5. Cancellation rate and lead-time distribution (candidate 2, partial).
> 6. An explicit **UNMEASURED** line for no-show, stating the size of the
>    ambiguous set (past confirmed appointments with no visit) **without**
>    calling any part of it a no-show.
>
> **Success criterion.** One leakage bucket is at least 2× the next largest.
> That bucket becomes M5.2's intervention target. If no bucket dominates, or if
> the ambiguous no-show set is larger than every measurable bucket combined,
> then M5.2 is **I1 (no-show instrumentation)** rather than an intervention —
> and that is a legitimate, informative outcome, not a failure.
>
> **Explicitly out of scope.** Any intervention, any reminder/recall feature,
> any backend change, any UI change.

---

## 12. What this document does *not* claim

- It does not claim a no-show rate. None is computable.
- It does not claim which leakage dominates. `DOMINANT_LEAKAGE = UNKNOWN`.
- It does not treat the M4.4 pilot fixtures or the frontend simulated seeds as
  business evidence.
- It does not propose an intervention.
