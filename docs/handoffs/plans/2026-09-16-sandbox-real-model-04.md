# SANDBOX-REAL-MODEL-04 — FOREMAN living brief

## Executive status

**Blocked before Sales Agent.** The single new synthetic sandbox booking-intent
event received HTTP 404 at the canonical inbound boundary. No Sales Agent turn,
OpenRouter request, tool call, outbound, receipt, or business mutation occurred.
The next decision is an ingress investigation, not a provider diagnosis.

## Objective and success criteria

Run exactly one new bounded real-model sandbox conversation and use the
sanitized Sales Agent diagnostics if the turn reaches the runtime. Stop on the
first external failure, preserve all existing state, and report the first
broken boundary without retry, fallback, replay, or repair.

The event did not reach the Sales Agent, so the Sales Agent diagnostic contract
was not exercised. The activity still satisfied its stop rule and established
the first observed boundary.

## Repository reality

- Backend HEAD at intake and smoke: `db5278954f11e4a8870051637d2046808133f927`.
- OpenRouter configuration was ready: provider `openrouter`, model
  `deepseek/deepseek-v4-flash-0731`, configured base URL, key presence, and
  `ready_for_real_model_smoke=true` without exposing the key.
- PostgreSQL was reachable and the canonical backend health endpoint returned
  HTTP 200; the Sales Agent loopback service was reachable.
- The actual new event request returned HTTP 404 from
  `POST /internal/messages/inbound` before persistence or Sales Agent entry.
- A later direct unauthenticated non-event probe returned HTTP 401, and source
  inspection shows the route is registered. The reason for the discrepancy is
  unresolved.
- Existing rows remained unchanged: two sandbox conversations, two inbound
  messages, one pending proposal in organization 1, zero appointments,
  outbounds, and sandbox receipts.

## Authority and evidence used

Used `AGENTS.md`, the REAL-MODEL-DIAGNOSTICS-01 handoff, the installed
OdontoFlow engineering, Foreman handoff, and verification instructions, the
sanitized preflight, local service health checks, sender/backend access logs,
route source, and read-only database queries. No parallel workers, scouts,
worktrees, provider requests, or broad repository audit were used.

## What was built and how

Nothing was built. The existing sender, canonical backend, and local services
were used unchanged. No code, schema, authentication, transport, provider, or
runtime configuration was modified. This activity adds only an evidence
handoff.

## Execution model

Solo supervised execution. Exactly one new synthetic sender event was attempted
and stopped at its first 404. The sender's configured Sales Agent attempt
budget was one; it was never reached. No retry or second paid request was made.

## Risks, conflicts, and protected surfaces

No secret or sensitive event payload was printed or persisted in the handoff.
The prior pending proposal was not modified. No automatic appointment was
created. The typed gateway, tenant boundary, fail-closed booking policy,
sandbox transport, provider isolation, and Sales Agent diagnostics remain
unchanged. The 404 root cause must not be guessed from the later 401 probe.

## Evidence and validation

```text
preflight=ready_for_real_model_smoke=true
provider_requests=0
sales_agent_turn_attempts=0
tool_calls=0
canonical_inbound_status=404
new_smoke_persisted_rows=0
proposals_total=1 (existing pending proposal, organization 1)
appointments_total=0
outbounds_total=0
sandbox_receipts_total=0
automatic_appointments_created=0
sales_agent_diagnostics=not_emitted
```

No pytest run was required because no code changed. Local services were stopped
after the read-only evidence collection.

## Decision log

- 2026-09-16 — Preflight and local services were healthy with the fixed
  OpenRouter/DeepSeek configuration and bounded time/token settings.
- 2026-09-16 — The one new event failed at canonical inbound HTTP 404 before
  Sales Agent; no provider request or business mutation was attempted.
- 2026-09-16 — Later non-event 401 evidence and registered route source confirm
  an ingress discrepancy but do not identify its cause; no repair was made.

## Next approval / next step

Approve exactly one bounded activity:

`SANDBOX-INGRESS-ROUTE-01 — resolve and verify why the sender's effective
backend origin/request returns 404 while the live registered route returns 401;
prove authenticated canonical inbound persistence, then stop before Sales Agent
and OpenRouter.`

Do not replay this event, modify the existing pending proposal, invoke a model,
or start the next activity automatically.

Technical handoff:
`odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-real-model-04.md`

Documentation commit: backend handoff only, with no product code changes.
