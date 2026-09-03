# V2.2 — Named Scenario Configuration — FOREMAN living brief

> Written for the Architect. Self-contained: readable without opening code.
> **Live document** — opened before any change, updated as decisions are made.

## Executive status

**Phase: OPENED — no change made yet.** Verdict: PENDING.

V2.2 replaces the simulator's one hard-coded clinic with a named, validated
**Scenario Configuration** — while the default scenario must reproduce today's
simulator exactly, byte for byte.

**Active gate:** none. This activity is authorised end to end by the brief.

**Baseline reconfirmed before touching anything** (V2.1's numbers, unchanged):
typecheck clean · **109 tests PASS** (12 files) · build PASS · `npm run
verificar` → *"Recorrido completo sin fallos"*.

## Objective and success criteria

**Objective.** Introduce a `ScenarioDefinition` contract and a pure
`compileScenario` boundary so the clinic's patients, doctors, treatments,
appointments, waitlist and patient-behaviour probabilities become named,
swappable, validated configuration — without touching the engine, the
transitions, the replay runtime, or the waitlist/risk logic, and without
changing the baseline scenario's observable behaviour in any way.

**Constraints set by the brief:**

- Do not rebuild the simulator. Do not rewrite engine / transitions /
  replay-runtime / waitlist logic / risk logic unless a small, strictly
  necessary adaptation is required — and if one is, explain it here.
- `baseline` scenario **must** reproduce exactly: 28 patients, 4 doctors, 10
  treatments, 60 appointments, 5 waitlist candidates, the existing labs/jobs,
  rules, demo roles, and the current demo start/end.
- No `Math.random`. Same scenario + same identifiers ⇒ same behaviour and same
  world, always.
- TypeScript/domain-native representation — no YAML, no config framework.
- Extend the existing configuration UI; do not build a second admin app or a
  full CRUD surface for all 60 appointments.
- The V2.1 synthetic boundary stays visible and non-dismissible.
- No cross-repo integration of any kind (§11 of the brief, restated in
  "Risks" below).
- Never rewrite donor history; keep provenance explicit for any contributor
  file touched.

**Acceptance criteria:**

| Criterion | Status |
|---|---|
| Baseline reconfirmed before modification | **DONE** — 109 tests, build, verify all clean |
| `ScenarioDefinition` contract defined | PENDING |
| `compileScenario(scenario) -> Catalogo` pure boundary | PENDING |
| `baseline` scenario compiles to a `Catalogo` deep-equal to today's `catalogoBase()` | PENDING |
| Patient behaviour probabilities parameterized, no `Math.random` | PENDING |
| Three named scenarios exist: `baseline`, `no-show-heavy`, `cancellation-recovery` | PENDING |
| Existing config UI extended: scenario selection, rules, behaviour, doctors, treatments | PENDING |
| Validation function rejects the required invalid-scenario cases | PENDING |
| Determinism contract proven by tests (replay-twice, rewind, scenario-switch) | PENDING |
| `reloj-sentinel` and `banda-sintetica` sentinels still pass | PENDING |
| No product change outside `odontoflow-sim` and Repo 0 | PENDING |
| Full contract green after the change (typecheck / test / build / verificar) | PENDING |

## Repository reality

**Canonical state before the activity**, verified by git — all five repos
clean and synced: planning `c2c8b6b` · backend `23527c2` · frontend `a967b24` ·
voice `4149a3e` · sim `da203a9` (master).

**What V2.1 already established, not re-derived here:** the simulator is a
pure, deterministic clinic engine. Authorship: Alejandro Marcelo (6 commits) +
Leonardo Panduro (1). A structural synthetic-data boundary
(`BandaSintetica`) is mounted in the shell's sticky header, guarded by 10
sentinel-style tests plus the clock sentinel (33 assertions, one per source
file).

**Where the seed and behaviour actually live**, read directly from the code
before designing anything:

- `src/domain/tipos.ts` — the `Catalogo` shape the runtime consumes:
  `pacientes`, `odontologos`, `tratamientos`, `citas`, `reglas`, `listaEspera`,
  `laboratorios`, `trabajosLab`. This shape is **not touched**.
- `src/domain/seed.ts` — `catalogoBase()` builds all of the above from literal
  data, including a **non-trivial reassignment algorithm**: an appointment
  spec's original doctor gets swapped for the first available same-day,
  non-overlapping doctor if the original doesn't work that day. This is real
  computation, not just data, and it is order-dependent.
- `src/domain/paciente-sim.ts` — `respuestaDe()` decides how a patient reacts
  to a reminder. Two things are hard-coded here: `ESCENARIO_DEMO` (4 patients
  with scripted, always-the-same reactions, checked **before** anything
  probabilistic) and the probability constants themselves (`0.62` confirm,
  `0.13` reschedule, `25 %` silence as the implicit remainder, eroded by prior
  no-shows via `0.1`/`0.25`/`0.7`/`0.3`).
- `src/runtime/mundo.ts` — `reproducir(cat, eventos, reglas, target)` is the
  **one call site** of `respuestaDe()` (line 626). It also imports `DEMO_START`
  directly from `seed.ts` as a module-level constant to drive its replay loop.
- `src/store/OdontoStore.tsx` — calls `catalogoBase()` once via
  `useMemo(catalogoBase, [])` (empty deps: computed exactly once, ever), and
  threads `reglas` as an **independent, live-editable piece of state**,
  separate from `cat.reglas` — the precedent I intend to follow for the new
  scenario/behaviour state.
- `src/components/VistaReglas.tsx` — the existing settings screen: 5 rule
  fields, per-field validation, a disabled-until-valid Save button, a Discard
  button, an explanatory panel. This is the UX to extend, not replace.

**A structural fact that shapes the whole design:** `DEMO_START`/`DEMO_END`
are imported as bare module constants by **four** runtime files
(`mundo.ts`, `horario.ts`, `snapshot.ts`, `siguiente-evento.ts`), not threaded
as parameters. Making the calendar window genuinely different **per scenario**
would require changing all four — that crosses from "small adaptation" into
"runtime rewrite," which the brief forbids without strict necessity. See
"What we will build" for the scoped decision this leads to.

**Protected surfaces:** backend, frontend, voice, MediStock (all untouched, as
in V2.1), the donor's commit history, `tests/reloj-sentinel.test.ts`,
`tests/banda-sintetica.test.tsx`, and the engine/transitions/waitlist/risk
modules (data-in, decision-out; no parameterization needed there — the
*inputs* they receive become scenario-driven, not their logic).

## Authority and evidence used

- **Repo 0** first, per protocol: `STATUS.md`, `PLAN.md`, `CAVELOG.md`, `HANDOFFS.md`.
- **V2.1's own documents**, reused, not re-audited: `odontoflow-sim/CANONICAL.md`,
  `SYNTHETIC_CLINIC_CONTRIBUTION_MAP.md`, the V2.1 living brief.
- **The current source**, read directly rather than assumed: `tipos.ts`,
  `seed.ts`, `paciente-sim.ts`, `mundo.ts`, `OdontoStore.tsx`,
  `VistaReglas.tsx`, `reloj-sentinel.test.ts`.

**Originality boundary.** The engine, the runtime, the domain vocabulary and
the existing UI are Alejandro Marcelo's and Leonardo Panduro's. This activity
adds a new configuration layer on top and makes the minimum number of
call-site adaptations needed for that layer to actually drive the existing
engine — each one is named and justified below, not silently absorbed into a
larger refactor.

## What we will build and how

**New files (mine), contributor files untouched by their addition:**

- `src/domain/scenario.ts` — the `ScenarioDefinition` contract plus
  `validateScenario()`, a pure function returning a list of human-readable
  errors. Field names follow the brief's own example (`metadata`, `calendar`,
  `rules`, `doctors`, `treatments`, `patients`, `appointments`, `waitlist`,
  `behavior`, `scriptedRoles`) — English, because this is a new layer, not a
  rename of the contributors' Spanish domain vocabulary underneath it.
  `laboratories`/`labJobs` are included as representable, per the brief,
  without expanding that domain.
- `src/domain/scenario-compiler.ts` — `compileScenario(scenario) -> Catalogo`,
  exactly the boundary the brief names, plus a small sibling
  `compileComportamiento(scenario)` for the behaviour parameters (see below),
  and a pure `mergeScenarioOverrides()` used by the editable UI.
- `src/domain/scenarios/{baseline,no-show-heavy,cancellation-recovery}.ts` —
  the three named scenarios, plus an `index.ts` registry.

**Reused contributor types, not duplicated:** `ScenarioDefinition` embeds
`Odontologo`, `Tratamiento`, `Paciente`, `Laboratorio`, and `Reglas` **directly
from `tipos.ts`**, so a doctor or a treatment is definitionally the same shape
whether it comes from a scenario or from the old seed. Appointments and
waitlist entries get a small scenario-native shape (`ScenarioAppointment`,
`ScenarioWaitlistCandidate`) because the runtime's `Cita`/`CandidatoListaEspera`
carry a *derived* `endsAt`/other fields the compiler computes — the scenario
should declare intent, not precompute what the compiler owns.

**The baseline scenario is derived from `catalogoBase()`, not transcribed by
hand.** Rather than hand-copying 60 appointments' resolved times and
doctor assignments (real risk of a silent transcription error against the
brief's own "must reproduce exactly" requirement), `scenarios/baseline.ts`
calls the existing `catalogoBase()` once and maps its **output** back into
`ScenarioDefinition` shape (dropping only the fields the compiler will
recompute: `endsAt`, `remindedAt`). This makes the equivalence test a real test
of the compiler's correctness — `compileScenario(baseline)` must independently
recompute the same `endsAt` values via the same duration formula, not merely
echo them back.

**Patient-behaviour parameterization — backward-compatible by construction.**
`paciente-sim.ts` gets a new exported type `ComportamientoConfig` and a new
exported constant `COMPORTAMIENTO_BASE` built from the **exact current
numbers** (`0.62`, `0.13`, and the `0.1`/`0.25`/`0.7`/`0.3` erosion formula),
with `scriptedRoles: ESCENARIO_DEMO` — `ESCENARIO_DEMO` itself stays exported
and unchanged, so the one existing test that imports it directly keeps
passing untouched. `respuestaDe()`'s signature gains one **optional** fourth
parameter, `comportamiento: ComportamientoConfig = COMPORTAMIENTO_BASE`. Every
existing 3-argument call site — in `mundo.ts` and in `tests/paciente-sim.test.ts`
— continues to compile and continues to observe **identical** behaviour,
because the default *is* the old hard-coded behaviour, not an approximation of
it.

**The one adaptation to a contributor runtime file:** `mundo.ts`'s
`reproducir()` gains one new **optional** parameter,
`comportamiento: ComportamientoConfig = COMPORTAMIENTO_BASE`, threaded to its
single `respuestaDe()` call site. Every existing 4-argument call — all of
`tests/mundo.test.ts`, `tests/cancelacion.test.ts`, `tests/actividad.test.ts`,
`tests/lista-espera.test.ts`, `tests/render.test.tsx` — keeps compiling and
keeps observing the old behaviour by default. This is the entire "adaptation"
to `mundo.ts`: one new optional parameter, one call-site edit, zero changes to
decision logic, zero changes to the engine/transitions/waitlist/risk modules.

**The calendar-window scoping decision — stated plainly, not hidden.**
`ScenarioDefinition.calendar.start/end` is a real, validated field
(`start < end` is enforced). For V2.2, all three named scenarios use the
**same** window as today's demo (`DEMO_START`/`DEMO_END`, unchanged constants
in `seed.ts`) — none of the three scenario descriptions in the brief call for
a different window; they vary behaviour and appointment mix, not the calendar.
`mundo.ts`, `horario.ts`, `snapshot.ts` and `siguiente-evento.ts` are therefore
**not touched** at all for calendar purposes — they keep importing
`DEMO_START`/`DEMO_END` exactly as before. Making the window itself
scenario-driven is **not built here**; it would require threading a parameter
through all four files, which is a runtime change bigger than "small," and no
scenario in this activity needs it. Flagged as a named limitation, not a gap
discovered later.

**Editable UI — extends `VistaReglas.tsx` in place, does not replace it.** The
existing 5-field rules section is untouched. New sections are appended in the
same view/tab: scenario selection (a `<select>` over the 3 named scenarios,
with their `metadata.description` shown), behaviour probabilities (confirm %,
reschedule %, with silence % shown as the **explicit derived remainder**,
`1 − confirm − reschedule`), and editable lists for doctors (name, specialty,
days attended) and treatments (name, duration, synthetic price — labelled as
such). Patients, appointments, waitlist and laboratories remain
scenario-defined, non-editable data in V2.2, exactly as the brief scopes it.

**How an edit takes effect.** The store keeps `escenarioId` plus a small
`overrides` record (`doctors?`, `treatments?`, `behavior?` — each, when
present, a **full replacement** of that section, not a partial merge; simplest
semantics, lowest bug surface). Any edit is applied by building the
**effective** `ScenarioDefinition` (base scenario + overrides),
**validating it**, and only committing if valid — exactly the same
disabled-until-valid pattern `VistaReglas.tsx` already uses for rules. A valid
edit deterministically recompiles `Catalogo`/`ComportamientoConfig` and the
replay recomputes from `DEMO_START`, precisely mirroring how a rules edit
already forces a full recalculation today.

**Deliberately not built**, per the brief's explicit exclusions and this
activity's own scope: any FastAPI connection, a simulator principal, an intent
adapter, an evaluator, canonical appointment states, waitlist/lab backend
tables, voice-vocabulary integration, a simulator screen ported into the
canonical frontend, agents, WhatsApp, editable patients/appointments/waitlist,
and a scenario-specific calendar window.

## Execution model

**Solo.** A dependency chain — contract, compiler, baseline derivation,
behaviour parameterization, scenarios, UI, validation, tests, full
re-verification — where each step's output is the next step's input, and
several steps touch the same handful of files (`OdontoStore.tsx`,
`VistaReglas.tsx`). No independent pieces exist to parallelize, and the
determinism requirement means every step needs the previous step's tests
green before proceeding, not compared against a parallel branch.

## Risks, conflicts, and protected surfaces

| Risk | Mitigation |
|---|---|
| **Silently changing baseline behaviour** | `baseline.ts` is *derived from* `catalogoBase()`, not transcribed; an equivalence test asserts `compileScenario(baseline)` is deep-equal to `catalogoBase()`, and a second asserts `compileComportamiento(baseline)` is deep-equal to `COMPORTAMIENTO_BASE`. |
| **`Math.random` creeping in for "randomized" scenarios** | Not used anywhere; `no-show-heavy` and `cancellation-recovery` only change the *parameters* fed into the existing hashed-id derivation in `respuestaDe()`, which stays 100 % deterministic. |
| **Breaking existing tests via a required new parameter** | Both new parameters (`respuestaDe`'s and `reproducir`'s) are **optional with defaults equal to old behaviour** — every existing call site keeps compiling and keeps passing unmodified. |
| **The synthetic boundary getting weakened while scenarios become editable** | Explicitly named as the standing precondition in V2.1's own handoff; `BandaSintetica`'s mount point in `Estacion.tsx` is not touched by this activity, and its 10-test sentinel is re-run as part of final verification. |
| **Cross-repo scope creep** | Only `odontoflow-sim` and Repo 0 change. Backend/frontend/voice are verified unmodified before push. |
| **The calendar-window field being decorative rather than real** | It is genuinely validated (`start < end`) and genuinely equal across all three scenarios by a documented, scoped choice — not silently ignored. |

## Evidence and validation

PENDING — nothing has been changed yet. Will record, per the brief's own
requirements: typecheck / full test count / build / `verificar` before and
after, the equivalence test results, the determinism test results, and manual
or deterministic proof of scenario switching plus each editable field.

## Decision and progress log

| Date | Entry |
|---|---|
| 2026-09-03 | **Brief opened before any change**, per instruction. |
| 2026-09-03 | Canonical state verified clean and synced across all five repos; sim baseline reconfirmed unchanged (109 tests, build, verify all green) before touching anything. |
| 2026-09-03 | Read `tipos.ts`, `seed.ts`, `paciente-sim.ts`, `mundo.ts`, `OdontoStore.tsx`, `VistaReglas.tsx`, `reloj-sentinel.test.ts` directly rather than assuming their shape from the brief's own sketch. |
| 2026-09-03 | **Design decision: `baseline.ts` derives from `catalogoBase()` rather than transcribing 60 appointments by hand** — turns the "must reproduce exactly" requirement into a mechanically-guaranteed property instead of a manual-transcription risk. |
| 2026-09-03 | **Design decision: both new parameters (`respuestaDe`'s 4th, `reproducir`'s 5th) are optional with defaults equal to today's hard-coded behaviour** — every existing call site and test needs zero changes to keep passing. |
| 2026-09-03 | **Design decision: the calendar window is validated but scoped-equal across all three V2.2 scenarios**, because making it genuinely per-scenario would require touching four runtime files — beyond "a small adaptation," and not needed by any of the three scenarios this activity defines. Recorded as a named limitation, not discovered later. |

## Next approval / next step

Implement in order: the contract and its validator, the compiler, the baseline
derivation with its equivalence test, the behaviour parameterization with its
backward-compatibility proof, the two new named scenarios, the UI extension,
the determinism test suite, then full re-verification of the whole contract.

Update this brief at each checkpoint; do not defer the write-up to the end.
