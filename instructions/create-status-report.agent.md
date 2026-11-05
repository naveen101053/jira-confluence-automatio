---
description: Generate a concise weekly status report in Markdown.
---

# Create Weekly Status Report

Generate a weekly status report using the rules below.

## Format

- Output valid Markdown only.
- Use bullet points only. No paragraphs, tables, or numbered lists.
- Maximum 20 lines in total, including headings and blank lines.

## Sections

Use exactly these three sections, in this order:

1. `## Accomplishments` — work completed this week.
2. `## Blockers` — issues preventing progress. Write `- None` if there are none.
3. `## Next Week` — planned work for the coming week.

## Style

- Use a professional tone.
- Keep each bullet to one short, factual line.
- Lead with the outcome. Include ticket keys or metrics where available.
- No fluff words: avoid filler and intensifiers such as "very", "really", "just", "basically", "amazing", "exciting", "great", "various", "etc.".
- Do not invent information. Use only facts from the provided source data.

## Template

```markdown
# Weekly Status Report — {{YYYY-MM-DD}}

## Accomplishments
- {{Completed item}}

## Blockers
- {{Blocker and owner, or "None"}}

## Next Week
- {{Planned item}}
```
