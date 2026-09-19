# CORE-01 — human proposal confirm/decline — FOREMAN handoff

Date: 2026-09-18 · Coordinator: Claude Opus 5 (FOREMAN) · Writer: Claude Sonnet
Mode: owner-authorized implementation · Backend commit `22d6dff`, **not pushed**

## Business outcome

Staff can now see the proposal AIRY produced and turn exactly one into exactly
one appointment, or decline it. Before this change the flow dead-ended: a
proposal could be persisted only behind `POST /agent-tools/call`, agent
confirmation was refused by design, and no authenticated human had any way to
read or act on it. The Reception/Scheduling business flow is now closed end to
end:

`AIRY proposal → persisted pending proposal → authenticated human list/read →
authorized confirm or decline → existing scheduling authority → one PostgreSQL
transaction, receipt and audit.`

DC-5 ("exactly one authorized appointment"), previously **BLOCKED before
CORE-01**, is now satisfied for the human path.

## SubCards completed

| SubCard | Outcome | Evidence |
|---|---|---|
| **A** | Failing tests + DTOs | 12 tests, red for the right reason: 404 on `GET /scheduling/appointment-proposals` |
| **B** | All 7 amendments implemented | `12 passed` |
| **C** | OpenAPI + regression + full suite | 48→52 paths; `16 passed`; `582 passed` |
| **D** | Coordinator-found coverage gap closed | `13 passed`; all 4 routes refuse anonymous callers with 401 |
| **E** | Authoritative re-run against the final tree | `583 passed, 21 warnings in 580.93s` |

A, B, C were the planned decomposition. **D was added by the coordinator** after
review, not by the plan — see *Coverage gap*. E exists only because D added a
13th test and the 582 figure would otherwise have been stale.

## Files changed and why

All six are inside CORE-01's approved write surface. `app/scheduling/service.py`
was in the write surface but **deliberately left untouched** — no shared helper
proved necessary, which is the strongest evidence that the booking authority was
reused rather than reshaped.

| File | Why |
|---|---|
| `app/agent_tools/booking.py` (+211/−42) | `decline_contact_booking_proposal`; `require_human_confirmation(ctx)` extracted; human-scoped temporal guard; location-scoped permission; list/get helpers |
| `app/scheduling/router.py` (+183) | the four tenant-scoped routes; `_authenticate_reviewer`; `_require_human_reviewer`; idempotency dependency |
| `app/scheduling/schemas.py` (+44) | `AppointmentProposalRead` / `Confirm` / `Decline` DTOs |
| `docs/api/openapi.json` / `.yaml` (+1494) | regenerated from the factory, 48→52 paths |
| `tests/test_appointment_proposals.py` (new, 619) | the 13 tests |

## Preserved contracts and invariants

Each verified by the coordinator against the code, not accepted from the
writer's summary:

- **`_book_appointment_core` is still the only appointment-creation authority** —
  one definition (`service.py:326`), two callers (`booking.py:354` proposal
  path, `service.py:450` direct path). Reused, never duplicated or wrapped. No
  `Appointment(...)` construction was added anywhere outside `service.py`.
- **No migration, no new status value.** Decline sets `status = "expired"` and
  records `PROPOSAL_DECLINED_ACTION = "appointment_proposal.declined"` —
  exactly the owner's MVP decision. `alembic/versions/**` untouched.
- **Decline idempotency is structural, not incidental.** The audit write sits
  inside the `status != "expired"` guard; `settle_receipt` sits outside it. A
  replayed decline therefore settles without emitting a second audit event.
- **Confirm guard order**: locked lookup → `require_permission(location_id=…)` →
  `require_human_confirmation(ctx)` → non-pending/expired guard → human-scoped
  later-inbound → `_book_appointment_core`. Agent refusal precedes the replay
  branch, as amendment 4 requires.
- **Handlers are thin** — authenticate, authorize, delegate. No business
  validation in the route layer.
- **Protected surfaces untouched**: `alembic/versions/**`, `errors.py`, `db.py`,
  `availability.py`, `catalog/schemas.py`, `agent_tools/reception.py`,
  `app/__init__.py`, `conftest.py`.
- **All 8 pre-existing scheduling routes intact** — verified by before/after
  route inventory, after a stray edit had transiently removed one (below).
- **OpenAPI diff was purely additive** (1494 insertions, 0 deletions), so no
  existing API contract changed.

## Accepted deviations

Three, each reviewed against the diff before acceptance:

1. **Removed the "already-confirmed → return the existing appointment"
   shortcut**, folded into the generic non-pending guard. Required for
   exactly-one-winner under concurrent confirm. Same-key replay is settled by
   `run_idempotent_command` *before* this function is entered, so replay never
   reaches the removed branch — confirmed in the guard ordering and by the
   replay test (200/200, no second appointment). The residual risk was on the
   agent path, which is why the two agent suites were run: 16 passed.
2. **The new routes call `require_authenticated_context` directly** rather than
   as a FastAPI dependency. As a dependency it made FastAPI auto-declare an
   OpenAPI security requirement, violating `test_security_boundary.py`'s
   contract that only `/internal/` and `/agent-tools/` operations may declare
   security. Enforcement is unchanged — `_authenticate_reviewer(request)` is the
   first statement in all four handlers and `_require_human_reviewer(ctx)` runs
   before `run_idempotent_command` — and this is now proven empirically at 401,
   not merely by reading.
3. **A SubCard-A fixture bug fixed**: seeded proposals used 2026-09-01 (a
   Tuesday) against a Monday-only availability rule, causing false
   `SLOT_BLOCKED` on intended-success paths. Changed to 2026-08-31 (Monday). No
   assertion was weakened — zero `!= 200` / `in (...)` / `>= 400` patterns
   remain in the file.

## Defects found and repaired during the activity

- **A stray edit deleted the `POST /appointments/{id}/reschedule` decorator**,
  silently unregistering an existing route. The writer caught it during OpenAPI
  verification and restored it; the coordinator independently confirmed via a
  before/after route inventory that all 8 pre-existing routes are present. This
  is the clearest argument for verifying the diff rather than the summary.
- The OpenAPI security-metadata violation (deviation 2).

## Coverage gap found by the coordinator

None of the original 12 tests asserted that the four new routes reject an
**unauthenticated** caller — the precise invariant amendment 2 exists to create.
It was closed in SubCard D, with the writer explicitly instructed to report a
defect rather than weaken the assertion if any route failed to refuse. Result:
all four return **401 `AUTHENTICATION_REQUIRED`**, discovered empirically from
`app/iam/credentials.authenticate()`, with zero appointments created and
proposal status unchanged. No defect.

## Tests actually executed

Every figure below was run; none is inferred.

| Command | Result |
|---|---|
| `python -m pytest tests/test_appointment_proposals.py -x -q` (SubCard A, red) | `1 failed, 2 warnings in 2.75s` — 404, route absent |
| `python -m pytest tests/test_appointment_proposals.py -q` (B) | `12 passed` |
| `python -m pytest tests/test_agent_booking_phase4.py tests/test_reception_agent_phase5.py -q` | `16 passed` |
| `python -m pytest -q` (C) | `582 passed, 21 warnings` |
| `python -m pytest tests/test_appointment_proposals.py -q` (D) | `13 passed` |
| `python -m pytest -q` (E, authoritative) | **`583 passed, 21 warnings in 580.93s (0:09:40)`** |

583 = 570 pre-CORE-01 baseline + 13. Zero failures, no regression. All against
real local PostgreSQL, run serially; no concurrent pytest at any point.

The 13 tests: tenant-scoped list; cross-tenant non-disclosure; cross-location
denial; confirm books exactly one appointment with one audit and one receipt;
same-key replay without duplication; two concurrent confirms yield one winner;
expired confirm fails closed; slot-conflict fails closed; decline expires the
proposal and reopens the conversation; repeat decline idempotent without
duplicate audit; declining a confirmed proposal refused; agent confirm refused
before any replay return; unauthenticated caller refused on all four routes.

## PostgreSQL evidence

Real local PostgreSQL throughout — zero mocks in the test file
(`mock|MagicMock|monkeypatch` count = 0). Concurrency is enforced by the
existing row lock: `with_for_update()` on the proposal in both confirm and
decline, with the practitioner GiST exclusion constraint remaining the ultimate
race authority. The `expired` value was reused precisely because the existing
`CHECK (status IN ('pending','confirmed','expired'))` constraint cannot admit a
fourth value without a migration, which was not authorized.

## OpenAPI

Regenerated with `.venv/bin/python scripts/generate_openapi.py` — the
repository's own process, never hand-edited. 48 → 52 paths; the four new
operations present; diff purely additive.

## Commit

**Backend `22d6dff`** — exactly the 6 write-surface files, +2509/−42. Parent
`8fcd9e1`. `origin/main` remains `193d48b`; the branch is **3 ahead, unpushed**.

**Planning `f99790e`** — 4 files: this handoff, `CAVELOG.md`,
`orchestration/current-activity.yaml` (CORE-01 recorded and closed at
`lifecycle_state: DONE`) and `orchestration/test_route.py`. Parent `33a6759`;
`origin/main` remains `8d61f3a`, the branch is **2 ahead, unpushed**.

Pre-existing work left untouched and uncommitted: backend `AGENTS.md` (+7) and
`.gitignore` (+1) plus 85 untracked paths; planning keeps 34 untracked paths.
Frontend was not touched at all — still `a788df5`, 19 dirty tracked files, zero
commits from this activity.

## Orchestration

Run `run_1514e1bd8481`. **One writer throughout** — the same terminal
(`term_d54321d8…`) carried SubCards A→E, with the backend checkout reused and
no new worktree created.

## Blockers and remaining risks

- **CORE-02 is not closed and was deliberately not pre-empted.** The other seven
  scheduling routes still rely on the `ERP_ANONYMOUS_COMPAT` fallback and do not
  check bearer tokens. This is a documented, intentional pilot decision in
  `app/__init__.py`, not a regression introduced here. CORE-01's four routes are
  independent of it.
- **`expired` cannot distinguish explicit decline from TTL expiry or
  supersession** in the status column alone; the audit action carries that
  distinction. If a read model later needs it in the column, that is a separate
  additive migration activity.
- **The agent_tools/scheduling layering compromise stands** — proposal commands
  live in `app/agent_tools/booking.py` while the HTTP routes live under
  scheduling. Bounded and deliberate; no refactor was attempted.
- **Patient-message consent semantics are still out of scope.** The temporal
  guard is not consent classification; CORE-01 implements operator-mediated
  confirmation only.
- **A residual Orca terminal** from the failed first dispatch
  (`term_2ff7fef1…`) remains running at an idle prompt. `worker-release`
  returned `identity_unproven / processAction: none` — Orca declines to reclaim
  a process it cannot prove it owns, and it was not force-killed outside the
  lifecycle mechanism. It is fenced: capability revoked, orchestration cannot
  feed it. Close it from the Orca UI.

## Process failure worth recording

The first dispatch (`ctx_caf2cc7fe68f`, all three SubCards in one task, host
`effortLevel=high`) ran 11h24m in a single turn. The coordinator judged it hung
and dispatched a replacement — **but it was alive**, and resumed writing after
being stopped. That put two writers on
`tests/test_appointment_proposals.py`, violating `max_parallel_writers: 1`. The
old worker detected it and escalated; Orca had already revoked its capability,
so it stopped. No corruption resulted (verified: clean full overwrite, 13 unique
tests, no conflict markers), but the violation was real. The corrected pattern —
one narrow SubCard per dispatch, named fixture anchors, explicit `--effort
medium`, and terminal reuse for follow-ups — produced SubCard A in under two
minutes.

## Next activity

**Owner decision required.** CORE-01 is complete; nothing here authorizes what
follows. `RECEPTION-CORE-CLOSEOUT-01` lists **CORE-02** (close the
`ERP_ANONYMOUS_COMPAT` seam) as the natural successor and it is now
dependency-ready, since CORE-01 was its only listed dependency. AGENT-02,
AGENT-03, CHAN-03 and CHAN-04 remain ready by ordering, not by approval.

Nothing was pushed, merged or deployed. No other Activity Card was started.
