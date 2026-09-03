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

Author of **two distinct projects**, deliberately recorded separately below
because they are different systems solving different problems:

1. **The voice assistant** — a standalone voice service plus the frontend view that consumes it (Contributions 1 and 2).
2. **The clinic operations simulator** — a pure, deterministic discrete-event simulation of clinic operations (Contribution 3).

**Do not collapse them into one contribution.** They share an author and a
domain, nothing else: different repositories, different stacks, different
purposes, and different integration paths.

Commits as `Alejandro Marcelo <alejandromarcelo@MacBook-Pro-de-Alejandro.local>`.

### Leonardo Panduro — `leonardopanduro-rgb`

Author of the **original ODONTO SMART frontend** (`8769f12` — "Implement
ODONTO SMART frontend"), the foundation the canonical OdontoFlow frontend is
built on. Owner of the repository the voice PR was opened against.

His repository is preserved as the `leonardo` remote in
`odontoflow-frontend`, **history untouched and never force-pushed**. The
canonical frontend is 8 commits ahead of his base; every one of those commits
sits on top of his work, not in place of it.

He is also the author of:

- **The visual baseline** — 7 screenshots committed in `8769f12`, the design
  record of the frontend as he intended it. Preserved with original git blob
  hashes and credited in [VISUAL_BASELINE.md](VISUAL_BASELINE.md).
- **One commit inside Alejandro's operations simulator** (`333af34`,
  "feat: ampliar demo operativa de OdontoFlow"). That repository is a **shared
  codebase**, not solely Alejandro's — see Contribution 3.

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

## Contribution 3 — `odontoflow` · clinic operations simulator

**A different project from the voice assistant.** Recorded separately on purpose.

| Field | Value |
|---|---|
| **Contributors** | **Alejandro Jesus Marcelo CH** (6 of 7 commits) · **Leonardo Panduro** (1 commit, `333af34`) |
| **Source repository** | https://github.com/AlejandroMarceloCh/odontoflow |
| **Source PR** | *none* — a standalone repository |
| **Exact SHA** | `b57f7bc6b1eca84a132b61a11ca687bbd5b5e58e` (branch **`master`**) |
| **Scale** | 7 commits · 1 branch · 0 tags · 55 files · ~6 200 lines of source |
| **Dates** | 2026-08-07 → 2026-08-08 |
| **Preservation** | `_preservation/odontoflow-contributors-2026-09-02/alejandro-odontoflow-b57f7bc.bundle` (complete history) + `alejandro-odontoflow-commits.txt`; checksums verified **20/20 OK** |
| **Current status** | **PROMOTED to `odontoflow-sim` (2026-09-03) — donor history intact** |
| **Canonical repo** | `git@github.com:MiguelAAR10/odontoflow-sim.git` (remote `origin`, **private**) · contributor upstream preserved as remote `alejandro` |
| **Local path** | `~/projects/portfolio/AI-EdgeRunners/odontoflow/odontoflow-sim` (promoted by `mv`, `.git` preserved, HEAD verified `b57f7bc`, `fsck` clean) |
| **Integration status** | **V2.1 DONE — promotion + safety boundary only.** No FastAPI, no intent adapter, no canonical states, no waitlist or lab tables, no voice vocabulary, no UI port, no agents, no WhatsApp. |
| **Authority** | **canonical synthetic clinic / ground-truth simulator** · **NOT a business authority** — never creates Visit / ServiceExecution / ServiceConsumption / Charge / Payment / InventoryMovement |

### What was built

A working clinic operations simulator: a pure domain core with no I/O and no
system clock, a virtual clock with a **reversible** timeline, a deterministic
seed, and a React operations centre.

| Component | Lines | What it is |
|---|---|---|
| `src/runtime/mundo.ts` | 693 | The replay engine: rebuilds the clinic from the seed and replays history to any instant |
| `src/runtime/snapshot.ts` | 555 | Paint-ready projection of the whole clinic |
| `src/domain/engine.ts` | 135 | **Pure, idempotent rules engine.** Reads no clock, has no effects |
| `src/domain/seed.ts` | 288 | Deterministic seed: 28 patients, 4 doctors, 10 treatments, 60 appointments, 5 waitlist candidates, 3 laboratories, 6 lab jobs |
| `src/domain/transitions.ts` | 42 | 9-state appointment machine; illegal transitions **raise** instead of corrupting data |
| `src/domain/paciente-sim.ts` | 105 | Deterministic patient behaviour from a hashed id — no randomness, no dates |
| `src/domain/risk.ts` | 60 | Explainable risk heuristic with a one-sentence reason |
| `src/domain/lista-espera.ts` | 62 | Waitlist matching and slot recovery |
| `src/domain/reprogramacion.ts` | 92 | Deterministic reschedule proposals |
| `src/domain/channel.ts` | 68 | Message drafting, neutral Peruvian Spanish |
| `src/components/`, `src/store/` | ~1 500 | Operations centre, agenda board, patients, doctors, laboratories, activity feed, editable rules |
| `scripts/verificar.ts` | 121 | The author's own 8-step end-to-end walkthrough |
| `tests/` | 11 files | Including `reloj-sentinel.test.ts` — 32 assertions that fail if **any** file reads real time |

### Verified state (measured 2026-09-02, on the donor's own contract)

- Node v24.12.0 / npm 11.6.2 · `npm install` clean
- `npm run typecheck` — **clean**
- `npm test` — **98 passed / 11 files / 1.31 s**
- `npm run build` — **PASS** (57 modules)
- `npm run verificar` — **"Recorrido completo sin fallos"**, all 8 steps

**Nothing was repaired during the baseline**, per the brief.

### Intellectual contribution worth naming

**The clock sentinel.** A test that scans every source file to prove none reads
real time. Its reasoning: if someone uses the system clock, advancing the
virtual clock silently stops working and the simulation breaks with no error.
That is the kind of test people write only after understanding what actually
makes their system fragile.

**Rebuild rather than undo.** Dragging the timeline backwards re-runs history
from the seed instead of reversing operations. That single choice is what makes
the simulator usable as a reproducible measurement baseline.

Also worth naming: the **waitlist recovery loop** and the **operations-centre
queue** — two product ideas OdontoFlow did not have and had not planned.

### Documentation drift — found in intake #2, **repaired in V2.1**

The README claimed the whole interface carried a visible *"Datos ficticios de
demostración"* label. Donor HEAD `b57f7bc` removed exactly those labels (14
deletions across 3 components) and no test noticed, so the README asserted
something false and a screenshot of the simulator became indistinguishable from
a real clinic's.

**Repaired in the first canonical commit (`da203a9`)**, not by editing the
contributors' work but by restoring the guarantee their README already promised:
a permanent, non-dismissible band mounted in the shell outside the view switch,
with sentinel tests so it cannot silently disappear again. The README is
corrected only where it was false; their voice and terminology are preserved.
Detail in [SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md §7](SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md)
and the [V2.1 brief](docs/handoffs/plans/2026-09-03-v2-1-simulator-promotion.md).

---

## Contribution 4 — visual baseline · Leonardo Panduro

| Field | Value |
|---|---|
| **Contributor** | **Leonardo Panduro** (`leonardopanduro-rgb`) |
| **Source** | https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/tree/main/screenshots |
| **Exact SHA** | `8769f12f5e3144fe5c2032d0f8445861dc304c76` ("Implement ODONTO SMART frontend", 2026-08-14) |
| **Assets** | 7 screenshots: agenda (desktop + mobile), agente, caja, chat, inventario, pacientes |
| **Preservation** | `_preservation/odontoflow-contributors-2026-09-02/leonardo-visual-baseline/` — originals extracted from the git object store, **git blob hashes match GitHub's exactly**, checksums verified |
| **Current status** | **PRESERVED · design reference** |
| **Integration status** | **Does not replace the canonical UI.** Design intent, not a UI specification. |
| **Authority** | **UX_REFERENCE** — the truth about design intent; the code is the truth about current behaviour |

Recorded in [VISUAL_BASELINE.md](VISUAL_BASELINE.md), including the two known
gaps: no baseline for the voice assistant, and mobile intent captured for the
agenda only.

---

## Integration ledger

Every future use of this work gets a row here, so credit is traceable after the
code has moved and been adapted.

| Date | What was integrated | From (SHA) | Into | Form | Credit |
|---|---|---|---|---|---|
| 2026-09-02 | The whole voice service (5 commits, 19 files, 2 219 lines) | `eb9a4ee` | `odontoflow-voice` (canonical) | **Promotion** — the donor clone itself, `.git` and all commits preserved; one new file added on top (`CANONICAL.md`, `4149a3e`) | **Alejandro Marcelo** authors every line of the service and all 5 commits |
| 2026-09-03 | The whole operations simulator (7 commits, 55 files, ~6 200 lines) | `b57f7bc` | `odontoflow-sim` (canonical, private) | **Promotion** — the contributor clone itself, `.git` and all commits preserved; one canonical commit on top (`da203a9`: `CANONICAL.md`, the synthetic boundary + its tests, one README paragraph) | **Alejandro Marcelo** (6 commits) and **Leonardo Panduro** (1, `333af34`) author every line; a shared codebase |
| 2026-09-02 | Voice assistant view: `AsistenteVozPage`, `Voice*` types (verbatim), `.voz-*` CSS (verbatim), the 5 client calls, route + nav entry | `c0f418d` | `odontoflow-frontend` `a967b24` | **Intentional port** onto a base 7 commits ahead. Adapted: flag/mock gate in `src/voice.ts`, navbar squeeze scoped to a modifier, summaries labelled `Borrador`. Commit carries `Co-authored-by: Alejandro Marcelo`. | **Alejandro Marcelo** designed and wrote the view; **Leonardo Panduro** authored the frontend base it sits on |

**When a row is added, it must name the donor SHA.** "Inspired by" is not
sufficient when the code is derived.

---

## Standing constraints

- `contrib-odonto-voz/` is a **sibling repository**, not part of the product. It keeps its own `origin` pointing at Alejandro's repo. It is not a submodule and is not built by any canonical pipeline.
- `catalogo.json` SKUs and prices are **SYNTHETIC** and must never be promoted into canonical product data. Its **aliases** are domain vocabulary and should be preserved, re-keyed onto real `products.id` / `services.id`.
- The donor's latency figures (2.2 s mean / 3.6 s worst) are **the author's measurements on Apple Silicon**. They must be re-measured before OdontoFlow quotes them.
- `whatsapp.py` carries the author's own honesty notice: the Meta Graph API payload shape was written from memory and is unverified. **Preserve that notice** in any port.
