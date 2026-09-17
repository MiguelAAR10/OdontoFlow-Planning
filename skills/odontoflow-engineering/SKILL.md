---
name: odontoflow-engineering
description: Use when building, reviewing, or reasoning about OdontoFlow's Sales Agent / n8n integration surface — sales_agent/, app/agent_tools/, app/messaging/, integration credentials, or any LLM-facing tool boundary. Canonical engineering contract for that surface; one page, read once per session that touches it.
---

# OdontoFlow Engineering — Sales Agent / Integration Surface

## Non-negotiable invariants

1. **API-first.** The Sales Agent is an HTTP client of `odontoflow-backend`,
   never a peer with direct database access: `sales_agent → HTTP → app`,
   never the reverse.
2. **PostgreSQL is canonical truth.** Conversation state, Agent Memory, and
   Business State are three different things and never merge — Business
   State lives only in the canonical database; Agent Memory is disposable
   and carries no authority. See `CONTEXT.md`.
3. **Domain rules live outside LLMs.** The model selects and sequences typed
   tools; it never computes price, availability, or clinical judgement itself.
4. **Typed tools only, no arbitrary SQL.** Every agent action is one of the
   allowlisted `agent_tools/*` calls behind `POST /agent-tools/call`.
5. **One writer per overlapping change surface.** Solo by default; escalate
   only per `foreman-handoff` §3's stated-value test.
6. **Risk-weighted TDD.** Failing tests first, against real PostgreSQL, for
   auth boundaries, tenant isolation, idempotency, and any forbidden-access
   surface. Not for CSS or layout.
7. **Preserve contributor history.** Never squash, rebase, amend or
   force-push a merged contributor commit.
8. **No secrets in the repo.** Model/provider credentials come from the
   environment; never printed, never committed.
9. **Evidence before claims.** Every PASS/DONE claim cites the command and its
   output — see the repo-local `verification-before-completion` skill.
10. **Handoffs persisted in Markdown**, one living brief per activity, in
    `odontoflow-planning/docs/handoffs/plans/` — never a parallel status file.
11. **Standard commit discipline.** One task = one commit;
    `feat|fix|test|docs: <summary>`; `main` stays green.
12. **MediStock is read-only**, outside the workspace. Never modify it.
13. **No horizontal infrastructure without explicit scope** — no new repo, no
    new orchestrator, no queue/cache layer, unless the current activity says so.

## Where to look next

- Current work: `odontoflow-planning/orchestration/current-activity.yaml`
- Domain words (Sales Agent, Conversation, Agent Memory, World State,
  Appointment, Patient Confirmation): `odontoflow-planning/CONTEXT.md`
- Repo roles, protected surfaces, coordinator/writer defaults:
  `odontoflow-planning/orchestration/project.yaml`
- Full execution spec (architecture, tool allowlist, acceptance criteria):
  `odontoflow-planning/docs/plans/2026-09-05-sales-agent-v0-integration.md`
- Backend-wide engineering rules (persistence, services, API shape):
  `odontoflow-backend/AGENTS.md`
- TDD mechanics, Postgres patterns, LangChain/LangGraph mechanics, n8n
  lifecycle, security hardening: already-installed repo-local skills in
  `odontoflow-backend/.claude/skills/` — lane routing in
  `odontoflow-planning/orchestration/skill-matrix.yaml`.
