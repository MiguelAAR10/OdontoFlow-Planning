---
title: OdontoFlow — Status (verified snapshot)
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning) — numbers re-verified from repos at verify time
---

# Status — Verified Snapshot (2026-08-16)

## Milestone

**CURRENT_MILESTONE = M4 Pilot Fit** (M0–M2 CLOSED · M3 PARTIAL · M5 NEXT · M6 LATER)

## HEADs (verified by git, not by docs)

- **BACKEND_HEAD:** `28d1e22` (`main`) — synced with origin
- **BACKEND_REMOTE:** `git@github.com:MiguelAAR10/OdontoFlow.git` — origin/main = `28d1e22`
- **BACKEND_TESTS:** 384 PASS (real PostgreSQL, port 5434; verified full run 2026-08-16)
- **MIGRATION:** 0008 (alembic 0001–0008 — location-aware inventory + transfers)
- **FRONTEND_HEAD:** `54b6e20` (`main`, local)
- **FRONTEND_REMOTE:** `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` — origin/main = `8769f12`
- **FRONTEND_SYNC:** ahead 4, behind 0 — **NOT PUSHED** (remote owned by Leonardo; push denied for MiguelAAR10 — SSH permission denied, ownership not bypassed → preserved locally, SHA `54b6e20`)
- **Legacy (medistock):** `ef2fffb` (`main`, synced) — READ ONLY, outside workspace

## Frontend real state (M4)

| Screen | State |
|---|---|
| Agenda | REAL |
| Patients | REAL |
| Cash | REAL (M4.1 — charges/payments via `/charges*`, Idempotency-Key) |
| Inventory | PROTOTYPE (backend location-aware REAL; UI gated on regenerated contracts) |
| Chat | PROTOTYPE |
| Agent | PROTOTYPE |

## Backend state (M4)

| Area | State |
|---|---|
| Inventory | REAL — Product × Location (location_id on every movement, composite FK, balance per location, consumption at visit location) |
| Transfers | REAL — atomic TRANSFER_OUT/TRANSFER_IN, one tx, idempotent (PF4), audited |
| Clinical/Economics | REAL — unchanged guarantees intact (PF1–PF4/PF7) |

## Tests

- **Backend:** 384 passed (verified full run 2026-08-16; 20 new: 17 location + 3 migration)
- **Frontend:** 54 passed / 8 files (21 new cash: adapter + mocked-axios transport); typecheck clean; build PASS

## OpenAPI paths (32, generated at backend HEAD — location-aware)

`/health` · `/leads`(+`/{id}`) · `/appointments`(+`/{id}`, `/cancel`, `/reschedule`) ·
`/availability-rules` · `/schedule-blocks` · `/slots/query` · `/capabilities` ·
`/practitioners`(+`/eligible`) · `/locations` · `/services` · `/patients`(+`/{id}`) ·
`/visits`(+`/{id}`) · `/visits/{visit_id}/executions` · `/executions/{execution_id}/charges` ·
`/executions/{execution_id}/consumptions` · `/charges`(+`/{id}`, `/{charge_id}/payments`) ·
`/products`(+`/{id}`, `/entries`, `/movements`, `/adjustments`, `/balance`, `/transfers`) —
`location_id` required en entries/adjustments (body) y balance/movements (query)

## Latest handoffs

- M4.1 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/cash-real.md` (CashPage real)
- M4.2 evidence: `odontoflow-backend/.audit/m4-pilot-fit/inventory-backend.md` (location-aware + transfers)
- Contract map: `odontoflow-frontend/.audit/m4-pilot-fit/frontend-contract-map.md`
- `2026-08-16-inventory-and-pf-closure-handoff.md` — PF7 inventory ledger + PF closure, 344→364 PASS
- `2026-08-15-economic-ops-bridge-handoff.md` — PF6, 324 PASS
- `2026-08-15-clinical-core-handoff.md` — PF5, 305 PASS
- Full index: [HANDOFFS.md](HANDOFFS.md)

## Blockers

- Frontend push blocked by ownership (Leonardo's remote). Attempted push verified
  denied for MiguelAAR10 (`ERROR: Permission to leonardopanduro-rgb/ODONTO-SMART-FRONT.git
  denied to MiguelAAR10`). Commit `54b6e20` preserved locally; handoff compacto listo.
- Inventory UI (Phase 2) gated: regenerar contracts TS desde el OpenAPI location-aware.

## Next activity

**NEXT_ACTIVITY = PILOT E2E (real journey: Patient → Appointment → Visit →
Execution → Consumption@Location → Charge → Payment → Cash UI → Inventory UI)**
+ DeepSeek read-only review (location/tenant integrity, stock authority, transfer
atomicity, money correctness, contract drift) + handoff M4.
