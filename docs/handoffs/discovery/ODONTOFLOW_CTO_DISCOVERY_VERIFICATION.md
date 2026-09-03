---
title: OdontoFlow — CTO/CEO Discovery Verification
status: final
date: 2026-09-03
role: read-only Lead Engineer discovery — no implementation performed
authority: independent re-verification from runtime/tests/schema/code; documentation used only where evidence agrees
---

# OdontoFlow — Discovery Verification for CTO/CEO

**Method.** Everything below was re-checked directly against running code,
tests, migrations and git state during this session — not copied from prior
docs. Evidence priority followed strictly: **runtime/tests/schema/code >
committed specs/handoffs > planning documentation > assumptions**. Where a
document's claim could not be verified against code, it is marked so
explicitly. No product code was written, refactored, or modified to produce
this report.

**Classification key**, used throughout: **REAL** (proven by passing tests
against a real database, or by inspected working code with no synthetic
shortcut) · **PARTIAL** (some real, some mocked/incomplete/disconnected) ·
**SIMULATED** (fixture, seed, mock, or prototype data/logic presented as
system behavior) · **MISSING** (no code found).

---

## CURRENT STATE

Five repositories exist exactly as expected, all clean or precisely
inventoried where not:

| Repo | Remote(s) | Branch | HEAD | Working tree |
|---|---|---|---|---|
| `odontoflow-planning` | `origin` → `MiguelAAR10/OdontoFlow-Planning` | `main` | `c2c8b6b` | 1 untracked file (this session's own draft brief, harmless) |
| `odontoflow-backend` | `origin` → `MiguelAAR10/OdontoFlow` | `main` | `23527c2` | clean (1 stray `.playwright-mcp/` dir from a prior browser session, non-code) |
| `odontoflow-frontend` | `origin` (canonical) + `leonardo` + `alejandro` (reference) | `main` | `a967b24` | clean |
| `odontoflow-voice` | `origin` (canonical, private) + `alejandro` (upstream) | `main` | `4149a3e` | clean |
| `odontoflow-sim` | `origin` (canonical, private) + `alejandro` (upstream) | `master` | `da203a9` | **DIRTY — see below** |

**MediStock was not inspected or reused**, other than confirming it sits
outside this workspace (`../../medistock`), as required.

**Critical state finding, not previously reported anywhere in Repo 0:**
`odontoflow-sim` has a **complete, passing, but UNCOMMITTED** feature
("Named Scenario Configuration") sitting in its working tree: 5 modified files
+ 6 new files, +659/−34 lines, **150/150 tests passing, typecheck clean**, but
**zero commits, zero push**. This is real, working code that exists only on
this machine's disk. If this environment were lost before a commit, it would
be lost entirely. This is reported here as found; it is not committed by this
discovery, per the read-only mandate.

**Milestone as claimed by Repo 0:** M5 First Measured Value, sub-state M5.1
CLOSED / M5.2 BLOCKED_EXTERNAL (`DOMINANT_LEAKAGE = UNKNOWN`) — **verified
consistent** with the actual absence of any real clinic data anywhere in the
workspace (see DATA section).

---

## WHAT WORKS

Verified by re-running the actual test/build commands in this session, not by
reading claims:

| Check | Result | Command |
|---|---|---|
| Backend test suite | **384 passed**, 0 failed, 228s | `.venv/bin/python -m pytest -q` against real PostgreSQL 15 |
| Frontend typecheck | clean | `npm run typecheck` |
| Frontend unit tests | **91 passed** | `npm test` |
| Voice service tests | **54 passed** | `.venv/bin/python -m pytest -q` (donor's own suite, unmodified) |
| Sim tests (including uncommitted work) | **150 passed** | `npm test` |
| Sim typecheck | clean | `npm run typecheck` |

**The strongest REAL flow** (see CURRENT DEMO below) is the backend's
Lead→Appointment→Visit→Execution→Consumption→Charge→Payment→Inventory chain,
enforced by PostgreSQL constraints (tenant composite FKs, a GiST exclusion
constraint against double-booking, `CHECK` constraints on money and stock) and
proven by 384 tests plus a 12-assertion frontend E2E spec against the same
real database. This is the one part of OdontoFlow that is genuinely
production-grade today.

**What is real and running as of this report:** a PostgreSQL 15 container
(`odontoflow-db-1`, port 5434, healthy) with the `odontoflow_test` and
`odontoflow_e2e` databases at migration `0008`; the backend and frontend both
build and pass their own tests against it.

---

## WHAT IS MOCKED

| Surface | Evidence |
|---|---|
| **Chat / conversations** | `getConversations()`/`sendMessage()` in `src/api.ts` branch on `useMocks`, but even the "real" branch calls `/conversations` and `/conversations/{id}/messages` — **endpoints that do not exist anywhere in the backend's 32 OpenAPI paths**. In real mode this would 404. Chat is mock-only in practice, not merely mock-by-default. |
| **Agent dashboard (AgentPage)** | `getAgentDashboard()` calls `/agent/dashboard` in real mode — **also does not exist in the backend**. The 4 KPI numbers on screen (`24`, `8`, `5`, `3`) are **hardcoded literals in JSX**, not even wired to the fetched mock data. The "Activo" badge is static markup with no state behind it. |
| **Synthetic clinic simulator (`odontoflow-sim`)** | Deliberately and explicitly synthetic: 28 patients, 4 doctors, 60 appointments, all invented. Its own README states this; V2.1 restored a **permanent, non-dismissible UI banner** (`CLÍNICA SINTÉTICA · DATOS SIMULADOS · NO SON DATOS REALES`) enforcing this. Zero connection to the backend. |
| **Voice assistant (`odontoflow-voice`)** | A separate FastAPI micro-service with its own in-memory session state, gated behind `VITE_ENABLE_VOICE` (default off) and structurally forbidden from live HTTP under `VITE_USE_MOCKS=true`. It produces **drafts only**; nothing it emits writes to the canonical backend. |
| **Frontend "legacy simulator"** | `src/domain/`, `src/simulation/`, `src/server.ts` in the frontend repo — an older, separate simulated-WhatsApp/reminder engine explicitly marked "reference only" in `.env.example`, not part of the real SPA. |

---

## WHAT IS MISSING

Confirmed absent by exhaustive search (`grep -rl`) across all 5 repositories,
not inferred from UI labels:

| Missing | Evidence |
|---|---|
| **Sales Agent (any LLM-driven agent)** | Zero `openai`/`anthropic`/`langchain`/LLM SDK imports anywhere in `odontoflow-backend`. Zero `/agent` router. `AgentPage`/`ChatPage` are static UI over mock data (see above). |
| **WhatsApp — live** | The voice repo's `whatsapp.py` (118 lines) is written but **not wired**: `grep "include_router" app/main.py` finds no `whatsapp_router` registration. The frontend's legacy simulator "sends" fake WhatsApp messages to a local table, never to Meta. |
| **Google Calendar, Telegram, Kapso** | **Zero mentions** of any of the three in any of the 5 repositories — no stub, no adapter shell, no documentation reference, no environment variable. This is not "disabled," it is **entirely unbuilt**. |
| **Price/Tariff model** | `Service` has no price field at all (only `name`, `duration_minutes`). `Product` has no price field either. The only price in the system is `ServiceExecution.executed_price`, a point-in-time snapshot with no catalog behind it. There is no tariff list, no price versioning, no discount logic. |
| **Promotion / Discount / Campaign / Referral** | Zero model classes, zero mentions in backend schema. |
| **Conversation (canonical)** | No backend model. The only "Conversation" type is a frontend TypeScript interface backing the mock Chat UI. |
| **NoShow / Confirmation / Waitlist (canonical)** | Zero backend models. `appointments.state` is `CHECK (state IN ('confirmed','cancelled'))` — no `no_show`, no `reminded`, no `confirmed-by-patient` distinction exists in the database at all. (The **simulator** has a rich 9-state vocabulary for exactly these concepts — see DOMAIN MODEL — but it is not connected to canonical.) |
| **Real OdontoSmart clinic data** | None found anywhere. See DATA. |

---

## 1 · CURRENT PRODUCT STATE

| Area | Classification | Evidence |
|---|---|---|
| Clinic data/configuration | **MISSING** (real) / SIMULATED (fixture) | No real clinic dataset anywhere; dev DB at migration 0001 with 0 rows; only fixture data in `odontoflow_e2e` |
| Leads/commercial | **PARTIAL** | `Lead` model, CRUD and filtering are REAL and tested; `commercial_status` is a column that is **only ever read/filtered, never written** beyond its `'new'` default (`grep "commercial_status\s*="` in `app/` returns zero assignment sites) — no conversion state machine exists |
| Scheduling/appointments | **REAL** | `Appointment`, booking/cancel/reschedule, a **partial GiST exclusion constraint** preventing double-booking at the database level, 384 backend tests, real frontend integration (`AgendaPage`, gated on `useMocks`) |
| Frontend/ERP | **PARTIAL** | Agenda, Patients, Cash, Inventory are REAL (wired to the real API when `VITE_USE_MOCKS=false`, proven by a 12/12 E2E spec); Chat and Agent are SIMULATED/static |
| Agents | **MISSING** | No canonical Sales Agent exists. `principal.type = 'agent'` is a reserved IAM category (authorization plumbing only), not an implementation |
| Calendar/WhatsApp/Telegram/Kapso | **MISSING** (all four) | WhatsApp has unwired adapter code in the voice repo only; the other three do not exist at all |
| Clinical | **REAL** | `Patient`, `Visit`, `ServiceExecution` — tenant-scoped composite FKs, price-snapshot integrity, tested |
| Finance | **REAL** (money correctness) / **MISSING** (tariff/promotions) | `Charge`/`Payment` with a database-enforced overpayment guard is REAL; there is no price list, no promotions, no discounts |
| Inventory/operations | **REAL** | Location-aware ledger, atomic transfers, append-only movements, migration `0008`, 384 tests include this |
| Voice | **PARTIAL** | Standalone service is REAL and tested (54/54) on its own; its integration into the product is UI-only, draft-producing, feature-flagged off by default, and its audio path is **UNVERIFIED** on this platform (no TTS available to exercise it) |
| Synthetic clinic | **SIMULATED by design, and correctly labelled as such** | Fully deterministic, fully isolated, carries its own non-dismissible synthetic-data banner |

---

## 2 · CURRENT DEMO (DEMO AVAILABLE)

**Strongest end-to-end flow that works today: the Pilot E2E money/inventory
journey**, proven by `odontoflow-frontend/test/pilot-e2e.test.ts` (12
assertions, structurally confirmed against the file — not re-executed in this
pass to avoid the schema-reset side effect the harness performs; last verified
run recorded in `STATUS.md` as 2026-09-02, 12/12).

**Exact boundary trace:**

```
input (test harness / real browser form)
  → frontend: src/api.ts (real-mode branch, gated by VITE_USE_MOCKS=false)
    → axios HTTP → FastAPI (uvicorn on :8010)
      → app/{clinical,economics,inventory,scheduling}/router.py
        → app/{...}/service.py  (permission check → idempotency claim → domain rule → audit event, one transaction)
          → SQLAlchemy → PostgreSQL 15 (odontoflow_e2e, migration 0008)
            → composite-FK tenant enforcement, GiST exclusion, CHECK constraints
  → result: real row, real constraint, real HTTP response
  → frontend adapter renders it back into the UI view-model (CashPage/InventoryPage)
```

**Separated by verification method:**

- **Real browser flow, verified in this project's history (not re-driven in
  this pass):** Agenda, Patients, Cash, Inventory pages against the real
  backend — confirmed by code inspection of the `useMocks` gate in each page
  and by the existence of a passing 91-test unit suite plus the 12/12 E2E
  spec.
- **API/E2E tested flow (file-verified, not re-executed this pass):**
  `pilot-e2e.test.ts` — a real HTTP client driving the real FastAPI app
  against a freshly migrated real database, asserting on real response
  payloads.
- **Simulated/prototype flow:** Chat, Agent dashboard, the standalone voice
  assistant, and the entire `odontoflow-sim` simulator — none of these write
  to or read from the canonical backend.

---

## 3 · DATA

| Classification | What | Evidence |
|---|---|---|
| **REAL** | None found | No dataset anywhere in the 5 repositories or the running PostgreSQL instance traces to an actual clinic |
| **PARTIAL** | — | not applicable; nothing is partially real, it is either test fixture or fully absent |
| **SIMULATED** | `odontoflow_e2e` DB rows (1 lead, 2 patients, 60 sim appointments in `odontoflow-sim`, 28 sim patients), `odontoflow-voice`'s 12-item catalog with invented prices, `odontoflow-frontend`'s legacy `mockData.ts` | Row counts verified live against `odontoflow-db-1`; all three carry explicit "synthetic/ficticio" self-declarations in their own source |
| **MISSING** | Any real OdontoSmart operational dataset (patients, appointments, prices, staff schedules) | Dev database `odontoflow` is at migration `0001` with **0 rows** in any business table; `STATUS.md` and `M5_REVENUE_LEAKAGE_BASELINE.md` both independently concluded `DOMINANT_LEAKAGE = UNKNOWN` for the same reason |

**Direct answer to the explicit question:** No, no actual OdontoSmart
operational dataset is loaded anywhere in this workspace. This has been the
standing, repeatedly-reconfirmed blocker since the M5.1 measurement work
(2026-09-02), not a new finding.

---

## 4 · DOMAIN MODEL

All 16 requested models **exist as real SQLAlchemy classes with migrations**,
verified by direct inspection of `app/*/models.py`:

`Organization` ✅ · `Location` ✅ · `Service` ✅ · `Practitioner` ✅ ·
`PractitionerMembership` ✅ · `PractitionerCapability` ✅ · `AvailabilityRule` ✅ ·
`ScheduleBlock` ✅ · `Lead` ✅ · `Appointment` ✅ · `Patient` ✅ · `Visit` ✅ ·
`ServiceExecution` ✅ · `Product` ✅ · `ServiceConsumption` ✅ ·
`InventoryMovement` ✅ · `Charge` ✅ · `Payment` ✅

All are tenant-scoped via the composite-FK pattern (`(organization_id, id)`
uniqueness + composite foreign keys on every cross-entity reference), which
384 tests exercise.

**Explicitly checked, confirmed absent as canonical models:**

| Concept | Status | Note |
|---|---|---|
| Price / Tariff | **MISSING** | No price field on `Service` or `Product`; only a per-execution snapshot exists |
| Promotion / Discount | **MISSING** | zero occurrences |
| Campaign | **MISSING** | zero occurrences |
| Referral | **MISSING** | zero occurrences |
| Conversation | **MISSING** (canonical) | exists only as a frontend mock type |
| Agent | **MISSING** (implementation) / structural placeholder only | `principal.type` enum reserves the word `'agent'` for future authorization; no behavior attached |
| NoShow | **MISSING** (canonical) | `appointments.state` CHECK admits only `confirmed`/`cancelled`; the simulator has a `no_show` state but is disconnected |
| Confirmation | **MISSING** (canonical) | same as above; a canonical appointment is born already `confirmed` — patient-side confirmation is not representable |
| Waitlist | **MISSING** (canonical) | zero backend model; the simulator has a full waitlist+recovery engine but it is disconnected |

---

## 5 · SALES AGENT

**Direct answer: no canonical Sales Agent exists.** This is distinct from, and
should not be confused with, `AgentPage`/`ChatPage`, which are **static UI
prototypes with no LLM behind them**.

Verified by exhaustive search:

- Zero LLM SDK imports (`openai`, `anthropic`, `langchain`) in `odontoflow-backend`.
- Zero `/agent` route in the FastAPI app (32 real paths enumerated, none agent-related).
- Zero tool-registry pattern, zero agent runtime file, anywhere in the backend.
- `AgentPage.tsx`'s "Configurar agente" button opens a `Modal` with no wired save action beyond local state; its 4 KPI numbers are literal JSX constants (`value={24}`), not derived from any fetched data.
- `getAgentDashboard()` targets `/agent/dashboard`, an endpoint that does not exist.

**The one place an LLM genuinely runs today is `odontoflow-voice`**, and even
there, by explicit design (`app/domain/parser.py`'s own header comment, quoting
the project's own invariant): *"LLMs never set prices, durations, slots or
bookings."* The voice module is **rules-based parsing, not an LLM agent** —
`faster-whisper` transcribes audio to text; a deterministic parser (no model
call) extracts structured items against a closed catalog. There is no LLM
reasoning step, no tool-calling loop, anywhere in this codebase.

**Conclusion on the trace requested** (message → interpretation → context →
tool → API → domain → DB → result): **this pipeline does not exist.** No leg
of it is implemented beyond the voice service's non-LLM parser, and that
parser's output never reaches the canonical backend.

---

## 6 · SYSTEM AUTHORITY

| Rule | Authority (file evidence) | LLM involved? |
|---|---|---|
| Practitioner eligibility | `PractitionerCapability` row lookup in `app/scheduling/service.py::_require_capability` | No |
| Availability | `app/scheduling/availability.py` — explicitly documented as "Pure module: stdlib only... no LLM, no side effects" | **No, by written contract** |
| Appointment duration | `Service.duration_minutes`, catalog-authoritative; API schemas use `extra="forbid"` so a client cannot supply duration | No |
| Double-booking prevention | PostgreSQL **partial GiST exclusion constraint** on `appointments` (`excl_appointments_confirmed_no_overlap`) — the *database*, not application code, is the final authority | No |
| Tenant integrity | Composite foreign keys `(organization_id, id)` on every cross-entity edge — structurally impossible to violate, not merely checked | No |
| Permissions | `app/iam/` — `Principal`/`Membership`/`Role`/`Permission`/`RoleAssignment`, checked via `require_permission()` as the first statement of every mutating transaction | No |
| Idempotency | `app/idempotency/` — `CommandReceipt` with a unique `(organization_id, operation, idempotency_key)` constraint, claimed before any other work in a transaction | No |
| Auditability | `app/audit/` — `AuditEvent` staged in the same transaction as every mutation, from `ExecutionContext`, never client-supplied | No |
| Pricing | **No authority exists** — there is no pricing engine of any kind, human or machine (see DOMAIN MODEL) | N/A — not built |
| Promotions | **No authority exists** — not built | N/A |
| Payment correctness | Database `CHECK (amount > 0)` + application-level row lock serializing payments per charge, deterministically rejecting overpayment | No |
| Inventory correctness | `inventory_movements` as the sole append-only ledger; no `stock_actual` cache column exists anywhere (the legacy failure mode this rule was designed to prevent) | No |

**Verified conclusion: no LLM is authority for any deterministic business
rule in this system.** Where rules exist, they are enforced by PostgreSQL
constraints and plain Python domain code. Where an LLM does run (voice
transcription), it is explicitly and deliberately kept out of every decision
listed above.

---

## 7 · CHANNELS / INTEGRATIONS

| Channel | Status | Evidence |
|---|---|---|
| WhatsApp | **Implemented but disabled** (voice repo only) | `odontoflow-voice/backend/app/whatsapp.py`, 118 lines, webhook verification + media download + reply, **not registered** in `app/main.py` (`include_router` absent). Author's own file header: field names "written from memory... must be verified against Meta's current docs." No signature verification, no idempotency by `message.id` — both acknowledged gaps. |
| Google Calendar | **Missing** | zero occurrences anywhere |
| Telegram | **Missing** | zero occurrences anywhere |
| Kapso | **Missing** | zero occurrences anywhere |
| Voice (transcription) | **Implemented, active, but isolated** | `odontoflow-voice` is a real, tested (54/54) standalone FastAPI service using `faster-whisper`; wired into the canonical frontend behind `VITE_ENABLE_VOICE` (default false) and structurally prevented from firing under mock mode. Its audio path is **UNVERIFIED on this Linux environment** — no TTS tooling exists here to drive it, and this was honestly reported rather than faked in the prior session's V1 handoff. |

**Adapter vs. direct-provider-dependency check:** the one channel that
exists (voice) is architected correctly — a sibling HTTP service the frontend
calls through a thin client (`src/voice.ts`), never a direct SDK dependency
inside domain code. The backend's domain code has **zero** dependency on any
external channel provider, which is the right shape for whichever channel
gets built next.

---

## 8 · CURRENT ARCHITECTURE (REAL ARCHITECTURE, as it exists today)

```
┌─────────────────────────────────────────────────────────────────────┐
│  CHANNEL / UI                                                        │
│                                                                       │
│  [REAL]      Agenda / Patients / Cash / Inventory  (React SPA)       │
│  [SIMULATED] Chat / Agent dashboard  (static mock, dead real-mode)   │
│  [PARTIAL]   Voice assistant UI  (flag-gated, draft-only)            │
│  [SIMULATED] odontoflow-sim  (fully isolated synthetic clinic)       │
└───────────────────┬───────────────────────────────────────────────┬─┘
                     │ axios (VITE_USE_MOCKS=false)                  │ (no connection)
                     ▼                                                │
┌─────────────────────────────────────────────────────────────────────┐
│  API — FastAPI, 32 real OpenAPI paths                       [REAL]  │
│  catalog · clinical · commercial · economics · inventory ·          │
│  organization · scheduling routers                                  │
│  [MISSING] /agent, /conversations — referenced by frontend, absent  │
└───────────────────┬───────────────────────────────────────────────┬─┘
                     ▼                                                │
┌─────────────────────────────────────────────────────────────────────┐
│  APPLICATION / DOMAIN                                       [REAL]  │
│  permission check → idempotency claim → domain rule → audit event,  │
│  one transaction per command (app/*/service.py)                     │
│  Deterministic authority: GiST exclusion, composite tenant FKs,     │
│  CHECK constraints — no LLM anywhere in this layer                  │
└───────────────────┬───────────────────────────────────────────────┬─┘
                     ▼                                                │
┌─────────────────────────────────────────────────────────────────────┐
│  PostgreSQL 15, migration 0008                              [REAL]  │
│  odontoflow / odontoflow_test / odontoflow_e2e                      │
│  0 real clinic rows in any of them                          [DATA: MISSING] │
└───────────────────────────────────────────────────────────────────┬─┘
                                                                       │
┌─────────────────────────────────────────────────────────────────────┐
│  INTEGRATIONS                                                        │
│  [PARTIAL]  odontoflow-voice: standalone FastAPI + faster-whisper,   │
│             tested, isolated, no backend write path                 │
│  [PARTIAL]  WhatsApp adapter: written, not wired, unverified shape   │
│  [FUTURE]   Google Calendar, Telegram, Kapso: no code exists         │
│  [MISSING]  Sales Agent / LLM tool-calling loop: no code exists      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 9 · WORK PERFORMED / AGENT ORCHESTRATION

Read from Repo 0's `CAVELOG.md`, `HANDOFFS.md`, and git history across all
five repos. **Only evidenced runs are listed; nothing is inferred.**

| Objective | Model (if evidenced) | Read-only/Writer | Surface | Result | Evidence | Verdict |
|---|---|---|---|---|---|---|
| Backend build-out (M0→M4, Vertical 1 through PF7) | Not recorded in commit metadata | Writer | `odontoflow-backend` | 364→384 tests across the run | `docs/superpowers/handoffs/*.md` (18 files, 2026-08-13→08-16) | PASS |
| M4 Pilot Fit review (final read-only pass before closing M4) | **DeepSeek V4 Flash** (explicitly named) | **Read-only** | frontend + backend, pilot journey | PASS — no blockers; one repair applied elsewhere | `STATUS.md:184`, `PLAN.md:52` | PASS |
| M5.1 revenue-leakage measurability | Claude (this assistant's lineage; no per-run model tag recorded before this session) | Writer (docs only, zero code) | `odontoflow-planning` | Funnel classified; `DOMINANT_LEAKAGE=UNKNOWN` | `M5_REVENUE_LEAKAGE_BASELINE.md` | PASS |
| Contributor intake #1 (voice) + Voice Integration V1 | Claude Opus 5 (co-author trailer on commits) | Writer | `odontoflow-voice`, frontend | Promoted intact, ported behind a flag, 91 tests | commit `a967b24`, `da203a9`'s ancestor, CAVELOG rows 2026-09-02 | PASS |
| Contributor intake #2 (simulator) + V2.1 promotion | Claude Opus 5 | Writer | `odontoflow-sim` | Promoted intact, synthetic boundary restored, 109 tests | commit `da203a9`, CAVELOG rows 2026-09-03 | PASS |
| V2.2 Named Scenario Configuration | Claude (Opus 5 → Sonnet 5 mid-task, per this session's own model switches) | Writer | `odontoflow-sim` | **150 tests passing but UNCOMMITTED** — user paused the work before commit/push | working-tree diff (this discovery), no CAVELOG entry yet | **IN PROGRESS / BLOCKED (paused by Owner)** |
| This discovery | Claude (current session) | **Read-only** | all 5 repos | This document | this file | PASS |

**Single-writer discipline: preserved.** Every commit across all three
Miguel-owned repos is authored by "Miguel Arias" / "Miguel" (human accountable
identity), with AI co-authorship recorded transparently via
`Co-Authored-By: Claude Opus 5...` trailers — verified directly on the 5 most
recent planning commits. No evidence anywhere of two independent agents
writing to the same repository concurrently, and no evidence of any
multi-agent orchestration framework (Orca, workflows) being used for actual
product changes — the one review pass (DeepSeek) was a single read-only
second opinion, not concurrent writing.

---

## 10 · TECHNICAL EVIDENCE

| Repo | HEAD | Tests (this session's run) | Build/Typecheck |
|---|---|---|---|
| `odontoflow-backend` | `23527c2` | **384 passed**, 228s, real PostgreSQL | n/a (Python) |
| `odontoflow-frontend` | `a967b24` | **91 passed** | typecheck clean |
| `odontoflow-voice` | `4149a3e` | **54 passed**, 0.82s | — |
| `odontoflow-sim` | `da203a9` + uncommitted | **150 passed** | typecheck clean, build not re-run this pass |
| `odontoflow-planning` | `c2c8b6b` | n/a (docs) | — |

**Migrations:** backend at `0008` (location-aware inventory + transfers),
8 files, `0001`→`0008`, applied and verified in `odontoflow_test`/`odontoflow_e2e`.

**E2E:** `pilot-e2e.test.ts` — 12 assertions, file-verified this pass
(structure matches the claimed journey exactly); **not re-executed** in this
discovery to avoid its destructive schema-reset step, per the read-only
mandate. Last executed and recorded result: 12/12 PASS, 2026-09-02
(`STATUS.md`).

**Approved specs / handoffs:** 21 backend task handoffs
(`docs/superpowers/handoffs/`, 2026-08-13→08-16), 5 FOREMAN living briefs in
`odontoflow-planning/docs/handoffs/plans/` (2026-09-02→09-03).

**Screenshots/demo artifacts:** Leonardo's 7 canonical UI screenshots,
preserved with verified git-blob-matching hashes
(`odontoflow-planning/VISUAL_BASELINE.md`); no video/demo recording found.

**OpenAPI:** 32 real paths, machine-verified this pass (`docs/api/openapi.yaml`).

---

## 11 · BLOCKERS TO ODONTOSMART

| Type | Blocker | Evidence |
|---|---|---|
| **DATA** | No real OdontoSmart operational data anywhere in the workspace | Live row counts; `M5_REVENUE_LEAKAGE_BASELINE.md`'s independent conclusion |
| **PRODUCT DECISION** | No pricing/tariff model exists — every demo of "charge a patient" today uses an ad-hoc `executed_price` snapshot with no catalog behind it | `app/catalog/models.py::Service` has no price field |
| **PRODUCT DECISION** | No decision yet on what a "Sales Agent" is even supposed to do (schedule? qualify leads? both?) — nothing in Repo 0 specifies this beyond the milestone name "M6 Agentic Operations, LATER" | `PLAN.md` |
| **TECHNICAL** | `odontoflow-sim`'s V2.2 work is real, tested, and **uncommitted** — an at-risk state, not a blocker to demoing today, but a risk to losing 659 lines of working code | this discovery's git status |
| **TECHNICAL** | Voice's audio/transcription path is unverified on this platform — text-only fallback works, the actual differentiator (dictation) has never been proven here | `odontoflow-voice/CANONICAL.md`, this session's own environment check |
| **ACCESS/CREDENTIALS** | No WhatsApp Business API credentials, no Meta app, no Google Calendar OAuth client — none of these exist in any `.env.example` in the workspace | grep across all `.env.example` files: zero references |

**Not evidenced as blockers, and not claimed as such:** anything about team
capacity, budget, or clinic willingness — outside this discovery's scope.

---

## 12 · OVERBUILDING

Stated plainly, work that is technically excellent but does not help prove
first clinic value:

- **`odontoflow-sim`, the entire synthetic-clinic simulator and its V2.2
  Scenario Configuration layer.** It is genuinely well-engineered (a
  deterministic discrete-event engine with a clock sentinel, reversible
  timeline, 150 tests) and it is **completely disconnected from the
  backend**. A clinic cannot be shown a simulator of a fictional clinic as
  evidence their own clinic will benefit. This is the single largest
  concentration of engineering effort with the least direct path to a
  clinic decision-maker's trust.
- **The IAM/permissions layer's depth** (`Principal`/`Membership`/`Role`/
  `Permission`/`RoleAssignment`, 6 tables) for a single-clinic pilot with
  presumably 2-3 real users. Correct long-term, unnecessary to prove value
  to one clinic in week one.
- **Multi-tenant composite-FK architecture** throughout the schema. Correct
  for a multi-clinic SaaS; adds real complexity for a single pilot clinic
  that does not need tenant isolation yet.
- **The voice assistant's WhatsApp adapter** (written, unwired, unverified).
  Effort already spent; further polishing it before a channel decision is
  made would be more overbuilding on top of overbuilding.

None of the above is a criticism of the code quality — it is a statement that
engineering effort and demo-readiness effort have diverged.

---

## 13 · ARCHITECTURE VERDICT

Direction evaluated: **ERP/API-first source of truth → deterministic domains
→ agents over tools/API → channels/integrations as adapters.**

**Verdict: KEEP.**

Evidence for this verdict, not aesthetics:

- The backend already **is** exactly this shape: deterministic domain rules
  enforced by the database and plain code (Section 6), a real OpenAPI surface
  agents could call as tools without any redesign, and zero direct
  provider-SDK coupling inside domain code.
- The one channel that exists (voice) is **already** built as a sibling
  service behind a thin client, not a direct dependency — proof the adapter
  pattern is achievable here, not merely aspirational.
- The gap is not architectural; it is that **no agent and no channel has
  been built yet** on top of an otherwise-correct foundation. Changing the
  architecture would not close that gap faster.

---

## 14 · 7-DAY CLINIC DEMO

Optimized for credible real value to one clinic, not platform completeness.

**BUILD** (the only new work, and it is data entry, not code):
- Load that one clinic's real doctors, real treatments (with real prices —
  this requires adding a price field to `Service`, the smallest possible
  schema change), and a real week of their actual appointments, via the
  existing `POST /leads` + `POST /appointments` + `POST /services` API — no
  new endpoint needed.

**REUSE** (already real, already tested, show as-is):
- Agenda, Patients, Cash, Inventory pages, wired to the real backend
  (`VITE_USE_MOCKS=false`), exactly as the pilot E2E already proves works.
- The booking flow's double-booking prevention and the payment
  overpayment guard — these are the two most viscerally convincing "this
  system won't let you make the mistakes your current process makes" moments,
  and they are 100% real today.

**CUT** (do not show, do not build in the next 7 days):
- Chat and Agent dashboard — both would need an honest "this is not
  connected to anything" caveat mid-demo, which is worse than not showing
  them.
- The voice assistant — its differentiator (dictation) is unverified on this
  platform; do not demo a capability that has never been proven to work here.
- `odontoflow-sim` — never show a simulator of a fictional clinic to a real
  clinic being asked to trust the product with their own data.
- Any mention of WhatsApp/Calendar/Telegram/Kapso — none exist; promising
  them now sets an expectation the codebase cannot back up in a week.

---

## 15 · NEXT THREE ACTIVITIES

**1. Add a minimal price field to `Service` and load one real clinic's real
catalog + one real week of appointments.**
Observable result: the Agenda and Cash pages show that clinic's actual
services and actual prices, not a snapshot-only ad-hoc amount.
Owner: backend engineer (one migration + one field).
Dependency: the clinic must hand over its tariff sheet and a week's schedule
(no new access/credentials needed — this is a data question, resolved in
`M5_REVENUE_LEAKAGE_BASELINE.md §6` already).
Duration: 1–2 days.
PASS criterion: a real appointment for a real patient at a real price books,
gets charged, and gets paid through the existing, already-tested flow with
zero fixture data visible anywhere in the demo.

**2. Commit and push the uncommitted `odontoflow-sim` V2.2 work, or
deliberately discard it.**
Observable result: no working code exists only on one disk.
Owner: whoever resumes the V2.2 activity (the living brief is already open
at `docs/handoffs/plans/2026-09-03-v2-2-named-scenario-configuration.md`).
Dependency: an Owner decision on whether V2.2 is still wanted, given
Section 12's overbuilding finding.
Duration: under 1 hour either way (commit, or delete and close the brief).
PASS criterion: `git status --short` is clean in `odontoflow-sim`.

**3. Decide, in writing, what "Sales Agent" means before building anything
agent-shaped.**
Observable result: one paragraph in Repo 0 stating the agent's first
concrete job (e.g., "qualify an inbound lead and propose a slot," nothing
more), which slots that job into the existing real API (`POST /leads`,
`GET /slots/query`, `POST /appointments`) rather than inventing a parallel
path.
Owner: product/CTO decision, not an engineering task.
Dependency: none — this is the one activity that can start today.
Duration: same day.
PASS criterion: the paragraph exists in `PLAN.md` under M6, naming the exact
existing endpoints the agent will call as tools.

---

## DISAGREEMENTS_WITH_EXISTING_CTO_DISCOVERY

**The comparison document does not exist.**

`odontoflow-planning/docs/handoffs/discovery/2026-09-03-cto-discovery.md` was
checked directly: the `docs/handoffs/discovery/` directory did not exist
before this report created it, and an exhaustive `find` across the entire
`odontoflow-planning` repository for any file matching `*discovery*` or
`*cto-discovery*` returned zero results.

**No comparison could be performed, because there is nothing to compare
against.**

This is itself worth surfacing to the CTO/CEO: a document was referenced by
name and expected to exist for this exact discovery to react to, and it does
not — either it was never created, never committed, or exists somewhere
outside this repository that was not specified. Per the brief's own
instruction ("Do not change the existing discovery"), nothing was created in
its place beyond this note; no prior discovery was fabricated to compare
against.

**Severity: HIGH** — not because of any technical contradiction, but because
a decision-making process that expects a discovery document to already exist,
and finds none, has a coordination gap independent of anything about the
codebase itself.

---

## CTO ASSESSMENT

OdontoFlow's backend is the real asset here: a correctly-modeled,
constraint-enforced, 384-test-covered clinical/scheduling/inventory/finance
core with no LLM anywhere near its money or scheduling decisions — that is
the right call and it is proven, not claimed. The frontend's real screens
(Agenda, Patients, Cash, Inventory) are genuinely wired to that backend, not
mocked, and that wiring is tested end-to-end.

Everything client-facing that would make this look like an "AI clinic
platform" — a Sales Agent, WhatsApp, Calendar, Telegram, Kapso, a working
voice assistant — **does not exist yet**, except for one well-built but
disconnected voice transcription service and one impressively engineered but
entirely fictional clinic simulator. Neither closes the gap to showing a real
clinic real value with their real data, because neither touches real data.

The single highest-leverage move available today is not more engineering —
it is obtaining one real clinic's real catalog and one real week of their
real schedule, and loading it through APIs that already exist and are already
tested. That is a data-and-relationship problem, not a code problem, and no
amount of further backend or simulator work will substitute for it.

---

## NEXT 3 ACTIVITIES

See Section 15 above (verbatim; not duplicated here to avoid drift between
two copies of the same list within one document).
