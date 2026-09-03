---
title: OdontoFlow — Status (verified snapshot)
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning) — numbers re-verified from repos at verify time
---

# Status — Verified Snapshot (2026-09-02)

## Milestone

**CURRENT_MILESTONE = M5 First Measured Value** (M0–M4 CLOSED · M5 NOW · M6 LATER)

**M5 sub-state:** M5.1 Revenue Leakage Measurability **CLOSED** (evidence:
[M5_REVENUE_LEAKAGE_BASELINE.md](M5_REVENUE_LEAKAGE_BASELINE.md)) ·
M5.2 **BLOCKED on real clinic data** (`DOMINANT_LEAKAGE = UNKNOWN`).

## HEADs (verified by git, not by docs)

- **BACKEND_HEAD:** `23527c2` (`main`) — synced with origin
- **BACKEND_REMOTE:** `git@github.com:MiguelAAR10/OdontoFlow.git` — origin/main = `23527c2`
- **BACKEND_TESTS:** 384 PASS (real PostgreSQL, port 5434; full run re-verified 2026-09-02, 171s, exit 0)
- **MIGRATION:** 0008 (alembic 0001–0008 — location-aware inventory + transfers)
- **FRONTEND_HEAD:** `a967b24` (`main`) — synced with canonical origin (voice UI port)
- **FRONTEND_REMOTE (canonical):** `git@github.com:MiguelAAR10/odontoflow-frontend.git` — origin/main = `a967b24`
- **FRONTEND_REMOTE (upstream/reference):** `https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT.git` — preserved as `leonardo`, at `8769f12`, history untouched, never force-pushed
- **FRONTEND_TESTS:** **91 unit PASS** (83 + 8 voice gate) · **Pilot E2E 12/12 PASS** (re-run 2026-09-02 on a fresh `odontoflow_e2e`) · typecheck clean · build PASS
- **VOICE_HEAD:** `4149a3e` (`main`) — donor `eb9a4ee` + 1 canonical commit, synced with origin
- **VOICE_REMOTE:** `git@github.com:MiguelAAR10/odontoflow-voice.git` (canonical, **private**) · contributor upstream `AlejandroMarceloCh/odonto-voz` preserved as `alejandro`
- **VOICE_TESTS:** **54 PASS** (0.89 s, Python 3.12.3) — the donor's own suite, unmodified
- **PLANNING_HEAD:** `c33d65b` (`main`) — synced with origin (before this snapshot's commit)
- **Legacy (medistock):** `ef2fffb` (`main`, synced) — READ ONLY, outside workspace

All three active repos: working tree **clean**, local HEAD **== origin/main**,
`git fetch --all` brought **zero** new upstream commits.

## Canonical environment (verified 2026-09-02)

| Repo | Runtime pin | Database | Test command |
|---|---|---|---|
| backend | Python `3.12` (`.python-version`), `pyproject.toml` (`odontoflow` 0.1.0) | PostgreSQL 15 in `odontoflow-db-1`, `127.0.0.1:5434`; `odontoflow_test` for pytest, `odontoflow_e2e` for the pilot harness | `.venv/bin/python -m pytest -q` |
| frontend | Node `24` (`.nvmrc`) | consumes the backend API | `npm run test` · `npm run test:e2e` · `npm run test:e2e:pilot` · `npm run typecheck` |

Bring the database up with `docker start odontoflow-db-1` (data volume
`odontoflow_odontoflow_pgdata`). Note: running `docker compose up` from
`odontoflow-backend/` derives a *different* compose project name and creates an
**empty** volume — always start the named container instead.

## Voice Integration V1 — DONE (2026-09-02)

**`odontoflow-voice` is now a canonical repo** — the voice/language adapter.
Promoted from the donor clone by `mv` so the `.git` and all **5 donor commits by
Alejandro Marcelo** survive untouched (HEAD verified `eb9a4ee`, `fsck` clean,
never squashed, never force-pushed). Upstream stays reachable as `alejandro`.

**Frontend:** the donor's assistant view is **ported, not merged** (`a967b24`).
`alejandro/feat/asistente-voz` still points at `c0f418d` and was never merged,
cherry-picked or rebased. Commit carries `Co-authored-by: Alejandro Marcelo`.

**Environment contract** — the gate is AND, not OR:

| `VITE_ENABLE_VOICE` | `VITE_USE_MOCKS` | behaviour |
|---|---|---|
| `false` (default) | anything | `/asistente` route not registered; nav item hidden; **no HTTP ever** |
| `true` | `true` (default) | page renders and explains itself; **no HTTP ever** |
| `true` | `false` | live, against `VITE_VOICE_URL` (default `http://127.0.0.1:8000`) |

Verified in a real browser, with the voice service **up and healthy**: mock mode
and disabled mode each produced **zero requests to :8000**. Agenda/Patients/
Cash/Inventory real-mode guarantees intact — pilot E2E **12/12** on a fresh DB.

**V1 writes no business state.** The voice service produces **structured
drafts** (labelled `Borrador` in the UI) and never creates `Visit`,
`ServiceExecution`, `ServiceConsumption`, `Charge`, `Payment` or
`InventoryMovement`. The backend remains the only business authority — and the
backend was **not modified** in this activity.

**Audio E2E: UNVERIFIED, not faked.** No TTS on this machine (`say` is
macOS-only; no `espeak`/`espeak-ng`/`pico2wave`/`festival`/`flite`), and
headless Chrome has no microphone. The donor's latency figures stay **their**
Apple Silicon measurements until re-measured here.

**Synthetic-catalog boundary held:** `catalogo.json` SKUs are **SYNTHETIC** and
were not promoted to canonical clinic data; its **aliases** are preserved as
**DOMAIN VOCABULARY**. Recorded in `odontoflow-voice/CANONICAL.md`.

Handoffs: `odontoflow-frontend/.audit/voice-v1/voice-ui-port.md` ·
`odontoflow-voice/CANONICAL.md`. Credit: [CONTRIBUTIONS.md](CONTRIBUTIONS.md).

## External activity since the last snapshot

- **One open pull request, on the upstream/reference repo only:**
  [leonardopanduro-rgb/ODONTO-SMART-FRONT#1](https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/pull/1)
  — "Vista Asistente de voz: dictado de inventario y resumen de consulta", by
  `AlejandroMarceloCh`, opened 2026-08-15, +390/−5 over 6 files. It targets
  `leonardo/main` (`8769f12`), **not** the canonical `origin`, and depends on an
  external voice service (`AlejandroMarceloCh/odonto-voz`). Canonical `main` is
  7 commits ahead of that base, so it is not fast-forward mergeable as-is.
  **Not merged, not evaluated** — outside M5 scope; recorded so it is not lost.
- No other commits, branches or PRs appeared on any of the three canonical repos.

## Frontend real state (M4 complete)

| Screen | State |
|---|---|
| Agenda | REAL |
| Patients | REAL |
| Cash | REAL (M4.1 — charges/payments via `/charges*`, Idempotency-Key) |
| Inventory | REAL (M4.3 — products, balance by Location, entries, adjustments, kardex, transfers) |
| Chat | PROTOTYPE |
| Agent | PROTOTYPE |

## Backend state (M4 complete)

| Area | State |
|---|---|
| Inventory | REAL — Product × Location (location_id on every movement, composite FK, balance per location, consumption at visit location) |
| Transfers | REAL — atomic TRANSFER_OUT/TRANSFER_IN, one tx, idempotent (PF4), audited |
| Clinical/Economics | REAL — unchanged guarantees intact (PF1–PF4/PF7) |

## Pilot E2E (M4.4 — CLOSED)

Real journey proven end-to-end against real FastAPI + real PostgreSQL with
`VITE_USE_MOCKS=false`: Patient → Appointment (confirmed) → Visit (location
derived) → ServiceExecution → ServiceConsumption → SALIDA at the Visit Location →
other Location unchanged → Charge → partial + full Payment → overpayment rejected
via the real envelope → CashPage reflects paid/outstanding (`loadCharges`) →
InventoryPage reflects the new Location balance (`loadProductBalance`) →
Transfer (conservation + shared `transfer_id`) → kardex + location-isolated
adjustment. Evidence: `odontoflow-frontend/.audit/m4-pilot-fit/pilot-e2e.md`.
Harness (reproducible): `scripts/pilot-e2e.sh`.

Final review (DeepSeek V4 Flash, read-only, one pass): **PASS — no blockers**
(location/tenant integrity, stock authority, transfer atomicity, money
correctness, contract drift, Agenda/Patients/Cash regressions). One repair
applied in the pass: mock-mode overpayment code aligned to the real backend
(`INVALID_INPUT`).

## Tests

- **Backend:** 384 passed (verified full run 2026-08-16; no backend commit in M4.3/M4.4 — the E2E proved zero backend defects)
- **Frontend:** 83 passed / 9 files (unit) · Pilot E2E 12/12 · Agenda+Patients real-backend regression 6/6 · typecheck clean · build PASS

## OpenAPI paths (32, generated at backend HEAD — location-aware)

`/health` · `/leads`(+`/{id}`) · `/appointments`(+`/{id}`, `/cancel`, `/reschedule`) ·
`/availability-rules` · `/schedule-blocks` · `/slots/query` · `/capabilities` ·
`/practitioners`(+`/eligible`) · `/locations` · `/services` · `/patients`(+`/{id}`) ·
`/visits`(+`/{id}`) · `/visits/{visit_id}/executions` · `/executions/{execution_id}/charges` ·
`/executions/{execution_id}/consumptions` · `/charges`(+`/{id}`, `/{charge_id}/payments`) ·
`/products`(+`/{id}`, `/entries`, `/movements`, `/adjustments`, `/balance`, `/transfers`) —
`location_id` required en entries/adjustments (body) y balance/movements (query)

## Latest handoffs

- M4.4 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/pilot-e2e.md` (Pilot E2E + final review)
- M4.3 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/inventory-ui.md` (InventoryPage real)
- M4.1 evidence: `odontoflow-frontend/.audit/m4-pilot-fit/cash-real.md` (CashPage real)
- M4.2 evidence: `odontoflow-backend/.audit/m4-pilot-fit/inventory-backend.md` (location-aware + transfers)
- Contract map: `odontoflow-frontend/.audit/m4-pilot-fit/frontend-contract-map.md`
- Full index: [HANDOFFS.md](HANDOFFS.md)

## Blockers

**One, and it is not technical: no real clinic operational data exists.**

Verified by live row census (2026-09-02) across every database on the instance:
`odontoflow_e2e` holds only the M4.4 pilot fixtures (`Lead E2E Piloto`,
`Bootstrap Clinic`, seeded 2026-08-17 by `.audit/accelerator/seed_e2e.py`), the
dev database `odontoflow` is at migration `0001` with zero rows, and the
frontend seeds are self-declared synthetic. Therefore `DOMINANT_LEAKAGE =
UNKNOWN` and M5.2 cannot start.

Unblocking requires a 90-day clinic export (≥ 300 appointments, ≥ 200 charges,
pseudonymous patient ids — full specification in
[M5_REVENUE_LEAKAGE_BASELINE.md §6](M5_REVENUE_LEAKAGE_BASELINE.md)).

**Voice V1 blockers: none.** Both donor sources are canonical or ported, with
authorship intact. Two open questions remain **for the clinic**, not for
engineering: the real tariff/supply catalog, and how one visit's total maps to
per-treatment charges (`Charge` is 1:1 with a `ServiceExecution`, so a
two-treatment visit needs two charges and the donor supplies one number).
Nothing writes money until that is answered.

**Found while testing, pre-existing, NOT fixed here:** the canonical backend has
**no CORS middleware**, so a browser calling `:8010` from `:5173` is blocked
(the same request via `curl` returns 200; `OPTIONS` returns 405). That is why
the pilot E2E is a **node** harness, and it means the SPA has never been driven
in a browser against the real backend. Out of scope for V1 — the backend was not
touched. The voice service does declare CORS for `:5173`, which is why its
browser E2E worked.

Infrastructure blockers: none. Repos clean and synced; backend suite green.

Known platform limitation (recorded, not a blocker): the donor's E2E harness
`auditar.py` is **macOS-only** (shells out to `say`), so the voice
audio/transcription path is **UNVERIFIED on Linux/WSL** and the donor's latency
figures remain the author's Apple Silicon measurements, not ours.

## Next activity

**NEXT_ACTIVITY = V2 — Synthetic Clinic Configuration.** Connect the donor's
preserved **alias vocabulary** to an editable Synthetic Clinic configuration, so
the synthetic catalog stops being a hard-coded file and becomes configurable
data — without ever promoting its SKUs to canonical clinic data.

Still true and unchanged by this activity: **M5's validation truth.** This
contribution supplies **no real clinic data**, so `DOMINANT_LEAKAGE` remains
`UNKNOWN` and the M5 baseline still needs the 90-day clinic export specified in
[M5_REVENUE_LEAKAGE_BASELINE.md §6](M5_REVENUE_LEAKAGE_BASELINE.md).

(Not another planning/architecture/Foundation/migration phase.)
