# AGENT-CONFIRM-FAIL-CLOSED-03 — FOREMAN living brief

## Executive status

**PASS — bounded fix implemented and verified; no next activity started.** The
MVP decision is now enforced at the authoritative booking command boundary:
an `agent` principal cannot convert a pending appointment proposal into an
appointment when the only persisted evidence is a later free-text inbound
message. The proposal remains pending and the stable error/audit path is
used. Authenticated human confirmation remains available through the existing
server-resolved principal context.

## Objective and success criteria

The objective was to prevent an LLM from treating a later patient turn as
affirmative booking consent. The fix had to be deterministic and bounded to
booking confirmation, preserve the completed temporal guard, and avoid
keywords, model assertions, caller trust flags, contact-level consent, new
schema, channel, or unauthenticated operator bypass.

Success criteria met:

- a fake model that proposes and then attempts confirmation after `No, thanks`
  receives `INVALID_INPUT`, leaves one proposal pending, and creates zero
  appointments;
- agent confirmation is rejected even after a later inbound message, while an
  authenticated human confirmation still succeeds;
- proposal token/conversation/tenant binding, expiry, idempotent replay,
  audit, and exactly-one appointment behavior remain covered;
- the real-PostgreSQL focused and full backend suites pass serially.

## Repository reality

The activity started from backend `6b0d2226e930030c3c1582851c20b9894b56225d`
(`AGENT-CONFIRM-GUARD-01`). That commit already required a later persisted
inbound message, but `Message` has raw text and timing only, and
`AppointmentProposal` plus `ConfirmAppointmentArguments` have no authoritative
consent classification or proposal-specific acceptance-message binding. The
blocked INTENT-02 regression reproduced `('confirmed', 1, 0, 0)` for the
negative message case.

The server-resolved `ExecutionContext.principal_type` is authoritative for
authenticated HTTP callers. The n8n Sales Agent credential resolves to
`agent`; the test/operator credential resolves to `human`. Existing unrelated
dirty and untracked worktree paths were preserved.

## Authority and evidence used

The work used the backend `AGENTS.md`, the repository-local
`odontoflow-engineering`, TDD, PostgreSQL, verification, code-review, and
Foreman instructions; the approved Sales Agent integration plan; planning
`CONTEXT.md`; the prior GUARD-01 and INTENT-02 handoffs; and the booking,
message, proposal, gateway, IAM, and cancellation contracts. Those sources
support only the fail-closed MVP decision. They do not define a new patient
consent protocol.

## What we built and how

`confirm_contact_booking_proposal` retains the existing transaction, permission
check, exact proposal lookup, confirmed replay branch, expiry check, and later
inbound-message guard. After those checks, an authenticated `agent` principal
receives `INVALID_INPUT` instead of reaching `_book_appointment_core`. This
uses no request/body trust flag and does not inspect message text. The gateway
continues to record the error audit event atomically with its response path.

Tests reuse the real-PostgreSQL fake-model W4 infrastructure. The negative
regression is retained; the existing W4 agent loop now asserts pending
proposals rather than automatic bookings, and the reception authorization test
proves the same proposal remains confirmable by the existing authenticated
human caller.

## Execution model

Solo FOREMAN execution. The booking command and directly relevant integration
tests share the same files and PostgreSQL test database, so parallel builders
would add contention without reducing risk.

## Risks, conflicts, and protected surfaces

The unresolved product dependency is future automatic booking: it still needs
a trusted, authenticated, proposal-bound patient acceptance mechanism before
an agent may be permitted to confirm. The current MVP intentionally fails
closed until that contract exists. No keyword classifier, LLM consent claim,
contact communication consent, schema migration, channel integration, agent
redesign, deployment, or production write was added.

The temporal guard, tenant/conversation isolation, proposal expiry,
idempotency/replay, audit behavior, and existing human confirmation path remain
in scope and covered. Protected paths (`app/errors.py`, `app/db.py`,
`app/scheduling/availability.py`, migrations) were not changed.

## Evidence and validation

The required red-green evidence was captured against real PostgreSQL before
the production guard:

```text
tests/test_sales_agent_w4.py::test_wf01_rejects_negative_later_message_before_booking
1 failed, 2 warnings
AssertionError: ('confirmed', 1, 0, 0) != ('proposed', 0, 1, 1)
```

After implementation, the focused booking/Sales Agent/reception set passed:

```text
7 passed, 2 warnings in 11.69s
```

It included the valid two-message booking and replay, conversation isolation,
expiry, same-turn rejection, negative `No, thanks` rejection, the W4
thread-isolation loop, and the authenticated-agent/human authorization flow.

The final serial backend suite passed:

```text
529 passed, 21 warnings in 505.22s (0:08:25)
```

Current collection is 529 tests: two more than the historical 527-pass
baseline (the prior same-turn regression and this negative-response
regression). `compileall`, `git diff --check`, and the protected-path diff
check passed. Ruff reported the same six pre-existing import/unused-import
diagnostics already present at the base commit; no new ruff diagnostics were
introduced by this activity.

## Decision and progress log

- 2026-09-16 — INTENT-02 evidence established that later free text cannot
  prove affirmative consent.
- 2026-09-16 — Owner/MVP decision approved fail-closed behavior for
  agent-driven confirmation without inventing a consent contract.
- 2026-09-16 — Agent principal guard implemented after temporal evidence and
  before appointment creation; authenticated human flow retained.
- 2026-09-16 — Focused and full real-PostgreSQL verification passed; bounded
  commit and technical handoff completed.

## Next approval / next step

No next activity is started automatically. Automatic agent booking remains
held until the product owner approves a trusted acceptance producer and its
proposal binding (for example, a server-authenticated patient action or a
separately authorized operator workflow). Any future reopening must preserve
the current fail-closed default for unverified free text.

## Handoff artifacts

- Backend technical handoff: `odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-fail-closed-03.md`
- Negative regression: `odontoflow-backend/tests/test_sales_agent_w4.py::test_wf01_rejects_negative_later_message_before_booking`
- Prior temporal-guard handoff: `odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-guard-01.md`
- Prior blocked intent handoff: `odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-intent-02.md`
