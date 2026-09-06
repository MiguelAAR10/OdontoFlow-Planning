# OdontoFlow FE0 — Frontend Engineering Bootstrap — CTO handoff

**Status: FE0 PASS. FE0B is READY and not started.** This is a compact,
self-contained handoff for Joel/CTO and the next coordinator.

## Decision and outcome

The owner standardized `odontoflow-frontend` on **Next.js App Router**. That
decision supersedes only the existing experience plan's Vite/React Router
decision; the rest of the experience plan remains the product direction.

FE0 did not migrate or redesign the application. It produced the amendment,
installed the narrow frontend skill environment, extracted the real Odonto
Smart brand contract/assets, made the browser harness runnable in WSL, captured
a current baseline, and prepared:

> The existing OdontoFlow operational frontend runs on Next.js App Router with
> route and API-contract parity, without redesigning the application or
> changing backend business behavior.

## Planning authority

- Amendment: `docs/plans/2026-09-05-frontend-nextjs-amendment.md`
- Orca run: `run_a673e67013d6`
- One planning task: `task_5b919935e97b`
- Planner dispatch: `ctx_be583922193a`
- Planner model: Claude Opus 5; `worker_done` received; planner released
- Amendment is frozen after coordinator validation against the real repository.

The amendment covers the twelve requested topics: staged reversible migration,
route/behavior parity, target boundaries, Server/Client split, FastAPI
integration, bounded BFF decision, env migration, frozen generated client,
test migration, browser verification, rollback, and exact FE0B acceptance.

## Repository reality at FE0

`odontoflow-frontend` is still the current Vite SPA: Vite 6.1, React 18.3,
React Router 6.28.1, TypeScript, Axios and Vitest 3.2.7 installed. HEAD is
`2324884f7e916f44442a57c897cacb91add0ba1e`; its pre-existing dirty surface is
`AGENTS.md` only.

Current routes are `/`, `/agenda`, `/agente`, `/pacientes`, `/caja`,
`/inventario`, `/chat`, flag-gated `/asistente`, and `*` → `/agenda`.
`src/api.ts` is the mock/real façade; `src/contracts/client.ts` owns Axios,
typed generated paths, `ApiError` and per-intent `Idempotency-Key`; the
generated `src/contracts/api.ts` remains stale relative to backend OpenAPI and
is explicitly frozen for FE0B. `VITE_USE_MOCKS` defaults to mocks, voice is
controlled by `VITE_ENABLE_VOICE`, and no direct browser Supabase/Auth or Clerk
configuration exists.

Backend authority was verified at
`254fe83ed756e8ad0100dac9ffde909fe8e8e0aa`. No backend contract or business
behavior was changed.

## Skills

Installed in the frontend through the current Skills CLI; remote provenance and
hashes are in `odontoflow-frontend/skills-lock.json`:

- `frontend-design` ← `anthropics/skills`
- `next-best-practices` ← `vercel-labs/openreview` (current matching Vercel
  Labs source discovered at execution)
- `vercel-react-best-practices` ← `vercel-labs/agent-skills`
- `web-design-guidelines` ← `vercel-labs/agent-skills`
- `webapp-testing` ← `anthropics/skills`

`odontoflow-engineering` and `verification-before-completion` are discoverable
through symlinks to their planning/backend canonical bodies; no bodies were
duplicated. The control-plane lanes are `frontend-foundation`, `frontend-ui`,
`frontend-auth`, and `frontend-review`. Clerk entries are registered as
desired/not-yet-loaded under `frontend-auth`; no Clerk account, package or
configuration was created.

## Brand and typography

Contract: `odontoflow-frontend/docs/brand/odonto-smart-contract.md`.
Provenance: `odontoflow-frontend/public/brand/odonto-smart/BRAND_ASSETS.md`.
The source repository remained read-only.

Source-extracted brand values include:

| Token | Value |
| --- | --- |
| brand cyan | `#41D4CB` |
| brand cyan strong | `#2BB5AD` |
| brand magenta | `#DE1BCE` |
| brand deep | `#1A0A2E` |
| dark background | `#0A0F1A` |
| canvas | `#FAFBFC` |
| surface | `#FFFFFF` |
| soft surface | `#F0FDFB` |
| primary text | `#0F172A` |
| secondary text | `#475569` |
| border | `#E2E8F0` |

Semantic status roles remain separate: success `#0CA453`, warning `#EC8A00`,
danger `#E51C3A`, info `#0872C9`. Cyan is not success and magenta is not
danger. Clash Display is reserved for display headings/key metrics; Satoshi is
for navigation, forms, tables, buttons and labels. No font binaries were
copied; the source's Fontshare CSS delivery is the recorded mechanism.

Copied assets are the approved horizontal, compact, circular and high-resolution
transparent PNG variants plus one documented real-clinic image. The opaque SVG,
Zone.Identifier files, source code, env/credential material, patient data and
obsolete assets were excluded.

## Browser evidence

Harness change: `scripts/visual-check.mjs` now supports WSL Playwright Chromium
selection, an installed-revision fallback, `VISUAL_BROWSER_PATH`, and an
evidence-only `VISUAL_SCREENSHOT_DIR`. No UI code was changed.

Baseline evidence: `odontoflow-frontend/.audit/fe0-bootstrap/`.
`BASELINE.md` records runtime, hashes and seven current-browser route captures.
The capture reported zero page errors and zero console errors. The legacy
interaction runner also exposed two pre-existing selector drifts (Cash heading
expectation and Inventory option-value selection); they are recorded for FE0B
and were not hidden by changing product behavior.

## Verification and scope integrity

- `npm test`: **10 files, 91/91 passed**
- `npm run typecheck`: passed for both TypeScript projects
- `npm run build`: Vite build and backend TypeScript half passed
- `skills list --json`: all seven local skill names discoverable
- brand source `ODONTO-SMART`: unchanged except its pre-existing untracked docs
- backend: no changes
- W4/n8n: untouched; still externally blocked pending Leonardo access
- no Next.js migration, Clerk configuration, OpenAPI regeneration, backend
  behavior change, Supabase browser access, GCP/deployment work or redesign

FE0 changes are limited to planning/current-activity/CAVELOG, frontend skill
installation and lock metadata, brand documentation/assets, and visual
test/evidence harness surfaces. The pre-existing frontend `AGENTS.md` change
was preserved and not mixed into this activity.

## Next activity: FE0B

Control plane: `orchestration/current-activity.yaml`.

FE0B is **Next.js Parity Migration**, `advance_automatically: false`. Before
dispatch, re-derive both HEADs and use the amendment's staged order. Preserve
Agenda, Patients, Cash, Inventory, Agent, Chat, the voice flag, the mock seam,
OpenAPI typed behavior, idempotency and backend authority. Keep Next thin:
presentation/routing/composition only in FE0B, browser-to-FastAPI transport
direct, no BFF/Route Handler, no Server Actions, no Clerk, no redesign.
