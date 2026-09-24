---
activity_id: AGENT-02
artifact_kind: canonical_spec_activity_card
generated_on: 2026-09-23
source_seed: docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml#AGENT-02
discovery_authorized: true
discovery_spec_status: complete_pending_W5_review
spec_artifact_status: COMPLETE_PENDING_W5_REVIEW
control_plane_lifecycle: NEEDS_PRODUCT_DISCOVERY
lifecycle_state: NEEDS_PRODUCT_DISCOVERY
post_review_lifecycle: BLOCKED_OWNER_DECISION_ONLY_AFTER_W5_PASS
implementation_authorized: false
ready_to_build: false
backend_evidence_head: 02fb031c6949c1c5ea69278a9e9a33a4cbb17f72
---

# AGENT-02 — Truthful AI Failure to Human Recovery — FOREMAN living brief

## Executive status

The Spec/Activity Card artifact is complete as a bounded W4 document repair,
but it is pending W5 review. This artifact is not a W5 PASS and does not
authorize implementation.

The artifact and the control-plane lifecycle are intentionally separate:

| Concern | Current value | Meaning |
|---|---|---|
| Spec artifact | `COMPLETE_PENDING_W5_REVIEW` | This file contains the repaired, evidence-bounded contract. |
| Control-plane lifecycle | `NEEDS_PRODUCT_DISCOVERY` | `orchestration/current-activity.yaml` remains in this state and is not edited by this pass. |
| Implementation | `implementation_authorized: false` | No SubCard may be dispatched or implemented. |
| Build readiness | `ready_to_build: false` | This artifact is not `READY_TO_BUILD`. |
| After review | `BLOCKED_OWNER_DECISION` only after W5 PASS | If owner gates remain, the coordinator may make that lifecycle transition only after W5 records PASS. |

The prior W4 repair dispatches `ctx_a5e4672fa57c` and
`ctx_168c655bac70` failed before any file write. This pass is the bounded
repair of the one canonical file and incorporates the W5 findings recorded in
`msg_62511247ddec` and `msg_cf584a56667d`.

Owner decisions required before any future SubCard dispatch:

- Choose the failure boundary: provider/runtime-only, or the seed wording of
  every post-auth failure. The branch table below preserves both options and
  does not silently broaden the contract.
- Select one existing seven-value `reason_code` and one fixed, content-free
  `reason_summary`; this brief does not list or invent literals.
- Decide how a failure-boundary invocation obtains the existing handoff
  command's idempotency identity, and what evidence is sufficient for no
  duplicate tool effect after a prior committed typed-tool mutation.
- Approve the expected public result when the handoff command write fails;
  durable recovery cannot be claimed without a committed row.
- Decide whether a second failure attempt that reaches `human_handoff` is
  tested as an automation-guard rejection or as a handoff-row reuse path.

## Objective and success criteria

Objective: after an authenticated, owner-approved provider/runtime failure, the
separate Sales Agent failure boundary reaches the existing tenant-bound human
handoff command and leaves one truthful recovery state, while preserving the
established sanitized diagnostics and public error contract.

Success criteria for the future implementation are A1–A7 in
**TEST-FIRST ACCEPTANCE**: one tenant-bound open handoff, no duplicate
handoff/receipt/domain-audit effect, unchanged branch-specific public errors,
no hidden retry/fallback or fabricated outbound, no prohibited recovery data,
tenant isolation, and an explicit handoff-write-failure outcome. The focused
tests must be written first and initially fail for the missing behavior; the
full required serial suite and exact results must be recorded before any PASS,
DONE, or READY claim.

Constraints are the existing `ReceptionHandoff` domain, the authenticated API
boundary, the seed write surface, and the owner gates above. Exclusions are a
new recovery architecture, direct database access from the Sales Agent,
provider fallback, queue/retry, whole-turn replay, frontend/channel work, and
any control-plane, seed, or CAVELOG change.

## Repository reality

- Repo 0 is the planning control plane. The canonical artifact is this file;
  `orchestration/current-activity.yaml` remains the status authority and
  currently says `NEEDS_PRODUCT_DISCOVERY`.
- The approved seed is
  `docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml#AGENT-02`.
  W1, W2, W3, and coordinator fan-in are the read-only evidence packets used
  here. Their recorded backend evidence head is
  `02fb031c6949c1c5ea69278a9e9a33a4cbb17f72`; future implementation must
  revalidate it.
- The packets establish an authenticated `POST /sales-agent/turn`, a
  sanitized diagnostic/public-error path, and an existing transactional
  `request_handoff`/`run_handoff_tool` command with tenant binding, one-open-row
  uniqueness, audit, receipt, and operator resume behavior. They also establish
  that the generic failure boundary does not currently call that command.
- W1–W3 found no proof for repeat provider/runtime failure, a prior committed
  typed-tool effect followed by failure, failure-row metadata sanitization, or
  cross-tenant failure-created recovery. They also found no literal list for
  the seven-value `reason_code` set in the packet evidence.
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
| Trigger | The owner-approved post-auth branch reaches the existing API translation boundary. Pre-auth rejection is excluded. |
| Durable result | Reuse the existing pending/claimed row or create exactly one tenant-bound `ReceptionHandoff` in `pending`; set `Conversation.status` to `human_handoff`; retain existing audit/idempotency conventions. [W2:F02-F05,F08-F10] |
| Public result | Preserve the existing branch status/code and trace-only details; keep sanitized diagnostics. Generic provider/runtime failure is HTTP 503 / `AGENT_EXECUTION_FAILED`; invalid structured response is HTTP 502 / `INVALID_AGENT_RESPONSE`. [W1:F004-F006; W1:E010; W3:A3] |
| Side effects | No retry, alternate provider, fabricated outbound, or new canonical business mutation. Do not claim rollback of a separately committed earlier tool mutation; prove the requested duplicate-effect boundary or return it to the owner. [W1:F007-F009; FI:RISK1] |
| Later human recovery | The existing authorized resume command resolves pending/claimed handoffs and sets the conversation `open`; it does not run the Sales Agent or manipulate its separate checkpointer. [W2:F11-F12,F17; W2:G05] |

The existing recursion-bound handoff path remains an adjacent contract; this
activity closes the missing generic post-auth failure connection and must not
create a second handoff path. [W1:F010; W3:F3]

## EXACT TRIGGER BOUNDARY

The implementation boundary is the existing `sales_agent.api` failure
translation path, subject to the owner choice in the branch table:

1. Authentication, tenant binding, agent-principal validation, and the
   required read permission have completed; the canonical `conversation_id`
   is known.
2. Runtime execution or the owner-approved set of post-auth failure branches
   has started or reached the API boundary.
3. Before returning the existing mapped error, make one bounded attempt to
   reach the existing `ReceptionHandoff` command in the authenticated tenant.
4. Do not trigger for authentication, permission, rate-limit, disabled
   integration, request-body, or other pre-runtime transport rejection. Do not
   reclassify inbound/ingress or outbound transport work into this card unless
   the owner selects the seed's every-post-auth-failure option.
   [W1:E003-E004,E010,E013; W2:F14,F18]

## FAILURE-BRANCH OWNER GATE

The seed says “every post-auth failure,” while the narrowest source-backed
interpretation is provider/runtime execution only. The owner must select one
option before implementation; this repair does not silently decide between
them. The mapped responses below are the current evidence, not new response
design. [W1:F004; W1:U005; W1:E006,E010; W3:E1]

| Branch at/after the authenticated turn gate | Current public behavior | Provider/runtime-only option | Seed “every post-auth failure” option | Test/decision requirement |
|---|---|---|---|---|
| Authentication, permission, rate-limit, disabled integration, request-body, or security transport rejection | Existing pre-runtime rejection; no runtime failure translation. | Exclude; no handoff. | Exclude; “post-auth” has not begun. | Assert the auth/transport exclusion; do not manufacture recovery from an unauthenticated or unauthorized request. [W1:E003-E004,E013] |
| Provider timeout, turn timeout, or generic runtime/provider exception | HTTP 503 / `AGENT_EXECUTION_FAILED`, trace-only details. | Include. | Include. | A1–A7 apply; preserve 503 and sanitized diagnostics. [W1:F004-F006; W1:E006,E010; W3:A3] |
| Typed `GatewayError` from inbound context or an authenticated typed-tool call | Typed gateway status/code (`status_code` or default 502); trace/request identifiers only. | Exclude as gateway/transport. | Include as a post-auth failure, retaining the typed response. | Record the owner choice and branch-specific status/code; no provider-body exposure. [W1:F004,E006-E007,E010] |
| Invalid structured agent response (`ValueError`) | HTTP 502 / `INVALID_AGENT_RESPONSE`, trace-only details. | Exclude as response validation. | Include as a post-auth failure, retaining 502. | Explicitly test 502 versus the generic 503; do not flatten the branches. [W1:F004,E006,E010; W3:A3] |
| `AgentUnavailableError` during runtime construction | HTTP 503 / `AGENT_UNAVAILABLE`, trace-only details. | Exclude as unavailable/runtime construction. | Include as a post-auth failure, retaining its mapped response. | Record inclusion and recovery expectation before dispatch. [W1:E006,E010] |
| Other lazy runtime-construction exception | Public mapping is not established by the packet evidence. | Exclude unless separately mapped. | Owner must choose inclusion and expected public result; do not infer one. | Preserve the unknown and add a test only after the owner-approved result exists. [W1:U005; W1:E006,E010] |
| Existing `GraphRecursionError` bounded handoff path | Typed handoff response from the existing recursion branch. | Keep as-is; it is not the generic provider/runtime path. | Keep as-is; it is an adjacent existing contract. | Do not double-write or change this path while connecting generic failure branches. [W1:F010-F011; W2:F14; W3:E7] |

The table is a decision gate, not permission to implement all rows. Until the
owner selects the boundary, the effective control-plane state remains
`NEEDS_PRODUCT_DISCOVERY` and neither SubCard is dispatchable.

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
  `/sales-agent/turn` idempotency architecture. Existing command idempotency
  must be reused only where the owner-approved boundary permits it.
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
- Failure-created `reason_code` must be an existing closed-set value and
  `reason_summary` must be fixed/allowlisted and bounded. Never persist a
  credential, provider response/body/header, exception text or stack, prompt or
  patient message text, or secret. The current explicit handoff field is
  caller-provided, so the failure path needs a direct sanitization assertion.
  [W2:F02,F15; W1:E011-E012; W3:A5,U2]
- Keep public failure responses trace-only and preserve the established status
  and code; diagnostic stage/category/upstream details do not become public.
  [W1:F004-F006; W3:A3]
- No fabricated outbound or delivery state; outbound remains downstream of a
  valid turn response. [W1:E021-E022; W3:E9-E10]

## What we will build and how

This is an API-first connection to the existing recovery command:

1. The separate Sales Agent process invokes the authenticated `BackendGateway`
   with `POST /agent-tools/call` for the existing `request_human_handoff`
   operation. It does not directly import backend command code, open a
   cross-process database connection, or access canonical tables.
2. The request uses only the existing tool request/idempotency contract: the
   authenticated tool endpoint, the existing handoff operation and arguments,
   and the existing mutation idempotency behavior. One gateway call is one
   authenticated POST; no gateway retry is introduced. [W1:E005,E007,E019;
   W2:F04,F08]
3. The backend's existing command remains the owner of tenant filtering,
   permission, row create/reuse, conversation transition, domain audit, and
   command receipt. The caller consumes the existing typed handoff outcome or
   mapped tool error; this brief defines no new response payload. [W1:E019;
   W2:F04,F08-F10]
4. The API failure translator preserves the selected branch's existing public
   status/code/details and sanitized diagnostic behavior. The handoff attempt
   is bounded and does not add a queue, retry, alternate provider, or second
   persistence path.

Conceptual future file scope is limited to the seed surface:

- `odontoflow-backend/sales_agent/api.py` — connect the owner-approved
  post-auth failure branches through the authenticated gateway boundary while
  preserving diagnostic and public-error behavior.
- `odontoflow-backend/app/agent_tools/reception.py` — only the minimal reuse or
  sanitization/idempotency seam required by the existing `ReceptionHandoff`
  command contract; no new domain or state.
- `odontoflow-backend/tests/test_sales_agent_failure_handoff.py` — the focused
  contract file named by the seed and absent at the packet evidence head.

No schema, migration, planning-state, seed, frontend, deployment, or
unrelated backend path is authorized by this card. The smallest useful graph
is tests first, then one implementation writer for the two overlapping
recovery surfaces.

## Risks, conflicts, and protected surfaces

- **Boundary conflict:** the seed's every-post-auth language is broader than
  the provider/runtime-only interpretation. The branch table is unresolved;
  no implementation or PASS may assume one.
- **Write-failure risk:** a handoff-tool failure can be swallowed by an
  existing recursion-bound path, so a handoff response does not prove a
  committed row. The test-first gate below forbids claiming durable recovery
  without commit. [W2:G04; W1:E019-E020]
- **Identity and duplicate-effect risk:** the turn has no idempotency field;
  the existing command has its own key/receipt behavior, and a repeated turn
  may be blocked before it reaches row reuse. A prior separately committed
  typed-tool effect and unknown provider/checkpointer effects remain unresolved.
  [W1:F007-F008,U003-U004; W2:F08-F10,G06; W3:G2-G3]
- **Metadata risk:** the packet says `reason_code` is a seven-value closed set
  but does not list the literals. The owner must select one existing value and
  one fixed content-free summary before implementation; W4 does not invent
  either. [W2:F02,E08; W3:U2]

Protected surfaces for this bounded pass are
`orchestration/current-activity.yaml`, `CAVELOG.md`, the approved seed,
backend/frontend source and tests, other plans/evidence, and all runtime,
provider, database, credential, and publication state. Only this canonical
Markdown file may change.

## WRITE SURFACE

This W4 task writes only this planning artifact. Future implementation, after
an owner sets `implementation_authorized: true` and W5 has passed, is limited
to the seed's surface:

- `odontoflow-backend/sales_agent/api.py` — connect the approved post-auth
  failure branches to the existing authenticated handoff boundary while
  preserving diagnostic and public-error behavior.
- `odontoflow-backend/app/agent_tools/reception.py` — only the minimal reuse or
  sanitization/idempotency seam required by the existing `ReceptionHandoff`
  command contract; no new domain or state.
- `odontoflow-backend/tests/test_sales_agent_failure_handoff.py` — the missing
  focused contract file named by the seed.

No schema, migration, planning-state, seed, frontend, deployment, or unrelated
backend path is authorized by this card.

## SUBCARDS

The graph is deliberately smallest useful: tests first, then one implementation
writer for the two overlapping recovery surfaces. Every SubCard below has an
explicit outcome, canonical dependencies, interfaces, write ownership,
evidence, acceptance, model class, and status.

### AGENT-02-T — failure-handoff contract tests

- `outcome:` Establish red-then-green evidence for the selected post-auth
  failure branches, one tenant-bound handoff, truthful public error, metadata
  sanitization, repeat-failure behavior, and duplicate-effect boundaries.
- `canonical_dependencies:` `[]` (`depends_on: []`); owner branch/key/reason
  gates and W5 PASS are prerequisites to dispatch, not guessed dependencies.
- `interfaces:` Authenticated synthetic Sales Agent turn/runtime seams and the
  existing tenant-bound handoff fixtures; no live provider, direct database
  access from the Sales Agent, or new product interface.
- `write_ownership:` Future writer owns only
  `odontoflow-backend/tests/test_sales_agent_failure_handoff.py`; it must not
  edit implementation, seed, planning state, or CAVELOG.
- `evidence:` W3:E1-E13, W3:A1-A7, W3:G2-G5; W1:E005,E007,E019-E020;
  W2:F04-F10,G04,G06.
- `acceptance:` Write tests first and initially fail for the missing behavior;
  cover A1–A7, the selected failure-branch table, one handoff/receipt/domain
  audit versus duplicate counts, the human-handoff guard outcome, the
  owner-approved reason code/summary, tenant isolation, and the committed
  versus uncommitted handoff-write outcome.
- `model_class:` `Codex Luna`.
- `worker_role:` `backend_contract_engineer`.
- `status:` `NOT_DISPATCHED` — blocked pending W5 PASS, owner gates, and
  `implementation_authorized: true`.

### AGENT-02-I — connect failure boundary to ReceptionHandoff

- `outcome:` Connect only the owner-approved failure branches to the existing
  handoff command through the authenticated API-first gateway boundary, while
  preserving public errors, diagnostics, tenant/permission rules, command
  idempotency, audit, receipt, and resume contracts.
- `canonical_dependencies:` `[AGENT-02-T PASS]` plus W5 PASS, the selected
  branch scope, key identity, reason code/summary, repeat-guard outcome, and
  handoff-write-failure outcome; no dependency may be invented around an
  unresolved owner decision.
- `interfaces:` Separate Sales Agent `BackendGateway` authenticated
  `POST /agent-tools/call` for existing `request_human_handoff`; existing
  `ReceptionHandoff` command/result only. No direct cross-process import or
  database access. [W1:E005,E007,E019; W2:F04,F08]
- `write_ownership:` Future writer owns only
  `odontoflow-backend/sales_agent/api.py` and
  `odontoflow-backend/app/agent_tools/reception.py` for the minimal seam;
  there is no parallel writer on either path and no schema/route/queue/worker.
- `evidence:` W1:F004,F007-F010,U003-U005,E005,E007,E019-E020; W2:F04-F10,
  F14,G04,G06; W3:A1-A7,G2-G5,U1-U4.
- `acceptance:` Focused A1–A7 tests pass for the selected branches; the
  existing public status/code/details and sanitized diagnostics remain
  unchanged; one committed recovery transition is proven; no retry/fallback,
  fabricated outbound, duplicate canonical effect, secret-bearing metadata,
  or cross-tenant access is introduced.
- `model_class:` `Codex Luna`.
- `worker_role:` `backend_integration_engineer`.
- `status:` `NOT_DISPATCHED` — depends on AGENT-02-T and all owner/W5 gates;
  implementation remains unauthorized.

## REAL DEPENDENCIES

- Seed dependency graph: `AGENT-02.dependencies: []`; this activity does not
  wait on CORE, CHAN, deployment, frontend, OpenRouter budget, or live channel
  decisions. [seed:AGENT-02]
- Existing runtime dependencies are the authenticated turn context and the
  already-shipped `ReceptionHandoff` domain, not a new service or queue.
  [W1:E002-E005,E019; W2:reuse_assessment]
- Before future writing, revalidate the backend HEAD and dirty paths; the
  packets are read-only evidence captured at
  `02fb031c6949c1c5ea69278a9e9a33a4cbb17f72`, not a promise that the worktree
  remains unchanged. [W1:backend; W2:backend_head; W3:backend]
- Owner decisions in **Executive status** and the failure-branch table are
  gates, not dependencies to be guessed around. If a test exposes a
  contradiction, stop at that decision rather than introducing infrastructure.

## WRITE OWNERSHIP

- W4 / planning agent: this one canonical Markdown artifact only.
- Future `AGENT-02-T`: one test writer, test file only.
- Future `AGENT-02-I`: one backend integration writer,
  `sales_agent/api.py` and `app/agent_tools/reception.py` only; no parallel
  writer on either path.
- Coordinator/owner: after W5 PASS, resolve the gates and explicitly authorize
  implementation. No worker may infer authorization from this spec or mark it
  `READY_TO_BUILD`.
- Repo 0 control-plane files, CAVELOG, the seed, frontend, runtime/provider,
  database, credentials, publication, and unrelated evidence remain untouched.

## TEST-FIRST ACCEPTANCE

The fan-in status describes current evidence, not a PASS for the future card.
The expected counts below distinguish the canonical handoff row, the command
receipt, and the domain audit from any generic tool-call observation. A generic
`agent_tool.called` audit may be recorded for a replay under the existing
boundary; it must not be mistaken for a second handoff domain mutation.

| ID | Contract to prove | Current status | Required focused evidence |
|---|---|---|---|
| A1 | One authenticated scoped failure leaves one `pending` tenant-bound handoff for that conversation and blocks automation. | **Absent** — no generic failure-to-row test. [FI:G1; W3:A1] | Invoke the owner-approved post-auth failure once; assert one row, tenant/conversation binding, `pending`, `human_handoff`, the selected public error, one committed handoff receipt/domain audit, and sanitized diagnostic. |
| A2 | A repeated failure leaves no second open handoff or duplicate canonical recovery transition. | **Partially covered** — explicit command replay/index only; repeat provider/runtime failure is untested. [FI:G2; W3:A2,G2] | Drive the second attempt through its actual boundary. If it reaches the writer, assert exactly one open handoff, one executed/replayed `conversations.request_handoff` receipt, and one `conversation.human_handoff_requested` domain audit for the transition, with no duplicate; if the human-handoff guard blocks it first, assert that outcome and record the owner decision because row reuse was not exercised. Resolve the key-identity gate before claiming PASS. [W1:F007-F008; W2:F04-F05,F08-F10,G06; W3:E4,E8] |
| A3 | Public provider/runtime failure remains the current content-free response. | **Covered** for synthetic generic failure only. [FI:G3; W3:A3] | Assert the exact selected branch status/code/details and no provider/exception content: generic provider/runtime is 503 / `AGENT_EXECUTION_FAILED`, invalid structured response is 502 / `INVALID_AGENT_RESPONSE`; retain branch-specific checks where the owner includes them. [W1:F004-F006,E010; W3:E5] |
| A4 | No hidden retry/fallback and no duplicate canonical mutation around failure. | **Partially covered** — controls exist, coupled mutation test absent. [FI:G4; W3:A4,G3] | After a deliberately prior committed typed-tool effect, assert baseline business rows plus one recovery transition only: no duplicate proposal/appointment, audit, receipt, handoff, or outbound counts, one turn attempt, no alternate provider/fallback, and no fabricated outbound. Do not claim rollback or control of provider-side effects that evidence marks unknown. [W1:F007-F008,U003-U004; W2:F08-F10,G06; W3:G2-G3] |
| A5 | Recovery metadata contains no credential, provider body, exception text, or patient message text. | **Partially covered** — logger is sanitized, failure row is not yet exercised. [FI:G5; W3:A5,U2] | Seed forbidden sentinel values at synthetic boundaries; inspect row, response, and captured diagnostic fields; allow only the owner-approved existing bounded/constant fields, including the selected closed-set reason code and fixed summary. [W2:F02,E08,F15; W1:E011-E012; W3:U2] |
| A6 | Failure recovery remains tenant-isolated. | **Partially covered** — general isolation exists, failure-created row test absent. [FI:G6; W3:A6] | Run equivalent authenticated failures for two tenants; assert each sees only its own handoff/metadata and cross-tenant access is rejected. [W2:F03-F04; W3:G5,U3] |
| A7 | A handoff command write failure is not reported as durable recovery without commit. | **Owner gate** — current recursion evidence can swallow the command failure and does not prove a committed row. [W2:G04; W1:E019-E020] | Test a failure before transaction commit; assert no durable handoff/receipt/domain audit is claimed absent commit. Preserve the originating established public error status/code/details unless the owner explicitly approves a different expected outcome; do not add queue, retry, fallback, or a second persistence path. |

The existing tests must remain green; no acceptance item may be waived because
the implementation is small. A4 is an owner gate if the current lack of
whole-turn idempotency prevents a truthful proof; the answer is escalation,
not a new retry/fallback or persistence design. [W2:F16,G06; W1:U003-U004]

### A2/A4 count and identity gate

The expected canonical result is one `ReceptionHandoff` row, one executed
command receipt/outcome for the recovery transition, and one
`conversation.human_handoff_requested` domain audit for the actual mutation.
An existing generic `agent_tool.called` observation may occur for each tool
request or replay; it is not permission to count a second handoff mutation.
The current turn request has no idempotency key, while the existing command
requires a key and the gateway generates a key per typed-tool invocation. The
stable identity or owner-approved derivation for a failure-created command is
therefore unresolved; a row uniqueness constraint alone does not prove one
receipt or one domain audit. [W1:F007-F008; W2:F08-F10,G06; W3:G2]

For A4, a prior typed-tool mutation is already committed in its own
transaction when the later failure occurs. The expected proof is no duplicate
canonical mutation beyond that observed baseline, not a claim that the prior
effect was rolled back. Exact checkpointer timing and provider-side effects are
unknown, so the test must either prove the requested boundary or return A4 to
the owner. [W1:F007-F008,U003-U004; W3:G3,U1]

### Repeat failure after `human_handoff`

Once the conversation is `human_handoff`, the automation guard can reject a
second LLM-facing tool call. The acceptance test must not assume that a second
`/sales-agent/turn` reaches the failure writer or row-reuse branch: it must
record whether the second attempt is blocked before runtime/tool invocation or
actually reaches the handoff command. If blocked, the test proves the guard
outcome and the owner must decide whether that is the required A2 outcome or
whether another authenticated boundary test is needed; if it reaches the
writer, the one-row/receipt/domain-audit counts apply. [W2:F04-F05,F14;
W3:E4,E8]

### Handoff write-failure owner gate

The existing handoff command's receipt claim, domain write, audit, and receipt
settlement are transaction-scoped. A command error before commit means there
is no durable recovery state to report, even if an outer path has a handoff
intent or a handoff-shaped response. The first test must force that failure and
make the expected public behavior explicit. The default preservation is the
originating branch's established public status/code/details; any different
owner-approved outcome must be recorded before implementation. There is no
queue, retry, fallback, or second persistence path. [W2:G04;
W1:E019-E020]

### Recovery metadata owner gate

W2:F02 establishes that `reason_code` is a seven-value closed set, and W2:E08
identifies the existing `HumanHandoffArguments`/tool contract, but the packet
does not list the seven literals. W3:U2 also says the future failure-created
`reason_summary` is not established. This brief therefore does not inspect the
backend to list values and does not invent one: the owner must select one
existing value from the source-backed set identified by W2:E08. Only after
that decision may tests and implementation use one fixed, content-free,
allowlisted summary; no runtime diagnostic, provider text, exception, prompt,
credential, or patient content may be interpolated. [W2:F02,E08; W3:U2]

## DEFINITION OF DONE

Only after W5 PASS, explicit owner authorization, and the lifecycle transition
to `BLOCKED_OWNER_DECISION` may future implementation begin:

- All owner gates are recorded as decisions, and the focused tests were
  written first and initially failed for missing behavior.
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
- A reviewer accepts the **REVIEW CONTRACT** and the coordinator emits a
  self-contained implementation handoff. Until then this artifact remains
  pending review/owner gates, not `READY_TO_BUILD`.

## Execution model

Current W4 work is a solo, bounded planning-document repair by the dispatched
Codex worker. No implementation worker is active. The future graph is
sequential and intentionally small: `AGENT-02-T` first, then `AGENT-02-I`,
with no overlapping writer on either surface. Both future writers use the
`Codex Luna` model class; their roles are `backend_contract_engineer` and
`backend_integration_engineer` respectively. Parallelism is not authorized
because the two SubCards have a dependency and overlapping recovery semantics.

## RECOMMENDED WRITER MODEL

Use Codex Luna for both future SubCards after W5 PASS and explicit owner
authorization. `AGENT-02-T` is the contract-test writer;
`AGENT-02-I` is the single code-aware integration writer for the two declared
backend surfaces. The model recommendation is not implementation
authorization.

## REVIEW CONTRACT

The independent reviewer must verify, with evidence:

1. The exact trigger table records the owner choice, excludes pre-auth
   rejection, preserves generic 503 versus invalid-response 502, and does not
   silently change the explicit recursion-bound handoff contract.
2. The API-first boundary is respected: the separate Sales Agent uses the
   authenticated `BackendGateway` POST `/agent-tools/call` for the existing
   handoff operation; there is no direct cross-process import or database
   access.
3. Only the existing `ReceptionHandoff` domain is used: no new state, table,
   queue, worker, route, schema, retry, fallback, frontend, channel, or
   deployment surface.
4. Tenant derivation, permissions, one-open-row uniqueness, idempotency/audit,
   and operator-only resume remain intact.
5. Public status/code/details and sanitized diagnostics remain unchanged; the
   failure row cannot contain the four prohibited content classes, and the
   owner-selected reason code/summary is fixed and bounded.
6. A1–A7 are tested at the authenticated failure boundary, not inferred from
   adjacent explicit-handoff or provider-control tests. A2 records guard
   blocking versus row reuse; A4 is either proven or returned as an owner
   decision with the duplicate-effect evidence gap intact.
7. Focused and full serial test commands/results are recorded before any PASS,
   DONE, or READY claim. No evidence may come from a live provider, secret, or
   synthetic result presented as clinic truth.

## HANDOFF CONTRACT

This artifact is the only W4 deliverable:

`docs/handoffs/plans/2026-09-23-agent-02-truthful-ai-failure-human-recovery.md`

The coordinator must leave `orchestration/current-activity.yaml` in
`NEEDS_PRODUCT_DISCOVERY` during this W5 review/repair pending state. Only
after W5 PASS may the coordinator set the control-plane lifecycle to
`BLOCKED_OWNER_DECISION` if the owner gates remain unresolved; it must not
dispatch either SubCard, modify `CAVELOG.md`, modify the seed, or mark the
activity `READY_TO_BUILD` before explicit authorization. After authorization,
dispatch `AGENT-02-T` then `AGENT-02-I` with the exact write ownership above.
Any new contradiction, missing handoff write, unresolved idempotency behavior,
or privacy ambiguity returns to the owner; it must not be resolved by adding
another architecture.

## AUTHORITY AND EVIDENCE USED

Packet aliases used throughout this brief:

- `seed` — `docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml`
- `W1` — `docs/superpowers/evidence/agent-02-failure-path-scout.yaml`
- `W2` — `docs/superpowers/evidence/agent-02-human-handoff-domain-scout.yaml`
- `W3` — `docs/superpowers/evidence/agent-02-contract-test-scout.yaml`
- `FI` — `docs/superpowers/evidence/agent-02-discovery-fan-in.yaml`

Planning conventions applied: the repository `AGENTS.md`, `CONTEXT.md`, the
project `foreman-handoff` skill, and the existing living-brief/Activity Card
shape. Source claims in this repair are taken from the persisted packets and
coordinator fan-in; this pass did not rediscover or inspect backend source.
The evidence packets' source inspection and their limitations remain theirs;
this file does not upgrade packet evidence into implementation verification.

## EVIDENCE AND VALIDATION

Read-only validation for this repair: the planning protocol, approved seed,
W1/W2/W3 evidence packets, coordinator fan-in, current canonical brief, and
planning conventions were read. The target file is the only path changed by
this pass. No backend source, test, provider, live database, external runtime,
credential, seed, `orchestration/current-activity.yaml`, or CAVELOG was edited
or run. Earlier W4 repair dispatches failed before writing; this pass makes the
single bounded document edit.

This section is evidence of specification repair only, not implementation
verification, W5 PASS, a business PASS, `BLOCKED_OWNER_DECISION`, or
`READY_TO_BUILD`.

## DECISION AND PROGRESS LOG

- **2026-09-23 — W4 initial artifact:** Compiled the approved AGENT-02 seed
  and read-only W1–W3 evidence into one canonical Spec + Activity Card. No
  implementation was authorized.
- **2026-09-23 — W4 bounded repair:** Incorporated W5 findings from
  `msg_62511247ddec` and `msg_cf584a56667d`; separated Spec artifact status
  from control-plane lifecycle, made the API-first boundary explicit, added
  branch/write-failure/count/guard/reason-code gates, and made every SubCard
  complete. Current lifecycle remains `NEEDS_PRODUCT_DISCOVERY` pending W5
  PASS; no control-plane or CAVELOG change was made.

## NEXT APPROVAL / NEXT STEP

W5 must review this repaired artifact and record PASS or a further bounded
finding. After W5 PASS, the coordinator may set the control-plane lifecycle to
`BLOCKED_OWNER_DECISION` and present the owner gates above. The owner must then
select the failure boundary, key identity/count proof, write-failure outcome,
reason code/summary, and repeat-guard outcome before authorizing the two
SubCards. Until those steps occur, no implementation, test writing, test
execution, commit, publication, seed update, CAVELOG update, or
orchestration-state update is allowed, and this artifact is not
`READY_TO_BUILD`.
