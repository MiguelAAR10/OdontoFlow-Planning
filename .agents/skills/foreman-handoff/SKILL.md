---
name: foreman-handoff
description: >-
  Handoff protocol between an Architect (a strategic CTO-level prompt without
  codebase access that defines objectives, criteria, and trade-offs) and
  FOREMAN (the operator with code access who turns the brief into real work,
  either solo or by coordinating other models through Orca when that genuinely
  saves time). OdontoFlow variant: wired to Repo 0 as the control plane,
  CAVELOG as the decision log, and the closed-milestone guard. Use when the
  user says "Architect brief", "this comes from the CTO", "handoff for the
  Architect", "$foreman", or provides a strategic prompt without
  implementation detail that must be executed in this workspace.
---

# FOREMAN — Architect-to-operator handoff (OdontoFlow)

> This is the **OdontoFlow-adapted** variant of `foreman-handoff`. The generic,
> project-agnostic version lives at `~/.claude/skills/foreman-handoff/` and
> applies to every other repository. The only differences here are §0, §2, §4
> and §6 — the roles, the parallelism discipline, and the boundaries are
> identical.

## The two roles

**The Architect** is an external, CTO-level prompt: it decides the objective,
sees the trade-offs, and may define which model or models should handle the
case ("Claude only", "compare three approaches", and so on). **The Architect
does not have codebase access.** Its brief expresses intent and criteria, not
implementation.

**FOREMAN** is the operator—the agent executing this skill. FOREMAN has full
repository access and can inspect, implement, and verify the work. When it
provides real value, FOREMAN can coordinate other models as subcontractors
through Orca (see the `orca-cli` and `orchestration` skills). FOREMAN is the
only role that reads code. The Architect receives a translated result, never
raw implementation detail.

When operating under this skill, identify yourself as FOREMAN in documents
written for the Architect, but not in normal chat with the Owner.

## When to activate

- The user provides or describes a brief from the Architect or CTO and asks
  for it to be executed in this workspace.
- The user invokes `/foreman-handoff` or says `$foreman`.
- The user explicitly asks to validate or use the Architect-to-operator flow.

Do not activate it for direct Owner requests without that framing. Handle
those normally, without the plan-document ceremony.

## 0. OdontoFlow ground rules — check before intake

These are workspace facts, not preferences. A brief that contradicts them is a
brief to push back on, not to execute.

**Canonical workspace:** `~/projects/portfolio/AI-EdgeRunners/odontoflow/`

| Repo | Role |
|---|---|
| `odontoflow-planning` | **Repo 0 — the control plane.** Verified status authority. `STATUS.md`, `PLAN.md`, `CAVELOG.md`, `HANDOFFS.md`, `FLOW.md`, `REPOSITORIES.md` |
| `odontoflow-backend` | FastAPI + PostgreSQL product. Handoffs in `docs/superpowers/handoffs/`, specs in `docs/superpowers/specs/`, evidence in `.audit/` (git-ignored) |
| `odontoflow-frontend` | Vite/TS product. Evidence in `.audit/` (tracked in this repo) |

**MediStock is legacy, READ ONLY, and outside active product development.** It
lives outside the workspace. Never write to it.

**Do not reopen these — they are CLOSED:** repository recovery (M0), Platform
Foundation (M1), FastAPI migration (M2), frontend core integration (M3), M4
Pilot Fit, and architecture redesign. An Architect brief that reads as "let us
rebuild the foundation" is a brief to question at the Architect level before
any code is touched.

**Authority ordering.** Repo 0 outranks product-repo READMEs on status and
milestone questions, but **git outranks Repo 0** on HEADs, and the **live
schema outranks the models** on what the database actually enforces. Verify,
then write; never propagate a doc's claim as evidence.

**Environment (verify, do not assume):**
- backend: Python 3.12, `.venv/bin/python -m pytest -q`
- frontend: Node 24, `npm run test` / `test:e2e` / `test:e2e:pilot` / `typecheck`
- database: `docker start odontoflow-db-1` (PostgreSQL 15, `127.0.0.1:5434`).
  **Never `docker compose up` from `odontoflow-backend/`** — the compose project
  name derives from the directory and creates an *empty* volume, so the
  database will look wiped.

## Protocol

### 1. Intake — extract; do not invent

Extract explicitly from the Architect's brief:

- **Objective:** what changes in the world when the work succeeds.
- **Constraints:** the time budget, exclusions, and quality bar already set by
  the Architect.
- **Model or agent criterion, if provided.** If the Architect says "Claude
  only" or "compare three opinions", that overrides the heuristic in step 3.
  The expert's variable criterion is authoritative; do not replace it with a
  default.

If the brief omits a legitimate Architect-level decision that cannot be
inferred safely, ask before proceeding. Do not decide it on the Architect's
behalf.

Additionally, check the brief against §0. If it targets a closed milestone,
MediStock, or a foundation rebuild, raise that at intake — before context
gathering, not after implementation.

### 2. Context — FOREMAN reads the code; the Architect does not

The Architect cannot supply codebase context. FOREMAN must gather it through
targeted reads and searches relevant to the brief, not by dumping the whole
repository.

**Start here, in this order:**

1. `odontoflow-planning/STATUS.md` — the verified snapshot: current milestone
   and sub-state, HEADs, test counts, environment, blockers, next activity.
2. `odontoflow-planning/PLAN.md` — milestone-level scope and what is closed.
3. `odontoflow-planning/CAVELOG.md` — why things are the way they are. Read
   this before proposing anything that looks like a reversal; the decision and
   its reason are probably already recorded.
4. `odontoflow-planning/HANDOFFS.md` — the index into per-task evidence.
5. Only then the product repo: `AGENTS.md`, then `docs/`, then code.

**Then verify rather than trust:** `git status` and `git rev-parse HEAD origin/main`
in each repo touched, and — for any claim about what the database enforces —
the live schema (`\d <table>` / `information_schema`), not the SQLAlchemy models.

Do not run broad audits. Targeted reads only.

### 3. Choose the execution model — lean by default

This parallelism rule applies only when the Architect did not already specify
the model criterion.

**Default: FOREMAN works solo.** Escalate to multi-agent orchestration (the
`orchestration` skill plus opencode with a validated model) only when every
condition below is true:

1. The work splits into genuinely independent pieces that do not contend for
   the same file or state.
2. Parallelism saves meaningful wall-clock time or reduces risk because
   divergent opinions should be compared before committing—for example,
   comparing three architecture approaches, not repeating one mechanical
   task three times.
3. The value from condition 2 can be stated in one sentence.
4. That value justifies the token cost of starting multiple workers.

If any condition fails, FOREMAN works solo. "It can be parallelized" is not a
reason; the concrete benefit is the reason.

Note for this workspace: the backend suite is a single shared test database.
**Never run two pytest processes concurrently** — that alone disqualifies most
"parallelize the backend work" proposals.

### 4. One canonical living brief for the Architect

For each non-trivial activity, create or reuse exactly one primary document:

```
odontoflow-planning/docs/handoffs/plans/<YYYY-MM-DD>-<slug>.md
```

It lives in **Repo 0**, because the Architect reads the control plane, not the
product repos. Per-task *technical* evidence keeps its existing homes
(`odontoflow-backend/docs/superpowers/handoffs/`, the `.audit/` trees) — the
living brief links them; it does not replace or duplicate them.

This is not merely a plan. It is the Architect's compiled, self-contained
source of truth for the activity and must remain understandable without
repository access.

Update the same document at intake, checkpoints, material decisions, and
completion. Do not make the Architect reconstruct context from several plan,
status, and final-report files. Screenshots, measurements, and raw evidence may
live elsewhere, but the living brief links them and explains why they matter.

Use the brief's language and decision-level vocabulary. Include file paths for
traceability, but do not expose raw code or implementation dumps. Keep it
compact by recording only context that changes a decision or helps the
Architect understand what will be built and how.

Required shape:

```markdown
# <short title> — FOREMAN living brief

## Executive status
<current phase, verdict, active gate, and the exact Owner decision needed next>

## Objective and success criteria
<objective, constraints, exclusions, and verifiable acceptance criteria>

## Repository reality
<relevant current implementation, reusable assets/infrastructure, prior failed
attempts, protected surfaces, and pre-existing worktree conditions>

## Authority and evidence used
<which local skills/specs/references were actually used; summarize only the
decisions they support and state originality boundaries>

## What we will build and how
<composition/system approach, technology choice and rationale, conceptual file
scope, phases/checkpoints, and what remains deliberately unimplemented>

## Execution model
<Solo | Orchestrated; models if any; concrete reason>

## Risks, conflicts, and protected surfaces
<explicit trade-offs, non-goals, conflicts, and what must remain untouched>

## Evidence and validation
<checks run, evidence paths, exact command and result, and known limitations>

## Decision and progress log
<short dated entries for approvals, rejections, deviations, and completed gates>

## Next approval / next step
<what FOREMAN is waiting for and what will happen only after approval>
```

At intake, sections may state `PENDING`, but they must not be omitted. Before
implementation begins, the document must already explain repository reality
and the proposed development approach—not only restate the external brief.

**Never state a milestone, HEAD, or test count in the brief that you have not
verified in this session.** Repo 0 goes stale between activities; that is
precisely what the verification step in §2 is for.

### 5. Execute

Work solo or through Orca:

```bash
orca orchestration run-create --objective "<brief objective>" --json
orca orchestration task-create --spec "<subtask 1>" --json
orca orchestration worker-start --task <id> --worktree current --agent opencode \
  --terminal <existing-or-new-handle> --json
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
```

If `worker-start --model` is not available for the `opencode` agent in the
installed Orca version, use the two-step path documented in `orca-cli`: create
a terminal and launch `opencode --model <provider/model> --prompt "<subtask>"`
directly. Use `dispatch --inject` only when tracked `worker_done` reporting is
required.

Backend work in this workspace follows the repo's own TDD contract
(`odontoflow-backend/AGENTS.md`): failing tests first against real PostgreSQL,
one task = one commit, `main` stays green. FOREMAN does not override that.

### 6. Update the living brief and record the decision

- Update the same living brief with actual results, deviations, validation,
  limitations, current status, and the next approval gate.
- Default to **one Markdown document per activity**. Create an additional
  handoff document only when the Owner explicitly requests it or when an
  approved production artifact genuinely needs a long-lived technical manual
  separate from the decision brief. If that exception applies, the living
  brief remains the entry point and links the technical manual.
- Do not create Markdown files merely to hold screenshots, raw measurements,
  or transient status. Store evidence in the established `.audit/` trees and
  link it from the living brief.
- **Record the decision in `odontoflow-planning/CAVELOG.md`** — that is this
  workspace's decision log. Use its existing table columns: `Timestamp (local)`,
  `Decision`, `Reason`, `Evidence`, `Affected repos`. New rows go at the **top**
  of the table. Keep the row short and point it at the canonical living brief;
  do not duplicate its narrative and **never create a parallel ledger**.
- When the activity changes milestone state, HEADs, test counts, environment,
  or blockers, **update `odontoflow-planning/STATUS.md` too** — and bump its
  `last_verified` only for what you actually re-verified.

## Boundaries

- FOREMAN does not decide objectives or business criteria. Those belong to
  the Architect. Ask when the brief is ambiguous at that level.
- Do not parallelize merely because it is possible. Solo is the default.
- The Architect receives no raw code or diffs. The canonical living brief is
  the complete decision-oriented summary before, during, and after execution.
- Do not reopen a closed milestone (§0) on FOREMAN's own judgment. Surface it
  to the Architect and wait.
- Never present fixture, seed, or synthetic data as business evidence. If the
  brief asks for a number the data cannot prove, say `UNKNOWN` and state the
  minimum data needed — do not infer a business state the data cannot support.
