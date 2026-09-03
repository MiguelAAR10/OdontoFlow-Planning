# Voice Integration V1 — FOREMAN living brief

> Written for the Architect. Self-contained: readable without opening the code.
> Raw evidence lives elsewhere and is linked, never pasted here.
>
> **Written retroactively.** The activity was executed before this brief
> existed — see the honesty note in the Decision log.

## Executive status

**Phase:** V1 complete. **Verdict: PASS.** No active gate on engineering.

Alejandro Marcelo's voice assistant is now part of OdontoFlow: his service is a
canonical repo with his authorship and all five of his commits intact, and his
UI is live behind an off-by-default feature flag. V1 is transport and interface
only — the assistant produces **drafts a human confirms**, and writes nothing
to the business.

**The exact Owner decision needed next** is not technical. Two questions belong
to the clinic, and one belongs to you:

1. **Clinic:** the real tariff / supply catalog. Today's catalog is synthetic.
2. **Clinic:** how one visit's total becomes charges. A `Charge` is 1:1 with a
   performed service, so a two-treatment visit needs two charges — and the
   assistant reports a single total. Splitting it proportionally, charging one
   line, or asking per treatment each produce *different money*. I refused to
   guess. **Nothing writes money until this is answered.**
3. **Owner:** the voice repository was created **private**. Visibility was not
   specified and publishing cannot be undone. One command flips it.

## Objective and success criteria

**Objective.** Bring the contributed voice work into the product without losing
authorship, history, tests, data or design intent — and without moving any
business authority into the voice service.

**Constraints set by the brief, and honoured:**

- Promote the existing donor clone; **never** copy files into a fresh repo.
- Never squash, rewrite, or force-push donor commits.
- Port the UI **intentionally**; do not merge, cherry-pick or rebase the donor branch.
- No business writes in V1.
- Keep the donor catalog intact and marked synthetic.
- Do not break the existing real-mode guarantees.
- Do not re-run the backend suite: the backend is unchanged.
- Do not fake an audio pass.

**Acceptance criteria — all verifiable, all met:**

| Criterion | Result |
|---|---|
| Voice repo promoted, donor HEAD unchanged | `eb9a4ee` — exact match after the move |
| All donor commits preserved and attributed | 5 of 5, authored by Alejandro Marcelo, verified on the remote |
| UI ported, donor branch untouched | canonical `a967b24`; donor ref still `c0f418d`, **not an ancestor of main** |
| Mock mode never contacts the service | zero requests, proven with the service *live and healthy* |
| Voice disabled never contacts the service | zero requests; route unregistered |
| Existing guarantees intact | pilot E2E **12/12** on a fresh database |
| No business writes | backend untouched at `23527c2`, clean |
| Audio honestly reported | **UNVERIFIED**, not claimed |

## Repository reality

Four repos in the canonical workspace; **Repo 0** (`odontoflow-planning`) is the
control plane and the only status authority.

**What already existed and was reused rather than rebuilt:**

- A frontend that had moved **7 commits and 36 files** beyond the donor's base,
  including a `contracts/` + `domain/` layer the donor never saw. Its
  `src/api.ts` is still the single façade every page imports through — so the
  contribution's instinct to add there was architecturally right.
- A design system (`Badge`, `DataTable`, `Button`) the donor already reused
  instead of inventing parallel components. Both APIs were still compatible.
- A node-based pilot E2E harness that proves the real-mode journey end to end.
- An inventory ledger that **already answers three of the four requests** the
  donor wrote to the backend — his `PETICIONES-A-MIGUEL.md` was written against
  the *legacy MediStock* schema, so his analysis was correct for the codebase he
  had, and obsolete for ours. Verified against the live schema, not the docs.

**Protected surfaces, untouched:** the backend (`23527c2`), MediStock (legacy,
read-only), and the donor's own files inside the voice repo — zero tracked
modifications there.

**Two pre-existing conditions found, neither introduced here, neither fixed:**

- **The backend declares no CORS.** A browser calling it from the SPA's origin
  is blocked, while the same request from a terminal succeeds. This is *why*
  the pilot E2E is a node harness, and it means the SPA has never been driven
  in a browser against the real backend. Out of V1's scope; recorded so it is
  not rediscovered as a mystery later.
- The pilot harness script assumes a log directory that may not exist and dies
  if it is missing. Worth one line to make it self-sufficient.

## Authority and evidence used

- **Repo 0** for milestone state, environment and prior decisions — read before
  touching anything, per the workspace's own ordering rule (Repo 0 outranks
  product READMEs on status; **git outranks Repo 0** on heads; the **live
  database schema outranks the models** on what is actually enforced).
- **The contributor's own documents** as the integration contract — his
  `CONTRATO-API.md`, README, and the two analysis documents. They were accurate
  and unusually honest about their own limits; I did not re-derive what they
  already settled.
- **The prior activity's map** (`VOICE_CONTRIBUTION_INTEGRATION_MAP.md`) for the
  per-file port classification, so V1 executed a decision already recorded
  rather than re-litigating it.

**Originality boundary, stated plainly:** the voice service and the assistant
view are **not my work**. The parser, the conversation engine, the flows, the
transcription layer, the catalog vocabulary, the API contract and the view are
Alejandro Marcelo's. The frontend they land on is Leonardo Panduro's. My
contribution to V1 is the promotion mechanics, the feature gate, three scoped
adaptations, the tests that prove the gate, and this record.

## What we will build and how

**Approach: a sibling service, not a library.** The voice assistant keeps its
own process, port and dependency tree. Nothing about it is compiled into the
backend or the frontend. That was the contributor's design and it is the right
one — it keeps a heavy, model-dependent component from becoming a hard
dependency of the product.

**Three adaptations, and the reasoning for each:**

1. **A structural feature gate.** The contribution's one real defect was that
   its calls were not gated on demo mode, so a demo build would still reach out
   to a live service — breaking a guarantee the pilot E2E depends on. The gate
   is now **AND, not OR**: the feature must be switched on *and* demo mode must
   be off. It refuses *before* the network layer is reachable, so the isolation
   is structural rather than a matter of discipline. Understandable omission —
   he branched before that convention tightened.

2. **His navigation fix, scoped instead of global.** He tightened every
   navigation item to fit a seventh, measured at two viewport widths. Since the
   feature is now opt-in, applying that globally would degrade the default
   layout for everyone. I kept **his numbers** and applied them only when the
   feature is on. He explicitly offered alternatives in his pull request; that
   design decision remains open and is yours, not mine.

3. **Draft labelling.** Every summary is marked as a draft, reinforcing what his
   own design already did by ending with *"review it and confirm"*. This is the
   visible expression of the no-business-writes rule.

**Deliberately not implemented in V1** — each is a real gap, none is a defect:

- No persistence: sessions live in memory and are lost on restart.
- No identity: the service is not yet a principal, so it *cannot* be permitted
  to write anything even if we wanted it to. This is the gate for every future
  write, and it is the largest structural gap on the contributor's side.
- No location awareness: a physical count does not yet know which branch it is.
- The WhatsApp channel: written by the contributor, deliberately disabled, and
  unverified against the provider by his own admission.

## Execution model

**Solo.** The parallelism bar was not met and it is worth saying why, since the
brief invited orchestration in earlier activities.

The work was a dependency chain, not a fan-out: promote the repo → verify the
baseline → port the UI → gate it → test the gate → drive it in a browser. Each
step's input was the previous step's output, and the files contended constantly.
There were no competing approaches worth comparing before committing. Spawning
workers would have added coordination cost and token spend for no wall-clock
saving and no better decision.

One honest caveat: two earlier activities in this stream specified an external
model for read-only inventory panes. That model was **not available in this
environment**, so those panes were executed directly rather than by the
specified subcontractor. The analysis stands on its evidence, but it is *not*
the independent second opinion the pane design intended. If you want that
independence, it has to be commissioned separately.

## Risks, conflicts, and protected surfaces

| Risk | Standing |
|---|---|
| **The audio path is unproven here** | The dictation path — the actual point of the product — has never run on this platform. Text works end to end; audio is untested because no speech-synthesis tooling exists here to drive it and headless browsers have no microphone. **The contributor's latency figures are his, measured on his hardware, and must not be quoted as ours.** |
| **A synthetic catalog could leak into real data** | Contained by rule and by documentation, not by code. The catalog's product codes and prices are invented **by the author's own statement**; only its spoken vocabulary is real knowledge. Nothing enforces this at runtime yet — V2 is where it becomes configuration. |
| **The service has no authentication** | Acknowledged by the contributor as a platform decision. Acceptable while it is local and writes nothing; **not** acceptable the moment it is reachable or allowed to write. |
| **A visit total cannot be split into charges** | Open, and deliberately unresolved. Guessing would put wrong numbers in the money ledger. |
| **Provenance erosion over time** | The real long-term risk. Ports get refactored and authorship quietly evaporates. Countered by an integration ledger that requires naming the source commit on every future reuse, and by a rule that the contributor's assets are not refactored for style. |

**Must remain untouched:** the backend; MediStock; the donor's files and commit
history in the voice repo; the donor's frontend branch; and the contributor's
own honesty notice about the unverified provider integration.

## Evidence and validation

**Automated, all green:**

- The contributor's own suite, unmodified: **54 tests pass** in under a second.
- Frontend: type checking clean, **91 unit tests** pass (the 83 that existed plus 8 new ones proving the gate), production build passes.
- The existing real-mode journey: **12 of 12** on a freshly reset database — the same result as before this work.
- The backend was deliberately **not** re-run. It is unchanged, so re-running it would prove nothing.

**Driven by hand in a real browser**, with the service live: the route loads and
reports itself connected; the text flow works; the inventory draft fills in
live and the contributor's self-correction handling resolves correctly; closing
with items missing does **not** silently finish — it names what was missed and
offers to carry the previous values, and doing so does not overwrite anything
dictated; the consultation draft comes out correct; correcting a field by hand
re-interprets it through the same rules as speech rather than storing raw text;
restart clears cleanly; and with the service killed the page degrades to a
plain "no connection" state while the rest of the application stays usable.

**The isolation test, done the meaningful way:** with the service **running and
healthy**, demo mode produced **zero** contact with it — and with the feature
switched off, the route was not even registered and the navigation entry was
absent. Anything weaker than "service alive and still not contacted" would not
have been a real test.

**Known limitations, stated rather than buried:**

- **Audio: unverified.** Not a pass, not claimed as one.
- The provider channel: unverified, by its author's own notice.
- The microphone requires a secure context, so on a plain-HTTP LAN address it
  will silently not work. Text input remains, which is why the contributor kept
  it beside the microphone.

Evidence paths: `odontoflow-frontend/.audit/voice-v1/voice-ui-port.md` ·
`odontoflow-voice/CANONICAL.md` ·
`odontoflow-planning/.audit/contributions/voice/` ·
`_preservation/odontoflow-contributors-2026-09-02/` (bundles, patches,
checksums — all verified).

## Decision and progress log

| Date | Entry |
|---|---|
| 2026-09-02 | **Prior activity closed:** contributor intake PASS. Both donor sources preserved with verified checksums and fully mapped; nothing integrated. Primary document: `VOICE_CONTRIBUTION_INTEGRATION_MAP.md`. |
| 2026-09-02 | Voice service **promoted by moving the existing clone**, never by copying files — copying would have destroyed five commits of authorship. History, head and integrity all verified afterwards. |
| 2026-09-02 | Canonical repository created **private**. Visibility was unspecified; publishing is irreversible and private→public is one command. **Escalated to the Owner rather than assumed.** |
| 2026-09-02 | Discovered the command-line tool was authenticated as the **wrong account**, which had been silently producing false "this does not exist" answers. Re-verified through a different channel, corrected, and restored the original account afterwards. |
| 2026-09-02 | Baseline re-verified **after** promotion and **before** any change: 54 tests pass. No stylistic refactor of the contributor's core modules, per the brief. |
| 2026-09-02 | UI ported with three adaptations (gate, scoped navigation fix, draft labelling). Donor branch left unmerged and intact. Commit credits the contributor as co-author. |
| 2026-09-02 | **Three of four of the contributor's backend requests were already solved** by earlier work; the fourth was judged not worth a speculative schema change. Old blockers verified against the live schema instead of assumed still open. |
| 2026-09-02 | **Charge allocation refused, not guessed.** Escalated to the clinic as a business decision. |
| 2026-09-02 | **Audio reported UNVERIFIED.** Two independent blockers, both environmental. Not faked. |
| 2026-09-02 | Backend's missing cross-origin configuration found and **left unfixed** — pre-existing, out of scope, recorded. |
| 2026-09-02 | **Honesty note on this brief.** The three activities in this stream arrived as Architect-shaped briefs — structured objectives and criteria, written without repository access, with a fixed return contract — but were not labelled as such, and I treated them as direct Owner requests. I recorded decisions and evidence properly, but produced **no single consolidated brief** for V1; its story was spread across five files, which is precisely what this protocol exists to prevent. The Owner caught it. This document closes that gap. The two earlier activities already have self-contained primary documents (`M5_REVENUE_LEAKAGE_BASELINE.md`, `VOICE_CONTRIBUTION_INTEGRATION_MAP.md`) and are **reused, not duplicated**. |

## Next approval / next step

**Next activity: V2 — Synthetic Clinic Configuration.** Turn the contributor's
preserved spoken vocabulary into editable configuration, so the synthetic
catalog stops being a hard-coded file — without ever promoting its invented
product codes into real clinic data.

**Nothing further happens on writes until the Owner returns two answers from the
clinic** (the real catalog, and how a visit total becomes charges) and one of
their own (repository visibility).

**Unchanged by this activity, and worth restating because it is the thing most
easily lost:** this contribution supplies **no real clinic data**. The M5
question of where the business actually loses money remains **unanswered**, and
still needs the 90-day clinic export specified in
`M5_REVENUE_LEAKAGE_BASELINE.md`. A working voice assistant is not evidence
about revenue.
