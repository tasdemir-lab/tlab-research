---
name: proofread
description: Run the proofreading protocol on academic documents. Checks grammar, typos, consistency, math notation, and academic writing quality. Produces a report without editing files.
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Proofread Academic Documents

Run the mandatory proofreading protocol on academic documents. This produces a report of all issues found WITHOUT editing any source files.

## Steps

1. **Identify files to review:**
   - If `$ARGUMENTS` is a specific filename: review that file only
   - If `$ARGUMENTS` is "all": review all documents in `paper/` and `code/*.qmd`

2. **For each file, launch the proofreader agent** that checks for:

   **GRAMMAR:** Subject-verb agreement, articles (a/an/the), prepositions, tense consistency
   **TYPOS:** Misspellings, search-and-replace artifacts, duplicated words
   **CONSISTENCY:** Citation format, notation, terminology
   **ACADEMIC QUALITY:** Informal language, missing words, awkward constructions
   **MATH NOTATION:** Symbol consistency, undefined notation, equation numbering

3. **Produce a detailed report** for each file listing every finding with:
   - Location (line number or section title)
   - Current text (what's wrong)
   - Proposed fix (what it should be)
   - Category and severity

4. **Save each report** to `_lab/evaluations/`:
   - For `.tex` files: `_lab/evaluations/FILENAME_proofread_report.md`
   - For `.qmd` files: `_lab/evaluations/FILENAME_qmd_proofread_report.md`

5. **IMPORTANT: Do NOT edit any source files.**
   Only produce the report. Fixes are applied separately after user review.

6. **Present summary** to the user:
   - Total issues found per file
   - Breakdown by category
   - Most critical issues highlighted
