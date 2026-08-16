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

- **BACKEND_HEAD:** `c85ccd8` (`main`) — synced with origin
- **BACKEND_REMOTE:** `git@github.com:MiguelAAR10/OdontoFlow.git` — origin/main = `c85ccd8`
- **BACKEND_TESTS:** 364 PASS (real PostgreSQL, port 5434)
- **MIGRATION:** 0007 (alembic 0001–0007)
- **FRONTEND_HEAD:** `2908cd1` (`main`)
- **FRONTEND_REMOTE:** `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` — origin/main = `8769f12`
- **FRONTEND_SYNC:** ahead 3, behind 0 — **NOT PUSHED** (remote owned by Leonardo; no push credentials/policy → preserved locally + bundle)
- **Legacy (medistock):** `ef2fffb` (`main`, synced) — READ ONLY, outside workspace

## Frontend real state (M3/M4)

| Screen | State |
|---|---|
| Agenda | REAL |
| Patients | REAL |
| Cash | PROTOTYPE |
| Inventory | PROTOTYPE |
| Chat | PROTOTYPE |
| Agent | PROTOTYPE |

## Tests

- **Backend:** 364 passed (verified full run 2026-08-16)
- **Frontend:** vitest suite present (`test/`: simulation, adapters, e2e agenda,
  reminder-flow, ui); typecheck clean (`tsc -p tsconfig.json`)

## OpenAPI paths (31, generated at backend HEAD)

`/health` · `/leads`(+`/{id}`) · `/appointments`(+`/{id}`, `/cancel`, `/reschedule`) ·
`/availability-rules` · `/schedule-blocks` · `/slots/query` · `/capabilities` ·
`/practitioners`(+`/eligible`) · `/locations` · `/services` · `/patients`(+`/{id}`) ·
`/visits`(+`/{id}`) · `/visits/{visit_id}/executions` · `/executions/{execution_id}/charges` ·
`/executions/{execution_id}/consumptions` · `/charges`(+`/{id}`, `/{charge_id}/payments`) ·
`/products`(+`/{id}`, `/entries`, `/movements`, `/adjustments`, `/balance`)

## Latest handoffs

- `2026-08-16-inventory-and-pf-closure-handoff.md` — PF7 inventory ledger + PF closure, 344→364 PASS, VERDICT PASS
- `2026-08-15-economic-ops-bridge-handoff.md` — PF6, 324 PASS
- `2026-08-15-clinical-core-handoff.md` — PF5, 305 PASS
- Full index: [HANDOFFS.md](HANDOFFS.md)

## Blockers

- Frontend push blocked by ownership (Leonardo's remote; no credentials). Commit
  `2908cd1` preserved locally and in `_preservation/` bundle.

## Next activity

**NEXT_ACTIVITY = Integrate CashPage and InventoryPage with existing FastAPI contracts.**
(`/charges`, `/charges/{id}/payments`, `/products/*` — not started)
