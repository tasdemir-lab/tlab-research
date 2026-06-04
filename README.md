# tlab-research

A Claude Code plugin providing agentic research workflows for academic economics projects.

## What This Plugin Provides

| Component | Count | Description |
|-----------|-------|-------------|
| Skills | 17 | Research workflow commands (`/tlab:commit`, `/tlab:lit-all`, etc.) |
| Agents | 2 | Specialist agents (proofreader, verifier) |
| Rules | 5 | Project rules synced via SessionStart hook |
| Hooks | 2 | File protection + rule sync |

## Installation

```bash
# Add the marketplace
claude plugin marketplace add tasdemir-lab/tlab-research

# Install the plugin (project scope)
claude plugin install tlab@tlab-research --scope project
```

## Available Skills

### Project Workflow

| Command | Description |
|---------|-------------|
| `/tlab:commit [msg]` | Stage, commit, create PR, merge to main |
| `/tlab:compile-latex [file]` | 3-pass LaTeX compilation (pdflatex/xelatex + bibtex) |
| `/tlab:data-analysis [dataset]` | End-to-end R analysis workflow |
| `/tlab:context-status` | Show session health + context usage |
| `/tlab:deep-audit` | Repository-wide consistency audit |

### Literature & References

| Command | Description |
|---------|-------------|
| `/tlab:lit-all [topic]` | Parallel multi-database literature sweep (uses paper_find_server + Zotero MCP) |
| `/tlab:lit-check [concern]` | Three-dimension literature check (methods, context, reference papers) |
| `/tlab:lit-review-assistant [topic]` | Search, summarize, and synthesize literature |
| `/tlab:zotero-import [args]` | Import references into Zotero with duplicate detection (requires Zotero MCP) |
| `/tlab:papercheck [paper]` | Extract page-anchored evidence from PDFs on specific threats (requires Antigravity CLI) |

### Writing & Tables

| Command | Description |
|---------|-------------|
| `/tlab:proofread [file]` | Grammar/typo/consistency review (report only) |
| `/tlab:validate-bib` | Cross-reference citations vs bibliography |
| `/tlab:latex-tables` | Generate publication-ready regression tables in LaTeX |
| `/tlab:r-to-latex-tables` | Convert R regression output to LaTeX tables (fixest/lm/glm) |
| `/tlab:quarto-academic-gotchas` | Troubleshoot Quarto theorem numbering, cross-refs, and includes |

### Review & Ideation

| Command | Description |
|---------|-------------|
| `/tlab:review-paper [file]` | Referee-style manuscript review with rubric scoring |
| `/tlab:review-r [file]` | R code review for quality, reproducibility, and domain correctness |
| `/tlab:econ-ideate [data\|corpus\|resume\|status]` | 8-phase research idea pipeline (requires NotebookLM CLI + Zotero MCP) |

## Example Prompts

### econ-ideate

```
# Data-first: start from a dataset, find research questions
/tlab:econ-ideate data data/raw/turkstat_lfs_2005_2022.csv --topic-hint "labor market effects of policy"

# Corpus-first: start from a topic, find gaps with data
/tlab:econ-ideate corpus --topic "wage subsidies and employment duration" --from-zotero almp-article

# Resume a previous run that paused at the gap-data matrix
/tlab:econ-ideate resume 20260604-wage-subsidies
```

### lit-all

```
/tlab:lit-all topic:"staggered difference-in-differences" years:2018-2025

# Or just describe what you need:
"Search all databases for papers on the employment effects of active labor market policies in developing countries"
```

### papercheck

```
# Check how a specific paper handles a specific threat
"Check whether Autor-Dorn-Hanson (2013) address migration as a confounder — controls vs robustness vs placebo? Use page-anchored quotes."

# Check multiple papers for the same concern
"Do Sjogren & Vikstrom (2015) and Card et al. (2018) address anticipation effects? How exactly?"
```

### lit-check

```
# Ask a methodological question — the skill classifies the dimension automatically
"How do papers handle pre-trends in staggered DiD?"
"What's the standard for weak instrument testing in labor economics?"
"Should I cluster standard errors at the firm or industry level?"
```

### zotero-import

```
/tlab:zotero-import --doi 10.1257/aer.20161500
/tlab:zotero-import --file refs.bib
# Or paste BibTeX directly after invoking:
/tlab:zotero-import
```

### review-paper

```
# Review your own manuscript
/tlab:review-paper paper/index.qmd

# Review an external paper PDF
/tlab:review-paper lit/papers/referee_report_target.pdf
```

### data-analysis

```
# Full pipeline from exploration to publication-ready output
/tlab:data-analysis data/final/matched_panel.rds

# Or describe the analysis goal:
/tlab:data-analysis "Run DiD on the matched panel, with event study plots and robustness to alternative matching"
```

## Optional MCP Servers

Some skills use MCP servers for database access. Skills degrade gracefully when servers are absent.

| MCP Server | Used by | Install |
|------------|---------|---------|
| Zotero | `lit-all`, `zotero-import`, `econ-ideate` | `claude mcp add zotero -- npx -y zotero-mcp@latest` |
| paper_find_server | `lit-all` | `claude mcp add paper_find_server -- npx -y paper-find-mcp@latest` |
| Antigravity CLI | `papercheck`, `lit-check` | Download from https://antigravity.google, run `agy install` (not an MCP — standalone CLI) |

## How Rules Work

Claude Code plugins can't load rules directly (as of 2026-03). This plugin uses a **SessionStart hook** to sync rules from the plugin to your project's `.claude/rules/_plugin_*.md` directory.

The synced rules are:
- `knowledge-base-template.md` — Research project knowledge base template
- `meta-governance.md` — Three-layer architecture guide
- `orchestrator-research.md` — Simplified orchestrator for R scripts
- `single-source-of-truth.md` — Output freshness enforcement
- `verification-protocol.md` — Task completion verification

These files are gitignored (`.claude/rules/_plugin_*`) since they are derived content from the plugin.

## Updating

```bash
claude plugin update tlab@tlab-research
```

Updated rules will be synced on the next session start.

## Template Companion

This plugin is designed to work with [research-template-bare](https://github.com/tasdemir-lab/research-template-bare), a scaffolding template for economics research projects. The template provides folder structure; this plugin provides the agentic workflow.

## License

MIT
