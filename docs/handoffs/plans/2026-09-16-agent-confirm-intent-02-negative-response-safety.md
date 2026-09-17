# AGENT-CONFIRM-INTENT-02 — Negative response safety — FOREMAN living brief

## Executive status

**BLOCKED — NEEDS_PRODUCT_DECISION.** The temporal guard from
AGENT-CONFIRM-GUARD-01 remains intact, but it proves only that a later patient
turn occurred. Against real PostgreSQL, a later `No, thanks` message still
allowed a forced fake-model `confirm_appointment` call to create an
Appointment. No implementation or commit is authorized until affirmative
consent semantics are defined.

## Objective and success criteria

Objective: determine whether the current booking contract prevents booking
after a patient explicitly declines or responds ambiguously. Success would
require a deterministic, authoritative affirmative signal bound to the exact
proposal, while preserving temporal ordering, idempotency, expiry, isolation,
and audit behavior.

The activity is stopped because the repository has no such signal or binding.
No keyword consent, LLM authority, schema migration, channel integration, or
agent redesign was introduced.

## Repository reality

Backend HEAD is `6b0d2226e930030c3c1582851c20b9894b56225d` on `main`; the branch
is one commit ahead of `origin/main`. The worktree had pre-existing unrelated
dirty/untracked files. This activity added only an uncommitted diagnostic
regression and the blocked handoff; production booking code is unchanged.

The booking command checks a pending, unexpired proposal and now requires an
inbound `Message` in the same organization/conversation with persisted
`created_at` later than the proposal. `Message` stores raw text and temporal /
delivery fields but no consent classification. `AppointmentProposal` has no
confirmation-message reference, and `ConfirmAppointmentArguments` carries only
the proposal ID and token. Contact-level `consent_status` is not appointment
consent; the approved Sales Agent plan explicitly says it is declared but not
implemented for compliance.

## Authority and evidence used

The inspection used the repository AGENTS contract, the
`AGENT-CONFIRM-GUARD-01` technical handoff, the canonical booking/message/
proposal models and schemas, the approved Sales Agent integration plan, the
planning `CONTEXT.md` definition of Patient Confirmation, and the existing
cancellation guard. The plan requires an explicit affirmative reply but does
not specify how free text becomes authoritative consent.

## What was tested

The existing fake-model W4 infrastructure was extended only in tests with a
fresh agent-memory database. It runs: proposal turn, later inbound `No,
thanks`, then a forced confirmation-tool call. The diagnostic assertion
expects a proposed response, zero appointments, one pending proposal, and one
stable confirmation error. Current output is:

```text
('confirmed', 1, 0, 0)
```

That is `(agent_outcome, appointment_count, pending_proposal_count,
confirmation_error_count)` and proves the temporal guard alone is insufficient.

## Execution model

FOREMAN worked solo. The backend test database is shared, so all pytest runs
were serial. No external service or production database was used.

## Risks, conflicts, and protected surfaces

The risk is a false positive booking after rejection or ambiguity. The safe
boundary is unresolved: raw text may be negative, ambiguous, unrelated, or
affirmative, but the application has no approved classifier or consent event.
The temporal guard, proposal token/conversation isolation, expiry, idempotency,
and audit path remain untouched. No protected path, migration, or production
write was used.

## Evidence and validation

```text
$ .venv/bin/python -m pytest -q tests/test_sales_agent_w4.py::test_wf01_rejects_negative_later_message_before_booking -vv
1 failed, 2 warnings
AssertionError: assert ('confirmed', 1, 0, 0) == ('proposed', 0, 1, 1)

$ .venv/bin/python -m pytest -q -rs tests/test_agent_booking_phase4.py::test_explicit_confirmation_books_once_and_returns_calendar_payload tests/test_agent_booking_phase4.py::test_confirmation_is_bound_to_the_original_conversation tests/test_agent_booking_phase4.py::test_expired_proposal_cannot_be_confirmed tests/test_sales_agent_w4.py::test_wf01_three_turn_loop_persists_once_and_keeps_threads_isolated tests/test_sales_agent_w4.py::test_wf01_rejects_same_turn_model_propose_then_confirm
5 passed, 2 warnings in 12.17s

$ .venv/bin/python -m pytest -q -rs
1 failed, 528 passed, 21 warnings in 562.97s
```

The historical green baseline at `6b0d2226` was 528 passed and 21 warnings;
the current diagnostic collection is 529 tests with one intentional failure.

## Decision and progress log

- 2026-09-16 — Adversarial real-PostgreSQL regression reproduced appointment
  creation after `No, thanks`.
- 2026-09-16 — Contract inspection found no authoritative affirmative consent
  representation or proposal-specific confirmation-message binding.
- 2026-09-16 — Implementation stopped; status is BLOCKED / NEEDS_PRODUCT_DECISION.

## Next approval / next step

The Owner must approve the authoritative consent contract: the exact affirmative
action; the trusted producer (for example, a proposal-bound channel/UI event or
operator action); the binding to proposal and inbound message; and negative,
ambiguous, and revocation behavior. Supported safe directions are a persisted
proposal-bound consent event, operator-mediated approval, or temporary
fail-closed/human handoff for unclassified free text. Keyword lists and model
claims are explicitly excluded. Do not start another activity automatically.

## Handoff artifacts

- Backend evidence: `../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-intent-02.md`
- Diagnostic regression: `../odontoflow-backend/tests/test_sales_agent_w4.py::test_wf01_rejects_negative_later_message_before_booking`
- Prior guard handoff: `../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-agent-confirm-guard-01.md`
