---
title: OdontoFlow — Repositories
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning)
---

# Repositories

Workspace root: `~/projects/portfolio/AI-EdgeRunners/odontoflow/`
(planning = this repo, backend y frontend son hermanos un nivel arriba: `../`)

| Repo | Local path | Remote | Role | HEAD (verified) | Source of truth | Write policy |
|---|---|---|---|---|---|---|
| planning | `odontoflow-planning/` | `git@github.com:MiguelAAR10/OdontoFlow-Planning.git` | project control plane, navigation, status | `1c63f02` | status/navigation | planning docs; `.audit/` git-ignored **except `.audit/contributions/`** (contributor provenance is versioned on purpose) |
| backend | `../odontoflow-backend/` | `git@github.com:MiguelAAR10/OdontoFlow.git` | FastAPI + PostgreSQL domain authority | `23527c2` (synced) | domain model, migrations, API contract, tests | product work; normal push (fast-forward only, no force) |
| frontend | `../odontoflow-frontend/` | `git@github.com:MiguelAAR10/odontoflow-frontend.git` (canonical) · upstream/reference `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` (`leonardo`) | React SPA | `9595abd` (origin/main) | UI behavior per backend contract | product work; normal push (fast-forward only, no force); Leonardo's repo preserved as upstream/reference; **`alejandro` = contributor remote, fetch-only** |

Contributor sources (inside the workspace, NOT canonical, NOT product repos):

| Repo | Local path | Remote | Role | HEAD (verified) | Source of truth | Write policy |
|---|---|---|---|---|---|---|
| contrib-odonto-voz | `../contrib-odonto-voz/` | `https://github.com/AlejandroMarceloCh/odonto-voz.git` (origin, contributor-owned) | **CONTRIBUTOR SOURCE / NOT CANONICAL BUSINESS AUTHORITY** — standalone voice service by Alejandro Marcelo | `eb9a4ee` | **nothing** — its `catalogo.json` is synthetic; its in-memory counts are never stock truth | **READ ONLY.** Never push. Never rewrite its history. Not a submodule, not built or deployed by any canonical pipeline. |

The frontend also carries a fetched contributor ref, intact and unmerged:
`alejandro/feat/asistente-voz` = `c0f418d` (donor PR
[ODONTO-SMART-FRONT#1](https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/pull/1)).

See [CONTRIBUTIONS.md](CONTRIBUTIONS.md) for authorship and exact SHAs, and
[VOICE_CONTRIBUTION_INTEGRATION_MAP.md](VOICE_CONTRIBUTION_INTEGRATION_MAP.md)
for the integration order.

Legado (fuera del workspace, respetado — READ ONLY):

| legacy | `../../medistock/` | `git@github.com:MiguelAAR10/MediStock.git` | legacy reference (streamlit/Flask era) | `ef2fffb` | historical domain knowledge | READ ONLY |

Related lineages (not part of canonical topology, do not treat as product repos):

- `~/projects/portfolio/ODONTO-SMART` — public marketing site (`MiguelAAR10/odonto-smart`), separate lineage.
- `~/projects/portfolio/Startup/Odonto` — public demo (`leonardopanduro-rgb/PROYECTO-ODONTO`), separate lineage.
- `~/projects/portfolio/odontoflow/` — old workspace (now only a stale README; superseded by this repo map).

Rules:

- No nested Git repositories: each repo above is a standalone root with its own `.git`.
- Never squash or rewrite history; preserve remotes and complete commit graphs.
- `.audit/` in planning is git-ignored (raw recovery artifacts never committed),
  **except `.audit/contributions/`**, which IS versioned: contributor provenance
  is durable evidence about someone else's authorship, and losing it would
  silently erase credit.
- **Contributor repos are never pushed to and never rewritten.** They keep their
  own `origin` pointing at their author.
- Bundles of all local-only commits live in
  `~/projects/portfolio/_preservation/odontoflow-recovery-2026-08-16/`;
  contributor bundles, patches and checksums in
  `~/projects/portfolio/_preservation/odontoflow-contributors-2026-09-02/`
  (see `CAVELOG.md`).
