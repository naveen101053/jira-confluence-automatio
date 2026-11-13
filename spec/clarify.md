# Specification Review: Gaps, Contradictions, and Clarifications

**Review date**: 2026-11-13 | **Reviewed**: [constitution.md](./constitution.md), [specification.md](./specification.md)
**Compared with source**: [project_spec.md](../project_spec.md)

## Summary

The specification captures the core weekly-report behavior, stack, and safety constraints, but it is **not yet fully implementation- or production-ready**. Several requirements depend on configuration or policy that is not defined, and some requirements offer alternatives without choosing one. The most important clarifications are the manual-run/report-date rules, Jira issue and sprint scopes, forecast behavior, web authorization, and report persistence/recovery.

Priority meanings:

- **P0 — Blocking**: resolve before implementing the affected behavior or enabling production runs.
- **P1 — Major**: resolve before acceptance testing or production deployment.
- **P2 — Clarification**: resolve to make implementation, review, or ongoing governance consistent.

## P0 — Blocking Decisions

### 1. Python source specification conflicts with the selected application stack

The source [project_spec.md](../project_spec.md), especially sections 6–7, specifies a Python application, CLI-style processing, and an operating-system scheduler. [specification.md](./specification.md) instead requires React 18/Vite, Node.js/Express, PostgreSQL, a web UI, and a backend scheduler. The new specification says it supersedes the Python proposal, but the original document remains present without a superseded/deprecated marker. Contributors may follow conflicting source requirements.

**Clarify**: Is `spec/specification.md` the sole implementation authority, with `project_spec.md` retained only as historical input? If so, mark the old technical proposal as superseded or update it. Confirm whether any source requirements—such as manual CLI execution—remain in scope.

### 2. Report date and reporting window are ambiguous for manual or delayed runs

FR-007 defines a window relative to the report date but does not require the report date to be Monday. The acceptance scenarios describe a Monday run. The manual-run story does not say whether users select a report date, whether it defaults to today, or how a run on a Tuesday/after downtime chooses the “preceding” reporting week. A delayed scheduled run also has no stated report-date rule.

**Clarify**: Must every report date be a Monday? For manual/recovery runs, can an authorized user select a Monday report date, and what is the default? Does a late scheduled run retain its intended Monday report date or use its actual run date? Define how the reporting period and filename derive from that date.

### 3. Jira project scope for defects and velocity is unresolved

FR-001 and FR-002 scope weekly completed and blocked work to `TCL` Stories with the exact label `Ready for deployment`. FR-012 does not state whether Priority 1 defects are limited to `TCL`, to the same label, or searched across other projects. FR-014 defines velocity over completed Stories but does not resolve its scope. FR-015 makes velocity scope configurable, while the open-decisions section explicitly leaves the choice unresolved.

**Clarify**:

- Which project(s), issue types, and labels are included in the critical-defect search?
- Should velocity use all `TCL` Stories or only `TCL` Stories with `Ready for deployment`? Define the production default and whether it can vary by board.
- Are defects included in the Jira issue type `Story` retrieval or queried separately?

### 4. Web application identity and authorization are unspecified

User Story 5 and section 9 say users must be authorized, and the constitution requires backend authorization, but no authentication method, user roles, access boundary, or authorization policy is defined. The UI can trigger Jira queries and display potentially sensitive assignee names, blocker reasons, and issue links.

**Clarify**: Who may view reports and trigger manual runs? Is there one administrator/Scrum Master role or multiple roles? What identity provider/session mechanism is required? Is the application local-only or reachable by a team? Define the authorization behavior for report download and run-history access.

### 5. Jira status, field, board, and blocked-work configuration is not defined

The spec makes completed/resolved statuses, board IDs, story-point field, blocked rule, blocker reason, and defect types configurable, but it does not define their accepted representations, validation rules, precedence, or whether the service may start without them. The Jira site, credentials, and production values are also open.

**Clarify**: Define a configuration schema and validation behavior. Specify whether status IDs, exact names, or status categories are used; how a blocked status/field/label rule is expressed; how a blocker reason is extracted; and which values are required to enable each report section. State whether missing production-critical configuration blocks a run or yields an explicitly partial report.

### 6. Forecast rules do not fully define which backlog stories fit

FR-018 and section 5 introduce Jira sprint order and rank, which were not specified in the source requirements. They define an ordered prefix, but not the outcome when the next story exceeds remaining capacity, whether later smaller stories may be skipped, or how stories without estimates affect the count. The “upcoming quarter” is not anchored to a quarter start date, and sprint inclusion at the quarter boundary is undefined.

**Clarify**:

- Confirm that sprint order and Jira rank are the intended prioritization order.
- Decide whether the forecast stops at the first story that does not fit or skips it and considers later stories.
- Define which sprint dates qualify as “before quarter end,” including sprints that straddle the date and the current sprint.
- Define whether the horizon is the current quarter or the next quarter, and how the quarter start/end are selected.
- Define the result when one or more backlog estimates are missing: show only point capacity, show a lower-bound count, mark the whole fit count unavailable, or another rule.

### 7. The initial Confluence scope needs an explicit product decision

The constitution describes a Jira/Confluence automation project, but the specification explicitly excludes all Confluence reads and writes because the source requirements contain no Confluence workflow. This is a valid MVP boundary, but it leaves the project title broader than the implemented feature and does not establish whether Confluence is a later release goal.

**Clarify**: Confirm Jira-only scope for this release and whether Confluence integration is intentionally deferred. If Confluence is expected in this release, define the source/destination, user workflow, permissions, content format, and side-effect confirmation requirements before adding it.

## P1 — Major Requirements Gaps

### 8. Sprint and completion semantics are incomplete

FR-008 defines weekly completion through status history, while FR-014 says stories are “completed in that sprint.” The spec does not define how sprint completion is identified, which status transition qualifies for sprint velocity, how reopened stories are handled across sprints, how issues moved between sprints are attributed, or how multiple sprint memberships are deduplicated.

**Clarify**: Define sprint identity/status/date rules, the completion event used for sprint totals, the attribution rule for moved/reopened issues, and how the system distinguishes a valid zero-point sprint total from missing estimate/history data.

### 9. Blocked and critical-defect report fields are underspecified

FR-011 says to include “relevant dates” without naming them. It does not distinguish required fields from optional fields, define formatting, or specify fallback behavior for a missing issue key/title/link. Critical defects are required to be listed prominently, but their required displayed details are not defined.

**Clarify**: Enumerate the required date fields (for example, created, updated, due, or blocked-since), their source and timezone, and the display fields for critical defects. Define which missing fields cause a data-quality caveat versus prevent the item from being reported.

### 10. Configuration ownership and persistence are unclear

FR-025 says PostgreSQL stores application configuration, while the technical constraints require environment-specific configuration and sensitive credentials to use an environment/secret mechanism. No precedence or ownership is defined for values supplied in the environment versus the database. The spec also does not say who can edit configuration or whether configuration changes are audited.

**Clarify**: Separate non-secret operational settings from secrets, identify the source of truth for each, define precedence and validation, and state whether configuration is editable through the UI or deployment-only. Define who may change it and whether changes require an audit record.

### 11. Report artifact storage and database consistency need a deployment contract

The Markdown artifact is stored under relative path `reports/`, while PostgreSQL stores run metadata. The spec does not say how that directory is mounted/persisted in Docker or production, how a deployed backend serves/downloads files, or how to recover if a file write succeeds but the database status update fails (or vice versa). File and database updates cannot be made atomic as one transaction.

**Clarify**: Define the durable storage location and volume/backup/retention policy, how artifact access is authorized, and reconciliation behavior for orphaned files or run rows. Specify when the run becomes successful and how a crash between file write and database update is recovered.

### 12. Duplicate and concurrent run behavior is undecided

FR-021 allows either a unique versioned filename or an explicit failure for a repeated report date. It does not select one behavior or define the suffix format. No requirement prevents overlapping scheduled and manual runs, multiple scheduler instances, or concurrent writes to the same report date.

**Clarify**: Choose one repeat-run policy and define stable filenames. Specify whether runs for the same date are serialized, rejected, or allowed concurrently; how duplicate scheduler delivery is prevented; and whether a manual retry may intentionally create a new report version.

### 13. Scheduler ownership and recovery behavior remain open

The spec requires backend scheduling but leaves the scheduler host, service availability, and missed-run policy to deployment. It does not define startup behavior, duplicate scheduling in multiple backend instances, daylight/timezone handling at deployment, or operator notification for a missed/failed run.

**Clarify**: Identify the deployment model and scheduler owner, how only one scheduled execution is guaranteed, whether missed runs are skipped or caught up, and how operators learn that a run was missed or failed. Define whether running the API without the scheduler is supported.

### 14. Partial data versus run failure is not consistently defined

FR-003/FR-004 say required query failures must be surfaced, while FR-016 allows unavailable/provisional velocity and forecast. The user-story scenarios allow either unavailable or provisional results, but do not say whether incomplete sprint or forecast data still permits a successful report. “Required” and “optional” query/field categories are not enumerated.

**Clarify**: List data required for a successful report versus data that may be omitted with a caveat. Define when incomplete Jira fields produce a successful-but-qualified report and when the whole run fails. Include the valid empty-result case so a legitimate zero-work week is distinguishable from a failed or incorrectly filtered query.

### 15. Error handling and retry limits lack operational parameters

The spec requires bounded retries and actionable errors but gives no timeout, retry-count/backoff ceiling, Jira rate-limit handling details, or classification of retryable responses. It also does not define run status transitions or sanitized error detail shape. SC-009 requires a failed run record “where possible,” which leaves behavior during a PostgreSQL outage unspecified.

**Clarify**: Set retry/timeout policy or explicitly defer it to implementation with acceptance bounds. Define run states and terminal transitions, what users see for each failure category, and how failures are observable when the database cannot record the run.

### 16. Report content and UI behavior are not fully testable

“Concise,” “one page where practical,” “relevant dates,” “prominently,” and “actionable” are subjective. FR-023 says users can review/download reports but does not specify whether Markdown is rendered or shown raw, how errors and long-running jobs are refreshed, or whether downloads preserve the original Markdown.

**Clarify**: Define the required visual prominence and report rendering behavior. Specify how manual-run status updates reach the UI, the expected states and transitions, and whether download returns the original artifact or a rendered/exported form. Keep the one-page target advisory unless a measurable layout constraint is required.

### 17. Security and privacy controls need enforcement details

The spec says report access is restricted and data is local, but does not define authentication, authorization, network exposure, TLS, session protection, rate limiting for manual-run endpoints, report retention/deletion, or whether generated Markdown is excluded from Git. Reports contain potentially sensitive Jira content and may be committed with repository changes.

**Clarify**: Decide network exposure and transport/session controls, endpoint authorization and abuse limits, report retention/deletion, and repository ignore/access policy for generated reports. Define whether audit events record who triggered or downloaded a report without storing issue content.

### 18. Non-functional and operational acceptance criteria are missing

The spec has no explicit requirements for maximum report duration/issue volume, UI/API availability, health checks, backup/restore, database migration deployment, supported Node.js version, or resource limits. These may be implementation decisions, but the expected operating envelope is unknown.

**Clarify**: State expected project/issue volume and acceptable run completion time, deployment/availability expectations, backup/restore responsibility, supported runtime versions, and operational health/alerting requirements—or explicitly defer them from the initial release.

## P2 — Constitution and Governance Clarifications

### 19. Several constitutional principles are not objectively reviewable

Terms such as “important outputs,” “appropriate authorization,” “consequential,” “safe local defaults,” “unnecessary sensitive content,” and “bounded retries where safe” have no criteria. This is acceptable as principle-level language, but teams may interpret it differently when deciding whether a feature conforms.

**Clarify**: Add examples or point these terms to project policies (authorization model, logging policy, retry policy, and side-effect review checklist) once those are chosen.

### 20. Governance does not identify amendment authority or approval process

The constitution requires a rationale, version/date update, and impact identification, but does not state who approves amendments, how version numbers change, or how conflicting specifications are resolved. It also does not identify which requirements in the current specification are release gates.

**Clarify**: Define an owner/approver, amendment/versioning convention, and precedence among constitution, feature specifications, and source/background documents. Explicitly identify production-blocking open decisions.

## Recommended Resolution Order

1. Resolve the report-date/manual-run contract, Jira issue scopes, velocity scope, and forecast policy.
2. Select the web application's identity/authorization model and decide whether Confluence is explicitly deferred.
3. Define required versus optional configuration/data, including blocked and defect classification.
4. Choose artifact persistence, repeat-run/concurrency behavior, scheduler ownership, and recovery semantics.
5. Add measurable acceptance criteria for partial-data success, security/privacy, and operational behavior.
6. Mark the Python proposal in `project_spec.md` as superseded or consolidate the source and feature specification.

