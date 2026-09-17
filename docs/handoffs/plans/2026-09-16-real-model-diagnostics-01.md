# REAL-MODEL-DIAGNOSTICS-01 — FOREMAN living brief

## Executive status

**Implemented and verified.** The existing Sales Agent 503 boundary now emits
sanitized, structured failure evidence while preserving its generic public
error contract and all no-retry/fail-closed behavior. The root cause of the
prior real-model 503 remains **UNKNOWN** because this activity was explicitly
not permitted to make another provider request.

## Objective and success criteria

Translate the prior partial failure into an evidence-first recovery contract:
classify recognized provider/runtime failures, preserve unknown as unknown,
capture safe trace/stage/timing/effect evidence, and make no business mutation,
retry, fallback, or provider request while diagnosing.

Excluded: OpenRouter smoke execution, model switch, fallback routing, timeout
retuning, WhatsApp, n8n deployment, consent/schema changes, production data,
and new observability infrastructure.

## Repository reality

At intake, backend `main` was `d6940c64cc0c8fe8ac88cdabd48e7435a8c4f86f`. The
runtime used `langchain-openai` through `init_chat_model`; the API caught a
generic `RuntimeError` and returned `AGENT_EXECUTION_FAILED` 503. Existing
HTTP security middleware already generated validated request/correlation IDs,
but the Sales Agent boundary did not attach them to failure evidence.

The prior smoke had loaded canonical context, then returned 503 without a
configured timeout, provider request ID, provider category, token/cost data,
or visible runtime telemetry. Its partial business-state result was already
preserved by existing one-attempt sender and canonical persistence contracts.

The worktree contained unrelated dirty/untracked user files. They were
preserved and are not part of this activity's staged change.

## Authority and evidence used

Used the repository `AGENTS.md`, the existing SANDBOX-REAL-MODEL-03 handoff,
OdontoFlow engineering/security/TDD/diagnosis/review/verification/Foreman
skills, and current OpenAI Python SDK documentation resolved through Context7
(`/openai/openai-python`). The SDK evidence supports classification through
`APIStatusError` subclasses, `APIConnectionError`, `APITimeoutError`,
`status_code`, and `request_id`; no response body is required.

## What we built and how

The smallest supported repair stays at the current runtime/API boundary:

- runtime stage tracking and a bounded `SalesAgentDiagnostic` value object;
- known OpenAI-compatible error classification with safe status/request ID
  extraction and explicit `unknown` fallback;
- internal observation of successful mutating-tool calls for partial-effect
  reporting;
- one `sales_agent_failure` JSON warning through existing logging;
- existing public error code/message retained, with only validated trace IDs in
  `details`;
- deterministic no-network tests for provider status/timeout, runtime/unknown,
  safe serialization, and no retry.

No new dependency, framework, schema, provider adapter, model fallback, or
recovery subsystem was introduced.

## Execution model

Solo FOREMAN execution. The runtime/API tests share the real PostgreSQL test
database and were run serially; no parallel worker would reduce risk for this
tightly coupled boundary.

## Risks, conflicts, and protected surfaces

The diagnostic record is deliberately allowlisted: no exception text, provider
body, auth header, credential, patient message, or stack trace. Public error
messages remain generic. A diagnostic warning cannot trigger a retry or mutate
canonical state. The typed gateway, tenant/IAM boundary, booking policy,
sandbox transport, fake-model path, native OpenAI path, and provider/model
server configuration remain unchanged.

The previous real-model category is not inferred from the new classifier; only
a future authorized request can populate a real provider failure record.

## Evidence and validation

- Focused Sales Agent/provider/auth/W3/W4/sandbox pack: **53 passed, 2
  warnings**.
- Ruff on changed Python surfaces: **passed**.
- `git diff --check`: **passed**.
- Existing concurrency test in isolation: **1 passed, 2 warnings**.
- Complete real-PostgreSQL suite: **570 passed, 21 warnings** in `437.52s`.
- No OpenRouter/OpenAI/model/sandbox/outbound request was made.

## Decision and progress log

- 2026-09-16 — Verified the 503 flattening boundary and ranked provider,
  runtime, and gateway hypotheses without assuming an OpenRouter cause.
- 2026-09-16 — Red tests reproduced the missing diagnostic type/classification
  and safe HTTP evidence; the minimal runtime/API repair made them green.
- 2026-09-16 — Focused pack, lint, diff check, isolated concurrency check, and
  full PostgreSQL suite passed; no external request was attempted.

## Next approval / next step

Exactly one future activity is recommended:
`SANDBOX-REAL-MODEL-04 — one newly authorized, bounded diagnostic smoke using
the existing OpenRouter model, stopping on the first external failure and
inspecting the sanitized record.` It must not replay prior events, switch
models, retry the workflow, or start automatically.

Technical handoff:
`odontoflow-backend/docs/superpowers/handoffs/2026-09-16-real-model-diagnostics-01.md`

Commit: the implementation, tests, changelog, and handoff are included in the
single bounded commit reported by FOREMAN.
