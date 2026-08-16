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
| **M3 — Frontend Core Integration** | **PARTIAL** |
| **M4 — Pilot Fit** | **NOW** |
| **M5 — First Measured Value** | **NEXT** |
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

## M3 — Frontend Core Integration — PARTIAL
Agenda **REAL** · Patients **REAL** · Cash **PROTOTYPE** · Inventory **PROTOTYPE** ·
Chat **PROTOTYPE** · Agent **PROTOTYPE** (frontend HEAD `6135025`, remote
`leonardopanduro-rgb/ODONTO-SMART-FRONT`).

## M4 — Pilot Fit — NOW
Next activity: integrate CashPage and InventoryPage with existing FastAPI
contracts (`/charges`, `/charges/{id}/payments`, `/products/*`).

## M5 — First Measured Value — NEXT
Platform Foundation closure stragglers; sale stock-out for `reventa`; finance
follow-ups (payment reversal, method catalog, invoice engine).

## M6 — Agentic Operations — LATER
External adapters (calendar/WhatsApp/billing) and agents as Principals over the
same deterministic tools; not designed yet.

> Backend roadmap detail, commit history, and gap analysis are owned by the
> backend repo: `docs/roadmap.md`, `docs/backend-evolution.md`, `docs/architecture.md`.
