---
name: lit-review-assistant
description: Search, summarize, and synthesize economics literature
workflow_stage: literature
compatibility:
  - claude-code
  - cursor
  - codex
  - antigravity-cli
author: Awesome Econ AI Community
version: 1.0.0
tags:
  - literature-review
  - papers
  - citations
  - synthesis
---

# Literature Review Assistant

## Purpose

This skill helps economists conduct literature reviews by structuring searches, summarizing papers, and synthesizing findings. It provides templates for organizing literature and identifying research gaps.

## When to Use

- Starting a literature review for a new project
- Finding related work for a paper's introduction
- Synthesizing existing evidence on a topic
- Identifying gaps in the literature

## Instructions

Before writing synthesis prose, read [../_shared-writing/anti-ai-writing-standard.md](../_shared-writing/anti-ai-writing-standard.md).

### Step 1: Define the Research Domain

Ask the user:
1. What is your specific research question?
2. What's the scope? (Narrow field survey vs. cross-disciplinary review)
3. What databases do you have access to? (JSTOR, EconLit, Google Scholar, NBER)
4. What time period is relevant?
5. Are there seminal papers to start from?

### Step 2: Structure the Search

Help define search terms:
1. **Primary terms**: Core concepts (e.g., "minimum wage", "employment")
2. **Methodological filters**: (RCT, IV, difference-in-differences)
3. **Outcome terms**: What effects are measured
4. **Geographic/temporal scope**: If relevant

### Step 3: Organize and Synthesize

Create a structured summary for each paper:
- Citation
- Research question
- Data and methods
- Key findings
- Limitations
- How it relates to user's project

When turning those notes into prose:
- synthesize across papers by disagreement, design, mechanism, or context
- avoid one-paper-at-a-time parade summaries unless the user explicitly wants an annotated bibliography
- avoid generic `the literature shows` language unless you immediately say which papers show what and why

### Step 4: Identify Patterns and Gaps

- What do papers agree on?
- Where are disagreements?
- What questions remain unanswered?
- What methods haven't been applied?

## Example Output: Literature Summary Template

```markdown
# Literature Review: [TOPIC]

## Search Strategy

**Databases:** EconLit, NBER, Google Scholar, SSRN
**Date range:** 2010-2024
**Search terms:** 
- ("minimum wage" OR "wage floor") AND (employment OR jobs)
- ("minimum wage") AND ("difference-in-differences" OR "DiD")

**Inclusion criteria:**
- Peer-reviewed or NBER working papers
- Focused on [specific outcome]
- Uses causal identification strategy

---

## Seminal Papers

### Card and Krueger (1994)
**Citation:** Card, D., & Krueger, A. B. (1994). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. *American Economic Review*, 84(4), 772-793.

**Research Question:** What is the effect of minimum wage increases on employment?

**Data & Method:** 
- DiD comparing NJ (treatment) to PA (control)
- Survey of fast-food restaurants before/after NJ minimum wage increase

**Key Findings:**
- No negative employment effect found
- Employment slightly increased in NJ relative to PA

**Contribution:** Challenged conventional view; pioneered quasi-experimental methods in labor economics

**Limitations:**
- Single state, short time horizon
- Potential survey response bias

---

### Cengiz et al. (2019)
**Citation:** Cengiz, D., Dube, A., Lindner, A., & Zipperer, B. (2019). The Effect of Minimum Wages on Low-Wage Jobs. *Quarterly Journal of Economics*, 134(3), 1405-1454.

**Research Question:** Do minimum wage increases destroy jobs or compress the wage distribution?

**Data & Method:**
- Bunching estimator using 138 minimum wage events
- Examine employment distribution around minimum wage

**Key Findings:**
- Jobs below the new minimum wage disappear
- But replaced by jobs just above the minimum
- No significant overall employment loss

**Contribution:** Novel bunching methodology; large-scale evidence

---

## Synthesis: What We Know

Rather than summarizing each paper separately, organize the literature around the key margins of disagreement. In this example, the central divide is not whether minimum wages matter in principle, but which margins adjust and under what market conditions. Early case-study evidence emphasizes limited disemployment effects after modest increases, while later multi-event studies argue that employment losses below the new minimum are often offset by gains just above it. A separate strand asks whether larger increases or low-productivity labor markets generate different responses. This structure lets the reader see where the literature converges, where it does not, and what kind of new evidence would move the debate.

## Research Gaps

1. **Mechanism:** How do firms absorb higher labor costs? (Prices, profits, productivity?)
2. **Long-run effects:** Most studies focus on 1-2 years
3. **Geographic heterogeneity:** Do effects differ in low vs. high cost-of-living areas?
4. **Spillovers:** Effects on workers earning above minimum wage

## Connection to Your Project

Your study of [SPECIFIC QUESTION] can contribute by:
- [How your work fills a gap]
- [What new data/method you bring]
```

## Paper Summary Template

```markdown
## [Author(s)] ([Year])

**Title:** [Full title]

**Published in:** [Journal/Working Paper Series]

**Research Question:** [One sentence]

**Data:**
- Source: [Dataset name]
- Period: [Years]
- Sample: [N observations, unit of analysis]

**Identification Strategy:** [Method in one sentence]

**Main Findings:**
1. [Key result 1 with magnitude]
2. [Key result 2]
3. [Robustness/heterogeneity]

**Limitations:**
- [Main concern 1]
- [Main concern 2]

**Relevance to your project:** [One sentence on how it connects]

**Key quote:** "[Most important direct quote]" (p. XX)
```

## Search Strategy Tips

### Google Scholar Operators
- `"exact phrase"` - Exact matching
- `author:surname` - Papers by specific author
- `source:journal` - Papers in specific journal
- `-exclude` - Exclude terms
- `[year]..[year]` - Date range

### Finding Seminal Papers
1. Check citations in recent survey papers
2. Look for papers with 1000+ citations
3. Check JEL codes in EconLit
4. Review "related articles" in Google Scholar

### Building Citation Networks
1. Start with 2-3 seminal papers
2. Check what recent papers cite them (forward citations)
3. Check their references (backward citations)
4. Identify clusters of related work

## Best Practices

1. **Use reference managers** (Zotero, Mendeley, BibDesk)
2. **Create annotated bibliographies** as you read
3. **Track search queries** for reproducibility
4. **Update regularly** before submission
5. **Balance breadth and depth** - cover field but focus on closest work
6. **Write comparative synthesis, not paper parades** - connect papers through design, finding, mechanism, or scope
7. **Keep contribution language concrete** - say what a paper identifies, measures, or explains rather than calling it `important` or `novel`
8. **Use UTF-8 in bib files** — write author/title fields with native characters (e.g., `Kılıçkaya`, `Özen`) when using XeLaTeX or BibLaTeX. Avoid LaTeX accent macros (`\c{c}`, `{\"o}`) which produce garbled output with modern engines.
9. **Keep citation keys ASCII-only** — transliterate non-ASCII characters in keys (e.g., `kilickaya2006` not `kılıçkaya2006`). Characters like `ç→c`, `ö→o`, `ı→i`, `ş→s`, `ğ→g`, `ü→u`.

## Common Pitfalls

- ❌ Only citing papers that support your argument
- ❌ Not engaging with contradictory findings
- ❌ Confusing correlation with causation when summarizing
- ❌ Citing papers you haven't actually read
- ❌ Missing important recent papers
- ❌ Turning the review into a serial list of mini-abstracts with no comparison across papers
- ❌ Using generic throat-clearing such as `the literature has extensively examined`
- ❌ Using LaTeX accent macros in bib files (`{\"o}`, `\c{c}`) instead of UTF-8 — causes garbled author names with XeLaTeX
- ❌ Using non-ASCII characters in citation keys — breaks cross-referencing in some BibTeX backends

## References

- [EconLit](https://www.aeaweb.org/econlit/) - Authoritative economics database
- [NBER Working Papers](https://www.nber.org/papers) - Latest research
- [IDEAS/RePEc](https://ideas.repec.org/) - Free economics papers
- [Connected Papers](https://www.connectedpapers.com/) - Visual citation networks

## Changelog

### v1.0.0
- Initial release with templates and search strategies
