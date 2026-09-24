---
activity_id: AGENT-02
artifact_kind: canonical_spec_activity_card
generated_on: 2026-09-23
source_seed: docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml#AGENT-02
discovery_authorized: true
discovery_spec_status: complete_after_W5_pass
spec_artifact_status: COMPLETE_AND_ACCEPTED_AFTER_W5_PASS
control_plane_lifecycle: DONE
lifecycle_state: DONE
post_review_lifecycle: DONE_AFTER_IMPLEMENTATION_VERIFICATION_AND_PUBLICATION
implementation_authorized: true
ready_to_build: false
backend_evidence_head: 02fb031c6949c1c5ea69278a9e9a33a4cbb17f72
backend_commit: 492dbb35f8c87b6f159efb540228055a62174aa7
verified_backend_remote_sha: 492dbb35f8c87b6f159efb540228055a62174aa7
closed_on: 2026-09-24
---

# AGENT-02 — Truthful AI Failure to Human Recovery — FOREMAN living brief

## Executive status

The accepted Spec passed W5, the recorded owner decisions authorized the
existing sequential SubCard graph, and AGENT-02 is now **DONE** after backend
implementation, verification, and publication. The closeout evidence below is
tied to the published backend commit and its verified `origin/main` SHA.

The artifact and the control-plane lifecycle are intentionally separate:

| Concern | Current value | Meaning |
|---|---|---|
| Spec artifact | `COMPLETE_AND_ACCEPTED_AFTER_W5_PASS` | This file contains the repaired, evidence-bounded contract accepted by W5. |
| Control-plane lifecycle | `DONE` | `orchestration/current-activity.yaml` records the completed activity. |
| Implementation | PASS | Existing typed handoff command and `ReceptionHandoff` are reused; no second recovery architecture was added. |
| Verification | PASS | Focused AGENT-02 tests: 10 passed / 2 warnings; final full serial PostgreSQL suite: 660 passed / 21 warnings. |
| Backend release | `492dbb35f8c87b6f159efb540228055a62174aa7` | Parent is the expected `02fb031c6949c1c5ea69278a9e9a33a4cbb17f72`; `origin/main` independently resolves to the release SHA. |
| Review | D1 PASS | Initial material defects were returned to the same writer and repaired; final review disposition is persisted in `task_db21f6f7c931`. |
| Owner gate | Complete | No further implementation is authorized by this closeout; wait for an explicit owner choice before starting other work. |

The prior W4 repair dispatches `ctx_a5e4672fa57c` and
`ctx_168c655bac70` failed before any file write. Their history remains
unchanged. This closeout records the completed implementation in the same
canonical Activity Card and living brief; it does not add a new Activity Card
or broaden the accepted recovery architecture.

Owner decisions applied by the completed implementation:

1. Failure scope is provider/runtime execution failure only: provider timeout,
   turn timeout, and generic provider/runtime exception mapped through the
   existing execution-failure boundary. Exclude authentication/permission,
   rate limit/request validation, `GatewayError`, invalid structured response,
   disabled integration, unrelated transport failures, and the existing
   recursion handoff path.
2. Failure handoff metadata uses `reason_code: other` and one fixed,
   content-free `reason_summary`: `Automatic assistance could not complete the
   conversation and human recovery is required.` Never persist provider body,
   exception text, stack, prompt, patient message, credential, or secret.
3. Repeated failure reuses the existing open `ReceptionHandoff` for tenant +
   conversation. Do not add whole-turn idempotency. Preserve the existing tool
   UUIDv4 contract and `ReceptionHandoff` open-row uniqueness/reuse as the
   business deduplication authority.
4. If handoff persistence fails, never fabricate recovery. Preserve the
   original public provider/runtime failure response and sanitized diagnostic
   behavior; claim a durable handoff only after the backend command commits.

## IMPLEMENTATION AND RELEASE CLOSEOUT — 2026-09-24

### Result

**PASS — AGENT-02 is implemented and published.** Only the approved runtime
failure categories (`provider_timeout`, `turn_timeout`, and `unknown`) make a
best-effort call through the authenticated `BackendGateway` to the existing
`request_human_handoff` typed tool. The backend reuses the tenant-bound open
`ReceptionHandoff`, keeps the existing public `503 / AGENT_EXECUTION_FAILED`
response and sanitized diagnostics, and writes only the fixed `other` reason
metadata. Handoff persistence failure does not fabricate a recovery claim.

The bounded product changes are `sales_agent/api.py`,
`app/agent_tools/reception.py`, and
`tests/test_sales_agent_failure_handoff.py`. The backend handoff is
`odontoflow-backend/docs/superpowers/handoffs/2026-09-24-agent-02-truthful-ai-failure-human-recovery.md`.
No schema, migration, queue, retry, fallback, frontend, n8n, or deployment
change was made.

### RED, implementation, and verification evidence

- **RED:** `task_fc9dc8c30be7` / `ctx_36fce6c0731f` first ran the new focused
  contract against the actual backend and recorded **7 failed / 0 passed**
  because failure-created recovery was missing. During the bounded repair,
  three new exclusion/reuse assertions also failed before the same writer
  repaired the behavior. Acceptance was not weakened.
- **Implementation:** Codex Luna created the tests first; one Claude Sonnet
  worker owned the implementation in `sales_agent/api.py` and
  `app/agent_tools/reception.py`. The same writer handled the bounded D1 repair
  in `task_47de38e92377`. Focused tests then passed **10 / 10**.
- **Focused verification:** `task_10023381cc73` / `ctx_7571c8fb81f2` ran
  `./.venv/bin/python -m pytest -q tests/test_sales_agent_failure_handoff.py`:
  **10 passed, 0 failed, 0 skipped, 2 warnings**.
- **Full serial PostgreSQL verification:** the same task ran
  `./.venv/bin/python -m pytest -q`: **660 passed, 0 failed, 0 skipped,
  21 warnings**. The suite ran after repair and before release; release did not
  rerun it.
- **Static review:** initial material findings about catching excluded
  `RuntimeError` categories and repeat-call reuse were repaired by the same
  writer. Final D1 disposition is **PASS** (`task_db21f6f7c931` /
  `ctx_1a241f9fd6a2`). The later receipt/audit concern was adjudicated against
  the owner contract: per-invocation UUIDv4 receipts and audit events are
  normal command provenance; the single open handoff row is business
  deduplication. No whole-turn idempotency was added.

### Backend publication

- Commit: `492dbb35f8c87b6f159efb540228055a62174aa7`
- Subject: `fix: route provider failures to human recovery`
- Expected parent: `02fb031c6949c1c5ea69278a9e9a33a4cbb17f72`
- Verified remote: `origin/main` =
  `492dbb35f8c87b6f159efb540228055a62174aa7`, independently confirmed with
  `git ls-remote`.
- Exact committed paths: the two implementation files, the focused test file,
  and the backend technical handoff named above. Staged paths matched this
  allowlist; `git diff --cached --check` passed; scoped secret scan found no
  matches in staged additions. Unrelated pre-existing backend dirt was not
  staged.
- Release task: `task_68d805a24986` / `ctx_1f312eed1847` in Run
  `run_a8f8429f181f`.

### Deviations and remaining risk

- **Narrow implementation seam:** `request_handoff` may run while the
  conversation is already `human_handoff`, solely to let the existing command
  reuse its open row. Other reception tools retain the automation-active
  guard. This bounded change was required by the repeat-failure test and was
  reviewed; it does not add another recovery path.
- **Non-blocking coverage note:** focused exclusion parametrization directly
  exercises authentication and rate-limit categories. Other excluded
  categories are protected by the explicit recovery allowlist and existing
  branch mappings. D1 found no correctness path that hands those excluded
  categories off.
- **Orca reporting deviation:** Orca marked the release Dispatch
  `agent_prompt_stalled` and revoked its reporting capability after creating
  the live backend terminal. That terminal completed the scoped commit/push;
  its output was reconciled into the Run Task result and the remote SHA was
  independently verified. This harness issue does not change product status.
- **Product blockers:** none known within the approved V1 scope. Provider-side
  effects outside the existing authenticated backend and the non-blocking
  exclusion-coverage note remain as documented limits.

## Objective and success criteria

Objective: after an authenticated provider/runtime execution failure in the
owner-approved scope, the separate Sales Agent failure boundary reaches the
existing tenant-bound human handoff command and leaves one truthful recovery
state, while preserving the established sanitized diagnostics and public error
contract.

The implementation closed A1–A7 in **TEST-FIRST ACCEPTANCE**: one
tenant-bound open handoff, existing public failure responses, no hidden
retry/fallback or fabricated outbound, no prohibited recovery data, tenant
isolation, and truthful handoff-write-failure behavior. Tests were written
first and demonstrated RED before product changes. Repeated typed calls retain
ordinary per-command UUIDv4 receipts/audit provenance; the existing open
`ReceptionHandoff` row and transition are the business deduplication
authority. Exact final test results are recorded above.

The implementation used the existing `ReceptionHandoff` domain,
authenticated API boundary, seed write surface, four owner decisions, and
one-card graph. It did not add a recovery architecture, direct database access
from the Sales Agent, provider fallback, queue/retry, whole-turn replay or
idempotency, frontend/channel work, or deployment.

## Repository reality

- Repo 0 is the planning control plane. This file remains the canonical
  living brief; `orchestration/current-activity.yaml` is the status authority
  and now says `DONE`.
- The approved seed is
  `docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml#AGENT-02`.
  W1, W2, W3, and coordinator fan-in are the read-only evidence packets used
  here. Their recorded backend evidence head is
  `02fb031c6949c1c5ea69278a9e9a33a4cbb17f72`; the published implementation
  commit and verified remote SHA are recorded in this closeout.
- The packets establish an authenticated `POST /sales-agent/turn`, a
  sanitized diagnostic/public-error path, and an existing transactional
  `request_handoff`/`run_handoff_tool` command with tenant binding, one-open-row
  uniqueness, audit, receipt, and operator resume behavior. They also establish
  that the generic failure boundary does not currently call that command.
- W1–W3 found no proof for repeat provider/runtime failure, a prior committed
  typed-tool effect followed by failure, failure-row metadata sanitization, or
  cross-tenant failure-created recovery. The owner decision fixes the
  failure-created value as `reason_code: other` with the fixed content-free
  summary recorded above; focused privacy assertions passed and the final
  serial suite passed.
- This W4 repair reads planning conventions and evidence packets only. It does
  not inspect backend source, run tests, contact a provider/live database,
  edit the seed, or change any other planning file.

## BUSINESS OUTCOME

After an authenticated provider/runtime failure, the conversation has exactly
one durable, tenant-bound open human recovery state (`ReceptionHandoff`,
normally `pending`) and the existing sanitized diagnostic/public error remains
truthful. No fabricated reply, false delivery, hidden retry, provider
fallback, or duplicate canonical mutation is introduced; an authorized
operator can use the existing resume path to resolve the handoff and reopen
the conversation. This is the approved closeout contract, not a new recovery
architecture. [seed:DC-6,AGENT-02; FI:F1-F5; W2:F11,F18]

## USER / CLINIC VALUE

The patient/contact is not silently abandoned after the model or runtime fails:
the clinic receives a recoverable canonical state instead of an opaque dead
end. Staff recovery remains a domain transition they can authorize; resume
resolves the handoff and reopens the conversation, but does not replay the
failed AI turn. No operator UI or claim worker is established by the inspected
packets, so “available” means canonical state plus the existing authorized
resume contract, not a promised new screen. [W2:F11-F13; W2:U02]

## CURRENT BEHAVIOR

- `POST /sales-agent/turn` authenticates the credential-derived tenant and
  principal, checks the agent principal and `conversations.read`, then invokes
  the runtime. [W1:E002-E004; FI:F2]
- Generic provider/runtime failure is classified into the existing sanitized
  diagnostic logger path and public error envelope (normally
  `AGENT_EXECUTION_FAILED` / HTTP 503); public details are trace identifiers,
  not provider bodies or exception text. Invalid structured output and typed
  gateway/unavailable branches retain their separate mapped responses.
  [W1:F004-F006; W1:E010-E012; W3:A3]
- The existing `request_handoff` / `run_handoff_tool` command atomically creates
  or reuses a tenant-scoped `ReceptionHandoff`, sets the conversation to
  `human_handoff`, audits, and settles its command receipt. A partial unique
  index permits only one pending/claimed row per tenant and conversation.
  [W2:F03-F05,F08-F10; W1:E019-E020]
- That durable command is reached by explicit handoff and the separate
  recursion-bound path; generic provider/runtime API failure branches do not
  call it. [W1:F010-F011; W2:F14; FI:CURRENT_HANDOFF_FLOW.current_failure_boundary]
- Provider retry, alternate-provider fallback, and whole-turn retry are absent;
  outbound enqueue occurs only after a valid turn response. Typed tool
  mutations commit in separate transactions, and `/sales-agent/turn` has no
  whole-turn idempotency contract, so duplicate effects after a later failure
  are not yet proven. [W1:F007-F009,E021-E023; W2:F16,G06; W3:A4,U1]

## DESIRED FAILURE STATE TRANSITION

| Moment | Canonical state / contract |
|---|---|
| Before failure | Authenticated tenant/principal has entered the turn; the conversation is non-closed and may be `open` or `awaiting_confirmation`; no new failure-created open handoff exists. |
| Trigger | The authenticated provider/runtime execution failure reaches the existing API translation boundary. Authentication/permission, rate limit/request validation, disabled integration, and other excluded branches do not trigger. |
| Durable result | Reuse the existing open pending/claimed row for the tenant + conversation or create exactly one tenant-bound `ReceptionHandoff` in `pending`; set `Conversation.status` to `human_handoff`; preserve the existing tool UUIDv4 contract and open-row uniqueness/reuse. [W2:F02-F05,F08-F10] |
| Public result | Preserve the existing provider/runtime failure response and trace-only details; keep sanitized diagnostics. The included failure is HTTP 503 / `AGENT_EXECUTION_FAILED`; excluded mapped branches retain their existing responses. [W1:F004-F006; W1:E010; W3:A3] |
| Side effects | No retry, alternate provider, fabricated outbound, or new canonical business mutation. Do not claim rollback of a separately committed earlier tool mutation; prove the requested duplicate-effect boundary or return it to the owner. [W1:F007-F009; FI:RISK1] |
| Later human recovery | The existing authorized resume command resolves pending/claimed handoffs and sets the conversation `open`; it does not run the Sales Agent or manipulate its separate checkpointer. [W2:F11-F12,F17; W2:G05] |

The existing recursion-bound handoff path remains an adjacent contract; this
activity closes the missing generic post-auth failure connection and must not
create a second handoff path. [W1:F010; W3:F3]

## EXACT TRIGGER BOUNDARY

The implementation boundary is the existing `sales_agent.api` failure
translation path for provider/runtime execution failures only:

1. Authentication, tenant binding, agent-principal validation, and the
   required read permission have completed; the canonical `conversation_id`
   is known.
2. Provider/runtime execution has started and a provider timeout, turn timeout,
   or generic provider/runtime exception reaches the existing
   execution-failure boundary.
3. Before returning the existing mapped error, make one bounded attempt to
   reach the existing `ReceptionHandoff` command in the authenticated tenant.
4. Do not trigger for authentication/permission, rate limit/request
   validation, `GatewayError`, invalid structured response, disabled
   integration, unrelated transport failures, or the existing recursion
   handoff path. Preserve each excluded branch's established response.
   [W1:E003-E004,E010,E013; W2:F14,F18]

## FAILURE-BRANCH DECISION (RESOLVED)

The owner selected provider/runtime execution failure only. The mapped
responses below remain the existing behavior; this decision does not add a
new response design. [W1:F004; W1:U005; W1:E006,E010; W3:E1]

| Branch at/after the authenticated turn gate | Current public behavior | Recorded decision | Test/implementation requirement |
|---|---|---|---|
| Authentication/permission, rate limit/request validation, disabled integration, or security transport rejection | Existing pre-runtime rejection; no runtime failure translation. | Exclude; no handoff. | Assert the exclusion; do not manufacture recovery from an unauthenticated or unauthorized request. [W1:E003-E004,E013] |
| Provider timeout, turn timeout, or generic provider/runtime exception mapped through the existing execution-failure boundary | HTTP 503 / `AGENT_EXECUTION_FAILED`, trace-only details. | Include. | A1–A7 apply; preserve 503 and sanitized diagnostics. [W1:F004-F006; W1:E006,E010; W3:A3] |
| Typed `GatewayError` from inbound context or an authenticated typed-tool call | Typed gateway status/code (`status_code` or default 502); trace/request identifiers only. | Exclude. | Preserve the typed response and no provider-body exposure; no failure handoff. [W1:F004,E006-E007,E010] |
| Invalid structured agent response (`ValueError`) | HTTP 502 / `INVALID_AGENT_RESPONSE`, trace-only details. | Exclude. | Preserve 502 versus the generic 503; no failure handoff. [W1:F004,E006,E010; W3:A3] |
| Separately mapped unavailable/runtime-construction or unrelated transport failure | Existing separate mapping where established; no generic execution-failure translation. | Exclude unless it is the generic execution-failure boundary described above. | Do not expand the trigger or infer a new public result. [W1:U005; W1:E006,E010] |
| Existing `GraphRecursionError` bounded handoff path | Typed handoff response from the existing recursion branch. | Exclude from this activity; keep as-is. | Do not double-write or change this path while connecting generic failure branches. [W1:F010-F011; W2:F14; W3:E7] |

The resolved table authorizes only the included provider/runtime execution
failure branch. The existing one-card graph is dispatchable in dependency
order; no new Activity Card or architecture is introduced.

## EXISTING COMPONENTS REUSED

- Authenticated `POST /sales-agent/turn`, its `ExecutionContext`, tenant
  binding, and existing error translation. [W1:E002-E004,E010]
- `SalesAgentDiagnostic` / `_record_failure` allowlisted diagnostic behavior
  and trace-only public response. [W1:E010-E012]
- `Conversation.human_handoff` automation gate and the existing
  `ReceptionHandoff` model/statuses/tenant composite keys. [W2:F01-F03,F05]
- `request_handoff` and `run_handoff_tool`: transaction, existing permission,
  audit, receipt, open-row reuse, and partial unique-index behavior.
  [W2:F04,F08-F10]
- Existing operator-only
  `POST /internal/conversations/{conversation_id}/resume`, its
  `conversations.resume` permission, and its resolve/reopen semantics.
  [W2:F11-F12,F17]
- Existing test lifecycle and synthetic auth/runtime/tenant fixtures; no live
  provider is needed for the focused contract. [W3:fixtures; W3:E1-E13]

## NON-GOALS

- No second recovery domain, diagnostic table, schema/migration, queue, cache,
  worker, claim/list/detail route, or observability platform.
- No provider/model fallback, hidden retry, whole-turn replay, or new
  `/sales-agent/turn` idempotency architecture. Preserve the existing tool
  UUIDv4 contract and use `ReceptionHandoff` open-row uniqueness/reuse for
  business deduplication.
- No frontend, operator UI, WhatsApp/live channel, n8n logic, deployment,
  hosting, or external-provider work.
- No change to appointment/proposal rules, agent booking guards, channel
  ingress, outbound delivery, or unrelated ERP modules.
- No agent-memory/checkpointer recovery or automatic resume. Human resume is
  the existing canonical command only. [W2:F11,F17; seed:non_goals]
- No widening of the public error body, no persistence of raw diagnostic
  content, and no reinterpretation of unknown provider-side effects as proven
  canonical behavior. [W1:U001-U006; W2:U01-U04]

## PRIVACY / SECURITY INVARIANTS

- Derive organization and principal only from the authenticated credential;
  never from request body or caller-supplied tenant headers. Every handoff read
  and write remains tenant-scoped and compatible with the existing composite
  foreign keys and one-open-row constraint. [W2:F03,F12; W1:E003-E004,E019]
- Preserve the existing authorization split: handoff creation uses
  `conversations.manage`; operator resume uses `conversations.resume`; the
  Sales Agent cannot resume. [W2:F04,F12; W2:E12,E22]
- Failure-created metadata is fixed to `reason_code: other` and the
  content-free `reason_summary` `Automatic assistance could not complete the
  conversation and human recovery is required.` Never persist a credential,
  provider response/body/header, exception text or stack, prompt or patient
  message text, or secret. The focused tests inspect this failure-created
  metadata and its sanitized public/diagnostic boundary.
  [W2:F02,F15; W1:E011-E012; W3:A5,U2]
- Keep public failure responses trace-only and preserve the established status
  and code; diagnostic stage/category/upstream details do not become public.
  [W1:F004-F006; W3:A3]
- No fabricated outbound or delivery state; outbound remains downstream of a
  valid turn response. [W1:E021-E022; W3:E9-E10]

## Approved implementation direction (as run)

This is an API-first connection to the existing recovery command:

1. The separate Sales Agent process invokes the authenticated `BackendGateway`
   with `POST /agent-tools/call` for the existing `request_human_handoff`
   operation. It does not directly import backend command code, open a
   cross-process database connection, or access canonical tables.
2. The request uses only the existing tool request contract: the authenticated
   tool endpoint, the existing handoff operation and arguments, and the
   existing UUIDv4 tool-key behavior. One gateway call is one authenticated
   POST; no gateway retry or whole-turn idempotency is introduced. [W1:E005,
   E007,E019; W2:F04,F08]
3. The backend's existing command remains the owner of tenant filtering,
   permission, row create/reuse, conversation transition, domain audit, and
   command receipt. Repeated failure reuses the existing open row for the
   tenant + conversation; open-row uniqueness/reuse is the business
   deduplication authority. The caller consumes the existing typed handoff
   outcome or mapped tool error; this brief defines no new response payload.
   [W1:E019; W2:F04,F08-F10]
4. The API failure translator preserves the selected branch's existing public
   status/code/details and sanitized diagnostic behavior. The handoff attempt
   is bounded and does not add a queue, retry, alternate provider, or second
   persistence path. If persistence fails before the backend command commits,
   the original provider/runtime response remains public and no durable
   handoff is claimed.

The completed product diff stayed within the seed write surface:

- `odontoflow-backend/sales_agent/api.py` — connect the provider/runtime
  execution-failure branch through the authenticated gateway boundary while
  preserving diagnostic and public-error behavior.
- `odontoflow-backend/app/agent_tools/reception.py` — only the minimal reuse or
  sanitization/idempotency seam required by the existing `ReceptionHandoff`
  command contract; no new domain or state.
- `odontoflow-backend/tests/test_sales_agent_failure_handoff.py` — the focused
  contract file named by the seed and absent at the packet evidence head.

No schema, migration, seed, frontend, deployment, or unrelated backend path
was changed. The executed graph was tests first, then one implementation
writer for the two overlapping recovery surfaces.

## Risks, conflicts, and protected surfaces

- **Boundary decision:** the seed's every-post-auth language is broader than
  the recorded provider/runtime-only scope. The resolved branch table excludes
  the broader branches; no implementation may expand it.
- **Write-failure risk:** a handoff-tool failure can be swallowed by an
  existing recursion-bound path, so a handoff response does not prove a
  committed row. Focused A7 verification confirms the original failure remains
  public and no durable recovery is claimed without commit. [W2:G04;
  W1:E019-E020; task_10023381cc73]
- **Identity and duplicate-effect risk:** the turn has no whole-turn
  idempotency field by decision; the existing tool UUIDv4 contract remains in
  force, and the existing open-row uniqueness/reuse is the business
  deduplication authority. Per-invocation receipts/audit events are normal
  command provenance. A prior separately committed typed-tool effect and
  unknown provider/checkpointer effects remain outside this activity's control.
  [W1:F007-F008,U003-U004; W2:F08-F10,G06; W3:G2-G3]
- **Metadata risk:** the owner decision fixes `reason_code: other` and one
  fixed content-free summary. Focused tests assert that provider body,
  exception text, stack, prompt, patient message, credential, and secret do not
  cross into the handoff row. [W2:F02,E08; W3:U2; task_10023381cc73]

Implementation protected the approved seed, unrelated backend/frontend source
and tests, other plans/evidence, and runtime/provider/database/credential
state. The authorized Planning lifecycle updates were limited to the existing
`orchestration/current-activity.yaml`, `CAVELOG.md`, and this living brief.

## WRITE SURFACE

The completed implementation stayed within the seed's bounded backend
surface:

- `odontoflow-backend/sales_agent/api.py` — connect the approved
  provider/runtime execution-failure branch to the existing authenticated
  handoff boundary while preserving diagnostic and public-error behavior.
- `odontoflow-backend/app/agent_tools/reception.py` — only the minimal reuse or
  sanitization seam required by the existing `ReceptionHandoff` command
  contract; no new domain, state, or whole-turn idempotency.
- `odontoflow-backend/tests/test_sales_agent_failure_handoff.py` — the missing
  focused contract file named by the seed.

No schema, migration, seed, frontend, deployment, or unrelated backend path
was changed. Planning closeout updates only the existing card, CAVELOG, and
this living brief.

## SUBCARDS

The graph is deliberately smallest useful: tests first, then one implementation
writer for the two overlapping recovery surfaces. Every SubCard below has an
explicit outcome, canonical dependencies, interfaces, write ownership,
evidence, acceptance, model class, and status.

### AGENT-02-T — failure-handoff contract tests

- `outcome:` Establish red-then-green evidence for the approved
  provider/runtime execution-failure branch, one tenant-bound handoff,
  truthful public error, metadata sanitization, repeat-failure behavior, and
  duplicate-effect boundaries.
- `canonical_dependencies:` `[]` (`depends_on: []`); W5 PASS and the recorded
  branch, metadata, repeat-failure, and write-failure decisions are
  prerequisites to dispatch.
- `interfaces:` Authenticated synthetic Sales Agent turn/runtime seams and the
  existing tenant-bound handoff fixtures; no live provider, direct database
  access from the Sales Agent, or new product interface.
- `write_ownership:` The Codex Luna test-first worker owned only
  `odontoflow-backend/tests/test_sales_agent_failure_handoff.py`; it must not
  edit implementation, seed, planning state, or CAVELOG.
- `evidence:` W3:E1-E13, W3:A1-A7, W3:G2-G5; W1:E005,E007,E019-E020;
  W2:F04-F10,G04,G06.
- `acceptance:` Tests were written first and initially failed for the missing
  behavior; focused A1–A7 acceptance passed. The existing `ReceptionHandoff`
  row is the business deduplication authority, and ordinary per-call
  UUIDv4 receipt/audit provenance remains intact.
- `model_class:` `Codex Luna`.
- `worker_role:` `backend_contract_engineer`.
- `status:` `DONE` — RED **7 failed / 0 passed**, followed by focused
  **10 passed** after implementation and bounded repair. Task
  `task_fc9dc8c30be7`; final verification `task_10023381cc73`.

### AGENT-02-I — connect failure boundary to ReceptionHandoff

- `outcome:` Connect only the recorded provider/runtime execution-failure
  branch to the existing handoff command through the authenticated API-first
  gateway boundary, while preserving public errors, diagnostics,
  tenant/permission rules, the existing UUIDv4 tool contract, open-row reuse,
  audit, receipt, and resume contracts.
- `canonical_dependencies:` `[AGENT-02-T PASS]` plus the W5 PASS and the four
  recorded owner decisions; no new dependency or architecture is introduced.
- `interfaces:` Separate Sales Agent `BackendGateway` authenticated
  `POST /agent-tools/call` for existing `request_human_handoff`; existing
  `ReceptionHandoff` command/result only. No direct cross-process import or
  database access. [W1:E005,E007,E019; W2:F04,F08]
- `write_ownership:` The single Claude Sonnet implementation writer owned only
  `odontoflow-backend/sales_agent/api.py` and
  `odontoflow-backend/app/agent_tools/reception.py` for the minimal seam;
  there is no parallel writer on either path and no schema/route/queue/worker.
- `evidence:` W1:F004,F007-F010,U003-U005,E005,E007,E019-E020; W2:F04-F10,
  F14,G04,G06; W3:A1-A7,G2-G5,U1-U4.
- `acceptance:` Focused A1–A7 tests pass for the approved provider/runtime
  branch; existing public status/code/details and sanitized diagnostics remain
  unchanged; one committed recovery transition is proven; no retry/fallback,
  fabricated outbound, duplicate canonical effect, secret-bearing metadata,
  or cross-tenant access is introduced.
- `model_class:` `Claude Sonnet` (owner-directed).
- `worker_role:` `backend_integration_engineer`.
- `status:` `DONE` — implemented after AGENT-02-T RED evidence and one bounded
  repair pass. Tasks `task_12f5cb5c280d` and `task_47de38e92377`.

## REAL DEPENDENCIES

- Seed dependency graph: `AGENT-02.dependencies: []`; this activity does not
  wait on CORE, CHAN, deployment, frontend, OpenRouter budget, or live channel
  decisions. [seed:AGENT-02]
- Existing runtime dependencies are the authenticated turn context and the
  already-shipped `ReceptionHandoff` domain, not a new service or queue.
  [W1:E002-E005,E019; W2:reuse_assessment]
- Before implementation, backend HEAD and dirty paths were revalidated at
  `02fb031c6949c1c5ea69278a9e9a33a4cbb17f72`; the resulting release commit
  and remote SHA are recorded above. [W1:backend; W2:backend_head; W3:backend]
- Owner decisions in **Executive status** and the failure-branch table are the
  fixed contract. If a test exposes a new contradiction, escalate it rather
  than introducing infrastructure or changing the accepted architecture.

## WRITE OWNERSHIP

- Planning activation and closeout: existing
  `orchestration/current-activity.yaml`, `CAVELOG.md`, and this canonical
  living brief.
- `AGENT-02-T`: Codex Luna test-first worker, focused test file only.
- `AGENT-02-I`: one Claude Sonnet implementation writer,
  `sales_agent/api.py` and `app/agent_tools/reception.py` only; no parallel
  writer on either path.
- The sequential graph is complete. No worker may add another Activity Card
  or change the accepted recovery architecture.
- The seed, frontend, runtime/provider configuration, database, credentials,
  and unrelated backend or Planning paths were not changed.

## TEST-FIRST ACCEPTANCE

The `Current status` cells below preserve the discovery-time evidence snapshot;
implementation outcomes and current PASS status are recorded in the closeout
section above.
The expected counts below distinguish the canonical handoff row, the command
receipt, and the domain audit from any generic tool-call observation. A generic
`agent_tool.called` audit may be recorded for a replay under the existing
boundary; it must not be mistaken for a second handoff domain mutation.

| ID | Contract to prove | Current status | Required focused evidence |
|---|---|---|---|
| A1 | One authenticated scoped failure leaves one `pending` tenant-bound handoff for that conversation and blocks automation. | **Absent** — no generic failure-to-row test. [FI:G1; W3:A1] | Invoke the provider/runtime execution-failure branch once; assert one row, tenant/conversation binding, `pending`, `human_handoff`, the 503 / `AGENT_EXECUTION_FAILED` public error, one committed handoff receipt/domain audit, and sanitized diagnostic. |
| A2 | A repeated failure leaves no second open handoff or duplicate canonical recovery transition. | **Partially covered** — explicit command replay/index only; repeat provider/runtime failure is untested. [FI:G2; W3:A2,G2] | Drive the second provider/runtime failure through its actual boundary and assert reuse of the existing open `ReceptionHandoff` for the tenant + conversation, no second open row, and no duplicate canonical recovery transition. Preserve the existing UUIDv4 tool-key contract; do not add whole-turn idempotency. [W1:F007-F008; W2:F04-F05,F08-F10,G06; W3:E4,E8] |
| A3 | Public provider/runtime failure remains the current content-free response. | **Covered** for synthetic generic failure only. [FI:G3; W3:A3] | Assert the exact 503 / `AGENT_EXECUTION_FAILED` status/code/details and no provider/exception content; excluded branches retain their existing responses and do not create a failure handoff. [W1:F004-F006,E010; W3:E5] |
| A4 | No hidden retry/fallback and no duplicate canonical mutation around failure. | **Partially covered** — controls exist, coupled mutation test absent. [FI:G4; W3:A4,G3] | After a deliberately prior committed typed-tool effect, assert baseline business rows plus one recovery transition only: no duplicate proposal/appointment, audit, receipt, handoff, or outbound counts, one turn attempt, no alternate provider/fallback, and no fabricated outbound. Do not claim rollback or control of provider-side effects that evidence marks unknown. [W1:F007-F008,U003-U004; W2:F08-F10,G06; W3:G2-G3] |
| A5 | Recovery metadata contains no credential, provider body, exception text, or patient message text. | **Partially covered** — logger is sanitized, failure row is not yet exercised. [FI:G5; W3:A5,U2] | Seed forbidden sentinel values at synthetic boundaries; inspect row, response, and captured diagnostic fields; allow only `reason_code: other` and the fixed summary `Automatic assistance could not complete the conversation and human recovery is required.` plus existing bounded/constant fields. [W2:F02,E08,F15; W1:E011-E012; W3:U2] |
| A6 | Failure recovery remains tenant-isolated. | **Partially covered** — general isolation exists, failure-created row test absent. [FI:G6; W3:A6] | Run equivalent authenticated failures for two tenants; assert each sees only its own handoff/metadata and cross-tenant access is rejected. [W2:F03-F04; W3:G5,U3] |
| A7 | A handoff command write failure is not reported as durable recovery without commit. | **Recorded decision** — current recursion evidence can swallow the command failure and does not prove a committed row. [W2:G04; W1:E019-E020] | Test a failure before transaction commit; assert no durable handoff/receipt/domain audit is claimed absent commit. Preserve the original provider/runtime public status/code/details and sanitized diagnostic behavior; do not add queue, retry, fallback, or a second persistence path. |

The implementation retained the existing tests and respected the recorded
absence of whole-turn idempotency. A4 is interpreted as no duplicate canonical
business effect beyond the observed baseline; per-invocation receipts and
audit events remain command provenance. A new contradiction is an escalation,
not a new retry/fallback or persistence design. [W2:F16,G06; W1:U003-U004]

### A2/A4 count and identity contract

The expected canonical result is one `ReceptionHandoff` row and one
`conversation.human_handoff_requested` transition for the actual mutation.
Each separate typed request retains its normal UUIDv4 command receipt and
audit provenance; per-invocation records do not create a second business
recovery state. An existing generic `agent_tool.called` observation may also
occur for each request or replay.
The current turn request intentionally has no whole-turn idempotency key. The
existing command's UUIDv4 tool-key contract remains unchanged, and its
tenant-plus-conversation open-row uniqueness/reuse is the business
deduplication authority for repeated failure. Do not add a new turn-level key
or idempotency layer; tests must prove the existing row reuse and canonical
transition behavior. [W1:F007-F008; W2:F08-F10,G06; W3:G2]

For A4, a prior typed-tool mutation is already committed in its own
transaction when the later failure occurs. The expected proof is no duplicate
canonical mutation beyond that observed baseline, not a claim that the prior
effect was rolled back. Exact checkpointer timing and provider-side effects are
unknown, so the test must prove the requested boundary without claiming
rollback or control of those effects. [W1:F007-F008,U003-U004; W3:G3,U1]

### Repeat failure after `human_handoff`

Repeated typed failure uses the existing open `ReceptionHandoff` for the
authenticated tenant + conversation. The existing tool UUIDv4 contract
remains unchanged, and open-row uniqueness/reuse is the business
deduplication authority; no whole-turn idempotency is added. The
`request_handoff` command alone may run while the conversation is already in
`human_handoff` so it can reuse that row; all other reception tools retain the
automation-active guard, and the recursion-bound path is unchanged.
[W2:F04-F05,F14; W3:E4,E8; task_47de38e92377; task_db21f6f7c931]

### Handoff write-failure decision

The existing handoff command's receipt claim, domain write, audit, and receipt
settlement are transaction-scoped. A command error before commit means there
is no durable recovery state to report, even if an outer path has a handoff
intent or a handoff-shaped response. Focused A7 tests force that failure and
assert the original provider/runtime public status/code/details and sanitized
diagnostic behavior remain public. No durable handoff is claimed until the
backend command commits; there is no queue, retry, fallback, or second
persistence path. [W2:G04; W1:E019-E020; task_10023381cc73]

### Recovery metadata decision

The failure-created metadata is fixed to `reason_code: other` and the exact
content-free `reason_summary` `Automatic assistance could not complete the
conversation and human recovery is required.` Tests and implementation must
never interpolate runtime diagnostics, provider text, exception text or stack,
prompt, patient content, credential, or secret. [W2:F02; W2:E08; W3:U2]

## DEFINITION OF DONE

AGENT-02 is `DONE`: W5 PASS and the four owner decisions authorized the
bounded implementation, and the following completion evidence is recorded:

- All four owner decisions are recorded, and the focused tests are written
  first and initially fail for missing behavior.
- The approved failure branches create/reuse exactly one tenant-bound open
  `ReceptionHandoff`, set `human_handoff`, and preserve the existing sanitized
  diagnostic and branch-specific public error contract.
- A1–A7 pass against the migrated PostgreSQL test lifecycle, followed by the
  full required serial backend suite with command/result evidence; no live
  provider or fabricated data is used to claim business behavior.
- No retry, fallback, fabricated outbound, duplicate canonical mutation,
  secret persistence, cross-tenant access, schema/migration, queue, frontend,
  channel, deployment, or unrelated refactor is introduced.
- The existing operator resume path remains the only human recovery transition
  and does not replay the AI turn.
- D1 final static review is PASS; the backend technical handoff and this
  existing living brief record implementation and release. No new Activity
  Card is registered.

## Execution model

Execution used the existing Orca Run `run_a8f8429f181f`. Codex Luna wrote the
focused tests first and established RED; one Claude Sonnet worker owned the
backend implementation and bounded repair; separate Codex Luna workers
performed static review and serial test verification. The dependency order
was preserved and no concurrent product writers were used. The final release
Task result was reconciled by the coordinator after Orca revoked the
Dispatch's reporting capability.

## RECOMMENDED WRITER MODEL

As executed: Codex Luna for `AGENT-02-T`, Claude Sonnet for the single
`AGENT-02-I` implementation writer, and Codex Luna for independent review and
test verification. Implementation and release are complete; this routing
does not authorize another writer.

## REVIEW CONTRACT

The independent reviewer must verify, with evidence:

1. The exact trigger table records the provider/runtime-only decision, excludes
   authentication/permission, rate limit/request validation, `GatewayError`,
   invalid structured response, disabled integration, unrelated transport
   failures, and the existing recursion-bound handoff path, while preserving
   the existing mapped responses.
2. The API-first boundary is respected: the separate Sales Agent uses the
   authenticated `BackendGateway` POST `/agent-tools/call` for the existing
   handoff operation; there is no direct cross-process import or database
   access.
3. Only the existing `ReceptionHandoff` domain is used: no new state, table,
   queue, worker, route, schema, retry, fallback, frontend, channel, or
   deployment surface.
4. Tenant derivation, permissions, one-open-row uniqueness/reuse, the existing
   UUIDv4 tool contract, audit, and operator-only resume remain intact; no
   whole-turn idempotency is introduced.
5. Public status/code/details and sanitized diagnostics remain unchanged; the
   failure row cannot contain provider body, exception text or stack, prompt,
   patient message, credential, or secret; `reason_code: other` and the fixed
   content-free summary are bounded.
6. A1–A7 are tested at the authenticated failure boundary, not inferred from
   adjacent explicit-handoff or provider-control tests. A2 proves reuse of the
   existing open row for tenant + conversation, and A4 proves no duplicate
   canonical effect without introducing whole-turn idempotency.
7. Focused and full serial test commands/results are recorded before any PASS,
   DONE, or READY claim. No evidence may come from a live provider, secret, or
   synthetic result presented as clinic truth.

## HANDOFF CONTRACT

This artifact remains the canonical living brief for the same Activity Card:

`docs/handoffs/plans/2026-09-23-agent-02-truthful-ai-failure-human-recovery.md`

The coordinator recorded W5 PASS, all four owner decisions, and final `DONE`
in `orchestration/current-activity.yaml`. The backend commit and verified
remote SHA are recorded above. The existing card is complete; do not dispatch
another implementation worker or start another Activity Card from this
closeout. Any newly discovered contradiction or privacy issue requires an
explicit owner decision and must not be resolved by adding another
architecture.

## AUTHORITY AND EVIDENCE USED

Packet aliases used throughout this brief:

- `seed` — `docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml`
- `W1` — `docs/superpowers/evidence/agent-02-failure-path-scout.yaml`
- `W2` — `docs/superpowers/evidence/agent-02-human-handoff-domain-scout.yaml`
- `W3` — `docs/superpowers/evidence/agent-02-contract-test-scout.yaml`
- `FI` — `docs/superpowers/evidence/agent-02-discovery-fan-in.yaml`

Planning conventions applied: the repository `AGENTS.md`, `CONTEXT.md`, the
project `foreman-handoff` skill, and the existing living-brief/Activity Card
shape. The accepted Spec's discovery-time source claims remain tied to the
persisted packets and fan-in; the implementation and release facts are
separately evidenced in the closeout section above and the backend handoff.

## PLANNING ACTIVATION EVIDENCE (HISTORICAL)

Read-only validation for this activation: the two existing AGENT-02 artifacts
and the repository git status/log were inspected; the persisted W5 PASS and
evidence references were preserved without re-review. No backend source, test,
provider, live database, external runtime, credential, seed, CAVELOG, or other
planning artifact was edited or run. This pass changes only
`orchestration/current-activity.yaml` and this canonical brief, and records the
four owner decisions, `READY_TO_BUILD`, and `implementation_authorized: true`.

This section records the Planning activation only. Implementation verification
and the business PASS are recorded in the closeout section above.

## DECISION AND PROGRESS LOG

- **2026-09-24 — Implementation and release closeout:** Recorded AGENT-02
  PASS, the exact backend commit and verified `origin/main` SHA, focused and
  full serial PostgreSQL results, final D1 PASS, the narrow guard exception,
  non-blocking coverage note, and Orca release-reporting deviation. Set the
  existing card to `DONE`; no new Activity Card or architecture was added.
- **2026-09-24 — Planning activation:** Recorded the four owner decisions:
  provider/runtime execution failure scope only; fixed `reason_code: other`
  and content-free summary; existing open `ReceptionHandoff` reuse with the
  UUIDv4 tool contract and no whole-turn idempotency; and preservation of the
  original sanitized provider/runtime failure when persistence does not
  commit. Set the existing card to `READY_TO_BUILD` with
  `implementation_authorized: true`; this was the authorized build gate and
  was later superseded by the completion record above.
- **2026-09-23 — W4 initial artifact:** Compiled the approved AGENT-02 seed
  and read-only W1–W3 evidence into one canonical Spec + Activity Card. No
  implementation was authorized.
- **2026-09-23 — W4 bounded repair:** Incorporated W5 findings from
  `msg_62511247ddec` and `msg_cf584a56667d`; separated Spec artifact status
  from control-plane lifecycle, made the API-first boundary explicit, added
  branch/write-failure/count/guard/reason-code gates, and made every SubCard
  complete. At that point the lifecycle remained `NEEDS_PRODUCT_DISCOVERY`
  pending W5 PASS; no control-plane or CAVELOG change was made.

## NEXT APPROVAL / NEXT STEP

The existing card is `DONE`; no implementation step remains in this
Activity Card. Wait for an explicit owner choice before registering or
starting any other work. No new Activity Card, architecture, seed, or
unrelated Planning artifact is authorized by this closeout.
