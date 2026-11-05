- Purpose: find stories that entered a configured completed status during the reporting window. Source rules: `project_spec.md` FR-1 and §5 "Completed work"; backlog: "Completed-work detection".
- Use when asked to detect, count, or list completed stories for a weekly report. Aggregation by assignee is a separate step, see "Output format".
- Input format:
  + `stories` — list of Jira issues with changelog, one object per issue:
    ```json
    {
      "key": "TCL-101",
      "fields": {
        "summary": "Title",
        "issuetype": {"name": "Story"},
        "labels": ["Ready for deployment", "other"],
        "status": {"name": "In Progress"},
        "assignee": {"displayName": "Name"} 
      },
      "changelog": {"histories": [
        {"created": "2026-11-03T10:15:00.000+0000",
         "items": [{"field": "status", "fromString": "In Progress", "toString": "Done"}]}
      ]}
    }
    ```
  + `fields.assignee` is `null` when unassigned.
  + `window_start`, `window_end` — IST datetimes from the reporting-window function. Half-open interval `[window_start, window_end)`, Monday 00:00 to Saturday 00:00.
  + `completed_statuses` — set of status names from config. Never hard-code status names.
  + `project_key` — from config, default `TCL`.
- Processing steps:
  + Filter scope first: project `project_key`, issue type `Story`, labels contain exactly `Ready for deployment` (other labels allowed, no partial or case-insensitive match).
  + Collect status transitions: from `changelog.histories`, keep items with `field == "status"`, each with its `created` timestamp.
  + Convert every `created` timestamp to IST (`Asia/Kolkata`) before any comparison. Parse the offset, do not assume UTC.
  + Sort transitions by timestamp ascending.
  + Mark a transition as completed entry when `toString` is in `completed_statuses` and `fromString` is not.
  + Keep completed entries where `window_start <= timestamp < window_end`.
  + Count the story once if at least one completed entry remains. Do not use current `fields.status`.
  + Record `completed_at` as the earliest in-window completed entry.
  + Keep in-window status transitions as `status_history` so later leave or re-entry is visible.
  + Skip stories with no qualifying entry: completed before the window, completed after the window, or only unrelated status changes.
- Output format:
  + Return a structured result, not prose:
    ```json
    {
      "window": {"start": "2026-11-02T00:00:00+05:30", "end": "2026-11-07T00:00:00+05:30"},
      "completed": [
        {"key": "TCL-101", "title": "Title", "assignee": "Name or null",
         "completed_at": "2026-11-03T15:45:00+05:30",
         "current_status": "In Progress",
         "status_history": [{"at": "2026-11-03T15:45:00+05:30", "from": "In Progress", "to": "Done"}]}
      ],
      "caveats": []
    }
    ```
  + One entry per story, sorted by `completed_at` then `key`.
  + Timestamps in ISO 8601 with `+05:30` offset.
  + Use `null` for missing assignee. Group and total in the assignee aggregation step, where `null` becomes the explicit `Unassigned` bucket.
  + Add a `caveats` line for each in-scope story with missing or unreadable changelog, naming the story key. Do not count it as completed or as zero.
- Constraints:
  + Count a story at most once, even if it entered and left completed status several times in the window.
  + A move between two completed statuses is not an entry.
  + Use status-change history only. Current status alone never qualifies a story.
  + Window is half-open. A transition at Saturday 00:00:00 IST is excluded, Monday 00:00:00 IST is included.
  + Do not fabricate missing values. Missing changelog means flag it, never default to `0`.
  + Do not log API tokens or unnecessary issue content.
  + Keep detection pure: no Jira calls inside it, input in, result out, so it can be tested with mocked data.
  + Verify with tests for: first-day and last-day boundaries, Saturday 00:00 exclusion, enter/leave/re-enter in window, completed before window, non-Monday run date, unrelated status changes, missing changelog.
  + Open configuration items that affect this step: completed status names and whether to use all `TCL` stories or only `Ready for deployment` ones (see `backlog.md` Phase 1).
