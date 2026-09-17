# RECEPTION-CORE-CLOSEOUT-01 — FOREMAN living brief

Date: 2026-09-17
Mode: planning only
Status: **NOT DONE — closeout plan persisted; no implementation dispatched**

## Executive status

Reception / Scheduling v1 has a substantial deterministic core, but it is not
yet a complete, publishable component. Catalog, location, practitioner,
tenant-scoped availability, appointment mutation, IAM, audit, and the local
sandbox seam are evidenced against the backend. The end-to-end completion gate
still has unresolved canonical ingress evidence, proposal acceptance/auth
surfaces, truthful agent failure recovery, outbound draining, provider-boundary
tests, and release/runtime reconciliation.

The smallest completion plan is persisted at:
`docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml`.

## Objective and success criteria

Close the business flow:

`lead/patient -> conversation -> service -> location -> practitioner -> deterministic availability -> proposal -> authorized confirmation -> appointment`

The component is DONE only when the YAML plan's DC-1 through DC-9 are all
verified. In particular, a canonical authenticated event must enter once;
AIRY may read current clinic state only through tenant-bound typed tools;
availability is deterministic; proposal and authorized confirmation are
exactly-once; failures leave truthful durable state; n8n remains transport-only;
providers are replaceable at adapter/configuration boundaries; and automatic
agent booking/cancel/reschedule remain intentionally manual and fail closed.

## Repository reality

- Backend: `main@14d918dae1c1cf954f0994f9b39841ac2ffe2969`; after
  `git fetch --prune`, local `main` is 11 commits ahead and 0 behind
  `origin/main@b7f11cef9bac6bbe6eb2a0bd144a541b8032f4bc`.
- Planning: `main@63274e1d59778d9f96ed9b69ab838a8c34db158b`, equal to
  `origin/main`; existing modified/untracked planning files were preserved.
- Frontend was checked only as an integration context: local
  `main@a788df56d2d7f0ea5359da3227bb86fb457ca214` is 1 ahead of its recorded
  remote, but `git fetch --prune` failed because the configured upstream
  repository was not found. It is not a backend completion authority.
- Voice and simulation repositories were not touched; they are frozen by the
  planning control plane.
- No reset, checkout, merge, rebase, clean, product-code edit, schema change,
  provider request, or implementation worker occurred in this activity.

## Authority and evidence used

- Fresh reality: `docs/handoffs/discovery/2026-09-17-reception-core-closeout-01-fresh-reality.yaml`.
- ERP core scout: `docs/handoffs/discovery/2026-09-17-reception-core-closeout-01-reception-core-status.yaml`.
- Integration/runtime scout: `docs/handoffs/discovery/2026-09-17-reception-core-closeout-01-integration-status.yaml`.
- Opus plan and DONE contract: `docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml`.
- Backend technical handoffs named by the plan, including the sandbox,
  OpenRouter, diagnostics, and agent-auth evidence.

Exactly two read-only DeepSeek V4.1 Flash scout sessions were used through the
installed Orca/OpenCode runtime: one ERP-core scout and one
integration/runtime scout. Exactly one Claude Opus planning session was used;
the native model alias `opus` was required after the unavailable
`anthropic/claude-opus-5` alias failed before planning. The initial failed
planner dispatch was closed and the same planner task was retried with the
native alias. No scout or planner was permitted to modify product files.

The scouts reported the canonical inbound 404-versus-401 discrepancy as
unresolved rather than guessing at its cause. The integration packet records
the needed discriminators: effective sender origin/full URL, responding
process, candidate route tables, and port identity.

## What remains, by boundary

The Opus YAML is authoritative for all activity fields, dependencies, write
surfaces, worker classes, tests, definitions of done, and classification.

- **Core business:** canonical proposal list/read/confirm/decline with
  authorized exactly-once confirmation; remove ERP anonymous compatibility
  reliance; regenerate the contract and run one full end-to-end regression.
- **Agent:** produce one bounded real-model result or a named stop; persist one
  tenant-bound human handoff on post-auth failure; make agent cancel/reschedule
  fail closed with the same authority as booking.
- **Channel/integration:** resolve canonical inbound ingress and replay;
  complete bounded sandbox claim/deliver/retry/dead-letter evidence; enforce
  n8n transport-only and provider-boundary contracts.
- **Deployment/release:** publish the verified head, make the agent service
  image start the bounded runtime, and reconcile the remote migration head
  additively and reversibly.

## Execution model

No implementation is authorized by this handoff. The next activity is one
small, evidence-first ingress task: **CHAN-01 — resolve the canonical inbound
404/401 discrepancy and prove authenticated single-entry persistence**. It must
stop before Sales Agent/OpenRouter and must not replay the prior real-model
smokes. After that, the coordinator should dispatch only the next dependency
whose approval and write surface are explicit in the Opus plan.

## Risks, conflicts, protected surfaces

- Do not call OpenRouter, switch models, add fallback routing, or spend provider
  credits during CHAN-01.
- Do not add WhatsApp, deploy n8n, change consent/booking policy, touch
  production data, or create an automatic appointment path.
- Preserve PostgreSQL constraints, tenant composite keys, IAM permissions,
  atomic audit, idempotency, sandbox provider isolation, and the generic
  external error envelope.
- The backend's 11 local-only commits must be reviewed as the intended
  closeout chain before any publication activity; the planning tree's existing
  unrelated dirty state must remain untouched.

## Evidence and validation

This is an audit/plan, not a product change. No pytest suite was run and no
real provider request was made. The YAML artifacts were produced from fresh
repository synchronization plus read-only source, handoff, and control-plane
evidence. Before implementation, each worker must use real PostgreSQL,
focused tests first, and one serial full suite only when its application or
contract change warrants it.

## Decision and progress log

- `RECEPTION-CORE-CLOSEOUT-01`: **PLANNED**, component remains NOT DONE.
- Fresh backend reality supersedes older handoff assumptions that named
  `db527895`, `d6940c6`, or earlier bases; the current audited head is
  `14d918d`.
- No implementation worker was dispatched. The only active follow-up is the
  explicitly named next activity above; it is not started automatically.

## Next approval / next step

Approve or reject the Opus plan as the closeout backlog. If approved, start
only CHAN-01 and return its evidence before any provider smoke or business
feature implementation.
