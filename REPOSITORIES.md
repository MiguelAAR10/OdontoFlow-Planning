---
title: OdontoFlow — Repositories
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning)
---

# Repositories

Workspace root: `~/projects/portfolio/AI-EdgeRunners/odontoflow/`
(planning = this repo; backend, frontend y voice son hermanos un nivel arriba: `../`)

| Repo | Local path | Remote | Role | HEAD (verified) | Source of truth | Write policy |
|---|---|---|---|---|---|---|
| planning | `odontoflow-planning/` | `git@github.com:MiguelAAR10/OdontoFlow-Planning.git` | project control plane, navigation, status | `04acfc1` | status/navigation | planning docs; `.audit/` git-ignored **except `.audit/contributions/`** (contributor provenance is versioned on purpose) |
| backend | `../odontoflow-backend/` | `git@github.com:MiguelAAR10/OdontoFlow.git` | FastAPI + PostgreSQL domain authority | `23527c2` (synced) | domain model, migrations, API contract, tests | product work; normal push (fast-forward only, no force) |
| frontend | `../odontoflow-frontend/` | `git@github.com:MiguelAAR10/odontoflow-frontend.git` (canonical) · upstream/reference `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` (`leonardo`) | React SPA | `a967b24` (origin/main) | UI behavior per backend contract | product work; normal push (fast-forward only, no force); Leonardo's repo preserved as upstream/reference; **`alejandro` = contributor remote, fetch-only** |

| voice | `../odontoflow-voice/` | `git@github.com:MiguelAAR10/odontoflow-voice.git` (canonical, **public** since 2026-09-03; `AlejandroMarceloCh` invited as write collaborator) · contributor upstream `https://github.com/AlejandroMarceloCh/odonto-voz.git` (`alejandro`) | **canonical voice/language adapter** — sibling service, own process + port 8000 | `4149a3e` (donor `eb9a4ee` + 1) | speech→structured **drafts** only; **NOT a business authority** | product work; normal push (no force, **never squash or rewrite the 5 donor commits**); `alejandro` is fetch-only |

| sim | `../odontoflow-sim/` | `git@github.com:MiguelAAR10/odontoflow-sim.git` (canonical, **public** since 2026-09-03; `AlejandroMarceloCh` + `leonardopanduro-rgb` invited as write collaborators) · contributor upstream `https://github.com/AlejandroMarceloCh/odontoflow.git` (`alejandro`) | **canonical synthetic clinic / ground-truth simulator** — sibling repo, Vite/React, zero backend, zero database | `da203a9` (donor `b57f7bc` + 1) | **synthetic ground truth only** · **NOT a business authority** | product work; normal push (no force, **never squash or rewrite the 7 donor commits**); `alejandro` is fetch-only |

**`odontoflow-sim` provenance (do not lose):** written by **Alejandro Marcelo
(6 commits) and Leonardo Panduro (1, `333af34`)** — a **shared codebase**.
Promoted 2026-09-03 from the contributor clone by `mv` (`.git` preserved, HEAD
verified `b57f7bc`, `fsck` clean), never re-created by copying files. Renamed on
purpose: the contributors' repo is called `odontoflow` but is a *simulator*.

**All its data is SYNTHETIC** — 28 patients, 4 doctors, 10 treatments, 60
appointments, 5 waitlist candidates, 3 laboratories, and behaviour probabilities
that are a **declared assumption, not a measurement**. None of it may ever
become canonical clinic data. The interface carries a permanent,
non-dismissible band (**CLÍNICA SINTÉTICA · DATOS SIMULADOS · NO SON DATOS
REALES**) mounted in the shell outside the view switch, guarded by sentinel
tests. See `odontoflow-sim/CANONICAL.md`.

**`odontoflow-voice` provenance (do not lose):** every line and all 5 commits of
history below `4149a3e` are authored by **Alejandro Marcelo**. Promoted from the
donor clone by `mv` (`.git` preserved, HEAD verified, `fsck` clean) — never
re-created by copying files. Its `backend/datos/catalogo.json` is
**SYNTHETIC + DOMAIN VOCABULARY**: the SKUs must never become canonical clinic
data, the aliases must be preserved. See `odontoflow-voice/CANONICAL.md`.

The frontend also carries a fetched contributor ref, intact and **still
unmerged** even though its content has now been ported:
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
- **Leonardo's visual baseline** (7 screenshots, originals from the git object
  store, blob hashes matching GitHub) is preserved under the contributor
  preservation root and credited in [VISUAL_BASELINE.md](VISUAL_BASELINE.md).
  It is **design intent, not a UI specification**, and does not replace the
  canonical UI.
- Bundles of all local-only commits live in
  `~/projects/portfolio/_preservation/odontoflow-recovery-2026-08-16/`;
  contributor bundles, patches and checksums in
  `~/projects/portfolio/_preservation/odontoflow-contributors-2026-09-02/`
  (see `CAVELOG.md`).
