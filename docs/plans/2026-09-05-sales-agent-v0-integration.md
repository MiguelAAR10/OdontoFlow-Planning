---
title: Sales Agent V0 — Integration Execution Spec
status: W4 NEEDS_PLANNING — repository harness complete; n8n lifecycle gate unavailable
date: 2026-09-05
planner: Claude Opus 5 (planning authority; no product code written)
implementer: GPT-5.6 Luna Max via Orca
evidence: docs/handoffs/discovery/2026-09-04-n8n-reception-branch-acceptance.md · ../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w1.md · ../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w2.md · ../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w3.md · ../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w4.md
---

# Sales Agent V0 — Integration Execution Spec

Planning/control-plane artifact. W1, W2, and W3 are complete; W4's
repository-backed synthetic edge is complete, while its actual n8n lifecycle
gate needs an available n8n runtime. W5/W6 remain held.

## W2 execution checkpoint — 2026-09-05

**Status:** PASS. The canonical backend checkout is `main` at
`5dda97375891fdc63d7ca96c46ae2c9c50542b69`, equal to `origin/main`, after one
normal W2 commit from base `3291787e9184c673fecceec403fc33fa347d5d8c`.
The independent full real-PostgreSQL suite is **478 passed, 0 failed, 21
warnings**. The backend worktree's pre-existing setup/documentation artifacts
outside W2 were preserved.

**Execution model:** one supervised Orca writer, GPT-5.6 Luna Max, in the
existing registered `odontoflow-backend` main worktree. No scout, parallel
writer, or new worktree. The backend lane is `api-and-interface-design`,
`postgres-best-practices`, `security-and-hardening`,
`test-driven-development`, and `verification-before-completion`; the
repo-mandated `odontoflow-engineering` guide also applies because W2 edits
`app/messaging`.

**W2 result:** risk-weighted real-PostgreSQL tests were written first and
observed RED, then the smallest route/service/schema change was implemented.
It reuses the existing organization/last-message index, preserves tenant and
one-open-conversation constraints, regenerates OpenAPI, and leaves migrations
and later agent/n8n work untouched. The shell remains the verification
authority.

The delivered contract is authenticated `GET /internal/conversations` with
tenant scope, status, exclusive `last_message_before`, deterministic ordering,
and bounded `limit` filters, plus permission-checked, idempotent and audited
`POST /internal/conversations/{conversation_id}/close`. The self-contained
handoff is `../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w2.md`.

Orca provenance: run `run_6b39d347f368`, task `task_a6e175e9a60f`, dispatch
`ctx_b571b331148a`; the worker completion was received and the worker was
released. W3, Sales Agent runtime, n8n, frontend, pricing, scheduling, and
infrastructure work were not started.

## W3 execution checkpoint — 2026-09-05

**Status:** PASS. The existing master spec remained the authority; no new
planning cycle was created. Backend `main` and `origin/main` now point to
`159cbe23769f0161d2cf4084d0020e4c30e160ed` after one normal W3 commit from
base `5dda97375891fdc63d7ca96c46ae2c9c50542b69`.

**Execution model:** one supervised Orca writer, GPT-5.6 Luna Max
(`gpt-5.6-luna`, max effort), in the existing registered
`odontoflow-backend` main worktree. No scout, extra reviewer, parallel writer,
or new worktree. The resolved `sales-agent` lane was used with the current
version-matched Orca guides and Context7 documentation for the LangChain
runtime contract.

**Orca provenance:** run `run_f669deadd6c3`, task `task_fa7d9ba85147`, dispatch
`ctx_a3372c0f4210`. The delivered vertical is the approved top-level
`sales_agent/` package, LangChain `create_agent()` without a custom
`StateGraph`, separate-database `PostgresSaver`, `thread_id = conversation_id`,
exactly seven authenticated typed gateway tools, bounded structured turns,
content-free telemetry, fake-model tests, and `POST /sales-agent/turn`.

Focused W3 verification passed **16 tests with 1 warning**. The one final full
PostgreSQL suite passed **494 tests with 20 warnings and 0 failures**. Compile
and diff checks passed; the `app/` import guard found no LangChain/LangGraph
imports, and the optional dependency isolation test passed. The technical
handoff is `../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w3.md`.
Verification is synthetic/test-only: no live model, clinic, provider,
revenue, or pricing validation was claimed. At that checkpoint, W4 was not
authorized automatically.

## W4 execution checkpoint — 2026-09-05

**Status:** NEEDS_PLANNING for the actual n8n lifecycle gate. The approved W4
definition was executed without a new planning cycle. The repository-backed
synthetic edge is complete; the backend advanced from
`159cbe23769f0161d2cf4084d0020e4c30e160ed` to
`254fe83ed756e8ad0100dac9ffde909fe8e8e0aa` (`main` equal to `origin/main`)
through the W4 artifact commit `e0b78bb` and a focused repeated-confirmation
test/handoff follow-up. The published W3 HTTP/runtime contract remains intact.

**Execution model:** one supervised Orca writer, GPT-5.6 Luna Max
(`gpt-5.6-luna`, max effort), in the existing registered
`odontoflow-backend` main worktree. No scout, extra reviewer, parallel writer,
or new worktree. The resolved `n8n` lane is
`odontoflow-engineering`, `n8n-workflow-lifecycle-official`,
`security-and-hardening`, and `verification-before-completion`.

**Orca provenance:** run `run_ed18add5892c`, task `task_cfcc6fee91bd`, dispatch
`ctx_b6c042f88c60`. The worker implemented the smallest synthetic WF-01 loop
against `provider=test`: normalization, backend-authoritative dedupe, bounded
conversation-scoped debounce, authenticated HTTP orchestration, Sales Agent
continuation, typed tools, canonical outbound persistence, and recorded E2E
evidence. The coordinator preflight found the existing backend n8n lab guide
and bootstrap script, but no n8n binary/container or exposed n8n MCP surface.
The worker therefore committed an inactive repository export at
`integrations/n8n/workflows/WF-01-sales-agent-v0.json` (`WF-01`, version
`0.1.0`) and a real HTTP/PostgreSQL harness without inventing workflow
validation or publication. The handoff is
`../odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w4.md`.

The selected W4/W3/messaging checks passed **40 tests with 1 warning**; the
coordinator reran the W4 file at **8 passed with 1 warning**. The one final
full PostgreSQL suite passed **502 tests with 20 warnings and 0 failures** in
654.23 seconds. JSON, compile, diff, and `app/` LangChain/LangGraph import
guard checks passed. The synthetic harness records inbound dedupe, resumed
conversation memory, isolated threads, canonical slot selection, explicit
confirmation, exactly-one booking, outbound persistence, handoff blocking,
and the seven-tool boundary. A second confirmation with a new provider message
ID was also verified to leave one appointment. No live model, clinic, provider,
revenue, or pricing validation was claimed.

Actual n8n `validate_workflow`, `get_workflow_details`, `test_workflow`, and
publication/version evidence remain unavailable because no n8n runtime or
workflow MCP surface exists in this environment. The export stays inactive;
the process-local debounce restart/concurrency limitation is documented, and
no Redis or direct database access was added.

W5 and W6 will not start automatically.

## 1. Current verified reality

| Fact | Value | How verified |
|---|---|---|
| Canonical backend main | `254fe83ed756e8ad0100dac9ffde909fe8e8e0aa` (`main` = `origin/main`) | git |
| W1/W2 integration | W1 complete; W2 handoff persisted at `odontoflow-backend/docs/superpowers/handoffs/2026-09-05-sales-agent-v0-w2.md` | git + handoff |
| W3 Sales Agent runtime | PASS; isolated `sales_agent/` package, separate PostgresSaver memory, seven typed tools, bounded structured turn, telemetry, and HTTP entrypoint | W3 handoff + focused/full PostgreSQL suites |
| Authorship | 4 Leonardo commits preserved; W1 forward-fix, W2 commit, and the W3 runtime commit are on main | git log |
| Merge cleanliness | **no conflicts** | W1 handoff |
| Backend suite | **502 passed / 0 failed / 20 warnings** | fresh post-W4 local PostgreSQL run, 654.23s |
| OpenAPI | **40 paths**; W2 adds only its approved internal messaging contract | generated docs + W2 handoff |
| Existing ERP schemas | **unchanged** — W2 touched only messaging router/service/schemas | git diff |
| LLM runtime in branch | **optional** — isolated top-level `sales_agent/` group; canonical `app/` remains free of LangChain/LangGraph imports | grep + pyproject + W3 import guard |
| Migration chain | strictly linear `0008→0009→…→0015` | `down_revision` inspection |
| Frontend credential flow | **none** — no `Authorization` header anywhere in `src/` | grep |
| `conversation-agent` profile | grants cancel + reschedule permissions | `scripts/issue_credential.py` |

**Two conclusions from the acceptance audit are superseded here, deliberately:**

- The audit recommended *asking the author to split `0014`/`0015`*. The frozen
  contract prefers forward fixes over rewriting contributor commits, and the
  chain is linear. **Superseded: take the chain whole under conditions (§10).**
- The audit concluded *LangChain is not needed to produce the observable
  outcome*. That remains true and is not contradicted by code. The contract
  selects LangChain for maintainability, thread-persistent state, testability
  outside the n8n canvas, and model portability — none of which the audit
  measured. **Superseded: adopt LangChain, bounded by §7's isolation rule.**

## 2. Frozen product outcome

One Sales Agent. Receives an inbound sales conversation, understands the
requested service, collects missing location/time preference, queries authorized
OdontoFlow context, offers deterministic valid slots, and creates an appointment
**only after explicit confirmation**. Later: scheduled follow-up, and explicitly
authorized commercial offers.

Never: invent prices, promotions, availability or clinical advice; write SQL;
bypass use cases; modify canonical state outside typed tools. Unsupported or
sensitive cases → `request_human_handoff`.

## 3. Chosen integration strategy

**STRATEGY A — merge preserving contributor commits, then one scoped
integration-fix commit.** Strategy B (porting a subset into new commits) is
rejected: it would discard Leonardo's authorship on 26 083 lines, re-derive code
that already passes 466 tests, and produce duplicate architecture — all cost, no
risk reduction, given the merge is conflict-free.

Execution shape:

1. Create `integration/sales-agent-v0` from `main` (`0ddd3a3`).
2. `git merge --no-ff codex/backend-n8n-pilot-20260903` — all 4 commits preserved,
   never squashed, never rebased, never force-pushed.
3. Apply **one** forward-fix commit (§11 CHANGE list). Co-authorship of the
   original commits is untouched.
4. Verify (§12). Only when green, fast-forward `main`. `main` never receives an
   unverified merge.

## 4. Target architecture

```
WhatsApp / test webhook
      │
      ▼
   n8n  ── ingress · normalize · dedupe · debounce · schedule · delivery
      │
      ├──► POST /internal/messages/inbound        (odontoflow-backend, authenticated)
      │
      ├──► POST /sales-agent/turn                 (sales_agent service — LangChain)
      │            │
      │            └──► POST /agent-tools/call    (typed tools only, 7 allowlisted)
      │
      └──► POST /internal/conversations/{id}/outbound
```

Three processes: `app` (deterministic domain authority), `sales_agent` (model
loop, no business authority), n8n (orchestration, outside the repos).
Dependency direction is one-way: `sales_agent → HTTP → app`. Never the reverse.

## 5. Memory ownership contract

Three states, physically separated:

| State | Owner | Storage | Authority |
|---|---|---|---|
| **A. Conversation / audit record** | `app` | canonical DB, Alembic-managed (`contact_identities`, `conversations`, `messages`) | Canonical record of what was said |
| **B. Agent working state** | `sales_agent` | **separate database `odontoflow_agent`**, LangGraph `PostgresSaver`, `thread_id = conversation_id` | None. Disposable |
| **C. Canonical business state** | `app` | canonical DB (`Lead`, `Service`, `Location`, `Practitioner`, availability, `Appointment`, `Patient`, economics, inventory) | The only business truth |

**A separate database — not a schema — is required.** `PostgresSaver.setup()`
creates its own tables; in the canonical `public` schema they would collide with
Alembic's exclusive schema ownership, with `tests/conftest.py`'s truncation list
and with `test_migrations`. A separate database also makes it structurally
impossible to write a foreign key from agent memory into business state, which
is the invariant "agent memory can never become business authority" expressed as
schema rather than as discipline. Dropping `odontoflow_agent` must be a no-op for
business correctness — that is an acceptance test (§15).

If `PostgresSaver` proves unusable on this stack, fall back to the officially
supported synchronous saver on the same separate database. Do **not** fall back
to in-memory state, and do **not** relocate it into the canonical database.

## 6. n8n ownership contract

**n8n owns:** WhatsApp/webhook ingress · payload normalization · burst debounce
(explicitly, because the backend does not coalesce — verified) · scheduled
follow-up triggers · provider delivery and lifecycle · retry of *transport*.

**OdontoFlow owns:** identity, tenancy, permissions, idempotency, availability,
booking, audit, conversation state, and the message record.

**Neither owns twice.** The branch's outbound *dispatcher* half
(`POST /internal/outbound/claim`, `.../result`) duplicates n8n's delivery role.
It stays in the codebase, unused: the `outbound-dispatcher` credential profile
is **not issued** in V0. Outbound *persistence*
(`POST /internal/conversations/{id}/outbound`) is used, so the transcript stays
complete.

n8n never connects to PostgreSQL directly. Ever.

## 7. LangChain runtime contract

**Location: `odontoflow-backend/sales_agent/` — a new top-level package in the
existing backend repo, run as its own process, with its own optional dependency
group.**

Rationale, from repository evidence: `docs/architecture.md` states *"No module
under `app/` imports an LLM SDK, an agent framework, or a vector store."* A
top-level sibling package keeps that literally true while avoiding a new
repository, for which no concrete deployment or dependency-isolation reason
currently exists (the agent is reachable over HTTP and needs no independent
release cadence yet). The invariant is enforced, not assumed: an **import-guard
test** asserts no module under `app/` imports `langchain`/`langgraph` — the same
sentinel style already used for the simulator's synthetic banner.

**Extraction trigger** (revisit only if hit): the agent needs an independent
deploy cadence or scaling profile, or acquires a second consumer.

Minimum runtime (mechanisms verified against the repo-local
`langchain-fundamentals` skill, not from memory):
- `create_agent()` — no custom `StateGraph`. The skill is explicit that
  `create_agent()` is the supported path and all alternatives are outdated.
- `PostgresSaver` checkpointer on `odontoflow_agent`; thread selected per invoke
  as `config={"configurable": {"thread_id": conversation_id}}`.
- Tools declared with the `@tool` decorator, each with a specific docstring and
  `Args:` block (the model's tool-selection quality depends on it), wrapping
  `POST /agent-tools/call` with the V0 credential.
- Structured final response via `response_format=<PydanticModel>`, read from
  `result["structured_response"]` — reply text + outcome + handoff flag.
- **Bounded** loop via `config={"recursion_limit": N}` per invoke, N
  configurable. Hitting the bound is a deterministic `request_human_handoff`,
  never an unbounded retry.
- Per-turn telemetry and tool-failure capture implemented as a `@wrap_tool_call`
  middleware rather than hand-rolled around each tool.
- One entrypoint: `POST /sales-agent/turn` taking `conversation_id` and the
  latest inbound message id.

**Two guard-rails the skill's examples would otherwise lead an implementer to
violate:**

1. **Do not use `MemorySaver`.** Every persistence example in the skill uses it;
   it is in-memory and would silently discard conversation state on restart. This
   plan requires `PostgresSaver` on the separate `odontoflow_agent` database (§5).
2. **Do not route human handoff through `HumanInTheLoopMiddleware`.** That
   middleware pauses the agent loop and stores the pending decision in the
   *checkpointer* — i.e. in state B, which has no authority. Handoff here is a
   canonical business fact: the `request_human_handoff` tool writes conversation
   state and an audit event in PostgreSQL under `conversations.manage`, and the
   backend then blocks every tool until an operator resumes. Keep it a tool.
   HITL middleware may be revisited later for *pre-send message approval*, which
   is a genuinely different concern.

Model ids in the skill's examples are illustrative and outdated; do not copy them
literally. The model is configuration (§7 portability), pinned at deploy time.

Context strategy: never send whole ERP state; load canonical context through
tools; keep recent turns verbatim; summarize older turns **only after a measured
threshold**, using a cheaper model, triggered by measurement not by guess; no
vector/semantic long-term memory. Thresholds are **configuration, not
constants** — the plan deliberately fixes no token numbers.

Telemetry per turn (structured log, one line): `conversation_id`, `model`,
`input_tokens`, `output_tokens`, `model_calls`, `tool_calls`, `tool_failures`,
`latency_ms`, `outcome`. No message content in telemetry.

## 8. Tool allowlist

Exactly seven, mapped to the branch's real `ToolName` values:

| V0 tool | Branch name | Permission required |
|---|---|---|
| reception context | `get_reception_context` | `services.read`, `locations.read`, `contact_appointments.read` |
| service catalog | `list_services` | `services.read` |
| locations | `list_locations` | `locations.read` |
| slot search | `query_available_slots` | `availability.read` |
| propose | `propose_appointment` | `contact_appointments.book` |
| confirm | `confirm_appointment` | `contact_appointments.book` |
| handoff | `request_human_handoff` | `conversations.manage` |

Every call additionally requires `conversations.read` (envelope).

**Dormancy is enforced by permission, not by prompt.** A new credential profile
`sales-agent-v0` grants only:
`conversations.read`, `services.read`, `locations.read`, `availability.read`,
`contact_appointments.read`, `contact_appointments.book`, `conversations.manage`,
`deliveries.create`.

It deliberately **excludes** `contact_appointments.cancel`,
`contact_appointments.reschedule`, `contact_profiles.manage`,
`practitioners.read`, `conversations.resume`, `deliveries.manage`. The existing
`conversation-agent` profile grants cancel and reschedule and is therefore
**not** used for V0.

`register_contact_profile` is not needed: `propose_appointment` calls
`ensure_contact_profile` internally under `contact_appointments.book`.
**Implementer must verify this permission derivation with a test** (§15) rather
than trusting this table.

Promotions are not exposed. No SQL/database tool is ever given to the model.

## 9. Auth compatibility decision

Keep the gate on the integration surface; restore ERP compatibility temporarily
and *visibly*.

1. In `create_app`, apply `require_authenticated_context` to
   `agent_tools_router` and `messaging_router` **only**.
2. `resolve_http_context` currently raises 401 when no gate ran. Add a narrow,
   **flag-controlled** fallback to `default_context()` for ungated ERP routers:
   `ERP_ANONYMOUS_COMPAT` (default `true` in development, **must be `false` in
   production**).
3. Retarget — never delete — the auth tests that probe via `/services`, so the
   negative/cross-tenant coverage now runs against an integration route. Add a
   test asserting that with `ERP_ANONYMOUS_COMPAT=false` the ERP routes return
   401, proving the removal path works before it is needed.

```
SECURITY_DEBT:    ERP business routes remain reachable without a credential,
                  resolving to the seeded `system` principal (all 33 permissions).
                  This restores today's `main` behaviour; it is NOT production-safe
                  and must never be described as such.
OWNER:            Miguel Arias
REMOVAL_TRIGGER:  the first of — (a) the ERP frontend ships a credential flow;
                  (b) the backend is exposed beyond localhost/pilot;
                  (c) any real clinic data is loaded.
```

No frontend authentication system is built in V0.

## 10. Migration handling decision

**Take the linear chain `0009→0015` whole.** No migration is modified, split,
renumbered or reordered. Deferred schema (`promotions`,
`appointment_reschedule_proposals`, `appointment_cancellation_proposals`,
`services.base_price`/`currency`) remains physically present **only** under all
four conditions, each of which is a test or a documented fact:

1. **Unreachable from the Sales Agent** — `promotions[]` and the price fields are
   removed from the `get_reception_context` payload (forward fix); cancel and
   reschedule are unreachable by permission (§8).
2. **No seeded value represented as real clinic data** —
   `scripts/seed_reception_demo.py` is **never run in any canonical environment**.
   Its five offers (S/99, S/399, S/699, 15 %, S/0) and all `base_price` values are
   labelled **UNVERIFIED / NON-AUTHORITATIVE** in `CANONICAL.md`. Provenance
   remains an open question for the clinic (§14).
3. **No business behaviour depends on it** — nothing in the booking path reads a
   promotion (verified: zero references outside the model and the one read).
4. **Documented** — this section plus a `CANONICAL.md` entry in the backend.

`Service.booking_mode` is the exception and is **kept**: it is a deterministic
safety rail enforced in the booking command, encoding no commercial assumption.

## 11. KEEP / CHANGE / DEFER / REJECT

**KEEP as-is:** ChannelAccount · ContactIdentity · Conversation · Message ·
outbound persistence · integration credentials · `/agent-tools/call` gateway ·
canonical catalog reads · canonical slot search (same `find_available_slots`) ·
propose/confirm (same `_book_appointment_core`) · human handoff + operator-only
resume · new permission codes · UUIDv4 idempotency tightening · `booking_mode`.

**CHANGE — the single forward-fix commit:**
1. Scoped auth gate + `ERP_ANONYMOUS_COMPAT` flag + retargeted auth tests (§9).
2. Remove `promotions[]` and `base_price`/`currency` from the
   `get_reception_context` payload.
3. Add the `sales-agent-v0` credential profile (§8).
4. `scripts/redact_message_content.py`: **refuse to run without an explicit
   `--organization-id`** (it currently redacts across all tenants — a latent
   cross-tenant bug).
5. `CANONICAL.md`: synthetic/unverified boundary for seeded prices and
   promotions; record that `consent_status` is declared but not implemented and
   must not be cited as consent compliance.

**DEFER (present, unused, with triggers):** reschedule · cancellation · outbound
claim/settle dispatcher · lab seeder · `base_price`/`currency` · template
messages (**trigger:** first WF-02 run against real WhatsApp outside the 24-hour
window — not needed while the pilot uses `provider=test`) · agent-tool rate-bucket
reclassification (**trigger:** measurement shows the 120/min mutation bucket
binds; V0 configures and measures rather than changing the auth path) · consent
wiring (**trigger:** first outbound to a contact who has not messaged first).

**REJECT for V0:** exposing `Promotion` to the agent · upselling · LangGraph
custom `StateGraph` · multi-agent runtime · graph DB · RAG · vector memory ·
recommendation engine · forecasting · OR optimization · a second workflow engine ·
a new repository.

## 12. Test strategy

Risk-weighted TDD — tests written first for the listed surfaces, not for CSS,
brand tokens or layout.

**Test-first (deterministic, real PostgreSQL, never SQLite):**
conversation query semantics · conversation close transition · auth boundaries
(both flag states) · tenant isolation · message dedupe · agent thread isolation ·
tool argument contracts · idempotency · proposal/confirmation · human handoff ·
**forbidden Promotion access** · model/tool call bounds where deterministic ·
the `app/` import-guard.

**Floor: 466.** Post-integration the suite must be ≥ 466 plus every test the
forward fixes require. Coverage is never reduced to make integration pass;
tests that must move are **retargeted, not deleted**.

Agent-runtime tests run in their own job with the optional dependency group, and
stub the model — no live model call in CI.

## 13. Minimal workstreams

| # | Workstream | Writer | Depends on |
|---|---|---|---|
| **W1** | Canonical integration: merge + forward-fix commit (§3, §11) | one | — |
| **W2** | WF-02 enablement: `GET /internal/conversations` + conversation close transition | one | W1 |
| **W3** | Sales Agent runtime: `sales_agent/` package, checkpointer, 7 tools, `/sales-agent/turn` | one | W1 |
| **W4** | n8n WF-01 wiring against `provider=test` | one | W1, W3 |
| **W5** | Engineering contract: repo-local skill + `AGENTS.md` updates (§19) | one | — (may run parallel; disjoint surface) |
| **W6** | Sales Agent operational UI | separate frontend workstream, later | W2, W3 |

W1→W2→W3→W4 is a strict chain: each changes the surface the next depends on.
W5 is the only genuinely independent write surface and is the only candidate for
a second parallel worker.

W2 and W3 are **PASS**. W4's repository-backed synthetic edge is complete, but
the activity is **NEEDS_PLANNING** for the unavailable n8n runtime lifecycle
gate. W5 and W6 remain held and must not be started automatically.

**Orchestration intent (not commands).** Default: **one writer**. Claude Opus 5
planned; GPT-5.6 Luna Max coordinates and implements; the shell holds
test/build/migration authority; Luna Max reviews and repairs when deterministic
verification fails or a real architectural contradiction appears; Terra High only
after repeated failure or unresolved high-risk ambiguity. **Never Sol.** A second
worker is justified only for W5 alongside W1. No new worktrees for convenience —
W1 already works on a dedicated integration branch.

Before acting, the coordinator must resolve the Orca executable for the current
session (preferring `ORCA_CLI_COMMAND` when the session provides it), verify the
runtime, inspect installed skills, and load the **version-matched** guides for
`orca-cli` and `orchestration` — trusting those runtime guides over any
remembered syntax, including anything implied by this plan. Plain Orca CLI covers
terminal/worktree/handoff needs; orchestration is warranted only if supervised
coordination genuinely adds value, and if used must carry real Orca
task/dispatch provenance rather than a substituted generic subagent. The retired
legacy orchestration run interface is not used.

## 14. Dependencies

- Docker container `odontoflow-db-1` on `127.0.0.1:5434`; scratch/pilot databases
  only. Never `docker compose up` from the backend directory.
- A second database `odontoflow_agent` for the checkpointer.
- Model provider credential for the agent process, from the environment. **No
  secret enters the repository**, and no token is printed.
- n8n instance able to reach the backend over HTTPS.
- **Open, blocking for any commercial claim (not for V0 booking):** provenance of
  the five seeded prices. Until the clinic confirms, they stay non-authoritative.

## 15. Acceptance criteria

V0 is accepted when all of the following are demonstrated, each by a test or a
recorded run:

1. Backend suite ≥ **466 pass**, real PostgreSQL, 0 failures.
2. ERP contract intact: 38 OpenAPI paths, none of the original 32 changed;
   Agenda/Patients/Cash/Inventory behave exactly as on `0ddd3a3`.
3. With `ERP_ANONYMOUS_COMPAT=true` the ERP frontend works unchanged; with
   `false` those routes return 401.
4. A `sales-agent-v0` credential completes the whole happy path
   (context → catalog → slots → propose → confirm) **and receives 403 on
   `propose_cancellation` and `propose_reschedule`**.
5. `get_reception_context` returns **no** `promotions` key and no price field.
6. Full WF-01 round trip on `provider=test`: inbound persisted → agent turn →
   typed tool calls → appointment created only after explicit confirmation →
   outbound persisted.
7. Double-confirm and duplicate inbound produce **exactly one** appointment.
8. Two conversations run concurrently without agent state crossing
   (`thread_id` isolation).
9. Handoff blocks every tool; only an operator credential resumes.
10. **Dropping `odontoflow_agent` loses no business state** — appointments,
    messages and audit remain complete and correct.
11. No module under `app/` imports LangChain/LangGraph (import-guard test).
12. Per-turn telemetry emitted with all nine fields, containing no message content.

## 16. First implementation vertical

**W1 — Canonical integration only.** One Luna Max writer. Not the agent, not the
routes.

Scope: create `integration/sales-agent-v0`; `--no-ff` merge of the 4 contributor
commits; the single forward-fix commit (§11 CHANGE, items 1–5); run the suite;
fast-forward `main` only when green.

Why this first: it is the one step every other workstream depends on, it has a
clean rollback boundary, and its verification is fully deterministic. It carries
integration risk only — no new-feature risk — so mixing it with W2/W3 would blur
which change caused a failure.

Definition of done: `main` contains all 4 contributor commits with authorship
intact, suite ≥ 466 green, acceptance criteria 1–5 satisfied, `CANONICAL.md`
updated, nothing force-pushed.

## 17. Expected files / surfaces

- `app/__init__.py` — scoped gate.
- `app/context.py` — flag-controlled ERP fallback.
- `app/config.py` — `ERP_ANONYMOUS_COMPAT`.
- `app/agent_tools/reception.py` — drop promotions/price from the payload.
- `scripts/issue_credential.py` — `sales-agent-v0` profile.
- `scripts/redact_message_content.py` — require `--organization-id`.
- `tests/test_authentication.py` — retargeted; new flag tests.
- `tests/` — new: forbidden-promotion, credential-profile, import-guard.
- `CANONICAL.md` (backend) — synthetic/unverified boundary.
- Later verticals: `app/messaging/router.py` (W2), `sales_agent/**` (W3),
  `pyproject.toml` optional group (W3), `AGENTS.md` + `.claude/skills/**` (W5).

## 18. Protected files / surfaces

Do not modify: any file under `alembic/versions/` · the 4 contributor commits
(never squash, rebase, amend or force-push) · `app/errors.py` · `app/db.py` ·
`app/scheduling/availability.py` · existing ERP request/response schemas ·
`app/catalog/schemas.py` · the canonical databases `odontoflow`,
`odontoflow_test`, `odontoflow_e2e` · **MediStock (read-only, outside the
workspace)** · `~/projects/portfolio/ODONTO-SMART` (brand source, read-only) ·
`odontoflow-sim`'s uncommitted V2.2 work.

## 19. Engineering contract (W5 — keep it small)

One repo-local skill plus `AGENTS.md` updates. Not a documentation project — a
single page a new contributor reads once. It must encode: API-first ·
PostgreSQL is canonical truth · domain rules live outside LLMs · typed tools only ·
no arbitrary SQL for agents · no LLM authority over price, availability or
clinical judgement · one writer per overlapping change surface · risk-weighted
TDD · preserve contributor history · no secrets in the repo · evidence before
claims · handoffs persisted in Markdown · standard commit discipline · MediStock
read-only · no horizontal infrastructure without explicit scope.

## 20. Handoff contract for Joel / CTO

**Decided, not open:** merge over port (A) · full migration chain with four
containment conditions · LangChain `create_agent` in `sales_agent/`, not a new
repo, not a custom graph · Postgres checkpointer in a **separate** database ·
seven tools, dormancy enforced by permission · promotions excluded · temporary
ERP anonymous compatibility, flagged and owned.

**Open, needs a human answer:** provenance of the five seeded prices (real clinic
tariff, or invented?). Until answered they stay non-authoritative, and no upsell
work starts.

**Standing risk accepted for V0:** ERP business routes remain unauthenticated
behind `ERP_ANONYMOUS_COMPAT`. Owner Miguel Arias; removal trigger in §9. This is
a knowing, dated trade — not a claim of safety.

**Evidence trail:** acceptance audit
`docs/handoffs/discovery/2026-09-04-n8n-reception-branch-acceptance.md` ·
W1's 471-pass verification and W2's 478-pass full PostgreSQL verification ·
this plan.

## Rollback boundary

- The merge happens on `integration/sales-agent-v0`. `main` is fast-forwarded
  only after a green suite, so a bad merge never reaches `main`.
- If a defect is found after `main` moves: `git revert -m 1 <merge-sha>` — a
  forward revert that preserves all contributor history. **Never force-push,
  never reset a published branch.**
- Schema: `alembic downgrade 0008` is permitted **only** while no real
  conversation or message rows exist. After the first real inbound message,
  forward-fix only.
- `odontoflow_agent` is independently disposable: dropping and recreating it
  loses conversation *fluency*, never business state (acceptance criterion 10).
- n8n workflows are versioned outside the repo and roll back independently.
