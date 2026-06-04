---
paths:
  - "code/**"
  - "output/**"
  - "paper/**"
---

# Single Source of Truth: Enforcement Protocol

**Analysis code is the authoritative source for ALL results.** Everything else is derived.

## The SSOT Chain

```
code/*.R, code/*.qmd (SOURCE OF TRUTH)
  +-- output/figures/*.pdf (derived)
  +-- output/tables/*.tex (derived)
  +-- output/*.rds (derived)
  +-- paper/manuscript.tex (CONSUMER -- references derived outputs)
  +-- master.bib (shared, repo root)

NEVER edit derived artifacts independently.
ALWAYS regenerate outputs by re-running the source code.
```

---

## Output Freshness Protocol (MANDATORY)

**Before including ANY output in the paper, verify it matches the current analysis code.**

### Freshness Check Procedure

1. Check modification dates: source code should be older than (or same as) output files
2. If code is newer than outputs, re-run the pipeline
3. Verify output files are non-zero size
4. Spot-check key numbers against expectations

### When to Re-Run

Re-run the full pipeline when:
- Any analysis script has been modified since last run
- Data files have been updated
- Package versions have changed (check `renv.lock`)
- Before any commit that includes paper changes

---

## Content Fidelity Checklist

```
[ ] All figures in paper/ reference files that exist in output/figures/
[ ] All tables in paper/ reference files that exist in output/tables/
[ ] Numbers cited in paper text match current output
[ ] No manually entered numbers -- all from computed sources
[ ] Bibliography entries match citations in text
```
