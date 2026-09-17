# SANDBOX-OUTBOUND-01 — Local Outbound Delivery — FOREMAN living brief

## Executive status

**BLOCKED — no safe local outbound delivery can be implemented under the
current provider/routing contract.** The existing queue, authenticated claim,
settle, retry, dead-letter, audit, and idempotency mechanisms are usable, but
there is no authoritative local sandbox destination. No product code or commit
was created.

The exact next decision is whether to approve a first-class local provider, a
server-owned binding that explicitly distinguishes a local sink from live
WhatsApp, or a real WhatsApp sandbox provider and credentials.

## Objective and success criteria

The requested outcome was a controlled local receiver consuming an existing
persisted outbound message through the authenticated `deliveries.manage`
claim/settle contracts, with safe duplicate, failure, retry, tenant, and audit
behavior. Live WhatsApp, patient traffic, paid models, n8n deployment,
migrations, production writes, and automatic booking were excluded.

The success criteria cannot be met safely until the receiver is proposal- and
provider-bound in an approved data/routing contract. A local process that
claims `test` rows would bypass the synthetic-provider exclusion. A process
that claims all `whatsapp` rows could mis-settle real-provider traffic as
locally delivered.

## Repository reality

- Backend HEAD at intake and close-out: `ad72435022054241fa27a784615b9ba8062ffecc`.
- The backend worktree retains the pre-existing unrelated modified/untracked
  paths; none were staged or changed by this activity.
- `ChannelAccount.provider` is constrained by the current model and migration
  `0015` to `whatsapp` or `test`.
- The claim service requires `deliveries.manage`, scopes by authenticated
  organization, leases with `FOR UPDATE SKIP LOCKED`, and excludes `test`.
- Settlement is tenant-scoped, processing-only, audited, retry-aware, and
  idempotent by the result key.
- The `outbound-dispatcher` server-credential profile already exists. No
  consumer, adapter, receiver, sandbox routing metadata, or external delivery
  implementation exists.
- The latest local smoke handoff identifies the missing connection as
  claim → provider transport → settle; the existing WF-01 export remains
  synthetic and inactive.

## Authority and evidence used

The repository `AGENTS.md`, installed OdontoFlow engineering, PostgreSQL,
security-hardening, TDD, verification, and Foreman-handoff procedures were
used. Targeted evidence came from `app/messaging/models.py`,
`app/messaging/schemas.py`, `app/messaging/service.py`,
`app/messaging/router.py`, migration `0015`, the dispatcher credential profile,
the messaging/security/bootstrap tests, and the prior local smoke/auth
handoffs. No provider, routing, settlement, or security rule was inferred.

## What we will build and how

Nothing is implemented in this activity. After the required decision, the
smallest safe slice would be:

1. encode the approved sandbox/live distinction in a server-authoritative
   channel contract;
2. consume through the existing authenticated claim route using a
   server-issued dispatcher credential;
3. transfer only the bound synthetic payload to the controlled receiver;
4. settle through the existing result route using a stable receiver message
   id and result idempotency key; and
5. prove duplicate, failure/retry, tenant isolation, audit, and final status
   against real PostgreSQL.

No generic messaging platform, provider, unauthenticated receiver, keyword
allowlist, caller trust flag, migration, or production adapter was added.

## Execution model

Solo FOREMAN. The shared PostgreSQL test database and the tightly coupled
claim/settle contract do not benefit from parallel workers.

## Risks, conflicts, and protected surfaces

The central safety risk is false settlement: a local consumer must not claim a
real WhatsApp-shaped row or report `sent`/`delivered` without a bound receiver
having accepted that exact payload. Reusing `provider=test` would violate the
existing synthetic-only boundary.

Protected surfaces and invariants remain unchanged: existing migrations,
`app/errors.py`, `app/db.py`, availability, booking fail-closed behavior,
Sales Agent authentication, tenant isolation, audit atomicity, claim leases,
retry/dead-letter rules, settlement idempotency, and all unrelated dirty
paths.

## Evidence and validation

Focused serial real-PostgreSQL checks:

```text
./.venv/bin/python -m pytest -q \
  tests/test_messaging_phase2.py \
  tests/test_security_boundary.py::test_integration_routes_deny_a_member_without_permissions \
  tests/test_security_boundary.py::test_failed_authentication_is_a_real_redacted_security_event \
  tests/test_bootstrap_n8n_lab.py
→ 19 passed, 2 warnings in 21.93s
```

The live `ck_channel_accounts_provider` definition contains only
`whatsapp`/`test`. A transaction-local `provider='sandbox'` insert failed at
that PostgreSQL check, and a follow-up query found no persisted sandbox row.
No production write was made. The previous full-suite evidence remains
535 passed; no full suite was rerun because no product code or contract
changed.

Technical handoff:
`../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-outbound-01.md`

## Decision and progress log

- 2026-09-16 — Verified HEAD `ad724350`, dirty paths, latest auth/local-smoke
  handoffs, outbound queue/claim/settle, IAM, provider, and idempotency
  contracts.
- 2026-09-16 — Re-ran the focused real-PostgreSQL messaging/security/bootstrap
  pack: 19 passed.
- 2026-09-16 — Confirmed PostgreSQL rejects a `sandbox` provider and that no
  existing server-authoritative receiver binding exists.
- 2026-09-16 — Stopped without implementation. This is a product/data/provider
  contract decision, not a safe code-only fix.

## Next approval / next step

Owner must select one supported contract: first-class local provider (with an
approved additive migration), explicit server-owned local-vs-live WhatsApp
binding, or real WhatsApp sandbox credentials. Only then should a new bounded
activity implement and verify the consumer. Do not start automatically.
