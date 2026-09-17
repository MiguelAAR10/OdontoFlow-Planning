# AGENT-TURN-AUTH-01 — Secure Sales Agent entrypoint — FOREMAN living brief

## Executive status

**PASS — the Sales Agent turn boundary is authenticated and tenant-bound; no
next activity was started.** `POST /sales-agent/turn` now accepts only the
server-configured, PostgreSQL-authenticated `agent` service principal with the
existing conversation-read permission. The prior booking temporal guard and
MVP fail-closed policy remain intact.

Backend result commit: `ad72435022054241fa27a784615b9ba8062ffecc`.

## Objective and success criteria

Secure the standalone Sales Agent HTTP entrypoint without adding a second
authentication system, breaking the fake-model test seam, or weakening booking
safety.

Success criteria met:

- missing and invalid bearer credentials are rejected before runtime execution;
- valid non-agent principals, cross-tenant credentials, and agents without the
  required permission are rejected before the runtime;
- an authorized server-issued `sales-agent-v0` agent credential reaches the
  injected fake runtime and receives the typed response;
- the process credential is bound to the runtime gateway identity, so a caller
  cannot select a different tenant through request data or an injected runtime;
- WF-01 forwards the existing agent credential, and the inactive export records
  the same header contract;
- the full real-PostgreSQL suite remains green.

Out of scope: human login, WhatsApp, n8n runtime deployment, provider billing,
new consent semantics, schema/migrations, IAM redesign, deployment, and
production writes.

## Repository reality

At intake the backend was `main@021fa529`, the PASS result of
LOCAL-RUNTIME-SMOKE-01. The route was open even though its internal backend
gateway already used the configured `SALES_AGENT_V0_CREDENTIAL`. The canonical
FastAPI app already supplied `require_authenticated_context`, PostgreSQL
credential resolution, tenant context, rate limiting, error envelopes, and
permission evaluation to `/internal/*` and `/agent-tools/*`; the standalone
Sales Agent app did not reuse that boundary.

The existing WF-01 runner had both `ODONTOFLOW_INBOUND_TOKEN` and
`ODONTOFLOW_AGENT_TOKEN`, but sent the latter only to backend outbound/tool
calls. The checked-in export was inactive and had no live n8n validation. The
existing W4 harness uses real PostgreSQL, an injected `SalesAgentRuntime`, and a
synthetic fake model; it remains the supported local verification path.

The backend worktree also contains pre-existing unrelated modified and
untracked paths (`.gitignore`, `AGENTS.md`, skill/tooling directories,
architecture/review material, and prior handoffs). They remain outside this
change. The planning worktree was already dirty and is updated only in its
existing control-plane files and this living brief.

## Authority and evidence used

The repository `AGENTS.md`, the installed `odontoflow-engineering`,
`security-and-hardening`, `test-driven-development`,
`verification-before-completion`, `code-review-and-quality`, and
`foreman-handoff` skills were used. Relevant authority was limited to the
Sales Agent route/runtime/gateway, WF-01 caller/export, existing IAM/context
helpers, and their tests. The previous LOCAL-RUNTIME-SMOKE-01 and
AGENT-CONFIRM-FAIL-CLOSED-03 handoffs established the real PostgreSQL fake
path and the booking safety boundary.

No new identity, consent, channel, or tenant rule was inferred. The endpoint
uses the existing server-resolved principal and permission vocabulary; the
additional process-credential match only binds that caller to the identity
already configured for the runtime's backend gateway.

## What we will build and how

The bounded implementation is complete:

1. Reuse `require_authenticated_context` and the existing `IntegrationBearer`
   scheme on the standalone Sales Agent route.
2. Require the caller to match the configured gateway credential, fail closed
   if configuration is absent or an injected runtime disagrees, require the
   server-resolved `agent` principal type, and evaluate
   `conversations.read` through the existing IAM service.
3. Reuse canonical error handlers, transport middleware, trace headers, and
   OpenAPI security publication for the standalone app.
4. Forward `ODONTOFLOW_AGENT_TOKEN` from the W4 runner/export and document that
   it is the same server-issued credential configured as
   `SALES_AGENT_V0_CREDENTIAL`.
5. Prove the boundary with real PostgreSQL tests, then run the focused pack and
   full suite serially.

No dispatcher, channel, model-provider, consent, or booking implementation is
part of this activity.

## Execution model

Solo FOREMAN. The shared PostgreSQL test database requires serial pytest runs,
and the route/caller/test changes form one tightly coupled authorization slice;
parallel workers would add contention without reducing risk.

## Risks, conflicts, and protected surfaces

The main risk was allowing a valid credential from another tenant to drive a
long-lived runtime whose backend gateway is configured for a different tenant.
The process-credential match fails closed on that mismatch; the PostgreSQL
auth context and backend tool permission checks remain authoritative.

The following stayed untouched: `app/errors.py`, `app/db.py`,
`app/scheduling/availability.py`, all existing migrations, canonical booking
guards, schema contracts, and `../../medistock`. No token is embedded in code
or the n8n export. The local injected runtime still requires a real issued
credential and auth session maker; injection is not an auth bypass.

The n8n export remains inactive and has not been validated against a live n8n
runtime. The next deployable-chain blockers remain the external channel/runtime,
outbound consumer, model-provider budget/key decision, and deployment shape.

## Evidence and validation

The intentional red run against the previously open route showed **5 failed,
1 passed, 2 warnings** in the new boundary test file. After implementation:

```text
Focused auth/Sales Agent/reception/IAM/security pack:
84 passed, 2 warnings in 59.74s

Full serial real-PostgreSQL suite:
535 passed, 21 warnings in 405.49s (0:06:45)
```

The current collection is 535 tests, versus the historical 527-pass baseline
and the pre-task 529-test collection. Additional checks passed: targeted Ruff
for the new route/auth test, JSON parsing of the n8n export, and
`git diff --check`. Existing W3/W4 fake-model tests continue to prove proposal,
temporal/fail-closed booking, isolation, expiry, idempotency, audit, and
synthetic-provider behavior.

Canonical backend evidence:
[`docs/superpowers/handoffs/2026-09-16-agent-turn-auth-01.md`](../../../../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-turn-auth-01.md)

## Decision and progress log

- 2026-09-16 — Verified backend `021fa529`; the Sales Agent turn route was
  unauthenticated while the internal gateway was already credentialed.
- 2026-09-16 — Added the real-PostgreSQL red boundary tests before changing
  production code.
- 2026-09-16 — Reused PostgreSQL bearer authentication/context and IAM
  permission evaluation; added fail-closed configured-identity binding and
  service-principal restriction.
- 2026-09-16 — Updated WF-01 caller/export, ran focused checks and the full
  serial suite; all required tests passed.

## Next approval / next step

No next activity is authorized or started automatically. The current
MVP-01 control-plane activity remains **NOT_STARTED** pending the existing
owner decisions on live channel/provider, n8n ownership, deployment shape,
and model-provider budget. Automatic agent booking also remains fail closed
until a trusted, authenticated, proposal-bound patient acceptance mechanism is
approved.
