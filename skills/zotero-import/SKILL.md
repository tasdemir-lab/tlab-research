---
name: zotero-import
description: >
  Import new references into Zotero with intelligent duplicate detection.
  Accepts BibTeX entries, DOIs, or paper titles. Uses agent judgment to detect
  duplicates (including working paper vs published version of the same work).
  Imports via Zotero's local connector API. Can be called explicitly or
  proactively by other skills (lit-all, papercheck, lit-review-assistant)
  when they discover new references.
argument-hint: "[--doi DOI | --file refs.bib | --from-skill]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Agent", "AskUserQuestion", "ToolSearch", "mcp__zotero__zotero_search_items", "mcp__zotero__zotero_get_item_metadata", "mcp__zotero__zotero_get_collections", "mcp__zotero__zotero_get_collection_items", "mcp__paper_find_server__get_crossref_paper_by_doi", "mcp__paper_find_server__search_crossref", "mcp__paper_find_server__search_semantic"]
---

# Zotero Import

Import new references into Zotero with agent-powered duplicate detection.
Handles the common economics problem: a working paper version already exists
in the library, and the incoming reference is the published version (or vice versa).
The agent reads both records and judges whether they represent the same work.

## Invocation

```
/tlab:zotero-import                              # Interactive — paste BibTeX or describe papers
/tlab:zotero-import --doi 10.1257/aer.2024.1234  # Import from DOI
/tlab:zotero-import --file refs.bib              # Import from .bib file
/tlab:zotero-import --from-skill                 # Called by another skill with refs in context
```

## Prerequisites — Zotero MCP Server

**Before doing anything else**, check whether Zotero MCP tools are available.

Look in the deferred tools list (already in your system prompt) for tools matching
`mcp__zotero__*`. This is a zero-cost check — no tool calls needed, just read your
system prompt.

### If `mcp__zotero__*` tools ARE present

Zotero MCP is installed. Proceed to Step 0.

### If `mcp__zotero__*` tools are NOT present

Zotero MCP server is not configured. Tell the user:

```
Zotero MCP server is not installed. This skill requires it for duplicate
detection and library search.

To install, run:

  claude mcp add zotero -- npx -y zotero-mcp@latest

This starts a local MCP server that connects to Zotero's API.
Requirements:
  - Node.js 18+ installed
  - Zotero running with the connector enabled (localhost:23119)
  - For write operations: set ZOTERO_API_KEY and ZOTERO_LIBRARY_ID
    environment variables (see https://github.com/nicekid1/zotero-mcp)

After installing, restart Claude Code and retry /tlab:zotero-import.
```

Then **STOP**. Do not attempt to import without the MCP server.

## Locating the Helper Script

The `bib_to_zotero.py` script lives alongside this skill file. To find it at runtime:

```bash
# Find the skill's scripts directory dynamically
SKILL_SCRIPTS="$(find ~/.claude/plugins/cache/tlab-research -path '*/zotero-import/scripts/bib_to_zotero.py' 2>/dev/null | sort -V | tail -1)"
```

If the script is not found, fall back to constructing BibTeX-to-Zotero JSON inline
(the conversion logic is documented in Step 4 below).

## Workflow

### Step 0: Preflight Check

Verify Zotero is running:

```bash
curl -s http://localhost:23119/connector/ping 2>/dev/null | grep -q "Zotero"
```

If not running, tell user: "Zotero must be running for import. Please start it." Then STOP.

### Step 1: Determine Collection Target

Detect the target collection from the current repo name:

1. Get the repo directory name: `basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)`
2. Search Zotero collections for a matching name using `zotero_get_collections`
3. If found, note the collection key and name
4. If not found, warn: "No Zotero collection named '{repo}' found. Items will go to whichever collection is currently selected in Zotero."

**Important**: The connector `saveItems` endpoint places items into whatever collection is currently selected in Zotero's UI. Remind the user: "Please make sure the '{collection}' collection is selected in Zotero."

### Step 2: Parse Input

Determine what the user provided and normalize to a list of candidate references:

| Input | Action |
|-------|--------|
| BibTeX string | Parse with `bibtexparser` |
| DOI | Fetch metadata via `get_crossref_paper_by_doi` |
| Paper title/author | Search via `search_crossref` or `search_semantic` to get full record |
| `--file path.bib` | Read and parse the file |
| `--from-skill` | References are already in conversation context from a prior skill |
| Nothing | Ask user to paste BibTeX, provide a DOI, or describe the paper |

For DOI or title inputs, resolve to a complete bibliographic record before proceeding.
When a search returns multiple candidates, pick the best match (prefer published version over working paper).

### Step 3: Deduplicate — One Reference at a Time

For **each** candidate reference, perform duplicate detection:

#### 3a. Search Zotero

First, load the Zotero MCP tool schemas if not already loaded:
```
ToolSearch("select:mcp__zotero__zotero_search_items")
```

Use `zotero_search_items` with the first author's last name + a distinctive title word.
Request enough results to catch variants (limit=10).

If the candidate has a DOI, also search by DOI.

#### 3b. Agent Judges Duplicates

Read the Zotero search results and the incoming reference. Decide:

**DUPLICATE (same work, any version):**
The incoming reference and an existing Zotero item represent the same intellectual work,
even if one is a working paper and the other is published, or titles differ slightly,
or years differ (common: WP 2018 -> published 2021).

Signals to consider:
- Same or very similar title (after ignoring punctuation, articles, subtitle variations)
- Same author set (order may differ, initials vs full names)
- One is clearly a later version of the other (NBER WP -> journal article)
- Same DOI
- Year within reasonable range (+/- 5 years for WP->publication pipeline)

**NEW:**
No existing Zotero item represents this work in any version.

#### 3c. Classify Duplicates Further

If DUPLICATE, determine:

- **Same version**: Both are journal articles, or both are working papers, with matching type fields.
  Check if existing Zotero record has empty fields that the incoming entry can fill (e.g., missing abstract, DOI, volume/pages). If yes, flag for **field merge** (requires Zotero Web API -- see Step 5).
- **Different version**: One is a working paper, the other is published (or different editions).
  Simply **skip** -- the existing version in Zotero stands.

### Step 4: Import New References

For each reference classified as NEW:

1. Write the BibTeX entries to a temp file (avoids shell quoting issues with abstracts):

```bash
# Locate the helper script
SCRIPT="$(find ~/.claude/plugins/cache/tlab-research -path '*/zotero-import/scripts/bib_to_zotero.py' 2>/dev/null | sort -V | tail -1)"

# Write entries to temp file, then import
python3 "$SCRIPT" --file /tmp/zotero_import.bib --collection "<repo-name>"
```

**Never pipe bibtex via `echo`** -- abstracts contain single quotes, special characters, and LaTeX
commands that break shell quoting. Always use `--file` or stdin redirection (`< file.bib`).

2. Parse the JSON output carefully. Check **each** result's `status` field:
   - `"imported"` -- success
   - `"error"` -- report the error message to the user
   - Check stderr for `WARNING: N entries failed to parse` -- these were silently dropped by bibtexparser

3. Verify import succeeded by searching Zotero for the newly added item.
   Also confirm it landed in the expected collection (the one shown in Step 1).

### Step 5: Handle Field Merges (Same-Version Duplicates)

When a same-version duplicate has missing fields that the incoming entry can fill:

**Without Zotero Web API (default):**
Report the merge opportunity to the user:
```
MERGE CANDIDATE: Existing item [KEY] "{title}" is missing: abstract, DOI
The incoming entry has these fields. To merge, update manually in Zotero or configure the Web API.
```

**With Zotero Web API (if ZOTERO_API_KEY is set):**
Use pyzotero to update the existing item's empty fields. (Future enhancement.)

### Step 6: Report

Print a summary:

```
## Zotero Import Summary

Collection: english-medium (3QSLTJEP)

| # | Reference | Action | Details |
|---|-----------|--------|---------|
| 1 | Author (2024) "Title..." | IMPORTED | New item added |
| 2 | Author (2021) "Title..." | SKIPPED | Duplicate of existing WP (2018) |
| 3 | Author (2023) "Title..." | SKIPPED | Already in library |
| 4 | Author (2020) "Title..." | MERGE | Existing item missing: abstract, DOI |

Added: 1 | Skipped: 2 | Merge candidates: 1
```

## Integration with Other Skills

This skill can be called **proactively** by other skills when they produce new references:

- **`lit-all`**: After a literature sweep, pass discovered references to `/tlab:zotero-import --from-skill`
- **`papercheck`**: After deep-reading a paper, import it if not already in Zotero
- **`lit-review-assistant`**: After synthesizing literature, import the bibliography
- **`lit-check`**: After checking a specific concern across papers, import new finds

The calling skill should either:
- Write BibTeX entries to a temp file (e.g., `/tmp/zotero_import.bib`) and invoke `/tlab:zotero-import --file /tmp/zotero_import.bib`
- Or place BibTeX entries or DOIs in the conversation context and invoke `/tlab:zotero-import --from-skill`

When `--from-skill` is used, the agent scans the recent conversation for:
1. BibTeX `@type{key, ...}` blocks
2. DOI strings (e.g., `10.xxxx/...`)
3. Structured reference lists with author/title/year

## Error Handling

| Error | Recovery |
|-------|----------|
| Zotero MCP not installed | Print install instructions. STOP. |
| Zotero not running | Tell user to start Zotero. STOP. |
| Connector returns empty/error | Check Zotero is responsive, retry once |
| BibTeX parse failure | Show the problematic entry, skip it, continue with others |
| No search results (false negative?) | Import anyway -- better a duplicate than a missing reference |
| Zotero search timeout | Retry with simpler query (author last name only) |
| Helper script not found | Fall back to manual JSON construction via the connector API |

## Notes

- Citation keys are managed by Better BibTeX in Zotero, not by this skill.
  The skill stores the original BibTeX key in the `extra` field for traceability.
- The connector `saveItems` places items in the currently-selected collection.
  Always remind the user to verify the correct collection is selected.
- This skill never modifies or deletes existing Zotero items (read-only for existing data).
- When in doubt about a duplicate, the agent should err on the side of importing.
  A duplicate in Zotero is less harmful than a missing reference.
