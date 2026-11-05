# Weekly Jira Status Report Generator

## 1. Purpose

Build a Java application that creates a weekly Markdown status report from Jira Cloud for the Costing work bench project. The Scrum Master reviews the generated draft and shares it with client product owners. The report should support planning the remaining business cases for the upcoming quarter using the team's recent delivery velocity.

This document defines the requested application; it does not change the existing Python calculator in this repository.

## 2. Goals and non-goals

### Goals

- Run every Monday at 9:00 AM India Standard Time (IST).
- Summarize the previous workweek, Monday through Friday.
- Report completed work and blocked work for the requested Jira scope.
- Show completed work counts in a team/assignee breakdown and provide details for blocked stories.
- Estimate how much future sprint backlog can fit before the configured quarter end, using recent story-point velocity.
- Save a dated Markdown draft in the repository for Scrum Master review.
- Prominently flag open Priority 1 defects without preventing report generation.

### Non-goals

- Automatically email or publish the report to stakeholders.
- Modify Jira issues, sprint assignments, or estimates.
- Treat the report as a substitute for Scrum Master review.

## 3. Users and workflow

1. A local scheduled run starts the generator on Monday at 9:00 AM IST.
2. The application reads Jira data, calculates weekly results and a provisional forecast, and writes a dated report under `reports/`.
3. If any open Priority 1 defects exist, the report flags them prominently; generation continues.
4. The Scrum Master reviews and corrects the draft, then shares it manually with client product owners.

## 4. Functional requirements

### FR-1: Jira scope

- Jira deployment: Jira Cloud.
- Project key: `TCL`.
- Issue type: `Story`.
- Weekly activity and blocked-story scope: stories with the exact label `Ready for deployment`.
- Completed-story count: stories in scope that entered a completed status during the previous Monday–Friday in IST.
- Blocked-story list: stories in scope that are currently identified as blocked when the report is generated.
- Stories with multiple labels remain in scope if they include `Ready for deployment`.
- Group completed counts by assignee; include an explicit unassigned group.

### FR-2: Report contents

Produce one concise Markdown report containing:

- Report date and reporting-period boundaries in IST.
- A compact completed-story count by assignee and a team total.
- A list of currently blocked stories, with each story's key, title, assignee, status, relevant dates, story points, blocker reason, and Jira link when available.
- A three-completed-sprint average velocity in story points per sprint.
- An upcoming-quarter forecast based on the future sprint backlog and the configured quarter-end date.
- A prominent section listing any open Priority 1 defects.
- A short caveat for missing or incomplete Jira data and for provisional forecasts.

The report should be concise and designed to fit on one page where practical. Do not silently omit blocked stories or other required information merely to force a page limit.

### FR-3: Velocity and forecast

- Calculate velocity as the average story points completed per sprint over the three most recently completed sprints.
- Use Jira sprint history and story-point values; do not infer missing estimates as zero.
- Treat one Jira Story as one business case for the initial forecast.
- Use future sprint backlog items, their story-point estimates, recent velocity, and the number of planned sprints before quarter end to estimate feasible delivery.
- Clearly show the forecast inputs and assumptions. Mark the forecast provisional or unavailable if required data is absent.
- Do not imply that a business case will be delivered solely because it fits the point-capacity estimate.

### FR-4: Critical defects

- A defect with Jira Priority `1` is critical.
- Find defects whose Jira status is not in the configured resolved/completed statuses.
- List and clearly flag open Priority 1 defects in the report.
- Continue to produce the draft even when such defects are open.

### FR-5: Draft creation

- Output format: Markdown.
- Default output pattern: `reports/weekly-status-YYYY-MM-DD.md`, using the report run date in IST.
- Preserve each dated report; do not overwrite prior reports.
- Do not send or publish automatically. Review and distribution remain manual.

### FR-6: Scheduling and manual execution

- Default schedule: every Monday at 09:00 in the `Asia/Kolkata` timezone.
- Provide a way to run the generator manually for testing or recovery.
- The local machine must be available at the scheduled time. The chosen operating-system scheduler and missed-run behavior must be configured during deployment.

## 5. Data and calculation rules

### Reporting window

For a Monday run, use the preceding Monday at 00:00 through Friday at 23:59:59 IST. Use a half-open date interval in implementation (`[Monday 00:00, Saturday 00:00)`) to avoid end-of-day boundary errors. Convert Jira timestamps to IST before determining the window.

### Completed work

Count a story once if its workflow history shows that it entered a configured completed status during the reporting window. Use status-change history rather than current status alone. If a story entered a completed status and later left it within the window, count it once and disclose the status history as needed.

### Blocked work

Include stories currently identified as blocked at report generation time. The Jira representation of “blocked” is not yet known and must be configured (status, field, or label rule). Include the available blocker reason and Jira link; do not fabricate missing values.

### Velocity

For each of the three most recently completed sprints, sum the story points of stories completed in that sprint. Average the three sprint totals. Missing estimates or unavailable sprint history must be reported as a data limitation, not treated as zero.

### Quarter forecast

Use the configured quarter-end date and planned future sprints before that date. Compare the available point capacity (recent average velocity multiplied by the number of planned sprints) against estimated points in the future sprint backlog. Since the initial business-case unit is one Story, show estimated business-case capacity and the number of backlog stories that fit, with assumptions visible. If quarter dates, sprint plans, business-case mapping, or estimates are incomplete, label the forecast provisional or unavailable.

### Open critical defects

Treat Priority `1` issues as critical. “Open” is determined by the configured set of Jira completed/resolved statuses, rather than a hard-coded status name.

## 6. Proposed technical design

- **Language:** Java. Select the Java LTS version and build tool during implementation.
- **Integration:** Jira Cloud REST APIs for issue search/details and changelog data; Jira Software Agile APIs or equivalent board/sprint data for sprint history and planned future sprints.
- **Configuration:** External configuration for Jira base URL, project/board identifiers, status mappings, blocked rule, field identifiers, quarter end, output directory, and schedule. Keep credentials out of source control.
- **Authentication:** Use an approved Jira Cloud service account or organizational integration. For a local run, credentials may be supplied through a local gitignored configuration file or environment variables. Never commit credentials or write them to logs.
- **Processing:** Separate Jira retrieval, report calculations, Markdown rendering, and scheduling/command-line execution so calculations can be tested independently.
- **Output:** Write each dated report atomically (temporary file followed by rename) so an interrupted run does not leave a partial report.
- **Logging:** Log run start/end, report path, and actionable error details. Do not log API tokens or unnecessary issue content.

The repository currently contains a Python calculator rather than a Java application. The Java project structure, dependency management, and local scheduler integration therefore need to be established as part of implementation.

## 7. Configuration required before production

The following values must be confirmed or supplied at setup:

1. Jira site URL, service account/authentication method, and Jira board ID(s).
2. Exact Jira field identifier for story points.
3. Status names/categories that count as completed/resolved.
4. How blocked stories are identified and how blocker reason is stored.
5. Which issue types count as defects and the Jira Priority value corresponding to `1`.
6. Quarter calendar and quarter-end date.
7. Whether the velocity calculation should use all `TCL` Stories or only Stories carrying `Ready for deployment`. The weekly activity scope remains label-filtered.
8. Local operating-system scheduler and behavior after a missed Monday run.
9. Java LTS version and build tool.

## 8. Error handling and data quality

- Fail the run explicitly when Jira authentication fails or required Jira queries cannot be completed; do not create a success-shaped empty report.
- Retry transient network/rate-limit failures with bounded backoff and respect Jira rate-limit responses.
- Paginate all Jira results; do not silently truncate issue lists.
- If optional fields are absent, render a clear placeholder such as “Not available” and identify the affected metric.
- If velocity inputs are incomplete, mark the velocity/forecast unavailable rather than substituting zero.
- If the report cannot be written, return a non-zero failure result and log the destination and reason.
- A failed run must not overwrite previously generated reports.

## 9. Security and privacy

- Use least-privilege Jira access sufficient to read the required projects, issues, history, and sprint data.
- Store tokens only in a local gitignored configuration file or approved secret store/environment; confirm the chosen approach before deployment.
- Ensure credentials, authorization headers, and sensitive issue data are excluded from logs.
- Include assignee names, issue summaries, blocker reasons, and Jira links only in the local draft intended for authorized review.
- Confirm local repository access and report-retention expectations before distributing generated reports.

## 10. Acceptance criteria

1. A Monday 09:00 `Asia/Kolkata` run selects the prior Monday–Friday reporting window correctly, including timestamps near midnight and week boundaries.
2. Only `TCL` Stories with the exact `Ready for deployment` label qualify for weekly completed counts and the blocked list.
3. A story entering a completed status during the reporting window is counted once; unrelated status changes and stories completed outside the window are excluded.
4. Completed counts are grouped by assignee, include unassigned work, and reconcile to the team total.
5. Currently blocked stories include the available requested details and are not omitted to enforce a one-page layout.
6. Velocity is the mean of the three most recently completed sprint totals, with missing data surfaced rather than interpreted as zero.
7. The quarter forecast uses configured future sprint backlog and quarter-end inputs, identifies one Story as one business case, and displays its assumptions.
8. An open Priority 1 defect is flagged while report generation still succeeds.
9. The application writes a dated Markdown report under `reports/` and preserves earlier reports.
10. Jira/API, calculation, report rendering, and file-write failures are explicit and do not produce a misleading successful report.
11. The report is a draft only; no stakeholder delivery occurs without Scrum Master review and manual sharing.

## 11. Verification plan

- Unit tests for reporting-window boundaries, status-change deduplication, assignee aggregation, velocity averaging, forecast arithmetic, and critical-defect classification.
- Tests for Markdown output, missing-field placeholders, dated filenames, and preservation of prior reports.
- Jira client tests using mocked responses for pagination, changelog retrieval, rate limits, authentication errors, and incomplete data.
- A manual integration test against a non-production Jira project or approved test dataset before enabling the Monday schedule.
- Verify that logs and generated files do not contain Jira credentials.
