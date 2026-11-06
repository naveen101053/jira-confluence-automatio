"""Multi-project tests for completed_work detection (CWB, ABC fixtures + cross-project isolation)."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from jira_report.calculations.completed_work import detect_completed_stories

IST = ZoneInfo("Asia/Kolkata")
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
WINDOW_START = datetime(2026, 11, 2, 0, 0, 0, tzinfo=IST)
WINDOW_END = datetime(2026, 11, 7, 0, 0, 0, tzinfo=IST)
COMPLETED_STATUSES = {"Done"}


def _load(name):
    return json.loads((FIXTURES_DIR / name).read_text())


def _keys(result):
    return [c["key"] for c in result["completed"]]


def test_cwb_completed_stories():
    stories = _load("completed_work_stories_cwb.json")
    result = detect_completed_stories(
        stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES, project_key="CWB"
    )
    assert _keys(result) == ["CWB-203", "CWB-201"]
    assert any("CWB-204" in c for c in result["caveats"])


def test_abc_completed_stories():
    stories = _load("completed_work_stories_abc.json")
    result = detect_completed_stories(
        stories, WINDOW_START, WINDOW_END, COMPLETED_STATUSES, project_key="ABC"
    )
    assert _keys(result) == ["ABC-304", "ABC-306", "ABC-301"]
    assert any("ABC-305" in c for c in result["caveats"])


def test_project_key_filters_out_other_projects():
    combined = (
        _load("completed_work_stories.json")
        + _load("completed_work_stories_cwb.json")
        + _load("completed_work_stories_abc.json")
    )
    result = detect_completed_stories(
        combined, WINDOW_START, WINDOW_END, COMPLETED_STATUSES, project_key="ABC"
    )
    assert all(key.startswith("ABC-") for key in _keys(result))
    assert _keys(result) == ["ABC-304", "ABC-306", "ABC-301"]
