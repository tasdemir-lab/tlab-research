# tlab-research

A Claude Code plugin providing agentic research workflows for academic economics projects.

## What This Plugin Provides

| Component | Count | Description |
|-----------|-------|-------------|
| Skills | 7 | Research workflow commands (`/tlab:commit`, `/tlab:proofread`, etc.) |
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

| Command | Description |
|---------|-------------|
| `/tlab:commit [msg]` | Stage, commit, create PR, merge to main |
| `/tlab:compile-latex [file]` | 3-pass LaTeX compilation (pdflatex/xelatex + bibtex) |
| `/tlab:proofread [file]` | Grammar/typo/consistency review (report only) |
| `/tlab:validate-bib` | Cross-reference citations vs bibliography |
| `/tlab:data-analysis [dataset]` | End-to-end R analysis workflow |
| `/tlab:context-status` | Show session health + context usage |
| `/tlab:deep-audit` | Repository-wide consistency audit |

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
