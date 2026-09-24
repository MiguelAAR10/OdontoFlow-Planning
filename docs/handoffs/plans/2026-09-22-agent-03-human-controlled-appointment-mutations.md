# AGENT-03 — Human-controlled appointment mutations

**Status:** DONE — backend commit published and post-push verified
**Implementation date:** 2026-09-22
**Release closeout:** 2026-09-23
**Activity:** AGENT-03 from `2026-09-17-reception-core-closeout-01.yaml`
**Implementation mode:** direct fallback
**Delivery mode:** Orca-supervised release (Codex gpt-5.6-luna)

The earlier Orca launch-configuration blocker and the repository commit
gate are resolved for this activity. The owner accepted YOLO / unrestricted
Orca worker mode and approved the one-time MediStock-clean exception for the
AGENT-03 backend commit. Implementation used the direct fallback; publication
used the existing Orca recovery Run. No product implementation was repeated.

## Business objective

AIRI may propose appointment cancellation or rescheduling, but an agent
principal must never execute either confirmation. Authorized human operations
must continue working. The change must preserve server-resolved identity, IAM
permissions, tenant isolation, proposal expiry, idempotency and replay behavior,
transaction integrity, audit, scheduling behavior, and the existing booking
confirmation refusal.

The owner explicitly authorized AGENT-03 in the 2026-09-22 request. The approved
card has no dependencies. The activity and compact worker brief were registered
in `orchestration/current-activity.yaml`; no different card was started.

## Focused context inspection

The relevant command paths are:

- `run_confirm_cancellation_tool` → `run_idempotent_command` →
  `confirm_cancellation_proposal`.
- `run_confirm_reschedule_tool` → `run_idempotent_command` →
  `confirm_reschedule_proposal`.

Both direct command functions claim a receipt and check permission before their
already-confirmed proposal shortcut. The tool adapters wrap those functions in
`run_idempotent_command`, which can resolve an existing receipt replay before
the command body can enforce a new rule. The booking module already defines
`require_human_confirmation`; it imports `ensure_contact_profile` from the
reception module, so sharing this helper may require moving the single helper
to `app/agent_tools/guards.py` to avoid an import cycle.

Relevant regression file: `tests/test_reception_agent_phase5.py`. The existing
booking refusal is in `app/agent_tools/booking.py` and
`tests/test_agent_booking_phase4.py`. No product contract contradiction was
found during this bounded inspection.

## Orca execution and write-authority evidence

- Runtime: Orca `1.4.190`, healthy local runtime `f1fe0a66-6263-4e57-a678-eac2acc9f9de`.
- Backend worktree: registered `main` worktree
  `2fe3780c-e9d2-49a9-b3ad-847069a9e19b::\\wsl.localhost\Ubuntu-24.04\home\miguel\projects\portfolio\AI-EdgeRunners\odontoflow\odontoflow-backend`.
- Before launch, all backend dispatches were completed, failed, or abandoned;
  no active writer owned the AGENT-03 surface. The live backend `main` inventory
  included the idle coordinator shell `term_fc74c4f0-221c-4c15-abfd-2fea6deb6635`
  and retained CORE-02 writer/reviewer terminals whose Dispatches were already
  completed. A deployment shell belonged to a different worktree.
- Run: `run_f7bcef0d21a4` — “AGENT-03 human-controlled appointment mutations”.
- Task: `task_19538d3b9169` — blocked with the unsafe launch-mode reason recorded.
- Writer Dispatch: `ctx_fb67f2dfbeec`.
- Writer terminal: `term_09fc80c1-1d9c-4f07-a28b-013e518b9809`.
- Requested and effective model in the Orca launch receipt: Claude `sonnet`.
- Reviewer Task/Dispatch: not created; no code was available to review.

### Launch security stop

The Orca Agents page initially showed Yolo, and Claude’s configured Arguments
contained `--dangerously-skip-permissions`. The coordinator temporarily selected
Manual as announced. However, the saved Claude Arguments still contained the
bypass flag, and the live supervised terminal showed `auto mode on`, not the
Manual indicator. Current Claude documentation distinguishes Auto from Manual:
Auto uses a model classifier to decide permission prompts. The host has local
developer/cloud credentials and no isolated remote Orca environment is
configured, so this was not adequate evidence for scoped manual approvals.

The [Claude Code permission modes guide](https://code.claude.com/docs/en/permission-modes)
distinguishes Auto, which uses a model classifier for permission prompts, from
Manual/default mode. The coordinator stopped the exact Dispatch before product
edits. Orca’s first stop call returned `dispatch_inactive`; an immediate
`worker-show` confirmed the
Dispatch had failed with `termination_reason=operator_close`,
`capability_revoked_at=2026-09-22 20:53:07`, and completion at
`2026-09-22 20:53:08`. The worker process exited. The terminal is disconnected,
not writable, and absent from the live terminal inventory. `worker-read`
returned no terminal output. A supported `worker-release` attempt returned
`state=retained`, `reason=identity_unproven`, `processAction=none`, and no
archive; no PID was killed and no unrelated terminal was touched. The initial
Yolo setting and original Claude argument were restored after stopping.

## Resume preflight (2026-09-22)

The owner-authorized activity was resumed from its existing Orca state. No Run,
Task, worktree, or Dispatch was created during this check, and the existing
blocked Task was not made dispatchable.

- Verified executable: `/home/miguel/.local/bin/orca-ide`; runtime `1.4.190`
  is healthy, with the existing Run `run_f7bcef0d21a4` and Task
  `task_19538d3b9169` still present. The installed `orchestration --full`
  guide was read, including its conditional recovery and cleanup rules.
- The prior Dispatch `ctx_fb67f2dfbeec` is `failed`, its capability was revoked,
  its worker is `process_exited`, and its exact terminal
  `term_09fc80c1-1d9c-4f07-a28b-013e518b9809` is disconnected, not writable,
  and absent from the live terminal inventory. The historical retained resource
  was not reused or repeatedly closed.
- The backend worktree has zero active Dispatches. The idle coordinator shell
  `term_fc74c4f0-221c-4c15-abfd-2fea6deb6635` remains at a shell prompt. Two
  historical CORE-02 terminals remain live and user-owned at settled prompts:
  `term_eb2e84d9-2e44-4c50-889e-fe473b179ca5` (Claude) and
  `term_9069cd99-dd18-4484-a6bb-8da0cef37946` (reviewer). Their Dispatches
  `ctx_78573cf4782a` and `ctx_bce609ff0148` are completed, with capabilities
  revoked. These sessions were not stopped, closed, or reused.
- The active Orca profile is `local-default` (`Personal`), confirmed by
  `orca-profile-index.json`. Its read-only profile data at
  `%APPDATA%/orca/profiles/local-default/orca-data.json` contains
  `settings.agentDefaultArgs.claude = "--dangerously-skip-permissions"`.
  The current owner-approved gate accepts Auto or Manual/default only when this
  bypass argument is absent. No fresh Claude process was launched.
- Orca reports only the local host and no remote environment. The local worker
  user's home contains
  `~/.config/gcloud/application_default_credentials.json`. The credential's
  production permissions were not inspected or exercised, so the worker's
  inability to access production write targets cannot be established.

**Decision:** stop before `task-update` and `worker-start`. The remaining
configuration is the active Claude default argument above. Resumption also
requires a verifiable execution boundary that prevents access to production
write targets. The coordinator must not modify global Orca settings. The
existing Run and Task remain available for a later safe resume.

## Delivered product changes and tests

The implementation is in the backend repository:

- `app/agent_tools/guards.py` owns the shared `require_human_confirmation`
  guard.
- `app/agent_tools/booking.py` imports that helper, preserving the existing
  booking refusal.
- `app/agent_tools/reception.py` checks the guard before direct cancellation
  and rescheduling command transactions and before tool receipt replay.
- `tests/test_reception_agent_phase5.py` covers pending and already-confirmed
  proposals through direct and tool paths, plus stored cancellation and
  rescheduling receipt replay. Test agents hold the relevant permissions.
- `CHANGELOG.md` records the behavior; no schema, API, OpenAPI, scheduling, or
  frontend changes were needed.

The detailed evidence is in the
[backend AGENT-03 handoff](../../../../odontoflow-backend/docs/superpowers/handoffs/2026-09-22-agent-03-human-controlled-appointment-mutations.md).

RED/GREEN and verification evidence:

- Initial new tests: **6 failed as expected** because direct/tool confirmation
  and stored receipt replay returned success without `INVALID_INPUT` refusal.
- Focused final AGENT-03 cases: **10 passed, 9 deselected**.
- Reception file before the final test matrix expansion: **15 passed**.
- Related reception, booking, IAM, tenant, idempotency, agent-tool and
  security-boundary files before the final expansion: **166 passed**.
- Final full serial suite against local PostgreSQL `odontoflow_test`:
  **650 passed, 21 existing warnings** in 8m59s.
- Independent read-only security review: **PASS**, no material finding. It did
  not run tests; its bearer-HTTP-path limitation is documented in the backend
  handoff. Coordinator diff review also confirmed the replay guard ordering.
- The scoped credential-pattern scan found no credential-like values in the seven intended implementation, changelog, and handoff files; `git diff --check` reported no whitespace errors.

Implementation execution used the direct fallback. The later publication
used an Orca-supervised Codex release; no Claude was used for release.

## Preserved contracts and pre-release publication state (2026-09-22)

This section records the state before the 2026-09-23 publication closeout below.

The existing IAM permission checks, server-resolved `ExecutionContext`,
tenant-scoped queries, proposal binding and expiry, receipt behavior, atomic
transaction/audit path, scheduling behavior, human cancellation/rescheduling,
and booking refusal remain intact. Agent refusal occurs before direct command
receipt claims and before tool-level stored outcome replay.

The backend remains on `main` at
`59be27678d7cc46041befe93206242f34ed145de`; changes are local and uncommitted.
No remote SHA exists and no push occurred. Backend `AGENTS.md` requires the
MediStock worktree to be clean before commit. The required read-only status
check found a pre-existing untracked `.audit/` directory in `../../medistock`;
it was preserved. No commit was created. The previous Orca Run
`run_f7bcef0d21a4`, Task `task_19538d3b9169` and failed Dispatch
`ctx_fb67f2dfbeec` remain historical launcher-recovery records only.

Unrelated backend dirty/untracked files and the existing local planning
`orchestration/current-activity.yaml` / `CAVELOG.md` edits were preserved.
This handoff is updated locally and unpublished.

## Delivery recovery preflight before owner decision (2026-09-22)

The final backend worktree was rechecked without modifying product files:

- Planning is on main at f4f13fd7b035a5c2d15a133cba40409c070b4dac, with local
  origin/main at the same SHA and zero ahead/behind. Backend is on main at
  59be27678d7cc46041befe93206242f34ed145de, with local origin/main at the
  same SHA and zero ahead/behind. No fetch or push was performed.
- The backend implementation remains the five authorized modified files
  listed above plus this technical handoff. The current product/test diff
  matches the paths and behavior in the handoff and the review's cited guard
  locations. No product implementation or test file changed during this
  delivery recovery.
- Existing test evidence remains 6 RED failures, 10 focused GREEN passes,
  166 related regressions before the final matrix expansion, and 650 full
  serial PostgreSQL passes / 21 warnings. No suite was rerun. Existing
  handoffs contain the result summaries but not raw pytest logs or a content
  hash, so correspondence to the final tree is verified by exact path and
  diff review rather than a content-addressed test artifact.
- The independent read-only reviewer returned PASS for the current security
  call paths: direct guards precede transaction/receipt claims, tool guards
  precede receipt replay, and the shared guard preserves human paths. Its
  review was not an Orca Task and did not run tests or touch the database. The
  reviewer noted that changelog and handoff updates were not yet present at its
  review point; those documentation-only files were added afterward. No
  product or test path changed after that review.

### MediStock commit gate

The backend AGENTS.md requires a clean tree in ../../medistock and the
coordinator to commit only after fan-in. This is a repository instruction, not
an active Git hook: no core.hooksPath is configured and the default hooks
directory contains only .sample hooks.

Read-only Git metadata reports MediStock at
ef2fffb7a348aa621f7a5b387e09a1553351000f with ?? .audit/; .audit/ is absent
from the index and HEAD. The existing handoff had already recorded this
untracked directory before the current delivery recovery. Its original
creator and creation time cannot be determined from Git metadata. There is no
permitted cleanup route: MediStock is read-only, and this activity does not
authorize changing its files or Git state. No evidence indicates AGENT-03
created it; no AGENT-03 path writes there.

One owner decision: approve or decline a documented one-time exception to the
MediStock-clean commit condition. Approval would permit only one scoped local
backend commit of AGENT-03 implementation, tests, changelog, and technical
handoff; .audit/ would remain untouched, and this would not authorize a push.
Declining leaves the verified implementation local and uncommitted. No files
have been staged.

### Separate credential follow-up

The remote database URL credential referenced by backend .env.local was shown
in earlier tool output. Its value is omitted and was not read, copied, or used
during this recovery. Action requested of the authorized credential owner:
rotate or revoke. Completion is unconfirmed. No production system was
accessed or changed.

The planning control plane and CAVELOG recorded this pre-release state. It
was superseded on 2026-09-23 by the approved exception and publication closeout
below. Do not start another Activity Card.

## Publication closeout (2026-09-23)

### Owner decisions and release scope

- The owner approved the one-time MediStock-clean gate exception for this
  AGENT-03 backend commit. MediStock .audit/ remained completely untouched.
- YOLO / unrestricted Orca worker mode was accepted for this development
  activity. Claude was not used for the release.
- Credential rotation/revocation remains a separate pending operational
  follow-up and does not block publication. No secret-like material was found
  in the intended AGENT-03 diff.

### Implementation and historical evidence

- Implementation mode: direct fallback. Delivery mode: Orca-supervised
  release in the existing Run run_0faacef0f28a.
- The audit artifact at
  ../../superpowers/evidence/agent-03-delivery-diff-audit.yaml recorded
  DIFF_AUDIT = PASS_UNCHANGED. All six intended path hashes and the intended
  diff hash matched the recovery snapshot at release.
- Historical evidence was reused: 6 expected RED failures, 10 focused passes
  (9 deselected), 166 related regressions, and 650 serial PostgreSQL passes /
  21 warnings. The independent read-only security review returned PASS.
  No tests were rerun during release recovery.
- The historical evidence is tied by path/diff hash continuity. Raw pytest logs
  and a test-time content hash were not captured.

### Backend publication

- Commit: 02fb031c6949c1c5ea69278a9e9a33a4cbb17f72
- Parent: 59be27678d7cc46041befe93206242f34ed145de
- Verified remote SHA: 02fb031c6949c1c5ea69278a9e9a33a4cbb17f72
- The post-push read-only Codex verifier returned PASS on Task
  task_4f8ef3b3cbef / Dispatch ctx_8d7bbc5f25a1. It confirmed the remote SHA,
  expected parent, and exactly these six paths with no unrelated files:
  app/agent_tools/booking.py, app/agent_tools/guards.py,
  app/agent_tools/reception.py, tests/test_reception_agent_phase5.py,
  CHANGELOG.md, and
  docs/superpowers/handoffs/2026-09-22-agent-03-human-controlled-appointment-mutations.md.
- The release Task was task_2db853df1e84 in the existing Run. Its Codex
  gpt-5.6-luna worker completed the commit and normal push; Orca marked its
  two Dispatch attempts agent_prompt_stalled and rejected worker_done after
  capability revocation. The coordinator recorded the recovered release
  result on the existing Task. No force push, reset, rebase, squash, cleanup,
  deployment, or second push was performed.
- The staged git diff --cached --check result was false because the unchanged
  backend technical handoff contains three trailing-space Markdown hard-break
  lines. The snapshot was preserved. The scoped staged secret-pattern scan
  returned clean.

### Harness debt and handoff

- Codex reported mcp_servers.context7.type as an ignored or unrecognized
  configuration setting. This is non-blocking harness debt and was not fixed.
- Claude agent_prompt_blocked remains a separate harness issue. Codex also
  reported agent_prompt_stalled during the release Dispatch attempts; both
  issues are separate from AGENT-03 product completion.
- Planning handoff:
  docs/handoffs/plans/2026-09-22-agent-03-human-controlled-appointment-mutations.md.
  Backend technical handoff:
  ../odontoflow-backend/docs/superpowers/handoffs/2026-09-22-agent-03-human-controlled-appointment-mutations.md.
- AGENT-03 is DONE. Wait for an explicit owner choice before starting any
  other Activity Card. Do not start AGENT-02.
