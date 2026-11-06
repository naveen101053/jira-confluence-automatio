"""Tests for jira_report.calculations.completed_work (see detect-completed-work.agent.md)."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from jira_report.calculations.completed_work import detect_completed_stories

IST = ZoneInfo("Asia/Kolkata")
FIXTURE_PATH = Path(__file__).parent.parent / "fixtures" / "completed_work_stories.json"
WINDOW_START = datetime(2026, 11, 2, 0, 0, 0, tzinfo=IST)
WINDOW_END = datetime(2026, 11, 7, 0, 0, 0, tzinfo=IST)
COMPLETED_STATUSES = {"Done"}


@pytest.fixture
def stories():
    return json.loads(FIXTURE_PATH.read_text())


def _by_key(result, key):
    return next(c for c in result["completed"] if c["key"] == key)


def test_straightforward_completion_in_window(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    entry = _by_key(result, "TCL-101")
    assert entry["assignee"] == "Asha Rao"
    assert entry["completed_at"] == "2026-11-03T15:45:00+05:30"


def test_window_start_boundary_is_inclusive(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    entry = _by_key(result, "TCL-103")
    assert entry["completed_at"] == "2026-11-02T00:00:00+05:30"
    assert entry["assignee"] is None


def test_window_end_boundary_is_exclusive(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    keys = [c["key"] for c in result["completed"]]
    assert "TCL-107" not in keys


def test_completed_before_window_excluded(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    keys = [c["key"] for c in result["completed"]]
    assert "TCL-104" not in keys


def test_unrelated_status_changes_excluded(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    keys = [c["key"] for c in result["completed"]]
    assert "TCL-105" not in keys
    assert "TCL-111" not in keys


def test_enter_leave_reenter_counted_once_with_earliest_entry(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    matches = [c for c in result["completed"] if c["key"] == "TCL-106"]
    assert len(matches) == 1
    entry = matches[0]
    assert entry["completed_at"] == "2026-11-02T10:00:00+05:30"
    assert len(entry["status_history"]) == 3


def test_missing_changelog_flagged_as_caveat_not_counted(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    keys = [c["key"] for c in result["completed"]]
    assert "TCL-108" not in keys
    assert any("TCL-108" in c for c in result["caveats"])


def test_out_of_scope_label_and_issuetype_excluded_without_caveat(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    keys = [c["key"] for c in result["completed"]]
    assert "TCL-109" not in keys
    assert "TCL-110" not in keys
    assert not any("TCL-109" in c or "TCL-110" in c for c in result["caveats"])


def test_non_monday_run_date_window_is_passed_through_unchanged(stories):
    # Window is computed elsewhere (reporting-window step); this step only consumes it.
    run_date_window_start = datetime(2026, 11, 2, 0, 0, 0, tzinfo=IST)
    run_date_window_end = datetime(2026, 11, 7, 0, 0, 0, tzinfo=IST)
    result = detect_completed_stories(
        stories, run_date_window_start, run_date_window_end, COMPLETED_STATUSES
    )
    assert result["window"] == {
        "start": "2026-11-02T00:00:00+05:30",
        "end": "2026-11-07T00:00:00+05:30",
    }


def test_sorted_by_completed_at_then_key(stories):
    result = detect_completed_stories(stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES)
    keys = [c["key"] for c in result["completed"]]
    assert keys == ["TCL-103", "TCL-106", "TCL-101", "TCL-102"]
