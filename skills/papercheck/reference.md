# Papercheck reference

## What counts as "addressing the issue"?
- **Controls**: adds covariate(s) or fixed effects that directly absorb the confounder.
- **Robustness**: shows estimates stable when adding the control, reweighting, restricting sample, alternative exposure definitions, etc.
- **Placebo / falsification**: tests implications that should be null if identification holds.
- **Sensitivity / bounds**: Oster/Altonji-Elder-Taber style logic, Rosenbaum, partial ID, etc.
- **Discussion-only**: mentions but does not test.

## Evidence standards
- Always extract **verbatim** excerpts + **page numbers**.
- If page numbers cannot be verified: verdict must be **Unclear**.

## Page number convention
Page numbers should be **PDF page numbers** (as shown in your PDF viewer's page counter, starting from 1), **not** the printed page numbers in the document footer. This ensures reproducibility:
- PDF page 1 = first page of the PDF file (often a cover or title page)
- If a paper's printed pagination starts at "1247", that might be PDF page 1 or later

When reporting, use format: "p.12 (PDF)" to indicate PDF page numbers when there might be ambiguity.

## Practical convention
Store PDFs under one of:
- ./lit/papers/
- ./papers/
- ./refs/

Evidence packs are written to:
- ./.papercheck/packs/
