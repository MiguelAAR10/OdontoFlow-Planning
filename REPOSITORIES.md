---
title: OdontoFlow — Repositories
status: active
last_verified: 2026-09-17
authority: Repo 0 (planning)
---

# Repositories

Workspace root: `~/projects/portfolio/AI-EdgeRunners/odontoflow/`
(planning = this repo; backend, frontend y voice son hermanos un nivel arriba: `../`)

| Repo | Local path | Remote | Role | HEAD (verified) | Source of truth | Write policy |
|---|---|---|---|---|---|---|
| planning | `odontoflow-planning/` | `git@github.com:MiguelAAR10/OdontoFlow-Planning.git` | project control plane, navigation, status | publication chain starts at `08b12a0b696c827ea1abdc6d2e2fb9e5517ba98b`; final remote head re-verified after the handoff update; unrelated local tooling/WIP remains preserved | status/navigation | planning docs; `.audit/` git-ignored **except `.audit/contributions/`** (contributor provenance is versioned on purpose) |
| backend | `../odontoflow-backend/` | `git@github.com:MiguelAAR10/OdontoFlow.git` | FastAPI + PostgreSQL domain authority | local/remote `193d48b49db6cc4cd04e82965adce08061aad715` (published 2026-09-17; includes the 11 local product commits plus onboarding/audit docs) | domain model, migrations, API contract, tests | product work; normal push (fast-forward only, no force) |
| frontend | `../odontoflow-frontend/` | `git@github.com:MiguelAAR10/odontoflow-frontend.git` (canonical `origin`) · dead upstream `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` (`leonardo`, 404 as of 2026-09-17) | React SPA | local `a788df5`, **1 ahead** of canonical `origin/main` (`0dbfa9e`) — **that commit is BLOCKED for publication**, see below | UI behavior per backend contract | product work; normal push to `origin` explicitly (fast-forward only, no force). **Onboarding hazard:** local `main` tracks `leonardo/main`, which no longer resolves — do not `git push` without specifying `origin`; **`alejandro` = contributor remote, fetch-only** |

| voice | `../odontoflow-voice/` | `git@github.com:MiguelAAR10/odontoflow-voice.git` (canonical, **public** since 2026-09-03; `AlejandroMarceloCh` invited as write collaborator) · contributor upstream `https://github.com/AlejandroMarceloCh/odonto-voz.git` (`alejandro`) | **canonical voice/language adapter** — sibling service, own process + port 8000 | `70ee066511baa0452246fc3b2107938c5db0126b` (freshly verified equal to `origin/main`; no action) | speech→structured **drafts** only; **NOT a business authority** | product work; normal push (no force, **never squash or rewrite the 5 donor commits**); `alejandro` is fetch-only |

| sim | `../odontoflow-sim/` | `git@github.com:MiguelAAR10/odontoflow-sim.git` (canonical, **public** since 2026-09-03; `AlejandroMarceloCh` + `leonardopanduro-rgb` invited as write collaborators) · contributor upstream `https://github.com/AlejandroMarceloCh/odontoflow.git` (`alejandro`) | **canonical synthetic clinic / ground-truth simulator** — sibling repo, Vite/React, zero backend, zero database | `19275c81fabb59bc36573887e423dfe84462f0b5` (`master`, equal to `origin/master`; `origin/main` absent; V2.2 worktree dirty and untouched) | **synthetic ground truth only** · **NOT a business authority** | product work; normal push (no force, **never squash or rewrite the 7 donor commits**); `alejandro` is fetch-only |

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

**Frontend publication block (2026-09-17, do not push without owner review):**
the one local-only commit `a788df5` ("feat(fe3a): salvage checkout through
charge") plausibly matches the FE3A-S1 salvage plan's recommended bounded
slice and fixes its named payload blocker, but no in-repo artifact
authorizes it — `.audit/fe3a-checkpoint.md` explicitly withheld commit
permission pending an integration-lead gate, and the commit itself has no
body or notes recording that gate was passed. It must remain blocked for
publication until the coordinator/integration lead confirms it in writing;
do not rewrite or discard it. The worktree also carries 19 modified tracked
files and 12 untracked paths — the uncommitted remainder of the same mixed
FE3A work. Full detail:
[`docs/handoffs/plans/2026-09-17-project-publish-01.md`](docs/handoffs/plans/2026-09-17-project-publish-01.md).

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
