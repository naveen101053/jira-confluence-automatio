# Jira/Confluence Automation Constitution

## Core Principles

### I. Correctness and Traceability
Automation MUST preserve the meaning and provenance of Jira and Confluence data. Calculations and transformations MUST be deterministic where their inputs are the same, and important outputs MUST make their source, time window, and assumptions clear. Missing, stale, or incomplete data MUST be surfaced rather than silently treated as valid or complete.

### II. Human Control of External Changes
Integrations MUST default to read-only behavior. Creating, editing, transitioning, publishing, or deleting Jira or Confluence content requires an explicitly requested feature and appropriate authorization. Operations with external side effects MUST be previewable and auditable; consequential or irreversible actions MUST require explicit confirmation. Retries MUST NOT duplicate side effects.

### III. Secure by Default
Use least-privilege credentials and keep secrets out of source control, browser code, container images, and logs. Jira and Confluence credentials MUST remain server-side. Validate and authorize requests at the backend, use parameterized database queries, and treat external content as untrusted input. Logs MUST exclude credentials and unnecessary sensitive content.

### IV. Clear Separation of Responsibilities
The frontend MUST present application state and user actions without owning integration credentials or business-critical authorization. The backend MUST own Jira/Confluence access, input validation, business rules, and persistence. Keep integration clients, business logic, API routes, and presentation concerns cohesive and independently testable.

### V. Resilient, Honest Integrations
Jira and Confluence API usage MUST handle pagination, rate limits, timeouts, and transient failures with bounded retries where safe. Authentication, permission, and data errors MUST be reported explicitly; the application MUST NOT return success-shaped empty results when an operation failed. Preserve API limits and avoid unnecessary requests.

### VI. Tested, Accessible User Experience
User-visible behavior MUST provide clear loading, empty, success, and error states. Interfaces MUST support keyboard use and accessible labels. Business rules, integration boundaries, and consequential workflows MUST have focused automated tests. Changes MUST pass the relevant tests and available type-check, lint, and build checks before release.

## Technology and Architecture Constraints

- **Frontend:** React 18 with Vite. Keep provider credentials and privileged operations out of the browser; communicate with the backend through its defined API.
- **Backend:** Node.js with Express. Validate untrusted input at API boundaries and centralize integration and authorization behavior on the server.
- **Database:** PostgreSQL 15, run through Docker for local development. Use versioned schema migrations, database constraints for durable invariants, and transactions for related writes. Persisted state and database credentials MUST be handled separately from disposable container state.
- Keep configuration environment-specific. Provide safe local defaults and document required variables without committing secret values.
- Changes to external APIs, persisted data, or automation behavior MUST include appropriate compatibility and migration considerations.

## Development and Quality Gates

- Prefer small, reviewable changes that preserve existing behavior unless a change is intentional and documented.
- Test business rules independently from live Jira or Confluence services; use controlled fixtures or mocks for automated integration tests.
- Cover failure paths, including permission errors, incomplete responses, rate limits, and database failures, for affected behavior.
- Do not enable a scheduled or production automation path until its authorization, configuration, and external side effects have been verified.
- Update directly related documentation when behavior, configuration, or operational requirements change.

## Governance

This constitution governs project specifications, implementation, and reviews. A more specific requirement may add detail but MUST NOT weaken these principles without an explicit constitution amendment. Amendments MUST state their rationale, update this file's version and date, and identify affected specifications or workflows. Reviewers and contributors are responsible for checking proposed changes against the constitution.

**Version**: 1.0.0  
**Ratified**: 2026-11-13  
**Last Amended**: 2026-11-13
