name: validate-instructions
description: Defines the task, files to check, validation checks, and output format for systematic file and result validation.
metadata:
    version: "1.0"
---

# Validation and Processing Instructions

## 1. Task Definition
Perform a systematic review, validation, and quality check on a set of generated or processed files according to predefined criteria. Ensure consistency, accuracy, and adherence to required formats across all outputs.

## 2. Target Files
- **Input / Source Files:** Specify the directory or pattern of files to be reviewed (e.g., `outputs/*.md`, `data/*.json`).
- **Processing Approach:** Use **Approach 3** (Process each file individually using a dedicated processing script or iterative prompt) to ensure deep, isolated analysis of every file.

## 3. Validation Checks
Perform the following checks on each target file:
1. **Structure & Schema Compliance:** Verify that all required sections, headers, keys, or fields are present and correctly formatted.
2. **Data Accuracy & Consistency:** Check internal consistency of data points, references, and claims across the file.
3. **Completeness:** Ensure no placeholders, missing values, or TODOs remain in production-ready files.
4. **Formatting & Syntax:** Validate markdown syntax, code block formatting, JSON/YAML validity, or any specific domain-related formatting rules.

## 4. Output Format
For each file processed, output a validation report structured as follows:

```markdown
### Validation Report: [File Name]
- **Status:** [Passed / Failed / Needs Review]
- **Checks Performed:**
  - [x] Structure & Schema Compliance
  - [x] Data Accuracy & Consistency
  - [x] Completeness
  - [x] Formatting & Syntax
- **Identified Issues:**
  - *(List any inconsistencies, errors, or formatting defects found, or state "None")*
- **Refinement Actions Taken:**
  - *(Describe any corrections made or recommended adjustments to the instruction file)*
 
---