---
name: review-r
description: Run the R code review protocol on R scripts. Checks code quality, reproducibility, domain correctness, and professional standards. Produces a report without editing files.
argument-hint: "[filename or 'all']"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Task"]
---

# Review R Scripts

Run the comprehensive R code review protocol.

## Steps

1. **Identify scripts to review:**
   - If `$ARGUMENTS` is a specific `.R` filename: review that file only
   - If `$ARGUMENTS` is `all`: find all `.R` files via `**/*.R` glob
   - If `$ARGUMENTS` is a directory: review all `.R` files in that directory

Before drafting the final report, read [../_shared-writing/anti-ai-writing-standard.md](../_shared-writing/anti-ai-writing-standard.md).

2. **For each script, launch the `r-reviewer` agent** with instructions to:
   - Follow the full protocol in the agent instructions
   - Follow the `r-code-conventions` rule for current standards
   - Save report to `output/` if it exists, otherwise print to screen

3. **After all reviews complete**, present a summary:
   - Total issues found per script
   - Breakdown by severity (Critical / High / Medium / Low)
   - Top 3 most critical issues
   - Keep the prose plain and specific; avoid generic audit language that could fit any script

4. **IMPORTANT: Do NOT edit any R source files.**
   Only produce reports. Fixes are applied after user review.
