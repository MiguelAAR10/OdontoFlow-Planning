---
title: OdontoFlow — Status (verified snapshot)
status: active
last_verified: 2026-08-17
authority: Repo 0 (planning) — numbers re-verified from repos at verify time
---

# Status — Verified Snapshot (2026-08-17)

## Milestone

**CURRENT_MILESTONE = M5 First Measured Value** (M0–M4 CLOSED · M5 NOW · M6 LATER)

## HEADs (verified by git, not by docs)

- **BACKEND_HEAD:** `28d1e22` (`main`) — synced with origin
- **BACKEND_REMOTE:** `git@github.com:MiguelAAR10/OdontoFlow.git` — origin/main = `28d1e22`
- **BACKEND_TESTS:** 384 PASS (real PostgreSQL, port 5434; verified full run 2026-08-16)
- **MIGRATION:** 0008 (alembic 0001–0008 — location-aware inventory + transfers)
- **FRONTEND_HEAD:** `20f38f1` (`main`) — pushed to origin
- **FRONTEND_REMOTE (canonical):** `git@github.com:MiguelAAR10/odontoflow-frontend.git` — origin/main = `20f38f1`
- **FRONTEND_REMOTE (upstream/reference):** `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` — preserved as `leonardo`, history untouched, not force-pushed
- **FRONTEND_TESTS:** 83 unit PASS · Pilot E2E 12/12 PASS · Agenda/Patients regression 6/6 PASS (real backend) · typecheck clean · build PASS
- **Legacy (medistock):** `ef2fffb` (`main`, synced) — READ ONLY, outside workspace

## Frontend real state (M4 complete)

| Screen | State |
|---|---|
| Agenda | REAL |
| Patients | REAL |
| Cash | REAL (M4.1 — charges/payments via `/charges*`, Idempotency-Key) |
| Inventory | REAL (M4.3 — products, balance by Location, entries, adjustments, kardex, transfers) |
| Chat | PROTOTYPE |
| Agent | PROTOTYPE |

## Backend state (M4 complete)

| Area | State |
|---|---|
| Inventory | REAL — Product × Location (location_id on every movement, composite FK, balance per location, consumption at visit location) |
| Transfers | REAL — atomic TRANSFER_OUT/TRANSFER_IN, one tx, idempotent (PF4), audited |
| Clinical/Economics | REAL — unchanged guarantees intact (PF1–PF4/PF7) |

## Pilot E2E (M4.4 — CLOSED)

Real journey proven end-to-end against real FastAPI + real PostgreSQL with
`VITE_USE_MOCKS=false`: Patient → Appointment (confirmed) → Visit (location
derived) → ServiceExecution → ServiceConsumption → SALIDA at the Visit Location →
other Location unchanged → Charge → partial + full Payment → overpayment rejected
via the real envelope → CashPage reflects paid/outstanding (`loadCharges`) →
InventoryPage reflects the new Location balance (`loadProductBalance`) →
Transfer (conservation + shared `transfer_id`) → kardex + location-isolated
adjustment. Evidence: `odontoflow-frontend/.audit/m4-pilot-fit/pilot-e2e.md`.
Harness (reproducible): `scripts/pilot-e2e.sh`.

Final review (DeepSeek V4 Flash, read-only, one pass): **PASS — no blockers**
(location/tenant integrity, stock authority, transfer atomicity, money
correctness, contract drift, Agenda/Patients/Cash regressions). One repair
applied in the pass: mock-mode overpayment code aligned to the real backend
(`INVALID_INPUT`).

## Tests

- **Backend:** 384 passed (verified full run 2026-08-16; no backend commit in M4.3/M4.4 — the E2E proved zero backend defects)
- **Frontend:** 83 passed / 9 files (unit) · Pilot E2E 12/12 · Agenda+Patients real-backend regression 6/6 · typecheck clean · build PASS

## OpenAPI paths (32, generated at backend HEAD — location-aware)

`/health` · `/leads`(+`/{id}`) · `/appointments`(+`/{id}`, `/cancel`, `/reschedule`) ·
`/availability-rules` · `/schedule-blocks` · `/slots/query` · `/capabilities` ·
`/practitioners`(+`/eligible`) · `/locations` · `/services` · `/patients`(+`/{id}`) ·
`/visits`(+`/{id}`) · `/visits/{visit_id}/executions` · `/executions/{execution_id}/charges` ·
`/executions/{execution_id}/consumptions` · `/charges`(+`/{id}`, `/{charge_id}/payments`) ·
`/products`(+`/{id}`, `/entries`, `/movements`, `/adjustments`, `/balance`, `/transfers`) —
`location_id` required en entries/adjustments (body) y balance/movements (query)

## Latest handoffs

- M4.4 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/pilot-e2e.md` (Pilot E2E + final review)
- M4.3 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/inventory-ui.md` (InventoryPage real)
- M4.1 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/cash-real.md` (CashPage real)
- M4.2 evidence: `odontoflow-backend/.audit/m4-pilot-fit/inventory-backend.md` (location-aware + transfers)
- Contract map: `odontoflow-frontend/.audit/m4-pilot-fit/frontend-contract-map.md`
- Full index: [HANDOFFS.md](HANDOFFS.md)

## Blockers

None. (Frontend push unblocked: canonical remote is now `MiguelAAR10/odontoflow-frontend`;
Leonardo's repo preserved as `leonardo` upstream/reference.)

## Next activity

**NEXT_ACTIVITY = M5 — First Measured Value**: Observe → Detect economic leakage →
Intervene → Measure outcome → Estimate economic effect → Measure delivery/human
cost. (Not another planning/architecture/Foundation/migration phase.)