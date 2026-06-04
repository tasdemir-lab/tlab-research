---
name: quarto-academic-gotchas
description: |
  Quarto manuscript pitfalls for academic papers with theorems, proofs, and modular includes.
  Triggers: theorem/proposition numbering problems in PDF, broken @sec- cross-references,
  "Section" rendering without a number, duplicate "Proposition 0.1. Proposition 1." in output.
author: Claude Code Academic Workflow
version: 1.0.0
---

# Quarto Academic Gotchas

Common pitfalls when writing academic manuscripts in Quarto with modular `.qmd` includes, theorem-like environments, and LaTeX table integration.

## Gotcha 1: Theorem Div IDs Cause Duplicate Numbering

### Problem
Using Quarto's div syntax `:::{#prp-name}` around manually labeled propositions creates auto-numbered labels (e.g., "Proposition 0.1") that duplicate the manual text ("**Proposition 1.**"), producing output like:

> Proposition 0.1. **Proposition 1.** Under the model assumptions...

### Trigger
- PDF output shows `Proposition 0.1. Proposition 1.` or `Proposition 0.2. Proposition 2.`
- Source uses `::: {#prp-name}` divs with manual `**Proposition N.**` text inside

### Solution
**Option A (manual numbering, no cross-ref):** Remove the div wrapper entirely. Write propositions as plain bold/italic text:
```markdown
**Proposition 1.** *Under the model assumptions...*
```

**Option B (auto-numbering, with cross-ref):** Use the div but remove the manual label. Let Quarto auto-number:
```markdown
::: {#prp-main}
*Under the model assumptions...*
:::
```
Then reference with `@prp-main`.

**Do not mix both.** Either use divs for auto-numbering or manual labels — never both.

### Verification
Render to PDF and check that propositions appear with a single, clean label.

## Gotcha 2: Cross-References Fail in Included Files

### Problem
Section IDs defined in included `.qmd` files (via `{{< include content/model.qmd >}}`) may not resolve when cross-referenced with `@sec-name`. The PDF renders "Section" with no number, or drops the reference entirely.

### Trigger
- PDF shows "Section uses total separation rates" instead of "Section 4.5 uses total separation rates"
- Source has `@sec-calibration` but `#sec-calibration` is defined in an included file

### Solution
Replace `@sec-` cross-references to sections in included files with plain text:
```markdown
# Instead of:
The calibration in @sec-calibration uses...

# Use:
The calibration below uses...
# Or:
The calibration in Section 4 uses...
```

Table and figure cross-references (`@tbl-`, `@fig-`) defined in included files generally work correctly — this issue is specific to section-level IDs.

### Verification
Search for `@sec-` references and verify each target section ID is in the main document, not an included file.

## Gotcha 3: LaTeX Tables with Labels Conflict with Quarto Divs

### Problem
When a `.tex` table file contains `\caption{...}` and `\label{tab:name}`, and the Quarto source wraps it in a `:::{#tbl-name}` div, Quarto warns:
```
Raw LaTeX table found with non-tbl label: tab:name
```
The table may get double-captioned or have broken cross-references.

### Solution
Remove `\caption` and `\label` from the `.tex` file. Let Quarto handle captions via the div syntax:
```markdown
::: {#tbl-my-table}
` ``{=latex}
{{< include ../output/tables/my-table.tex >}}
` ``
Caption text here
:::
```

The `.tex` file should contain only the `tabular`/`threeparttable` environment, not `\caption` or `\label`.

### Verification
Check generated `.tex` files for `\caption` or `\label` that conflict with Quarto div IDs.

## Gotcha 4: Section Cross-References Resolve to Empty Without `number-sections`

### Problem
`@sec-name` references render as "Section" with no number in the PDF. The text reads "As argued in Section , this..." — the reference silently fails.

### Trigger
- PDF shows "Section ," or "Section " with no number after it
- Source uses `@sec-ols-method` but output shows empty reference
- The YAML does **not** include `number-sections: true`

### Root Cause
Quarto defaults to unnumbered sections (`\setcounter{secnumdepth}{-\maxdimen}`). The `@sec-` mechanism compiles to `\ref{sec-name}`, which requires numbered sections to produce output. Without numbering, `\ref{}` resolves to an empty string — no error, no warning.

### Solution
Add `number-sections: true` at the **top level** of the YAML (not nested under `format:`):
```yaml
number-sections: true
format:
  pdf:
    pdf-engine: xelatex
    ...
```

### Verification
After rendering, search the PDF for "Section " (with trailing space) to catch any empty references.

## Quick Checklist

Before rendering a Quarto academic manuscript:
- [ ] `number-sections: true` is set if using `@sec-` cross-references
- [ ] No `#prp-`/`#thm-` divs around manually numbered theorems
- [ ] No `@sec-` references to sections defined in included files
- [ ] No `\caption`/`\label` in `.tex` table files that Quarto wraps in `#tbl-` divs
- [ ] Proposition/theorem labels don't appear duplicated in PDF
