# Module 12 Completion Report

## Instruction File
- Filename: Blocked-work-detection.agent.md

```markdown
- Use `tools/Blocked-work-detection.py` when asked to count, total, or report the number of blocked stories/work items from a Jira issues export. Source rules: `project_spec.md` FR-1 and §5 "Blocked work"; backlog: "Blocked-work detection".
  + Do not count by hand — always run the tool.
  + Does not extract blocker reason, assignee, dates, or Jira link — only the count and optional keys.
- Inputs:
  + `stories_file` — path to a JSON file with a list of Jira issues (same shape as `detect-completed-work.agent.md` input: `key`, `fields.issuetype`, `fields.labels`, `fields.status`).
  + Blocked rule — how Jira marks a story as blocked: status name, label, or field. This is an open config item (`backlog.md` Phase 1).
  + If the user supplies a different rule (label or field, or a status other than `Blocked`), use it via the matching flag.
  + If no blocked rule is supplied, do not ask the user — treat status `Blocked` as confirmed ("Yes") and run with `--blocked-status Blocked`.
- If no real Jira data is supplied or reachable, use the sample fixture `tests/fixtures/blocked_work_stories.json` and say so.
- Invoke:
  + `python tools/Blocked-work-detection.py <stories_file> [--project-key KEY] [--blocked-status NAME] [--blocked-label NAME] [--blocked-field NAME] [--list]`
  + `--blocked-status`, `--blocked-label`, `--blocked-field` are repeatable; a story is blocked if any of them matches.
  + `--blocked-field` matches when `fields.<NAME>` is non-empty.
  + `--project-key` defaults to `TCL`.
  + `--list` also prints the blocked story keys.
  + Example: `python tools/Blocked-work-detection.py tests/fixtures/blocked_work_stories.json --blocked-status Blocked --blocked-label Blocked --list`
  + Use `python tools/Blocked-work-detection.py -h` to show usage.
- Scope applied by the tool (do not pre-filter): project `TCL`, issue type `Story`, exact label `Ready for deployment`. Each story key is counted once.
- If the rule was defaulted to status `Blocked` (not supplied by the user), state this assumption in the answer; never ask for confirmation.
- Tool output format:
  + `Total blocked work items: 3`
  + With `--list`: one indented story key per line.
- If the tool exits with an error (unreadable file, invalid JSON, not a list), fix the input and rerun — do not fall back to manual counting.
- Present results:
  + State the blocked rule, project key, and source file used.
  + Show **Total blocked work items** in bold, as reported by the tool.
  + List story keys only when `--list` was used or the user asked for them.
  + Keep the answer concise — no restating of the tool's raw output beyond the count and keys.
```

## Script File
- Filename: Blocked-work-detection.py
- Language: Python

```python
#!/usr/bin/env python3
"""Count currently blocked work items from a Jira issues JSON export.

Scope (project_spec.md): project `TCL`, issue type `Story`, exact label `Ready for deployment`.
A story is blocked when its current status, a label, or a field matches the configured rule.
The blocked rule is still an open config item, so it is passed in, never hard-coded.
"""

import argparse
import json
import sys

DEFAULT_PROJECT_KEY = "TCL"
SCOPE_LABEL = "Ready for deployment"


def in_scope(story: dict, project_key: str) -> bool:
    fields = story.get("fields") or {}
    return (
        str(story.get("key", "")).startswith(f"{project_key}-")
        and (fields.get("issuetype") or {}).get("name") == "Story"
        and SCOPE_LABEL in (fields.get("labels") or [])
    )


def is_blocked(story: dict, statuses: set, labels: set, field_names: set) -> bool:
    fields = story.get("fields") or {}
    if (fields.get("status") or {}).get("name") in statuses:
        return True
    if labels & set(fields.get("labels") or []):
        return True
    return any(fields.get(name) for name in field_names)


def count_blocked(stories: list, project_key: str, statuses: set, labels: set, field_names: set):
    """Return (blocked_count, sorted blocked keys). Each story key is counted once."""
    keys = {
        story["key"]
        for story in stories
        if in_scope(story, project_key) and is_blocked(story, statuses, labels, field_names)
    }
    return len(keys), sorted(keys)


def main() -> None:
    parser = argparse.ArgumentParser(description="Count blocked Jira stories.")
    parser.add_argument("stories_file", help="JSON file containing a list of Jira issues")
    parser.add_argument("--project-key", default=DEFAULT_PROJECT_KEY, help="default: TCL")
    parser.add_argument("--blocked-status", action="append", default=[], help="status name treated as blocked (repeatable)")
    parser.add_argument("--blocked-label", action="append", default=[], help="label treated as blocked (repeatable)")
    parser.add_argument("--blocked-field", action="append", default=[], help="fields key whose non-empty value means blocked (repeatable)")
    parser.add_argument("--list", action="store_true", help="also print the blocked story keys")
    args = parser.parse_args()

    statuses, labels, field_names = set(args.blocked_status), set(args.blocked_label), set(args.blocked_field)
    if not (statuses or labels or field_names):
        statuses = {"Blocked"}
        print("Note: no blocked rule given, assuming status 'Blocked'.", file=sys.stderr)

    try:
        with open(args.stories_file, encoding="utf-8") as handle:
            stories = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        sys.exit(f"Error: cannot read stories file: {error}")
    if not isinstance(stories, list):
        sys.exit("Error: stories file must contain a JSON list of issues.")

    total, keys = count_blocked(stories, args.project_key, statuses, labels, field_names)
    print(f"Total blocked work items: {total}")
    if args.list:
        for key in keys:
            print(f"  {key}")


if __name__ == "__main__":
    main()
```

## Script Execution Output
```
> python tools/Blocked-work-detection.py --help
usage: Blocked-work-detection.py [-h] [--project-key PROJECT_KEY]
                                 [--blocked-status BLOCKED_STATUS]
                                 [--blocked-label BLOCKED_LABEL]
                                 [--blocked-field BLOCKED_FIELD] [--list]
                                 stories_file

Count blocked Jira stories.

positional arguments:
  stories_file          JSON file containing a list of Jira issues

options:
  -h, --help            show this help message and exit
  --project-key PROJECT_KEY
                        default: TCL
  --blocked-status BLOCKED_STATUS
                        status name treated as blocked (repeatable)
  --blocked-label BLOCKED_LABEL
                        label treated as blocked (repeatable)
  --blocked-field BLOCKED_FIELD
                        fields key whose non-empty value means blocked
                        (repeatable)
  --list                also print the blocked story keys
```
