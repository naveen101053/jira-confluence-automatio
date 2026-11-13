# Module 17 Completion Report

## Specification Contents

# Feature Specification: Weekly Jira Status Report Automation

**Status**: Draft
**Created**: 2026-11-13
**Source**: `project_spec.md`
**Constitution**: [Jira/Confluence Automation Constitution](./constitution.md)

## 1. Overview

Build a web application and scheduled backend service that generates a weekly Markdown status report from Jira Cloud for the Costing work bench project (`TCL`). The report is a draft for Scrum Master review. It summarizes completed and blocked work, recent team velocity, a provisional quarter-end forecast, and open Priority 1 defects.

The Scrum Master can review generated reports and trigger a run manually for testing or recovery. Report distribution and changes to Jira remain outside the application's scope.

The required implementation stack is React 18 with Vite, Node.js with Express, and PostgreSQL 15 via Docker. This stack supersedes the Python implementation proposal in the source draft; the source draft's functional requirements remain the basis of this specification.

## 2. Goals and Non-Goals

### Goals

- Generate a report every Monday at 09:00 in `Asia/Kolkata`.
- Calculate the previous workweek's completed stories accurately from Jira status history.
- List currently blocked stories and their available details.
- Calculate three-sprint average velocity and a clearly qualified quarter forecast.
- Highlight open Priority 1 defects without suppressing the report.
- Preserve dated Markdown reports for human review.
- Provide a manual run and a web interface to review report output and run status.

### Non-Goals

- Automatically email, publish, or otherwise distribute reports.
- Create, edit, transition, or delete Jira issues.
- Write to Confluence or publish report content to Confluence in the initial release.
- Replace Scrum Master review or represent a forecast as a delivery commitment.
- Define a production scheduler deployment or missed-run policy before the relevant configuration is approved.

## 3. Users and Prioritized User Stories

### User Story 1 — Generate a reliable weekly report (Priority: P1)

As a Scrum Master, I want the system to generate the weekly report from Jira on schedule so that I can review a consistent summary of the team's recent work.

**Why P1**: Scheduled report generation is the primary purpose of the application.

**Acceptance scenarios**

1. **Given** valid Jira access and complete required configuration, **when** the scheduled run starts Monday at 09:00 `Asia/Kolkata`, **then** the system fetches the configured Jira data, calculates the report, and writes a dated Markdown draft.
2. **Given** a report run date, **when** its reporting window is calculated, **then** it covers the preceding Monday at 00:00 through the following Saturday at 00:00 in `Asia/Kolkata`, using a half-open interval.
3. **Given** Jira authentication or a required query fails, **when** the run finishes, **then** it is recorded as failed, the failure is actionable, and no success-shaped empty report is created.
4. **Given** a report has already been generated for the date, **when** another run is requested, **then** the earlier report is preserved and the new run does not silently overwrite it.

### User Story 2 — Review completed and blocked work (Priority: P1)

As a Scrum Master, I want completed work grouped by assignee and current blockers listed with useful context so that I can review the week's delivery and impediments.

**Acceptance scenarios**

1. **Given** an in-scope story entered a configured completed status during the reporting window, **when** the report is generated, **then** it is counted once, including if it later left a completed status during that window.
2. **Given** a story did not enter a completed status during the reporting window, **when** the report is generated, **then** it is not counted as completed merely because its current status is completed.
3. **Given** an in-scope story has no assignee, **when** completed work is grouped, **then** it appears in an explicit `Unassigned` group and the groups reconcile to the team total.
4. **Given** an in-scope story is currently blocked, **when** the report is generated, **then** it appears with the available key, title, assignee, status, relevant dates, story points, blocker reason, and Jira link.
5. **Given** a requested optional issue field is unavailable, **when** a blocked story is rendered, **then** the report says `Not available` for that field rather than fabricating a value or omitting the story.

### User Story 3 — Understand velocity and forecast assumptions (Priority: P1)

As a Scrum Master, I want recent sprint velocity and a qualified quarter-end forecast so that I can use them as planning inputs without mistaking them for commitments.

**Acceptance scenarios**

1. **Given** complete data for the three most recently completed sprints, **when** velocity is calculated, **then** the report shows the average of the three sprint totals in story points per sprint.
2. **Given** any required sprint total or story-point estimate is missing, **when** velocity or forecast is prepared, **then** missing values are not treated as zero and the affected result is marked unavailable or provisional with the data limitation stated.
3. **Given** quarter-end, planned future sprints, velocity, and backlog estimates are available, **when** the forecast is calculated, **then** it shows its inputs, point capacity, and the number of backlog stories fitting within that capacity.
4. **Given** a forecast is shown, **when** a reader reviews it, **then** the report clearly says it is provisional and not a delivery commitment.

### User Story 4 — Review critical defects (Priority: P1)

As a Scrum Master, I want open Priority 1 defects highlighted in the report so that critical work remains visible without preventing the weekly report from being produced.

**Acceptance scenarios**

1. **Given** one or more issues match the configured defect issue type, Priority `1`, and a status not in the configured resolved/completed statuses, **when** the report is generated, **then** each is listed prominently as an open critical defect.
2. **Given** an open Priority 1 defect exists, **when** report generation succeeds otherwise, **then** the report is still produced.
3. **Given** issue type or resolved-status configuration is missing, **when** the system cannot reliably classify defects, **then** it reports the limitation instead of claiming there are no open critical defects.

### User Story 5 — Run and review reports from the web application (Priority: P2)

As a Scrum Master, I want to trigger a manual run and review prior report runs so that I can test or recover a report without relying solely on the schedule.

**Acceptance scenarios**

1. **Given** an authorized user requests a manual run, **when** the run is accepted, **then** the application provides its run status and records whether it succeeded or failed.
2. **Given** a report has been generated, **when** an authorized user opens it, **then** the Markdown report is available for review and download.
3. **Given** a run is in progress or has failed, **when** the user views run history, **then** its status and relevant timestamps or actionable failure details are visible.

## 4. Functional Requirements

### Jira scope and retrieval

- **FR-001**: The Jira source MUST be Jira Cloud. The initial project key MUST be `TCL`, and the issue type for weekly completed and blocked work MUST be `Story`.
- **FR-002**: Weekly completed and blocked work MUST be limited to issues with the exact label `Ready for deployment`. An issue with additional labels remains in scope if it contains that exact label.
- **FR-003**: The Jira client MUST retrieve all matching results, including pagination and required changelog/sprint data. It MUST NOT silently truncate results.
- **FR-004**: Jira requests MUST respect rate limits. Transient network and rate-limit failures MAY be retried with bounded backoff; authentication, permission, and non-transient failures MUST be surfaced.
- **FR-005**: Jira access MUST be read-only for this feature.

### Reporting window and completed work

- **FR-006**: The default schedule MUST be every Monday at 09:00 in `Asia/Kolkata`.
- **FR-007**: A report run MUST identify its report date and use the preceding Monday 00:00 inclusive through Saturday 00:00 exclusive in `Asia/Kolkata` as its reporting window.
- **FR-008**: Completion MUST be determined from Jira status history. Count an in-scope story once if it entered any configured completed status during the reporting window, regardless of its status at report time or later transitions in the same window.
- **FR-009**: The report MUST group completed-story counts by assignee, include an `Unassigned` group, and show a team total that reconciles to the group counts.

### Blocked work and critical defects

- **FR-010**: The report MUST list in-scope stories currently identified as blocked at report time. The blocked rule MUST be configurable as a Jira status, field, or label rule.
- **FR-011**: For each blocked story, include the issue key, title, assignee, status, relevant dates, story points, blocker reason, and Jira link when available. Missing optional values MUST be rendered as `Not available`.
- **FR-012**: The system MUST identify critical defects as issues of the configured defect issue type with Jira Priority `1` whose status is not in the configured resolved/completed statuses.
- **FR-013**: Open critical defects MUST be prominently listed. Their presence MUST NOT fail an otherwise successful report run.

### Velocity and forecast

- **FR-014**: Velocity MUST be the mean story-point total for the three most recently completed sprints. Each sprint total is the sum of points for stories completed in that sprint.
- **FR-015**: Story-point field identifiers, sprint/board identifiers, status mappings, and velocity issue scope MUST be supplied through configuration.
- **FR-016**: Missing sprint history or point estimates MUST NOT be interpreted as zero. The report MUST identify incomplete inputs and mark velocity or forecast unavailable/provisional as appropriate.
- **FR-017**: The quarter forecast MUST use the configured quarter-end date, planned future sprints before that date, recent average velocity, and estimated points for future backlog stories.
- **FR-018**: For the initial forecast, one Jira Story MUST represent one business case. Show the planned sprint count, point capacity, backlog estimate basis, and the number of backlog stories that fit. Use Jira's sprint sequence and backlog rank to evaluate stories in order.
- **FR-019**: The forecast MUST be labeled provisional and MUST NOT imply that an item will be delivered solely because it fits the point-capacity estimate.

### Output, run history, and application

- **FR-020**: Each successful run MUST produce a concise Markdown draft with the report date, reporting boundaries in IST, completed-work summary, blocked-story details, velocity, forecast, open Priority 1 defects, and data-quality caveats.
- **FR-021**: The default output path MUST be `reports/weekly-status-YYYY-MM-DD.md`, using the report date in IST. The system MUST preserve previous reports. A repeat run for the same date MUST use a unique versioned filename or fail explicitly; it MUST NOT silently overwrite an earlier draft.
- **FR-022**: Report output MUST be written atomically. A failed or interrupted write MUST NOT leave a partial report or replace a prior successful report.
- **FR-023**: The React application MUST provide report review and download, manual report triggering, and visibility into run status and history.
- **FR-024**: The Node.js/Express backend MUST perform Jira access, report calculations, authorization, persistence, scheduling, and file operations. The browser MUST NOT receive Jira credentials.
- **FR-025**: PostgreSQL MUST persist report-run metadata and application configuration needed to operate the service. Sensitive integration credentials MUST be supplied through an approved environment/secret mechanism and MUST NOT be stored as plaintext in PostgreSQL.
- **FR-026**: The system MUST NOT email, publish, or share report content automatically. Distribution remains a manual action after Scrum Master review.

## 5. Report Content and Data Rules

### Required report sections

1. Report date and reporting period in IST.
2. Completed-story counts by assignee, including `Unassigned`, and a team total.
3. Currently blocked stories and all available requested details.
4. Average velocity across the three most recently completed sprints.
5. Quarter forecast, its assumptions, and an explicit provisional/unavailable status.
6. Prominent list of open Priority 1 defects.
7. Concise caveats for missing, incomplete, or stale data.

The report SHOULD fit on one page where practical. Required information MUST NOT be silently omitted to meet a page limit.

### Reporting window

Represent the time window as `[Monday 00:00, Saturday 00:00)` in `Asia/Kolkata`. Convert Jira timestamps to the reporting timezone before deciding whether status transitions fall inside the interval. This avoids dependence on an end-of-day timestamp precision.

### Forecast rules

Calculate point capacity as average velocity multiplied by the number of planned future sprints before quarter end. Evaluate estimated future backlog Stories in Jira sprint order and rank order, counting the ordered prefix that fits within available capacity. If required inputs or any required backlog estimates are incomplete, do not treat unknown point values as zero; identify the limitation and mark the story-fit result provisional or unavailable.

## 6. Data Entities

- **Application configuration**: Jira base URL, project key, board identifiers, story-point field identifier, completed/resolved status mappings, blocked-work rule, defect issue types, quarter end, velocity scope, and schedule settings. Secret values are not part of this entity.
- **Report run**: Unique run identifier, trigger type (scheduled/manual), report date, reporting window, lifecycle status, start/end timestamps, output path, and sanitized failure details if applicable.
- **Report artifact**: Generated Markdown file associated with a successful report run. The file is the reviewable report; run metadata is stored in PostgreSQL.

Issue details are retrieved from Jira for report generation. Persist only the information required for run history and application operation; do not retain an unnecessary copy of Jira issue content.

## 7. External Interfaces and Technical Constraints

- **Frontend**: React 18 with Vite. Display report output, run status, and actionable error states accessibly.
- **Backend**: Node.js with Express. Enforce server-side authorization and validation; isolate Jira client, calculations, report rendering, persistence, and scheduling concerns.
- **Database**: PostgreSQL 15 through Docker. Use versioned migrations, database constraints for durable invariants, and transactions for related metadata changes.
- **Jira Cloud**: Use approved read-only credentials and the Jira REST/Agile APIs or equivalent endpoints for issue data, status history, and sprint data.
- Configuration MUST be environment-specific. Credentials MUST NOT appear in source control, frontend bundles, container images, reports, or logs.
- Scheduler deployment MUST document process availability requirements and the policy for missed runs before production use.

## 8. Error Handling and Data Quality

- Authentication failure, permission denial, required-query failure, calculation failure, and report-write failure MUST be distinguishable and actionable.
- A failed run MUST have a failed status and MUST NOT generate a misleading successful report.
- Optional missing fields MUST be shown as `Not available`; required missing calculation inputs MUST invalidate or qualify the affected metric.
- Respect API pagination and rate-limit responses. Retries MUST be bounded and used only when safe.
- Logs MAY include run identifiers, timestamps, outcomes, and output paths, but MUST NOT include credentials, authorization headers, or unnecessary issue content.
- A report file MUST not be marked successful in run history until the atomic write has completed.

## 9. Security, Privacy, and Accessibility

- Grant Jira access only to the project and read operations needed for reporting.
- Store credentials in an approved secret store or environment configuration. Never commit credentials or return them to the browser.
- Restrict report access to authorized users; generated reports may contain assignee names, issue summaries, blocker reasons, and Jira links.
- Confirm report retention and authorized local repository access before distributing reports.
- Escape or safely render Jira-sourced text in the web UI. The UI MUST provide keyboard-operable controls, accessible labels, and clear loading, empty, success, and error states.

## 10. Success Criteria

- **SC-001**: For a Monday 09:00 `Asia/Kolkata` run, the selected reporting interval is the prior Monday 00:00 through Saturday 00:00 exclusive, including correct classification of timezone and week-boundary timestamps.
- **SC-002**: Only `TCL` Stories with the exact `Ready for deployment` label appear in weekly completed and blocked work.
- **SC-003**: Completed stories are counted once from status history, and grouped counts including unassigned work reconcile exactly to the team total.
- **SC-004**: Every currently blocked in-scope story appears in the report with all available requested details; no blocker is dropped to meet a page limit.
- **SC-005**: Velocity matches the mean of the three most recently completed sprint totals, and missing estimates/history are never treated as zero.
- **SC-006**: Forecast inputs, capacity, story-fit count, assumptions, and provisional status are visible; no forecast is presented as a delivery commitment.
- **SC-007**: Open Priority 1 defects are prominently reported while otherwise valid report generation continues.
- **SC-008**: Successful runs produce a dated Markdown report atomically, preserve earlier reports, and record matching run metadata.
- **SC-009**: Jira, calculation, persistence, and file-write failures are explicit, create a failed run record where possible, and never yield a misleading successful report.
- **SC-010**: Automated delivery to stakeholders and write operations to Jira or Confluence do not occur.

## 11. Verification Plan

- Unit tests: reporting-window boundaries and timezone conversion; completion-history deduplication; assignee aggregation; blocked classification; velocity averaging; forecast capacity and ordered story-fit calculation; defect classification.
- Component tests: Markdown sections, missing-value placeholders, caveats, filename generation, repeat-run behavior, and atomic output preservation.
- Backend tests with mocked Jira responses: pagination, changelog retrieval, rate limits, authentication/permission errors, incomplete data, and retry bounds.
- API and persistence tests: manual run lifecycle, run history, authorization, configuration validation, and failure recording.
- Frontend tests: report loading/download, manual run status, accessible interaction, and loading/empty/error states.
- Manual integration test against a non-production Jira project or approved test dataset before enabling the production schedule.
- Verify logs, frontend bundles, generated reports, container configuration, and database records do not expose credentials.

## 12. Assumptions and Open Decisions

- Jira weekly report generation is the initial product scope. The source requirements do not define a Confluence use case; therefore the initial release does not read from or write to Confluence.
- Weekly activity and blocked work are label-filtered. The source requirements leave velocity scope unresolved (all `TCL` Stories versus only `Ready for deployment` Stories); this MUST be selected in configuration and confirmed before production reporting.
- The exact Jira site URL, authentication method, board IDs, story-point field, completed/resolved statuses, blocked rule, blocker-reason field, defect issue types, quarter calendar/end date, and report-retention policy must be supplied before production.
- The approved identity/authorization model for users of the web application must be selected before exposing manual runs or report history.
- The scheduler's host, missed-run behavior, and the behavior when the service is unavailable at the scheduled time must be decided during deployment.
- The backlog fit calculation assumes ordered Jira backlog items and one Story per business case; confirm whether this remains valid if the team's business-case mapping changes.

## Commit History

```text
481fcab Add dashboard preview and SpecKit artifacts
dc35568 test
d1caf8f test
fba4587 test
eb5e076 chore: project skeleton for prototype’
4421f6b test
21c5738 test
e1a302a Merge branch 'main' of https://github.com/naveen101053/jira-confluence-automatio
7e35694 test
568550d Added Phase 1
7cfe338 first commit
afe3508 first commit
745c300 first commit
dbebe47 first commit
8bfa8b7 1
fe88d95 3
d181628 3
5c9aa2e 2
dbcf9f6 v1
a107a8a t1
89e55f0 v2
005257f te
8dee40f v1
56b010e compound interest
b86b7a3 test
4194cac updTE
f395558 test
df0f6f4 test
fdcc214 test
a11afd7 test
e889eae test
cafc889 test
35db30a updated
1ecd6eb report
80fbe89 initial version
6a2ac02 test
70d07da todo
843cad8 Add status report template, instructions, and example
53ce5ba new report
071b811 Update project_spec.md
b952e1f Weekly status report - jira
d1a04c2 Update module 03 report with latest git state
2d541b5 Add division functionality and module 03 completion report
a04cb16 Remove work/ from .gitignore to track local work files
47d51b1 Refactor calculator usage in demo script and update README for class-based implementation
5f1d1ba Add calculator multiplication demo
5a2dacc Initial calculator with add and subtrac
5e3c91e Initial commit: simple Python calculator project
```

## Commit Count

48

## Project Files

```text
.env.example
.github/copilot-instructions.md
.github/prompts/to-Blocked-work-detection.prompt.md
.github/prompts/to-calculate-compound-interest.prompt.md
.github/prompts/to-create-status-report.prompt.md
.github/prompts/to-creating-instructions.prompt.md
.github/prompts/to-detect-completed-work.prompt.md
.gitignore
README.md
TODO.md
backend/src/calculations/blockedWork.ts
backend/src/calculations/completedWork.ts
backend/src/calculations/criticalDefects.ts
backend/src/calculations/forecast.ts
backend/src/calculations/reportingWindow.ts
backend/src/calculations/velocity.ts
backend/src/config/env.ts
backend/src/jira/client.ts
backend/src/reports/markdownRenderer.ts
backend/src/reports/reportStore.ts
backend/src/routes/reports.ts
backend/src/server.ts
backend/src/shared/index.ts
backend/src/worker/runReport.ts
backend/src/worker/scheduler.ts
backend/tests/reporting.test.ts
backlog.md
calculator.py
docker-compose.yml
frontend/index.html
frontend/package-lock.json
frontend/package.json
frontend/src/App.tsx
frontend/src/api/client.ts
frontend/src/components/BlockedStoriesList.tsx
frontend/src/components/CompletedWorkTable.tsx
frontend/src/components/CriticalDefects.tsx
frontend/src/components/ReportSummary.tsx
frontend/src/components/VelocityForecast.tsx
frontend/src/main.tsx
frontend/src/pages/DashboardPage.tsx
frontend/src/styles.css
frontend/tsconfig.json
frontend/vite.config.ts
instructions/Blocked-work-detection.agent.md
instructions/calculate-compound-interest.agent.md
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/detect-completed-work.agent.md
instructions/main.agent.md
instructions/validate-instructions.agent.md
jira_report/__init__.py
jira_report/calculations/__init__.py
jira_report/calculations/completed_work.py
main.py
outputs/backlog.md
outputs/bad.md
outputs/ok.md
package.json
phase-1/README.md
project_spec.md
reports/example.md
reports/instructions.md
reports/template.md
reports/weekly-status-2026-11-05.md
reports/weekly-status-report.md
requirements-dev.txt
spec/analyze.md
spec/clarify.md
spec/constitution.md
spec/plan.md
spec/specification.md
spec/task-001-inventory.md
spec/tasks.md
tests/calculations/test_completed_work.py
tests/calculations/test_completed_work_multi_project.py
tests/fixtures/blocked_work_stories.json
tests/fixtures/completed_work_stories.json
tests/fixtures/completed_work_stories_abc.json
tests/fixtures/completed_work_stories_cwb.json
tools/Blocked-work-detection.py
tools/compound_interest.py
tools/mcp-echo.ps1
work/module-03-report.md
work/module-08-report.md
work/module-09-report.md
work/module-10-report.md
work/module-12-report.md
work/module-13-report.md
work/module-14-report.md
work/module-15-report.md
work/module-16-report.md
```
