---
paths:
  - "code/**"
  - "paper/**"
  - "output/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

## For R Scripts:
1. Run `Rscript code/FILENAME.R`
2. Verify output files (PDF, RDS, tables) were created with non-zero size
3. Spot-check estimates for reasonable magnitude
4. Verify all expected outputs exist in `output/`

## For Quarto Documents:
1. Run `quarto render code/FILENAME.qmd`
2. Verify HTML (and GFM if configured) output was created
3. Check for render warnings or errors

## For LaTeX/Paper Compilation:
1. Compile with the project's chosen engine (pdflatex or xelatex):
   ```bash
   cd paper && pdflatex -interaction=nonstopmode manuscript.tex
   bibtex manuscript
   pdflatex -interaction=nonstopmode manuscript.tex
   pdflatex -interaction=nonstopmode manuscript.tex
   ```
2. Check for overfull hbox warnings
3. Check for undefined citations
4. Verify PDF was generated: `ls -la paper/manuscript.pdf`
5. Open the PDF for visual verification

## For Data Pipeline:
1. Verify input data files exist before running
2. Run scripts in pipeline order
3. Check that each step's outputs feed correctly into the next step
4. Verify final outputs in `output/figures/` and `output/tables/`

## Common Pitfalls:
- **Assuming success**: Always verify output files exist AND contain correct content
- **Stale outputs**: Re-run scripts if source data or code changed
- **Path issues**: All paths should be relative to repository root (use `here::here()`)

## Verification Checklist:
```
[ ] Output file created successfully
[ ] No compilation/render errors
[ ] Figures/tables display correctly
[ ] Paths resolve correctly
[ ] Reported results to user
```
