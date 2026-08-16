---
title: OdontoFlow — Decision Log (CAVELOG)
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning)
---

# CAVELOG — Decision Log

| Timestamp (local) | Decision | Reason | Evidence | Affected repos |
|---|---|---|---|---|
| 2026-08-16 | Do not push frontend | Remote `ODONTO-SMART-FRONT` belongs to leonardopanduro-rgb; policy forbids pushing without explicit authorization. Local work is bundle-protected. | recovery manifest, remote-owner check | frontend |
| 2026-08-16 | Bundle all local-only commits before any move | Backend HEAD `9bb7361` and frontend HEAD `6135025` exist only locally; not reachable from any remote branch. Any loss of local `.git` would lose 7 commits total. | `git branch -r --contains` empty for both; repository-inventory.md | backend, frontend, ODONTO-SMART |
| 2026-08-16 | Store recovery artifacts outside product repos | Keep `_preservation/` outside `AI-EdgeRunners/` product trees so preservation never enters product scope and survives cleanups. | preservation dir layout | all |
| 2026-08-16 | Canonical topology: `odontoflow-backend/`, `odontoflow-frontend/` under `AI-EdgeRunners/` | Plan-specified single workspace; planning is Repo 0; medistock stays READ ONLY legacy; no nested `.git`; old `portfolio/odontoflow/` workspace left in place (stale README) until verified and approved for removal. | recovery plan; destination-name conflict check passed | backend, frontend |
| 2026-08-16 | Plain `mv` (same filesystem) for relocation | Preserves every `.git`, full object store, remotes, worktrees; no history rewrite, no squash. | HEADs + remotes + worktree lists unchanged post-move | backend, frontend |
| 2026-08-16 | Backend push is a clean fast-forward → normal push only, no force | LOCAL `9bb7361`, REMOTE `8dd83eb`, merge-base == remote HEAD (AHEAD 5, BEHIND 0). | merge-base computation; recovery manifest | backend |
| 2026-08-16 | Repair only stale path references; no product behavior changes | Paths that became invalid after relocation get fixed; docs that are append-only records are left untouched. | traceability-inventory.md §7 | backend, frontend |
| 2026-08-16 | Frontend HEADs/status documented in planning STATUS.md | Backend/workspace READMEs were 1–4 milestones stale; planning is now the verified-status authority. | traceability-inventory.md §4 | planning |
| 2026-08-16 | Verification results recorded | fsck clean both repos; HEADs/remotes unchanged post-move; backend 364 passed; frontend typecheck clean; all planning links resolve; legacy path resolves read-only. | verification step output | all |
| 2026-08-16 | Nest workspace under `AI-EdgeRunners/odontoflow/` | User created the folder and requested all odonto product repos live inside it; medistock stays OUTSIDE as read-only legacy. | user decision; `ls` verification | planning, backend, frontend |
| 2026-08-16 | Update path refs for nested workspace | After nesting, medistock refs in live docs became `../../medistock`; planning docs updated to `../odontoflow-*`. Append-only handoffs/CHANGELOG untouched. | `git grep` re-scan | backend docs |

## Recovery artifact

Preservation root: `~/projects/portfolio/_preservation/odontoflow-recovery-2026-08-16/`

- `odontoflow-backend-9bb7361.bundle` — sha256 `e8d8d417…`
- `odontoflow-frontend-6135025.bundle` — sha256 `1cad3caf…`
- `odonto-smart-marketing-0d59878.bundle` — sha256 `e73bf2a3…`
- `SHA256SUMS.txt`, `MANIFEST.md` (remotes, branches, divergence analysis)
