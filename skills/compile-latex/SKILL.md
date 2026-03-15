---
name: compile-latex
description: Compile the paper manuscript with LaTeX (3 passes + bibtex). Supports both pdflatex and xelatex.
argument-hint: "[filename without .tex extension, defaults to 'manuscript']"
allowed-tools: ["Read", "Bash", "Glob"]
---

# Compile LaTeX Paper

Compile the research paper using LaTeX with full citation resolution.

## Steps

1. **Determine the filename:**
   - If `$ARGUMENTS` is provided, use it as the filename (without .tex extension)
   - Otherwise, default to `manuscript`

2. **Compile with 3-pass sequence** (pdflatex by default):

```bash
cd paper
pdflatex -interaction=nonstopmode $FILENAME.tex
BIBINPUTS=..:$BIBINPUTS bibtex $FILENAME
pdflatex -interaction=nonstopmode $FILENAME.tex
pdflatex -interaction=nonstopmode $FILENAME.tex
```

**Alternative (xelatex):**
```bash
cd paper
xelatex -interaction=nonstopmode $FILENAME.tex
BIBINPUTS=..:$BIBINPUTS bibtex $FILENAME
xelatex -interaction=nonstopmode $FILENAME.tex
xelatex -interaction=nonstopmode $FILENAME.tex
```

**Alternative (latexmk):**
```bash
cd paper
BIBINPUTS=..:$BIBINPUTS latexmk -pdf -interaction=nonstopmode $FILENAME.tex
```

3. **Check for warnings:**
   - Grep output for `Overfull \\hbox` warnings
   - Grep for `undefined citations` or `Label(s) may have changed`
   - Report any issues found

4. **Open the PDF** for visual verification:
   ```bash
   open paper/$FILENAME.pdf          # macOS
   # xdg-open paper/$FILENAME.pdf    # Linux
   ```

5. **Report results:**
   - Compilation success/failure
   - Number of overfull hbox warnings
   - Any undefined citations
   - PDF page count

## Why 3 passes?
1. First pass: Creates `.aux` file with citation keys
2. bibtex: Reads `.aux`, generates `.bbl` with formatted references
3. Second pass: Incorporates bibliography
4. Third pass: Resolves all cross-references with final page numbers

## Important
- Default engine is **pdflatex**; use xelatex if the document requires Unicode fonts
- Bibliography file lives at the repo root (`master.bib`); `BIBINPUTS=..` makes it visible from `paper/`
- All compilation happens from within the `paper/` directory
