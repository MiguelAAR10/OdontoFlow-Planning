---
title: OdontoFlow — Project Control Plane
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning) — navigation and status authority
---

# OdontoFlow

Multi-tenant dental clinic platform. FastAPI/PostgreSQL domain authority with a
React frontend, evolved from the MediStock legacy reference.

## Product Vision

A clinical operating platform where the **backend domain is the single source of
truth** (durations, availability, permissions, provenance, idempotency) and the
frontend adapts to the real API contract — never the reverse.

## Current Milestone

**PF7 CLOSED** — inventory ledger + full PF closure (migrations 0001–0007,
364 backend tests). Frontend integrated with real API for Agenda and Pacientes;
remaining screens stay MOCK until their domain authority exists.

## Repo Map

Workspace root: `~/projects/portfolio/AI-EdgeRunners/odontoflow/`

| Path | Role |
|---|---|
| `odontoflow-planning/` | Repo 0 — project control plane (this repo, not versioned) |
| `../odontoflow-backend/` | FastAPI product repository — domain authority |
| `../odontoflow-frontend/` | React SPA — Leonardo's product repository |

Fuera del workspace (legado respetado, NO tocar):
`~/projects/portfolio/AI-EdgeRunners/medistock/` — Legacy reference — READ ONLY

## Navigation

- [REPOSITORIES.md](REPOSITORIES.md) — repo roles, remotes, write policy
- [PLAN.md](PLAN.md) — project milestones
- [FLOW.md](FLOW.md) — real domain flow with DONE/NOW/NEXT/DEFERRED marks
- [STATUS.md](STATUS.md) — verified snapshot (HEADs, tests, OpenAPI, phase)
- [HANDOFFS.md](HANDOFFS.md) — index of backend implementation handoffs
- [CAVELOG.md](CAVELOG.md) — decision log
- [.audit/recovery/](.audit/recovery/) — repository + traceability forensic inventory (2026-08-16)

Acceso rápido: backend `cd ../odontoflow-backend` · frontend `cd ../odontoflow-frontend` · legado (solo lectura) `cd ../../medistock`
