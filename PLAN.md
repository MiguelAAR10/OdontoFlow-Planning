---
title: OdontoFlow — Plan (milestones)
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning) — milestone-level only; backend detail lives in backend docs/roadmap.md
---

# Plan — Milestones

## M1 — Vertical 1: Lead → Appointment  — DONE
Commercial lead, catalog, organization/practitioner capability, deterministic
availability, transactional booking (GiST conflict safety), cancel/reschedule,
HTTP E2E. Backend closed; frontend Agenda wired to real API.

## M2 — Platform Foundation PF1–PF4  — DONE
Tenancy, authorization, provenance, idempotent commands (migrations 0001–0004).

## M3 — Clinical Core (PF5)  — DONE
Patient, Visit, ServiceExecution (migration 0005). Frontend Pacientes on real API.

## M4 — Economic & Ops Bridge (PF6)  — DONE
Product, ServiceConsumption, Charge, Payment (migration 0006).

## M5 — Inventory Ledger + PF Closure (PF7)  — DONE
Append-only InventoryMovement, derived balances, consumption→SALIDA, migration 0007,
permission gating on all mutating services, BLOCKER-2 resolved.

## M6 — Platform Foundation closure + Finance follow-ups  — NEXT
architecture.md §9 stragglers; sale stock-out for `reventa`; payment reversal /
method catalog / invoice engine.

## M7 — Multi-location stock & transfers  — NEXT (additive)
`location_id` + TRANSFER movements.

## M8 — External adapters (Calendar, WhatsApp, billing)  — LATER
Adapters around the domain, never domain authorities.

## M9 — Operational optimization / agent execution  — LATER
Agents as Principals over the same deterministic tools; not designed yet.

> Backend roadmap detail, commit history, and gap analysis are owned by the
> backend repo: `docs/roadmap.md`, `docs/backend-evolution.md`, `docs/architecture.md`.
