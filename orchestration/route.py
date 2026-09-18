#!/usr/bin/env python3
"""Read-only planning entry-point router.

Answers one question: given the current activity state, what does this session
do next? It never dispatches, never writes, and never contacts a model. It is
the executable form of the routing table in ../CLAUDE.md; if the two disagree,
CLAUDE.md wins and this file is the bug.

    python3 orchestration/route.py                 # current activity
    python3 orchestration/route.py --state FILE    # any activity file
    python3 orchestration/route.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = REPO_ROOT.parent
DEFAULT_STATE = REPO_ROOT / "orchestration" / "current-activity.yaml"

# state -> (what this session does, what it must not do)
ROUTES = {
    "NEEDS_PRODUCT_DISCOVERY": (
        "Run product discovery as Opus (grill-me is disabled here: ask the nine "
        "questions directly), produce a SPEC + product delivery plan, stop for "
        "owner approval.",
        "Do not write code. Do not dispatch a writer.",
    ),
    "SPEC_APPROVED": (
        "Run targeted functional validation, then technical design. Emit an "
        "Activity Card with dependency-aware SubCards.",
        "Do not re-run discovery. Do not author a second SPEC.",
    ),
    "READY_TO_BUILD": (
        "Dispatch one authorized writer per write surface and work the "
        "dependency-ready SubCards to completion.",
        "Do not produce another validation report. Do not re-validate what the "
        "card already records.",
    ),
    "IN_PROGRESS": (
        "Continue this card's remaining dependency-ready SubCards.",
        "Do not start a different Activity Card.",
    ),
    "NEEDS_VERIFICATION": (
        "Verify against acceptance, then write the self-contained handoff.",
        "Do not mark DONE without evidence.",
    ),
    "KNOWN_FIX": (
        "Implement the bounded fix directly.",
        "Do not author a SPEC, run discovery, or decompose into SubCards.",
    ),
    "BLOCKED_OWNER_DECISION": (
        "Present the decision, the options and the trade-offs, then stop.",
        "Do not decide it on the owner's behalf.",
    ),
    "CONTRACT_CONTRADICTION": (
        "Return to the owner with the cited contradiction. Preserve every "
        "completed SubCard the contradiction does not touch.",
        "Do not discard or re-open unaffected completed work.",
    ),
    "DONE": (
        "Nothing. Report status and wait for an explicit owner choice.",
        "Do not auto-select the next activity.",
    ),
}

REPO_PATHS = {
    "odontoflow-planning": REPO_ROOT,
    "odontoflow-backend": WORKSPACE_ROOT / "odontoflow-backend",
    "odontoflow-frontend": WORKSPACE_ROOT / "odontoflow-frontend",
}


def effective_state(activity: dict) -> tuple[str, list[str]]:
    """Enumerated state after the lifecycle_contract rules are applied."""
    notes: list[str] = []
    state = activity.get("lifecycle_state")

    if not state:
        notes.append(
            "no lifecycle_state field: treating as NEEDS_PRODUCT_DISCOVERY"
        )
        return "NEEDS_PRODUCT_DISCOVERY", notes
    if state not in ROUTES:
        notes.append(
            f"unknown lifecycle_state {state!r}: treating as "
            "NEEDS_PRODUCT_DISCOVERY"
        )
        return "NEEDS_PRODUCT_DISCOVERY", notes

    # Authorization gate: validated is not the same as authorized.
    if state in ("READY_TO_BUILD", "IN_PROGRESS"):
        if not activity.get("implementation_authorized"):
            notes.append(
                f"{state} without implementation_authorized: true -> "
                "BLOCKED_OWNER_DECISION"
            )
            return "BLOCKED_OWNER_DECISION", notes

    # PASS is not DONE. A validation report never closes an authorized card.
    result = str((activity.get("validation") or {}).get("result") or "")
    if state == "READY_TO_BUILD" and result.upper().startswith("PASS"):
        notes.append(
            "validation.result is PASS and the card is authorized: PASS is not "
            "DONE — implement against the existing report, do not rewrite it"
        )

    return state, notes


def ready_subcards(activity: dict) -> tuple[list[dict], list[dict]]:
    """(dispatchable, blocked) SubCards under dependency + write-ownership rules."""
    subcards = activity.get("subcards") or []
    done = {s.get("id") for s in subcards if s.get("status") == "done"}
    in_flight_paths: set[str] = set()
    for s in subcards:
        if s.get("status") == "in_progress":
            in_flight_paths.update(s.get("write_ownership") or [])

    dispatchable, blocked = [], []
    claimed = set(in_flight_paths)
    for s in subcards:
        if s.get("status") not in (None, "todo", "ready"):
            continue
        missing = [d for d in (s.get("dependencies") or []) if d not in done]
        if missing:
            blocked.append({**s, "_reason": f"waiting on {', '.join(missing)}"})
            continue
        overlap = sorted(set(s.get("write_ownership") or []) & claimed)
        if overlap:
            blocked.append(
                {**s, "_reason": f"write surface already claimed: {', '.join(overlap)}"}
            )
            continue
        dispatchable.append(s)
        claimed.update(s.get("write_ownership") or [])  # one writer per surface
    return dispatchable, blocked


def worker_target(repo: str) -> dict:
    """Where a worker for this repo runs, and whether it will load instructions."""
    path = REPO_PATHS.get(repo)
    if path is None:
        return {"repo": repo, "error": "unknown repo"}
    loader = path / "CLAUDE.md"
    skills = path / ".claude" / "skills"
    return {
        "repo": repo,
        "cwd": str(path),
        "loads_instructions": loader.is_file(),
        "loader": str(loader),
        "local_skills": sorted(p.name for p in skills.iterdir()) if skills.is_dir() else [],
        "warning": None
        if loader.is_file()
        else f"{loader} missing: a worker here loads NO repository instructions",
    }


def route(activity: dict) -> dict:
    state, notes = effective_state(activity)
    action, forbidden = ROUTES[state]
    out = {
        "activity_id": activity.get("activity_id"),
        "declared_state": activity.get("lifecycle_state"),
        "effective_state": state,
        "action": action,
        "forbidden": forbidden,
        "notes": notes,
    }

    if state in ("READY_TO_BUILD", "IN_PROGRESS", "KNOWN_FIX"):
        repo = activity.get("repo", "odontoflow-planning")
        out["dispatch"] = worker_target(repo)
        out["skill_lane"] = activity.get("skill_lane")
        dispatchable, blocked = ready_subcards(activity)
        if dispatchable or blocked:
            out["dispatchable_subcards"] = [
                {"id": s.get("id"), "model_class": s.get("model_class")}
                for s in dispatchable
            ]
            out["blocked_subcards"] = [
                {"id": s.get("id"), "reason": s.get("_reason")} for s in blocked
            ]

    # A finished activity still has to surface the pending owner choice, or the
    # control plane goes quiet about work that is already validated and waiting.
    if state in ("BLOCKED_OWNER_DECISION", "DONE"):
        cand = activity.get("next_activity_candidate")
        if cand:
            out["owner_decision"] = {
                "activity_id": cand.get("activity_id"),
                "question": cand.get("owner_decision_required"),
                "would_become": cand.get("would_become"),
            }
        elif activity.get("owner_decision_required"):
            out["owner_decision"] = {
                "activity_id": activity.get("activity_id"),
                "question": activity.get("owner_decision_required"),
            }

    if state == "CONTRACT_CONTRADICTION":
        preserved = [
            s.get("id")
            for s in (activity.get("subcards") or [])
            if s.get("status") == "done"
        ]
        out["preserve_completed"] = preserved
        out["contradiction"] = activity.get("contradiction")

    return out


def render(d: dict) -> str:
    lines = [
        f"activity        : {d['activity_id']}",
        f"declared state  : {d['declared_state']}",
        f"effective state : {d['effective_state']}",
        "",
        f"DO   : {d['action']}",
        f"DON'T: {d['forbidden']}",
    ]
    for n in d["notes"]:
        lines.append(f"note : {n}")
    if "skill_lane" in d and d["skill_lane"]:
        lines.append(f"lane : {d['skill_lane']}")
    if "dispatch" in d:
        t = d["dispatch"]
        lines += ["", f"dispatch repo   : {t.get('repo')}", f"worker cwd      : {t.get('cwd')}"]
        lines.append(f"loads instr.    : {t.get('loads_instructions')}")
        if t.get("local_skills"):
            lines.append(f"local skills    : {', '.join(t['local_skills'])}")
        if t.get("warning"):
            lines.append(f"WARNING         : {t['warning']}")
    if d.get("dispatchable_subcards") is not None:
        lines.append("")
        for s in d["dispatchable_subcards"]:
            lines.append(f"  dispatch now  : {s['id']} ({s.get('model_class')})")
        for s in d["blocked_subcards"]:
            lines.append(f"  blocked       : {s['id']} — {s['reason']}")
    if "owner_decision" in d:
        o = d["owner_decision"]
        lines += ["", f"OWNER DECISION  : {o.get('activity_id')}", f"  {o.get('question')}"]
    if "preserve_completed" in d:
        lines += ["", f"preserve done   : {', '.join(d['preserve_completed']) or '(none)'}"]
        if d.get("contradiction"):
            lines.append(f"contradiction   : {d['contradiction']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", type=Path, default=DEFAULT_STATE)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.state.is_file():
        print(f"no activity state at {args.state}", file=sys.stderr)
        return 2
    activity = yaml.safe_load(args.state.read_text()) or {}
    decision = route(activity)
    print(json.dumps(decision, indent=2) if args.json else render(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
