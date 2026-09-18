# CLAUDE.md — OdontoFlow Planning entry point (Repo 0)

This is the only instruction file Claude Code auto-loads here. `AGENTS.md` is
**not** auto-loaded by Claude Code (it is read by Codex and other agents), so it
is imported below rather than duplicated. Edit the canonical body in `AGENTS.md`;
keep this file to routing.

@AGENTS.md

## 0. First action in every session

Read `orchestration/current-activity.yaml` **before** proposing work. Branch on
its `lifecycle_state` field — never on the free-text `status:` prose, and never
on your own reading of the docs. If `lifecycle_state` is absent or unknown,
treat it as `NEEDS_PRODUCT_DISCOVERY` and say so.

To see the routing decision without acting on it:

```bash
python3 orchestration/route.py                    # current activity
python3 orchestration/route.py --state <FILE>     # any activity file
```

The router is read-only. It never dispatches, and its verdict is advisory to
the same rules written below — if they disagree, the rules win and the router
is the bug.

## 1. Lifecycle states and what each one authorizes

| `lifecycle_state` | What this session does | What it must NOT do |
|---|---|---|
| `NEEDS_PRODUCT_DISCOVERY` | Run product discovery yourself (§2), produce a SPEC + product delivery plan, stop for owner approval | Write code; dispatch a writer |
| `SPEC_APPROVED` | Targeted functional validation, then technical design; emit an Activity Card with SubCards (§3) | Re-run discovery; author a second SPEC |
| `READY_TO_BUILD` | Dispatch one authorized writer per write surface and work dependency-ready SubCards to completion (§4) | Produce another validation report; re-validate what the card already records |
| `IN_PROGRESS` | Continue the **same** card's remaining dependency-ready SubCards | Start a different Activity Card |
| `NEEDS_VERIFICATION` | Verify against acceptance, then write the self-contained handoff | Mark `DONE` without evidence |
| `KNOWN_FIX` | Implement directly — no SPEC, no discovery, no card decomposition | Escalate a one-file fix into product planning |
| `BLOCKED_OWNER_DECISION` | Present the decision, options, and trade-offs; stop | Decide it on the owner's behalf |
| `CONTRACT_CONTRADICTION` | Return to the owner with the cited contradiction; preserve every unaffected completed SubCard | Discard or re-open work the contradiction does not touch |
| `DONE` | Nothing. Report status and wait | Auto-select the next activity |

`advance_automatically: false` is in force. One valuable activity at a time.

**Validation PASS ≠ product DONE.** They are different fields
(`validation.result` vs `lifecycle_state`). A successfully written validation
report is not a stopping point: if the card is `READY_TO_BUILD` and
`implementation_authorized: true`, writing the report and stopping is the
failure this harness exists to prevent.

## 2. Product discovery (`NEEDS_PRODUCT_DISCOVERY`)

Opus runs this directly. **The `grill-me` skill is disabled in this environment**
(`skillOverrides."grill-me": "off"` in `~/.claude/settings.json` — verified
2026-09-17), so do not route to it or wait for it. Ask the questions here:

business problem · who the user is · expected value · observable outcome ·
business rules · invariants · non-goals · acceptance · risks

Stop when all nine are answered or explicitly deferred by the owner. Output a
SPEC (persistent WHAT/WHY/CONTRACT) plus a product delivery plan, using the
existing conventions in `docs/plans/` and `docs/handoffs/plans/`. Material
product decisions need owner approval.

Do **not** re-open discovery or author a new SPEC for an activity that already
has an approved, bounded product contract. Re-open it only when new evidence
actually invalidates that contract — then set `CONTRACT_CONTRADICTION`.

## 3. Activity Cards and SubCards (`SPEC_APPROVED`)

Cards live in the existing planning artifacts — `orchestration/current-activity.yaml`
and the activity lists in `docs/handoffs/plans/*.yaml`. Do not introduce a second
task system, a tracker, or a new directory tree.

Each SubCard carries: `outcome` · `dependencies` · `interfaces` ·
`write_ownership` · `evidence` · `acceptance` · `model_class` · `status`.

A SubCard is dispatchable when every id in `dependencies` has `status: done` and
no other in-flight SubCard claims an overlapping path in `write_ownership`.

## 4. Dispatch (`READY_TO_BUILD` / `IN_PROGRESS`)

Planning owns product intent, decisions, orchestration state, integration
coordination, and the final handoff. Planning writes no product code.

- Backend SubCards run with cwd = `../odontoflow-backend` (or its Orca worktree).
- Frontend SubCards run with cwd = `../odontoflow-frontend` (or its worktree).

A worker loads its repo-local `CLAUDE.md` and `.claude/skills/` from **its own
working directory** — nothing is inherited from planning. So dispatch into the
right checkout and let the repo supply its skills. Do not copy backend or
frontend skills into planning. Load only what the worker's lane in
`orchestration/skill-matrix.yaml` lists.

One writer per overlapping write surface (`max_parallel_writers: 1`).
Parallelize only SubCards that are independently executable, have stable
interfaces, name an integration owner, and are safely isolated.

**Models are named explicitly at dispatch — never inherited.** Verified
accessible on this host, 2026-09-17:

| Role | Identifier | Verified |
|---|---|---|
| Lead product/architecture judgment | `claude` agent, `--model opus` (Opus 5) | this session |
| Approved GPT alternative | `openai/gpt-6-astra` | `opencode run` → `ASTRA_OK` |
| Mid-tier coordinator / writer default | `openai/gpt-5.6-luna` | `opencode run` → `LUNA_OK` |

Opus is the primary decision-making operator. GPT Astra is an approved
alternative for consequential judgment, not a second standing lead — do not run
two independent lead operators by default. Use the mid-tier coordinator for
mechanical scheduling, dependency tracking, worker lifecycle, and evidence
collection. Pick implementation models by task difficulty, risk, quota, and
observed performance. Never cycle through unverified model ids; if an id is not
in the table above, probe it or ask.

Dispatch shape (resolve against the installed guide at run time —
`orca skills get orchestration`; this is the 1.4.x form):

```bash
orca orchestration worker-start --task <id> --worktree current \
  --agent claude --model opus --effort high --json
```

## 5. Boundaries

Honor `protected_surfaces` in `orchestration/project.yaml` and in the current
activity. If a change would touch a protected surface or unrelated dirty work,
report the exact conflict and stop that change — do not work around it.

Preserve existing dirty worktrees and active sessions. Evidence outranks docs;
git and live schema outrank both. Record decisions in `CAVELOG.md`; never start
a parallel ledger.
