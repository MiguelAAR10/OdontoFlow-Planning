---
title: OdontoFlow — Project Control Plane
status: active
last_verified: 2026-08-17
authority: Repo 0 (planning) — navigation and status authority
---

# OdontoFlow

A **deterministic, multi-tenant clinic operations platform** for dental clinics — the operational ERP
where humans, agents and integrations operate the **same** domain layer under the **same** rules.

## The value proposition (why it exists)

Dental clinics run on referrals, appointments, consumables and cash — and most of that lives in
spreadsheets, WhatsApp and memory. OdontoFlow turns the whole operating loop into **one truthful
transactional system**:

- **CRM → Scheduling**: a commercial Lead becomes a confirmed Appointment, with availability and
  conflicts enforced by PostgreSQL (a practitioner can never be double-booked, even under a race).
- **Clinical → Economics**: a confirmed Appointment becomes a Visit → ServiceExecution → Charge → Payment.
- **Operations**: clinical consumption **automatically draws stock at the branch where the visit
  happened**, and stock moves between branches with atomic, audited transfers.

Two principles make it valuable:

1. **PostgreSQL is the final authority.** Durations, availability, tenant integrity, stock and payments
   are enforced by constraints — not by application checks and never by an LLM.
2. **Deterministic and agent-native.** Prices, slots, stock and payments are decided in code. Agents and
   integrations will call the exact same services humans use, with a permission model and an audit trail
   that records who did what and why.

The legacy `MediStock` Flask system is a **read-only reference**, outside the product.

## Repositories

Workspace root: `~/projects/portfolio/AI-EdgeRunners/odontoflow/`

| Repo | Role | Remote |
|---|---|---|
| `odontoflow-planning/` (this repo) | Project control plane: status, roadmap, repos map, handoffs, changelog | `MiguelAAR10/OdontoFlow-Planning` |
| `odontoflow-backend/` | FastAPI + PostgreSQL **domain authority** (384 tests, migration 0008) | `MiguelAAR10/OdontoFlow` |
| `odontoflow-frontend/` | React SPA adapting to the real backend contract (Agenda/Patients/Cash/Inventory REAL) | `MiguelAAR10/odontoflow-frontend` (Leonardo's original repo preserved as upstream/reference) |

Start here: [`STATUS.md`](STATUS.md) (verified snapshot) · [`REPOSITORIES.md`](REPOSITORIES.md) ·
[`HANDOFFS.md`](HANDOFFS.md) · [`CAVELOG.md`](CAVELOG.md).

## Roadmap

| Milestone | Status |
|---|---|
| M0 — Repository Recovery | CLOSED |
| M1 — Platform Foundation | CLOSED |
| M2 — FastAPI Core Migration | CLOSED |
| M3 — Frontend Core Integration | CLOSED |
| **M4 — Pilot Fit** | **CLOSED** (2026-08-17) |
| **M5 — First Measured Value** | **NOW** |
| M6 — Agentic Operations | LATER |

**M4 Pilot Fit (closed):** Cash real on `/charges*`; inventory location-aware (Product × Location) with
atomic transfers; Inventory UI real; a no-mock pilot E2E proved the full journey
(Patient → Appointment → Visit → Execution → Consumption@Location → Charge → Payment → Cash UI →
Inventory UI → Transfer). Final DeepSeek review: PASS.

**M5 First Measured Value (now):** Observe → detect economic leakage → intervene → measure outcome →
estimate economic effect → measure delivery/human cost. Not another planning/architecture/migration phase.

## How we work (collaboration model)

This project is built by humans **and** coding agents side by side. To keep it coherent:

1. **The backend is the single source of truth.** Frontend work always regenerates its TypeScript
   contracts from the backend OpenAPI and adapts to it — never the reverse.
2. **TDD is mandatory in the backend** (failing tests first, real PostgreSQL, no SQLite). Frontend
   changes must keep `typecheck` + unit tests + build green, and real-backend E2E where the contract
   changed.
3. **One task = one commit; evidence travels with the task.** Every milestone records its evidence under
   `.audit/m4-pilot-fit/` and a handoff in [`HANDOFFS.md`](HANDOFFS.md).
4. **Reviews gate shipping.** After implementation, an independent read-only review runs (location/tenant
   integrity, stock authority, transfer atomicity, money correctness, contract drift) with at most one
   repair pass. Commits happen after fan-in, never before.
5. **Scoped panes.** Builders own one repo each and never touch the other's files or the legacy
   `MediStock`.
6. **Consistency docs for agents.** Each repo carries its own operating contract (`AGENTS.md`): backend
   directives in `odontoflow-backend/AGENTS.md`, frontend rules in `odontoflow-frontend/AGENTS.md`. Read
   them before touching code — they encode the same rules as this page.
7. **Isolated per-repo environments.** Backend = Python 3.12 venv + `pyproject.toml`; frontend = Node 24 +
   `package.json`/`package-lock.json`. Variables documentadas en cada `.env.example`. Reference completa:
   `../ENVIRONMENT.md` (raíz del workspace, junto al mapa maestro).

### A typical delivery loop

```
brief (scope, contract, no-go's)
  → writer agent(s) implement (TDD, own repo only)
  → deterministic shell verifies (typecheck/tests/build/E2E)
  → read-only review (one pass)
  → commit + push (fast-forward only)
  → Repo 0 records exact HEADs + evidence
  → planning STATUS/CAVELOG/HANDOFFS updated
```

## How to onboard a new collaborator (or a new agent)

1. Read this README, then [`STATUS.md`](STATUS.md) for the verified current state.
2. Read the repo you'll touch: `odontoflow-backend/README.md` + `docs/` (architecture, api-reference,
   rules-and-permissions, flows) or `odontoflow-frontend/README.md` + `docs/frontend-architecture.md`.
3. Read the `AGENTS.md` of that repo before writing any code.
4. Pick the smallest task that matches the current milestone (see `STATUS.md → Next activity`).