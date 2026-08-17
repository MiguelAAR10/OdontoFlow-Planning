---
title: OdontoFlow — Decision Log (CAVELOG)
status: active
last_verified: 2026-08-16
authority: Repo 0 (planning)
---

# CAVELOG — Decision Log

| Timestamp (local) | Decision | Reason | Evidence | Affected repos |
|---|---|---|---|---|
| 2026-08-16 | M4.2 Location-Aware Inventory: commit + push | Movement ledger extended Product × Organization → Product × Location (migration `0008`: `location_id` NOT NULL composite FK, backfill truthful + fail-loud, reversible); transfers TRANSFER_OUT/IN atomic + idempotent + audited. 384 tests PASS. Committed `28d1e22` and pushed `c85ccd8..28d1e22` to MiguelAAR10/OdontoFlow (clean fast-forward, no force). | full suite 384; migration cycle tests; OpenAPI regenerated + verified | backend |
| 2026-08-16 | M4.1 Real Cash UI: commit local, push intent denied | CashPage rewired to real `/charges` + `/charges/{id}/payments` (Idempotency-Key), outstanding derived, income/expense/cierres/comisiones deferred. 54 frontend tests PASS + build. Committed `54b6e20`. Push to Leonardo's remote re-attempted (https y SSH) → **denied** (`Permission to leonardopanduro-rgb/ODONTO-SMART-FRONT.git denied to MiguelAAR10`). Ownership not bypassed; SHA preserved + compact handoff. | `git push` outputs; cash-adapter/cash-transport tests | frontend |
| 2026-08-16 | Frontend evidence committed in-repo | `.audit/m4-pilot-fit/` (contract map + cash-real.md) committed with `54b6e20` (frontend tracks .audit; backend ignores it). | git ls-files | frontend, backend |
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
| 2026-08-16 | Close Repo 0: init planning as git repo | Planning becomes versioned control plane; track only spine docs + `.gitignore`; `.audit/` ignored (raw recovery artifacts). Commit `c6e71a1` "chore: establish OdontoFlow project control plane". | `git init -b main`; verified not inside a worktree | planning |
| 2026-08-16 | Create dedicated remote `OdontoFlow-Planning` under MiguelAAR10 | `gh` authenticated as MiguelAAR10 with `repo` scope; private repo created and pushed normally. | `gh repo create --private --push` output; `ls-remote` match | planning |
| 2026-08-16 | Freeze roadmap to canonical M0–M6 | M0 Recovery CLOSED · M1 Platform Foundation CLOSED · M2 FastAPI Core CLOSED · M3 Frontend Integration PARTIAL · M4 Pilot Fit NOW · M5 First Measured Value NEXT · M6 Agentic Operations LATER. No new Platform Foundation phase as next activity. | user directive; PLAN.md | planning |
| 2026-08-16 | Backend doc commit + normal push | Diff verified documentation/path-only (4 `.md` files); committed `c85ccd8` "docs: repair canonical workspace references"; recompute: ahead 6, behind 0, merge-base == remote HEAD → clean fast-forward; pushed `8dd83eb..c85ccd8`. No force. | `git diff --name-only`; merge-base computation; push output | backend |
| 2026-08-16 | Frontend doc commit, no push (ownership) | Diff verified README/path-only; committed `2908cd1` "docs: repair canonical backend references"; recompute: ahead 3, behind 0, clean fast-forward; `git push --dry-run` fails (no credentials for https github.com, remote owned by leonardopanduro-rgb). Ownership not bypassed; commit preserved locally + bundle. | dry-run failure output; remote owner check | frontend |
| 2026-08-16 | Backend M4.2 commit + normal push | Inventory location-aware + transfers: committed `28d1e22` "feat: location-aware inventory with atomic transfers"; full suite 384 PASS (verified re-run); fast-forward push `c85ccd8..28d1e22`. No force. | pytest full run; push output | backend |
| 2026-08-16 | Frontend M4.1 commit, push to new canonical remote | User created `MiguelAAR10/odontoflow-frontend` and asked to push everything to main. Commit `54b6e20` "feat: real cash UI against charges API"; remote `miguel` added; pushed `54b6e20` as new `main`; Leonardo's repo left untouched. | remote add + push output | frontend |
| 2026-08-17 | Canonicalize frontend remotes | `origin` renamed to `leonardo` (Leonardo's repo preserved as upstream/reference) and `miguel` renamed to `origin` (`git@github.com:MiguelAAR10/odontoflow-frontend.git`). History untouched, no force. Verified `origin/main == 54b6e20` before implementation. | `git remote -v`; `git rev-parse origin/main` | frontend |
| 2026-08-17 | Frontend M4.3+M4.4 commit + normal push | Inventory UI + pilot E2E: committed `20f38f1` "feat: integrate location-aware inventory with FastAPI"; unit 83 PASS, typecheck clean, build PASS, Pilot E2E 12/12, Agenda+Patients regression 6/6; fast-forward push `54b6e20..20f38f1`. Backend received no commit (E2E proved zero backend defects). | verification outputs; push output | frontend |
| 2026-08-17 | Close M4 at Repo 0 | M3/M4 marked CLOSED, M5 NOW at Repo 0; canonical frontend remote recorded; Leonardo's repo recorded as upstream/reference. | this commit | planning |

## Recovery artifact

Preservation root: `~/projects/portfolio/_preservation/odontoflow-recovery-2026-08-16/`

- `odontoflow-backend-9bb7361.bundle` — sha256 `e8d8d417…`
- `odontoflow-frontend-6135025.bundle` — sha256 `1cad3caf…`
- `odonto-smart-marketing-0d59878.bundle` — sha256 `e73bf2a3…`
- `SHA256SUMS.txt`, `MANIFEST.md` (remotes, branches, divergence analysis)

> Bundles capture the pre-freeze state (backend `9bb7361`, frontend `6135025`).
> After the close-out, backend is pushed to `c85ccd8`; frontend advanced locally
> to `2908cd1` (3 commits ahead of remote, still not pushed — Leonardo's repo).
