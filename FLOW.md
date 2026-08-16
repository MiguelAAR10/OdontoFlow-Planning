---
title: OdontoFlow — Domain Flow
status: active
last_verified: 2026-08-16
authority: backend repo (domain model) — this file is navigation only
---

# Domain Flow

Real flow, as implemented at backend HEAD `9bb7361` (migrations 0001–0007).

```
Lead
 → Appointment          [book/reschedule/cancel — idempotent, conflict-safe]
 → Patient              [clinical; per-org DNI; visit origin or walk-in]
 → Visit                [attended encounter]
 → ServiceExecution     [per-visit executed services, price snapshot]
 → Charge/Payment       [1:1 charge per execution, N:1 payments, derived paid/outstanding]
 → ServiceConsumption/Inventory  [consumption anchored to execution; ledger movement ENTRADA/SALIDA/ADJUSTMENT]
```

Legend per stage (implemented capability):

| Stage | Mark | Status |
|---|---|---|
| Lead → Appointment (Vertical 1) | DONE | booking, availability, cancel/reschedule, E2E |
| Patient / Visit / ServiceExecution (PF5) | DONE | migration 0005 |
| Charge / Payment (PF6) | DONE | migration 0006 |
| ServiceConsumption / Inventory ledger (PF7) | DONE | migration 0007; negative-balance guard |
| Sale stock-out for `reventa` products | NEXT | movement exists; invoice linkage deferred |
| Payment reversal / method catalog / invoice engine | NEXT | deferred finance follow-ups |
| Multi-location stock & transfers | NEXT | additive (`location_id` + TRANSFER) |
| External adapters (calendar/WhatsApp/billing) | DEFERRED | adapters only, never domain authority |
| Agent execution as Principals | DEFERRED | not designed yet |

Notes:

- `ServiceConsumption` is anchored to a real `ServiceExecution`; consumption
  writes a SALIDA ledger movement in the same transaction (DB trigger).
- No direct mutable-stock decrements anywhere; `InventoryBalance` is derived at
  read time from the append-only ledger.
