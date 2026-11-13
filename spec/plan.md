# Implementation Plan: Weekly Jira Status Report Automation

**Status**: Draft | **Basis**: [specification.md](./specification.md) | **Review findings**: [clarify.md](./clarify.md)
**Governing principles**: [constitution.md](./constitution.md)

## Plan Principles

- Implement the approved React 18/Vite, Node.js/Express, and PostgreSQL 15/Docker stack. Do not start a parallel Python implementation.
- Preserve and reuse existing application code where it satisfies the approved requirements; inspect current code and tests before replacing or duplicating behavior.
- Keep Jira access read-only and credentials server-side. Do not add Confluence operations to this release unless its scope is explicitly redefined and approved.
- Complete the blocking decisions in Phase 0 before implementing behavior that depends on them.
- Do not enable production scheduling until authorization, configuration, artifact persistence, and recovery behavior are verified.
- No calendar estimates are included because staffing, deployment target, and unresolved decisions are not specified.

## Phase 0 — Baseline and Decision Closure

**Objective**: Establish one authoritative specification and resolve requirements that would otherwise force implementation guesses.

**Work**

1. Inventory the current frontend, backend, tests, Docker setup, and reusable report calculations. Record which specification requirements are already implemented and which need changes.
2. Confirm that `spec/specification.md` is the implementation authority and mark the Python proposal in `project_spec.md` as superseded or consolidate the documents.
3. Decide the report-date contract for scheduled, delayed, and manual runs, including manual date selection and filename derivation.
4. Confirm the Jira scope for defects and velocity; select the velocity scope.
5. Define the forecast horizon, eligible sprints, issue ordering, handling of a story that exceeds remaining capacity, and missing-estimate behavior.
6. Define required versus optional Jira configuration/data and whether incomplete data can still produce a successful qualified report.
7. Choose the web identity/authorization model, access boundary, and whether Confluence is explicitly deferred.
8. Select the repeat-run and concurrency policy, artifact storage/retention, scheduler ownership, and missed-run recovery behavior.
9. Define configuration ownership/precedence and production Jira field/status mappings.

**Milestone M0 — Approved implementation baseline**

- Blocking questions in [clarify.md](./clarify.md) are answered or explicitly deferred from the release.
- The specification contains a single source of truth for stack, run semantics, data scope, authorization, and release gates.
- Jira credentials, report retention, and deployment ownership have approved handling.

**Exit gate**: Do not start dependent implementation while report-date semantics, Jira scopes, forecast rules, or authorization remain unresolved.

## Phase 1 — Application and Data Foundation

**Objective**: Make the chosen stack reproducible and establish stable contracts between the frontend, backend, and database.

**Work**

1. Align existing project structure and package/build scripts with React 18/Vite and Node.js/Express; preserve current useful TS/TSX modules and tests.
2. Add or verify Docker-based PostgreSQL 15 development setup, persistent local data, health checks, and safe environment configuration.
3. Establish database migrations and schema for application configuration and report-run metadata, with constraints and transaction boundaries.
4. Define backend API contracts for configuration validation, report-run creation/status/history, and report retrieval/download.
5. Implement the approved authentication and authorization boundary before exposing report data or manual-run operations.
6. Add baseline lint, type-check, unit-test, and build commands using the repository's existing conventions.

**Milestone M1 — Reproducible application foundation**

- Frontend, backend, and PostgreSQL start in the documented local environment.
- Database migrations can be applied on a fresh database and preserve required data on restart.
- API contracts and authorization behavior are documented and covered by focused tests.
- No Jira credential is present in frontend code or tracked configuration.

## Phase 2 — Jira Cloud Integration

**Objective**: Retrieve only the approved read-only data, with complete pagination and explicit failure behavior.

**Work**

1. Implement or adapt a server-side Jira client using the approved credential mechanism and least-privilege access.
2. Validate Jira URL, project/board identifiers, status mappings, field IDs, blocked rule, and configured velocity/defect scopes at startup or run time.
3. Retrieve weekly issue fields, status changelogs, defect data, completed sprint history, and planned future sprint/backlog data required by the approved configuration.
4. Handle pagination, rate limits, timeouts, and bounded retries for safe transient failures.
5. Normalize Jira responses into internal typed data structures; preserve relevant timestamps and source context.
6. Add mocked integration tests for pagination, changelogs, permissions, rate limits, partial responses, and malformed/missing fields.

**Milestone M2 — Jira data contract verified**

- All required Jira datasets can be retrieved without truncation.
- Authentication/permission/query failures are distinguishable from legitimate empty results.
- The Jira client exposes only required read operations; tests and code review verify there are no Jira write operations and that secrets are not logged or returned to the browser.

## Phase 3 — Report Domain Rules and Calculations

**Objective**: Implement and verify deterministic calculations independently of live Jira calls.

**Work**

1. Implement report-date and half-open reporting-window calculations in `Asia/Kolkata`, including the approved manual and delayed-run rules.
2. Implement exact project/type/label filtering for weekly scope.
3. Count completed Stories once from configured status-history transitions; group by assignee, include `Unassigned`, and reconcile to the total.
4. Identify currently blocked in-scope Stories using the approved blocked rule and retain available details without fabricating missing values.
5. Calculate the three-sprint velocity using the approved sprint and issue attribution rules; distinguish genuine zero totals from incomplete data.
6. Calculate point capacity and story fit using the approved quarter and backlog ordering policy; surface assumptions and incomplete inputs.
7. Identify open Priority 1 defects using the approved project/type/status scope.
8. Add focused unit tests for boundaries, reopened/moved issues, deduplication, missing data, zero values, and forecast edge cases.

**Milestone M3 — Calculation rules accepted**

- Domain tests cover all defined business rules and edge cases.
- Results are deterministic for the same normalized inputs.
- No unknown estimate, missing field, or failed query is silently treated as zero or as an empty successful result.

## Phase 4 — Report Generation, Persistence, and Run Orchestration

**Objective**: Turn verified Jira data and calculations into durable, traceable Markdown report runs.

**Work**

1. Implement the Markdown renderer with all required report sections, placeholders, provenance, forecast assumptions, and data-quality caveats.
2. Implement report-file creation in the approved durable location using an atomic write and the agreed repeat-run naming policy.
3. Persist report-run metadata and lifecycle status in PostgreSQL; associate each successful run with its artifact.
4. Implement orchestration that records trigger type, report date/window, timestamps, output path, and sanitized failures.
5. Add protection against duplicate scheduled triggers and overlapping manual/scheduled runs according to the Phase 0 decision.
6. Implement backend operations for manual triggering, run status/history, and authorized report retrieval/download.
7. Add failure and recovery handling for database/file inconsistencies, including a defined response when run metadata cannot be persisted.
8. Add tests for report content, file naming, repeat runs, atomic writes, run transitions, authorization, and persistence failures.

**Milestone M4 — End-to-end backend report run**

- A controlled Jira fixture can produce a complete Markdown artifact and corresponding successful run record.
- Failed retrieval, calculation, persistence, or file writes do not produce a misleading successful report or overwrite an earlier artifact.
- Run history and artifact access follow the approved authorization and retention rules.

## Phase 5 — Web Review and Manual Operations

**Objective**: Enable authorized users to initiate and review report runs safely.

**Work**

1. Implement the React dashboard for report history and run details.
2. Add the manual-run flow using the agreed report-date and repeat-run behavior.
3. Display queued/running/succeeded/failed states, useful timestamps, and sanitized actionable errors.
4. Render or display the Markdown report according to the approved UI decision and provide the original artifact download.
5. Provide clear loading, empty, success, and error states; ensure keyboard operation and accessible labels.
6. Verify authorization for dashboard, manual-run, history, and download actions.
7. Add frontend tests for user workflows, accessibility basics, API errors, and status refresh behavior.

**Milestone M5 — Authorized review workflow complete**

- An authorized Scrum Master can trigger a manual run, monitor it, review the report, and download the artifact.
- Unauthorized requests cannot trigger runs or retrieve reports.
- UI states and controls meet the constitution's accessibility and error-visibility requirements.

## Phase 6 — Scheduling, Integration Validation, and Release Readiness

**Objective**: Verify the full application in a controlled environment and enable production use only after operational gates pass.

**Work**

1. Implement the approved Monday 09:00 `Asia/Kolkata` schedule in the selected deployment model.
2. Verify single-execution behavior, missed-run policy, service restart behavior, and manual recovery.
3. Run end-to-end tests across React, Express, PostgreSQL, report storage, and mocked Jira services.
4. Perform a manual integration test against a non-production Jira project or approved test dataset.
5. Validate logs, browser bundles, Docker configuration, database records, and generated files for credential or unnecessary issue-data exposure.
6. Verify report retention, backup/recovery, migrations, health checks, and operational alerting against the approved deployment requirements.
7. Run the required automated tests, type-check, lint, and production builds; resolve failures before release.
8. Document configuration, startup/shutdown, scheduler operations, failure recovery, and Scrum Master review/distribution responsibilities.

**Milestone M6 — Production release gate passed**

- SC-001 through SC-010 in [specification.md](./specification.md) are demonstrably satisfied.
- Production configuration and least-privilege Jira access are reviewed.
- Scheduled execution, recovery behavior, artifact durability, and authorized report access are verified.
- No automatic email, publication, Jira writes, or Confluence writes are enabled.

## Dependency and Milestone Sequence

`M0 → M1 → M2 → M3 → M4 → M5 → M6`

The UI may be prototyped against agreed API contracts during Phases 2–4, but it MUST NOT be considered complete until M4's run lifecycle and authorization behavior are stable. Production scheduling is gated on M6; it is not enabled as a side effect of local development setup.

## Cross-Phase Traceability

| Phase | Primary specification coverage |
|---|---|
| Phase 0 | Section 12 assumptions/open decisions; `clarify.md` P0 findings |
| Phase 1 | FR-023–FR-025; technology constraints; authorization and persistence foundations |
| Phase 2 | FR-001–FR-005, FR-010, FR-012, FR-015 |
| Phase 3 | FR-006–FR-019; SC-001–SC-007 |
| Phase 4 | FR-020–FR-022, FR-025–FR-026; SC-008–SC-009 |
| Phase 5 | FR-023–FR-024; User Story 5; accessibility/security requirements |
| Phase 6 | FR-004, FR-006, FR-026; SC-001–SC-010; verification and operational requirements |

