#!/usr/bin/env python3
"""Scenario proofs for the planning entry-point router.

Dry-run only: no model is contacted, no worker is dispatched, nothing is
written. Run with plain python3 (no pytest, no venv):

    python3 orchestration/test_route.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from route import DEFAULT_STATE, REPO_ROOT, route  # noqa: E402

FAILURES: list[str] = []
PASSES: list[str] = []


def check(scenario: str, claim: str, ok: bool) -> None:
    (PASSES if ok else FAILURES).append(f"{scenario}: {claim}")


# ---------------------------------------------------------------- scenario A
def scenario_a() -> None:
    """New product initiative routes to Opus discovery and an approvable SPEC."""
    s = "A new-product-initiative"
    d = route({"activity_id": "NEW-THING", "lifecycle_state": "NEEDS_PRODUCT_DISCOVERY"})
    check(s, "effective state is NEEDS_PRODUCT_DISCOVERY",
          d["effective_state"] == "NEEDS_PRODUCT_DISCOVERY")
    check(s, "routes to discovery + SPEC + product delivery plan",
          "discovery" in d["action"] and "SPEC" in d["action"]
          and "product delivery plan" in d["action"])
    check(s, "does not route to the disabled grill-me skill",
          "disabled" in d["action"])
    check(s, "forbids code and dispatch before approval",
          "not write code" in d["forbidden"] and "dispatch" in d["forbidden"])
    check(s, "no dispatch target is resolved", "dispatch" not in d)

    # An activity with no lifecycle_state at all must fail into discovery,
    # not into silent implementation.
    d2 = route({"activity_id": "UNTYPED"})
    check(s, "missing lifecycle_state falls back to discovery",
          d2["effective_state"] == "NEEDS_PRODUCT_DISCOVERY")


# ---------------------------------------------------------------- scenario B
def scenario_b() -> None:
    """Approved CORE-01-like work reuses its SPEC + validation and reaches
    READY_TO_BUILD without generating another validation report."""
    s = "B approved-activity-reuses-validation"
    core01 = {
        "activity_id": "CORE-01",
        "lifecycle_state": "READY_TO_BUILD",
        "implementation_authorized": True,
        "repo": "odontoflow-backend",
        "skill_lane": "backend + sales-agent",
        "spec": "docs/handoffs/plans/2026-09-17-reception-core-closeout-01.yaml",
        "validation": {
            "result": "PASS with bounded contract amendments",
            "report": "docs/handoffs/plans/2026-09-17-core-01-validation.md",
        },
    }
    d = route(core01)
    check(s, "reaches READY_TO_BUILD", d["effective_state"] == "READY_TO_BUILD")
    check(s, "action is implementation, not validation",
          "Dispatch" in d["action"] and "validation" not in d["action"])
    check(s, "explicitly forbids a second validation report",
          "another validation report" in d["forbidden"])
    check(s, "PASS is called out as not-DONE",
          any("PASS is not" in n for n in d["notes"]))
    check(s, "does not re-enter discovery or SPEC authoring",
          d["effective_state"] not in ("NEEDS_PRODUCT_DISCOVERY", "SPEC_APPROVED"))

    # The real validation report exists on disk and is the one to reuse.
    report = REPO_ROOT / core01["validation"]["report"]
    check(s, "the reusable validation report exists on disk", report.is_file())

    # Unauthorized is the difference between validated and dispatchable.
    d2 = route({**core01, "implementation_authorized": False})
    check(s, "validated but unauthorized degrades to BLOCKED_OWNER_DECISION",
          d2["effective_state"] == "BLOCKED_OWNER_DECISION")


# ---------------------------------------------------------------- scenario C
def scenario_c() -> None:
    """An authorized card dispatches the correct role in the correct repo and
    resolves that repo's local skills."""
    s = "C dispatch-lands-in-correct-repo"
    d = route({
        "activity_id": "CORE-01",
        "lifecycle_state": "READY_TO_BUILD",
        "implementation_authorized": True,
        "repo": "odontoflow-backend",
        "skill_lane": "backend + sales-agent",
    })
    t = d["dispatch"]
    check(s, "worker cwd is the backend checkout",
          t["cwd"].endswith("odontoflow-backend"))
    check(s, "backend worker will load repository instructions",
          t["loads_instructions"] is True)
    check(s, "backend-lane skills resolve locally",
          {"test-driven-development", "postgres-best-practices",
           "verification-before-completion"} <= set(t["local_skills"]))
    check(s, "sales-agent-lane skill resolves locally",
          "odontoflow-engineering" in t["local_skills"])
    check(s, "the lane is named at dispatch", d["skill_lane"] == "backend + sales-agent")

    # Frontend: the router must report, not hide, a repo that loads nothing.
    f = route({
        "activity_id": "FE-X",
        "lifecycle_state": "READY_TO_BUILD",
        "implementation_authorized": True,
        "repo": "odontoflow-frontend",
    })["dispatch"]
    check(s, "frontend worker cwd is the frontend checkout",
          f["cwd"].endswith("odontoflow-frontend"))
    check(s, "frontend instruction gap is reported, not silent",
          (f["loads_instructions"] is True) or bool(f["warning"]))


# ---------------------------------------------------------------- scenario D
def scenario_d() -> None:
    """A simple known fix bypasses unnecessary product planning."""
    s = "D known-fix-bypasses-planning"
    d = route({
        "activity_id": "FIX-typo-in-error-envelope",
        "lifecycle_state": "KNOWN_FIX",
        "repo": "odontoflow-backend",
    })
    check(s, "stays in KNOWN_FIX", d["effective_state"] == "KNOWN_FIX")
    check(s, "implements directly", "Implement" in d["action"])
    check(s, "forbids SPEC / discovery / decomposition ceremony",
          "SPEC" in d["forbidden"] and "discovery" in d["forbidden"]
          and "decompose" in d["forbidden"])
    check(s, "still resolves a real dispatch target",
          d["dispatch"]["cwd"].endswith("odontoflow-backend"))
    # A known fix needs no authorization gate — that gate is for cards.
    check(s, "no owner-authorization stall on a bounded fix",
          d["effective_state"] != "BLOCKED_OWNER_DECISION")


# ---------------------------------------------------------------- scenario E
def scenario_e() -> None:
    """A real product-contract contradiction returns to the owner without
    discarding unaffected completed work."""
    s = "E contradiction-preserves-completed-work"
    d = route({
        "activity_id": "CORE-01",
        "lifecycle_state": "CONTRACT_CONTRADICTION",
        "contradiction": "SPEC says decline is a distinct status; the DB CHECK "
                         "constraint admits only pending/confirmed/expired.",
        "subcards": [
            {"id": "SC-1", "status": "done"},
            {"id": "SC-2", "status": "done"},
            {"id": "SC-3", "status": "todo"},
        ],
    })
    check(s, "returns to the owner", "owner" in d["action"])
    check(s, "preserves completed SubCards",
          d["preserve_completed"] == ["SC-1", "SC-2"])
    check(s, "forbids discarding unaffected work",
          "discard" in d["forbidden"] and "unaffected" in d["forbidden"])
    check(s, "the contradiction itself is carried to the owner",
          "CHECK constraint" in (d["contradiction"] or ""))
    check(s, "does not dispatch while contradicted", "dispatch" not in d)


# ---------------------------------------------------------------- scenario F
def scenario_f() -> None:
    """SubCards continue after approval; unrelated Activity Cards cannot
    auto-start."""
    s = "F subcards-continue-cards-do-not"
    d = route({
        "activity_id": "CORE-01",
        "lifecycle_state": "IN_PROGRESS",
        "implementation_authorized": True,
        "repo": "odontoflow-backend",
        "subcards": [
            {"id": "SC-1", "status": "done",
             "write_ownership": ["tests/test_appointment_proposals.py"]},
            {"id": "SC-2", "status": "in_progress",
             "write_ownership": ["app/scheduling/router.py"]},
            {"id": "SC-3", "status": "todo", "dependencies": ["SC-1"],
             "write_ownership": ["app/scheduling/schemas.py"],
             "model_class": "capable"},
            {"id": "SC-4", "status": "todo", "dependencies": ["SC-1"],
             "write_ownership": ["app/scheduling/router.py"],
             "model_class": "capable"},
            {"id": "SC-5", "status": "todo", "dependencies": ["SC-3"],
             "write_ownership": ["docs/api/openapi.yaml"],
             "model_class": "cheap"},
        ],
    })
    ready = [x["id"] for x in d["dispatchable_subcards"]]
    blocked = {x["id"]: x["reason"] for x in d["blocked_subcards"]}
    check(s, "a dependency-ready SubCard continues", ready == ["SC-3"])
    check(s, "one writer per surface: SC-4 waits on the claimed router.py",
          "SC-4" in blocked and "already claimed" in blocked["SC-4"])
    check(s, "SC-5 waits on its unfinished dependency",
          "SC-5" in blocked and "waiting on SC-3" in blocked["SC-5"])
    check(s, "forbids starting a different Activity Card",
          "different Activity Card" in d["forbidden"])

    # A finished card must not select the next one by itself.
    done = route({"activity_id": "PROJECT-PUBLISH-01", "lifecycle_state": "DONE"})
    check(s, "a DONE card does nothing further", done["action"].startswith("Nothing"))
    check(s, "a DONE card forbids auto-selecting the next activity",
          "auto-select" in done["forbidden"])
    check(s, "a DONE card dispatches nothing", "dispatch" not in done)


# ------------------------------------------------------- live control plane
def live_state() -> None:
    """The real current-activity.yaml parses and routes truthfully."""
    s = "LIVE current-activity.yaml"
    activity = yaml.safe_load(DEFAULT_STATE.read_text())
    d = route(activity)
    check(s, "the live control plane parses and routes",
          d["effective_state"] in ("DONE", "BLOCKED_OWNER_DECISION"))
    check(s, "it starts nothing on its own", "dispatch" not in d)
    check(s, "it surfaces the pending CORE-01 owner decision",
          d.get("owner_decision", {}).get("activity_id") == "CORE-01")
    check(s, "the lifecycle contract is present in the canonical file",
          "lifecycle_contract" in activity)
    check(s, "the planning entry point Claude Code actually loads exists",
          (REPO_ROOT / "CLAUDE.md").is_file())


def main() -> int:
    for fn in (scenario_a, scenario_b, scenario_c, scenario_d,
               scenario_e, scenario_f, live_state):
        fn()
    for line in PASSES:
        print(f"PASS  {line}")
    for line in FAILURES:
        print(f"FAIL  {line}")
    print(f"\n{len(PASSES)} passed, {len(FAILURES)} failed")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
