# HARNESS-ENTRY-01 — planning entry-point repair — FOREMAN living brief

Date: 2026-09-17 · Operator: Claude Opus 5 (FOREMAN) · Mode: harness repair
Repos touched: `odontoflow-planning`, `odontoflow-backend` (instruction loader
only — **no product code, no migration, no test, no deployment, no push**)

## Executive status

**DONE and verified.** The planning entry point now loads its own harness and
routes on an enumerated lifecycle state. 42/42 scenario proofs pass, and the
before/after was measured with real Claude sessions, not asserted.

One change was **deliberately not made**: `odontoflow-frontend/CLAUDE.md`. That
repo is a declared protected surface and is heavily dirty. See *Blocked*.

Consolidated as two bounded commits — planning and backend separately. Nothing
was pushed, merged or reset. No activity was started, and no writer ever ran.

## Verified root cause

The harness was not broken in its design. **It was never loaded.**

Claude Code reads `CLAUDE.md`. It does **not** read `AGENTS.md`. All three
OdontoFlow repositories carried their contract only in `AGENTS.md`, and none had
a `CLAUDE.md`. So every rule — the current-activity pointer, activity
classification, model routing, the skill allowlist, one-writer, the stop
conditions — was invisible to the operator at session start. The operator began
every session blind and improvised, which is exactly what the symptoms looked
like.

Measured, not assumed. A real headless Claude session started in
`odontoflow-planning` **before** the change was asked to list the instruction
files in its context. It returned exactly one:

```
/home/miguel/.claude/rules/context7.md
AGENTS.md NOT LOADED
```

That is the whole root cause. Three consequences followed from it:

1. **No lifecycle state existed to route on.** `orchestration/current-activity.yaml`
   carried only a free-text `status:` string. The token `READY_TO_BUILD` did not
   occur anywhere in the repository; neither did `NEEDS_SPEC`, `IN_PROGRESS`, or
   `APPROVED`. The vocabulary in use was `PASS` / `DONE` / `BLOCKED` /
   `NOT_STARTED` — which is precisely the PASS-vs-DONE conflation the brief
   names. There was no state meaning *"validated and authorized, now build"*.
2. **The live evidence of that failure is in the repo.** CORE-01 was validated
   earlier the same day: `docs/handoffs/plans/2026-09-17-core-01-validation.md`
   returns **PASS with bounded contract amendments**, declares the plan
   implementation-ready, lists the write surface and test plan — and ends *"No
   implementation writer was dispatched."* The session wrote the report and
   stopped. Meanwhile `current-activity.yaml` still pointed at the finished
   PROJECT-PUBLISH-01 and had never registered CORE-01 at all. Validated work
   was invisible to the control plane.
3. **The harness routed to a skill that cannot run.** `grill-me` is set to
   `"off"` in `~/.claude/settings.json` (all 99 `skillOverrides` entries are
   `off`). Per the Claude Code contract, `off` means Claude cannot see the skill
   at all. Routing product discovery to `grill-me` was routing into a void.
   This also resolves open question #2 in `TCADD_REPO_HARNESS.md` §34, which had
   it as UNKNOWN.

`TCADD_REPO_HARNESS.md` itself is a 44 KB *forensic extraction* — an accurate
description of the harness, untracked, and loaded by nothing. It documents the
system; it does not run it.

## Canonical files changed, and why

Modify-existing-first. No new framework, no duplicate YAML, no template tree, no
mandatory skill collection.

| File | New? | Why |
|---|---|---|
| `odontoflow-planning/CLAUDE.md` | new | The one file Claude Code actually auto-loads. It `@AGENTS.md`-imports the existing canonical prose rather than copying it, then adds the routing gate: read `lifecycle_state`, branch, dispatch. ~110 lines. This single file is the repair. |
| `odontoflow-planning/orchestration/current-activity.yaml` | modified | The canonical Analysis artifact. Added `lifecycle_contract` (the 9 enumerated states + 4 rules), `lifecycle_state`, `implementation_authorized`, and a `validation:` block separate from state. Added `next_activity_candidate` registering CORE-01's verified reality as **awaiting owner authorization**. Nothing existing was removed or rewritten. |
| `odontoflow-planning/orchestration/route.py` | new | Read-only router: the executable form of the CLAUDE.md table, and the dry-run mechanism (the repo had no test convention). It never dispatches, never writes, never contacts a model. |
| `odontoflow-planning/orchestration/test_route.py` | new | The scenario proofs below. Plain `python3`, no pytest, no venv. |
| `odontoflow-backend/CLAUDE.md` | new | A worker launched with cwd = backend loads *that* directory's `CLAUDE.md` and `.claude/skills/`, inheriting nothing from planning. Without this file a backend worker loaded no instructions either. Imports the existing `AGENTS.md`; adds the worker contract (lane skills, one writer, no concurrent pytest, protected surfaces, preserve dirt). |

Those five are the mechanism. The consolidation diff-check found the activity's
**full** footprint is eight files — the five above plus three the first report
mentioned only in prose:

| File | New? | Why |
|---|---|---|
| `odontoflow-planning/CAVELOG.md` | modified | The existing decision log. One appended row, newest-first, no parallel ledger. |
| `odontoflow-planning/docs/handoffs/plans/2026-09-17-harness-entry-point-repair.md` | new | This brief. |
| `odontoflow-planning/.gitignore` | modified | `__pycache__/`. This activity introduced the first Python into a repo that had none, and running the dry-run left `orchestration/__pycache__/route.cpython-312.pyc` untracked. The artifact was deleted and the pattern added so the harness cannot pollute the repo on every run. |

The `@AGENTS.md` import is a documented Claude Code feature (recursive, max 4
hops). It means there is still exactly one canonical body per contract — editing
`AGENTS.md` continues to be the way to change the rules, and Codex keeps reading
the same file.

## Execution behavior — before vs after

| | Before | After |
|---|---|---|
| Instructions loaded in planning | `context7.md` only; `AGENTS.md NOT LOADED` | `CLAUDE.md` + imported `AGENTS.md`; operator can quote the routing command |
| Instructions loaded by a backend worker | none | `CLAUDE.md` + imported `AGENTS.md`; self-identifies as "backend implementation worker" |
| Routing input | free-text `status:` prose, read by a human | enumerated `lifecycle_state`, 9 states, machine-checkable |
| `READY_TO_BUILD` | did not exist anywhere in the repo | defined, gated on `implementation_authorized`, forbids writing a second validation report |
| Validation PASS | same field as DONE | `validation.result` and `lifecycle_state` are different fields; a PASS on an authorized card explicitly annotates "PASS is not DONE" |
| Validated-but-unregistered work | CORE-01 validated, control plane pointed elsewhere | CORE-01 registered with its SPEC, validation report, write surface, and the exact owner question |
| Product discovery | routed to `grill-me` (invisible/off) | Opus asks the nine questions directly; the disabled skill is stated, not depended on |
| Model at dispatch | inherited / named historically, never probed | named explicitly, all three probed live today |
| SubCard readiness | not represented | dependency + write-ownership overlap resolved deterministically |

## Model routing — verified, not assumed

Probed on this host today. No model identifier in the changed files is unverified.

| Role | Identifier | Proof |
|---|---|---|
| Primary decision-making operator | `claude` agent, `--model opus` (Opus 5) | this session |
| Approved GPT alternative | `openai/gpt-6-astra` | `opencode run` → `ASTRA_OK` |
| Mid-tier coordinator / writer default | `openai/gpt-5.6-luna` | `opencode run` → `LUNA_OK` |

`project.yaml`'s historical alias "GPT-5.6 Luna Max" resolves to
`openai/gpt-5.6-luna`. Dispatch shape was taken from the installed
version-matched guide (`orca skills get orchestration`, orca-ide 1.4.x), not
invented: `worker-start --agent claude --model opus --effort high`, where
`--effort` requires `--model`. Opus stays the single lead; Astra is an approved
alternative, not a second standing operator.

## Tests and scenario results

```
$ python3 orchestration/test_route.py
42 passed, 0 failed
```

Dry-run only — no model was contacted and no worker dispatched by the suite.

| Scenario | Result | What was proven |
|---|---|---|
| **A** new product initiative | PASS (6) | Routes to Opus discovery + SPEC + product delivery plan; does not route to disabled `grill-me`; forbids code and dispatch pre-approval; an activity with *no* `lifecycle_state` fails into discovery rather than into silent implementation |
| **B** approved CORE-01-like activity | PASS (7) | Reaches `READY_TO_BUILD` reusing the existing SPEC and validation; action is implementation, not validation; a second validation report is explicitly forbidden; "PASS is not DONE" is raised; the reusable report is confirmed present on disk; validated-but-unauthorized correctly degrades to `BLOCKED_OWNER_DECISION` |
| **C** authorized card dispatches | PASS (7) | Worker cwd resolves to the real backend checkout; that repo loads instructions; backend-lane skills (`test-driven-development`, `postgres-best-practices`, `verification-before-completion`) and the sales-agent-lane `odontoflow-engineering` resolve from the backend's own `.claude/skills/`; the frontend instruction gap is *reported*, not hidden |
| **D** simple known fix | PASS (5) | `KNOWN_FIX` implements directly; SPEC, discovery and decomposition are forbidden; no owner-authorization stall on a bounded fix |
| **E** product-contract contradiction | PASS (5) | Returns to the owner carrying the cited contradiction; completed SubCards `SC-1`,`SC-2` preserved; discarding unaffected work forbidden; dispatches nothing |
| **F** SubCards vs Activity Cards | PASS (7) | The dependency-ready SubCard continues; a second SubCard claiming an in-flight `router.py` is blocked by one-writer; a SubCard with an unfinished dependency waits; starting a different Activity Card is forbidden; a `DONE` card does nothing and auto-selects nothing |
| **LIVE** real `current-activity.yaml` | PASS (5) | The real control plane parses, starts nothing on its own, and surfaces the pending CORE-01 owner decision |

End-to-end loader proof, run as real Claude sessions against the real repos:

- planning, before: instruction list = `context7.md` only, `AGENTS.md NOT LOADED`
- planning, after: `CLAUDE.md` present, `AGENTS.md` text present, correct routing
  command quoted back
- backend, after: `CLAUDE.md` present, `AGENTS.md` text present, role reported as
  "backend implementation worker … product intent and handoff belong to the
  planning repo upstream"

Live router on the real control plane:

```
activity        : PROJECT-PUBLISH-01
effective state : DONE
DO   : Nothing. Report status and wait for an explicit owner choice.
DON'T: Do not auto-select the next activity.
OWNER DECISION  : CORE-01
  Authorize CORE-01 implementation (yes/no). The product contract is approved
  and validated; only the dispatch authorization is missing.
```

## Blocked — reported, not worked around

**`odontoflow-frontend/CLAUDE.md` was not created.** A frontend worker therefore
still loads no repository instructions.

The conflict is explicit and current. `orchestration/current-activity.yaml`
lists under `protected_surfaces`:

> `odontoflow-frontend/**` (canonical origin healthy, but the local FE3A commit
> `a788df5` is unauthorized and the worktree is dirty — do not touch)

Verified: HEAD `a788df5` is ahead of `origin/main` `0dbfa9e`, with 19 modified
tracked files including product source. Per the instruction to stop on protected
surfaces rather than route around them, the change was not made.

The fix is one file the owner can apply in seconds once the surface is released,
mirroring the backend one:

```markdown
# CLAUDE.md — OdontoFlow Frontend entry point
Claude Code does not auto-load `AGENTS.md`; the canonical contract is imported.

@AGENTS.md

## Worker contract
You are a frontend implementation worker. Product intent, activity selection and
the final handoff belong to `../odontoflow-planning`.
Lane skills resolve from this repo's own `.claude/skills/`:
next-best-practices, vercel-react-best-practices, odontoflow-engineering,
verification-before-completion (+ frontend-design, web-design-guidelines for UI).
Visual PASS is human-only. Respect protected_surfaces; preserve pre-existing dirt.
```

`orchestration/route.py` reports this gap explicitly rather than failing
silently, so it cannot be forgotten.

## Unresolved limitations

- **Real writer execution is still unverified.** No implementation worker was
  ever dispatched by this activity — not to backend, not to frontend, not
  through Orca. What is proven is *routing*: that an authorized card resolves
  the correct repository, that a worker started there loads that repository's
  contract and skills, and that dependency and one-writer rules gate SubCards
  correctly. That an actual writer then completes a SubCard end-to-end remains
  untested and will first be exercised by CORE-01.
- **Frontend loader missing** (above). Until applied, scenario C is proven real
  for backend and reported-as-gap for frontend.
- **The router is advisory.** It encodes the rules but cannot force an operator
  to obey them; `CLAUDE.md` is the binding surface and the router is a check on
  it. If they diverge, `CLAUDE.md` wins and the router is the bug.
- **No SubCards exist yet in the live control plane.** SubCard handling is
  proven against fixtures; CORE-01's decomposition happens when it is authorized.
- **`grill-me` remains globally off.** The harness no longer depends on it, but
  if the owner wants that skill back it is a `~/.claude/settings.json` change
  outside this repair's scope.
- **`TCADD_REPO_HARNESS.md` is still untracked** and still loaded by nothing. It
  was deliberately not tracked or wired in — it is documentation, and making it
  a loaded instruction file would contradict the small-prompt rule it documents.
- **Astra/Luna probes prove reachability, not quota.** Sustained availability was
  not measured.

## Commit status

Consolidated 2026-09-17 after an exact-diff check, as two separate bounded
commits. **Nothing was pushed, merged, reset or cleaned.**

**Backend — `8fcd9e15bfae6913cff53344f868b6252a8fb879`** (parent `c92b558`),
exactly one file: `CLAUDE.md`. `origin/main` remains `193d48b`; the branch is
now 2 ahead, unpushed.

**Planning** — the commit containing this brief, parent `8d61f3a`, exactly six
files: `CLAUDE.md`, `orchestration/current-activity.yaml`,
`orchestration/route.py`, `orchestration/test_route.py`, `CAVELOG.md`,
`.gitignore`, plus this handoff. Both tracked-file diffs are purely additive —
65 insertions, **0 deletions** — so no prior control-plane content was rewritten.

Pre-existing work was left untouched and uncommitted:

- backend: modified `AGENTS.md` (+7) and `.gitignore` (+1), and ~90 untracked
  paths (`.agents/skills/**`, `.claude/skills/**`, `.playwright-mcp/**`,
  `docs/architecture/**`, `docs/reviews/**`, `docs/superpowers/**`,
  `skills-lock.json`)
- planning: ~35 untracked paths (`TCADD_REPO_HARNESS.md`, `archify/**`,
  `docs/plans/**`, `docs/requests/**`, `docs/requirements/**`, `docs/visuals/**`,
  the CORE-01 validation and amendment documents, `.mcp.json`, `.codex/`,
  `skills-lock.json`, the `writing-for-agents` skill)
- frontend: not touched at all; `a788df5` and its 19 dirty tracked files stand
- the three Orca worktrees and the frozen `odontoflow-sim` / `odontoflow-voice`
  trees were never entered

## One next activity

**Owner decides CORE-01.** The product contract is approved, the validation is
current and reusable, the write surface and test plan are named, and the harness
now routes it correctly. The only missing thing is authorization.

To start it, set in `orchestration/current-activity.yaml`:
`activity_id: CORE-01` · `lifecycle_state: READY_TO_BUILD` ·
`implementation_authorized: true` · `repo: odontoflow-backend`, then run
`python3 orchestration/route.py` to confirm the dispatch target before
dispatching one `backend_domain_engineer` writer. The implementation session
must **not** produce a second validation report — it implements against
`docs/handoffs/plans/2026-09-17-core-01-validation.md`.

Do not start AGENT-03, CORE-02, CHAN-03, or integration work from this brief.
