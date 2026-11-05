# How to Fill Out the Weekly Status Report

Use [template.md](./template.md). See [example.md](./example.md) for a completed report. Save the finished report as `reports/weekly-status-YYYY-MM-DD.md` (run date in IST) and never overwrite an earlier report.

## General rules

- Replace every `{{placeholder}}`. Do not leave any in the final report.
- Use IST for all dates and times, formatted `YYYY-MM-DD`.
- Never write `0` for missing data. Write `Not available` and add a line under **Data Caveats**.
- Do not invent values (blocker reasons, links, estimates). Leave `Not available` if Jira does not hold them.
- Keep the report to about one page, but never drop blocked stories or required sections to do it.
- The report is a draft. Review it before sharing, and share it manually.

## Header

- **Report date:** the Monday the report is generated.
- **Reporting period:** the previous Monday 00:00 through Friday 23:59:59 IST (the window is `[Monday 00:00, Saturday 00:00)`).

## Open Priority 1 Defects

- Include every defect with Jira Priority `1` whose status is not in the configured resolved/completed statuses.
- If there are none, write `None.` and remove the table.
- Keep this section at the top, even when empty.

## Completed Stories

- Scope: project `TCL`, issue type `Story`, label exactly `Ready for deployment` (other labels may also be present).
- Count a story once if its status history shows it entered a completed status during the reporting period, even if it later left that status.
- Do not use current status alone. Exclude stories completed outside the period.
- List one row per assignee, plus an `Unassigned` row (use `0` here only when verified that none exist).
- The **Team total** must equal the sum of the rows.

## Blocked Stories

- Include every in-scope story that is blocked at the time of generation, per the configured blocked rule.
- Fill every column. Use `Not available` for missing values.
- Relevant dates: for example, the date it became blocked or its due date.
- If none are blocked, write `None.` and remove the table.

## Velocity

- Sum story points of stories completed in each of the three most recently completed sprints, then average the three totals.
- If any sprint's data or estimates are missing, write `Not available` and explain in **Data Caveats**.

## Upcoming-Quarter Forecast

- Point capacity = average velocity × planned sprints before the quarter end date.
- Count how many future-backlog stories fit within that capacity (one Story = one business case).
- List all inputs and assumptions. Keep the label `PROVISIONAL`.
- If quarter dates, sprint plans, or estimates are missing, mark the forecast `Not available`.
- Do not state or imply that a story will be delivered.

## Data Caveats

- List each missing or incomplete data item and the metric it affects.
- Always keep the line saying the forecast is provisional.
