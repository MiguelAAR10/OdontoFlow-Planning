# CORE-02 — Secure Reception/Scheduling authentication

Date: 2026-09-22
Status: **PASS — implemented, reviewed, committed and published**

## Business objective and delivered behavior

CORE-02 closes the implicit `ERP_ANONYMOUS_COMPAT` identity on the protected
Lead-to-Appointment and Reception/Scheduling API boundary. Missing or invalid
credentials now receive `401 AUTHENTICATION_REQUIRED` on 31 protected route
operations while the compatibility flag is enabled. The existing bearer IAM
dependency creates the `ExecutionContext` first; endpoint handlers reuse that
context and therefore keep the existing permission and tenant contracts.

The four CORE-01 proposal operations were already direct-authenticated. They
now reuse the router-level cached context, so proposal list/read/confirm/decline
still require a credential and the human-only confirmation gate remains in
place. Economics and inventory routes remain on their approved compatibility
path; health and documentation endpoints remain public.

## Verified repository heads and publication

| Repository | Verified state | Publication |
|---|---|---|
| `odontoflow-backend` | CORE-01 base `22d6dff3774b45b3201c0f6ac41dd484f4d5fdda`; CORE-02 `59be27678d7cc46041befe93206242f34ed145de` | `origin/main` = `59be27678d7cc46041befe93206242f34ed145de` |
| `odontoflow-planning` | pre-change `f7cbe32d2033276a699efc8e10ffa4086da1dfc0`; planning closeout commit recorded below | pushed after closeout commit |

CORE-01 history was verified and published before CORE-02: backend remote
`22d6dff3774b45b3201c0f6ac41dd484f4d5fdda`; planning remote
`f7cbe32d2033276a699efc8e10ffa4086da1dfc0`. Both pushes were normal
fast-forwards after fresh fetch and ancestry checks.

## Live write-authority reconciliation

- Orca runtime `f1fe0a66-6263-4e57-a678-eac2acc9f9de` was healthy and the
  version-matched `orca-ide` executable was used throughout.
- Historical CORE-01 terminal `term_2ff7fef1-018b-4c73-b8ae-35adf963a840`
  was absent from the complete live-terminal inventory. Its known failed
  dispatch, abandoned worker, revoked capability, settled stop and
  `processAction=none` were treated as bookkeeping residue.
- The only reported live backend shell,
  `term_fc74c4f0-221c-4c15-abfd-2fea6deb6635`, was connected at the backend
  `main` prompt, had no task or dispatch association, and had no active writer
  capability. It was an idle coordinator/human shell, so the exclusive-write
  gate was SAFE.
- CORE-02 Run `run_7e46837e9c83`; writer Task `task_ef045f8e0371`; writer
  Dispatch `ctx_78573cf4782a`; writer terminal
  `term_eb2e84d9-2e44-4c50-889e-fe473b179ca5`; resource completed with
  `workerState=succeeded`, `dispatchStatus=completed`.
- Writer release returned the supported lifecycle result
  `state=retained`, `reason=user_takeover`, `processAction=none`; the terminal
  is identified, idle at the completed prompt, and has no active task.
- Independent reviewer Task `task_811559ec5bbb`; Dispatch
  `ctx_bce609ff0148`; terminal `term_9069cd99-dd18-4484-a6bb-8da0cef37946`.
  Reviewer release returned the same identified retained/user-owned bookkeeping
  state. No unidentified process was killed and no unrelated terminal was
  touched.

## Protected route inventory

The complete machine-readable matrix is
[`2026-09-22-core-02-route-matrix.yaml`](2026-09-22-core-02-route-matrix.yaml).
The 27 operations below previously reached `resolve_http_context` and could
use the compatibility system identity; the four proposal operations already
performed direct authentication and are included to show the complete
protected boundary.

| Method | Path | Existing permission | Regression evidence |
|---|---|---|---|
| GET | `/leads` | `leads.read` | `leads_list_requires_auth` |
| POST | `/leads` | `leads.create` | `leads_create_requires_auth` |
| GET | `/leads/{lead_id}` | `leads.read` | `lead_read_requires_auth` |
| POST | `/services` | `services.manage` | `services_create_requires_auth` |
| GET | `/services` | `services.read` | `services_list_requires_auth` |
| GET | `/locations` | `locations.read` | `locations_list_requires_auth` |
| POST | `/locations` | `locations.manage` | `locations_create_requires_auth` |
| POST | `/practitioners` | `practitioners.manage` | `practitioners_create_requires_auth` |
| POST | `/capabilities` | `capabilities.manage` | `capabilities_create_requires_auth` |
| GET | `/practitioners/eligible` | `practitioners.read` | `eligible_practitioners_requires_auth` |
| POST | `/patients` | `patients.create` | `patients_create_requires_auth` |
| GET | `/patients` | `patients.read` | `patients_list_requires_auth` |
| GET | `/patients/{patient_id}` | `patients.read` | `patient_read_requires_auth` |
| POST | `/visits` | `visits.create` | `visits_create_requires_auth` |
| GET | `/visits` | `visits.read` | `visits_list_requires_auth` |
| GET | `/visits/{visit_id}` | `visits.read` | `visit_read_requires_auth` |
| GET | `/visits/{visit_id}/executions` | `executions.read` | `visit_executions_requires_auth` |
| GET | `/executions` | `executions.read` | `executions_list_requires_auth` |
| POST | `/visits/{visit_id}/executions` | `executions.create` | `execution_create_requires_auth` |
| POST | `/availability-rules` | `availability.manage` | `availability_rule_requires_auth` |
| POST | `/schedule-blocks` | `availability.manage` | `schedule_block_requires_auth` |
| POST | `/slots/query` | `availability.read` | `slot_query_requires_auth` |
| GET | `/appointments` | `appointments.read` | `appointments_list_requires_auth` |
| GET | `/appointments/{appointment_id}` | `appointments.read` | `appointment_read_requires_auth` |
| POST | `/appointments` | `appointments.create` | `appointment_create_requires_auth` |
| POST | `/appointments/{appointment_id}/cancel` | `appointments.cancel` | `appointment_cancel_requires_auth` |
| POST | `/appointments/{appointment_id}/reschedule` | `appointments.reschedule` | `appointment_reschedule_requires_auth` |
| GET | `/scheduling/appointment-proposals` | `appointments.read` | existing CORE-01 proposal auth/regression tests |
| GET | `/scheduling/appointment-proposals/{proposal_id}` | `appointments.read` | existing CORE-01 tenant/auth tests |
| POST | `/scheduling/appointment-proposals/confirm` | `contact_appointments.book` | existing human-only confirm tests |
| POST | `/scheduling/appointment-proposals/decline` | `contact_appointments.book` | existing human-only decline tests |

The existing `/agent-tools/*` and `/internal/*` operations remain explicitly
authenticated. `/health`, `/docs`, `/redoc`, and `/openapi.json` remain public
according to their existing contracts.

## Implementation and preserved contracts

Changed backend files:

- `app/__init__.py` adds the existing `require_authenticated_context`
  dependency to the catalog, clinical, commercial, organization and scheduling
  routers alongside the already protected integration routers.
- `app/context.py` documents and preserves the cached `ExecutionContext` seam;
  only unrelated economics/inventory routers can still use the compatibility
  fallback.
- `app/scheduling/router.py` removes the proposal-specific second credential
  parse and reads the already authenticated context while retaining the
  human-principal allow-list.
- `tests/test_core02_business_auth_boundary.py` adds the focused contract;
  `tests/test_security_boundary.py` updates the intentional protected-route
  inventory and leaves the legacy compatibility tests on `/products`.
- `docs/api/openapi.json` and `docs/api/openapi.yaml` were regenerated through
  `scripts/generate_openapi.py`; the change is additive security metadata.
- `CHANGELOG.md` records the bounded closeout.

IAM permission evaluation, organization identity sourcing from the credential,
tenant-scoped reads and mutations, idempotency receipts, audit events,
deterministic availability, appointment locks/exclusion semantics, proposal
binding/expiry/confirmation/decline, and agent confirmation refusal were not
rewritten. No migration, new authentication framework, scheduling algorithm,
frontend, integration, deployment, or production database change was made.

## Verification evidence

- Pre-change real-PostgreSQL baseline: `pytest -q` → **583 passed, 21
  warnings**. The coordinator run completed in 623.71s; the writer's captured
  baseline artifact completed in 518.03s. An earlier attempt while the
  documented container was stopped produced 583 connection errors; the
  canonical `odontoflow-db-1` container was restarted and became healthy before
  the valid baseline.
- Test-first red: `tests/test_core02_business_auth_boundary.py` was run with
  only the new tests present and the three implementation files temporarily
  stashed; **56 of 57 cases failed** with the pre-change anonymous behavior.
- Focused green: **57 passed** in the new CORE-02 file.
- Requested auth/tenant/proposal/agent regression pack: **142 passed**.
- Final full serial PostgreSQL suite: **640 passed, 21 warnings in 683.93s**.
  No tests were deleted, weakened, skipped or xfailed.
- OpenAPI comparison found **31 operation-level security additions**, no
  non-security operation changes, and 52 total documented paths. The generated
  YAML and JSON agree.
- Independent read-only review: **PASS**, no repair. The reviewer confirmed
  all 31 target operations, the compatibility bypass boundary, tenant
  isolation, proposal human-only behavior, agent fail-closed behavior, and no
  credential logging or duplicated IAM logic.

## Commits, blockers and next activity

- Backend commit: `59be27678d7cc46041befe93206242f34ed145de`; remote SHA verified
  at `origin/main` after a normal fast-forward push.
- Planning artifact commit: `f020eb2ffe1ae9a3c898d6f61052480b976621aa`;
  `origin/main` was verified at the same SHA after a normal fast-forward push.
  This SHA contains the route matrix, CAVELOG, current-activity update and this
  handoff. The documentation-only annotation that records this verification is
  the subsequent planning commit; the final planning head is reported in the
  closeout status.
- Residual runtime bookkeeping: the two completed Orca worker terminals remain
  identified and retained as `user_owned` with `processAction=none`; their
  tasks are completed and no writer is active. The owner can close those idle
  panes through the Orca UI if desired.
- No CORE-02 product blocker remains. The next activity is an owner-selected
  planning decision; do not auto-start AGENT-02, AGENT-03, CHAN-03, deployment,
  frontend, n8n, WhatsApp or OpenRouter work.
