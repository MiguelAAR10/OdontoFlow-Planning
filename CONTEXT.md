---
title: OdontoFlow — Domain Vocabulary
status: active
last_verified: 2026-09-17
authority: Repo 0 (planning)
---

# Context — Domain Vocabulary

Words, not implementation. For state/milestones see `STATUS.md`/`PLAN.md`; for
routing see `orchestration/`; for the full Sales Agent design see
`docs/plans/2026-09-05-sales-agent-v0-integration.md`.

**Contact** — whoever is messaging in, identified by channel (`ChannelAccount`)
and phone. A Contact becomes a **Patient** only once qualified into the
canonical clinical record; not every Contact is a Patient.

**Conversation** — the canonical record of one Contact's ongoing exchange.
Owned by `odontoflow-backend`, in PostgreSQL. One open Conversation per
Contact; it reaches `closed` through an explicit transition, never by timeout.
It is what was said — the audit trail, not the agent's reasoning.

**Sales Agent** — the model-driven process that reads a Conversation, decides
what to say and which typed tool to call, and proposes bookings. It has no
authority of its own: every price, slot, and booking decision it produces is
computed by deterministic tools in `odontoflow-backend`, never invented. Its
only two write paths are *propose* and *confirm* (see Patient Confirmation),
plus Human Handoff when the case is outside its remit.

**Typed tool** — the only interface any agent (Sales Agent, future adapter) has
to Business State: a fixed, allowlisted function with a typed contract
(`POST /agent-tools/call`), never raw SQL or free-form access. If a capability
has no typed tool, no agent can do it — that is the enforcement mechanism, not
a convention.

**Human Handoff** — the deterministic, tool-triggered transition that takes a
Conversation out of agent hands: every tool then fails closed until an
operator resumes. A canonical business fact recorded like any other, not a
paused agent loop or an agent-side retry.

**Agent Memory** — the Sales Agent's own working state (conversation thread,
in-progress reasoning), physically separate from canonical Business State.
Disposable: dropping it must never lose a Conversation, an Appointment, or any
other canonical fact. It is fluency, not truth. Conversation state, Agent
Memory, and Business State are three different things and never merge.

**Business State / World State** — the one canonical state OdontoFlow
maintains (`Lead`, `Patient`, `Appointment`, availability, economics,
inventory), read and written only through typed tools regardless of which
actor — ERP user, Sales Agent, future adapter — initiates the change.

**Canonical / Real / Simulated** — three different truth-claims, never
interchangeable. *Canonical* is the one Business State above. *Real* means
verified against it or against live clinic data — never assumed from a
document. *Simulated* is `odontoflow-sim`'s permanently-labeled synthetic
World State: useful for measurement, never promotable to canonical and never
to be mistaken for it.

**Appointment** — a scheduled booking against real availability. Authoritative
regardless of who proposed it; the same booking command underlies both the ERP
and the Sales Agent path, so a slot is a slot everywhere.

**Patient Confirmation** — the explicit affirmative reply required before a
*proposed* Appointment becomes a *confirmed* one. Nothing is booked on a first
message; confirmation is a distinct, later step, and a duplicate confirmation
must still resolve to exactly one Appointment.
