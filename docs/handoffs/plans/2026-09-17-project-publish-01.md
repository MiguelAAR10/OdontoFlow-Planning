# PROJECT-PUBLISH-01 — Documentation-only onboarding refresh

Date: 2026-09-17
Mode: **documentation and controlled publication** — no product code,
migration, test, environment, or secret-bearing file was touched. The
documentation writer did not commit or push; the coordinator committed and
published the reviewed planning/backend documentation with normal fast-forward
pushes.
Status: **DONE — planning and backend published; frontend intentionally blocked.**

This is the self-contained entry point for anyone picking up publication or
onboarding work after this pass. It answers what is being built, what works,
what is not done, where the logic lives, how to test it, what is off-limits,
how to pick the next task, and where the deeper evidence is.

## What is being built

**OdontoFlow** — a deterministic, multi-tenant clinic operations platform
(PostgreSQL + FastAPI) where humans, agents and integrations operate the same
domain layer under the same rules. The current focus (milestone **M5 — First
Measured Value**) is closing **Reception / Scheduling v1**: the flow that
turns a lead/patient conversation into a confirmed Appointment, with **AIRY**
(the Sales Agent) as one more caller of the same deterministic tools a human
ERP user uses. See [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md) for the
full shape, including the Mermaid diagram, and the vocabulary in
[`CONTEXT.md`](../../../CONTEXT.md).

## What works (verified against real PostgreSQL, sandbox-scoped)

- The deterministic domain core: commercial Lead → booking, multi-tenant IAM,
  execution provenance, idempotent commands, clinical/economic/inventory
  cores (Platform Foundation PF1–PF7, M4 Pilot Fit — see `STATUS.md`).
- The Sales Agent (AIRY) runtime: LangGraph-based, its own
  `langgraph-checkpoint-postgres` memory store, 7 typed tools behind
  `POST /agent-tools/call` (`get_reception_context`, `list_services`,
  `list_locations`, `query_available_slots`, `propose_appointment`,
  `confirm_appointment`, `request_human_handoff`).
- `POST /sales-agent/turn` requires an authenticated agent principal
  (`AGENT-TURN-AUTH-01`, PASS 2026-09-16).
- A controlled, development-only **sandbox** channel provider (additive
  migration `0019_sandbox_provider`) proves the full inbound → agent turn →
  outbound → receipt loop end-to-end, with replay/duplicate protection and
  fail-closed behavior on missing/invalid credentials or cross-tenant
  ingress (`SANDBOX-INBOUND-01`, `SANDBOX-OUTBOUND-02`, `CHAN-01`, `CHAN-02` —
  all PASS, 2026-09-16/17).
- Booking confirmation is fail-closed: same-turn agent propose→confirm is
  rejected (`AGENT-CONFIRM-GUARD-01`); agent-driven confirmation is disabled
  entirely until a trusted proposal-bound acceptance mechanism exists
  (`AGENT-CONFIRM-FAIL-CLOSED-03`).
- Backend `main` is published at
  `193d48b49db6cc4cd04e82965adce08061aad715`, containing the 11 local product
  commits and the scoped onboarding/audit-evidence documentation commits. The
  remote was verified at that exact SHA after normal fast-forward pushes; no
  secrets were introduced by the product delta or documentation commits.

## What is not done (do not read the above as "shipped")

- **Reception / Scheduling v1 as a whole component is NOT DONE.** See
  `docs/handoffs/plans/2026-09-17-reception-core-closeout-01.md` and its
  `.yaml` DONE contract (DC-1..DC-9). Open items include: canonical proposal
  list/read/confirm/decline with authorized exactly-once confirmation
  (`CORE-01`), durable tenant-bound human handoff after authenticated failure
  (`AGENT-02`), agent cancel/reschedule fail-closed (`AGENT-03`), n8n
  transport-only assertions (`CHAN-03`), provider-boundary standing tests
  (`CHAN-04`), and the deploy chain (`DEPLOY-01..05`).
- No real WhatsApp provider or credentials are chosen. OpenRouter configuration
  exists, but the prior real-model attempts did not close a complete acceptance
  loop; any further paid smoke budget is an **owner decision**, not an
  automatic fallback or a publication-task action.
- No real clinic data is loaded anywhere; `M5.2` (revenue-leakage baseline)
  is `BLOCKED_EXTERNAL` on that data.
- **The planning repo was FE2-era on `origin/main` before this pass.** The
  reviewed control-plane publication is now at
  `08b12a0b696c827ea1abdc6d2e2fb9e5517ba98b`; unrelated local tooling and WIP
  remain uncommitted and preserved.
- The backend `README.md`/`DEVELOPMENT.md` test-count claims (previously
  "384 tests") could not be reconciled: `CHANGELOG.md` says 403 at migration
  `0008`, an untracked GAP document says 492, and STATUS.md's most recent
  verified full-suite run (`REAL-MODEL-DIAGNOSTICS-01`, 2026-09-16) reports
  **570 passed / 21 warnings**. No suite was re-run by this documentation
  pass (read-only). Treat `STATUS.md`'s most recent dated entry as the
  freshest number and the backend docs' hardcoded counts as historical only.

## Where the logic lives

| Concern | Location |
|---|---|
| Domain services, PostgreSQL invariants | `odontoflow-backend/app/**` (see `docs/architecture.md` there) |
| Sales Agent (AIRY) runtime, tools, memory | `odontoflow-backend/sales_agent/**` |
| Migrations | `odontoflow-backend/alembic/versions/` (head: `0019_sandbox_provider`) |
| n8n workflow definitions (transport only) | `odontoflow-backend/integrations/n8n/` |
| Frontend UI adapting to the backend contract | `odontoflow-frontend/src/**` |
| Reception/Scheduling v1 closeout plan | `docs/handoffs/plans/2026-09-17-reception-core-closeout-01.{md,yaml}` |
| Per-task technical evidence | `odontoflow-backend/docs/superpowers/handoffs/*` (append-only) |
| Project-wide verified state | `STATUS.md` (this repo) |
| Decision history | `CAVELOG.md` (this repo, newest row first) |

## How to test

See [`DEVELOPMENT.md`](../../../DEVELOPMENT.md) (this repo) for the full
first-day runbook. Summary:

```bash
# Backend, from odontoflow-backend/
docker start odontoflow-db-1                 # PostgreSQL 15, :5434
uv sync --locked
uv run alembic upgrade head                  # -> 0019_sandbox_provider
uv run python -m app.run                     # http://127.0.0.1:8000/docs
uv run python -m pytest -q                   # full suite, real PostgreSQL only

# Focused (Reception / Sales Agent surface)
uv run python -m pytest tests/test_sales_agent_w4.py tests/test_reception_agent_phase5.py -q

# Frontend, from odontoflow-frontend/ (canonical origin only — see publication note below)
npm install
npm run dev                                  # mock mode by default
npm test
npm run test:e2e:pilot                       # needs PostgreSQL :5434 + backend venv
```

Never run two backend pytest processes concurrently against the same test
database. Use `.env.example` for variable **names** only — never commit or
paste secret values.

## Prohibited surfaces (this activity and generally)

- `odontoflow-backend/alembic/versions/**`, `app/errors.py`, `app/db.py`,
  `app/scheduling/availability.py`, existing ERP request/response schemas —
  do not touch without the task explicitly asking.
- The 4 `leonardopanduro-rgb` commits merged into `sales-agent-v0` and any
  other contributor-authored history — never squash, rebase, amend, or
  force-push.
- Canonical databases `odontoflow`, `odontoflow_test`, `odontoflow_e2e`.
- **Frontend files are entirely out of scope for this documentation pass** —
  see the publication block below.
- Secrets, `.env` values, and unreviewed raw audit artifacts remain outside
  the publication. The selected sanitized planning discovery packets were
  reviewed for publication; no packet was rewritten.

## Frontend and planning publication state

- **Frontend (`odontoflow-frontend`) origin is healthy**: `origin/main` =
  `0dbfa9e6705efb5b1e6553e3841ca204533cdf97`, local `main` is exactly 1 commit
  ahead (`a788df56d2d7f0ea5359da3227bb86fb457ca214`, "feat(fe3a): salvage
  checkout through charge"). That commit plausibly matches the FE3A-S1 salvage
  plan's recommended bounded slice and fixes the named payload blocker, but
  **no in-repo artifact authorizes it** — the checkpoint doc explicitly
  withheld commit permission pending an integration-lead gate, and the commit
  has no body/notes recording that gate was passed. **Decision: this commit
  MUST REMAIN BLOCKED for publication** until the coordinator/integration
  lead explicitly confirms it in writing. Do not rewrite or discard it either
  — it is someone's real work.
- The frontend worktree is also dirty beyond that commit: 19 modified tracked
  files and 12 untracked paths, the uncommitted remainder of the same mixed
  FE3A work (`CashPage`, `PatientsPage`, styles, harness config, later
  adapter tests). None of this was touched by this activity.
- Frontend local `main` tracks `leonardo/main`, which now 404s (repository
  gone). **Canonical remote is `origin` = `MiguelAAR10/odontoflow-frontend`.**
  This is an onboarding hazard: a naive `git push` to the tracked upstream
  will fail; push to `origin` explicitly.
- **Planning (`odontoflow-planning`)** is published at
  `08b12a0b696c827ea1abdc6d2e2fb9e5517ba98b`. The commit contains the
  reviewed control-plane refresh, current Reception/Scheduling handoffs and
  selected sanitized discovery packets; unrelated local tooling and WIP
  remains uncommitted and preserved.
- **Backend (`odontoflow-backend`)** is published at
  `193d48b49db6cc4cd04e82965adce08061aad715`. The two untracked CHAN-01
  evidence files with token-like strings remain untracked and were not
  published.

## Task selection — what to pick up next

**No artifact in this repository selects the next implementation activity.**
Per the owner's explicit 2026-09-17 authorization, only `CHAN-01` was
approved, and it (plus the already-PASS `CHAN-02`) is now closed. The
dependency-ordering fact from the Opus closeout plan — not an approval — is:

- Dependency-free, ready now: `CORE-01` (canonical proposal list/read/confirm/
  decline), `AGENT-02` (durable human handoff), `AGENT-03` (agent cancel/
  reschedule fail closed), `CHAN-03` (n8n transport-only assertions, dep
  `CHAN-01` done), `CHAN-04` (provider-boundary tests, dep `CHAN-02` done).
- Gated, not ready: `CORE-02`/`CORE-04` (dep `CORE-01`), `AGENT-01` (deps
  `CHAN-01`/`CORE-01`/`AGENT-02` **plus** an owner-approved paid model
  budget), `DEPLOY-01..03` (dep the `CORE-04` chain).
- Owner-gated, deferred: `CHAN-05`/`CHAN-06`, `DEPLOY-04`/`DEPLOY-05`.

**This document does not authorize `CORE-01`, `CHAN-03`, or any other next
activity.** `orchestration/current-activity.yaml` has been updated to point at
this documentation pass and to record explicitly that the next implementation
activity is owner-decision-required — the coordinator/owner must choose one
and persist it there before any dispatch.

## Handoff location and how this fits the protocol

Per `DEVELOPMENT.md`'s living-brief protocol: this file is the canonical,
self-contained entry point for **PROJECT-PUBLISH-01**. Selected sanitized
planning evidence was published alongside it; technical evidence it references
otherwise keeps its existing homes (`odontoflow-backend/docs/superpowers/`,
`docs/handoffs/discovery/`) and is linked, not copied. When the next activity
is chosen, open or reuse a living brief under `docs/handoffs/plans/`, record
the decision as a new top row in `CAVELOG.md`, and update `STATUS.md`'s
"Next activity" section — do not create a parallel document.

## Files changed by this activity

Documentation plus controlled publication, within the allowed write surface: `README.md`,
`DEVELOPMENT.md`, `STATUS.md`, `CAVELOG.md`, `HANDOFFS.md`,
`REPOSITORIES.md`, `orchestration/current-activity.yaml`,
`docs/ARCHITECTURE.md` (new), this file (new), and
`odontoflow-backend/README.md` + `odontoflow-backend/DEVELOPMENT.md` (stale
migration/test/agent-existence claims corrected). No frontend file, code,
migration, test, `.gitignore`, environment, or secret-bearing file was edited.
The reviewed planning commit `08b12a0b` and backend commit `193d48b8` were
published normally; unrelated dirt was not staged.

## Uncertainty / things the coordinator should double-check

- The exact current full-suite backend test count is genuinely unresolved
  (three conflicting historical numbers; no suite was run by this pass).
  Recommend the next backend-touching activity re-run and record it once,
  then treat that as the new baseline.
- Whether the frontend FE3A-S1 commit (`a788df5`) should ever be published is
  an owner/integration-lead call, not a documentation call — flagged, not
  decided, here.
- The two untracked backend evidence files with token-like strings
  (`2026-09-17-chan-01-{live-route,sender}.yaml`) were not opened by this
  pass; they should be reviewed before anyone tracks or publishes them.
