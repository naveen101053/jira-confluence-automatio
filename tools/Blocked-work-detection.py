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
