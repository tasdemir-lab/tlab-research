---
name: papercheck
description: Verify what specific papers do about a confounder/threat/method (controls vs robustness vs placebo vs sensitivity). Use when deciding whether to add a control, claim identification, or respond to "has the literature handled this?" Requires page-anchored quotes from PDFs and outputs a cached evidence pack.
author: Murat Taşdemir
version: 1.1.0
tags:
  - research
  - literature-review
  - evidence-extraction
  - PDF-analysis
  - causal-inference
---

# Papercheck Skill

## Prerequisites

**Required:** Antigravity CLI (`agy`) must be installed and configured.
- Install: Download from https://antigravity.google, then run `agy install`
- Configure: Run `agy` once to authenticate with your Google account

## Goal
When a research decision depends on what a key paper did about a *specific* concern (confounder, selection, anticipation, migration, composition, trends, multiple testing, weak ID, etc.), create an **auditable evidence pack** from the PDF(s) instead of relying on memory or generic summaries.

Claude Code will ask to activate this Skill when relevant; user confirms before the full Skill loads. (Normal Skills activation flow.)

## Workflow (always follow)
1) **Restate the question** in a falsifiable form:
   - "Did Paper X address Threat Z?"
   - "How exactly: controls vs robustness vs placebo vs sensitivity/bounds?"
   - "What does that imply for *our* design choice?"

2) **Locate PDFs** (preferred order):
   - If user provided paths, use those.
   - Else search in order: `./lit/papers/`, `./papers/`, `./refs/`, then project root.
   - **Matching strategy**: Search for filenames containing author surname + year (e.g., `ADH2013`, `Autor2013`, `autor_dorn_hanson_2013`). Use glob patterns like `*autor*2013*.pdf` (case-insensitive).
   - If multiple matches, prefer the one with the most complete author list in filename.

3) **Run the evidence extraction script** (do not read entire PDFs into Claude):
   ```bash
   # Locate the script dynamically (version changes on plugin update)
   SCRIPT="$(find ~/.claude/plugins/cache/tlab-research -path '*/papercheck/scripts/papercheck.py' 2>/dev/null | sort -V | tail -1)"
   python "$SCRIPT" \
     --pdf <path> \
     --issue "<issue>" \
     --outdir .papercheck/packs
   ```
   - If multiple papers: use multiple `--pdf` flags in one command.
   - The script requires Antigravity CLI (`agy`). If it fails with "not found", ask user to install it.

4) **Report results in a decision-oriented way**
   - Start with a table-like bullets: Paper → Verdict → What they do (controls/robustness/etc.)
   - Then list 3–10 **verbatim** quotes with **page numbers** per paper.
   - End with: "Recommended path for our paper" + "When we should still add the control anyway".

## Error handling
- **Antigravity CLI not found**: Ask user to install it (see Prerequisites above).
- **PDF not found**: List searched directories and ask user to provide the correct path.
- **Timeout**: The script has a 5-minute default timeout. For very large PDFs, suggest `--timeout 600`.
- **JSON parse error**: Check `.papercheck/packs/<key>.raw.txt` for the raw `agy` output.

## Evidence pack standard (non-negotiable)
- No page-anchored quote ⇒ mark as **Unclear** (do not pretend).
- Prefer main text; include appendix if that’s where robustness lives.
- Highlight differences across papers (some control, some only robustness).

## Outputs and caching
- Script writes JSON + a readable Markdown pack under `.papercheck/packs/`.
- Reuse cached packs rather than re-reading PDFs.
- Cache is keyed by PDF content hash + issue text hash, so:
  - Same PDF + same issue = cache hit (fast)
  - Same PDF + different issue wording = new extraction (even if semantically similar)
- **Cache management** (use the same `$SCRIPT` variable from step 3):
  - List cached packs: `python "$SCRIPT" --pdf dummy --issue dummy --list-cache`
  - Clear all cached packs: `python "$SCRIPT" --pdf dummy --issue dummy --clear-cache`

## Additional resources
- Prompt/spec details: [reference.md](reference.md)
- Usage patterns: [examples.md](examples.md)
