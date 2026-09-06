# FE2 — Real Agenda Operations V1

## Status

- Status: PASS
- Task ID: `task_fe2_20260906`
- Dispatch ID: `ctx_fe2_20260906`
- Repository: `odontoflow-frontend`
- Writer: GPT-5.6 Luna Max frontend writer
- Base frontend HEAD: `0f0531f79ea52af5bfaa03bf7df6032365581869`
- Result frontend HEAD: `0dbfa9e6705efb5b1e6553e3841ca204533cdf97`
- Canonical backend HEAD: `254fe83ed756e8ad0100dac9ffde909fe8e8e0aa`
- Auto-advance: false; FE3 was not started

FE2 adds real Agenda operations to the FE1A Odonto Smart shell without
changing backend contracts, scheduling rules, financial behavior, or other
product verticals.

## Contract-first preflight

Source OpenAPI: `../odontoflow-backend/docs/api/openapi.yaml`.

- OpenAPI source SHA-256: `2b0929d7eef9f084b9387a9eacd832c1270a1b6c20232087c0a28cb1df0ae074`
- Existing generated frontend contract: `src/contracts/api.ts`
- Existing generated contract SHA-256: `7289f15c757d7141b0b36e9ec3921ed15c71e7df90eb3c8c0f3fcaa03990cb2f`
- A fresh `openapi-typescript` 7.13.0 generation was compared in `/tmp`.
- The 5,468-line generated diff is outside the FE2 scheduling surface: newer
  agent/internal paths, schemas, and response headers. The scheduling paths
  and FE2 schemas are already present and compatible, so `src/contracts/api.ts`
  was not regenerated.
- `src/contracts/client.ts` continues to derive response types from the
  generated contract; no handwritten scheduling response types were added.

## FE2 contract map

| Capability | Backend contract | Frontend use |
| --- | --- | --- |
| Locations | `GET /locations` → `LocationRead { id, name, timezone, is_active }` | Location filter, timezone mapping, appointment create context |
| Services | `GET /services` → `ServiceRead { id, name, duration_minutes, is_active }` | Appointment create and slot query |
| Eligible practitioners | `GET /practitioners/eligible?service_id&location_id` → `PractitionerRead { id, display_name, is_active }` | Slot-driven appointment create |
| Appointments | `GET /appointments?from_date&to_date[&location_id][&practitioner_id]` → `AppointmentListItem` | Canonical week read; names and IDs come from backend |
| Appointment detail | `GET /appointments/{appointment_id}` → `AppointmentListItem` | Drawer refresh/detail |
| Availability | `POST /slots/query` with `SlotQuery { service_id, location_id, window_start, window_end }` → `SlotResult { practitioner_id, start, end }` | Create and reschedule slot picker; no free-text real time |
| Create | `POST /appointments` with `AppointmentCreate { lead_id, service_id, location_id, practitioner_id, start }` → `AppointmentRead` | Global New Appointment, with `Idempotency-Key` |
| Reschedule | `POST /appointments/{appointment_id}/reschedule` with `{ new_start }` → `AppointmentRead` | Selected canonical slot, same practitioner, backend command, refresh |
| Cancellation | `POST /appointments/{appointment_id}/cancel` with empty `AppointmentCancel {}` → `AppointmentRead` | Explicit appointment cancellation, confirmation, refresh |

The appointment list relation is canonical: `lead_name`, `service_name`,
`practitioner_name`, and `location_name` are rendered from
`AppointmentListItem`. The practitioner filter uses the returned
`practitioner_id`/name relation; the location filter is also sent to the
backend. Status choices are derived from loaded appointment states rather than
invented UI values.

## Agenda and appointment behavior

- `/agenda` remains the main operational entry.
- Week and Day structures are available; the calendar data region remains
  flat and readable.
- Real loading, empty, and error states are explicit.
- Location, supported practitioner, and actual loaded status filters do not
  fabricate values.
- Appointment cards use canonical UTC start/end values and the location
  timezone; cancelled cards remain visible and de-emphasized.
- The drawer displays only supported lead, service, date/time, duration,
  location, practitioner, and state fields.
- Active non-cancelled appointments expose `Reprogramar` and `Cancelar cita`.
  There is no “cancel treatment” action.
- Reschedule is appointment → `POST /slots/query` → same-practitioner slot
  selection → `POST /appointments/{id}/reschedule` → list/detail refresh.
  The mutation receives only the selected backend slot instant.
- Cancellation is appointment-only and requires confirmation. No cancellation
  reason control was added because the current typed contract explicitly has an
  empty body.

## Financial boundary

`AppointmentListItem` and `AppointmentRead` expose no charge/payment
association or financial-impact projection. The cancellation contract only
changes appointment state. FE2 therefore displays no financial notice and
does not mutate charges, payments, refunds, credits, fees, or deposits.

Authority remains:

```text
browser → generated typed client → FastAPI → application/domain → PostgreSQL
```

The frontend performs no availability calculation, conflict decision,
authoritative state transition, or financial consequence calculation.

## Visual/material implementation

`odontoflow-frontend/DESIGN.md` is the canonical ERP contract and now records
the owner decision: Odonto Smart branded claymorphism is the primary
interactive material; restrained glassmorphism is secondary layering.

Material classes are explicit:

- `brand-dark`: sidebar and identity shell;
- `clay-interactive`: filters, buttons, slot controls, summary cards;
- `glass-overlay`: topbar, drawer, modal/scrim layers;
- `flat-data`: calendar, tables, forms, inventory/data grids.

Cyan and magenta remain identity accents; semantic status tokens remain
separate. The official transparent logo and Fontshare Clash Display/Satoshi
delivery remain in use. `BRAND_ASSETS.md` was retained; no new asset was
required for FE2 and no source brand repository was mutated.

The official logo is rendered through `BrandLogo`; no constructed HeartPulse
logo or hardcoded Leonardo profile remains in the product UI. The topbar user
slot is explicitly `Contexto local / Sin sesión` until FE1B/Clerk.

## Evidence

Real browser report:

- `.audit/fe2-browser-real.json`
- mode: real (`NEXT_PUBLIC_USE_MOCKS=false`)
- viewports: 1440, 1024, 390
- results: 5/5 passed
- console errors: 0
- page errors: 0
- request failures: 0

Real screenshots under `.audit/fe2-browser-real/`:

- `agenda-1440-before.png`
- `agenda-1440-after-create.png`
- `agenda-1024.png`
- `agenda-390.png`
- `appointment-drawer-1440.png`
- `appointment-after-reschedule.png`
- `cancellation-confirmation.png`
- `appointment-cancelled.png`
- `shell-mobile-drawer-390.png`
- `inventory-1440.png`

Mock visual evidence is under `.audit/fe2-visual/final/`; the visual harness
completed 7/7 flows with zero page errors.

## Verification

- `git diff --check`: PASS
- `npm run typecheck`: PASS
- `npm test`: 10 files, 91 tests passed
- `npm run build`: PASS on Next.js 16.3.4
- `npm run test:e2e:pilot`: 12 tests passed
- Agenda integration: 3 tests passed
- `NEXT_PUBLIC_USE_MOCKS=true npm run test:visual`: 7 flows passed
- Real browser FE2 harness: 5 flows passed, zero unexpected errors
- Web Interface Guidelines review: corrected drawer/modal layering,
  labelled controls, native buttons/links, visible focus, reduced-motion
  behavior, semantic status text, and responsive evidence timing; no blocking
  findings remain for the touched FE2 surfaces.

## Deviations and next

- The mobile calendar remains a contained horizontal data-region scroll at
  390px so the six-day structure is not squeezed into unreadable columns.
- Backend-conflicting or cancelled appointments remain visible as canonical
  records; FE2 does not hide or resolve them in the UI.
- No backend writer, OpenAPI regeneration, Clerk work, Agenda V2 follow-up,
  Inventory V2, Collections, Patients V2, n8n, or Agent Cockpit work was
  started.
- Next: stop and await an explicit FE3 dispatch.
