# Implementation Tasks: Weekly Jira Status Report Automation

**Status**: Draft
**Plan**: [plan.md](./plan.md)
**Specification**: [specification.md](./specification.md)
**Review findings**: [clarify.md](./clarify.md)

## Task Conventions

- Tasks are grouped by the implementation-plan phases. Complete dependencies before starting a task.
- Acceptance criteria are the task's definition of done; phase milestones are gates, not substitutes for task criteria.
- No effort or calendar estimates are included because staffing and deployment decisions are unknown.
- Phase 0 decisions must be recorded in the specification before dependent implementation begins.

## Phase 0 — Baseline and Decision Closure

### T-001 — Inventory the existing application

**Depends on**: None
**References**: Plan Phase 0

**Acceptance criteria**

- Frontend, backend, tests, Docker configuration, and report calculations are inventoried.
- Each major specification requirement is marked as already implemented, incomplete, or absent in the inventory.
- Reusable code and known validation commands are identified without replacing existing behavior.

### T-002 — Resolve the source-of-truth specification

**Depends on**: T-001
**References**: `project_spec.md`; specification sections 1 and 12; clarify finding 1

**Acceptance criteria**

- The authoritative implementation specification is explicitly identified.
- The Python proposal in `project_spec.md` is marked superseded, consolidated, or retained with a clear boundary that prevents conflicting implementation instructions.
- Manual execution expectations are explicitly included or excluded.

### T-003 — Define report-date and reporting-window behavior

**Depends on**: None
**References**: FR-006–FR-008; clarify finding 2

**Acceptance criteria**

- The specification defines valid report dates and the default date for manual runs.
- Scheduled delays, missed runs, and recovery runs have explicit report-date and period behavior.
- The filename and reporting window are deterministically derived from the report date in `Asia/Kolkata`.

### T-004 — Decide Jira scopes and configuration values

**Depends on**: None
**References**: FR-001–FR-005, FR-010, FR-012, FR-015; clarify findings 3 and 5

**Acceptance criteria**

- Project, issue-type, label, board, and velocity scopes are explicitly selected for completed work, blocked work, velocity, and critical defects.
- Required Jira status/field identifiers and the blocked-rule representation are documented.
- The specification states which configuration is required for a run and what happens when required configuration is missing.

### T-005 — Finalize sprint and forecast rules

**Depends on**: None
**References**: FR-014–FR-019; clarify findings 6 and 8

**Acceptance criteria**

- Sprint completion, issue attribution, reopen/move handling, and valid zero-point totals are defined.
- Quarter horizon and sprint eligibility at the quarter boundary are defined.
- Backlog order, story-fit behavior when an item exceeds remaining capacity, and treatment of missing estimates are defined.

### T-006 — Approve user access and product scope

**Depends on**: None
**References**: FR-023–FR-026; clarify findings 4 and 7

**Acceptance criteria**

- User identities, roles, authentication method, access boundary, and authorization rules for viewing, triggering, and downloading are documented.
- The release's Confluence scope is explicitly confirmed as deferred or expanded with requirements.
- The specification does not imply Confluence operations if they are out of scope.

### T-007 — Define run operations, storage, and data-quality policy

**Depends on**: None
**References**: FR-016, FR-020–FR-025; clarify findings 10–18

**Acceptance criteria**

- Required versus optional Jira data and the boundary between successful-qualified and failed runs are documented.
- Configuration source-of-truth and precedence are defined for database settings and environment/secret settings.
- Artifact persistence, retention, repeat-run naming, concurrency, and file/database recovery behavior are selected.
- Scheduler ownership, missed-run behavior, deployment assumptions, and minimum operational requirements are documented.

### T-008 — Publish the approved baseline

**Depends on**: T-001–T-007
**References**: Plan milestone M0

**Acceptance criteria**

- Decisions from T-002–T-007 are reflected in `spec/specification.md`.
- The plan and task dependencies are updated if the decisions change phase boundaries.
- No unresolved P0 item from [clarify.md](./clarify.md) requires an implementation guess.

**Milestone M0**: Implementation baseline approved; dependent implementation may begin.

## Phase 1 — Application and Data Foundation

### T-009 — Align frontend and backend project setup

**Depends on**: T-008
**References**: Constitution technology constraints; FR-023–FR-024

**Acceptance criteria**

- React 18/Vite frontend and Node.js/Express backend have reproducible development and build commands.
- Existing useful TypeScript/TSX modules and tests remain usable or are migrated with equivalent coverage.
- Supported Node.js version and package-manager commands are documented.

### T-010 — Establish Docker PostgreSQL development environment

**Depends on**: T-008
**References**: Constitution database constraints; FR-025

**Acceptance criteria**

- PostgreSQL 15 starts through the documented Docker workflow and reports healthy before dependent services use it.
- Local database state persists across container restarts and can be recreated using documented steps.
- Credentials are provided through local environment configuration, not committed values or image layers.

### T-011 — Add database migrations and core schema

**Depends on**: T-010
**References**: Constitution database constraints; specification section 6

**Acceptance criteria**

- Versioned migrations create the approved application-configuration and report-run metadata schema.
- A fresh database can be migrated successfully, and durable invariants are enforced with constraints.
- Related metadata changes use transactions where required by the approved data model.

### T-012 — Define and document backend API contracts

**Depends on**: T-008
**References**: FR-023–FR-025

**Acceptance criteria**

- Contracts define configuration validation, manual-run submission, run status/history, and artifact retrieval.
- Request validation, authorization requirements, response states, and error categories are specified.
- The frontend and backend can implement against the same contract without relying on undocumented behavior.

### T-013 — Implement application authentication and authorization

**Depends on**: T-012
**References**: Constitution security principles; specification section 9

**Acceptance criteria**

- Protected API operations enforce the identity and role policy approved in T-006.
- Unauthorized users cannot trigger runs, view run history, or retrieve report artifacts.
- Tests cover permitted and denied access for each protected operation.

### T-014 — Establish automated quality gates

**Depends on**: T-009
**References**: Constitution quality gates

**Acceptance criteria**

- Documented commands exist for relevant tests, type-checking, linting, and production builds.
- Each command runs non-interactively and returns a failing exit status when its check fails.
- Baseline checks pass for the project state after setup.

**Milestone M1**: Local frontend/backend/database setup, migrations, API contracts, authorization, and quality checks are reproducible.

## Phase 2 — Jira Cloud Integration

### T-015 — Implement validated application configuration

**Depends on**: T-011, T-008
**References**: FR-015, FR-025; clarify findings 5 and 10

**Acceptance criteria**

- Configuration validation covers Jira URL, project/board scopes, field IDs, status mappings, blocked rule, quarter, and schedule settings selected in T-004/T-005.
- Secret values are loaded only from the approved environment/secret mechanism and are not serialized into the application configuration record.
- Invalid or missing required configuration produces an explicit, field-specific error.

### T-016 — Implement a server-side, read-only Jira client

**Depends on**: T-015
**References**: FR-003–FR-005; Constitution security and integration principles

**Acceptance criteria**

- Jira credentials are used only by the backend and are never included in browser-visible responses or logs.
- The client exposes only the approved read operations needed by this feature.
- Authentication and permission errors are classified and surfaced without success-shaped fallback data.

### T-017 — Retrieve weekly issue data and changelogs

**Depends on**: T-016
**References**: FR-001–FR-003, FR-008, FR-010–FR-013

**Acceptance criteria**

- Queries apply the approved project, issue-type, and label scopes.
- Issue fields required for weekly counts, blocked stories, and defects are retrieved.
- Status changelog retrieval is complete for the selected issues and supports the approved reporting-window calculation.
- Pagination is followed until all matching results are retrieved.

### T-018 — Retrieve sprint history and future backlog data

**Depends on**: T-016
**References**: FR-014–FR-018

**Acceptance criteria**

- The client retrieves the three most recently completed sprints and the approved future sprint/backlog data.
- Sprint identifiers, completion dates/status, membership, points, and backlog ordering required by the forecast rules are preserved.
- Missing or inaccessible sprint data is reported distinctly from a valid empty sprint/backlog result.

### T-019 — Handle Jira transient failures and rate limits

**Depends on**: T-016
**References**: FR-004; clarify finding 15

**Acceptance criteria**

- Timeouts, rate limits, and transient errors follow the retry policy selected in T-007.
- Retries are bounded and are not used for authentication, permission, or other non-retryable failures.
- Exhausted retries produce an actionable integration error with no misleading empty result.

### T-020 — Normalize Jira responses and test the adapter

**Depends on**: T-017–T-019
**References**: FR-003–FR-004; Constitution integration and test principles

**Acceptance criteria**

- Jira responses are mapped into internal typed data structures independent of raw API response shapes.
- Fixtures cover pagination, status changes, rate limits, permission failures, and missing/invalid fields.
- Adapter tests pass without contacting a live Jira instance.

**Milestone M2**: Required Jira data is retrieved completely, normalized, and covered by controlled integration tests.

## Phase 3 — Report Domain Rules and Calculations

### T-021 — Implement report-date and IST window calculation

**Depends on**: T-008
**References**: FR-006–FR-007; SC-001

**Acceptance criteria**

- The approved scheduled/manual/delayed report-date rules produce a half-open interval in `Asia/Kolkata`.
- Tests cover timestamps at both interval boundaries, week transitions, and report-date validation.
- The output includes the exact report date and interval used for a run.

### T-022 — Filter scope and count completed stories

**Depends on**: T-020, T-021
**References**: FR-001–FR-003, FR-008; SC-002

**Acceptance criteria**

- Only issues in the approved weekly scope are considered.
- A story is counted once when its status history enters a configured completed status during the interval, including a later transition out of that status.
- Current status alone does not qualify a story; outside-window and unrelated transitions are excluded.

### T-023 — Group completed stories by assignee

**Depends on**: T-022
**References**: FR-009; SC-003

**Acceptance criteria**

- Completed counts include every assignee and an explicit `Unassigned` group.
- Group totals reconcile exactly to the team total.
- Tests cover no completed stories, multiple assignees, and unassigned stories.

### T-024 — Classify blocked stories and render their data model

**Depends on**: T-020, T-015
**References**: FR-010–FR-011; SC-004

**Acceptance criteria**

- The selected blocked rule is applied to current issue state and approved weekly scope.
- Each blocked record contains the agreed required fields and all available optional fields.
- Missing optional data is represented explicitly and does not silently remove a blocked issue.

### T-025 — Calculate three-sprint velocity

**Depends on**: T-018, T-015
**References**: FR-014–FR-016; SC-005

**Acceptance criteria**

- Velocity equals the mean of the three most recently completed sprint totals under the approved attribution and scope rules.
- Valid zero-point totals are distinguished from missing estimates or incomplete sprint history.
- Incomplete required inputs produce the approved unavailable/provisional result and an explicit limitation.

### T-026 — Calculate and qualify the quarter forecast

**Depends on**: T-018, T-025
**References**: FR-017–FR-019; SC-006

**Acceptance criteria**

- Capacity uses the approved average velocity and eligible sprint count before the configured quarter end.
- Story-fit count follows the approved issue order, oversize-story, and missing-estimate rules.
- The result includes assumptions and is clearly provisional, never a delivery commitment.

### T-027 — Identify open Priority 1 defects

**Depends on**: T-020, T-015
**References**: FR-012–FR-013; SC-007

**Acceptance criteria**

- Classification uses the approved project/type/Priority/status configuration.
- Open Priority 1 defects are returned with the agreed report fields.
- Missing classification configuration is surfaced as a limitation, not reported as zero open defects.

### T-028 — Complete domain edge-case test suite

**Depends on**: T-021–T-027
**References**: Specification section 11

**Acceptance criteria**

- Focused tests cover timezone boundaries, reopened/moved issues, deduplication, aggregation, blocked classification, missing estimates, forecast edge cases, and critical-defect status.
- All business-rule tests run independently of live Jira.
- Tests demonstrate that unknown data is not coerced to zero or success.

**Milestone M3**: Domain calculations are deterministic, complete against the approved rules, and accepted by tests.

## Phase 4 — Report Generation, Persistence, and Run Orchestration

### T-029 — Implement the Markdown report renderer

**Depends on**: T-023–T-027
**References**: FR-020; specification sections 5 and 8

**Acceptance criteria**

- The report includes all required sections and the report date/window in IST.
- Missing optional values and incomplete metrics use the approved placeholders and caveats.
- Defects are visually prominent and the renderer does not omit required blocked stories to meet a page target.

### T-030 — Implement durable atomic artifact storage

**Depends on**: T-008, T-011
**References**: FR-020–FR-022; clarify finding 11

**Acceptance criteria**

- Artifacts are written to the approved persistent location and use the approved date/version naming policy.
- Writes are atomic and do not replace previous successful reports.
- Tests cover interrupted/failed writes, same-date collisions, and file preservation.

### T-031 — Implement report-run persistence and lifecycle

**Depends on**: T-011
**References**: FR-025; specification sections 6 and 8

**Acceptance criteria**

- Run records capture the approved trigger, report date/window, status, timestamps, artifact path, and sanitized failure information.
- Run status changes follow documented valid transitions.
- Database constraints and transactions protect required metadata invariants.

### T-032 — Orchestrate report generation

**Depends on**: T-020, T-028–T-031
**References**: FR-020–FR-022; SC-008–SC-009

**Acceptance criteria**

- A run calls retrieval, calculations, rendering, artifact storage, and metadata updates in the approved order.
- A run is not marked successful until its artifact is durably written.
- Failures are classified and reported; failed runs do not create misleading success artifacts.

### T-033 — Prevent duplicate and conflicting runs

**Depends on**: T-031–T-032
**References**: FR-021–FR-022; clarify finding 12

**Acceptance criteria**

- Concurrent/manual/scheduled runs follow the selected serialization or rejection policy.
- Duplicate scheduled execution does not overwrite or duplicate an artifact contrary to the approved policy.
- Tests cover concurrent starts and same-report-date retries.

### T-034 — Expose authorized run operations

**Depends on**: T-012–T-013, T-032–T-033
**References**: FR-023–FR-025; User Story 5

**Acceptance criteria**

- The API supports manual run submission and run status/history using the documented contract.
- Responses distinguish accepted/in-progress/success/failure states and provide sanitized actionable errors.
- Authorization is enforced on every operation and validated by tests.

### T-035 — Expose authorized report retrieval and download

**Depends on**: T-013, T-030, T-034
**References**: FR-023; specification section 9

**Acceptance criteria**

- Authorized users can retrieve the report associated with a successful run and download the original Markdown artifact.
- Unauthorized users cannot infer or access report paths or file contents.
- User-controlled identifiers cannot escape the configured artifact storage boundary.

### T-036 — Verify backend end-to-end and recovery behavior

**Depends on**: T-029–T-035
**References**: Specification sections 8 and 11; SC-008–SC-009

**Acceptance criteria**

- Controlled Jira fixtures produce a successful artifact and corresponding run record.
- Tests cover Jira, calculation, database, artifact, and interrupted-run failures.
- File/database inconsistency recovery matches the policy recorded in T-007.

**Milestone M4**: Backend report generation, metadata, API operations, artifact access, and recovery behavior work end-to-end.

## Phase 5 — Web Review and Manual Operations

### T-037 — Build report history and run detail views

**Depends on**: T-034
**References**: FR-023; User Story 5

**Acceptance criteria**

- Authorized users can view report-run history and open a run's status/details.
- Empty history, loading, and API error states are shown distinctly.
- No sensitive integration credential is present in frontend assets or responses.

### T-038 — Add the manual-run workflow

**Depends on**: T-034, T-037
**References**: User Story 5; FR-023

**Acceptance criteria**

- An authorized user can submit a manual run using the approved report-date behavior.
- The UI displays the accepted run and its current status without implying success before completion.
- Invalid dates, duplicate requests, and authorization failures are explained to the user.

### T-039 — Add report preview and download

**Depends on**: T-035, T-037
**References**: FR-020, FR-023; specification section 9

**Acceptance criteria**

- The report is presented using the approved Markdown rendering behavior and its original artifact can be downloaded.
- Jira-sourced text is safely rendered and cannot inject executable markup into the application.
- Missing reports and download failures produce explicit UI states.

### T-040 — Complete accessibility and frontend workflow tests

**Depends on**: T-037–T-039
**References**: Constitution Principle VI; specification sections 9 and 11

**Acceptance criteria**

- Primary dashboard, run, and download flows are keyboard-operable and have accessible labels.
- Tests cover loading, empty, success, failure, and unauthorized states.
- Frontend type-check, tests, lint, and production build pass.

**Milestone M5**: Authorized users can trigger, monitor, review, and download reports through the accessible web application.

## Phase 6 — Scheduling, Integration Validation, and Release Readiness

### T-041 — Implement the approved scheduled trigger

**Depends on**: T-007, T-032–T-033
**References**: FR-006; clarify finding 13

**Acceptance criteria**

- The configured deployment runs the report on Monday at 09:00 `Asia/Kolkata`.
- Only one scheduled execution occurs under the approved deployment topology.
- Restart and missed-run behavior match the decision recorded in T-007.

### T-042 — Run full-stack automated verification

**Depends on**: T-036, T-040–T-041
**References**: Specification section 11; SC-001–SC-010

**Acceptance criteria**

- React, Express, PostgreSQL, artifact storage, and mocked Jira run together in the documented environment.
- End-to-end tests cover scheduled and manual paths, run history, report display/download, and failure handling.
- All required tests, type-checks, lint, and production builds pass.

### T-043 — Perform non-production Jira integration validation

**Depends on**: T-042
**References**: Specification sections 7 and 11

**Acceptance criteria**

- A manual integration run uses an approved non-production project or dataset and least-privilege read access.
- Jira results are reconciled against an approved sample for scope, status history, blockers, velocity, and defects.
- Any discrepancy is resolved or documented before enabling the production schedule.

### T-044 — Complete security, privacy, and operations review

**Depends on**: T-041–T-043
**References**: Constitution Principles II–VI; specification sections 8–9

**Acceptance criteria**

- Review confirms credentials are absent from source, frontend bundles, images, logs, reports, and database records.
- Authorization, report retention/access, backup/recovery, migrations, health checks, and operational alerts meet approved requirements.
- No Jira writes, Confluence writes, email, or publication are enabled.

### T-045 — Publish runbook and pass the release gate

**Depends on**: T-042–T-044
**References**: Plan milestone M6; SC-001–SC-010

**Acceptance criteria**

- Documentation covers configuration, startup/shutdown, schedule operations, manual recovery, failure response, and report review/distribution.
- Each success criterion SC-001–SC-010 has recorded verification evidence.
- Production scheduling is enabled only after the approved configuration, access, and recovery checks pass.

**Milestone M6**: Production release criteria are met and the report remains a human-reviewed draft.

## Dependency Summary

- **M0 gate**: T-001–T-007 → T-008.
- **M1 gate**: T-009–T-014.
- **M2 gate**: T-015–T-020.
- **M3 gate**: T-021–T-028.
- **M4 gate**: T-029–T-036.
- **M5 gate**: T-037–T-040.
- **M6 gate**: T-041–T-045.

Tasks within a phase may proceed in parallel when their listed prerequisites are complete. Production scheduling and release tasks remain blocked until the preceding verification and approval gates pass.

