# AIRYTHM-REALITY-01 — Lead → Appointment vertical reality audit — FOREMAN living brief

> Final handoff. Self-contained: the CTO has no codebase access.
> Activity: first repository-grounded audit after the Web-memory recovery.
> Verdict: **NOT_CONNECTED — the middle of the loop is real; both ends are missing.**

## Executive status

**Answer to the product question: NO — the system cannot complete the first sellable vertical end-to-end today.** The deterministic core, conversation persistence, the Sales Agent runtime, the tool gateway, availability, the two-phase proposal and the canonical appointment are genuinely built and proven against real PostgreSQL. But nothing real gets **in** (no channel adapter), nothing real gets **out** (no outbound consumer), the agent has **never run against a real model provider**, its HTTP entrypoint is **unauthenticated**, and the audit found "explicit patient confirmation" was **prompt-enforced only**. AGENT-CONFIRM-GUARD-01 now closes that code-level booking gap; the remaining connectivity and product-decision blockers still keep the overall verdict NOT_CONNECTED.

Active gate: none for the audit or completed guard. Two additional Owner
decisions still gate the real loop.

## Objective and success criteria

Objective: determine the real state of the Lead → Appointment vertical and select exactly ONE next development activity; the selected activity and its completion are recorded below.
Met: reconciliation matrix (§Reality), execution trace (§Trace), gap map, one-activity contract (§Next step), all persisted below.

## Repository reality (verified 2026-09-15, not trusted from docs)

| Repo / worktree | Branch | HEAD | Dirty | Role |
|---|---|---|---|---|
| odontoflow-backend (canonical) | main | `b7f11ce` | untracked docs only | FastAPI + PostgreSQL domain authority |
| deploy worktree `~/orca/workspaces/odontoflow-backend/deploy-sales-agent-cloud` | `MiguelAAR10/deploy-sales-agent-cloud` | `cb918fb` | clean | Agent image (`Dockerfile.sales-agent`) + Gemini dep; **no loop logic** (diff verified empty for `sales_agent/ app/ integrations/`) |
| `origin/codex/render-current-lab-20260908` | remote-only | `b140ede` | — | 1 unmerged commit: reception continuity state (P1, not on main) |
| `origin/codex/backend-n8n-pilot-20260903` | remote-only | `d5274d3` | — | ancestor of main (fully merged) |
| `integration/sales-agent-v0` | local+remote | — | — | ancestor of main (ignore) |
| odontoflow-frontend | main | `a788df5` | dirty | Operator ERP; Agenda real, Chat/Agent mock-only |
| odontoflow-planning (Repo 0) | main | `63274e1` | dirty (this audit + prior 09-13 docs) | Control plane |
| Recovered Web memory (4 files) | — | — | — | intent evidence, staged `.audit/recovery/web-memory-2026-09-15/` |

Follow-up state (2026-09-16): backend `main` advanced to
`6b0d2226e930030c3c1582851c20b9894b56225d` for AGENT-CONFIRM-GUARD-01;
`origin/main` remains at the pre-task base. The backend worktree retains only
pre-existing unrelated dirty/untracked files outside the bounded commit.

**Runtime environment:** `odontoflow-db-1` (postgres:15-alpine) healthy on 127.0.0.1:5434, schema at alembic `0018`. **No n8n** (no container/binary/port 5678; MCP 401). Nothing on :8000. Backend venv has `langchain 1.4.0`, `langgraph 1.2.11`, `langgraph_checkpoint_postgres`, `langchain_openai` — **no `langchain_google_genai`**.

## The vertical as it actually is

```
[real patient] ✗ no adapter anywhere (whatsapp is a DB enum only)
WF01Runner (test provider only, rejects provider != "test")
  → POST /internal/messages/inbound            ✅ real, real-PG tested
  → POST /sales-agent/turn                     ⚠️ exists · NEVER real-model · NO AUTH
  → 7 typed tools → POST /agent-tools/call     ✅ Bearer + permissions + audit
  → query_available_slots → find_available_slots ✅ + GiST DB invariant
  → propose_appointment (token, 15-min TTL)    ✅ two-phase, FOR UPDATE, audit
  → [patient says yes in a new message]        ✅ persisted later-inbound booking guard (added 2026-09-16)
  → confirm_appointment → Appointment(confirmed) ✅ + audit + idempotency
  → outbound reply persisted                   ✅
  → /internal/outbound/claim                   ✗ NOTHING POLLS IT (dispatcher never built)
  → operator UI                                ✗ Chat/Agent mock-only; /internal is browser-unsafe; Agenda ✅
```

Full trace with producer/consumer/contract/test/runtime per transition: `.audit/airy-reality-01/vertical-trace.md`.
Memory reconciliation matrix (26+ claims, VERIFIED_CURRENT / PARTIALLY_VERIFIED / STALE / NOT_IMPLEMENTED / BLOCKED / UNKNOWN): `.audit/airy-reality-01/reality-reconciliation.md`.

## Authority and evidence used

- Planner (Claude Opus, read-only): `.audit/airy-reality-01/planner-plan.md`.
- Scouts (read-only, one report each): `scout-a-core-backend.md`, `scout-b-sales-agent.md`, `scout-c-integration-runtime.md`, `scout-d-operator-frontend.md` (same directory).
- Coordinator-run tests (serialized; no concurrent pytest):
  - Focal: `.venv/bin/python -m pytest -q tests/test_lead_to_appointment_e2e.py tests/test_sales_agent_w4.py tests/test_reception_agent_phase5.py` → **19 passed, 2 warnings in 26.70s**
    (`evidence/focal-tests-2026-09-15.log`)
  - Full suite: `.venv/bin/python -m pytest -q -rs` → **527 passed, 0 skipped, 0 failed, 21 warnings in 535.32s** (`evidence/full-suite-2026-09-15.log`)
- Recovered Web memory: `.audit/recovery/web-memory-2026-09-15/` (CTO/CEO/PRODUCT/ARCHITECTURE; two architecture variants found in the source folder, the 2194-line variant staged as canonical).
- Prior audits corroborated: `docs/reviews/2026-09-11-backend-product-reality.md`, `docs/architecture/{AS-IS,TO-BE,GAP}*.md`.

## What the audit changed vs. prior knowledge

1. **New P0 discovered and then closed:** explicit patient confirmation was prompt-enforced only in the booking path (`app/agent_tools/booking.py`); AGENT-CONFIRM-GUARD-01 added the persisted later-inbound guard, matching the cancellation path's established semantics (`app/agent_tools/reception.py`).
2. **Control-plane correction:** `deliveries.manage` + the `outbound-dispatcher` profile already exist (since 2026-08-30); the real gap is the consumer worker. `orchestration/current-activity.yaml:48` was stale on this.
3. **Agent image exists but only on an unmerged worktree** (`Dockerfile.sales-agent`); main's Dockerfile cannot run the agent.
4. **Model reality is worse than "unproven":** the only real attempt (Gemini, deploy branch) failed `429 ResourceExhausted` (billing).
5. **Operator surfaces are absent, not just mocked:** the backend routes the UI calls (`/conversations`, `/agent/dashboard`) do not exist; no proposal/handoff concept in the frontend; `/internal/*` is documented browser-unsafe.
6. **Memory contradictions recorded** (never silently resolved): ARCH §39.1 "no canonical Sales Agent" is stale; "Lead lifecycle not verified" sharpens to "no state machine at all"; Cloud Run "TARGET/PROPOSED" is stale for backend-only.

## Execution model

Orchestrated: one read-only planner (Claude Opus, high effort) + four disjoint read-only scouts (Claude Sonnet) + coordinator-run serialized tests. Planner and scout dispatches: `ctx_292e2154e236` (planner, released), `ctx_3018a2c8e725` (A), `ctx_e2ce1cb0f606` (B), `ctx_7c3bdb6d8ccb` (C), `ctx_71b685c8b376` (D). Orca run `run_85bc67973ed4`. Orca retained scout terminals A/B/C under `user_takeover` authority (`processAction: none`); D was released. Release was retried; Orca keeps A/B/C retained, so they were left open by Orca authority (never force-closed) — the Owner may close them manually. No worktree was created; nothing outside the evidence tree was written.

## Risks, conflicts, and protected surfaces

- Read-only audit: no code, schema, migrations, or protected surface touched (`app/errors.py`, `app/db.py`, `app/scheduling/availability.py`, existing migrations, `medistock`, `odontoflow-sim` all untouched).
- No secrets persisted: env files inspected for key names only.
- No production mutations; no external side effects (no live WhatsApp/Cloud Run/n8n calls; Cloud Run liveness left UNKNOWN).
- AGENT-CONFIRM-GUARD-01 implementation used only real test PostgreSQL and changed no schema, migration, protected path, channel, deployment, or production data. The same-turn booking defect is now rejected server-side; remaining real-loop risk is the unconnected inbound/model/outbound/auth surface described above.

## Decision and progress log

- 2026-09-15 — Memory located at `/mnt/c/Users/arias/Downloads/AIRYTHM-WebMemory/`; staged read-only into `.audit/recovery/web-memory-2026-09-15/`. No `NEEDS_MEMORY_FILES` stop required (files ARE accessible to the Orca workspace; durable copy placed in the control plane; `.audit/` is git-ignored by convention — Owner may promote a tracked copy if desired).
- 2026-09-15 — Planner and 4 scouts dispatched, reports accepted, workers released/retained as above.
- 2026-09-15 — Focal tests 19 passed; full suite 527 passed / 0 skipped.
- 2026-09-15 — Audit verdict: NOT_CONNECTED; first broken link = inbound channel; decision-free P0 repairs = confirmation gate, outbound consumer, agent-turn auth, agent image from main.
- 2026-09-15 — Next activity selected (below).
- 2026-09-16 — **AGENT-CONFIRM-GUARD-01 PASS:** booking confirmation now requires a persisted inbound `Message` in the same conversation with `created_at` later than the proposal; same-turn fake-model confirmation leaves the proposal pending and creates zero appointments. Backend commit `6b0d2226e930030c3c1582851c20b9894b56225d`; evidence: `../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-guard-01.md`.

## Next approval / next step — the ONE selected activity

**ID:** `AGENT-CONFIRM-GUARD-01` — *Code-enforce explicit patient confirmation in the booking confirm path.*

- **BUSINESS OUTCOME:** a canonical Appointment can only exist when the patient confirmed it in a separate, later message; the agent can never book a slot off its own proposal inside one turn. The clinic can trust "confirmed".
- **CURRENT FAILURE / GAP AT DISPATCH:** `confirm_contact_booking_proposal` (`app/agent_tools/booking.py:257-303`) checked only proposal status + TTL + token; no code-level "later inbound message than the proposal" requirement, unlike `confirm_cancellation_proposal` (`app/agent_tools/reception.py:781-800`). `SYSTEM_PROMPT` was the only guard; LangGraph could emit propose+confirm in a single turn. Closed by the implementation result below.
- **OBSERVABLE RESULT:** with a scripted fake model that calls `propose_appointment` then `confirm_appointment` in one turn, confirm is rejected with a stable AppError code, the proposal stays `pending`, and the canonical DB holds **0 appointments**; the happy path (proposal turn → later inbound yes → confirm turn) still books **exactly one** confirmed Appointment with the existing audit chain.
- **WRITE SURFACE:** `odontoflow-backend/app/agent_tools/booking.py` (+ optional shared helper); `odontoflow-backend/tests/test_agent_booking_phase4.py` and/or a focused new test file; update `tests/test_sales_agent_w4.py` if its scenario must add the later patient message. No schema/migration; no protected surfaces.
- **DEPENDENCIES:** none external. Requires the test PostgreSQL (`odontoflow_db_1`, :5434). Reuses the existing cancellation-flow semantics — no new product rule; if the Owner wants a different definition of "explicit confirmation", that is a product decision to state before dispatch.
- **RISK:** LOW. Main risk: existing agent tests that confirm without a new message must be updated to the intended semantics; exactly-one booking and idempotency must remain proven.
- **RECOMMENDED MODEL CLASS:** capable coding model, one writer (project default: GPT-5.6 Luna Max; Sonnet/Opus-class acceptable). Escalation only if semantics are contested.
- **REQUIRED SKILLS:** `odontoflow-engineering`, `test-driven-development`, `verification-before-completion`, `postgres-best-practices`.
- **MINIMUM TESTS:** (1) adversarial same-turn propose→confirm rejected, 0 appointments, proposal pending; (2) cross-conversation confirm still NOT_FOUND; (3) expired proposal still rejected; (4) happy two-message confirmation books exactly one appointment with audit; (5) focal suites (`test_sales_agent_w3/w4`, `test_agent_booking_phase4`, `test_reception_agent_phase5`) green; (6) full suite green (≥527 passed).
- **DONE CONDITION:** gate implemented TDD-first against real PostgreSQL; all minimum tests green; full suite green; one commit + handoff per repo contract; no protected surface touched.

## AGENT-CONFIRM-GUARD-01 — implementation result (2026-09-16)

**Status: PASS.** The canonical booking command now rejects confirmation unless
PostgreSQL contains a later inbound message in the same organization and
conversation. The guard runs before appointment creation and does not trust
model-generated claims. Existing proposal expiry, cross-conversation binding,
idempotency, atomic audit behavior, and exactly-one appointment replay remain
covered.

Evidence from the bounded backend task:

- Red regression: same-turn fake-model `propose_appointment` →
  `confirm_appointment` incorrectly returned `confirmed` before the guard.
- Focused real-PostgreSQL suite: **38 passed, 2 warnings**.
- Full serial real-PostgreSQL suite: **528 passed, 21 warnings**.
- Historical pre-change baseline: **527 passed, 21 warnings**; the current
  count is 528 because this task adds one regression test.

The implementation and evidence handoff are committed under
`odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-guard-01.md`.
No next activity is started automatically.

### Why this activity (and what it does NOT claim)

The **first broken link is the missing inbound channel** (G1) followed by the real model (G2), but both are Owner-decision-gated (provider + credentials; provider + billing). G4 (this activity) is the only P0 defect wholly inside the vertical that is dispatchable today with zero external decisions, and it must land **before** a real channel is enabled, or the first real patients can be booked without confirming. It is a parity repair: the cancellation flow already implements exactly this gate. It does **not** make the loop runnable by itself; the remaining decision-free P0s are G3 (outbound dispatcher consumer), G5 (`/sales-agent/turn` auth), G6 (agent image from `main`), and the decision-gated G1/G2.

**Owner decisions pending (gate the real loop):**
1. WhatsApp/provider for sandbox + who owns credentials (G1).
2. Model provider + key/billing — OpenAI (no key today) vs Gemini (key present, billing exhausted) (G2).
3. Cloud Run agent deployment shape (same service vs separate; config committed) — affects G6.
4. Whether "real inbound" for the first sellable vertical means a live WhatsApp channel or an operator-driven message path (changes whether G1 or a smaller operator path is the target).

## Artifacts (all under `odontoflow-planning/`)

| Artifact | Path |
|---|---|
| This living brief (final handoff) | `docs/handoffs/plans/2026-09-15-airy-reality-01-lead-to-appointment.md` |
| Planner plan | `.audit/airy-reality-01/planner-plan.md` |
| Scout reports A-D | `.audit/airy-reality-01/scout-{a,b,c,d}-*.md` |
| Memory reconciliation matrix | `.audit/airy-reality-01/reality-reconciliation.md` |
| Real Lead → Appointment trace + gap map | `.audit/airy-reality-01/vertical-trace.md` |
| Test evidence (focal + full suite logs) | `.audit/airy-reality-01/evidence/` |
| Task specs (planner + scouts) | `.audit/airy-reality-01/*-task-spec.md` |
| Recovered Web memory (staged) | `.audit/recovery/web-memory-2026-09-15/` |
| AGENT-CONFIRM-GUARD-01 backend handoff | `../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-guard-01.md` |
