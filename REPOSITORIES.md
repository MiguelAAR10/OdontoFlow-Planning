---
title: OdontoFlow — Repositories
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning)
---

# Repositories

Workspace root: `~/projects/portfolio/AI-EdgeRunners/odontoflow/`
(planning = this repo, backend y frontend son hermanos un nivel arriba: `../`)

| Repo | Local path | Remote | Role | HEAD (verified) | Source of truth | Write policy |
|---|---|---|---|---|---|---|
| planning | `odontoflow-planning/` | none (not versioned) | project control plane, navigation, status | — | status/navigation | planning docs, audit artifacts |
| backend | `../odontoflow-backend/` | `git@github.com:MiguelAAR10/OdontoFlow.git` | FastAPI + PostgreSQL domain authority | `9bb7361` | domain model, migrations, API contract, tests | product work; normal push to origin/main (currently ahead 5, clean fast-forward) |
| frontend | `../odontoflow-frontend/` | `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` | React SPA (Leonardo) | `6135025` | UI behavior per backend contract | product work; **push restricted** — remote owned by leonardopanduro-rgb, push only on explicit authorization |

Legado (fuera del workspace, respetado — READ ONLY):

| legacy | `../../medistock/` | `git@github.com:MiguelAAR10/MediStock.git` | legacy reference (streamlit/Flask era) | `ef2fffb` | historical domain knowledge | READ ONLY |

Related lineages (not part of canonical topology, do not treat as product repos):

- `~/projects/portfolio/ODONTO-SMART` — public marketing site (`MiguelAAR10/odonto-smart`), separate lineage.
- `~/projects/portfolio/Startup/Odonto` — public demo (`leonardopanduro-rgb/PROYECTO-ODONTO`), separate lineage.
- `~/projects/portfolio/odontoflow/` — old workspace (now only a stale README; superseded by this repo map).

Rules:

- No nested Git repositories: each repo above is a standalone root with its own `.git`.
- Never squash or rewrite history; preserve remotes and complete commit graphs.
- Bundles of all local-only commits live in
  `~/projects/portfolio/_preservation/odontoflow-recovery-2026-08-16/`
  (see `CAVELOG.md`).
