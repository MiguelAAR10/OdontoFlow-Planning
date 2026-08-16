---
title: OdontoFlow — Status (verified snapshot)
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning) — numbers re-verified from repos at verify time
---

# Status — Verified Snapshot (2026-08-16)

## HEADs (verified by git, not by docs)

- **Backend:** `9bb7361` (`main`, ahead 5 of origin/main) — clean working tree
- **Frontend:** `6135025` (`main`, ahead 2 of origin/main) — clean working tree
- **Legacy (medistock):** `ef2fffb` (`main`, synced) — READ ONLY
- **Migrations:** 0001–0007 (alembic)

## Tests

- **Backend:** 364 passed (per 2026-08-16 handoff; 355 `def test_` collected
  statically at verify time, suite runs against real PostgreSQL on port 5434)
- **Frontend:** vitest suite present (`test/`: simulation, adapters, e2e agenda,
  reminder-flow, ui); typecheck via `tsc -p tsconfig.json`

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

## Current phase

**M5 DONE / M6 NEXT** — Platform Foundation closure + finance follow-ups are the
open roadmap work; frontend Caja/Inventario/Chat/Agente remain MOCK until their
domain authority exists.

## Blockers

None currently known. (BLOCKER-2 resolved at the PF-closure commit.)

## Next activity

Platform Foundation closure review (`docs/architecture.md` §9 stragglers in the
backend repo) — **not started**.
