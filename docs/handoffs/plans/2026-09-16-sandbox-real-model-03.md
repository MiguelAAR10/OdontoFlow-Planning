# SANDBOX-REAL-MODEL-03 — Foreman Handoff

Date: 2026-09-16

Backend base: `odontoflow-backend/main@18fae8deeccd423fe1d55d98144b5e3f4c0f2f76`

Status: **PARTIAL FAILURE — bounded real-model turn returned HTTP 503**

## Decision and implementation result

The existing OpenRouter/OpenAI-compatible boundary was retained. No new model
framework or dependency was added. The Sales Agent now receives these
server-side bounded controls:

```text
provider=openrouter
model=deepseek/deepseek-v4-flash-0731
base_url=https://openrouter.ai/api/v1
key_source=OPENROUTER_API_KEY only
per_model_request_timeout=20.0 seconds
max_retries=0
max_output_tokens=512
overall_turn_timeout=180.0 seconds
gateway_http_timeout=10.0 seconds
recursion_limit=12
```

Native OpenAI and fake-model paths remain supported. Provider/model/base URL
and credentials are not request-controlled. The existing typed gateway,
tenant-bound IAM credential, sandbox sender, fail-closed proposal policy, and
one-attempt mutating turn were preserved.

## One new smoke result

The owner key was present and the sanitized preflight was:

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

Exactly one new fictitious sandbox event was sent. The sender used one
authenticated `/sales-agent/turn` attempt with a 195-second caller timeout;
the 20-second provider request deadline and 180-second overall turn deadline
did not fire. The response was HTTP 503 after approximately 7.5 seconds.
No replay, model switch, fallback, second paid request, outbound persistence,
or sandbox consumer run occurred.

Database evidence:

```text
conversation_id=2 organization_id=1 channel_provider=sandbox
inbound_message_id=2 received
agent_tool_audit=1 successful get_reception_context, 38ms
model-driven business tools=0
proposal for conversation 2=0
appointments total=0
outbounds total=0
sandbox receipts total=0
open sandbox outbounds=0
prior proposal id=1 remains pending with appointment_id=None
```

The first broken boundary is the Sales Agent model-execution boundary after
the canonical context load. The exact category remains **uncertain**: the
existing API returned a content-free 503 and the Uvicorn log exposed only the
access status, with no provider request ID, error body, token usage, cost, or
runtime telemetry record. The failure was not a configured timeout. It cannot
be distinguished from provider rejection/availability, model response/tool
calling incompatibility, or a runtime integration error without a sanitized
failure classification at the existing boundary.

## Verification

- Focused provider/runtime/sandbox pack after final code change: **37 passed**.
- Lint and diff checks: passed.
- No-network adapter probe: `request_timeout=20.0`, `max_retries=0`,
  `max_tokens=512`.
- Full real-PostgreSQL suite: **565 passed, 1 unrelated concurrency failure,
  21 warnings**. The failed existing idempotency race test passed in isolation
  (**1 passed**); no changed file overlaps that path.

Technical handoff:
`odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-real-model-03.md`

## Exactly one recommended next activity

`SANDBOX-REAL-MODEL-04 — Expose a sanitized provider/runtime failure category`
without changing provider/model, gateway, booking policy, or fallback behavior.
Do not start it automatically.
