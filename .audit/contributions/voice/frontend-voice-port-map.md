---
title: Frontend voice contribution — port map
status: evidence
date: 2026-09-02
donor_pr: https://github.com/leonardopanduro-rgb/ODONTO-SMART-FRONT/pull/1
donor_ref: alejandro/feat/asistente-voz
donor_head: c0f418dc5b296715fa4b0a6cb8cbd0da9f7eba0f
donor_base: 8769f12f5e3144fe5c2032d0f8445861dc304c76
canonical_head: 9595abdc3f77437ddb10e6816caf435deac00cb8
author: Alejandro Jesus Marcelo CH (AlejandroMarceloCh)
authority: CONTRIBUTOR SOURCE — NOT canonical
---

# Frontend voice contribution — port map

**Nothing was merged, cherry-picked or rebased.** The donor ref is fetched and
intact at `alejandro/feat/asistente-voz`. Canonical `main` is untouched at
`9595abd`.

## PR facts (verified via `gh`, not assumed)

| Field | Value |
|---|---|
| PR | leonardopanduro-rgb/ODONTO-SMART-FRONT **#1**, **OPEN**, not draft |
| Title | Vista Asistente de voz: dictado de inventario y resumen de consulta |
| Author | `AlejandroMarceloCh` (Alejandro Jesus Marcelo CH) |
| Created / updated | 2026-08-15T12:46:49Z / 2026-08-16T16:02:05Z |
| Base | `main` @ `8769f12` (Leonardo's repo) |
| Head | `feat/asistente-voz` @ **`c0f418d`** — matches the expected SHA exactly |
| Size | **+390 / −5** across **6 files**, 2 commits |
| `mergeable` | MERGEABLE — **but only against `8769f12`**, not against ours |

Commits (both by Alejandro Marcelo):
- `e5f4256` 2026-08-15 · feat: vista Asistente de voz
- `c0f418d` 2026-08-16 · feat: vista Asistente de voz rediseñada al mockup

## Why merge status is irrelevant here

Canonical `main` is **7 commits ahead** of the donor's base, with
**36 files changed, +6 735 / −370** in between. GitHub says MERGEABLE because
it evaluates against Leonardo's `main`; against ours the contribution must be
**ported deliberately, file by file**.

Per instruction, the contribution is **not judged by conflicts**. The
assessment below is about intent and current-contract fit. The product/UX
intent — *the dentist dictates; the system fills what is done by hand* — is
sound, wanted, and preserved in full.

---

## Per-file classification

### `src/App.tsx` (+2/−0) → **PORT_DIRECTLY**

Adds the `AsistenteVozPage` import and a `<Route path="asistente">`.

**Canonical has not touched this file since the donor's base.** The patch
applies as-is; the `asistente` route is free (verified). Zero risk.

### `src/components/Navbar.tsx` (+2/−1) → **PORT_DIRECTLY**

Adds the `Mic` icon import and a 7th nav item `{ to: "/asistente", label: "Asistente", icon: Mic }`.

**Canonical has not touched this file either.** `lucide-react` is still a
dependency (`^0.468.0`), so `Mic` resolves. Zero risk.

### `src/types.ts` (+64/−0) → **PORT_DIRECTLY**

Adds 8 purely additive interfaces: `VoiceHealth`, `VoiceTranscription`,
`VoiceStockRow`, `VoiceStockSummary`, `VoiceVisitSummary`, `VoiceAttachment`,
`VoiceMessage`, `VoiceReply`, `VoiceTurn`.

Canonical changed this file (+83/−74) but **defines nothing named `Voice*`
(verified by grep) — there is no collision.** The additions are append-only and
mirror `CONTRATO-API.md` exactly.

One naming note, not a blocker: these types use the donor's Spanish wire names
(`paciente_ref`, `cantidad_consumida`, `total_bruto`, `metodos_pago`). That is
**correct** — they describe the voice service's wire format, and renaming them
would hide the contract. The translation to OdontoFlow's own English domain
names belongs in the adapter, not in the type.

### `src/index.css` (+103/−4) → **PORT_WITH_ADAPTER**

103 added lines: flat BEM classes for the assistant view (including `.tabular`,
which **canonical does not define** — verified, so the page needs this CSS).

The 4 modified lines are the **navbar squeeze**: `.nav-link` `min-width`
160 → 118 px, `.main-nav__links` `gap` 27 → 15, and 135 → 104 / gap 8 at the
1450 px breakpoint. The author explains it: a 7th item overflowed below 1600 px,
and says in the PR *"Si prefieres otra solución —un menú «más», o mover el
asistente dentro de `/chat`— dime y lo cambio."*

**Canonical has not modified those lines**, so the patch would apply — but this
is a **global change to every nav item's geometry** to fit one new item. It is
the one donor change that should be a deliberate design decision rather than an
automatic port. Adapter: take the 103 additive lines as-is; decide the navbar
question separately (squeeze, overflow menu, or nest under an existing route).

### `src/api.ts` (+26/−0) → **PORT_WITH_ADAPTER**

Adds a second axios instance and five voice calls:

```
voiceApi = axios.create({ baseURL: import.meta.env.VITE_VOZ_URL ?? "http://127.0.0.1:8000" })
getVoiceHealth · sendVoiceText · sendVoiceAudio · restartVoiceSession · editVoiceField
```

Architecturally this is the right seam — canonical still routes every page
through `src/api.ts` as the façade (verified: all 6 pages import from `../api`),
which then dispatches between `mockData` and the real `src/contracts/client.ts`.
The donor's additions are append-only and collide with nothing (`grep Voice`
in canonical `api.ts` → nothing).

**Three adaptations are required, and one of them is a real invariant breach:**

1. **`VITE_USE_MOCKS` is bypassed.** Every other canonical call is gated on
   `useMocks`; the voice calls are not. So with `VITE_USE_MOCKS=true` — the
   default in `.env.example` — the assistant page would still fire live HTTP at
   a real service. That breaks the canonical guarantee that mocks mode performs
   no real calls, which M4 established and the pilot E2E depends on. The port
   must add a mock path (or an explicit "voice unavailable in mocks" state).
2. **`VITE_VOZ_URL` is undeclared.** Canonical declares its env vars in
   `.env.example` (only `VITE_BACKEND_URL` and `VITE_USE_MOCKS` exist today).
   The port must add `VITE_VOZ_URL` there.
3. **The hardcoded `http://127.0.0.1:8000` fallback** silently points at
   localhost in any environment. Canonical's convention is an explicit env var
   with the E2E harness port documented; follow it.

### `src/pages/AsistenteVozPage.tsx` (+193/−0, new file) → **PORT_WITH_ADAPTER**

The whole feature. No conflict — the file does not exist in canonical.

**What it does well, and should be preserved:**
- **Reuses canonical components** rather than inventing its own: `Badge` and `DataTable`. Both APIs are still compatible — `Badge` takes `tone?: Tone` and `Tone` still includes `green`/`amber` (verified); `Column<T>` is still `{key, header, width?, render}` (verified). This is exactly the right instinct for a contributor.
- **Degrades gracefully.** `getVoiceHealth()` on mount sets a `conectado` tri-state; if the voice service is absent the page shows an empty state and an amber pill instead of crashing.
- **Surfaces latency** (`12 s de audio · procesado en 2.4 s`) under each dictation — a deliberate trust affordance, and the right one for a slow local model.
- **Records via `MediaRecorder`** with permission-denied and empty-audio handling, and a `blob.size > 1200` guard against silent clips.
- **Editable summary fields** that round-trip through `editVoiceField`, so a hand correction re-enters the parser instead of storing raw text.

**Adaptations required:**
1. Depends on the `src/api.ts` voice functions → inherits all three adapter items above.
2. Depends on the `.tabular` CSS class it brings in `index.css` → port the CSS together with the page, or the numbers lose their alignment.
3. **Browser support:** `MediaRecorder` + `getUserMedia` require a secure context (HTTPS or `localhost`). On a LAN IP over plain HTTP the microphone will silently not work. Must be stated in the deployment note.
4. **No test.** Canonical carries 83 unit tests plus a pilot E2E; this page arrives with none. Not a reason to reject it — a reason to write one at port time.

---

## Nothing is OBSOLETE, nothing is discarded

No donor change falls into `OBSOLETE` or `REIMPLEMENT_AGAINST_CURRENT_CONTRACT`.
The contribution targets a **separate voice service**, not OdontoFlow's own API,
so canonical's contract evolution (the `contracts/`+`domain/` layers added after
the donor's base) does not invalidate any of it.

`KEEP_AS_REFERENCE` applies to exactly one thing: **the navbar squeeze**, which
should be kept as the author's documented reasoning about the overflow while the
final navigation decision is made separately.

## Summary

| File | Classification | Blocker |
|---|---|---|
| `src/App.tsx` | **PORT_DIRECTLY** | none |
| `src/components/Navbar.tsx` | **PORT_DIRECTLY** | none |
| `src/types.ts` | **PORT_DIRECTLY** | none |
| `src/index.css` | **PORT_WITH_ADAPTER** | navbar geometry is a design decision |
| `src/api.ts` | **PORT_WITH_ADAPTER** | **`VITE_USE_MOCKS` bypass** · undeclared `VITE_VOZ_URL` · hardcoded localhost |
| `src/pages/AsistenteVozPage.tsx` | **PORT_WITH_ADAPTER** | inherits the api.ts items · needs its CSS · secure-context requirement · no test |
| navbar squeeze rationale | **KEEP_AS_REFERENCE** | — |

**Overall: a high-quality, well-behaved contribution.** It reuses the existing
design system, degrades gracefully, and documents its own trade-offs. The single
substantive defect is the `VITE_USE_MOCKS` bypass, which is a one-function fix
and understandable — the donor branched before that convention was tightened.
