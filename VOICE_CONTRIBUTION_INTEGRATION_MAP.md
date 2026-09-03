---
title: OdontoFlow — Voice Contribution Integration Map
status: active
last_verified: 2026-09-02
authority: Repo 0 (planning) — synthesis; evidence in .audit/contributions/voice/
milestone: contributor intake (does not change M5 validation truth)
---

# Voice Contribution — Integration Map

One synthesis over both donor sources. **No implementation. Nothing merged.**

Evidence: `.audit/contributions/voice/odonto-voz-inventory.md` ·
`.audit/contributions/voice/frontend-voice-port-map.md` · raw runs in the same
directory · bundles and checksums in
`_preservation/odontoflow-contributors-2026-09-02/`.

Credit and exact SHAs: [CONTRIBUTIONS.md](CONTRIBUTIONS.md).

---

## 1 · WHAT THEY BUILT

Alejandro built a **complete, working voice module** in two halves that talk
over HTTP:

**A standalone voice service** (`odonto-voz`, 5 commits, 2 219 lines) in which a
dentist dictates and the system fills two things done by hand today:

- **Inventory audit** — free dictation while walking the shelf; the system names what was missed and offers to leave it as last time.
- **Visit summary** — five guided questions producing patient reference, treatments, supplies consumed, amount and payment methods, emitted as one business JSON.

**A frontend view** (PR #1, +390/−5) that consumes it: recording, a live
inventory table, a consultation stepper, an editable summary, per-dictation
latency, and a graceful offline state.

The architecture's load-bearing idea: `procesar()` is **channel-agnostic**.
Browser, WhatsApp and tests enter through the same function. That is why the
WhatsApp adapter is 118 lines and not a redesign.

The other load-bearing idea: **no LLM in the parsing path.** Rules against a
closed catalog, argued from OdontoFlow's own invariant that *"LLMs never set
prices, durations, slots or bookings"* — because a hallucinated quantity is a
real inventory discrepancy, whereas a rule failure is fixed by adding an alias.

---

## 2 · WHAT WORKS

Measured here on 2026-09-02, not taken on trust:

| Claim | Verdict | Evidence |
|---|---|---|
| Dependencies install from its own `requirements.txt` | ✅ clean, exit 0 | pinned exactly as declared, no conflict |
| Test suite | ✅ **54 passed / 0 failed / 0.69 s** | `donor-pytest-raw.txt` |
| Consultation flow over real HTTP | ✅ correct business JSON — `total_bruto: 120`, `metodos_pago: ["yape"]`, `consumo {ANESTESIA:2, AGUJA:4}`, `servicios {RESINA-SIMPLE:2, PROFILAXIS:1}` | `donor-http-textflow.txt` |
| Inventory flow over real HTTP | ✅ accumulation, missing-item report, `igual` closing 12/12 without overwriting | same |
| **Self-correction** `"tres, no, cuatro resinas"` → 4 | ✅ **works** | same |
| Mixed payment (several methods, deduplicated) | ✅ | 21 parser tests + live run |
| Frontend components reused from the design system | ✅ `Badge`/`DataTable` APIs still compatible | verified against canonical `9595abd` |
| **Audio / transcription path** | ⚠️ **UNVERIFIED on Linux** | no TTS available to drive it |
| `auditar.py` E2E harness | ❌ **macOS-only** — needs the `say` binary | `donor-auditar-raw.txt`: first 2 text checks pass, then `FileNotFoundError: 'say'` |
| WhatsApp adapter | ❌ **unverified**, by the author's own notice | never exercised |

`auditar.py` is **platform-bound, not broken.** Per instruction, no repair was
attempted.

---

## 3 · WHAT IS TESTED

**54 tests, all passing, none touching audio or network** — which is why the
suite runs in under a second.

| Area | Tests | Coverage quality |
|---|---|---|
| `parser.py` | 21 | **Excellent.** Number words, `"veintiséis y veintisiete"` as two numbers, self-correction, filler words, long-alias-wins, one number never split across two products, quantity after the noun, and *"text with no catalog match invents nothing"*. |
| `conversacion.py` | 19 | **Good.** Both flows, missing-item report, `igual`, accumulation, last-value-wins, re-ask on unrecognized input, numbered menu. |
| `main.py` (API) | 9 | **Adequate.** Health, catalog, session isolation, 404s, full consultation, field editing, invalid field. |

**Untested:** `transcriptor.py` (no test touches audio), `whatsapp.py` (zero
tests), and the frontend page (zero tests — canonical carries 83 unit tests plus
a pilot E2E, so this is the gap to close at port time).

---

## 4 · WHAT DATA EXISTS

| Asset | Classification | Disposition |
|---|---|---|
| `catalogo.json` — 12 supplies, 8 treatments, 5 payment methods | **SYNTHETIC** (SKUs/names) | **DO NOT PROMOTE** to canonical product data |
| `catalogo.json` — **spoken aliases** | **DOMAIN VOCABULARY** | **PRESERVE — highest-value data in the contribution** |
| `CONTEO_PREVIO` (all zeros) | **CONFIGURATION** (degenerate placeholder) | Discard; the real prior is the ledger balance |
| The 5 consultation questions | **CONFIGURATION** + declared assumption | Keep the data-not-code shape; replace content when the clinic's form arrives |
| `DISPARADORES`, `PALABRAS_CIERRE`, `SALUDOS` | **DOMAIN VOCABULARY** | Preserve |
| `backend/tests/*` inline catalogs | **TEST FIXTURE** | Stays in the donor repo |

**The catalog is two different things, and the split is the whole point.** The
file's own `_nota` and the README say the SKUs are *"inventado para poder
probar"*. But the aliases are real product knowledge that cannot be derived
from a tariff sheet: `colgate`→pasta, `carpule`/`carpules`→anestesia,
`suctor`→eyector, `braquets`/`cambio de ligas`→ortodoncia, `sacar la muela`→
extracción, `yapeo`/`yapeó`→yape, `bcp`/`interbank`/`bbva`→transferencia,
`izipay`/`pos`→tarjeta.

That vocabulary came from listening to how Peruvian dentists and patients
actually talk. It is the part that must survive.

---

## 5 · WHAT ASSUMPTIONS EXIST

Declared by the author (credit for declaring them):

1. Closed catalog; **the parser never invents a SKU.**
2. **No LLM** in the decision path.
3. **All local** — audio never leaves the machine (Ley 29733, PII).
4. The **5 consultation questions are a stated assumption**, not the clinic's real form.
5. State is **in-memory** and lost on restart — "when Miguel's PostgreSQL arrives, it comes from there".
6. **No authentication** — "a platform decision, not this module's".
7. `whatsapp.py` Graph API shape **written from memory, must be verified**.

Structural, and *not* stated by the author — these are the ones that matter for integration:

8. **No tenancy.** No `organization_id` anywhere. Violates PF1.
9. **No location.** A physical count has no branch. Violates M4.2's truth key.
10. **No actor.** Nothing records who dictated — ironic, since `PETICIONES-A-MIGUEL.md` §3 asks the backend for exactly this.
11. **`anterior` is always 0**, so `diferencia` is currently meaningless in practice.
12. Integer quantities only; Spanish only; alias matching is exact (a transcription variant not in the catalog is silently dropped — a safe failure, but a silent one).
13. **Session ids are `uuid4().hex[:12]`** (48 bits) and `GET /sesion/{id}` is unauthenticated — fine on localhost, not a capability token.

---

## 6 · WHAT CURRENT ODONTOFLOW ALREADY SOLVES

`PETICIONES-A-MIGUEL.md` was written against the **legacy MediStock schema**
(`movimientos_stock`, `001_stock_ledger_trigger.sql`,
`003_sp_register_entrada.sql`). Alejandro's analysis was correct **for that
codebase**. The current FastAPI backend at `23527c2` (migration `0008`) is a
different system, and M4.2 independently solved most of it.

Verified against the live schema and `app/inventory/`, `app/economics/` — not
against docs:

| # | DONOR_NEED | CURRENT_ODONTOFLOW_CAPABILITY | STATUS | ADAPTER_NEEDED |
|---|---|---|---|---|
| 1 | **`AJUSTE` movement type** — a physical count is not a SALIDA | `MOVEMENT_TYPE_CHECK` admits `ADJUSTMENT` alongside `ENTRADA`/`SALIDA`/`TRANSFER_OUT`/`TRANSFER_IN`. `POST /products/{id}/adjustments` exists. | ✅ **SOLVED** | Map count → **delta**: `AdjustmentCreate.quantity` is a signed non-zero *delta*, not an absolute count. The donor already computes `diferencia = contado − anterior` — feed that. |
| 2 | **`motivo` field**, closed vocabulary, mandatory for adjustments | `inventory_movements.reason` exists **and is structurally mandatory** for adjustments: `CHECK ((type <> 'ADJUSTMENT') OR (reason IS NOT NULL AND reason <> ''))`. Schema requires `min_length=1`. | ✅ **SOLVED — stronger than asked** (enforced by the database, not merely present) | **Partial gap:** `reason` is free `String(255)`, **not** the closed enum the donor proposed (`CONTEO`/`MERMA`/`ROBO`/`VENCIMIENTO`/`TRASPASO`/`CORRECCION`). A voice count can pass `"CONTEO"` today, but nothing prevents free text, so reasons will not aggregate. Closing this is a small, separate decision. |
| 3 | **Actor / provenance** on the movement | PF3: every movement command stages an `audit_events` row **in the same transaction**, carrying `actor_id`, `actor_type` and `correlation_id` from the `ExecutionContext`. Plus PF4 `command_receipts` with `principal_id`. | ✅ **SOLVED** — via the audit trail, not a column on the movement | The voice service must act as a real **Principal** with an `ExecutionContext`. It has **no identity today** (assumption 10), so this is the largest structural gap on the donor's side. |
| 4 | **`id_sede`** + a `TRASPASO` movement type | M4.2: `location_id` **NOT NULL on every movement** with a composite FK into `locations(organization_id, id)`; balance derived per `(organization_id, product_id, location_id)`; **transfers are an atomic `TRANSFER_OUT`/`TRANSFER_IN` pair** sharing `transfer_id`, with partial unique indexes and a deferred trigger so a half-pair can never commit. | ✅ **SOLVED — exactly as requested, including the transfer type** | The voice flow has **no notion of branch**. A count must be told *which location*. This is a product question (does the dentist pick a branch, or is it derived?), not a backend gap. |
| 5 | `cantidad_esperada` — store what the system believed, alongside the count | **Does not exist.** No `expected_quantity` column anywhere (verified across `app/` and `alembic/`). | ⚠️ **NOT SOLVED** | Arguably **unnecessary**: the balance is a derived read-time aggregate, so "expected" is computable via `get_balance` at count time. But *computable now* ≠ *recorded then* — the historical expectation is not reconstructible after later movements land. If the clinic's shrinkage analysis needs it, this is a genuine (small) migration. **Do not add it speculatively.** |

Additional donor-facing capabilities already present, which the donor could not
have known about:

| Donor output | Current capability | Status |
|---|---|---|
| `consumo[]` — supplies consumed in the visit | `POST /executions/{id}/consumptions` creates `ServiceConsumption` **and atomically writes the SALIDA movement at the visit's location** (never client-supplied), 1:1 via `id_consumo_origen UNIQUE` | ✅ **SOLVED — direct mapping** |
| `servicios[]` — treatments performed | `ServiceExecution` per visit, with `executed_price` as a point-in-time snapshot; `UNIQUE(org, visit, service)` | ✅ **SOLVED** |
| `total_bruto` — one gross amount for the visit | `Charge` is **1:1 with a ServiceExecution** (`uq_charges_org_execution`) | ⚠️ **MISMATCH — see below** |
| `metodos_pago[]` — several methods | `Payment` is N:1 to a charge with a free `method` string; overpayment deterministically rejected | ✅ **SOLVED** (mixed payment is expressible) |

### The one genuine modelling mismatch

The donor emits **one `total_bruto` for the whole visit**. OdontoFlow charges
**per ServiceExecution, 1:1**. A visit with two treatments therefore needs
**two charges**, and the donor gives a single number with no allocation rule.

This cannot be resolved by an adapter alone — it needs a product decision:
split by `executed_price` proportion, charge one execution and treat the rest as
zero, or ask the dentist per treatment. **Do not guess it in code.** It is the
first question to put to the clinic, and it is cheap to ask.

Also note `Payment.method` is a free `String(50)` with no closed catalog, while
the donor has a proper payment-method vocabulary with aliases. The donor's
vocabulary is **better than ours here** and is worth adopting.

---

## 7 · WHAT SHOULD BE REUSED

In descending order of value per unit of risk:

1. **`parser.py` — reuse nearly verbatim.** 327 lines, stdlib only, 21 tests, zero state, no network. Spanish number words, alias matching, self-correction, amount and payment extraction. Rewriting this would be pure waste, and worse: we would lose the 21 tests that encode the edge cases.
2. **The alias vocabulary from `catalogo.json`.** Re-key onto real `products.id` / `services.id`; keep every alias.
3. **`CONTRATO-API.md` as the integration contract.** It already documents both attachment shapes and the four conversation rules the front must respect. Keep it as the reference rather than re-deriving it.
4. **The five conversation rules** from `conversacion.py` — especially *`listo`/`igual` are text-only commands* (so a dictated "listo" cannot close a count) and *with missing items the inventory does not self-close*. Both are hard-won product judgements.
5. **`flujos.py`'s data-not-code shape** — questions as data so the clinic's real form replaces content without touching the engine.
6. **`auditar.py`'s style** — objective-level assertions ("the self-correction resolves to 4"), not function-level. This is closer to OdontoFlow's own pilot-E2E philosophy than a unit test would be.
7. **The `PARA-ENCHUFAR-WHATSAPP.md` analysis** — the inbound-webhook vs on-premise conflict, three options with costs, and a recommendation (own relay over Cloudflare Tunnel, to avoid explaining a third party to a privacy-sensitive client). That is real product thinking and would have to be redone otherwise.
8. **Frontend: `App.tsx`, `Navbar.tsx`, `types.ts` — port directly.** Canonical has not touched those files since the donor's base; no collisions (verified).

---

## 8 · WHAT SHOULD BE ADAPTED

| Item | Adaptation |
|---|---|
| **Session state** | Replace the in-memory `SESIONES`/`CONTEO_PREVIO` dicts with persistence. `CONTEO_PREVIO` should not exist at all — the prior count is `get_balance(product, location)`. |
| **Identity** | The voice service must act as a real **Principal** with an `ExecutionContext` (PF3) so every write is attributed and permission-checked. This is the single largest structural gap. |
| **Tenancy** | Every voice write needs `organization_id` from the context, never from a body field (PF1/X3). |
| **Location** | A count and a consumption need a `location_id`. Product decision: dentist picks, or derive from the visit. |
| **Writes** | Any voice-originated mutation goes through the **existing** `app/inventory` / `app/economics` services with an `Idempotency-Key` (PF4). The voice service must never write SQL. |
| **`reason` vocabulary** | Adopt the donor's closed enum idea (`CONTEO`/`MERMA`/…) rather than free text, so reasons aggregate. Separate small decision. |
| **`total_bruto` → charges** | Needs the allocation rule (§6). Ask the clinic. |
| **`auditar.py`** | Make the TTS portable, or better: **commit audio fixtures** — removes the TTS dependency entirely and makes the audio assertions deterministic. |
| **`whatsapp.py`** | Verify the Graph API shape against Meta's current docs; add `X-Hub-Signature-256` verification and idempotency by `message.id` (both author-acknowledged gaps). **Preserve the author's honesty notice.** |
| **Frontend `api.ts`** | Gate the voice calls on `VITE_USE_MOCKS` (currently bypassed — a real invariant breach), declare `VITE_VOZ_URL` in `.env.example`, drop the hardcoded localhost fallback. |
| **Frontend page** | Port with its CSS; note the `MediaRecorder` secure-context requirement; write at least one test. |
| **Navbar geometry** | Decide deliberately: squeeze, overflow menu, or nest under an existing route. The author explicitly offered alternatives. |
| **Latency claims** | Re-measure on the target hardware. The donor's 2.2 s/3.6 s are Apple Silicon numbers. |

---

## 9 · WHAT SHOULD NOT BECOME BUSINESS AUTHORITY

Non-negotiable:

1. **`catalogo.json` SKUs, names and the implied price list.** Synthetic by the author's own statement. The real catalog is the clinic's tariff.
2. **`CONTEO_PREVIO` zeros.** A placeholder. `anterior: 0` is not a prior count, and any `diferencia` computed from it today is meaningless.
3. **The voice service's in-memory state.** Never a source of truth for stock, money, or clinical facts. `inventory_movements` is the only stock authority; `charges`/`payments` the only money authority.
4. **The 5 consultation questions.** A declared assumption pending the clinic's real form.
5. **`auditar.py`'s latency numbers.** The author's measurements on other hardware.
6. **The transcription itself.** A transcript is evidence of what was said, not proof of what happened. Voice output is a **proposal** requiring confirmation — which the donor's own design already honours (`"Listo, esto es lo que entendí. Revísalo y confirma."`).
7. **`whatsapp.py`'s Graph API assumptions.** Unverified by the author's own notice.
8. **Nothing in `contrib-odonto-voz/` is built, tested or deployed by any canonical pipeline.** It is a sibling repository, not a submodule.

And the M5 rule stands unchanged: **this contribution supplies no real clinic
data.** `DOMINANT_LEAKAGE` remains `UNKNOWN`. A synthetic catalog and a
prototype's in-memory counts are not a Revenue Leakage Baseline.

---

## 10 · EXACT INTEGRATION ORDER

Each step is independently valuable and independently abandonable. **No step
here is authorized yet** — this is the order, not a go-ahead.

| # | Step | Why first | Cost | Risk |
|---|---|---|---|---|
| **0** | **Ask the clinic two questions**: (a) the real tariff/supply catalog, (b) how one visit's total maps to per-treatment charges. | Both block correctness, neither needs code, and guessing (b) puts wrong money in the ledger. | ~0 | none |
| **1** | **Port the frontend view behind a feature flag, mocks-safe.** `App.tsx`/`Navbar.tsx`/`types.ts` direct; `api.ts` with the `VITE_USE_MOCKS` gate; page + its CSS; one test. | Highest visible value, zero backend risk, nothing writes anything. Makes the work real and reviewable. | low | low — read-only |
| **2** | **Extract `parser.py` + the alias vocabulary as a library**, re-keyed onto real `products.id`/`services.id`, with the donor's 21 tests carried over. | The single most valuable asset. Independent of transport, identity and persistence. | low | low — pure functions |
| **3** | **Make the E2E harness portable** — commit audio fixtures instead of shelling out to `say`. | Until this exists, the audio path is unverified on our platform and every latency claim is someone else's measurement. | low | none |
| **4** | **Give the voice service an identity**: a Principal + `ExecutionContext`, permissions, and `Idempotency-Key` on every command. | The gate for *any* write. Everything downstream depends on it. | medium | medium — touches PF1/PF2/PF3/PF4 |
| **5** | **Wire the inventory count → `ADJUSTMENT`**, passing `diferencia` as the signed delta, `reason="CONTEO"`, and an explicit `location_id`; prior count from `get_balance`, never from `CONTEO_PREVIO`. | The donor's #1 blocker is already solved; this is the first real write and the cheapest to verify against the ledger. | medium | medium — writes stock |
| **6** | **Wire the visit summary → executions/consumptions/charges/payments**, once step 0(b) has answered the allocation question. | Money. Must not move before the mapping rule is a clinic decision. | medium-high | **high — writes money** |
| **7** | **Close the `reason` vocabulary** (`CONTEO`/`MERMA`/`ROBO`/…) so adjustment reasons aggregate. | Small, and makes the shrinkage analysis the owner does by hand actually queryable. | low | low |
| **8** | **WhatsApp**, last. Verify the Graph shape against Meta, add signature verification and `message.id` idempotency, then start the 4 non-code Meta steps (which take days and should be *begun* early even though the code lands last). | Highest external dependency, lowest marginal value until 1–6 work. | high | high — external, unverified |

**Do not reorder 6 before 0(b).** That is the one sequencing error in this list
that would put wrong numbers into the money ledger.

**`cantidad_esperada` (donor request #5) is deliberately absent from this
order.** It is computable today from the derived balance; add it only if the
clinic's shrinkage analysis proves it needs the historical expectation
recorded. Do not add it speculatively.

---

## 11 · What this map does not claim

- It does not claim the audio path works on our platform — **unverified**.
- It does not claim the WhatsApp adapter works — unverified by its own author.
- It does not treat the synthetic catalog as clinic data, or the prototype's counts as stock truth.
- It does not authorize any step in §10.
- It changed no product code, and no donor file.
