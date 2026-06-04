---
name: r-to-latex-tables
description: Generate publication-quality LaTeX tables from R regression models (fixest, lm, glm). Use when R scripts produce .tex table files, when converting modelsummary/stargazer output to match Stata esttab style, or when building programmatic R-to-LaTeX table pipelines for econometrics papers.
---

# R-to-LaTeX Tables

## Quick Start

This skill creates **R helper functions** that extract regression results from model objects and write publication-ready `.tex` files in the traditional `threeparttable` + `tabular` style used by Stata's `esttab`. It replaces `modelsummary`/`tabularray` output with hand-controlled LaTeX.

## When to Use

- R scripts generate `.tex` table files from regression output
- Tables need to match Stata `esttab` style (double `\hline`, `\cmidrule`, `\multirow`)
- `modelsummary` or `stargazer` output needs restyling
- Table notes are missing or need customization
- Multiple table layouts needed (standard, paneled, stratified)

## Core Pattern

The pipeline has three layers:

```
Model objects (fixest/lm/glm)
  → Extraction (summary()$coeftable)
    → Formatting (adaptive precision + stars)
      → LaTeX assembly (threeparttable template)
        → writeLines() to .tex file
```

**Never use `modelsummary(..., output = "file.tex")` if you need Stata-style output.** It produces `tabularray` tables that look different and lack proper table notes.

## Required LaTeX Packages

Ensure the paper's preamble includes:

```latex
\usepackage{booktabs}        % \cmidrule
\usepackage{threeparttable}  % tablenotes
\usepackage{multirow}        % \multirow for coefficient labels
```

## Formatting Functions

### Adaptive Coefficient Formatting

Stata shows at least 2 significant digits. Fixed 3-decimal formatting loses information for small coefficients (e.g., `0.00027` becomes `0.000`). Use adaptive precision:

```r
format_coef_value <- function(x) {
  ax <- abs(x)
  if (ax < 1e-10) return(formatC(x, format = "f", digits = 3))
  if (ax >= 1)    return(formatC(x, format = "f", digits = 3))
  leading_zeros <- floor(-log10(ax))
  d <- max(leading_zeros + 2, 3)  # at least 2 sig digits
  d <- min(d, 5)                  # cap at 5 decimal places
  formatC(x, format = "f", digits = d)
}
```

**Examples:** `0.041` → `"0.041"`, `-0.0062` → `"-0.0062"`, `0.00027` → `"0.00027"`

### Stars and Standard Errors

```r
format_coef_star <- function(coef_val, pval) {
  val <- format_coef_value(coef_val)
  stars <- if (pval < 0.01) "***"
           else if (pval < 0.05) "**"
           else if (pval < 0.10) "*"
           else ""
  paste0(val, stars)
}

format_se_paren <- function(se_val) {
  paste0("(", formatC(se_val, format = "f", digits = 3), ")")
}

format_nobs <- function(n) {
  formatC(n, format = "d", big.mark = ",")
}
```

## Extracting from Models

Use `summary(model)$coeftable` — it works reliably for `fixest`, `lm`, and `glm`:

```r
ct <- summary(model)$coeftable
ct[coef_name, "Estimate"]    # coefficient
ct[coef_name, "Std. Error"]  # standard error
ct[coef_name, "Pr(>|t|)"]   # p-value
nobs(model)                  # observations
```

**Do not rely on** `coef()` + `se()` + `pvalue()` separately — `se()` may not exist as an exported generic in all packages. The coeftable is always available.

## Table Structure Templates

### Standard 4-Column Table (Formal/Informal, Employment/Wage)

The most common layout for DiD papers with treatment/control across sectors:

```
\begin{center}
  \begin{threeparttable}
    \begin{tabular}{...}
      \hline\hline
      & Formal (col 1-2) & Informal (col 3-4)   ← \cmidrule groups
      & (1) & (2) & (3) & (4)                   ← column numbers
      & Employment & Real Wage & ...              ← outcome labels
      \hline
      \multirow{2}{*}{Label} & coef & coef & ...  ← coefficient row
                              & (se) & (se) & ...  ← SE row
      \hline
      Observation & N & N & N & N
      \hline\hline
    \end{tabular}
    \begin{tablenotes}[para,flushleft]            ← table notes
      \footnotesize
      \item \textbf{Note:} ...
    \end{tablenotes}
  \end{threeparttable}
\end{center}
```

For full R function code for each layout, see [table-templates.md](table-templates.md).

### Other Layouts

- **Paneled table** — Multiple treatment groups (e.g., age 18-20 vs 21-24), each with their own coefficient + SE + observation rows
- **Stratified table** — Columns = subgroups (e.g., education levels), rows = different outcomes with per-outcome observation counts

## Table Notes

**Table notes are mandatory.** Every empirical table must have a `\begin{tablenotes}` block specifying:

1. Data source and time period
2. Target and control group definitions
3. Control variables included
4. Fixed effects used
5. Standard error clustering
6. Significance levels

Pass notes as a character vector (one line per sentence) for source readability:

```r
table_note = c(
  "It is used the rounds of THLFS between 2016 and 2019 in these models.",
  "The target group consists of male aged between 18-24, ...",
  "These models include full interaction of marital status, age and four education categories.",
  "Additionally, year, region fixed effects and regional trend were used in all models.",
  "Robust standard errors are clustered by NUTS2 region classification ...",
  "***,** and * indicate significance levels of \\%1, \\%5 and \\%10, respectively."
)
```

## Writer Function Architecture

Each project should have a `helpers_did.R` (or similar) with:

1. **Formatting functions** — `format_coef_value()`, `format_coef_star()`, `format_se_paren()`, `format_nobs()`
2. **Table writers** — One function per layout type, taking model list + coef_map + note + filename
3. **No dependency on `modelsummary`** — Pure R + `writeLines()` for full control

Writer function signature pattern:

```r
write_did_table <- function(models,      # list of feols/lm models
                            coef_map,    # named char vec: R name → display label
                            table_note,  # char vector of note lines
                            filename,    # output file name
                            row_spacing = FALSE)  # [0.5em] between coef groups
```

The function:
1. Extracts coeftable from each model
2. Formats coefficients with adaptive precision + stars
3. Formats SEs in parentheses (fixed 3dp)
4. Assembles the LaTeX template with `sprintf()`
5. Writes with `writeLines()`

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| `modelsummary` produces `tabularray` not `tabular` | Use custom writer functions |
| Missing table notes | Always include `tablenotes` block |
| `\num{}` from siunitx wrapping | Don't use siunitx for coefficients |
| Small coefficients show as `0.000` | Use `format_coef_value()` adaptive precision |
| Missing `\usepackage{booktabs}` | Crashes on `\cmidrule` — add to preamble |
| `\multirow` without package | Add `\usepackage{multirow}` |
| Observation counts without commas | Use `formatC(n, format = "d", big.mark = ",")` |
| `se()` not found | Use `summary(m)$coeftable[, "Std. Error"]` instead |

## Checklist

Before delivering tables:

- [ ] Uses `threeparttable` + `tabular` (not `tabularray`)
- [ ] Has `\hline\hline` at top and bottom (not `\toprule`/`\bottomrule`)
- [ ] Has `\cmidrule(lr)` for column group headers
- [ ] Coefficient labels use `\multirow{2}{*}{...}`
- [ ] Table notes present with data/sample/controls/FE/SE/stars info
- [ ] Observations formatted with commas
- [ ] Small coefficients show 2+ significant digits
- [ ] All required LaTeX packages declared in preamble
- [ ] `.tex` files are fragments (no `\begin{document}`) for `\input{}` inclusion
