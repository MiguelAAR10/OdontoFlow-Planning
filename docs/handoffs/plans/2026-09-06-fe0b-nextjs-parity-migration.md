# FE0B — Next.js parity migration handoff

Status: PASS. FE0B is complete; FE1 is not started.

## Outcome

The existing OdontoFlow operational frontend now runs on Next.js App Router
with observable route and API-contract parity. This was a framework migration,
not a redesign, auth implementation, data-layer rewrite, or backend change.

| Marker | Value |
|---|---|
| Target repository | `odontoflow-frontend` |
| Previous platform | Vite + React Router |
| New platform | Next.js `16.3.4` App Router + React `18.3.1` |
| Base HEAD | `f31a66c645bd01f09fbe3a27abd454337cab77cf` |
| Result HEAD | `e6b86481f9180fec496885b9d9ab25f1ebf462bb` |
| Commit | `feat: migrate frontend to Next.js App Router` |
| Published | `origin/main` |
| Backend HEAD observed | `254fe83ed756e8ad0100dac9ffde909fe8e8e0aa` |
| Orca task | `task_648128ef391a` |
| Orca dispatch | `ctx_a1f345b2cfc9` |
| Worker | GPT-5.6 Luna Max (`gpt-5.6-luna`, max) |

## Route mapping

| Existing surface | App Router surface | Result |
|---|---|---|
| `/` | `app/page.tsx` → `redirect("/agenda")` | preserved |
| `/agenda` | `app/(shell)/agenda/page.tsx` | preserved |
| `/agente` | `app/(shell)/agente/page.tsx` | preserved |
| `/pacientes` | `app/(shell)/pacientes/page.tsx` | preserved, including `?patient=` |
| `/caja` | `app/(shell)/caja/page.tsx` | preserved |
| `/inventario` | `app/(shell)/inventario/page.tsx` | preserved |
| `/chat` | `app/(shell)/chat/page.tsx` | preserved |
| `/asistente` | flag-gated `app/(shell)/asistente/page.tsx` | redirects to Agenda when disabled; renders when enabled |
| unknown path | `app/[...rest]/page.tsx` → `redirect("/agenda")` | preserved observably |

Next returns the expected server redirect status (`307`) for `/` and unknown
paths; the final URL and Agenda behavior match the former client redirect.

## Environment mapping

| Former Vite key | Next key | Boundary |
|---|---|---|
| `VITE_BACKEND_URL` | `NEXT_PUBLIC_BACKEND_URL` | browser-visible API base URL |
| `VITE_USE_MOCKS` | `NEXT_PUBLIC_USE_MOCKS` | browser-visible build-time mock gate |
| `VITE_ENABLE_VOICE` | `NEXT_PUBLIC_ENABLE_VOICE` | browser-visible build-time route/nav gate |
| `VITE_VOICE_URL` | `NEXT_PUBLIC_VOICE_URL` | browser-visible voice service URL |
| `DATABASE_URL` | unchanged | legacy simulator/server-only |
| `SIMULATION_TIME_ZONE` | unchanged | legacy simulator/server-only |

`src/env.ts` is the only application environment accessor and uses literal
static `process.env.NEXT_PUBLIC_*` reads. No secrets were added and no Vite
environment reference remains in the application graph.

## Component and API boundaries

- `app/layout.tsx`, route pages, root redirect, and catch-all are Server
  Components with routing/composition responsibilities only.
- `(shell)/layout.tsx`, all operational views, and interactive components remain
  Client Components because they use state, effects, browser events, and
  client-side API calls. This preserves parity instead of forcing an
  optimization rewrite.
- Browser → `src/api.ts` → `src/contracts/client.ts` → FastAPI remains the
  transport path. There is no Route Handler BFF, Server Action, Clerk,
  Supabase, direct database access, or business logic in Next.js.
- `src/contracts/api.ts` was not regenerated and has no diff. The existing typed
  endpoints, `ApiError`/`toApiError`, per-intent `Idempotency-Key` headers,
  appointment-created event, mock/synthetic seam, and backend authority remain
  intact.

## Files and surfaces

Created:

- `app/` App Router layouts, routes, root redirect, and catch-all redirect.
- `next.config.ts`, `src/env.ts`, standalone `vitest.config.ts`.
- `.audit/fe0b-nextjs/` route/mode/interaction evidence, before/after captures,
  and the target-repository handoff.

Moved or adapted:

- `src/pages/` → `src/views/` to avoid Next's reserved `src/pages` boundary.
- React Router navigation APIs → `next/link`, `usePathname`, `useRouter`, and
  `useSearchParams`.
- Vite environment access → the Next public environment contract.
- Visual harness → Next production build/start with WSL Chromium discovery,
  including `chrome-linux` and `chrome-linux64` layouts.

Removed after parity was demonstrated:

- `index.html`, `src/main.tsx`, `src/App.tsx`, `vite.config.ts`.
- Direct `vite`, `@vitejs/plugin-react`, and `react-router-dom` dependencies.
- Vite-only test/config bootstrap; the current `vitest.config.ts` preserves the
  integration exclusions.

The generated contract, domain/simulation/server harness, backend, brand source,
and W4/n8n were not changed.

## Verification evidence

Target-repository evidence is under
[`odontoflow-frontend/.audit/fe0b-nextjs/`](../../../odontoflow-frontend/.audit/fe0b-nextjs/):

- [`FE0B-HANDOFF.md`](../../../odontoflow-frontend/.audit/fe0b-nextjs/FE0B-HANDOFF.md)
  — detailed implementation handoff and freeze markers.
- `route-parity-vite-baseline.json`, `route-parity-mock-off.json`, and
  `route-parity-mock-on.json` — route, heading, redirect, voice-gate, and
  no-voice-request probes.
- `interaction-parity.json` — global patient search, native navigation, and
  New Appointment toast.
- `before/mock/` and `after/mock/` — FE0 versus FE0B captures for Agenda,
  Patients, Cash, Inventory, Agent, Chat, and responsive navigation.
- `verification-unit.log` — `npm test`: 10 files, 91/91 passed.
- `verification-typecheck.log` — both TypeScript projects passed.
- `verification-build-final.log` — Next production build plus backend `tsc`.
- `verification-pilot.log` — isolated FastAPI/PostgreSQL pilot, 12/12 passed.
- `verification-agenda-integration.log` and
  `verification-patients-integration.log` — 3/3 each against FastAPI.
- `after/visual-final.log` — 7/7 visual flows passed, zero page errors.

The two pre-existing visual-smoke selector drifts were reconciled to verified
current behavior: Cash uses `Cobros`/charge payment controls, and Inventory
selects backend location IDs rather than label values. No product behavior was
changed to satisfy stale selectors.

## Deferred debt and known deviations

- Voice-on browser verification proves the route and mock isolation; live voice
  HTTP remains external-service dependent and was not started.
- The combined `npm run test:e2e` exploratory run can collide with a previously
  seeded fixed pilot fixture. The required isolated pilot reset and isolated
  Agenda/Patients integration runs passed; this is retained as a shared-state
  harness limitation.
- Client components remain intentionally broad for parity. Server-side ERP
  fetching, BFF/auth transport, Clerk, and component/design-system work belong
  to separately planned activities.
- FE1 design work remains deferred: no brand-shell, typography redesign,
  sidebar, Clerk UI, or screen redesign was started.

## Rollback boundary

Revert commit `e6b86481f9180fec496885b9d9ab25f1ebf462bb` to return to the
Vite/React Router implementation at `f31a66c645bd01f09fbe3a27abd454337cab77cf`.
The protected FE0 baseline remains under
`odontoflow-frontend/.audit/fe0-bootstrap/`; FE0B evidence is separate.

## Next activity

Keep `advance_automatically: false`. The next recommended activity is FE1 only
after Joel/CTO accepts this handoff and the owner explicitly opens it. Do not
start Clerk, redesign, or W4/n8n work as part of FE0B.
