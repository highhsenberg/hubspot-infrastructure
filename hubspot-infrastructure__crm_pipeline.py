#!/usr/bin/env python3
"""
HubSpot CRM Infrastructure (lite)
------------------------------------
A small, readable model of the three things most CRM infrastructure work
actually is: lifecycle stage management, workflow automation, and funnel
reporting.

1. Lifecycle stages -- each contact's stage is recomputed from an activity
   score against a fixed set of thresholds (subscriber -> lead -> mql -> sql
   -> opportunity -> customer).
2. Workflow automation -- whenever a contact's stage changes, a matching
   action fires (assign an owner, create a task, notify a team, etc.).
3. Funnel reporting -- a snapshot of how many contacts currently sit in
   each lifecycle stage.

Usage:
    python crm_pipeline.py --input contacts.csv
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from typing import Any, Dict, List

STAGE_ORDER = ["subscriber", "lead", "mql", "sql", "opportunity", "customer"]

STAGE_THRESHOLDS = [
    (90, "customer"),
    (75, "opportunity"),
    (60, "sql"),
    (40, "mql"),
    (20, "lead"),
    (0, "subscriber"),
]

WORKFLOW_ACTIONS = {
    "lead": "Add welcome email sequence",
    "mql": "Notify marketing, add to nurture-to-sales handoff list",
    "sql": "Assign to AE, create task 'first call within 24h'",
    "opportunity": "Create deal record, notify sales manager",
    "customer": "Trigger onboarding sequence, notify CS team",
}

STALL_THRESHOLD_DAYS = 90


@dataclass
class Contact:
    name: str
    email: str
    old_stage: str
    new_stage: str
    activity_score: int
    last_activity_days_ago: int
    action: str
    stalled: bool


def load_contacts(path: str) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_stage(activity_score: int) -> str:
    for threshold, stage in STAGE_THRESHOLDS:
        if activity_score >= threshold:
            return stage
    return "subscriber"


def process_contact(row: Dict[str, Any]) -> Contact:
    score = int(row["activity_score"])
    last_activity = int(row["last_activity_days_ago"])
    old_stage = row["current_stage"]
    new_stage = compute_stage(score)

    action = ""
    if new_stage != old_stage:
        action = WORKFLOW_ACTIONS.get(new_stage, "")

    return Contact(
        name=row["name"],
        email=row["email"],
        old_stage=old_stage,
        new_stage=new_stage,
        activity_score=score,
        last_activity_days_ago=last_activity,
        action=action,
        stalled=last_activity > STALL_THRESHOLD_DAYS,
    )


def stage_distribution_report(contacts: List[Contact]) -> Dict[str, Dict[str, Any]]:
    total = len(contacts)
    counts = {stage: 0 for stage in STAGE_ORDER}
    for c in contacts:
        counts[c.new_stage] += 1
    return {
        stage: {"count": counts[stage], "pct": round(100 * counts[stage] / total, 1) if total else 0.0}
        for stage in STAGE_ORDER
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="HubSpot CRM Infrastructure (lite)")
    parser.add_argument("--input", default="contacts.csv")
    args = parser.parse_args()

    rows = load_contacts(args.input)
    contacts = [process_contact(row) for row in rows]

    print("=== Lifecycle stage transitions ===\n")
    for c in contacts:
        direction = "unchanged"
        if STAGE_ORDER.index(c.new_stage) > STAGE_ORDER.index(c.old_stage):
            direction = "advanced"
        elif STAGE_ORDER.index(c.new_stage) < STAGE_ORDER.index(c.old_stage):
            direction = "regressed"

        print(f"{c.name} <{c.email}>")
        print(f"  {c.old_stage} -> {c.new_stage} ({direction}, score={c.activity_score})")
        if c.stalled:
            print(f"  ! Stalled - no activity in {c.last_activity_days_ago} days")
        if c.action:
            print(f"  Workflow triggered: {c.action}")
        print()

    print("=== Stage distribution ===\n")
    report = stage_distribution_report(contacts)
    for stage in STAGE_ORDER:
        info = report[stage]
        print(f"  {stage:12} {info['count']} contacts ({info['pct']}%)")


if __name__ == "__main__":
    main()
