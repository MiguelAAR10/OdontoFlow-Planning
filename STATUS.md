---
title: OdontoFlow — Status (verified snapshot)
status: active
last_verified: 2026-09-17
authority: Repo 0 (planning) — numbers re-verified from repos at verify time
---

# Status — Verified Snapshot (2026-09-17)

## Milestone

**CURRENT_MILESTONE = M5 First Measured Value** (M0–M4 CLOSED · M5 NOW · M6 LATER)

**M5 sub-state:** M5.1 Revenue Leakage Measurability **CLOSED** (evidence:
[M5_REVENUE_LEAKAGE_BASELINE.md](M5_REVENUE_LEAKAGE_BASELINE.md)) ·
M5.2 **BLOCKED on real clinic data** (`DOMINANT_LEAKAGE = UNKNOWN`).

**Active workstream (2026-09-17):** `RECEPTION-CORE-CLOSEOUT-01` — closing
Reception / Scheduling v1 (`lead/patient -> conversation -> service ->
location -> practitioner -> deterministic availability -> proposal ->
authorized confirmation -> appointment`). Status: **NOT_DONE, planning
only**. `CHAN-01` (canonical inbound ingress verified) and `CHAN-02`
(sandbox outbound runner re-verified) both **PASS**. See
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the flow and
[`docs/handoffs/plans/2026-09-17-reception-core-closeout-01.md`](docs/handoffs/plans/2026-09-17-reception-core-closeout-01.md)
for the DONE contract. No next implementation activity is authorized — see
"Next activity" below and `orchestration/current-activity.yaml`.

**PROJECT-PUBLISH-01 (2026-09-17):** documentation-only onboarding refresh.
Corrected stale HEADs/next-activity pointers below, added
`docs/ARCHITECTURE.md`, and wrote the self-contained
[`docs/handoffs/plans/2026-09-17-project-publish-01.md`](docs/handoffs/plans/2026-09-17-project-publish-01.md).
Publication itself (committing/pushing this working tree, or the backend's
11 ahead-of-origin commits, or the frontend's blocked FE3A commit) is **not**
performed by this activity — that is a coordinator/owner decision.

## SANDBOX-REAL-MODEL-01 — INITIAL BLOCKER / PROVIDER BOUNDARY SUPERSEDED (2026-09-16)

At the initial `22e2b51` handoff, the supported runtime was only the native
OpenAI path and the required OpenAI/agent credentials were absent. Gemini was
not a supported path. The later `OPENROUTER-RUNTIME-01` activity added an
explicit OpenRouter configuration boundary and the authenticated agent
credential was resolved for the local sandbox. The real-model smoke chain
still does **not** establish a complete acceptance loop: the provider/model
configuration exists, but the observed attempts did not close the full
business flow and no additional paid smoke is authorized by this publication
activity. See the [living brief](docs/handoffs/plans/2026-09-16-sandbox-real-model-01.md)
and the subsequent real-model handoffs in this repository.

## SANDBOX-INBOUND-01 — PASS (2026-09-16)

The controlled development-only sandbox loop now composes explicit
`provider=sandbox` input → authenticated canonical inbound persistence → the
existing fake-model Sales Agent turn → sandbox outbound persistence → the
authorized loopback consumer → one durable sandbox receipt. A replay of the
same provider message creates no second inbound, agent turn, outbound, or
receipt. The fake model's same-turn booking attempt is rejected by the existing
fail-closed guard, leaving one pending proposal and zero appointments. Missing
or invalid credentials, cross-tenant ingress, and `test`/`whatsapp` sender
events fail closed. No schema, channel framework, consent mechanism, live
provider, paid model, deployment, or production write was added.

Backend commit: `22e2b51011a83fbf1e2c745aecda29b44265c71e`. Serial real-PostgreSQL validation:
**550 passed / 21 warnings**, current collection 550 versus historical 527 and
previous 545. Focused sandbox-inbound: **5 passed / 2 warnings**; focused
booking/Sales Agent/reception/messaging/outbound pack: **59 passed / 2
warnings**. See the [living brief](docs/handoffs/plans/2026-09-16-sandbox-inbound-01.md)
and [backend handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-inbound-01.md).

## SANDBOX-OUTBOUND-02 — PASS (2026-09-16)

The CTO-approved first-class `sandbox` provider now supports a controlled
development-only outbound path: persisted message → authenticated
`deliveries.manage` claim scoped to `provider=sandbox` → exact-payload receipt
at the authenticated loopback receiver → existing idempotent settlement.
`provider=test` remains non-dispatchable and the sandbox consumer cannot claim
or deliver `whatsapp` rows. The new receipt table is tenant-bound by
PostgreSQL composite FK; duplicate receiver calls replay one receipt, receiver
failure uses the existing transient retry path, and sandbox success settlement
is rejected without a matching server-owned receipt. Missing credentials,
remote/arbitrary receiver URLs, and provider fallback fail closed.

Backend commit: `872ddd2915be186fdda8f5bb195b142c49bd6843`. Final serial real-PostgreSQL suite:
**545 passed / 21 warnings**, current collection 545 versus historical 527 and
intake 535. Focused sandbox: **10 passed / 2 warnings**; disposable migration
cycle: **9 passed / 20 warnings**. No WhatsApp, inbound adapter, paid model,
deployment, consent, automatic booking, or production data was touched. See
the [living brief](docs/handoffs/plans/2026-09-16-sandbox-outbound-02.md) and
[backend handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-outbound-02.md).

## SANDBOX-OUTBOUND-01 — BLOCKED (2026-09-16)

The existing authenticated outbound queue can claim and settle only rows
whose channel provider is not `test`, while PostgreSQL permits only
`whatsapp`/`test` provider values and no server-owned local receiver binding
exists. A local consumer cannot safely distinguish a synthetic sandbox row
from live WhatsApp traffic without a new provider/routing contract. No code,
migration, consumer, receiver, or production write was added. Focused serial
real-PostgreSQL checks: **19 passed / 2 warnings**. See the
[SANDBOX-OUTBOUND-01 living brief](docs/handoffs/plans/2026-09-16-sandbox-outbound-01.md)
and [backend handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-outbound-01.md).

Required owner decision: approve a first-class local provider (with additive
schema work), an explicit server-owned local-vs-live WhatsApp binding, or a
real WhatsApp sandbox provider and credentials.

## AIRYTHM-REALITY-01 — Lead → Appointment vertical reality audit (2026-09-15)

Read-only audit (Opus planner + 4 Sonnet scouts + coordinator-run serialized
tests) after the Web-memory recovery, at backend `main @ b7f11ce` and frontend
`main @ a788df5`. **Verdict: NOT_CONNECTED** (the middle is real; both ends missing). The deterministic core, conversation
persistence, Sales Agent runtime, 7-tool gateway, availability, two-phase
proposal and canonical Appointment are real and proven against real
PostgreSQL: full suite **527 passed / 0 skipped / 21 warnings in 535.32s**
(focal 19 passed). Missing: real inbound channel (zero adapter code), real
model provider (only attempt failed `429` billing), outbound dispatcher
consumer (no process polls `/internal/outbound/claim`), and agent-turn auth.
The follow-up AGENT-CONFIRM-GUARD-01 implementation now enforces explicit
patient confirmation server-side in the booking path: a persisted later inbound
message is required before an Appointment can be created.
Control-plane correction: `deliveries.manage` + the `outbound-dispatcher`
profile already exist — the missing piece is the consumer worker. Selected
next activity: **AGENT-CONFIRM-GUARD-01** (code-enforce the booking
confirmation gate); complete. Evidence and brief:
[`docs/handoffs/plans/2026-09-15-airy-reality-01-lead-to-appointment.md`](docs/handoffs/plans/2026-09-15-airy-reality-01-lead-to-appointment.md),
`.audit/airy-reality-01/`.

## AGENT-CONFIRM-GUARD-01 — PASS (2026-09-16)

The booking confirmation command requires authoritative persisted evidence of a
later inbound `Message` in the same conversation as the proposal. A real
PostgreSQL fake-model regression rejects same-turn propose→confirm, leaves one
proposal pending, and creates zero appointments. The valid two-message flow,
cross-conversation isolation, expiry, exactly-one idempotency, and audit
behavior remain green. Focused suite: **38 passed, 2 warnings**. Full suite:
**528 passed, 21 warnings** (current collection **528**, versus the historical
**527 passed, 21 warnings** baseline). No schema, migration, protected path,
channel, deployment, or production data changed. See the backend
[technical handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-guard-01.md).

## AGENT-CONFIRM-FAIL-CLOSED-03 — PASS (2026-09-16)

The current MVP decision is enforced at the canonical booking command: a
server-authenticated `agent` principal cannot consume a pending appointment
proposal merely because a later inbound free-text message exists. The command
returns `INVALID_INPUT`, leaves the proposal pending, creates zero
appointments, and preserves the gateway audit path. Authenticated human
confirmation remains valid; no new consent semantics were invented.

Backend commit: `55f22cce3a8e50f2f18d7b2fce258cbe953ad33`. Focused
booking/Sales Agent/reception checks: **7 passed / 2 warnings**. Full serial
real-PostgreSQL suite: **529 passed / 21 warnings** in 505.22s. Current
collection is 529, versus the historical 527-pass baseline. `compileall`,
`git diff --check`, and protected-path checks passed. Ruff retains six
pre-existing import/unused-import diagnostics with no new diagnostics from
this task. See the [FAIL-CLOSED-03 living brief](docs/handoffs/plans/2026-09-16-agent-confirm-fail-closed-03.md)
and [backend handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-fail-closed-03.md).

## LOCAL-RUNTIME-SMOKE-01 — PASS (2026-09-16)

The existing PLAT-01 PostgreSQL CORE container, FastAPI `/health` and `/docs`,
and the in-process fake-model W4 runtime were verified locally with explicit
local settings. The real-PostgreSQL smoke left proposals pending and created
zero appointments, including after a later `No, thanks` message; outbound
persistence passed and synthetic `provider=test` remained intentionally
unclaimable. Focused serial checks: **4 passed / 2 warnings**. No product,
schema, test, channel, n8n, dispatcher, or production-data change was made.
See the [LOCAL-RUNTIME-SMOKE-01 living brief](docs/handoffs/plans/2026-09-16-local-runtime-smoke-01.md),
[backend handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-local-runtime-smoke-01.md),
and backend commit `021fa5297f520313f4920d6916e069f09fb640dc`.

## AGENT-TURN-AUTH-01 — PASS (2026-09-16)

`POST /sales-agent/turn` now reuses the existing PostgreSQL-backed bearer
authentication and tenant context. It accepts only the configured server-issued
`agent` principal with `conversations.read`; missing, invalid, mismatched,
cross-tenant, non-agent, and insufficient-permission callers are rejected
before the runtime. WF-01 now forwards the existing agent credential to the
turn endpoint, and local fake-model injection remains gated by a real issued
credential. The prior temporal and fail-closed booking guards, tool-level IAM,
audit, expiry, idempotency, and isolation remain intact. No migration, schema,
channel, deployment, consent mechanism, or production data changed.

Backend commit: `ad72435022054241fa27a784615b9ba8062ffecc`. Focused auth/Sales
Agent/reception/IAM/security checks: **84 passed / 2 warnings**. Full serial
real-PostgreSQL suite: **535 passed / 21 warnings** in 405.49s. Current
collection is 535, versus the historical 527-pass baseline and the pre-task
529-test collection. See the [AGENT-TURN-AUTH-01 living brief](docs/handoffs/plans/2026-09-16-agent-turn-auth-01.md)
and [backend handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-turn-auth-01.md).

## AGENT-CONFIRM-INTENT-02 — BLOCKED / NEEDS_PRODUCT_DECISION (2026-09-16)

The temporal guard does not prove affirmative consent. A real-PostgreSQL
adversarial fake-model run persisted `No, thanks` after a proposal and then
called `confirm_appointment`; it observed `('confirmed', 1, 0, 0)` for outcome,
appointments, pending proposals, and confirmation errors. The existing
`Message` and booking proposal contracts have no authoritative consent
classification or proposal-specific confirmation-message binding. No keyword
rule, model assertion, or migration was added. The diagnostic test is
intentionally uncommitted and red pending the Owner decision. See the
[blocked handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-intent-02.md)
and [living brief](docs/handoffs/plans/2026-09-16-agent-confirm-intent-02-negative-response-safety.md).

## PLAT-01 Runtime Foundation — 2026-09-07

Project-scoped read-only Supabase MCPs for the owner-supplied core and
agent-memory refs, n8n MCP environment substitution, and the isolated
`odontoflow-dev` gcloud configuration are prepared. This runtime-only update
does not reopen the closed foundation milestone, change FE3A, or start PLAT-02.
The compact contract and verification limits live in
[the PLAT-01 handoff](docs/handoffs/plans/2026-09-07-plat-01-supabase-runtime-foundation.md).

## Frontend FE1A — PASS

FE1A is complete on the canonical frontend at
`0f0531f79ea52af5bfaa03bf7df6032365581869`, pushed normally to
`origin/main`. The existing operational product now uses the verified Odonto
Smart visual foundation: semantic brand/status tokens, Fontshare Clash
Display/Satoshi, official transparent PNG logo assets, the sidebar + topbar
shell, responsive mobile drawer, and shared accessibility-focused primitives.

The implementation preserved Agenda, Patients, Cash, Inventory, Agent, Chat,
Voice gating, global patient search, New Appointment, the typed client/mock
seam, FastAPI authority, Agenda cancel/reschedule behavior, and Inventory
movement behavior. No Clerk, backend, API, business-table, Agenda V2,
Inventory V2, W4/n8n, Supabase or GCP work was started.

Fresh evidence: **91/91 frontend unit tests**, typecheck, production build,
visual harness **7/7**, and native Python Playwright exact-size evidence all
passed. The browser report confirms official logo/font/token checks,
search→Patients, New Appointment, navigation, voice-off gating, and zero
console/page errors. See the
[FE1A handoff](docs/handoffs/plans/2026-09-06-fe1a-odonto-smart-visual-foundation.md),
[ERP design contract](../odontoflow-frontend/DESIGN.md), and
`../odontoflow-frontend/.audit/fe1a-browser-verification.json`.

## Sales Agent V0 — W4 NEEDS_PLANNING

W4 (synthetic n8n WF-01 edge) delivered the repository-backed export and
deterministic HTTP/PostgreSQL harness at backend HEAD
`254fe83ed756e8ad0100dac9ffde909fe8e8e0aa`, synced with `origin/main`. The
artifact is inactive (`WF-01`, version `0.1.0`) and restricted to
`provider=test`; the harness proves normalization, bounded conversation-scoped
debounce, backend-authoritative provider-message dedupe, resumed Sales Agent
threads, isolation, canonical availability/proposal/confirmation, exactly-one
booking, outbound persistence, handoff blocking, and the seven-tool boundary.

Focused W4/W3/messaging checks passed **40 / 1 warning**; the coordinator
reran `tests/test_sales_agent_w4.py` at **8 passed / 1 warning**. The one final
full real-PostgreSQL suite passed **502 / 0 failed / 20 warnings** in 654.23s.
JSON/compile/diff checks and the `app/` LangChain/LangGraph import guard passed.
All evidence is synthetic/test-only: no live model, clinic, provider, revenue,
or pricing validation was claimed.

The actual n8n lifecycle gate is **NEEDS_PLANNING** because this environment
has no n8n binary/container or workflow MCP surface. Therefore there is no
honest `validate_workflow`, `get_workflow_details`, `test_workflow`, publish,
workflow ID, or runtime version evidence; the export remains inactive. The
handoff records the process-local debounce restart/concurrency limitation and
the next action: provision/register an isolated n8n test runtime, then run the
official lifecycle with test credentials. W5/W6 remain held.
See the [W4 handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w4.md).

## Sales Agent V0 — W3 PASS

W3 (Sales Agent Runtime) is complete on the canonical backend. The approved
runtime is isolated in the top-level optional `sales_agent/` package and uses
LangChain `create_agent()`, a separate PostgreSQL `PostgresSaver` database,
`thread_id = conversation_id`, exactly seven authenticated typed gateway tools,
bounded structured turns, content-free telemetry, fake-model tests, and
`POST /sales-agent/turn`. The canonical `app/` process has no LangChain or
LangGraph imports, and no Alembic or business-table changes were made.

The backend advanced from `5dda97375891fdc63d7ca96c46ae2c9c50542b69` to
`159cbe23769f0161d2cf4084d0020e4c30e160ed`, synced with `origin/main`. The
coordinator reran the focused W3 suite at **16 passed / 1 warning**; the one
final full real-PostgreSQL suite was **494 passed / 0 failed / 20 warnings**.
Verification is synthetic/test-only: no live model, clinic, provider, revenue,
or pricing validation was claimed. W4's repository-backed edge follows below;
its actual n8n lifecycle gate remains held.
See the [W3 handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w3.md)
and the [W2 handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w2.md).

## Sales Agent V0 — W2 PASS (prior milestone)

W2 (Conversation Listing + Close Transition) is complete on the canonical
backend. Base `3291787e9184c673fecceec403fc33fa347d5d8c` advanced to
`5dda97375891fdc63d7ca96c46ae2c9c50542b69`, which is synced with `origin/main`.
The independent full real-PostgreSQL suite is **478 passed / 0 failed / 21
warnings**; OpenAPI is reproducible with **40 paths**; Alembic remains at
`0015` with no revision added. W3 followed this milestone and is recorded
above. See the
[W2 handoff](../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w2.md).

## HEADs (verified by git, not by docs — refreshed 2026-09-17 by PROJECT-PUBLISH-01)

- **BACKEND_HEAD:** `14d918dae1c1cf954f0994f9b39841ac2ffe2969` (`main`) — 11 commits ahead of origin, 0 behind; verified fast-forward-safe to publish (backend audit packet, 2026-09-17)
- **BACKEND_REMOTE:** `git@github.com:MiguelAAR10/OdontoFlow.git` — `origin/main` = `b7f11cef9bac6bbe6eb2a0bd144a541b8032f4bc`
- **BACKEND_TESTS:** not re-run by this documentation pass. Most recent verified full run: **570 passed / 21 warnings** (`REAL-MODEL-DIAGNOSTICS-01`, 2026-09-16). Historical numbers conflict (`CHANGELOG.md` 403 at migration `0008`; an untracked GAP doc says 492) — treat the most recent dated STATUS.md entry as current, not any hardcoded number in the backend README/DEVELOPMENT.
- **MIGRATION:** `0019_sandbox_provider` (alembic `0001`–`0019`, linear chain, no branches)
- **FRONTEND_HEAD:** `a788df56d2d7f0ea5359da3227bb86fb457ca214` (`main`) — 1 commit ahead of canonical `origin/main`; **that commit is unauthorized for publication** (FE3A-S1 salvage, no in-repo gate sign-off) — see [`REPOSITORIES.md`](REPOSITORIES.md) and the PROJECT-PUBLISH-01 handoff. Worktree is also dirty (19 modified + 12 untracked paths, remainder of the same FE3A work).
- **FRONTEND_REMOTE (canonical):** `git@github.com:MiguelAAR10/odontoflow-frontend.git` — `origin/main` = `0dbfa9e6705efb5b1e6553e3841ca204533cdf97`. Local `main`'s tracked upstream is `leonardo/main`, which now 404s (repo gone) — **push to `origin` explicitly, never rely on the tracked upstream.**
- **FRONTEND_REMOTE (upstream/reference, dead):** `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` — unreachable as of 2026-09-17 (GitHub 404); local `leonardo/main` ref is stale.
- **FRONTEND_TESTS:** not re-verified by this pass; see the frontend audit packet (`.audit/project-publish-01-frontend.yaml`) for the dirty-worktree file list.
- **VOICE_HEAD / SIM_HEAD:** not re-verified by this pass (frozen, untouched siblings per `orchestration/current-activity.yaml`); last verified values (`4149a3e`, `da203a9`) are historical, see prior snapshot below.
- **PLANNING_HEAD:** `63274e1d59778d9f96ed9b69ab838a8c34db158b`, equal to `origin/main` (planning itself is not ahead) — but everything from 2026-09-07 onward, including this refresh, exists only as uncommitted/untracked files in this working tree. A fresh clone of `OdontoFlow-Planning` sees none of it; publishing this state is a coordinator decision, not performed here.
- **Legacy (medistock):** `ef2fffb` (`main`, synced) — READ ONLY, outside workspace, not re-verified this pass.

The W4 backend commits are clean and synced with `origin/main`; its worktree
retains only the pre-existing uncommitted setup/documentation artifacts noted
in the W4 handoff. Planning evidence is intentionally updated in the shared
working tree rather than committing unrelated pre-existing planning changes.

## Canonical environment (verified 2026-09-02)

| Repo | Runtime pin | Database | Test command |
|---|---|---|---|
| backend | Python `3.12` (`.python-version`), `pyproject.toml` (`odontoflow` 0.1.0) | PostgreSQL 15 in `odontoflow-db-1`, `127.0.0.1:5434`; `odontoflow_test` for pytest, `odontoflow_e2e` for the pilot harness | `.venv/bin/python -m pytest -q` |
| frontend | Node `24` (`.nvmrc`) | consumes the backend API | `npm run test` · `npm run test:e2e` · `npm run test:e2e:pilot` · `npm run typecheck` |

Bring the database up with `docker start odontoflow-db-1` (data volume
`odontoflow_odontoflow_pgdata`). Note: running `docker compose up` from
`odontoflow-backend/` derives a *different* compose project name and creates an
**empty** volume — always start the named container instead.

## Voice Integration V1 — DONE (2026-09-02)

**`odontoflow-voice` is now a canonical repo** — the voice/language adapter.
Promoted from the donor clone by `mv` so the `.git` and all **5 donor commits by
Alejandro Marcelo** survive untouched (HEAD verified `eb9a4ee`, `fsck` clean,
never squashed, never force-pushed). Upstream stays reachable as `alejandro`.

**Frontend:** the donor's assistant view is **ported, not merged** (`a967b24`).
`alejandro/feat/asistente-voz` still points at `c0f418d` and was never merged,
cherry-picked or rebased. Commit carries `Co-authored-by: Alejandro Marcelo`.

**Environment contract** — the gate is AND, not OR:

| `VITE_ENABLE_VOICE` | `VITE_USE_MOCKS` | behaviour |
|---|---|---|
| `false` (default) | anything | `/asistente` route not registered; nav item hidden; **no HTTP ever** |
| `true` | `true` (default) | page renders and explains itself; **no HTTP ever** |
| `true` | `false` | live, against `VITE_VOICE_URL` (default `http://127.0.0.1:8000`) |

Verified in a real browser, with the voice service **up and healthy**: mock mode
and disabled mode each produced **zero requests to :8000**. Agenda/Patients/
Cash/Inventory real-mode guarantees intact — pilot E2E **12/12** on a fresh DB.

**V1 writes no business state.** The voice service produces **structured
drafts** (labelled `Borrador` in the UI) and never creates `Visit`,
`ServiceExecution`, `ServiceConsumption`, `Charge`, `Payment` or
`InventoryMovement`. The backend remains the only business authority — and the
backend was **not modified** in this activity.

**Audio E2E: UNVERIFIED, not faked.** No TTS on this machine (`say` is
macOS-only; no `espeak`/`espeak-ng`/`pico2wave`/`festival`/`flite`), and
headless Chrome has no microphone. The donor's latency figures stay **their**
Apple Silicon measurements until re-measured here.

**Synthetic-catalog boundary held:** `catalogo.json` SKUs are **SYNTHETIC** and
were not promoted to canonical clinic data; its **aliases** are preserved as
**DOMAIN VOCABULARY**. Recorded in `odontoflow-voice/CANONICAL.md`.

**Single entry point for this activity (FOREMAN living brief):**
[docs/handoffs/plans/2026-09-02-voice-integration-v1.md](docs/handoffs/plans/2026-09-02-voice-integration-v1.md)
— decision-level, readable without opening code. Technical handoffs it links:
`odontoflow-frontend/.audit/voice-v1/voice-ui-port.md` ·
`odontoflow-voice/CANONICAL.md`. Credit: [CONTRIBUTIONS.md](CONTRIBUTIONS.md).

## V2.1 — Simulator promoted — DONE (2026-09-03)

**`odontoflow-sim` is now a canonical repo** — the synthetic clinic /
ground-truth simulator. Promoted from the contributor clone by `mv` so the
`.git` and all **7 commits survive untouched**: HEAD verified `b57f7bc`, `fsck`
clean, never squashed or force-pushed. Both authors confirmed **on the remote**,
not just locally: **6 Alejandro Marcelo, 1 Leonardo Panduro** (`333af34`) — a
**shared codebase**. Upstream stays reachable as `alejandro`.

**Authorship:** Alejandro Marcelo + Leonardo Panduro.
**Data classification: SYNTHETIC ONLY** — 28 patients, 4 doctors, 10 treatments,
60 appointments, 5 waitlist candidates, 3 laboratories, and behaviour
probabilities that are a **declared assumption, not a measurement**. None of it
may become canonical clinic data.

**The synthetic boundary is now structural.** Intake #2 found that the donor's
README claimed the whole interface was labelled synthetic while HEAD had removed
exactly those labels — and no test noticed. Repaired in the first canonical
commit: a permanent, non-dismissible band
(**CLÍNICA SINTÉTICA · DATOS SIMULADOS · NO SON DATOS REALES**) mounted in the
station shell's **sticky header, outside the view switch**, so it is present on
every view and at every scroll position **by construction**. No dismiss
affordance exists at all; one single text, no responsive variants.

Guarded by 10 sentinel-style tests in the spirit of the authors' own clock
sentinel: they assert the property (unconditional, outside the switch, inside
the sticky header, no dismiss control, no display toggles, no parallel shell),
not merely today's output.

**Verified after the repair:** typecheck clean · **109 tests PASS** (12 files) ·
build PASS · `npm run verificar` still *"Recorrido completo sin fallos"*,
including *"ir y volver reproduce el mismo mundo"*. **Determinism unchanged**;
the clock sentinel is intact and grew 32→33 assertions on its own by picking up
the new file.

**V2.1 is promotion + safety boundary ONLY.** No FastAPI connection, no intent
adapter, no canonical appointment states, no waitlist or laboratory tables, no
voice vocabulary, no simulator UI ported to the canonical frontend, no agents,
no WhatsApp. **Canonical backend, frontend and voice all unchanged.**

Single entry point: [docs/handoffs/plans/2026-09-03-v2-1-simulator-promotion.md](docs/handoffs/plans/2026-09-03-v2-1-simulator-promotion.md)
· Boundaries: `odontoflow-sim/CANONICAL.md`
· Map: [SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md](SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md)
· Credit: [CONTRIBUTIONS.md](CONTRIBUTIONS.md)

## External activity since the last snapshot

- **One open pull request, on the upstream/reference repo only:**
  [leonardopanduro-rgb/ODONTO-SMART-FRONT#1](https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/pull/1)
  — "Vista Asistente de voz: dictado de inventario y resumen de consulta", by
  `AlejandroMarceloCh`, opened 2026-08-15, +390/−5 over 6 files. It targets
  `leonardo/main` (`8769f12`), **not** the canonical `origin`, and depends on an
  external voice service (`AlejandroMarceloCh/odonto-voz`). Canonical `main` is
  7 commits ahead of that base, so it is not fast-forward mergeable as-is.
  **Not merged, not evaluated** — outside M5 scope; recorded so it is not lost.
- No other commits, branches or PRs appeared on any of the three canonical repos.

## Frontend real state (M4 complete)

| Screen | State |
|---|---|
| Agenda | REAL |
| Patients | REAL |
| Cash | REAL (M4.1 — charges/payments via `/charges*`, Idempotency-Key) |
| Inventory | REAL (M4.3 — products, balance by Location, entries, adjustments, kardex, transfers) |
| Chat | PROTOTYPE |
| Agent | PROTOTYPE |

## Backend state (M4 complete)

| Area | State |
|---|---|
| Inventory | REAL — Product × Location (location_id on every movement, composite FK, balance per location, consumption at visit location) |
| Transfers | REAL — atomic TRANSFER_OUT/TRANSFER_IN, one tx, idempotent (PF4), audited |
| Clinical/Economics | REAL — unchanged guarantees intact (PF1–PF4/PF7) |

## Pilot E2E (M4.4 — CLOSED)

Real journey proven end-to-end against real FastAPI + real PostgreSQL with
`VITE_USE_MOCKS=false`: Patient → Appointment (confirmed) → Visit (location
derived) → ServiceExecution → ServiceConsumption → SALIDA at the Visit Location →
other Location unchanged → Charge → partial + full Payment → overpayment rejected
via the real envelope → CashPage reflects paid/outstanding (`loadCharges`) →
InventoryPage reflects the new Location balance (`loadProductBalance`) →
Transfer (conservation + shared `transfer_id`) → kardex + location-isolated
adjustment. Evidence: `odontoflow-frontend/.audit/m4-pilot-fit/pilot-e2e.md`.
Harness (reproducible): `scripts/pilot-e2e.sh`.

Final review (DeepSeek V4 Flash, read-only, one pass): **PASS — no blockers**
(location/tenant integrity, stock authority, transfer atomicity, money
correctness, contract drift, Agenda/Patients/Cash regressions). One repair
applied in the pass: mock-mode overpayment code aligned to the real backend
(`INVALID_INPUT`).

## Tests

- **Backend:** 494 passed (verified full run 2026-09-05; W3 runtime complete; no migration added)
- **Frontend:** 91 passed / 10 files (unit) · visual harness 7/7 · exact-size browser evidence PASS · typecheck clean · build PASS

## OpenAPI paths (40, generated at backend HEAD — location-aware + W2 messaging)

`/health` · `/leads`(+`/{id}`) · `/appointments`(+`/{id}`, `/cancel`, `/reschedule`) ·
`/availability-rules` · `/schedule-blocks` · `/slots/query` · `/capabilities` ·
`/practitioners`(+`/eligible`) · `/locations` · `/services` · `/patients`(+`/{id}`) ·
`/visits`(+`/{id}`) · `/visits/{visit_id}/executions` · `/executions/{execution_id}/charges` ·
`/executions/{execution_id}/consumptions` · `/charges`(+`/{id}`, `/{charge_id}/payments`) ·
`/products`(+`/{id}`, `/entries`, `/movements`, `/adjustments`, `/balance`, `/transfers`) —
`location_id` required en entries/adjustments (body) y balance/movements (query) ·
`/agent-tools/call` · `/internal/messages/inbound` ·
`/internal/conversations/{conversation_id}/outbound` · `/internal/outbound/claim` ·
`/internal/outbound/{outbound_id}/result` · `/internal/conversations/{conversation_id}/resume` ·
`/internal/conversations` · `/internal/conversations/{conversation_id}/close`

## Latest handoffs

- FE1A Odonto Smart visual foundation + operational shell:
  `docs/handoffs/plans/2026-09-06-fe1a-odonto-smart-visual-foundation.md`
- W4 synthetic WF-01 edge: `odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w4.md`

- W3 Sales Agent runtime: `odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w3.md`
- W2 conversation listing + close: `odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w2.md`
- M4.4 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/pilot-e2e.md` (Pilot E2E + final review)
- M4.3 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/inventory-ui.md` (InventoryPage real)
- M4.1 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/cash-real.md` (CashPage real)
- M4.2 evidence: `odontoflow-backend/.audit/m4-pilot-fit/inventory-backend.md` (location-aware + transfers)
- Contract map: `odontoflow-frontend/.audit/m4-pilot-fit/frontend-contract-map.md`
- Full index: [HANDOFFS.md](HANDOFFS.md)

## Blockers

**One, and it is not technical: no real clinic operational data exists.**

Verified by live row census (2026-09-02) across every database on the instance:
`odontoflow_e2e` holds only the M4.4 pilot fixtures (`Lead E2E Piloto`,
`Bootstrap Clinic`, seeded 2026-08-17 by `.audit/accelerator/seed_e2e.py`), the
dev database `odontoflow` is at migration `0001` with zero rows, and the
frontend seeds are self-declared synthetic. Therefore `DOMINANT_LEAKAGE =
UNKNOWN` and M5.2 cannot start.

Unblocking requires a 90-day clinic export (≥ 300 appointments, ≥ 200 charges,
pseudonymous patient ids — full specification in
[M5_REVENUE_LEAKAGE_BASELINE.md §6](M5_REVENUE_LEAKAGE_BASELINE.md)).

**V2.1 blockers: none.** The promotion and visibility decisions are made and
executed. One design question remains open and it is not blocking: reconciling
the simulator's own visual language (dark workstation, monospace numerics) with
Leonardo's baseline — a conversation for the Owner and Leonardo, not a refactor.

**Real M5 validation: `BLOCKED_EXTERNAL`.** `DOMINANT_LEAKAGE = UNKNOWN`. The
simulator does not change this — it contributes **no real clinic data**, and the
baseline still needs the 90-day clinic export in
[M5_REVENUE_LEAKAGE_BASELINE.md §6](M5_REVENUE_LEAKAGE_BASELINE.md).

**Voice V1 blockers: none.** Both donor sources are canonical or ported, with
authorship intact. Two open questions remain **for the clinic**, not for
engineering: the real tariff/supply catalog, and how one visit's total maps to
per-treatment charges (`Charge` is 1:1 with a `ServiceExecution`, so a
two-treatment visit needs two charges and the donor supplies one number).
Nothing writes money until that is answered.

**Found while testing, pre-existing, NOT fixed here:** the canonical backend has
**no CORS middleware**, so a browser calling `:8010` from `:5173` is blocked
(the same request via `curl` returns 200; `OPTIONS` returns 405). That is why
the pilot E2E is a **node** harness, and it means the SPA has never been driven
in a browser against the real backend. Out of scope for V1 — the backend was not
touched. The voice service does declare CORS for `:5173`, which is why its
browser E2E worked.

Infrastructure blockers: none. Repos clean and synced; backend suite green.

Known platform limitation (recorded, not a blocker): the donor's E2E harness
`auditar.py` is **macOS-only** (shells out to `say`), so the voice
audio/transcription path is **UNVERIFIED on Linux/WSL** and the donor's latency
figures remain the author's Apple Silicon measurements, not ours.

## Next activity

**NEXT_ACTIVITY = OWNER-DECISION-REQUIRED (as of 2026-09-17).**

No artifact in this repository selects the next *implementation* activity for
the backend/agent workstream. The 2026-09-17 living brief authorized only
`CHAN-01`; both it and the already-approved `CHAN-02` are now PASS (see the
active-workstream note under "Milestone" above). The Opus closeout plan for
`RECEPTION-CORE-CLOSEOUT-01` orders, but does not approve, the following
dependency-free candidates: `CORE-01` (canonical proposal list/read/confirm/
decline), `AGENT-02` (durable human handoff), `AGENT-03` (agent cancel/
reschedule fail closed), `CHAN-03` (n8n transport-only assertions),
`CHAN-04` (provider-boundary standing tests). The coordinator/owner must
explicitly choose one and persist it in `orchestration/current-activity.yaml`
before any dispatch. See
[`docs/handoffs/plans/2026-09-17-project-publish-01.md`](docs/handoffs/plans/2026-09-17-project-publish-01.md)
for the full picture, including the separately blocked frontend publication
decision.

The prior pointer here (`V2.2 — Named Scenario Configuration`, for
`odontoflow-sim`) is **superseded as "next" but not cancelled** — the
simulator's own working tree still holds that uncommitted V2.2 work,
untouched and frozen per `orchestration/current-activity.yaml`. Resume it as
its own decision, not as a default. Full detail in
[SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md §12](SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md)
if it is picked back up.

(Not another planning/architecture/Foundation/migration phase.)
