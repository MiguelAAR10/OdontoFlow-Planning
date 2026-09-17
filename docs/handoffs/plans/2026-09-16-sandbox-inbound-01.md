# SANDBOX-INBOUND-01 — Controlled end-to-end sandbox loop — FOREMAN living brief

## Executive status

**PASS — controlled sandbox inbound-to-outbound loop verified at backend
commit `22e2b51011a83fbf1e2c745aecda29b44265c71e`; no next activity started.** The development-only
sender uses the existing authenticated inbound, Sales Agent, outbound, and
sandbox-consumer boundaries. The fake model's same-turn booking attempt remains
fail closed, with zero appointments created.

## Objective and success criteria

Close one controlled local loop:

```text
sandbox input → canonical inbound → authenticated Sales Agent turn
  → sandbox outbound → authorized sandbox consumer → local receipt
```

The acceptance proof must show one canonical inbound message, one agent reply
persisted as a sandbox outbound, one durable sandbox receipt, a pending
proposal if the fake model proposes, and zero appointments. Replaying the same
input must not create another inbound message, agent-driven outbound, or
delivery. Missing/invalid credentials and cross-tenant use must fail at the
existing boundaries.

Explicit exclusions: WhatsApp, n8n deployment, paid models, automatic agent
booking, new consent semantics, IAM redesign, human login, production data,
schema changes, and a generic channel framework.

## Repository reality

Backend intake is `main@872ddd2915be186fdda8f5bb195b142c49bd6843`, the PASS
commit for SANDBOX-OUTBOUND-02. The worktree already contains unrelated
modified/untracked paths (`.gitignore`, `AGENTS.md`, skill/tooling folders,
architecture/review material, and earlier handoffs); they must remain
unstaged and untouched.

Relevant existing contracts are real PostgreSQL canonical inbound persistence
at `app/messaging/router.py` and `service.py`, authenticated
`/sales-agent/turn` at `sales_agent/api.py`, the API-first typed gateway and
fake-model runtime path in `sales_agent/`, canonical outbound enqueue, and the
loopback-only sandbox consumer in `integrations/sandbox/consumer.py`. The
checked-in WF-01 harness/export is intentionally `provider=test` and is not a
sandbox shortcut.

## Authority and evidence used

FOREMAN is using the backend `AGENTS.md`, SANDBOX-OUTBOUND-02 technical
handoff, LOCAL-RUNTIME-SMOKE-01 and W4 handoffs/tests, plus the installed
`odontoflow-engineering`, TDD, PostgreSQL, security-hardening,
verification-before-completion, code-review, and Foreman-handoff skills. These
establish API-first agent access, server-side tenant/auth authority, real
PostgreSQL tests, provider isolation, and one bounded commit. No new consent
or booking authority is inferred.

## What we will build and how

1. Add a small sandbox sender/adapter with strict local configuration and
   server-issued inbound and agent credentials. It will normalize a fixed
   `sandbox` inbound event and call the existing HTTP contracts in order.
2. Stop on canonical inbound dedupe before invoking the agent again; do not
   add a second conversation store or retry the mutating agent turn.
3. Reuse the existing injected `GenericFakeChatModel`/`SalesAgentRuntime` in a
   real-PostgreSQL integration test. The same-turn fake confirmation must leave
   a proposal pending under the already-shipped fail-closed guard.
4. Reuse `SandboxConsumer` for claim → receiver → settlement and assert the
   durable database state and replay behavior.
5. Add only the local startup/smoke commands and generated contract updates
   required by the checked-in adapter; no live runtime or paid provider.

## Execution model

Solo FOREMAN. The shared PostgreSQL test database and coupled inbound/agent/
outbound/consumer sequence make parallel builders or pytest processes unsafe.

## Risks, conflicts, and protected surfaces

The main risk is allowing an adapter to treat model output as booking or to
turn a duplicate/replayed inbound into a second business action. The sender
will pass only canonical IDs to the Sales Agent, use the existing typed tools,
and rely on PostgreSQL/provider/auth boundaries. It will not inspect or invent
consent, call booking directly, or fall back to `test`/`whatsapp`.

Protected paths remain `app/errors.py`, `app/db.py`,
`app/scheduling/availability.py`, existing migrations, `../../medistock`, and
unrelated dirty files. No migration is expected because `sandbox` and its
outbound receipt contract already exist.

## Evidence and validation

TDD red evidence was captured before implementation: the new regression
collected 2 failures and 1 existing passing test because
`integrations.sandbox.sender` did not yet exist. The corrected real-
PostgreSQL sandbox-inbound suite is **5 passed / 2 warnings**. The focused
booking, Sales Agent, reception, messaging, outbound, and sandbox pack is
**59 passed / 2 warnings**. The serial full backend suite is **550 passed / 21
warnings** in 444.49 seconds, with no skips. Current collection is 550 versus
the historical 527-pass baseline and the previous 545-test outbound result.
Focused Ruff and `git diff --check` pass for the bounded change. The exact
flow/database evidence and local commands are in the linked backend handoff:
`odontoflow-backend/docs/superpowers/handoffs/2026-09-16-sandbox-inbound-01.md`.

## Decision and progress log

- 2026-09-16 — Verified base commit and unrelated dirty state; no broad
  reality audit repeated.
- 2026-09-16 — Confirmed existing inbound, Sales Agent auth, fake-model,
  canonical outbound, and sandbox consumer contracts are sufficient to try a
  thin adapter without a new product/schema decision.
- 2026-09-16 — TDD red phase confirmed the sender was absent; implementation
  added only the strict sandbox sender and focused real-PostgreSQL regressions.
- 2026-09-16 — PASS: one sandbox inbound persisted exactly once, the existing
  fake model proposed and failed closed on same-turn confirmation, one sandbox
  outbound reached one durable loopback receipt, and replay added no business
  actions. Missing/invalid credentials, cross-tenant ingress, and
  test/whatsapp provider misuse failed closed.

## Next approval / next step

No next activity is authorized or started automatically. The bounded sender is
ready for the controlled local fake-model smoke only. WhatsApp, n8n, paid
models, automatic booking, consent semantics, deployment, and production data
remain outside this activity.
