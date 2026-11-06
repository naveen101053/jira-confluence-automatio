"""Completed-work detection (detect-completed-work.agent.md).

Pure function: stories + window + config in, structured result out.
No Jira calls here, so it can be tested with mocked data.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


def _to_ist(timestamp: str) -> datetime:
    """Parse an ISO-8601 timestamp (any offset) and convert to IST."""
    return datetime.fromisoformat(timestamp).astimezone(IST)


def _in_scope(story: dict[str, Any], project_key: str) -> bool:
    key = story.get("key", "")
    fields = story.get("fields", {})
    issuetype = fields.get("issuetype", {}).get("name")
    labels = fields.get("labels", [])
    return (
        key.startswith(f"{project_key}-")
        and issuetype == "Story"
        and "Ready for deployment" in labels
    )


def detect_completed_stories(
    stories: list[dict[str, Any]],
    window_start: datetime,
    window_end: datetime,
    completed_statuses: set[str],
    project_key: str = "TCL",
) -> dict[str, Any]:
    """Detect stories that entered a completed status within [window_start, window_end)."""
    completed: list[dict[str, Any]] = []
    caveats: list[str] = []

    for story in stories:
        if not _in_scope(story, project_key):
            continue

        key = story["key"]
        histories = story.get("changelog", {}).get("histories")
        if not histories:
            caveats.append(
                f"{key}: in-scope (Story, labeled Ready for deployment) but changelog "
                "missing/unreadable — excluded from count, not assumed zero."
            )
            continue

        transitions: list[tuple[datetime, str, str]] = []
        for history in histories:
            for item in history.get("items", []):
                if item.get("field") != "status":
                    continue
                transitions.append(
                    (_to_ist(history["created"]), item.get("fromString"), item.get("toString"))
                )
        transitions.sort(key=lambda t: t[0])

        in_window = [t for t in transitions if window_start <= t[0] < window_end]
        completed_entries = [
            t for t in in_window if t[2] in completed_statuses and t[1] not in completed_statuses
        ]
        if not completed_entries:
            continue

        completed_at = completed_entries[0][0]
        fields = story.get("fields", {})
        assignee = fields.get("assignee")
        completed.append(
            {
                "key": key,
                "title": fields.get("summary"),
                "assignee": assignee.get("displayName") if assignee else None,
                "completed_at": completed_at.isoformat(),
                "current_status": fields.get("status", {}).get("name"),
                "status_history": [
                    {"at": t[0].isoformat(), "from": t[1], "to": t[2]} for t in in_window
                ],
            }
        )

    completed.sort(key=lambda c: (c["completed_at"], c["key"]))

    return {
        "window": {"start": window_start.isoformat(), "end": window_end.isoformat()},
        "completed": completed,
        "caveats": caveats,
    }
