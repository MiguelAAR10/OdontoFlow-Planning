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
| planning | `odontoflow-planning/` | `git@github.com:MiguelAAR10/OdontoFlow-Planning.git` | project control plane, navigation, status | `c6e71a1` | status/navigation | planning docs, audit artifacts (`.audit/` git-ignored) |
| backend | `../odontoflow-backend/` | `git@github.com:MiguelAAR10/OdontoFlow.git` | FastAPI + PostgreSQL domain authority | `28d1e22` (synced) | domain model, migrations, API contract, tests | product work; normal push (fast-forward only, no force) |
| frontend | `../odontoflow-frontend/` | `git@github.com:MiguelAAR10/odontoflow-frontend.git` (canonical) · upstream/reference `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` (`leonardo`) | React SPA | `20f38f1` (origin/main) | UI behavior per backend contract | product work; normal push (fast-forward only, no force); Leonardo's repo preserved as upstream/reference |

Legado (fuera del workspace, respetado — READ ONLY):

| legacy | `../../medistock/` | `git@github.com:MiguelAAR10/MediStock.git` | legacy reference (streamlit/Flask era) | `ef2fffb` | historical domain knowledge | READ ONLY |

Related lineages (not part of canonical topology, do not treat as product repos):

- `~/projects/portfolio/ODONTO-SMART` — public marketing site (`MiguelAAR10/odonto-smart`), separate lineage.
- `~/projects/portfolio/Startup/Odonto` — public demo (`leonardopanduro-rgb/PROYECTO-ODONTO`), separate lineage.
- `~/projects/portfolio/odontoflow/` — old workspace (now only a stale README; superseded by this repo map).

Rules:

- No nested Git repositories: each repo above is a standalone root with its own `.git`.
- Never squash or rewrite history; preserve remotes and complete commit graphs.
- `.audit/` in planning is git-ignored (raw recovery artifacts never committed).
- Bundles of all local-only commits live in
  `~/projects/portfolio/_preservation/odontoflow-recovery-2026-08-16/`
  (see `CAVELOG.md`).
