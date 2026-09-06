---
title: Frontend Next.js Amendment — supersedes the Vite/React Router decision only
status: PLANNED — no implementation started
date: 2026-09-05
planner: Claude Opus 5 (planning authority; no product code written)
amends: docs/plans/2026-09-05-frontend-experience-v1.md
supersedes: >
  ONLY §2 invariant 1 ("Do not migrate to Next.js. Vite + React 18 + React
  Router stays.") and the matching `scope.out` line "any Next.js migration,
  component-library adoption, or React refactor" in §15. Everything else in the
  experience plan — §1 reality, §2 invariants 2–9, §3 brand, §4 IA, §5 design
  system, §6 typography, §7 Clerk boundary, §8 data boundary, §9 screen map,
  §11 sequence, §12 FE1, §13 missing contracts, §14 decisions, §16 rollback —
  remains in force and is NOT restated here.
target_repo: odontoflow-frontend (product) — no other repo is touched
evidence: >
  Direct inspection at write time — odontoflow-frontend HEAD
  2324884f7e916f44442a57c897cacb91add0ba1e (tree clean except ` M AGENTS.md`);
  `npm test` executed 2026-09-05: 10 files, 91 tests, 91 passed, vitest 3.2.7,
  node v24.12.0, npm 11.6.2. Next.js App Router evidence from official docs via
  Context7 (/vercel/next.js): `docs/01-app/02-guides/migrating/from-vite.mdx`,
  `.../from-create-react-app.mdx`, `docs/01-app/02-guides/backend-for-frontend.mdx`,
  `docs/01-app/02-guides/environment-variables.mdx`,
  `docs/01-app/02-guides/server-and-client-boundary.mdx`,
  `docs/01-app/01-getting-started/05-server-and-client-components.mdx`,
  `docs/01-app/03-api-reference/05-config/01-next-config-js/rewrites.mdx`.
---

# Frontend Next.js Amendment

**Owner decision (input to this document, not a finding):** the OdontoFlow
frontend standardizes on **Next.js**. This amendment converts that decision into
a staged, reversible, implementation-ready migration contract. It is a *narrow*
amendment: it changes the framework, and nothing else.

Read the experience plan first. This document only says what changes.

---

## 0. Naming reconciliation (a real collision, resolved here)

The experience plan §15 uses the label `FE0` for "install the six-skill frontend
lane" as a dependency of FE1. This activity also uses `FE0`. Resolution:

| Label | Meaning from here on |
|---|---|
| **FE0** | The Next.js standardization activity (planning + migration). |
| **FE0A** | *This document.* Planning only. Complete when this file is accepted. |
| **FE0B** | The migration implementation vertical. **Not started. Not begun here.** |
| ~~`FE0` (experience plan §15)~~ | Renamed **skill-lane install**; it becomes task zero of FE0B, not of FE1. |

**Sequence change to experience plan §11:** FE0B is inserted **before FE1**.
Rationale: FE1 rewrites the shell, `index.html`, `tailwind.config.js`, and the
visual harness (§12.3). Doing that on Vite and then migrating would redo the same
files twice and would invalidate FE1's before/after screenshot evidence. FE1's
§12.3 file list must be re-based onto the Next tree after FE0B lands; nothing
else in FE1 changes.

---

## 1. Repository reality (verified 2026-09-05, not assumed)

`odontoflow-frontend` @ `2324884`, working tree clean except ` M AGENTS.md`.

| Fact | Verified value | Where |
|---|---|---|
| Entry | `ReactDOM.createRoot(document.getElementById("root"))` inside `<React.StrictMode>` + `<BrowserRouter future={{v7_startTransition,v7_relativeSplatPath}}>` | `src/main.tsx` |
| Router | `react-router-dom` 6.28.1; one layout route `AppShell` with `<Outlet/>` | `src/App.tsx`, `src/components/AppShell.tsx` |
| Routes (8) | `/`→`/agenda` · `/agenda` · `/agente` · `/pacientes` · `/caja` · `/inventario` · `/chat` · `/asistente` (flag) · `*`→`/agenda` | `src/App.tsx:14-30` |
| Router API in use | `BrowserRouter`, `Routes`, `Route`, `Navigate`, `Outlet`, `NavLink`, `useNavigate` (×2), `useLocation` (×1) — **nothing else** | `grep -rn react-router-dom src/` |
| Build | `vite build && tsc -p tsconfig.backend.json`; `outDir: dist-web`; dev pinned `127.0.0.1:5173` | `package.json`, `vite.config.ts` |
| Second build half | `tsc -p tsconfig.backend.json` → `dist/`, run by `npm start` (`node dist/src/server.js`) — the **legacy simulator harness**, unrelated to the SPA | `package.json`, `tsconfig.backend.json` |
| Env reads (7 sites) | `VITE_BACKEND_URL` (`src/api.ts:72`, `src/contracts/client.ts:33`), `VITE_USE_MOCKS` (`src/api.ts:75`, `src/voice.ts:43`), `VITE_ENABLE_VOICE` (`src/voice.ts:40`), `VITE_VOICE_URL` (`src/voice.ts:48`) | `grep -rn import.meta.env src/` |
| Mock seam | `const useMocks = import.meta.env.VITE_USE_MOCKS !== "false"` — module-load constant, single façade `src/api.ts` (729 lines) | `src/api.ts:75` |
| Transport | one axios instance per module: `src/api.ts:71`, `src/contracts/client.ts:31`, `src/voice.ts:79` | — |
| Generated contract | `src/contracts/api.ts`, 74 835 B, mtime **2026-08-17 11:01**, **32 paths** | `openapi-typescript` |
| Contract source | `../odontoflow-backend/docs/api/openapi.yaml`, 222 260 B, mtime **2026-09-05 12:34** → generated file is **stale** (confirms experience plan §1.8) | — |
| Idempotency | `Idempotency-Key` header on every mutation in `src/contracts/client.ts`; `newIdempotencyKey()` per intent | — |
| Error envelope | `ApiError {code,message,httpStatus,details}` + `toApiError` | `src/contracts/client.ts:41-69` |
| Tests | **10 files, 91 tests, 91 passed** (`npm test`, 2026-09-05, vitest **3.2.7**). 3 integration specs excluded from `npm test`, included by `vitest.e2e.config.ts` | measured |
| Test shape | **No test imports a `.tsx`. No jsdom. No React rendering. No `@vitest-environment`.** Every spec is a Node-level adapter/domain test | `grep -rn 'from "../src' test/` |
| E2E | `test/pilot-e2e.test.ts` (12 cases), `agenda-integration` (3), `patients-integration` (3); driver `scripts/pilot-e2e.sh` (reset → alembic → uvicorn :8010 → vitest) | — |
| Visual harness | `scripts/visual-check.mjs`: programmatic `createServer` from **`vite`** on `:5189`, `playwright-core`, 7 flows, viewport 1692×929, fails on any `pageerror`/console error | — |
| Harness defects (pre-existing) | (a) hardcoded `executablePath: "C:\\Program Files\\Google\\Chrome\\..."` — unresolvable on this host; (b) writes into `screenshots/`, **the directory holding Leonardo's byte-verified baseline** | verified in file |
| Baseline | `screenshots/*.png` — 7 files, mtime 2026-08-15, git-blob + sha256 verified in `planning/VISUAL_BASELINE.md` | — |
| Directories absent | no `app/`, no `pages/`, no `public/`, no `.claude/skills`, no `.agents/skills` | `ls` |
| Runtime | node **v24.12.0**, npm 11.6.2, `.nvmrc` 24, `engines.node >=20` | measured |
| Tailwind | 3.4.17, `content: ["./index.html","./src/**/*.{ts,tsx}"]`; 3 `@tailwind` directives in `src/index.css` (432 lines, mostly hand-written CSS) | — |

### 1.1 Contributor-owned surfaces (identified from the repo — protected)

| Surface | Author | Provenance |
|---|---|---|
| `8769f12` "Implement ODONTO SMART frontend" — the entire visual language, `src/index.css`, all 7 pages, all components, `screenshots/*.png` | **Leonardo Panduro** (`leonardopanduro-rgb`) | commit author is Leonardo himself; every later commit sits on top |
| `src/voice.ts`, `src/pages/AsistenteVozPage.tsx`, the `voiceItem` nav entry + `.main-nav__links--dense` / `.nav-link` scoping in `src/index.css:311-321`, `test/voice-adapter.test.ts` | **Alejandro Jesus Marcelo CH** (`AlejandroMarceloCh`) | `a967b24` carries `Co-authored-by: Alejandro Marcelo`; port record `.audit/voice-v1/voice-ui-port.md` (donor `c0f418d`) |

**FE0B rule:** these files move only if the framework forces the move, the diff
is mechanical (import path / directive / env key), and the `Co-authored-by`
trailers and `.audit/voice-v1/voice-ui-port.md` are preserved verbatim. A
framework migration must not become a rewrite of contributed work. If a
contributed file needs a *behavioral* change to run under Next, that is an abort
trigger (§11), not a judgement call.

### 1.2 Plan-vs-repo discrepancies found

1. **`AGENTS.md` §4 says "83 tests". Measured: 91.** `DEVELOPMENT.md` (91) is
   correct; `AGENTS.md` is stale. Experience plan §1.10 flagged the disagreement
   and refused to pick — resolved here by execution. FE0B corrects `AGENTS.md`.
2. `package.json` pins `vitest ^3.2.4`; installed is **3.2.7**. Harmless; record
   the measured version in evidence, not the pin.
3. **`src/pages/` is the exact directory name Next.js reserves for the Pages
   Router under a `src/` root.** A hand-authored `src/pages/AgendaPage.tsx` next
   to an App Router tree is at best ambiguous and at worst becomes a route
   `/AgendaPage`. → FE0B renames `src/pages/` → `src/views/` (mechanical; import
   paths only). Verify the exact collision behavior at implementation time — the
   rename removes the question either way.
4. **Do not set Next's `distDir` to `./dist`** as the official Vite-migration SPA
   example does: `dist/` is already the `outDir` of `tsconfig.backend.json` and is
   what `npm start` runs. Leave Next on its default `.next`.
5. Experience plan §12.3 lists `EDIT index.html`. After FE0B there is no
   `index.html` — its content becomes `app/layout.tsx` + `metadata`. FE1's file
   list is re-based, not reinterpreted.
6. `tailwind.config.js` `content` references `./index.html`; `tsconfig.json`
   carries `"types": ["vite/client"]` and `"jsx": "react-jsx"` — all Vite-specific.
7. The visual harness clobbers the protected baseline directory (§1, harness
   defects). It has evidently never completed on this host (baseline mtimes are
   untouched since 2026-08-15) — the risk is real and unrealized.
8. Frontend has **no skill lane installed** (no `.claude/skills`, no
   `.agents/skills`) — confirms `orchestration/skill-matrix.yaml` `frontend:
   skills: []`. Installing it is task zero of FE0B.

---

## 2. What this amendment changes, exactly

**Superseded — experience plan §2 invariant 1.** Replace:

> ~~1. **Do not migrate to Next.js.** Vite + React 18 + React Router stays.~~

with:

> **1. The frontend standardizes on Next.js (App Router).** React 18 stays.
> Vite and `react-router-dom` are retired by FE0B. Next.js owns **presentation,
> routing/composition, and auth transport only**. It is never a source of
> business truth.

**Superseded — experience plan §15 `scope.out`.** The line "any Next.js
migration, component-library adoption, or React refactor" now reads "any
component-library adoption or React refactor" for FE1; the Next.js migration is
FE0B and precedes it.

**Unchanged and re-affirmed:** invariants 2–9 of §2 (backend authority,
generated contracts, honest `useMocks`, one error envelope, idempotency per
intent, never invent clinical functionality, preserve contributor work, synthetic
stays labelled), §7 Clerk architecture invariant, §8 data boundary.

### 2.1 Non-negotiable boundary for Next.js in this system

```
Next.js        presentation · routing/composition · (later) auth transport
FastAPI        business authority — prices, availability, stock, money,
               permissions, idempotency replay, error envelope
PostgreSQL     reached only through FastAPI
Browser        holds a short-lived session token and nothing else
```

- **No business logic in Next.js.** No Server Action that computes a price, a
  slot, a balance, or a stock level. No validation that duplicates a backend rule.
- **No direct Supabase browser access. No Supabase Auth.** Unchanged from §8.
- **No `ofk_` integration credential in the Next process, ever.** The backend's
  `credentials.py` states it must never be embedded in a browser; a Next server
  holding one would silently make Next an authority.
- **No GCP / deployment work in FE0B.** Local `next dev` / `next build` /
  `next start` only.
- **No Clerk in FE0/FE0B.** No package, no key, no account, no config, no login
  UI. Clerk remains FE1b, per experience plan §7.

---

## 3. Staged, reversible migration (the safest order)

Five stages, one commit each, on one branch off `2324884`. Each stage is green
(`typecheck` + 91 tests + build + visual) before the next begins. Reverting stage
*n* leaves stages 1..*n*−1 intact and working.

### Stage A — Preflight and baseline (no Next.js)

Purpose: make evidence possible *before* anything moves.

1. Install the frontend skill lane (experience plan §10; canonical body once,
   symlinked; provenance in `skills-lock.json`). Update
   `orchestration/skill-matrix.yaml` `frontend` lane — **coordinator's edit, not
   the writer's**, and out of scope for FE0A.
2. `scripts/visual-check.mjs`: make the browser path env-overridable
   (`VISUAL_BROWSER_PATH`, defaulting to Playwright's resolved Chromium) and the
   output directory env-overridable (`VISUAL_SCREENSHOT_DIR`, default unchanged).
   Two one-line classes of change.
3. Capture the **BEFORE** run into `.audit/fe0b-nextjs/before/` (never into
   `screenshots/`). Record `npm test` count, `git rev-parse HEAD`, backend
   `openapi.yaml` sha256 as the contract freeze marker.

Revert: trivial; no app code touched.

### Stage B — One environment accessor (still Vite)

Purpose: remove `import.meta.env` from the app graph *before* Next exists,
because `import.meta.env` is undefined under Next's bundler and would throw at
module load.

1. New `src/env.ts` — the **only** module in the app that reads the environment.
   It exports exactly the four values in use and **preserves today's defaulting
   semantics byte-for-byte**:
   - `BACKEND_URL` = `process.env.NEXT_PUBLIC_BACKEND_URL` (may be `undefined`;
     axios then issues relative URLs — today's behavior, preserved)
   - `USE_MOCKS` = `process.env.NEXT_PUBLIC_USE_MOCKS !== "false"`
   - `VOICE_ENABLED` = `process.env.NEXT_PUBLIC_ENABLE_VOICE === "true"`
   - `VOICE_URL` = `process.env.NEXT_PUBLIC_VOICE_URL ?? VOICE_DEFAULT_URL`
   Each written as a **literal static member access** — no destructuring, no
   `process.env[key]` — because Next inlines only static access.
2. `src/api.ts`, `src/contracts/client.ts`, `src/voice.ts` import from `env.ts`.
   No other line changes in those files.
3. Bridge for the Vite half of the migration: `vite.config.ts` gains a `define`
   mapping those four exact expressions from `loadEnv`. **Guard it so it does not
   apply under Vitest** (`if (!process.env.VITEST)`) — a `define` is a
   transform-time text replacement and would silently defeat `vi.stubEnv`, which
   is how `test/voice-adapter.test.ts` and `test/cash-transport.test.ts` prove the
   gates. This bridge is deleted in Stage E.
4. Test edits — **key renames only, no assertion changes**:
   `test/voice-adapter.test.ts` (3 keys), `test/cash-transport.test.ts` (2 keys),
   `test/agenda-integration.test.ts`, `test/patients-integration.test.ts`,
   `test/pilot-e2e.test.ts` (2 keys each), `scripts/pilot-e2e.sh` (2 exports),
   `.env.example` (4 keys, with the old→new mapping documented in-file).

Revert: one commit; restores `import.meta.env`.

### Stage C — Next.js alongside Vite, SPA-compatible shell

Purpose: prove the app runs on Next with **zero page changes**, using the pattern
the official Vite migration guide prescribes.

1. Add `next` (pin the current stable release; confirm the exact version and
   Node floor against `/vercel/next.js` at implementation time — do not assume).
   Vite stays installed and working; scripts become `dev`/`build` (Next) and
   `dev:vite`/`build:vite` (kept as the rollback path this stage only).
2. `app/layout.tsx` — Server Component. Owns `<html lang="es">`, `<body>`, the
   global `import "../src/index.css"`, and `metadata` carrying exactly today's
   `<title>Odonto Smart</title>`, description, and `themeColor: "#071e3a"`. The
   Inter Google-Fonts `<link>` is reproduced as-is in this stage (FE1 replaces it
   with Fontshare — not FE0B's job).
3. `app/[[...slug]]/page.tsx` — Server Component rendering a `'use client'`
   `ClientOnly` that does `dynamic(() => import('../../src/App'), { ssr: false })`.
   This is the documented pattern (`from-vite.mdx`); the `ssr: false` option is
   only legal inside a Client Component, which is why the wrapper exists.
   `src/App.tsx` and its `BrowserRouter` are **unmodified** — so all 8 routes,
   the `*`→`/agenda` catch-all, and the voice route-registration gate keep their
   exact current semantics by construction.
4. `next.config.ts`: no `output: 'export'` (see §3.1), no `distDir` override
   (§1.2 item 4), no rewrites.
5. `tsconfig.json`: `"jsx": "preserve"`, drop `"vite/client"` from `types`, add
   `next-env.d.ts` and `"plugins": [{ "name": "next" }]`, add `app/**/*.tsx` to
   `include`. `tsconfig.backend.json` **untouched**.
6. `next dev -p 5173 -H 127.0.0.1` — deliberately the same origin Vite used, so
   the backend's `CORS_ALLOWED_ORIGINS` note (experience plan §1.11) and every
   local env file stay valid.
7. `.gitignore`: add `.next/`, `next-env.d.ts`, `.env*.local`.

Revert: one commit; `dev:vite` still runs the app.

### Stage D — Native App Router route tree

Purpose: reach real App Router routing; retire `react-router-dom`.

Route-for-route, one file per existing path (§4 for the exact tree). `NavLink` →
`next/link` + `usePathname`; `useNavigate` → `useRouter().push`; `useLocation`
(read of `?patient=`) → `useSearchParams`; `<Outlet/>` → `children` in
`app/(shell)/layout.tsx`. `Navigate` redirects → `redirect()` in a Server
Component. `app/[[...slug]]/page.tsx` is deleted at the end of this stage.

Behavior parity is the gate, not code shape. The 7 visual flows and 91 tests run
unchanged at the end of the stage.

Revert: one commit; Stage C's compat shell returns.

### Stage E — Decommission Vite

Delete `vite.config.ts`, `index.html`, `src/main.tsx`, the `define` bridge, the
`dev:vite`/`build:vite` scripts, `@vitejs/plugin-react`, `vite`,
`react-router-dom`, and `dist-web/` from `.gitignore`. Introduce a standalone
`vitest.config.ts` carrying the same `test.exclude` list (§9). Update
`tailwind.config.js` `content` to `["./app/**/*.{ts,tsx}","./src/**/*.{ts,tsx}"]`.
Update `AGENTS.md` §4/§5 (commands, the three-place test-registration rule, the
measured test count) and `DEVELOPMENT.md`.

Revert: one commit; the dual-toolchain state returns.

### 3.1 Two Next.js configuration decisions, made explicitly

| Decision | Choice | Rationale |
|---|---|---|
| `output: 'export'` (static SPA) vs Node server | **Node server (`next start`)** | Exact parity for `/`→`/agenda` and `*`→`/agenda` needs a runtime `redirect()`; a static export 404s on unknown paths, which is a behavior change. It also keeps the BFF option open for FE1b at zero cost. This is the one genuine architectural addition of FE0B — a Node process the SPA did not have — and §2.1 bounds what it may contain. |
| `basePath` / `distDir` overrides | **Neither** | Vite had no `base`; `dist/` is already owned by `tsconfig.backend.json`. |

---

## 4. Target directory and module boundaries

```
app/                                  ROUTING + COMPOSITION ONLY. No business logic.
  layout.tsx                          Server — html/body, global CSS, fonts, metadata
  page.tsx                            Server — redirect("/agenda")
  (shell)/layout.tsx                  Client — the AppShell (header, nav, global
                                      "Nueva cita" modal, toast); children == <Outlet/>
  (shell)/agenda/page.tsx             Server shell → <AgendaView/>            (client)
  (shell)/agente/page.tsx             Server shell → <AgentView/>
  (shell)/pacientes/page.tsx          Server shell → <PatientsView/>
  (shell)/caja/page.tsx               Server shell → <CashView/>
  (shell)/inventario/page.tsx         Server shell → <InventoryView/>
  (shell)/chat/page.tsx               Server shell → <ChatView/>
  (shell)/asistente/page.tsx          Server shell, voice-gated (§6.3)
  [...rest]/page.tsx                  Server — redirect("/agenda")  (catch-all parity)

src/                                  UNCHANGED OWNERSHIP
  views/            <- renamed from src/pages/ (§1.2 item 3). One file per screen,
                       'use client'. Content unchanged.
  components/       AppShell, Header, Navbar, Button, Badge, DataTable, KpiCard,
                    Modal — public APIs unchanged (experience plan §12.4)
  api.ts            THE façade + useMocks seam. Untouched except its env import.
  contracts/api.ts  GENERATED. Byte-identical after FE0B. Never hand-edited.
  contracts/client.ts  THE transport boundary. Untouched except its env import.
  env.ts            NEW. The only reader of process.env in the app graph.
  voice.ts, types.ts, mockData.ts, index.css   unchanged (env import aside)
  domain/ simulation/ server.ts index.ts ui.ts LEGACY Node harness — untouched,
                    still compiled by tsconfig.backend.json, still run by npm start,
                    NOT part of the Next graph
public/                               created by FE0B only if an asset needs it;
                                      brand assets are FE1's job
.audit/fe0b-nextjs/                   FE0B evidence (before/after screenshots, handoff)
```

**Hard boundary:** nothing under `app/` may import `src/mockData.ts`, construct an
axios instance, read `process.env` directly, or contain a domain rule. `app/` is a
routing manifest that mounts client views. All data flow continues to run
Browser → `src/api.ts` → `src/contracts/client.ts` → FastAPI.

---

## 5. Server vs Client Component boundaries

This is an interactive ERP whose entire data path is a browser-side façade with a
module-load mock seam. The honest boundary is therefore **high and thin**.

| Layer | Kind | Why |
|---|---|---|
| `app/layout.tsx`, `app/page.tsx`, `app/[...rest]/page.tsx`, each `(shell)/*/page.tsx` | **Server** | Document shell, `metadata`, and `redirect()`. No data access. |
| `app/(shell)/layout.tsx` (AppShell), all of `src/views/*`, all of `src/components/*` | **Client** (`'use client'` at each entry) | `useState`/`useEffect`, event handlers, `window.dispatchEvent("appointment-created")`, `document` keydown in `Modal`, `window.setInterval` in the voice view. |
| `src/api.ts`, `src/contracts/client.ts`, `src/voice.ts`, `src/mockData.ts` | **Browser modules** — reached only through the client graph | They carry the `useMocks` seam, the `Idempotency-Key` semantics and the `ApiError` envelope. |

**Rules for FE0B:**

1. Put `'use client'` at the **entry** of each view and at `app/(shell)/layout.tsx`
   — not on leaf components, and not on `src/api.ts`. One directive per boundary
   file; imported modules join the client graph automatically.
2. **No `'use server'` anywhere in FE0B.** No Server Actions, no server-side
   fetching of ERP data. Moving a single fetch to the server would relocate the
   `Idempotency-Key`, the auth header, and the error envelope out of the tested
   transport boundary, and would break the `useMocks` seam and the 91 Node adapter
   tests that bind to it. That is a business-authority question, not a rendering
   one, and it is explicitly out of scope.
3. Do **not** pass functions or class instances (e.g. `ApiError`) across a
   server→client prop boundary; the server pages pass nothing.
4. `client-only` as a guard on `src/api.ts` is *optional*. Verify it does not break
   the Node vitest suites before adopting; if it does, drop it — the `'use client'`
   entries are sufficient.

**Post-FE0B posture:** Server Components are available but unused for data. Any
later proposal to fetch ERP data server-side is a new decision requiring a plan
amendment, not an FE0B liberty.

---

## 6. FastAPI integration boundary

### 6.1 What does not change

`src/contracts/client.ts` remains the single transport boundary: one axios
instance, `baseURL` from `env.ts`, `Idempotency-Key` per intent on every mutation,
`toApiError` → `ApiError {code,message,httpStatus,details}`, generated types from
`src/contracts/api.ts`. Every backend path, method, header and body shape is
identical after FE0B. FastAPI remains the sole business authority.

### 6.2 Transport topology in FE0B

**Browser → FastAPI directly** — exactly as today. No proxy, no rewrite, no Route
Handler. The backend already mounts `CORSMiddleware` with `Authorization`,
`Idempotency-Key`, `X-Request-Id`, `X-Correlation-Id` allowed and
`allow_credentials=False` (experience plan §1.11), which is precisely a
header-bearer design. Keeping `next dev -p 5173` (§3, Stage C) means the allowed
origin does not even change.

### 6.3 The voice flag and route gate — preserved exactly

Today the gate is *route registration*: with `VITE_ENABLE_VOICE` off the
`/asistente` route does not exist and falls through to `*` → `/agenda`; and
`guardVoiceCall()` blocks HTTP unless `voiceEnabled && !useMocks`. Under
file-system routing, a route file always exists. Parity is defined **observably**:

| Env | Required observable behavior after FE0B |
|---|---|
| `NEXT_PUBLIC_ENABLE_VOICE` unset/`false` | navigating to `/asistente` lands on `/agenda`; the nav item is absent; **zero** voice HTTP |
| `=true`, `NEXT_PUBLIC_USE_MOCKS=true` | page renders; **zero** voice HTTP; the page states why |
| `=true`, `NEXT_PUBLIC_USE_MOCKS=false` | live against `NEXT_PUBLIC_VOICE_URL` |

Implementation: `app/(shell)/asistente/page.tsx` calls `redirect("/agenda")` when
the flag is off, and otherwise renders the view behind a flag-gated `dynamic()`
import so the module is not pulled into the bundle when disabled. `src/voice.ts`'s
`guardVoiceCall()` — Alejandro's contributed gate as hardened in `a967b24` — is
**not modified**; `test/voice-adapter.test.ts` (8 cases) remains the proof and its
assertions are unchanged.

---

## 7. Is Next.js a thin BFF for Clerk-authenticated FastAPI calls?

**Bounded answer: no — not in FE0B, and not by default afterwards. Keep the
browser→FastAPI direct path, and reserve the seam.**

Rationale:

1. **Parity is the FE0B deliverable.** A BFF hop adds a network segment, a second
   error surface, and a second place where headers can be dropped — inside the one
   activity whose entire acceptance is "nothing observable changed".
2. **It would degrade the existing test evidence.** `pilot-e2e` (12), `agenda-` and
   `patients-integration` (3+3) call the real adapters from Node against
   `NEXT_PUBLIC_BACKEND_URL`. A BFF would either be bypassed by those suites —
   making them unrepresentative of the browser path — or force booting Next inside
   the E2E harness, for no FE0B benefit.
3. **Clerk does not need it.** Clerk's browser SDK holds a short-lived session
   token; the backend's CORS is already `allow_credentials=False` with
   `Authorization` allowed, which forces the header-bearer design the experience
   plan §7.3 specifies. A BFF is required only when a server must hold a secret or
   set an httpOnly cookie. Neither requirement exists.
4. **Clerk is not in FE0B at all.** Building a BFF now would be speculative
   infrastructure for an unimplemented feature.

**What FE0B must do instead — reserve the seam (one line of design, zero code):**
keep exactly one transport module (`src/contracts/client.ts`) whose base URL comes
from exactly one accessor (`src/env.ts`). Then FE1b can choose, without touching a
single view:

- **(a) direct + interceptor** — one axios interceptor attaching
  `Authorization: Bearer ${await getToken()}` (experience plan §7.3 step 5); or
- **(b) `app/api/erp/[...path]/route.ts`** — a Route Handler proxy, if and only if
  a future requirement demands a server-held secret or a cookie session.

**If (b) is ever adopted, it is bound by these rules, stated now so they are not
invented later:** pass-through transport only — forward method, path, query, body,
`Authorization`, `Idempotency-Key`, `X-Request-Id`, `X-Correlation-Id`, and the
backend's status and error envelope verbatim. It must never read, transform,
aggregate, cache, or validate a business payload; never generate an
`Idempotency-Key`; never make a second call to satisfy one client call; and never
hold an `ofk_` integration credential. FastAPI stays the business authority in
either topology.

---

## 8. Environment variables and the secret/public boundary

| Today | FE0B | Exposure | Notes |
|---|---|---|---|
| `VITE_BACKEND_URL` | `NEXT_PUBLIC_BACKEND_URL` | **public** | may be undefined → relative URLs (today's behavior, preserved) |
| `VITE_USE_MOCKS` | `NEXT_PUBLIC_USE_MOCKS` | **public** | semantics preserved exactly: mocks ON unless the literal string `"false"` |
| `VITE_ENABLE_VOICE` | `NEXT_PUBLIC_ENABLE_VOICE` | **public** | ON only on the literal string `"true"` |
| `VITE_VOICE_URL` | `NEXT_PUBLIC_VOICE_URL` | **public** | falls back to `VOICE_DEFAULT_URL` (`http://127.0.0.1:8000`) |
| `DATABASE_URL` | `DATABASE_URL` (unchanged) | **SECRET — server only** | legacy simulator harness only; must never gain a `NEXT_PUBLIC_` prefix and must never enter the Next module graph |
| `SIMULATION_TIME_ZONE` | unchanged | server only | legacy harness |
| `VISUAL_BASE_URL`, new `VISUAL_BROWSER_PATH`, `VISUAL_SCREENSHOT_DIR` | unchanged | tooling only | not application env |

**Boundary rules:**

1. `NEXT_PUBLIC_*` values are **inlined into the client bundle at build time and
   are permanently public**. This is the same exposure Vite's `VITE_*` already had
   — FE0B adds no new exposure — but it is stated so nobody later adds a secret
   behind that prefix. All four migrated values are non-secret by nature (two URLs,
   two booleans).
2. An **unprefixed** variable referenced from client code is replaced with an
   empty string, silently. `src/env.ts` is therefore the only place that reads the
   environment, so this failure mode has exactly one place to be reviewed.
3. Static access only: `process.env.NEXT_PUBLIC_X` written literally. No
   destructuring, no computed keys — Next's inlining is a textual substitution.
4. Build-time baking means runtime env changes do not affect an already-built
   bundle — identical to Vite today. Deployment-time configuration is **not** an
   FE0B problem (no deployment work in scope), but it is recorded as a known
   property for whoever plans hosting later.
5. Never in this repo: a Clerk secret key, an `ofk_` credential, a database URL for
   the app, or any Supabase key. `.env` / `.env*.local` stay gitignored;
   `.env.example` documents the old→new mapping during the transition and drops the
   `VITE_*` names at Stage E.

---

## 9. OpenAPI generated client — preservation

1. **`src/contracts/api.ts` is frozen for the whole of FE0B.** Acceptance is
   mechanical: `git diff --numstat 2324884..HEAD -- src/contracts/api.ts` returns
   **nothing**. It is generated, and a framework migration is not a contract change.
2. **No regeneration in FE0B.** The generated file is stale against the backend
   (§1: contract mtime 2026-08-17 vs `openapi.yaml` 2026-09-05; 32 paths vs the
   backend's newer `/agent-tools/*`, `/internal/*`, `/availability-rules`,
   `/schedule-blocks`). Regenerating inside a migration would blend a contract
   delta into a framework delta and destroy the parity argument. Record the backend
   `openapi.yaml` sha256 at Stage A as the freeze marker and re-verify it at
   completion. Regeneration stays where experience plan §1.8 put it: before Agent/
   Chat work.
3. `npm run openapi:generate` keeps its exact command and relative source path
   (`../odontoflow-backend/docs/api/openapi.yaml`); `openapi-typescript` stays a
   devDependency. The command is toolchain-independent and must still run after
   Stage E — verified as part of acceptance.
4. `src/contracts/client.ts` keeps every exported function signature, every path
   string, every header, `ApiError`, `toApiError`, `newIdempotencyKey`, and the
   `export type { paths }` re-export. Its permitted diff for the entire FE0B is
   **the env import and the `baseURL` expression** — nothing else.
5. `AGENTS.md` §2 rule 1 (contracts are generated, never handwritten) is unchanged
   and re-affirmed.

---

## 10. Test migration

**Finding that shapes this section: Vitest needs almost nothing from the
framework.** No spec imports a `.tsx`, none uses jsdom, none renders React. The 91
tests are Node-level adapter, transport, and legacy-domain tests. The migration is
therefore config relocation plus env-key renames — not a test rewrite.

| Item | FE0B action |
|---|---|
| Runner | **Vitest stays.** No Jest, no runner change. |
| `vite.config.ts` `test.exclude` | moves verbatim to a standalone `vitest.config.ts` at Stage E (same 3 excluded integration specs) |
| `vitest.e2e.config.ts` | keeps the same `include` list; drop `@vitejs/plugin-react` only if verified unused |
| `@vitest-environment` | none today, none added |
| Env keys in specs | renamed at Stage B — `voice-adapter` (3), `cash-transport` (2), `agenda-integration` / `patients-integration` / `pilot-e2e` (2 each). **Assertion logic untouched.** |
| `vi.stubEnv` technique | preserved; it works against `process.env` in Node. **Do not add a `define` to the vitest config** — it is a transform-time substitution and would silently defeat the stubbing that proves the voice and mock gates. |
| `scripts/pilot-e2e.sh` | 2 exported env names renamed; DB reset, alembic, uvicorn `:8010`, and the vitest invocation unchanged |
| `tsconfig.json` | `jsx: preserve`, drop `vite/client` types, add `next-env.d.ts` + next plugin, add `app/**/*.tsx`, add `src/views/**` |
| `tsconfig.backend.json` | **untouched**; `npm run build`'s second half (`tsc -p tsconfig.backend.json` → `dist/`) and `npm start` keep working |
| AGENTS.md §5 | the three-place registration rule becomes `vitest.config.ts` exclude / `vitest.e2e.config.ts` include / `tsconfig.backend.json` exclude; §4 test count corrected 83 → measured |
| E2E intent | unchanged: browser-less Node E2E against real FastAPI + PostgreSQL through the same adapters the views bind to |

**Gate:** 91/91 pass at the end of every stage; pilot E2E 12/12 at Stage C and at
Stage E. Report measured counts, never the pinned or documented ones.

---

## 11. Browser / visual verification

`scripts/visual-check.mjs` remains **the** reproducible gate. Playwright MCP is
allowed for exploration only.

**Required changes (and only these):**

1. Stage A: `VISUAL_BROWSER_PATH` env override (fixes the hardcoded Windows Chrome
   path); `VISUAL_SCREENSHOT_DIR` env override.
2. Stage C: replace the programmatic `createServer` from `vite` on `:5189` with the
   Next server on the same port. Use `next build && next start -p 5189` rather than
   `next dev` — `next dev` compiles a route on first request, and the harness waits
   on `networkidle`, which makes cold-compile latency a flake source.

**Everything else is frozen:** the 7 flows, their order, the 1692×929 viewport and
the 1024/390 responsive pass, every accessible-name selector (`Nueva cita`,
`Cerrar modal`, `Abrir navegación`, `Sede`, `Buscar pacientes`, `Ver ficha`,
`Transferir a humano`, …), the `pageerror`/console-error failure condition, and the
screenshot filenames. **No assertion may be weakened.** A selector may change only
where the DOM legitimately moved, and each such change is justified line-by-line in
the FE0B handoff. If a flow cannot pass without weakening it, that is an abort
trigger.

**Baseline protection.** `screenshots/*.png` are Leonardo's originals, byte-verified
in `planning/VISUAL_BASELINE.md` (git-blob + sha256, 20/20 OK). FE0B writes BEFORE
captures to `.audit/fe0b-nextjs/before/` and AFTER captures to
`.audit/fe0b-nextjs/after/`, and **never** into `screenshots/`. Verify the baseline
still matches `SHA256SUMS.txt` at completion.

**Mode labelling.** The harness runs mock mode (`NEXT_PUBLIC_USE_MOCKS` default
true). Every artifact filename records its mode (experience plan §8.7). A real-mode
browser capture is not required by FE0B; if one is produced it needs the backend
running with `CORS_ALLOWED_ORIGINS` set to the Next origin, and it is labelled real.

**Parity evidence beyond the harness:** a route-by-route table capturing, for each
of the 8 paths, the HTTP status, the final URL after redirect, and the page's `h1`,
under both voice-flag settings — before (Vite) and after (Next).

---

## 12. Rollback

- One branch off `2324884` in `odontoflow-frontend`; **one commit per stage**,
  revertable in reverse order. Vite is not deleted until Stage E, so a full return
  to the Vite app is `git revert` of E, D, C.
- Nothing outside `odontoflow-frontend` is touched: no backend, no W4/n8n, no brand
  source, no `odontoflow-sim`, no `odontoflow-voice`, no `medistock`. The only
  control-plane edits (`skill-matrix.yaml` frontend lane, `current-activity.yaml`,
  `CAVELOG.md`) belong to the coordinator and are outside FE0A's write scope.
- No dependency is removed before Stage E; every earlier change is additive.
- `src/contracts/api.ts` never changes, so no contract rollback exists to perform.

**Abort triggers — stop, report, do not force through:**

1. Any of the 91 tests fails and cannot be fixed without changing page behavior or
   an assertion's intent.
2. Any of the 7 visual flows requires a weakened assertion.
3. `git diff` shows any change in `src/contracts/api.ts`.
4. The voice gate's three observable behaviors (§6.3) cannot all be demonstrated.
5. Route parity cannot be shown for all 8 paths including the `*`→`/agenda` fallback.
6. A contributor-owned file requires a **behavioral** change (§1.1).
7. Any protected surface from experience plan §12.4 needs to change.
8. The migration cannot be completed without introducing business logic into
   `app/` or a Next server (§2.1).

---

## 13. FE0B acceptance contract

**Activity:** `FE0B-nextjs-app-router-migration` · **Repo:** `odontoflow-frontend`
only · **Base:** `2324884` (re-derive with `git rev-parse HEAD` before dispatch)
**Status: READY — implementation-ready and NOT started.**

**Observable outcome (verbatim, non-negotiable):**

> The existing OdontoFlow operational frontend runs on Next.js App Router with
> route and API-contract parity, without redesigning the application or changing
> backend business behavior.

### Acceptance criteria

**Parity**
1. All 8 paths resolve with today's behavior: `/`→`/agenda`, `/agenda`,
   `/agente`, `/pacientes`, `/caja`, `/inventario`, `/chat`, and any unknown
   path → `/agenda`. Evidenced by the route table of §11.
2. `/asistente` satisfies all three rows of the §6.3 table; `test/voice-adapter.test.ts`
   passes with unchanged assertions.
3. The global patient search still navigates to `/pacientes?patient=<id>` and the
   Patients view still reads that query parameter.
4. The global "Nueva cita" modal still lives in the shell, still issues one
   `Idempotency-Key` per intent, and still fires the `appointment-created` event
   the Agenda view listens for.
5. Agenda, Patients, Cash, Inventory, Agent and Chat each render and behave
   identically in mock mode; no screen gains, loses, or fakes a data field.

**Preservation**
6. `npm run typecheck` clean on **both** tsconfigs.
7. `npm test` — **91/91 pass** (measured 2026-09-05; report the count actually
   measured at execution). No spec deleted, no assertion weakened; the only test
   diffs are the env-key renames of §10.
8. `npm run build` succeeds and still produces **both** halves: the Next build and
   `tsc -p tsconfig.backend.json` → `dist/`. `npm start` still runs the legacy
   harness.
9. `./scripts/pilot-e2e.sh` — 12/12; `agenda-integration` 3/3;
   `patients-integration` 3/3, against real FastAPI + PostgreSQL.
10. `npm run test:visual` — all 7 flows pass, **zero** `pageerror`, **zero**
    console errors.
11. Public APIs of `Button`, `Badge`, `Modal`, `DataTable`, `KpiCard`, `Column<T>`
    unchanged.
12. `src/domain/`, `src/simulation/`, `src/server.ts`, `src/index.ts`, `src/ui.ts`
    untouched.

**Contract and boundary**
13. `git diff --numstat 2324884..HEAD -- src/contracts/api.ts` is **empty**. The
    backend `openapi.yaml` sha256 matches the Stage A freeze marker. No
    regeneration was run.
14. `src/contracts/client.ts` diff is limited to the env import and the `baseURL`
    expression.
15. `src/api.ts` keeps the `useMocks` seam with identical semantics; with
    `NEXT_PUBLIC_USE_MOCKS=false` the app consumes zero mock business data.
16. Zero `'use server'` directives, zero Server Actions, zero server-side ERP
    fetching. No `app/api/**` route handler exists. Grep-verifiable.
17. `process.env` is read in exactly one application module, `src/env.ts`.
    Grep-verifiable.
18. No Clerk package, key, account or config. No Supabase client. No `ofk_`
    credential. No secret behind a `NEXT_PUBLIC_` prefix. No GCP/deployment
    artifact.
19. No business rule (price, availability, money, stock) exists anywhere under
    `app/` or in a Next server process.

**Contributor surfaces and evidence**
20. `screenshots/*.png` still verify against
    `_preservation/.../SHA256SUMS.txt`; FE0B evidence lives in
    `.audit/fe0b-nextjs/`.
21. `Co-authored-by` trailers and `.audit/voice-v1/voice-ui-port.md` are intact;
    contributed files carry mechanical diffs only (§1.1).
22. `AGENTS.md` §4 test count corrected to the measured value; §4/§5 commands and
    the three-place registration rule updated; `DEVELOPMENT.md` updated. `.env.example`
    carries only the `NEXT_PUBLIC_*` names at completion.
23. FE0B handoff records: measured test counts, both git HEADs, the pinned Next
    version, every selector change with justification, the route parity table, and
    before/after screenshots.

### Scope

**In:** the five stages of §3 — skill-lane install, visual-harness preflight, the
`src/env.ts` accessor, the Next App Router tree, `src/pages/`→`src/views/`,
react-router removal, Vite decommission, config/doc updates, evidence capture.

**Out:** any redesign or restyle (that is FE1); Clerk or any auth UI; OpenAPI
regeneration; a BFF or Route Handler; Server Actions or server-side data fetching;
any backend change; Supabase; GCP or deployment; touching `odontoflow-sim`,
`odontoflow-voice`, `ODONTO-SMART`, `medistock`, or W4/n8n; fixing the honesty
defects catalogued in experience plan §1.9 (each belongs to its own vertical).

### Blockers

**None for FE0B.** Recorded for the sequence, not for this activity: FE1's §12.3
file list must be re-based onto the Next tree; FE1b still needs decisions D1/D2 and
backend contract MC1; FE5 still needs MC3/MC4 and decision D5.

---

## 14. What this amendment did not decide

- Hosting, deployment, and runtime topology for the Next server — deliberately out
  of scope; §3.1 records only that `next start` is a Node process.
- Whether FE1b uses the direct-interceptor or the proxy transport (§7 recommends
  direct and reserves the seam; the choice is FE1b's, under the §7 rules).
- Whether any screen later benefits from server rendering — a new decision
  requiring its own amendment, not an FE0B liberty (§5).
- The stale generated contract — deliberately frozen; it stays experience plan
  §1.8's problem, before Agent/Chat work.
