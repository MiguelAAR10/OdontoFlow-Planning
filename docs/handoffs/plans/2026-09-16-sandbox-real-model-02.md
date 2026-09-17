# SANDBOX-REAL-MODEL-02 — First Real LLM End-to-End Smoke — FOREMAN HANDOFF

Date: 2026-09-16

Smoke base: `odontoflow-backend/main@1d4a710b15299c0ddb2317a230cb4a2fdd806052`

Status: **PARTIAL FAILURE — OPENROUTER TOOL EXECUTION REACHED THE CANONICAL
GATEWAY, BUT THE SALES AGENT TURN TIMED OUT**

## Executive result

One and only one synthetic booking-intent inbound event was sent through the
existing local chain. Canonical inbound persistence, authenticated Sales Agent
entry, OpenRouter-backed tool execution, availability lookup, and pending
proposal creation were observed. The mutating Sales Agent turn did not return
its final structured reply before the one-shot smoke client timed out at
15,278 ms. The local Sales Agent process was stopped at its exact PID after
that first failure. No replay, model change, fallback, consumer run, or
second paid request occurred.

The first broken boundary is runtime/provider timeout handling. The existing
OpenAI-compatible client is constructed without an explicit provider timeout,
output-token cap, or zero-retry setting. The existing sender correctly has one
attempt for the mutating Sales Agent turn. The minimum repair is a targeted
runtime-bound change; no agent redesign or provider change is indicated.

## Provider configuration

```text
provider=openrouter
model=deepseek/deepseek-v4-flash-0731
base_url=https://openrouter.ai/api/v1
adapter=existing langchain-openai / init_chat_model OpenAI-compatible path
key_source=OPENROUTER_API_KEY only
additional_dependency=none
```

The server-side environment names are `SALES_AGENT_MODEL_PROVIDER`,
`SALES_AGENT_MODEL`, `SALES_AGENT_MODEL_BASE_URL`, `OPENROUTER_API_KEY`,
`SALES_AGENT_V0_CREDENTIAL`, `SALES_AGENT_DATABASE_URL`,
`SALES_AGENT_BACKEND_URL`, `SANDBOX_BACKEND_URL`, `SANDBOX_RECEIVER_URL`,
`SANDBOX_INBOUND_TOKEN`, and `SANDBOX_DISPATCHER_TOKEN`. The Sales Agent
credential was the existing tenant-bound `sales-agent-v0` IAM credential from
the prior bootstrap; it was not reissued or printed during this smoke.

No Gemini path, `langchain-openrouter`, WhatsApp, n8n, production endpoint,
automatic booking, or model fallback was used. The provider/model/base URL and
credential are server-side settings; no caller request field can override
them.

## Preflight and service state

The credential-free preflight immediately before the smoke was:

```text
provider=openrouter
model=deepseek/deepseek-v4-flash-0731
base_url_configured=true
openrouter_api_key_configured=true
sales_agent_credential_configured=true
postgres_configured=true
sandbox_configured=true
ready_for_real_model_smoke=true
```

PostgreSQL was the healthy local `odontoflow-db-1` container on port 5434.
The canonical backend was started on loopback port 8000 and the Sales Agent
API on loopback port 8001, then both were stopped cleanly. All credentials came
from ignored `.env.local`; none was printed, copied into this brief, or
committed.

## Runtime budget evidence

```text
SALES_AGENT_RECURSION_LIMIT=12
SALES_AGENT_REQUEST_TIMEOUT_SECONDS=10.0
sender agent-turn attempts=1
sender canonical ingress/outbound transport attempts=up to 3 with idempotency
smoke client timeout=15.0 seconds
provider client probe: max_retries=2, timeout=None, max_tokens=None
```

The event count was exactly one and the graph recursion limit was finite. The
provider-specific controls were not finite enough for a reliable paid smoke:
the current runtime has no explicit output-token cap or provider timeout, and
the installed OpenAI client retains its default retry setting. This was
recorded, not changed, after the first error.

## Tool and tenant evidence

All observed business actions crossed the authenticated typed
`POST /agent-tools/call` gateway. The organization-1 audit rows for the one
conversation were:

```text
2 get_reception_context success
3 list_services success
4 list_locations success
5 get_reception_context success
6 query_available_slots success
8 propose_appointment success
```

Durations were respectively 72, 24, 27, 59, 57, and 147 ms. The proposal
creation audit was row 7 (`appointment_proposal.created`). No confirmation
tool call occurred. The server-issued Sales Agent credential resolved to
organization 1, and every observed tool audit row was organization 1. The
loopback database contained one organization, so this proves the configured
tenant scope but is not a second-tenant adversarial exercise.

## Database evidence

Baseline before the event:

```text
organizations=1
sandbox_channels=1
sandbox_pending_outbound=0
conversations=0
appointments=0
pending_appointment_proposals=0
agent_credentials_org1=1
```

After the failed turn:

```text
conversation_id=1 organization_id=1 channel_account_id=1 contact_identity_id=1
inbound message_count=1 message_id=1 delivery_status=received
proposal_id=1 organization_id=1 status=pending appointment_id=None
conversation_status=awaiting_confirmation
proposal_service_id=3 location_id=1 practitioner_id=1
proposal_start_utc=2026-09-22T14:00:00+00:00
proposal_end_utc=2026-09-22T15:00:00+00:00
outbound_count=0
appointments_org1=0
channel_provider=sandbox
```

This is the intended fail-closed booking result: availability was checked,
one pending proposal exists, and automatic confirmed appointments are zero.

## Outbound and metrics

No outbound reply was available to persist, so the canonical outbound command,
sandbox receiver, claim, receipt, and settlement were not invoked:

```text
canonical inbound=1 request (201)
Sales Agent turn=1 attempt (no response before timeout)
canonical outbound=0
sandbox claim/receive/settle=0
provider model-call count=not reported because completion telemetry was not emitted
input/output tokens=not reported
OpenRouter cost=not reported by the canceled runtime response
first-boundary latency=15,278 ms
```

The tool results prove that OpenRouter output reached the typed tools, but no
provider HTTP error category was returned. The final provider/runtime request
was still open at cancellation. A provider-side charge cannot be ruled out;
there was no follow-up request.

## Tests and evidence commands

- HEAD and the latest OpenRouter bootstrap handoff were verified.
- Sanitized preflight was run and returned `ready_for_real_model_smoke=true`.
- PostgreSQL and both loopback API health/openapi boundaries were checked.
- Read-only SQL collected the counts, IDs, proposal state, audit tool names,
  tenant IDs, and zero-appointment/outbound evidence above.
- No product/runtime code changed, so no focused or full pytest run was
  warranted for this evidence-only smoke. No provider call was made after the
  first failure.

Technical evidence handoff in the backend:
`odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-real-model-02.md`

## Exactly one recommended next activity

`SANDBOX-REAL-MODEL-03 — Bound the existing OpenRouter execution`: implement
and test only an explicit provider timeout, `max_retries=0`, and finite output
token cap at the existing runtime boundary, retaining native OpenAI support,
server-side provider selection, typed gateway access, and fail-closed booking;
then perform one new smoke. Do not start automatically.
