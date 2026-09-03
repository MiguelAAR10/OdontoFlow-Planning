---
title: odonto-voz — read-only component inventory
status: evidence
date: 2026-09-02
source_repo: https://github.com/AlejandroMarceloCh/odonto-voz
source_head: eb9a4ee0381972658fb8a9e717d4e056820d3d4e
author: Alejandro Jesus Marcelo CH (AlejandroMarceloCh)
local_path: ~/projects/portfolio/AI-EdgeRunners/odontoflow/contrib-odonto-voz
authority: CONTRIBUTOR SOURCE — NOT canonical business authority
---

# odonto-voz — component inventory

Read-only inspection. **No donor file was modified.** The only writes inside the
donor clone were `backend/.venv/` (git-ignored by the donor's own `.gitignore`)
and the Whisper `tiny` model cache, both required to run its documented baseline.

Repository: 5 commits, one branch (`main`), no tags, 19 files, 2 219 lines.

---

## 1. What it is

A standalone FastAPI service in which a dentist dictates by voice and the system
fills two things done by hand today:

- **Inventory audit** — free dictation while walking the shelf; the system reports what was missed.
- **Visit summary** — five guided questions producing patient, treatments, supplies consumed and the charge.

It is a **sibling service**, not a library: it owns its own process, port (8000)
and dependency tree. It never writes to a database. It emits JSON and expects
the business backend to persist it.

---

## 2. Components

### `backend/app/parser.py` — 327 L · the highest-value asset

| | |
|---|---|
| **Purpose** | Spoken Spanish → structured items. Number words, catalog aliases, amounts, payment methods. |
| **Inputs** | raw text, `Catalogo`, target families |
| **Outputs** | `ItemDetectado(codigo, nombre, familia, cantidad, confianza, fragmento)`, `list[int]` amounts, `list[str]` payment codes |
| **State ownership** | none — pure functions |
| **Dependencies** | stdlib only (`re`, `unicodedata`, `collections`, `dataclasses`) |
| **Tests** | 21 in `test_parser.py`, all passing |
| **Security** | no I/O, no network, no eval. Safe by construction. |

**Assumptions, declared in-code:**
- Quantity precedes the noun in Spanish (`"doce pastas"`), searched backwards over a 4-token window skipping filler words.
- A number-run splits into several numbers when a term is ≥ the previous one — `"veintiséis y veintisiete"` is two numbers (dental pieces), not 53.
- Self-correction: the **last mention with a quantity wins** (`"tres, no, cuatro resinas"` → 4), but a mention *without* a quantity never overwrites one that had it.
- One number can never be assigned to two products (`consumidos` set).
- Amounts count only when adjacent to `soles`/`sol`/`s`.

**Deliberate design decision (documented, and correct):** *no LLM.* The module
header cites OdontoFlow's own invariant — *"LLMs never set prices, durations,
slots or bookings"* — and argues a hallucinated quantity produces a real
inventory discrepancy, whereas a rule failure is fixed by adding an alias.

**Known limitations:** exact alias matching only (no fuzzy/phonetic), so a
transcription variant not in the catalog is silently dropped rather than
mis-assigned — a safe failure, but a silent one. Integer quantities only (no
`2.5 ml`). Spanish-only.

**Integration value: VERY HIGH.** Stdlib-only, fully tested, no state, no
network. It is the piece most worth reusing verbatim.

### `backend/app/conversacion.py` — 317 L

| | |
|---|---|
| **Purpose** | The two-flow state machine. **Channel-agnostic by design.** |
| **Inputs** | `(Sesion, Entrada, Catalogo, previo)` |
| **Outputs** | `list[Mensaje]` — only the turn's *new* messages; business JSON in `Mensaje.adjunto` |
| **State ownership** | `Sesion` (id, flujo, paso, datos, conteo, mensajes, terminado) — **caller-held, in-memory** |
| **Dependencies** | `flujos`, `parser`. No FastAPI, no DB, no network. |
| **Tests** | 19 in `test_conversacion.py`, all passing |
| **Security** | no I/O. Session ids are `uuid4().hex[:12]` — 48 bits, fine for a local prototype, **not** an unguessable capability token. |

`procesar()` is the single entry point for browser, WhatsApp and tests alike.
This is what makes WhatsApp an adapter rather than a redesign.

**Business rules encoded (and verified end-to-end):**
1. `listo` / `igual` are **text-only commands** — ignored when `es_audio=True`, so a dictated "listo" cannot accidentally close the count.
2. With missing items the inventory **does not self-close** (`terminado: false`); it names what was missed and offers to complete.
3. Several audios accumulate; **the last value dictated overwrites** — that is how correcting yourself works.
4. One session = one flow; changing flow requires restart.
5. `editar_campo()` re-runs corrected text **through the same parser**, so typing and dictating produce identical data. Raw uninterpreted text is never stored.

**Integration value: HIGH** for the flow logic and those five rules; the
in-memory `Sesion` must be replaced by persistence before production.

### `backend/app/flujos.py` — 107 L

Questions and triggers **as data, not code** — explicitly so the clinic's real
template can replace them without touching the engine. Contains the **declared
assumption** that the 5 consultation questions come from a meeting description,
*not* from the clinic's real form.

`PALABRAS_CIERRE`, `DISPARADORES`, `SALUDOS`, `POR_NUMERO` (1/2 menu) are
domain vocabulary. **Integration value: HIGH as vocabulary**, and the
data-not-code shape is the right pattern to keep.

### `backend/app/transcriptor.py` — 96 L

| | |
|---|---|
| **Purpose** | Local transcription via faster-whisper |
| **Inputs** | audio path (any ffmpeg-readable format), `Catalogo` |
| **Outputs** | `Transcripcion(texto, segundos_audio, segundos_proceso, modelo)` |
| **State ownership** | module-level `_modelo` singleton behind a `threading.Lock` |
| **Dependencies** | **`faster-whisper`, `ctranslate2`, and an `ffmpeg` binary on PATH** |
| **Tests** | none directly — no test touches audio |
| **Security** | **strong privacy posture**: audio never leaves the machine, justified by Peru's Ley 29733 (PII: patient names, diagnoses). No route to any transcription API. Uses `subprocess.run` with an argument **list** (no shell), so the ffmpeg call is not injectable. |

Measured by the author: `small`, CPU, Apple Silicon, 7 real audios — **2.2 s mean, 3.6 s worst**. Model configurable via `ODONTO_MODELO`.

The domain prompt is **built from the catalog**, not hand-written, so it cannot drift when a product is added.

**Known limitations:** first boot downloads ~500 MB (`small`); loaded in a
background thread at startup so the first audio of the day is not slowed. CPU
`int8` only. No timeout on transcription.

**Integration value: MEDIUM-HIGH** — the privacy stance and the
catalog-derived prompt are the reusable ideas; the dependency weight is real.

### `backend/app/main.py` — 179 L

FastAPI surface: `GET /salud`, `GET /catalogo`, `POST /mensaje`, `POST /audio`,
`POST /sesion/{id}/campo`, `GET /sesion/{id}`, `POST /sesion/{id}/reiniciar`.
CORS open to `:5173` only.

**State ownership — the key limitation:** module-level `SESIONES: dict` and
`CONTEO_PREVIO: dict`, both **in-memory and lost on restart**, acknowledged in a
code comment as a prototype decision to be replaced by PostgreSQL.

`CONTEO_PREVIO` is initialized to **0 for every supply**, so `anterior` is a
placeholder, not a real prior count.

**Security characteristics — must be stated plainly:** **no authentication, no
authorization, no rate limit, no request size limit on the audio upload.**
Any client reaching the port has full use of it, and can read any session by id
via `GET /sesion/{id}`. The author documents this as "a platform decision, not
this module's". Uploaded files are written to `tempfile.mkdtemp()` using the
client-supplied `archivo.filename` — a path-traversal surface worth reviewing
before this is ever exposed beyond localhost.

**Tests** 9 in `test_api.py`, all passing (TestClient, no audio, no network).

**Integration value: MEDIUM** — the endpoint shape and the response envelope
are good; the transport must be re-hosted under OdontoFlow's tenancy,
permissions and idempotency before it can write anything.

### `backend/app/whatsapp.py` — 118 L · **written, deliberately disabled**

WhatsApp Cloud API adapter: webhook verification (challenge), two-hop signed
media download, transcription, `procesar()`, reply. Not wired into `main.py`;
activation is two lines plus four env vars.

**The author's own honesty notice is in the file header** and must be preserved:
the Graph API payload field names (`entry[0].changes[0].value.messages[]`,
`audio.id`) and routes were **written from memory** and must be checked against
Meta's current docs before being trusted.

**Security gaps, author-acknowledged:** **no `X-Hub-Signature-256` verification**
on the inbound webhook (so a forged POST would be processed), and **no
idempotency by `message.id`** — Meta retries when it does not get a fast 200,
which would double-process a dictation. The phone number *is* the session key
(`SESIONES_WA[telefono]`), so anyone spoofing a payload could read/steer
another doctor's session.

**Tests** none. **Integration value: MEDIUM as a design** (the channel-agnostic
proof), **LOW as code** until verified against Meta and hardened.

### `auditar.py` — 207 L (repo root)

An objective-level end-to-end harness: drives both flows against a **real
running server with real generated audio** and asserts business outcomes —
that `"tres, no, cuatro"` resolves to 4, that the inventory names what was
missed and accepts `igual`, that the consultation returns correct amounts,
payments, supplies and treatments. Exits 1 on failure, for CI. Also asserts a
latency bound (worst < 15 s).

**Hard dependency: macOS.** Line 42 shells out to `say -v Paulina` to synthesize
the audio. See §4.

**Integration value: HIGH as intent** — this is the right *shape* of test
(verify the objective, not the functions); the TTS step must be made portable.

### `backend/datos/catalogo.json` — 37 L

See §5 (data inventory).

### Documentation — 359 L across 4 files

| File | Content | Value |
|---|---|---|
| `README.md` (99 L) | setup, measured latency, architecture, and an explicit "what it does not do yet" | HIGH |
| `CONTRATO-API.md` (122 L) | full endpoint + response contract, both attachment shapes, and 4 conversation rules the front must respect | **HIGH — this is the integration contract** |
| `PETICIONES-A-MIGUEL.md` (62 L) | 4 reasoned requests to the business backend | HIGH — see the compatibility map |
| `PARA-ENCHUFAR-WHATSAPP.md` (76 L) | the 4 non-code steps, and a real analysis of the inbound-webhook vs on-premise conflict with a recommendation (own relay over Cloudflare Tunnel) | HIGH — genuine product thinking |

Documentation quality is unusually high: assumptions are declared, limitations
are volunteered rather than hidden, and trade-offs carry their reasoning.

---

## 3. Test baseline — measured 2026-09-02

Run in the donor's own environment, exactly as its README documents.

| | |
|---|---|
| **Python** | 3.12.3 (donor README requires 3.10+) |
| **Install** | `pip install -r requirements.txt` — **clean, exit 0**, no dependency conflict |
| **Resolved versions** | fastapi 0.141.1 · uvicorn 0.52.3 · python-multipart 0.0.32 · httpx 0.28.1 · faster-whisper 1.2.1 · ctranslate2 4.8.1 · pytest 9.1.1 (all pinned exactly as declared) |
| **Command** | `.venv/bin/python -m pytest tests/ -q` |
| **Result** | **54 passed, 0 failed** |
| **Runtime** | **0.69 s** (wall 1.31 s) |
| **Warnings** | 2, both third-party deprecations (`starlette.testclient` + `anyio.abc.BlockingPortal`) — not donor defects |

The README claims 45 tests; the actual count at HEAD is **54**. The doc is
stale in the donor's favour, not against it.

Raw output: `donor-pytest-raw.txt`.

**No test touches audio or network**, as documented — which is why the suite
runs in under a second and needed no model download.

### Additional verification performed here (beyond the donor's suite)

Both flows driven **end-to-end over real HTTP** against a booted donor server
(`ODONTO_MODELO=tiny`), text channel. Raw output: `donor-http-textflow.txt`.

- Consultation: 5 questions traversed; business JSON correct — `total_bruto: 120`, `metodos_pago: ["yape"]`, `consumo: {ANESTESIA: 2, AGUJA: 4}`, `servicios: {RESINA-SIMPLE: 2, PROFILAXIS: 1}`, `paciente_ref: "Juan Perez"`.
- Inventory: accumulation across turns, **self-correction `"tres, no, cuatro"` → `RESINA = 4`**, missing items named at `listo`, `igual` closing all 12 of 12 without overwriting dictated values (`PASTA-DENTAL = 12`).

This confirms the parser and the state machine work over the real transport,
not only in unit tests.

---

## 4. Environment requirements — stated, not hidden

| Requirement | Status here | Consequence |
|---|---|---|
| Python 3.10+ | ✅ 3.12.3 | — |
| `ffmpeg` on PATH | ✅ 6.1.1 | — |
| Whisper model download (~500 MB for `small`) | ⚠️ not downloaded; ran `tiny` instead | **First boot on any new machine pays this once.** Not a defect; a deployment fact. |
| **macOS `say`** (for `auditar.py`) | ❌ **absent — macOS-only** | **`auditar.py` CANNOT run on Linux/WSL.** |
| No TTS alternative | ❌ no `espeak`/`espeak-ng`/`pico2wave`/`festival`/`flite` installed | The audio path could not be exercised locally at all. |

### `auditar.py` attempt — recorded honestly

Attempted against the booted server. Raw output: `donor-auditar-raw.txt`.

The first two **text** checks **PASSED**:
- ✓ El saludo ofrece los dos flujos
- ✓ Elige inventario con lenguaje natural

It then died at the first audio step:

```
File "auditar.py", line 42, in decir
    subprocess.run(["say", "-v", "Paulina", "-o", str(aiff), texto], ...)
FileNotFoundError: [Errno 2] No such file or directory: 'say'
```

**Verdict: `auditar.py` is NOT BROKEN — it is platform-bound.** Its logic is
sound and its first checks pass; it assumes the macOS TTS the author developed
on. Per instruction, **no repair was attempted.**

**Consequence to carry forward:** the transcription path
(`transcriptor.py`, `POST /audio`) is **UNVERIFIED on Linux**. The donor's
latency numbers (2.2 s mean / 3.6 s worst) are the author's measurements on
Apple Silicon and must be **re-measured on the target machine** before being
quoted as ours. Making the harness portable (any TTS, or committed audio
fixtures) is the smallest fix that unlocks this — and committed fixtures would
be strictly better, since they remove the TTS dependency and make the audio
assertions deterministic.

---

## 5. Data assets

| Asset | Classification | Notes |
|---|---|---|
| `backend/datos/catalogo.json` — 12 supplies, 8 treatments, 5 payment methods | **SYNTHETIC** + **DOMAIN VOCABULARY** | See below — the split matters. |
| `CONTEO_PREVIO` (`main.py:32`) | **CONFIGURATION** (degenerate) | All zeros. `anterior` is a placeholder, never a real prior count. |
| `backend/tests/*` fixtures | **TEST FIXTURE** | Inline catalogs inside the test files. |
| `FLUJOS` / `CONSULTA` questions (`flujos.py`) | **CONFIGURATION** + declared assumption | Author states these are **not** the clinic's real template. |
| `DISPARADORES`, `PALABRAS_CIERRE`, `SALUDOS` | **DOMAIN VOCABULARY** | How a Peruvian dentist actually speaks. |

### The catalog is two different things and must be split

The **SKUs, names and prices side is synthetic** — the file's own `_nota` and
the README say so: *"El catálogo actual es **inventado** para poder probar. El
bueno sale del tarifario de la clínica."*

The **aliases are real product knowledge** and are the most valuable data in the
contribution: `colgate` → PASTA-DENTAL, `carpule`/`carpules` → ANESTESIA,
`suctor` → EYECTOR, `braquets`/`brackets`/`cambio de ligas` → ORTO-CONTROL,
`sacar la muela`/`exodoncia` → EXTRACCION, `yapeo`/`yapeó` → yape,
`bcp`/`interbank`/`bbva`/`scotiabank` → transferencia, `izipay`/`pos` → tarjeta.

These are Peruvian clinical and payment colloquialisms that cannot be derived
from a tariff sheet — they come from listening to how people talk. The README
is right that *"the precision is won in `catalogo.json`, not in the model."*

**Rule: the synthetic SKU list must NOT be promoted into canonical product
data. The alias vocabulary must be preserved and carried across, re-keyed onto
real `products.id` / `services.id`.**

---

## 6. Cross-cutting assumptions

1. **A closed catalog; the parser never invents a SKU.** Correct and load-bearing.
2. **No LLM in the decision path.** Aligns with OdontoFlow's own invariant.
3. **All local; audio never leaves the machine** (Ley 29733). A deliberate privacy stance to preserve.
4. **Single tenant.** No organization anywhere — no `organization_id`, no notion of a clinic. Structural gap vs OdontoFlow's PF1.
5. **Single location.** No `location_id`; a physical count has no branch. Structural gap vs M4.2.
6. **No actor.** Nothing records who dictated. Ironic, since `PETICIONES-A-MIGUEL.md` §3 asks the business backend for exactly this.
7. **In-memory state**, author-acknowledged.
8. **No authentication**, author-acknowledged as a platform decision.
9. **Integer quantities only.**
10. **`anterior` is always 0**, so `diferencia` is currently meaningless in practice — the real prior must come from the ledger balance.

---

## 7. Integration value summary

| Component | Value | Verdict |
|---|---|---|
| `parser.py` | **VERY HIGH** | Reuse nearly verbatim. Stdlib-only, 21 tests, no state. |
| `catalogo.json` **aliases** | **VERY HIGH** | Preserve as vocabulary; re-key to real ids. |
| `CONTRATO-API.md` | **HIGH** | The integration contract; keep as the reference. |
| `conversacion.py` flow rules | **HIGH** | Reuse the 5 rules; replace in-memory `Sesion`. |
| `flujos.py` data-not-code shape | **HIGH** | Keep the pattern and the vocabulary. |
| `auditar.py` intent | **HIGH** | Keep the objective-level style; make the TTS portable. |
| `transcriptor.py` | **MEDIUM-HIGH** | Privacy stance + catalog-derived prompt are the ideas; weigh the dependency. |
| `PARA-ENCHUFAR-WHATSAPP.md` analysis | **MEDIUM-HIGH** | Real product thinking on the on-premise/webhook conflict. |
| `main.py` transport | **MEDIUM** | Re-host under tenancy/permissions/idempotency. |
| `whatsapp.py` code | **LOW until verified** | Unverified against Meta; missing signature check and idempotency. |
| `catalogo.json` **SKUs** | **DO NOT PROMOTE** | Synthetic by the author's own statement. |
| `CONTEO_PREVIO` zeros | **DO NOT PROMOTE** | Placeholder, not data. |

---

## 8. What this inventory does not claim

- It does not claim the audio/transcription path works on Linux — that is **unverified** here.
- It does not claim the WhatsApp adapter works — the author says it is unverified, and nothing here tested it.
- It does not treat the synthetic catalog as clinic data.
- It does not treat the author's latency measurements as ours.
- It did not modify, fix, or reformat any donor file.
