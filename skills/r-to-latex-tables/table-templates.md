# Table Template Code

Full R function implementations for each table layout.

## Standard 4-Column Table

The workhorse for DiD/causal inference papers. Four outcome columns grouped
under two headers (e.g., Formal/Informal × Employment/Wage).

```r
write_did_table <- function(models, coef_map, table_note, filename,
                            row_spacing = FALSE) {
  stopifnot(length(models) == 4)
  stopifnot(length(coef_map) >= 1)

  path <- here::here("output", "tables", filename)
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)

  cts      <- lapply(models, function(m) summary(m)$coeftable)
  nobs_vec <- sapply(models, nobs)

  coef_names  <- names(coef_map)
  coef_labels <- unname(coef_map)

  coef_lines <- character()
  for (k in seq_along(coef_names)) {
    cn  <- coef_names[k]
    lab <- coef_labels[k]

    if (k > 1 && row_spacing) {
      coef_lines <- c(coef_lines, "                [0.5em]")
    }

    vals <- character(4)
    ses  <- character(4)
    for (j in 1:4) {
      if (cn %in% rownames(cts[[j]])) {
        vals[j] <- format_coef_star(cts[[j]][cn, "Estimate"],
                                     cts[[j]][cn, "Pr(>|t|)"])
        ses[j]  <- format_se_paren(cts[[j]][cn, "Std. Error"])
      }
    }

    coef_lines <- c(coef_lines, sprintf(
      "        \\multirow{2}{*}{%s} &  \\multicolumn{1}{c}{%s}   & \\multicolumn{1}{c}{%s}   &  \\multicolumn{1}{c}{%s} & \\multicolumn{1}{c}{%s}    \\\\",
      lab, vals[1], vals[2], vals[3], vals[4]
    ))
    coef_lines <- c(coef_lines, sprintf(
      "            &  \\multicolumn{1}{c}{%s}    & \\multicolumn{1}{c}{%s}   &  \\multicolumn{1}{c}{%s}   & \\multicolumn{1}{c}{%s}  \\\\",
      ses[1], ses[2], ses[3], ses[4]
    ))
  }

  obs_line <- sprintf(
    "\\textit{Observation}       &\\centering\\arraybackslash %s & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s  \\\\",
    format_nobs(nobs_vec[1]), format_nobs(nobs_vec[2]),
    format_nobs(nobs_vec[3]), format_nobs(nobs_vec[4])
  )

  if (length(table_note) > 1) {
    table_note <- paste(table_note, collapse = "\n    ")
  }

  lines <- c(
    "\\begin{center}",
    "    \\small",
    "    \\begin{threeparttable}",
    "        \\small",
    "        \\begin{tabular}{@{}*{5}{p{.20\\textwidth}@{}}}",
    "        \\hline\\hline",
    "          &\\multicolumn{2}{c}{Formal} & \\multicolumn{2}{c}{Informal} \\\\ \\cmidrule(lr){2-3} \\cmidrule(lr){4-5}",
    "          &\\multicolumn{1}{c}{(1)}&\\multicolumn{1}{c}{(2)}&\\multicolumn{1}{c}{(3)}&\\multicolumn{1}{c}{(4)}\\\\",
    "          &\\multicolumn{1}{c}{Employment}&\\multicolumn{1}{c}{Real Wage}&\\multicolumn{1}{c}{Employment}&\\multicolumn{1}{c}{Real Wage}\\\\",
    "        \\hline",
    coef_lines,
    "\\hline",
    obs_line,
    "\\hline\\hline",
    "\\end{tabular}",
    "\\begin{tablenotes}[para,flushleft]",
    "    \\footnotesize",
    paste0("    \\item \\textbf{Note:} ", table_note),
    "    \\end{tablenotes}",
    "\\end{threeparttable}",
    "\\end{center}"
  )

  writeLines(lines, path)
  message("Saved: ", path)
  invisible(path)
}
```

### Usage

```r
write_did_table(
  models   = list(m1, m2, m3, m4),
  coef_map = c("dd" = "Target*Post18"),
  table_note = c("Data source sentence.", "Sample definition.", "..."),
  filename = "table-pr-effect.tex"
)
```

### Multiple Coefficient Rows

For event study / parallel trend tables with multiple year interactions:

```r
# Build coef_map dynamically from fixest i() coefficients
coef_names <- grep("year::", names(coef(model)), value = TRUE)
coef_labels <- setNames(
  gsub("year::(\\d+):target", "\\1", coef_names),
  coef_names
)

write_did_table(
  models      = list(m1, m2, m3, m4),
  coef_map    = coef_labels,
  table_note  = note_lines,
  filename    = "table-parallel-trend.tex",
  row_spacing = TRUE  # adds [0.5em] between year rows
)
```

## Stratified Table (Columns = Subgroups)

Columns are subgroup categories (e.g., education levels). Rows are different
outcomes, each with coefficient + SE + observation rows. Used when running
the same model separately for each subgroup.

```r
write_did_table_education <- function(outcome_panels, table_note, filename) {
  path <- here::here("output", "tables", filename)
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)

  cn <- "dd"
  outcome_names <- names(outcome_panels)

  outcome_lines <- character()
  for (i in seq_along(outcome_panels)) {
    panel <- outcome_panels[[i]]
    label <- outcome_names[i]

    if (i > 1) {
      outcome_lines <- c(outcome_lines, "                [0.5em]")
    }

    vals <- character(4)
    ses  <- character(4)
    obs  <- character(4)
    for (j in 1:4) {
      ct <- summary(panel[[j]])$coeftable
      vals[j] <- format_coef_star(ct[cn, "Estimate"], ct[cn, "Pr(>|t|)"])
      ses[j]  <- format_se_paren(ct[cn, "Std. Error"])
      obs[j]  <- format_nobs(nobs(panel[[j]]))
    }

    outcome_lines <- c(outcome_lines,
      sprintf("                \\multirow{2}{*}{%s}  &  \\multicolumn{1}{c}{%s}         &      \\multicolumn{1}{c}{%s}          &       \\multicolumn{1}{c}{%s}  &       \\multicolumn{1}{c}{%s}         \\\\",
              label, vals[1], vals[2], vals[3], vals[4]),
      sprintf("                                                    &  \\multicolumn{1}{c}{%s}        &      \\multicolumn{1}{c}{%s}         &       \\multicolumn{1}{c}{%s}         &       \\multicolumn{1}{c}{%s}         \\\\",
              ses[1], ses[2], ses[3], ses[4]),
      "",
      sprintf("                \\textit{Observation}          & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s \\\\",
              obs[1], obs[2], obs[3], obs[4])
    )
  }

  if (length(table_note) > 1) {
    table_note <- paste(table_note, collapse = "\n                    ")
  }

  lines <- c(
    "\\begin{center}",
    "        \\small",
    "        \\begin{threeparttable}",
    "            \\begin{tabular}{@{}*{5}{p{.20\\textwidth}@{}}}",
    "                \\hline\\hline",
    "                            &\\multicolumn{1}{c}{(1)}&\\multicolumn{1}{c}{(2)}&\\multicolumn{1}{c}{(3)}&\\multicolumn{1}{c}{(4)}\\\\",
    "                            &\\multicolumn{1}{c}{\\multirow{2}{*}{No School}}   & \\multicolumn{1}{c}{Primary and} & \\multicolumn{1}{c}{\\multirow{2}{*}{High School}} & \\multicolumn{1}{c}{\\multirow{2}{*}{University}} \\\\",
    "                            &                                                 & \\multicolumn{1}{c}{Secondary school} & & \\\\",
    "                \\hline",
    outcome_lines,
    "                \\hline \\hline",
    "                \\end{tabular}",
    "                \\begin{tablenotes}[para,flushleft]",
    "                    \\footnotesize",
    paste0("                    \\item \\textbf{Note:} ", table_note),
    "                \\end{tablenotes}",
    "        \\end{threeparttable}",
    "    \\end{center}"
  )

  writeLines(lines, path)
  message("Saved: ", path)
  invisible(path)
}
```

### Usage

```r
write_did_table_education(
  outcome_panels = list(
    "Formal Employment"   = list(m_ed0, m_ed1, m_ed2, m_ed3),
    "Formal Real Wage"    = list(m_ed0, m_ed1, m_ed2, m_ed3),
    "Informal Employment" = list(m_ed0, m_ed1, m_ed2, m_ed3),
    "Informal Real Wage"  = list(m_ed0, m_ed1, m_ed2, m_ed3)
  ),
  table_note = note_lines,
  filename   = "table-pr-effect-education.tex"
)
```

### Adapting Column Headers

The column headers (No School, Primary/Secondary, High School, University) are
hardcoded in this template. To generalize, pass a `col_labels` parameter and
build the header rows dynamically. The key pattern is the two-row header with
`\multirow{2}{*}{}` for single-word labels and a line break for multi-word
labels like "Primary and / Secondary school".

## Paneled Table (Multiple Treatment Groups)

Standard Formal/Informal headers but with multiple panels (e.g., different age
groups), each panel having its own coefficient + SE + observation rows.

```r
write_did_table_age_panels <- function(panels, table_note, filename) {
  path <- here::here("output", "tables", filename)
  dir.create(dirname(path), recursive = TRUE, showWarnings = FALSE)

  cn <- "dd"
  panel_names <- names(panels)

  panel_lines <- character()
  for (i in seq_along(panels)) {
    panel <- panels[[i]]
    label <- panel_names[i]

    if (i > 1) {
      panel_lines <- c(panel_lines, "                        [0.5em]")
    }

    vals <- character(4)
    ses  <- character(4)
    obs  <- character(4)
    for (j in 1:4) {
      ct <- summary(panel[[j]])$coeftable
      vals[j] <- format_coef_star(ct[cn, "Estimate"], ct[cn, "Pr(>|t|)"])
      ses[j]  <- format_se_paren(ct[cn, "Std. Error"])
      obs[j]  <- format_nobs(nobs(panel[[j]]))
    }

    panel_lines <- c(panel_lines,
      sprintf("                        \\multirow{2}{*}{%s}", label),
      sprintf("                                               &  \\multicolumn{1}{c}{%s}  & \\multicolumn{1}{c}{%s}  &  \\multicolumn{1}{c}{%s} & \\multicolumn{1}{c}{%s}    \\\\",
              vals[1], vals[2], vals[3], vals[4]),
      sprintf("                                               &  \\multicolumn{1}{c}{%s}   & \\multicolumn{1}{c}{%s}  &  \\multicolumn{1}{c}{%s}   & \\multicolumn{1}{c}{%s}  \\\\",
              ses[1], ses[2], ses[3], ses[4]),
      "                        [0.5em]",
      sprintf("                        \\textit{Observation}       & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s & \\centering\\arraybackslash %s   \\\\",
              obs[1], obs[2], obs[3], obs[4])
    )
  }

  if (length(table_note) > 1) {
    table_note <- paste(table_note, collapse = "\n                ")
  }

  lines <- c(
    "\\begin{center}",
    "    \\small",
    "            \\begin{threeparttable}",
    "               \\small",
    "                \\begin{tabular}{@{}*{5}{p{.20\\textwidth}@{}}}",
    "                        \\hline\\hline",
    "                        &\\multicolumn{2}{c}{Formal} & \\multicolumn{2}{c}{Informal} \\\\ \\cmidrule(lr){2-3} \\cmidrule(lr){4-5}",
    "                        &\\multicolumn{1}{c}{(1)}&\\multicolumn{1}{c}{(2)}&\\multicolumn{1}{c}{(3)}&\\multicolumn{1}{c}{(4)}\\\\",
    "                        &\\multicolumn{1}{c}{Employment}&\\multicolumn{1}{c}{Real Wage}&\\multicolumn{1}{c}{Employment}&\\multicolumn{1}{c}{Real Wage}\\\\",
    "                        \\hline",
    panel_lines,
    "                        \\hline\\hline",
    "                \\end{tabular}",
    "                \\begin{tablenotes}[para,flushleft]",
    "                \\footnotesize",
    paste0("                \\item \\textbf{Note:} ", table_note),
    "                \\end{tablenotes}",
    "            \\end{threeparttable}",
    "\\end{center}"
  )

  writeLines(lines, path)
  message("Saved: ", path)
  invisible(path)
}
```

### Usage

```r
write_did_table_age_panels(
  panels = list(
    "Male aged between 18-20" = list(s1, s2, s3, s4),
    "Male aged between 21-24" = list(m1, m2, m3, m4)
  ),
  table_note = note_lines,
  filename   = "table-pr-effect-age.tex"
)
```

## Adapting to Other Column Structures

The templates above assume a 4-column Formal/Informal layout. To adapt:

1. **Change `colspec`**: Replace `{@{}*{5}{p{.20\textwidth}@{}}}` with the
   appropriate number of columns
2. **Change group headers**: Replace `Formal`/`Informal` `\cmidrule` groups
   with your column groupings
3. **Change column labels**: Replace `Employment`/`Real Wage` with your outcome names
4. **Adjust the model list length**: The `for (j in 1:4)` loops should match
   your number of columns

The core pattern (extract → format → assemble → write) stays the same regardless
of the number of columns or their labels.
