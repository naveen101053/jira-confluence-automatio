# QA Report

**Application:** Costing Workbench weekly delivery dashboard  
**Test date:** 2026-11-13  
**Environment:** Docker Compose; Chrome; `http://127.0.0.1:5174/`

## Summary

The dashboard loads successfully and the development stack is running. The report-generation flow could not be completed: the page has no forms or input fields, no submit controls, and the **Generate report** button is disabled. The UI explicitly identifies its figures as fictional preview data and says it is not connected to Jira or a report service.

## Pages visited

| Page | Result |
|---|---|
| Overview (`/`, then `/#overview`) | Loaded successfully. Clicked the Overview navigation link and captured a full-page screenshot in Chrome. |
| Reports | Not available; the navigation button is disabled and marked “Soon.” |
| Settings | Not available; the navigation button is disabled. |

Only Overview is implemented as an accessible page in the current UI.

## Elements and flows tested

- Inspected the Overview page and its accessible element tree.
- Confirmed there are **0 forms**, **0 input/select/textarea fields**, and **0 submit controls**.
- Confirmed **Generate report**, the date-range control, **View report**, **View all**, **Reports**, and **Settings** are disabled.
- Identified enabled controls: **Notifications** and **Dismiss preview notice**. The report submission flow is unavailable, so no form was filled and no submit action could be performed.
- Identified links: Costing Workbench home, Overview, two blocker-story titles, and the Priority 1 defect title.
- The project switcher and “View setup guide” appear in the UI but are not exposed as links or buttons.

## Checks and results

| Check | Result |
|---|---|
| Frontend page request | Pass — HTTP 200 at `http://127.0.0.1:5174/`. |
| Backend health endpoint | Pass — HTTP 200 at `http://127.0.0.1:8000/health`; response reports `mode: health-only` and `reporting: not-implemented`. |
| Browser console | Pass — no console errors or warnings found after reloading the starting page. |
| Frontend build/type check (`npm run build --prefix .\frontend`) | Pass. |
| Backend syntax (`python -m py_compile .\backend\app.py`) | Pass. |
| Compose configuration (`docker compose config --quiet`) | Pass. |
| Compose services | Pass — backend container healthy; frontend container running. |

The full-page screenshot was captured in Chrome and attached in the conversation; it was not saved to the workspace.

## Bugs and gaps found

1. **Report generation is unavailable (blocker for the main flow).** No form or submission flow exists, and **Generate report** is disabled. The frontend is not connected to the backend or Jira.
2. **Reports and Settings pages are unavailable.** Both navigation controls are disabled; only Overview can be visited.
3. **The backend does not implement reporting.** Its health endpoint is operational, but Jira retrieval, report generation, and a report API are not implemented. Dashboard figures remain sample data.
4. **Compose configuration was initially empty**, preventing the stack from starting.
5. **Host port 5173 was already occupied.** Compose maps the frontend to host port 5174 instead.

## Fixes applied during this session

- Added backend and frontend services to [`../docker-compose.yml`](../docker-compose.yml), including a backend health check and frontend startup dependency.
- Added a clearly identified health-only backend in [`../backend/app.py`](../backend/app.py) and [`../backend/Dockerfile`](../backend/Dockerfile).
- Added the frontend container definition in [`../frontend/Dockerfile`](../frontend/Dockerfile) and excluded local build/dependency artifacts with [`../frontend/.dockerignore`](../frontend/.dockerignore).
- Started the stack successfully. The frontend is available at `http://127.0.0.1:5174/`; the backend health endpoint is at `http://127.0.0.1:8000/health`.

These fixes make the preview stack runnable; they do not implement Jira reporting or enable report generation.

## Current status

**Stack:** Running and healthy for the backend health check.  
**Dashboard:** Loads successfully, but remains preview-only.  
**Main report workflow:** Not testable until a report form/API and Jira integration are implemented and the Generate report control is enabled.  
**Other pages:** Reports and Settings are not available.
