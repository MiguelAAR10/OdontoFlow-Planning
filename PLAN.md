---
title: OdontoFlow — Plan (canonical milestones)
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning) — milestone-level only; backend detail lives in backend docs/roadmap.md
---

# Plan — Canonical Milestones

| Milestone | Status |
|---|---|
| **M0 — Repository Recovery** | **CLOSED** (2026-08-16) |
| **M1 — Platform Foundation** | **CLOSED** |
| **M2 — FastAPI Core Migration** | **CLOSED** |
| **M3 — Frontend Core Integration** | **CLOSED** |
| **M4 — Pilot Fit** | **CLOSED** |
| **M5 — First Measured Value** | **NOW** |
| **M6 — Agentic Operations** | **LATER** |

## M0 — Repository Recovery — CLOSED
Canonical workspace `AI-EdgeRunners/odontoflow/` with planning/backend/frontend;
MediStock legacy READ ONLY outside the workspace; recovery bundles preserved in
`_preservation/`; Repo 0 established as git repo with remote `OdontoFlow-Planning`.

## M1 — Platform Foundation — CLOSED
PF1 tenancy · PF2 authorization · PF3 provenance · PF4 idempotent commands
(migrations 0001–0004).

## M2 — FastAPI Core Migration — CLOSED
Vertical 1 (Lead → Appointment) E2E; Agenda read endpoints; PF5 clinical,
PF6 economics, PF7 inventory ledger + PF closure (migrations 0005–0007,
364 tests PASS).

## M3 — Frontend Core Integration — CLOSED
Agenda **REAL** · Patients **REAL** · Cash **REAL** · Inventory **REAL** ·
Chat **PROTOTYPE** · Agent **PROTOTYPE** (frontend HEAD `20f38f1`, canonical
remote `MiguelAAR10/odontoflow-frontend`, Leonardo's repo preserved as
upstream/reference).

## M4 — Pilot Fit — CLOSED (2026-08-17)
- **M4.1 Cash Real** — CLOSED: CashPage on `/charges` + `/charges/{id}/payments`
  (Idempotency-Key, real paid/outstanding, overpayment via backend envelope).
- **M4.2 Multi-branch Inventory** — CLOSED: location_id on every movement,
  balance per Product × Location, consumption at Visit Location, atomic
  transfers (migration 0008, 384 backend tests PASS).
- **M4.3 Inventory Real UI** — CLOSED: products, balance by Location, entries,
  adjustments, kardex, transfers against the regenerated location-aware
  OpenAPI; zero mock business data with `VITE_USE_MOCKS=false`.
- **M4.4 Pilot E2E** — CLOSED: one real journey (Patient → Appointment → Visit →
  Execution → Consumption@Location → Charge → Payment → Cash UI → Inventory UI →
  Transfer) proven 12/12 against real FastAPI + PostgreSQL.
- Final DeepSeek read-only review: **PASS** (one repair applied: mock-mode
  overpayment code aligned to backend `INVALID_INPUT`).

## M5 — First Measured Value — NOW
Observe → Detect economic leakage → Intervene → Measure outcome → Estimate
economic effect → Measure delivery/human cost. (Not a planning/architecture/
Foundation/migration phase.)

## M6 — Agentic Operations — LATER
External adapters (calendar/WhatsApp/billing) and agents as Principals over the
same deterministic tools; not designed yet.

> Backend roadmap detail, commit history, and gap analysis are owned by the
> backend repo: `docs/roadmap.md`, `docs/backend-evolution.md`, `docs/architecture.md`.
