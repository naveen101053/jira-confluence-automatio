- Use `tools/Blocked-work-detection.py` when asked to count, total, or report the number of blocked stories/work items from a Jira issues export. Source rules: `project_spec.md` FR-1 and §5 "Blocked work"; backlog: "Blocked-work detection".
  + Do not count by hand — always run the tool.
  + Does not extract blocker reason, assignee, dates, or Jira link — only the count and optional keys.
- Required inputs (ask the user if missing, do not guess):
  + `stories_file` — path to a JSON file with a list of Jira issues (same shape as `detect-completed-work.agent.md` input: `key`, `fields.issuetype`, `fields.labels`, `fields.status`).
  + Blocked rule — how Jira marks a story as blocked: status name, label, or field. This is an open config item (`backlog.md` Phase 1); never hard-code it.
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
- If no blocked rule is passed, the tool assumes status `Blocked` and prints a note to stderr — state this assumption in the answer.
- Tool output format:
  + `Total blocked work items: 3`
  + With `--list`: one indented story key per line.
- If the tool exits with an error (unreadable file, invalid JSON, not a list), fix the input and rerun — do not fall back to manual counting.
- Present results:
  + State the blocked rule, project key, and source file used.
  + Show **Total blocked work items** in bold, as reported by the tool.
  + List story keys only when `--list` was used or the user asked for them.
  + Keep the answer concise — no restating of the tool's raw output beyond the count and keys.
