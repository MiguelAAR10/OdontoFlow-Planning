# LOCAL-RUNTIME-SMOKE-01 — FOREMAN living brief

## Executive status

**PASS — local safe smoke verified; no next activity started.** The existing
PostgreSQL CORE, FastAPI app, and fake-model Sales Agent test runtime ran
locally with real PostgreSQL and no paid model. Proposal creation, negative
response safety, outbound persistence, and the current synthetic-provider
boundary are evidenced. The next blocking connection is deliberately outside
this activity: an authorized outbound dispatcher/live channel. Automatic agent
booking remains fail closed pending the already-approved trusted
proposal-bound acceptance mechanism.

Backend result commit: `021fa5297f520313f4920d6916e069f09fb640dc`.

## Objective and success criteria

Establish the smallest reproducible local smoke procedure for the existing
Lead → Appointment components, without changing the fail-closed booking
policy, adding architecture, or writing production data.

Success criteria met:

- existing PLAT-01 PostgreSQL container is healthy and local CORE is at the
  repository migration head;
- FastAPI starts with explicit local settings and answers `/health` and
  `/docs`;
- the supported fake-model/WF-01 test runtime persists a proposal and verifies
  pending proposal plus zero appointments in real PostgreSQL;
- a later `No, thanks` message cannot create an appointment and the error is
  audited;
- outbound persistence and its current consumer boundary are identified;
- exact startup/smoke commands, outputs, limitations, and next blocking
  connection are persisted in the backend technical handoff.

## Repository reality

Backend intake was `main@55f22cce3a8e50f2f18d7b2fce258cbe953ad33`, immediately
after AGENT-CONFIRM-FAIL-CLOSED-03. Its worktree had unrelated pre-existing
dirty/untracked paths; none were staged or changed. The planning worktree was
also already dirty and was preserved. The prior fail-closed implementation and
temporal guard remain unchanged.

The backend's README and DEVELOPMENT guide contain stale historical test and
migration counts. The n8n lab guide is a PowerShell-oriented integration guide,
and the checked-in WF-01 export is inactive. This activity uses a new,
self-contained handoff recipe rather than broad runbook cleanup.

## Authority and evidence used

The execution used the repository `AGENTS.md`, the installed
`odontoflow-engineering`, `postgres-best-practices`,
`verification-before-completion`, and `foreman-handoff` skills; PLAT-01's
existing named PostgreSQL setup; the AGENT-CONFIRM-FAIL-CLOSED-03 handoff; the
W4 runner/tests; and the messaging outbound service/router/tests. These sources
establish that PostgreSQL is canonical, the fake Sales Agent path is
HTTP-shaped but injectable for tests, and `provider=test` is synthetic-only.
No new consent or delivery semantics were inferred.

## What we will build and how

No product implementation is needed. The bounded artifact is documentation:

1. Reuse `odontoflow-db-1` on port 5434 and explicitly target local CORE,
   avoiding the ignored external `.env.local` target.
2. Start FastAPI from `app.run` and verify `/health` plus `/docs`.
3. Run the existing W4 fake-model tests serially against `odontoflow_test` and
   their disposable separate agent-memory databases.
4. Run the focused outbound persistence and synthetic-provider claim tests.
5. Record the durable outbound write boundary and the claim/settle boundary;
   do not add a dispatcher or live channel.

## Execution model

Solo FOREMAN. The tests share a real PostgreSQL test database and the requested
work is one documentation/runtime verification lane, so parallel workers would
add contention without reducing risk.

## Risks, conflicts, and protected surfaces

The ignored `.env.local` in this checkout points at an external target and is
also sourced by `scripts/platform/doctor.sh`; running doctor as-is is therefore
not a safe local smoke check. Its `postgresql://` target also selects the
missing `psycopg2` driver in this environment, so doctor exits failed before a
safe local check. It was not edited or staged. Explicit local environment
overrides are the documented workaround.

The current `provider=test` output is persisted but excluded from
`/internal/outbound/claim`; no external dispatcher, n8n runtime, WhatsApp,
real-model credential, migration, schema, auth bypass, consent mechanism, or
production write is in scope. The booking temporal and fail-closed guards,
tenant/conversation isolation, expiry, idempotency, and audit behavior are
preserved.

## Evidence and validation

Fresh local evidence, run serially:

- `odontoflow-db-1` was healthy on `127.0.0.1:5434`; local CORE reported
  PostgreSQL 15.18 and Alembic `0018 (head)`.
- API startup with explicit local `DATABASE_URL` succeeded; `/health` was
  HTTP 200 with `{"status":"ok"}` and `/docs` was HTTP 200; the process was
  stopped cleanly after the check.
- `test_wf01_three_turn_loop_persists_once_and_keeps_threads_isolated` plus
  `test_wf01_rejects_negative_later_message_before_booking`: **2 passed, 2
  warnings in 6.52s**. Assertions observed pending proposals, zero
  appointments, persisted negative text, fail-closed `INVALID_INPUT` audit,
  and outbound receipts/status.
- `test_outbound_message_and_queue_row_are_atomic_and_idempotent` plus
  `test_synthetic_provider_is_persisted_but_never_claimed_for_external_dispatch`:
  **2 passed, 2 warnings in 3.25s**.
  Backend documentation result: commit
  `021fa5297f520313f4920d6916e069f09fb640dc`.
- `./scripts/platform/doctor.sh` was intentionally not treated as a pass:
  it reported `doctor: FAILED` after loading the ignored external
  `.env.local` target and failing its missing `psycopg2` driver import. The
  direct local commands succeeded.

The previous PASS handoff already recorded the current 529-test full suite;
this activity made no product/test/schema change and therefore did not rerun
the full suite.

Canonical technical evidence:
`odontoflow-backend/docs/superpowers/handoffs/2026-09-16-local-runtime-smoke-01.md`.

## Decision and progress log

- 2026-09-16 — Reused the existing PLAT-01 PostgreSQL CORE container; no new
  Docker architecture was created.
- 2026-09-16 — Verified FastAPI and the injected fake-model Sales Agent path
  with explicit local settings and real PostgreSQL.
- 2026-09-16 — Confirmed the fail-closed negative-response result remains
  effective: pending proposal, zero appointments, audited error.
- 2026-09-16 — Confirmed outbound persistence is durable, while synthetic
  `provider=test` remains intentionally outside external claiming.

## Next approval / next step

No next activity is authorized or started automatically. The next connection
requires an explicit deployment/channel decision for an authorized outbound
worker and live provider. Independent of that, automatic booking remains held
until a trusted, authenticated, proposal-bound patient acceptance source is
approved; this smoke task did not alter that policy.
