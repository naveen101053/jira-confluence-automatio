# Implementation Backlog — Weekly Jira Status Report Generator

Source: [project_spec.md](project_spec.md)

Decisions baked into this backlog:
- MVP = weekly completed + blocked report first; velocity/forecast and defect flagging follow once the base report pipeline works.
- "Core Features" = calculations + Markdown rendering built and tested against **mocked/sample** Jira data (no live API calls).
- "Integration" = wiring the real Jira Cloud REST/Agile APIs, CLI, and the Windows scheduler.
- Python 3.12, `venv` + `pip` (`requirements.txt`).
- Scheduler: Windows Task Scheduler.
- Testing includes a Jira sandbox/test project for real-API verification, in addition to mocked tests.
- Tasks are kept fine-grained (~1–4 hrs each).

---

## Phase 1: Setup

### Open configuration items (spec §7) — resolve before/alongside implementation
- [ ] Confirm Jira site URL, service account/auth method (API token vs OAuth), and board ID(s) — [#1](https://github.com/naveen101053/jira-confluence-automatio/issues/1)
- [ ] Confirm exact Jira field identifier (custom field ID) for story points
- [ ] Confirm status names/categories that count as "completed/resolved"
- [ ] Confirm how blocked stories are identified (status, flag field, or label) and where blocker reason is stored
- [ ] Confirm which issue types count as defects and the Priority value/name corresponding to "1"
- [ ] Confirm quarter calendar and quarter-end date source (config value vs Jira field)
- [ ] Confirm whether velocity uses all `TCL` Stories or only `Ready for deployment`-labeled Stories
- [ ] Confirm missed-run behavior for the Windows Task Scheduler job (e.g., run on next startup vs skip)
- [ ] Record all confirmed values in a config reference doc/table for future maintainers

### Project & environment scaffolding
- [ ] Create Python 3.12 virtual environment (`.venv`) for the new app, separate from the existing calculator
- [ ] Create `requirements.txt` with initial dependencies (e.g., `requests`, `pyyaml`/`python-dotenv`, `pytz`/`zoneinfo` usage, test libs)
- [ ] Create package folder structure: `jira_report/` with submodules `jira_client/`, `calculations/`, `rendering/`, `cli.py`
- [ ] Add `__init__.py` files and confirm package imports resolve
- [ ] Add `.gitignore` entries for local config/secrets files and `.venv`
- [ ] Create `config.example.yaml` (or `.env.example`) template listing all required configuration keys from §7, without real values
- [ ] Implement config loader module that reads local gitignored config file / env vars and validates required keys are present
- [ ] Set up basic logging configuration (console + file handler), ensuring no tokens/secrets are logged
- [ ] Add a `reports/` output path setting to config (default `reports/`)
- [ ] Verify `python -m jira_report.cli --help` (or equivalent) runs without error on a fresh checkout

---

## Phase 2: Core Features (logic against mocked/sample data)

### Data models
- [ ] Define `Story` model (key, title, assignee, status, status history, story points, labels, dates, Jira link)
- [ ] Define `Sprint` model (id, name, start/end dates, state: active/closed/future)
- [ ] Define `Defect` model (key, title, priority, status, Jira link)
- [ ] Create sample/mocked fixture data representing stories, sprints, and defects for local development

### Reporting window (FR-1 / §5)
- [ ] Implement function to compute prior Monday 00:00 → Saturday 00:00 IST half-open interval for a given "run" datetime
- [ ] Implement Jira timestamp → IST conversion helper
- [ ] Handle edge cases: run date not a Monday, timestamps near midnight, DST-equivalent boundary (IST has no DST, but test explicitly)

### Completed-work detection (FR-1, §5)
- [ ] Implement status-change history scan to detect entry into a configured "completed" status within the window
- [ ] Deduplicate: count a story once even if it entered/left completed status multiple times in-window
- [ ] Exclude stories completed outside the window or with unrelated status changes
Approach 3

### Blocked-work detection (FR-1, §5)
- [ ] Implement configurable "blocked" rule evaluator (status / field / label based, per confirmed config)
- [ ] Extract blocker reason and Jira link per story, rendering "Not available" when missing

### Assignee aggregation (FR-1, FR-2)
- [ ] Implement grouping of completed stories by assignee, including an explicit "Unassigned" bucket
- [ ] Compute team total and verify it reconciles with the sum of per-assignee counts

### Velocity calculation (FR-3, §5)
- [ ] Implement lookup of three most recently completed sprints from sprint history
- [ ] Sum story points completed per sprint; average across the three sprints
- [ ] Detect and surface missing story-point estimates or unavailable sprint history as explicit data-limitation flags (never default to zero)

### Quarter forecast (FR-3, §5)
- [ ] Implement point-capacity calculation (velocity × number of planned sprints before quarter end)
- [ ] Implement backlog story-points comparison against capacity, mapping one Story to one business case
- [ ] Compute number of backlog stories that fit within capacity
- [ ] Implement "provisional"/"unavailable" labeling when quarter dates, sprint plans, or estimates are incomplete
- [ ] Ensure forecast output never implies guaranteed delivery

### Critical defects (FR-4)
- [ ] Implement filter for Priority "1" issues not in the configured resolved/completed status set
- [ ] Produce a structured list of open P1 defects for rendering

### Markdown rendering (FR-2, FR-5)
- [ ] Implement report header section (report date, reporting period boundaries in IST)
- [ ] Implement completed-story-by-assignee section with team total
- [ ] Implement blocked-stories section (key, title, assignee, status, dates, points, blocker reason, link)
- [ ] Implement velocity section (3-sprint average, with data-limitation caveats when applicable)
- [ ] Implement quarter forecast section (inputs, assumptions, capacity, fitting story count)
- [ ] Implement prominent open-P1-defects section
- [ ] Implement missing/incomplete-data caveat section
- [ ] Keep layout concise/one-page-oriented without omitting required blocked-story details

### File output (FR-5, §8)
- [ ] Implement dated filename generation: `reports/weekly-status-YYYY-MM-DD.md` using IST run date
- [ ] Implement atomic write (write to temp file, then rename) so interrupted runs don't leave partial reports
- [ ] Ensure existing dated reports are never overwritten (fail/skip with clear message on collision)

---

## Phase 3: Integration (live Jira wiring, CLI, scheduler)

### Jira Cloud REST client
- [ ] Implement authenticated HTTP session (API token auth) using config-supplied credentials
- [ ] Implement JQL-based issue search for `project = TCL AND issuetype = Story AND labels = "Ready for deployment"`
- [ ] Implement pagination handling so no issue list is silently truncated
- [ ] Implement per-issue changelog/status-history retrieval
- [ ] Implement bounded retry with backoff for transient network/rate-limit failures, respecting Jira rate-limit headers
- [ ] Map configured story-points field ID and blocked-indicator field/label into internal models

### Jira Agile API (sprints)
- [ ] Implement board/sprint lookup for the configured board ID(s)
- [ ] Implement retrieval of the three most recently completed sprints and their completed story points
- [ ] Implement retrieval of future/planned sprint backlog items and their point estimates

### Defects
- [ ] Implement JQL/query for defect issue type(s) with Priority = 1 and status not in resolved/completed set

### End-to-end wiring
- [ ] Replace mocked data sources with live Jira client calls behind the same interfaces used in Phase 2
- [ ] Implement explicit failure path: auth failure or incomplete required queries abort the run (no success-shaped empty report) and return non-zero exit code
- [ ] Ensure failed runs do not write or overwrite any report file

### CLI & manual execution (FR-6)
- [ ] Implement CLI entry point supporting a manual "run now" invocation for testing/recovery
- [ ] Add CLI flag/option to override the run date (for testing historical windows)
- [ ] Add CLI exit codes: 0 success, non-zero on failure, with actionable log message

### Scheduling (FR-6)
- [ ] Create Windows Task Scheduler task definition targeting Monday 09:00 `Asia/Kolkata` (convert to local machine timezone)
- [ ] Configure missed-run behavior per confirmed setup decision (§7 item)
- [ ] Document and script task registration (e.g., PowerShell script using `schtasks`/`Register-ScheduledTask`)
- [ ] Verify the scheduled task invokes the venv's Python interpreter and correct entry point

---

## Phase 4: Testing

### Unit tests — calculations
- [ ] Reporting-window boundary tests (non-Monday run date, midnight edge cases, week-boundary timestamps)
- [ ] Status-change dedup tests for completed-story detection (enter/leave/re-enter within window)
- [ ] Assignee aggregation tests, including unassigned bucket and total reconciliation
- [ ] Velocity averaging tests, including missing-estimate and unavailable-sprint-history cases
- [ ] Forecast arithmetic tests, including provisional/unavailable labeling paths
- [ ] Critical-defect classification tests (status-category edge cases)

### Unit tests — rendering & output
- [ ] Markdown output tests for each report section's structure/content
- [ ] Missing-field placeholder tests ("Not available" rendering)
- [ ] Dated filename generation tests
- [ ] Preservation-of-prior-reports tests (no overwrite on collision)
- [ ] Atomic-write tests (simulated interruption leaves no partial report)

### Jira client tests (mocked)
- [ ] Pagination handling tests with mocked multi-page responses
- [ ] Changelog retrieval tests with mocked status-history payloads
- [ ] Rate-limit and backoff behavior tests with mocked 429/Retry-After responses
- [ ] Authentication-error handling tests (401/403 mocked responses)
- [ ] Incomplete/missing-data handling tests (absent story points, absent sprint history)

### Jira sandbox / real-API verification
- [ ] Provision or obtain access to a non-production Jira Cloud sandbox/test project
- [ ] Seed sandbox with representative Stories, labels, sprints, and a sample P1 defect
- [ ] Run manual integration test against the sandbox and compare output to expected report
- [ ] Verify pagination and rate-limit handling against sandbox (or a controlled simulation)

### Security/quality checks
- [ ] Verify logs and generated report files never contain Jira credentials/tokens
- [ ] Run a full manual end-to-end test before enabling the Monday schedule

---

## Phase 5: Documentation

- [ ] Write `README.md` section for the new app: purpose, prerequisites, setup steps
- [ ] Document configuration file schema (all keys from `config.example.yaml`, with descriptions)
- [ ] Document manual run instructions (CLI usage, flags, exit codes)
- [ ] Document Windows Task Scheduler setup/registration steps and how to verify the scheduled job
- [ ] Document the report structure/fields for Scrum Master end users (what each section means)
- [ ] Document known limitations and explicit non-goals (no auto-publish, no Jira writes, draft-only)
- [ ] Document security/credential-handling approach (where tokens live, least-privilege scope)
- [ ] Document how to update configuration when Jira field IDs/status names change
