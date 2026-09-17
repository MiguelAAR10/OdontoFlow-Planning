# SANDBOX-OUTBOUND-02 — First-class sandbox delivery — FOREMAN living brief

## Executive status

**PASS — the approved development-only sandbox delivery slice is complete;
no next activity was started.** Backend base was `ad724350`; the bounded
implementation adds provider isolation, an authenticated loopback receiver,
durable duplicate-safe receipts, and a one-shot authorized consumer. The final
backend commit is recorded in the CAVELOG and close-out response.

## Objective and success criteria

The CTO-approved first-class `sandbox` provider now supports one safe local
outbound lifecycle:

```text
persist → provider-bound claim → authenticated local receiver → durable receipt
  → existing settlement → delivered/retry/dead-letter state
```

Acceptance criteria met:

- `sandbox` persists through an additive migration without changing existing
  `test` or `whatsapp` rows;
- only `provider=sandbox` rows can be claimed by the sandbox consumer;
- a configured loopback receiver and server-issued `deliveries.manage`
  credential are mandatory;
- the receiver binds one exact outbound payload to one tenant-bound receipt;
- duplicate processing replays the same receipt and does not create a second
  delivery;
- receiver failure uses the existing transient settlement/retry path;
- cross-tenant rows are not visible, and `test`/`whatsapp` cannot escape;
- sandbox success cannot be manufactured through the generic settle boundary
  without the server-owned local receipt;
- temporal/fail-closed booking, Sales Agent authentication, tenant isolation,
  expiry, audit, idempotency, and existing provider semantics remain intact.

Explicit exclusions remain: WhatsApp, inbound adapters, paid models, n8n
deployment, patient data, consent rules, production migration/deployment,
production writes, human-login redesign, and automatic booking.

## Repository reality

At intake the backend was `main@ad72435022054241fa27a784615b9ba8062ffecc`,
following the blocked SANDBOX-OUTBOUND-01 handoff. The worktree already had
unrelated modified/untracked paths (`.gitignore`, `AGENTS.md`, skill/tooling
directories, architecture/review material, and earlier handoffs); they were
preserved and excluded from the bounded commit. The prior outbound contract
already provided PostgreSQL queue persistence, authenticated tenant-scoped
claim/settle, leases, retry/dead-letter transitions, audit, and the existing
`outbound-dispatcher` profile, but the provider CHECK admitted only `whatsapp`
and `test`, with `test` intentionally excluded from external claim.

The approved decision authorizes additive development/testing schema work. The
implementation therefore adds migration `0019`, the `sandbox` provider, and a
receipt table with a composite tenant/outbound foreign key. It does not reuse
the synthetic provider or make a WhatsApp-shaped row look local.

## Authority and evidence used

FOREMAN used the repository `AGENTS.md`, the existing SANDBOX-OUTBOUND-01
handoff, and the installed `odontoflow-engineering`, PostgreSQL best-practices,
security-hardening, TDD, verification-before-completion, API/interface-design,
code-review, and Foreman-handoff skills. Reads were limited to messaging
models/schemas/services/router, IAM/context/credential patterns, migrations,
the local setup, and directly relevant tests.

The implementation reuses the existing `ExecutionContext`,
`require_authenticated_context`, `deliveries.manage`, claim/settle service,
audit staging, and PostgreSQL transaction/tenant conventions. No new trust
flag, caller-supplied delivery assertion, live provider, or consent rule was
inferred.

## What we built and how

1. Extended the closed provider vocabulary with `sandbox` and added a provider
   selector to the existing claim request. The service allowlist is explicit:
   `whatsapp` and `sandbox`; `test` is never externally claimed.
2. Added `sandbox_delivery_receipts` with one receipt per
   `(organization_id, outbound_id)`, a canonical payload SHA-256, a stable
   server-generated provider id, PostgreSQL tenant FKs, and duplicate-safe
   locking. Sandbox successful settlement requires the matching receipt.
3. Added the authenticated `/internal/sandbox/receive` route. It accepts only
   the canonical sandbox text payload, checks the persisted outbound JSON and
   provider, and records/audits the receipt atomically.
4. Added a one-shot `integrations.sandbox.SandboxConsumer` and
   `scripts/sandbox_dispatcher.py`. Configuration requires explicit loopback
   backend/receiver origins, the exact receiver path, and a server-issued
   dispatcher credential. Receiver 5xx/408/429 becomes transient failure;
   malformed/rejected delivery becomes permanent failure. No arbitrary URL or
   provider fallback exists.
5. Added real-PostgreSQL provider, receipt, retry, idempotency, tenant, and
   exclusion regressions; refreshed migration expectations and OpenAPI; added
   `.env.example` and the technical handoff with local commands.

## Execution model

Solo FOREMAN. The shared PostgreSQL test database and tightly coupled
claim/receive/settle transaction make parallel builders or test processes
unsafe and provide no meaningful time benefit.

## Risks, conflicts, and protected surfaces

The principal risk was false local delivery: a consumer could settle a live
WhatsApp row or report success without a receiver accepting the exact stored
payload. Provider claim filtering, the fixed loopback receiver contract,
server-issued IAM, exact payload comparison, receipt uniqueness, and the
sandbox-specific settlement gate address that risk.

The following remained untouched: `app/errors.py`, `app/db.py`,
`app/scheduling/availability.py`, all prior migrations, `../../medistock`,
Sales Agent authentication, fail-closed booking, n8n workflows, provider
billing, production configuration, and unrelated dirty paths. Migration 0019
is additive and its downgrade refuses to discard sandbox accounts or receipts.

## Evidence and validation

TDD red evidence preceded the implementation: the old PostgreSQL provider CHECK
rejected `sandbox`; once the provider selector was added, the new receiver and
consumer tests were red because their route/table/module did not yet exist.
The final focused and migration checks were:

```text
./.venv/bin/python -m pytest -q tests/test_sandbox_outbound.py
10 passed, 2 warnings in 18.48s

./.venv/bin/python -m pytest -q tests/test_migrations.py
9 passed, 20 warnings in 39.43s
```

`tests/test_migrations.py` upgrades a throwaway PostgreSQL database from empty
to head, checks the exact table set, and exercises downgrade/re-upgrade. The
sandbox tests prove persistence, claim isolation, authenticated receipt and
settlement, duplicate replay, success-without-receipt rejection, transient
retry, cross-tenant rejection, configuration fail-closed behavior, and
`test`/`whatsapp` exclusion.

The final serial full backend suite was:

```text
./.venv/bin/python -m pytest -q
545 passed, 21 warnings in 655.14s (0:10:55)
```

Current collection is **545**, versus the historical **527-pass** baseline
and **535** at intake. No failures or skips occurred. Warnings are the
existing Starlette TestClient and Alembic `path_separator` deprecations.
Focused Ruff, compileall, OpenAPI JSON validation, dispatcher CLI help, and
diff checks passed. Technical evidence and exact local startup/smoke commands:
[`backend technical handoff`](../../../../odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-outbound-02.md).

## Decision and progress log

- 2026-09-16 — Verified the blocked prior handoff and backend base
  `ad724350`; no broad reality audit repeated.
- 2026-09-16 — CTO approved a first-class `sandbox` provider and additive
  development/testing migration.
- 2026-09-16 — Wrote and ran the red provider/receiver/consumer regressions;
  implemented the smallest provider-bound receipt/consumer slice.
- 2026-09-16 — Disposable migration, focused real-PostgreSQL tests, relevant
  messaging/auth/tenant pack, static checks, and final full suite passed.
- 2026-09-16 — Bounded backend commit created; planning CAVELOG/STATUS and
  this living brief record the final result.

## Next approval / next step

No next activity is authorized or started automatically. The sandbox path is
only a controlled local development/testing receiver. A future WhatsApp/live
adapter, inbound channel, deployment, model-provider decision, or any patient
consent/automatic-booking mechanism requires its own approved activity.
