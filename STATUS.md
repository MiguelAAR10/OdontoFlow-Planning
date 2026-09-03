---
title: OdontoFlow — Status (verified snapshot)
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning) — numbers re-verified from repos at verify time
---

# Status — Verified Snapshot (2026-09-02)

## Milestone

**CURRENT_MILESTONE = M5 First Measured Value** (M0–M4 CLOSED · M5 NOW · M6 LATER)

**M5 sub-state:** M5.1 Revenue Leakage Measurability **CLOSED** (evidence:
[M5_REVENUE_LEAKAGE_BASELINE.md](M5_REVENUE_LEAKAGE_BASELINE.md)) ·
M5.2 **BLOCKED on real clinic data** (`DOMINANT_LEAKAGE = UNKNOWN`).

## HEADs (verified by git, not by docs)

- **BACKEND_HEAD:** `23527c2` (`main`) — synced with origin
- **BACKEND_REMOTE:** `git@github.com:MiguelAAR10/OdontoFlow.git` — origin/main = `23527c2`
- **BACKEND_TESTS:** 384 PASS (real PostgreSQL, port 5434; full run re-verified 2026-09-02, 171s, exit 0)
- **MIGRATION:** 0008 (alembic 0001–0008 — location-aware inventory + transfers)
- **FRONTEND_HEAD:** `9595abd` (`main`) — synced with canonical origin
- **FRONTEND_REMOTE (canonical):** `git@github.com:MiguelAAR10/odontoflow-frontend.git` — origin/main = `9595abd`
- **FRONTEND_REMOTE (upstream/reference):** `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` — preserved as `leonardo`, at `8769f12`, history untouched, never force-pushed
- **FRONTEND_TESTS:** 83 unit PASS · Pilot E2E 12/12 PASS · Agenda/Patients regression 6/6 PASS (real backend) · typecheck clean · build PASS (last verified 2026-08-17)
- **PLANNING_HEAD:** `1c63f02` (`main`) — synced with origin (before this snapshot's commit)
- **Legacy (medistock):** `ef2fffb` (`main`, synced) — READ ONLY, outside workspace

All three active repos: working tree **clean**, local HEAD **== origin/main**,
`git fetch --all` brought **zero** new upstream commits.

## Canonical environment (verified 2026-09-02)

| Repo | Runtime pin | Database | Test command |
|---|---|---|---|
| backend | Python `3.12` (`.python-version`), `pyproject.toml` (`odontoflow` 0.1.0) | PostgreSQL 15 in `odontoflow-db-1`, `127.0.0.1:5434`; `odontoflow_test` for pytest, `odontoflow_e2e` for the pilot harness | `.venv/bin/python -m pytest -q` |
| frontend | Node `24` (`.nvmrc`) | consumes the backend API | `npm run test` · `npm run test:e2e` · `npm run test:e2e:pilot` · `npm run typecheck` |

Bring the database up with `docker start odontoflow-db-1` (data volume
`odontoflow_odontoflow_pgdata`). Note: running `docker compose up` from
`odontoflow-backend/` derives a *different* compose project name and creates an
**empty** volume — always start the named container instead.

## Contributor sources (NOT canonical business authority)

- **`contrib-odonto-voz/`** — standalone voice service by **Alejandro Marcelo**,
  imported **intact** at `eb9a4ee` (5 commits, full history, own `origin`).
  **READ ONLY**, never pushed, not a submodule, not built by any pipeline.
  Its own tests: **54 PASS / 0.69 s** (re-verified 2026-09-02). Its
  `catalogo.json` is **SYNTHETIC**; its alias vocabulary is genuine product
  knowledge worth preserving.
- **`alejandro/feat/asistente-voz`** = `c0f418d` — donor frontend PR
  [ODONTO-SMART-FRONT#1](https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/pull/1),
  fetched into `odontoflow-frontend` and **left intact**. **Not merged, not
  cherry-picked, not rebased.** Canonical `main` unchanged at `9595abd`.
- Authorship and exact SHAs: [CONTRIBUTIONS.md](CONTRIBUTIONS.md). Synthesis and
  integration order: [VOICE_CONTRIBUTION_INTEGRATION_MAP.md](VOICE_CONTRIBUTION_INTEGRATION_MAP.md).
  Evidence: `.audit/contributions/voice/`. Bundles + checksums:
  `_preservation/odontoflow-contributors-2026-09-02/`.
- **Three of the four requests in the donor's `PETICIONES-A-MIGUEL.md` are
  already solved** by M4.2 (`ADJUSTMENT` type · `reason` mandatory by CHECK ·
  `location_id` + atomic transfers · actor via PF3 audit). They were written
  against the **legacy MediStock schema**, not this backend. Only
  `cantidad_esperada` is genuinely absent — and it is computable from the
  derived balance, so it is deliberately **not** being added speculatively.
- **Open modelling question, not a gap:** the donor emits one `total_bruto` per
  visit while `Charge` is 1:1 with a `ServiceExecution`. The allocation rule is
  a **clinic decision**, not a code decision. Nothing writes money until it is
  answered.

## External activity since the last snapshot

- **One open pull request, on the upstream/reference repo only:**
  [leonardopanduro-rgb/ODONTO-SMART-FRONT#1](https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/pull/1)
  — "Vista Asistente de voz: dictado de inventario y resumen de consulta", by
  `AlejandroMarceloCh`, opened 2026-08-15, +390/−5 over 6 files. It targets
  `leonardo/main` (`8769f12`), **not** the canonical `origin`, and depends on an
  external voice service (`AlejandroMarceloCh/odonto-voz`). Canonical `main` is
  7 commits ahead of that base, so it is not fast-forward mergeable as-is.
  **Not merged, not evaluated** — outside M5 scope; recorded so it is not lost.
- No other commits, branches or PRs appeared on any of the three canonical repos.

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

**One, and it is not technical: no real clinic operational data exists.**

Verified by live row census (2026-09-02) across every database on the instance:
`odontoflow_e2e` holds only the M4.4 pilot fixtures (`Lead E2E Piloto`,
`Bootstrap Clinic`, seeded 2026-08-17 by `.audit/accelerator/seed_e2e.py`), the
dev database `odontoflow` is at migration `0001` with zero rows, and the
frontend seeds are self-declared synthetic. Therefore `DOMINANT_LEAKAGE =
UNKNOWN` and M5.2 cannot start.

Unblocking requires a 90-day clinic export (≥ 300 appointments, ≥ 200 charges,
pseudonymous patient ids — full specification in
[M5_REVENUE_LEAKAGE_BASELINE.md §6](M5_REVENUE_LEAKAGE_BASELINE.md)).

**Contributor intake blockers: none** — both donor sources imported intact,
preserved with verified checksums, fully mapped, zero product code changed. Two
open questions are for the clinic, not for engineering: the real tariff/supply
catalog, and how one visit's total maps to per-treatment charges.

Infrastructure blockers: none. Repos clean and synced; backend suite green.

Known platform limitation (recorded, not a blocker): the donor's E2E harness
`auditar.py` is **macOS-only** (shells out to `say`), so the voice
audio/transcription path is **UNVERIFIED on Linux/WSL** and the donor's latency
figures remain the author's Apple Silicon measurements, not ours.

## Next activity

**NEXT_ACTIVITY = obtain the clinic data sample**, then run experiment
**M5.1-E1 — Revenue Leakage Baseline Extract** (read-only SQL query pack over a
90-day real export in a scratch database; no code, no migration, no
intervention). Specification: [M5_REVENUE_LEAKAGE_BASELINE.md §11](M5_REVENUE_LEAKAGE_BASELINE.md).

M5.1 established that the money surface is exactly measurable today
(execution-without-charge, under-charge, aged outstanding) while **no-show is
not measurable at all** — no no-show state, no appointment resolution state, so
absence of a visit conflates no-show with an unrecorded visit. Instrumenting
that (**I1**, audit-only, no migration) is M5.2 *only if* the real data shows
the ambiguous set is material. Measure first, instrument second.

(Not another planning/architecture/Foundation/migration phase.)