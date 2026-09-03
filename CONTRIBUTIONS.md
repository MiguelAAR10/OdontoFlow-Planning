---
title: OdontoFlow — Contributions & Provenance
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning) — durable authorship record
---

# Contributions & Provenance

Durable record of work contributed by people other than the maintainer.

**Rules this file exists to enforce:**

1. **Donor code is never presented as newly authored OdontoFlow code.** If it
   came from a contributor, this file says so, with the exact SHA.
2. **Credit survives integration.** Porting, adapting or rewriting a
   contribution does not erase who thought of it first.
3. **Contributor sources are not business authority.** Their synthetic data
   never becomes canonical product data.

---

## Contributors

### Alejandro Jesus Marcelo CH — `AlejandroMarceloCh`

Author of the **voice assistant** work: a standalone voice service and the
frontend view that consumes it.

Commits as `Alejandro Marcelo <alejandromarcelo@MacBook-Pro-de-Alejandro.local>`.

### Leonardo Panduro — `leonardopanduro-rgb`

Author of the **original ODONTO SMART frontend** (`8769f12` — "Implement
ODONTO SMART frontend"), the foundation the canonical OdontoFlow frontend is
built on. Owner of the repository the voice PR was opened against.

His repository is preserved as the `leonardo` remote in
`odontoflow-frontend`, **history untouched and never force-pushed**. The
canonical frontend is 7 commits ahead of his base; every one of those commits
sits on top of his work, not in place of it.

---

## Contribution 1 — `odonto-voz` · standalone voice service

| Field | Value |
|---|---|
| **Contributor** | Alejandro Jesus Marcelo CH (`AlejandroMarceloCh`) |
| **Source repository** | https://github.com/AlejandroMarceloCh/odonto-voz |
| **Source PR** | *none* — a standalone repository, contributed as a sibling service |
| **Exact SHA** | `eb9a4ee0381972658fb8a9e717d4e056820d3d4e` (branch `main`) |
| **Scale** | 5 commits · 1 branch · 0 tags · 19 files · 2 219 lines |
| **Dates** | 2026-08-15 → 2026-08-16 |
| **Preservation** | `_preservation/odontoflow-contributors-2026-09-02/odonto-voz-eb9a4ee.bundle` (complete history, checksum verified) |
| **Current status** | **PROMOTED to `odontoflow-voice` (2026-09-02) — donor history intact** |
| **Canonical repo** | `git@github.com:MiguelAAR10/odontoflow-voice.git` (remote `origin`, private) · contributor upstream preserved as remote `alejandro` |
| **Local path** | `~/projects/portfolio/AI-EdgeRunners/odontoflow/odontoflow-voice` (promoted by `mv`, `.git` preserved, HEAD verified unchanged, `fsck` clean) |
| **Integration status** | **V1 DONE** — transport + UI only. Produces structured drafts; writes no business state. |
| **Authority** | **canonical voice/language adapter** · **NOT a business authority** — never creates Visit / ServiceExecution / ServiceConsumption / Charge / Payment / InventoryMovement |

### Original components (all authored by Alejandro)

| Component | Lines | What it is |
|---|---|---|
| `backend/app/parser.py` | 327 | Spanish speech → structured items. Number words, catalog aliases, amounts, payment methods. **Stdlib only, no LLM by design.** |
| `backend/app/conversacion.py` | 317 | Channel-agnostic two-flow state machine. `procesar()` serves browser, WhatsApp and tests identically. |
| `auditar.py` | 207 | Objective-level E2E harness with real generated audio. |
| `backend/app/main.py` | 179 | FastAPI surface (7 endpoints). |
| `backend/app/whatsapp.py` | 118 | WhatsApp Cloud API adapter — written, deliberately disabled. |
| `backend/app/flujos.py` | 107 | Flows and questions **as data, not code**. |
| `backend/app/transcriptor.py` | 96 | Local faster-whisper transcription, singleton model. |
| `backend/datos/catalogo.json` | 37 | Closed catalog with **spoken aliases**. |
| `README.md` · `CONTRATO-API.md` · `PETICIONES-A-MIGUEL.md` · `PARA-ENCHUFAR-WHATSAPP.md` | 359 | Setup, the API contract, reasoned backend requests, and the WhatsApp deployment analysis. |
| `backend/tests/` | 434 | 54 tests (parser 21 · conversation 19 · api 9 + parametrized). |

### Verified state (measured 2026-09-02, not claimed)

- Dependency install from the donor's own `requirements.txt`: **clean, exit 0.**
- Donor test suite: **54 passed, 0 failed, 0.69 s.**
- Both flows driven end-to-end over real HTTP: **correct business JSON**, including the self-correction `"tres, no, cuatro"` → 4.
- `auditar.py`: **cannot run outside macOS** — depends on the `say` TTS binary. Its first two text checks pass; it is platform-bound, not broken. **No repair attempted.**
- Audio/transcription path: **UNVERIFIED on Linux** (no TTS available to drive it).

### Intellectual contribution worth naming explicitly

Beyond the code: the **decision not to use an LLM in the parsing path**,
argued from OdontoFlow's own invariant, and the **all-local privacy stance**
justified under Peru's Ley 29733. Also the observation that *"the precision is
won in `catalogo.json`, not in the model"* — which is correct and is the
insight that makes the alias vocabulary the most valuable data in the
contribution.

`PETICIONES-A-MIGUEL.md` deserves separate credit: four reasoned requests to
the business backend, written against the **legacy MediStock schema**. Three of
the four were independently solved by OdontoFlow's M4.2 work. Correct analysis,
different codebase — see the integration map.

---

## Contribution 2 — frontend voice view · donor PR #1

| Field | Value |
|---|---|
| **Contributor** | Alejandro Jesus Marcelo CH (`AlejandroMarceloCh`) |
| **Source repository** | https://github.com/AlejandroMarceloCh/ODONTO-SMART-FRONT (fork) |
| **Source PR** | https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/pull/1 — **OPEN** |
| **PR repo owner** | `leonardopanduro-rgb` (Leonardo) |
| **Branch** | `feat/asistente-voz` |
| **Exact head SHA** | `c0f418dc5b296715fa4b0a6cb8cbd0da9f7eba0f` |
| **Exact base SHA** | `8769f12f5e3144fe5c2032d0f8445861dc304c76` (Leonardo's `main`) |
| **Commits** | `e5f42567cf822d111e82d46cd88695674adfd1e6` · `c0f418dc5b296715fa4b0a6cb8cbd0da9f7eba0f` |
| **Scale** | +390 / −5 across 6 files |
| **Dates** | 2026-08-15 → 2026-08-16 |
| **Local ref** | `alejandro/feat/asistente-voz` in `odontoflow-frontend` (fetched, intact) |
| **Preservation** | `frontend-donor-c0f418d.bundle` · `frontend-pr1-asistente-voz.patch` · `frontend-pr1-metadata.json` (checksums verified) |
| **Current status** | **FETCHED INTACT · PORTED (V1)** — the donor ref itself is still untouched |
| **Integration status** | **PORTED, not merged.** Applied intentionally onto canonical `main` as `a967b24`; `alejandro/feat/asistente-voz` still points at `c0f418d` and was never merged, cherry-picked or rebased. |
| **Authority** | **CONTRIBUTOR SOURCE / NOT CANONICAL** |

### Original components

| File | Change | Authored content |
|---|---|---|
| `src/pages/AsistenteVozPage.tsx` | +193 (new) | The whole assistant view: recording, live inventory table, guided-consultation stepper, editable summary, latency display, graceful offline state. |
| `src/index.css` | +103 / −4 | Flat BEM styles for the view; plus a navbar geometry fix for the 7th nav item. |
| `src/types.ts` | +64 | 8 TypeScript interfaces mirroring the voice API contract. |
| `src/api.ts` | +26 | Second axios instance + 5 voice client calls. |
| `src/App.tsx` | +2 | Route registration. |
| `src/components/Navbar.tsx` | +2 / −1 | Nav entry with `Mic` icon. |

### Quality noted for the record

The contribution **reuses the existing design system** (`Badge`, `DataTable`,
`Button`, `KpiCard`) instead of inventing parallel components, **degrades
gracefully** when the voice service is absent, and **documents its own
trade-offs** in the PR body — including offering to change the navbar approach
if the maintainer prefers another solution. That is how a contribution should
arrive.

---

## Integration ledger

Every future use of this work gets a row here, so credit is traceable after the
code has moved and been adapted.

| Date | What was integrated | From (SHA) | Into | Form | Credit |
|---|---|---|---|---|---|
| 2026-09-02 | The whole voice service (5 commits, 19 files, 2 219 lines) | `eb9a4ee` | `odontoflow-voice` (canonical) | **Promotion** — the donor clone itself, `.git` and all commits preserved; one new file added on top (`CANONICAL.md`, `4149a3e`) | **Alejandro Marcelo** authors every line of the service and all 5 commits |
| 2026-09-02 | Voice assistant view: `AsistenteVozPage`, `Voice*` types (verbatim), `.voz-*` CSS (verbatim), the 5 client calls, route + nav entry | `c0f418d` | `odontoflow-frontend` `a967b24` | **Intentional port** onto a base 7 commits ahead. Adapted: flag/mock gate in `src/voice.ts`, navbar squeeze scoped to a modifier, summaries labelled `Borrador`. Commit carries `Co-authored-by: Alejandro Marcelo`. | **Alejandro Marcelo** designed and wrote the view; **Leonardo Panduro** authored the frontend base it sits on |

**When a row is added, it must name the donor SHA.** "Inspired by" is not
sufficient when the code is derived.

---

## Standing constraints

- `contrib-odonto-voz/` is a **sibling repository**, not part of the product. It keeps its own `origin` pointing at Alejandro's repo. It is not a submodule and is not built by any canonical pipeline.
- `catalogo.json` SKUs and prices are **SYNTHETIC** and must never be promoted into canonical product data. Its **aliases** are domain vocabulary and should be preserved, re-keyed onto real `products.id` / `services.id`.
- The donor's latency figures (2.2 s mean / 3.6 s worst) are **the author's measurements on Apple Silicon**. They must be re-measured before OdontoFlow quotes them.
- `whatsapp.py` carries the author's own honesty notice: the Meta Graph API payload shape was written from memory and is unverified. **Preserve that notice** in any port.
