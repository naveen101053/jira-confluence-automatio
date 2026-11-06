# Instructions Catalog

Each entry below is an instruction file with a one-line description. Optional sub-fields after `+`:
- **Keywords** — trigger words/phrases: if user's request matches, load this instruction.
- **Target** — file glob pattern: if current file or context matches, consider this instruction relevant.
- **Exceptions** — edge cases or clarifications that don't fit in the one-liner.

---

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — create, update, and install instructions, skills, and IDE wrappers.
  + Keywords: create instruction, update instruction, new instruction, skill, prompt file, wrapper, catalog, main.agent.md
  + Target: `instructions/**`, `.github/prompts/**`, `.github/copilot-instructions.md`

- [`./instructions/calculate-compound-interest.agent.md`](./calculate-compound-interest.agent.md) — calculate compound interest with `tools/compound_interest.py`; defines when to use it, how to invoke it, and how to present results.
  + Keywords: compound interest, interest earned, future value, final amount, principal, annual rate, compounding, compounded monthly
  + Target: `tools/compound_interest.py`
  + Exceptions: does not cover simple interest, loan amortization, or recurring contributions.

- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — generate a concise weekly status report (Accomplishments, Blockers, Next Week) in Markdown.
  + Keywords: status report, weekly report, weekly status, team update, progress report
  + Target: `reports/weekly-status-*.md`
  + Exceptions: Jira-based report format lives in `reports/instructions.md` and `reports/template.md`; use only when Jira data is available.

- [`./instructions/detect-completed-work.agent.md`](./detect-completed-work.agent.md) — detect stories that entered a completed status in the reporting window from Jira status history; defines input, steps, output, and constraints.
  + Keywords: completed work, completed stories, detect completed, status history, changelog, deduplicate, reporting window
  + Target: `jira_report/calculations/**`, `tests/**/test_completed*`
  + Exceptions: does not cover assignee grouping, velocity, or Jira retrieval.

- [`./instructions/Blocked-work-detection.agent.md`](./Blocked-work-detection.agent.md) — count blocked stories from a Jira issues JSON export with `tools/Blocked-work-detection.py`; defines when to use it, how to invoke it, and how to present results.
  + Keywords: blocked work, blocked stories, blocked items, count blocked, blocked count, blocker, blocked rule
  + Target: `tools/Blocked-work-detection.py`, `tests/fixtures/blocked_work_stories.json`
  + Exceptions: does not extract blocker reason, assignee, dates, or Jira links; blocked rule (status/label/field) must be supplied since it is an open config item.

