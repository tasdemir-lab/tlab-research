---
name: econ-ideate
description: >
  Research idea finder for economics. Two entry points — data-first
  (given a dataset, find questions) and corpus-first (given papers or
  a topic, find gaps). Fuses literature synthesis (Piyas-style prompts)
  with data availability to produce a ranked shortlist of testable
  research ideas. Commands: data, corpus, resume, status.
author: Murat Tasdemir
version: 0.2.3
argument-hint: "<subcommand> [args]"
allowed-tools: ["Agent", "Read", "Write", "Edit", "Bash", "Glob", "Grep", "AskUserQuestion", "Skill", "ToolSearch", "mcp__zotero__zotero_get_collections", "mcp__zotero__zotero_get_collection_items", "mcp__zotero__zotero_semantic_search", "mcp__zotero__zotero_search_items", "mcp__zotero__zotero_find_and_attach_pdfs", "mcp__zotero__zotero_get_item_metadata"]
tags:
  - research
  - ideation
  - literature-synthesis
  - economics
  - multi-agent
---

# Econ Ideate

> **Status: v0.2.3.** Phases 2–4 use NotebookLM as the primary synthesis
> engine (grounded Q&A over the full corpus), with `papercheck` as a
> cross-check layer on the top 5 papers. Phase 8 adds audio overview +
> mind map as deliverables.
>
> **v0.2.1 P0 fixes (from spec review):** gap × data matrix now
> long-format with a stable header contract (5.3 ↔ 9.4); frontmatter
> `allowed-tools` aligned with body; `08_deliverables/` added to
> directory skeleton; Phase 2 synchronization barrier now explicit
> (no `ask` calls before indexing completes); `completed: bool` +
> `completed_at` in manifest schema with a binding events.jsonl append
> protocol; Phase 8.0 explicitly runs Piyas Prompt 8 before report
> assembly; binding path convention (all phase paths resolve against
> `<run-dir>`); Step 2.0 reuses any notebook already in the manifest
> before creating a new one; Mode C (`--papers` only) has a hash-based
> slug fallback.
>
> **v0.2.2 (2026-04-21) dry-run contract fixes:** first compressed
> end-to-end exercise surfaced two structural spec errors, both now
> fixed — (a) §2.0 auth preflight no longer false-halts on
> `token_fetch: null`; (b) new **Invocation Contracts** section
> documents the harness-level truth that `Skill` is recursive and
> `Agent` auto-loads by name; §1A.4, §1B.1, §2.2, §5.1, §7.1–§7.3 all
> rewritten to reference it. See `known-gaps.md` entries R1–R6 for the
> full audit.
>
> **v0.2.3 (2026-04-21) Phases 1B–5 end-to-end fixes (R7 batch):**
> second ERPT-topic run exercised every phase through 5.5 pause and
> surfaced 6 NotebookLM CLI contract issues, all now patched:
> (1) Invocation Contracts now includes a JSON-trim rule for
> `ask --json --save-as-note` (footer breaks strict parse);
> (2) §2.1 upload now reconciles via `source list` (add is non-atomic);
> (3) §2.1 adds a content-usability probe (`status: ready` ≠ usable);
> (4) §2.1 uses native `source wait` with source-type-calibrated
> timeouts; (5) §1B.1 Mode A falls through to WebSearch when Zotero
> semantic search is degenerate; (6) §5.4 runs a direct `KI-\d+` regex
> pass before Jaccard so scout-annotated killed ideas are caught.
> §5.3 also gains a per-gap cap (max(5, top-feasibility)) plus a 60-row
> total warning (F10 addressed).
>
> **Still not dry-run end-to-end past Phase 5.** Phases 6–8 (ideation,
> filter chain, report) remain unexercised; §7 validation is
> pattern-inherited from §5.1, not directly fired. Known-gaps P1/P2
> items F1–F9 carry forward (F10 now resolved).

Research idea finder for economics. Converges paper-space and data-space into a
ranked shortlist of feasible, testable ideas.

**Two entry points:**
- **Data-first** — start with a dataset, find what the literature has missed
- **Corpus-first** — start with papers or a topic, find gaps with supporting data

**Eight-phase pipeline.** Corpus-first and data-first differ only in phases 1–2,
then merge at phase 3. The convergence artifact is the **gap × data matrix**
(phase 5), which the skill pauses on for user review by default.

## Prerequisites

Before first use, verify:
- **NotebookLM CLI installed and authenticated.** Phases 2–4 depend on it.
  ```bash
  notebooklm --version          # should print a version
  notebooklm auth check --json  # should show token_fetch: true
  ```
  If either fails: `pip install notebooklm-py && notebooklm login`.
- **Skill tool access.** `lit-all`, `papercheck`, `fact-collect` must be
  invocable via the Skill tool in the current project.
- **Sub-agents available.** Files exist under `~/.claude/agents/`:
  `data-scout`, `world-watcher`, `mind-scanner`, `project-scanner`,
  `data-gatekeeper`, `research-assistant`, `senior-professor`.
- **Optional but recommended:** `~/projects/.research-factory/` directory
  (for `killed_ideas.md` dedup and `datasets_registry.json` context).

### Zotero MCP (optional but recommended)

Check the deferred tools list in your system prompt for `mcp__zotero__*` tools.

- **If present**: Zotero MCP is available. Corpus assembly (Phase 1B) will use
  it to find papers the user already owns.
- **If absent**: Zotero features are skipped silently. The skill proceeds with
  other sources. To install:
  ```
  claude mcp add zotero -- npx -y zotero-mcp@latest
  ```
  Requires: Node.js 18+, Zotero running with connector enabled.

## Commands

| Command | Purpose |
|---------|---------|
| `/econ-ideate data <dataset-path> [--topic-hint "..."]` | Data-first entry |
| `/econ-ideate corpus --topic "..." [--from-zotero COL \| --papers @p1 ...]` | Corpus-first entry |
| `/econ-ideate resume <run-id>` | Resume a paused or failed run at last phase |
| `/econ-ideate status` | List recent runs and their state |
| `/econ-ideate help` | Show this table |

**Common flags:**
- `--depth quick|standard|deep` (default: standard)
- `--auto` (skip phase-5 review pause)
- `--output-dir <path>` (override default output location)

---

## Step 0: Parse Subcommand

Read `$ARGUMENTS`. Extract the first word as subcommand.

Route:
- `data <path>` → Step 1A (Data-First Entry)
- `corpus` with `--topic`/`--from-zotero`/`--papers` → Step 1B (Corpus-First Entry)
- `resume <run-id>` → Step 9 (Resume)
- `status` → Step 10 (Status)
- `help` or unknown → print the command table above

If subcommand is missing or malformed, use AskUserQuestion to clarify.

---

## Invocation Contracts

Two harness facts that the rest of the spec assumes. Read once — every
"invoke X" phrasing below is shorthand for these patterns.

**Skill-tool invocation is recursive, not function-call.** A call to
`Skill(skill="<s>", args="...")` loads `<s>`'s SKILL.md into the current
conversation and hands execution back to econ-ideate. It does NOT return
a structured result. The protocol is:

1. Call `Skill(skill="<s>", args="...")`.
2. Execute `<s>`'s steps inline — econ-ideate becomes the driver.
3. Read whatever files `<s>` wrote to disk. Glob by mtime under the
   target skill's documented output directory.

Applies to `lit-all` (§1A.4, §1B.1), `papercheck` (§2.2), and
`fact-collect` (§8.3).

**Agent-tool auto-loads agents by name.** A call to
`Agent(subagent_type="<agent>", prompt="<task>")` automatically uses
`~/.claude/agents/<agent>.md` as the subagent's system prompt, tool
allowlist, and model. Do NOT read the `.md` file and inject it into a
`general-purpose` wrapper prompt — that is redundant on this harness.

Applies to scouts (§5.1), filter chain (§7.1–§7.3), and any other
named-agent dispatch in this spec.

**Exception — model override.** To override the agent's configured model
(e.g., §7.3 forces opus), pass `model: "opus"` on the Agent call. The
`subagent_type` still points to the correct agent file; only the model
flips. Background waiters and Phase 6 per-cell ideation workers (which
have no configured `.md`) keep `subagent_type: "general-purpose"`.

**NotebookLM `ask --json --save-as-note` emits mixed output.** The CLI
writes the JSON object and then appends a plain-text footer line like
`Saved as note: <Title> (<id>...)` after the closing `}`. Strict
`json.loads(whole_file)` fails. Every `ask --json --save-as-note`
invocation (§2.3, §2.4, §2.5, §3.1, §3.2, §4.1, §4.2, §8.0) must use the
**last-`}` trim** before parsing:

```python
raw = open(path).read()
payload = raw[:raw.rfind('}') + 1]
d = json.loads(payload)
```

The trim is safe because `ask --json` always emits exactly one top-level
JSON object followed by optional footer text; a valid response never
contains text after the closing brace. If `rfind('}')` returns -1, treat
the response as corrupt and log
`{"step":"notebooklm_response_corrupt","path":"..."}`.

---

## Step 1A: Data-First Entry

### 1A.1 Validate Input

Verify the dataset path exists. Accept: `.csv`, `.rds`, `.parquet`, `.dta`, `.xlsx`,
or a DATASTOR/API spec (string starting with `datastor:` or `api:`).

If file, check size and row count cheaply (`wc -l` for csv, `Rscript -e` for rds).

### 1A.2 Create Run Directory

Slugify the dataset name: `tcmb_policy_rate.csv` → `tcmb-policy-rate`.

Generate base `run_id`: `{YYYYMMDD}-{slug}` (e.g., `20260420-tcmb-policy-rate`).

**Collision handling:** If `~/projects/.econ-ideate/runs/<run_id>/` already
exists:
1. Check its `manifest.yaml`. If `completed: true`, append `-v2` (then `-v3`,
   etc.) until a free id is found.
2. If incomplete (paused or crashed), ask the user:
   - **Resume** existing → exit, suggest `/econ-ideate resume <run-id>`
   - **Start fresh** → append `-v2` suffix and proceed
   - **Overwrite** → only if user explicitly confirms; rename old dir to
     `<run-id>.archived-{timestamp}` before creating new

**Path expansion:** Resolve `~` to absolute path (e.g., via
`os.path.expanduser` or shell `eval echo`) BEFORE writing to
`manifest.yaml`. YAML parsers do not expand tildes on read.

Default output location: `~/projects/.econ-ideate/runs/<run-id>/`
(resolve `~` to absolute path at runtime; override via `--output-dir`).

Create the full phase-directory skeleton:
```
<run-id>/
├── manifest.yaml
├── events.jsonl
├── 00_input/  01_corpus/  02_synthesis/  03_stress_test/
├── 04_gaps/   05_convergence/  06_ideas/  07_shortlist/
├── 08_deliverables/  (holds podcast.mp3, briefing.md from phase 8.3b)
└── report.md  (created at phase 8)
```

**Path convention (binding for all subsequent phases).** `<run-dir>` is
the absolute path computed above. Every relative path referenced in
later phases — e.g. `02_synthesis/intake_map.md`,
`05_convergence/gap_data_matrix.md`, `08_deliverables/podcast.mp3` —
resolves against `<run-dir>`. Two acceptable implementations:
1. Prefix every `Write`, `Edit`, and `notebooklm download ...` path with
   `<run-dir>/` (explicit, preferred — survives any cwd change).
2. `cd <run-dir>` at the start of each phase and restore cwd at phase
   end.
Never write a phase artifact to the caller's cwd. If a later step
appears to do so, treat it as a spec bug and prefix with `<run-dir>/`.

### 1A.3 Profile the Dataset (Phase 1 for data-first)

**Language choice:** prefer R if `.rds`/`.dta` (via `haven`) or if R is
installed and user works in R; prefer Python otherwise. Check via
`command -v Rscript` and `command -v python3`. If neither exists, skip
scripted profile and ask user for manual description.

Write a profile script to `00_input/profile.R` or `00_input/profile.py`
that extracts:
- N rows, N cols
- Variable names + types
- Panel structure (unit ID, time ID) if detectable — heuristic: any column
  named `id`/`unit`/`firm`/`country`/`region`/`pid` + any column named
  `year`/`date`/`time`/`quarter`/`month`
- Time range and frequency (detect via diff of time column)
- Geographic scope if detectable (country codes ISO-2/ISO-3, Turkish NUTS,
  US FIPS, region strings)
- Missing rate per variable
- Top-level summary stats for numeric vars (mean, sd, min, max, p25, p75)

Run the script. Save output to `00_input/dataset_profile.md`.

**Opaque-variable guard.** If more than 30% of variable names look opaque
(single letters, `v01`–`v99`, generic `x1`/`x2`, fewer than 4 characters
and non-alphabetic), flag them and **ask the user for a glossary**:

> "The dataset has opaque variable names ({list first 5}). Can you
> provide a short glossary (`var → description`)? Without it, the
> literature reverse-lookup in the next step will produce noise."

Save glossary (if provided) to `00_input/variable_glossary.md` and use it
in 1A.4 instead of raw names.

If profiling script itself fails, ask the user for a 3-sentence manual
description and save to `00_input/dataset_profile.md`.

### 1A.4 Literature Reverse-Lookup (Phase 2 for data-first)

Build a `lit-all` seed query from the dataset profile:
- Variable names → keyword candidates
- Time range + geography → setting descriptor
- Add user's `--topic-hint` if provided

Invoke `lit-all` via the Skill tool with the assembled query (depth:
`standard`, or propagate user's `--depth`). Per the Invocation Contracts
section, Skill invocation is recursive: after
`Skill(skill="lit-all", args="...")` completes inline, this skill must:

1. Glob `_lit/lit-all-results-*.md` (fallback: `lit/`, `literature/`)
   and pick the newest by mtime.
2. Copy or symlink the sibling `.bib` to
   `<run-dir>/01_corpus/bibliography.bib`.
3. Parse the `.md` tables into `<run-dir>/01_corpus/corpus.json` (see
   Schema section).

Deduplicate against the user's Zotero library (check via `zotero_semantic_search`
before treating a paper as new). Filter entries whose result contains
`"Error:"` (Zotero local-API 404s on stale index items) and log
`{"step":"zotero_fetch_failed","item_key":"<key>"}` per the events
protocol.

Write `02_synthesis/data_angle_notes.md`: from the profile + the lit-returned
papers, note 3–5 angles where this dataset has coverage the literature lacks
(finer geography, longer panel, higher frequency, new variables, etc.).

### 1A.5 Rejoin Main Flow

Update manifest: mark phase 1 complete (profile done), phase 2 **partial**
(reverse-lookup corpus assembled, but synthesis not yet run). Proceed to
**Step 2 (Phase 2: Synthesize)** — data-first runs the full Piyas 3/6/7
synthesis on the reverse-lookup'd corpus, exactly like corpus-first. This
keeps both paths symmetric: every run produces a knowledge map before
gap-hunting.

The `data_angle_notes.md` from 1A.4 is retained and fed into phase 4 as
additional gap seeds, but it does not replace synthesis.

---

## Step 1B: Corpus-First Entry

### 1B.1 Resolve Corpus

Three modes:

**Mode A: Topic only** (`--topic "..." ` without `--from-zotero`/`--papers`)
- Invoke `lit-all` via Skill tool with the topic, depth per user flag.
  Per Invocation Contracts: execute lit-all inline, then glob the newest
  `_lit/lit-all-results-*.md` + `.bib` it writes (fallback: `lit/`,
  `literature/`). Copy the `.bib` to `<run-dir>/01_corpus/bibliography.bib`
  and parse the `.md` into `corpus.json`.
- Also run `zotero_semantic_search` on the topic to surface owned papers.
  Filter out entries whose result text contains `"Error:"` (Zotero local-
  API 404s on stale index items).
- **Degenerate-Zotero guard.** If the semantic search returns ≥ 50%
  `Error:` rows, OR if the top similarity score among valid items is
  < 0.2, treat the Zotero library as under-curated for this topic:
  log `{"step":"zotero_degenerate","errors":N,"top_sim":X}` and do NOT
  lean on Zotero as a primary source — rely on `lit-all` and a targeted
  WebSearch fallback instead. Empirically, a user's Zotero coverage on
  off-specialty topics can hit 80%+ failure (2026-04-21 ERPT run:
  16/20 404s, 0 topical valid items).
- Merge the two result sets; dedupe by DOI/citekey.

**Mode B: Zotero collection** (`--from-zotero "COLLECTION_NAME"`)
- Call `zotero_get_collections` to find the collection
- Call `zotero_get_collection_items` to fetch all entries
- If topic hint also given, optionally augment with `lit-all`

**Mode C: User papers** (`--papers @p1.pdf @p2.pdf ...`)
- Use the provided PDFs as the corpus base
- Extract metadata via a light pass (title/year/authors from filename + first page)
- Optionally augment with `lit-all` if `--topic` also given

### 1B.2 Create Run Directory

Same skeleton and collision-handling rules as Step 1A.2 (including the
binding path convention). Slug derivation, in order:
1. If `--topic` is provided: slugify the topic string (lowercase,
   non-alnum → `-`, collapse runs, strip leading/trailing `-`, cap 60
   chars).
2. Else if `--from-zotero COLLECTION` is provided: slugify the Zotero
   collection name.
3. Else (Mode C — `--papers` only, no topic): derive slug as
   `papers-{hash}` where `{hash}` is the first 8 hex chars of SHA1 over
   the sorted paper stems joined by `|`. If computing the hash fails
   for any reason, fall back to `papers-{YYYYMMDD-HHMM}`.

Slug must match `[a-z0-9][a-z0-9-]{0,60}` — reject and re-derive with a
fallback if it doesn't.

**Corpus-size cap.** Check corpus size after 1B.1:
- Effective upper bound is set by the user's NotebookLM plan tier
  (Standard 50, Plus 100, Pro 300, Ultra 600). The skill doesn't enforce
  this directly — NotebookLM will refuse uploads beyond the plan limit in
  Phase 2.1. When that happens, fall back gracefully (see 2.1).
- **> 200 papers (most plans):** warn the user. Upload + indexing will
  take a while (~30s–10min per source). Offer to narrow first: tighter
  topic, filter by year (≥ 2015), or restrict to top venues (AER/QJE/JPE/
  ReStud/Ecma + top 5 field). Default if user skips: upload up to the
  plan limit, prioritized by citation count / recency.
- **< 5 papers:** warn and offer to broaden the topic or drop to data-first
  if applicable. NotebookLM synthesis is weak below this threshold.

### 1B.3 Build Corpus Manifest

For each paper in the corpus, extract:
```json
{"citekey": "...", "authors": "...", "year": YYYY, "venue": "...",
 "doi": "...", "pdf_path": "...", "abstract": "...",
 "core_claim": "", "methodology": ""}
```

Write to `01_corpus/corpus.json`. Leave `core_claim` and `methodology` empty —
they get filled in phase 2.

### 1B.4 Proceed

Update manifest: phase 1 complete. Proceed to **Step 2 (Phase 2: Synthesize)**.

---

## Step 2: Phase 2 — Synthesize (Piyas 3, 6, 7) via NotebookLM

**Applies to both entry types.** For data-first, the corpus comes from the
reverse-lookup in 1A.4; the data-angle notes are preserved and fed to
phase 4.

**Engine:** NotebookLM is the primary synthesis engine. It ingests the
full corpus and answers Piyas-style questions with per-sentence citations
grounded in the uploaded sources. `papercheck` runs as a cross-check on
the top 5 papers (2.2) to catch any NotebookLM divergence.

### 2.0 Setup NotebookLM Notebook

**Auth preflight:**
```bash
notebooklm auth check --json
```
The CLI emits a JSON object with a top-level `status` field (`"ok"` or
`"error"`) plus a `checks` sub-object. Halt only if the overall signal is
bad:
- `status != "ok"`, OR
- the command exits non-zero, OR
- `checks.cookies_present == false` or `checks.sid_cookie == false`.

Do **not** halt on `checks.token_fetch == null` alone — that field is
often `null` on a fresh check even when auth is functional. A real auth
failure will surface on the first `notebooklm ask` / `source add` call;
the handler in the "NotebookLM auth expired mid-run" error section below
catches that case.

If halting: print
> "NotebookLM auth preflight failed (status != ok or cookies missing).
> Run `notebooklm login` and retry `/econ-ideate resume {run-id}`."

**Create or reuse notebook (resume-safe).**

1. Read `manifest.yaml`. If `notebooklm_notebook_id` is already set
   (prior run or resume), verify the notebook still exists:
   ```bash
   notebooklm source list -n <existing_id> --json
   ```
   - Exit 0 → reuse it. Skip the `create` step and the re-upload in 2.1
     (sources are already there; proceed straight to the indexing
     barrier).
   - Exit non-zero OR error message indicating notebook missing / auth
     mismatch → log `{"step":"notebook_reuse_failed","reason":"..."}`
     and fall through to create.

2. Create only when no reusable notebook exists:
   ```bash
   notebooklm create "econ-ideate: {run-id}" --json
   ```
   Parse `id` from JSON. Save as `notebooklm_notebook_id` in
   `manifest.yaml` **immediately** (before any upload) so a crash
   mid-2.1 doesn't orphan the notebook on the next resume.

3. **All subsequent NotebookLM calls in this run MUST use
   `-n <notebook_id>`** (explicit flag — the skill is parallel-safe and
   must not rely on `notebooklm use`).

**Orphan cleanup.** If collision handling in 1A.2/1B.2 archives a run
(`<run-id>.archived-{timestamp}`), also note its
`notebooklm_notebook_id` (if any) in a top-level
`~/projects/.econ-ideate/orphans.jsonl` with `{archived_at, run_id,
notebook_id}`. The user can later sweep these with `notebooklm delete
<id>`. The skill itself never auto-deletes notebooks.

### 2.1 Upload Corpus to NotebookLM

For each paper in `01_corpus/corpus.json`:
1. Prefer local PDF (`pdf_path` if present).
2. Fall back to DOI resolver URL (`https://doi.org/{doi}`).
3. Fall back to any URL in the metadata.
4. Skip papers with none of the above; log to `events.jsonl` with reason
   `no_ingestable_source`.

Upload with:
```bash
notebooklm source add <path-or-url> --json -n <notebook_id>
```

Parse `source_id` from each response. Update `corpus.json` entries with
`notebooklm_source_id`.

**`source add` is NOT atomic.** A failing response
(`{"error": true, ...}` with no `id`) does not mean "no state change" —
the server may still have created a source record with `status: error`
that shows up in the next `source list`. After uploading ALL intended
sources, **run `notebooklm source list --json -n <notebook_id>` once to
reconcile**: this is the authoritative set. Record every source_id
(including error-status ones) so downstream cleanup can delete them.

**Wait for indexing (synchronization barrier).** Use the native
`notebooklm source wait` command — there is no need for a custom polling
subagent on short corpora. For each non-error source_id from the
reconciliation above:

```bash
notebooklm source wait <source_id> -n <notebook_id> --timeout <T> --json
```

Timeout by source type:
- PDF / file: `--timeout 600` (10 min; large PDFs can take multi-minute)
- URL / web page: `--timeout 120` (web pages typically index in seconds)

For corpora > 20 sources, dispatch one background Agent
(`subagent_type: general-purpose`) that loops through the waits; the main
thread awaits the subagent's return. For ≤ 20 sources, run the waits
serially in the main thread — observed wall-time for all-URL corpora is
under 60 seconds total (2026-04-21 ERPT run: 6 web sources, 32 s total).

**Ordering rule.** Phase 2.2 (papercheck on local PDFs) MAY run in
parallel with this wait — papercheck never calls NotebookLM. Phases 2.3,
2.4, 2.5, 2.6 and everything downstream (3.x, 4.x, 8.1) **MUST NOT
start** until the wait completes. Premature `ask` calls against a
partially-indexed corpus produce answers that look grounded but reflect
only the subset indexed at query time.

**Content-usability probe (after indexing).** `status: ready` does NOT
guarantee the source contains usable content — paywalled pages can
ingest successfully but contain only boilerplate (2026-04-21 ERPT run:
Tandfonline DOI page indexed `ready` with nothing but site chrome).
After the wait barrier, issue ONE probe:

```bash
notebooklm ask "For each source in this notebook, reply with one sentence of its substantive content. If a source contains only website boilerplate, navigation, or a paywall stub, reply EMPTY for that source." --json -n <notebook_id>
```

Parse using the trim-to-last-`}` rule from Invocation Contracts. Count
sources flagged `EMPTY`; subtract from the `ready` count to get
`n_sources_usable`. Log
`{"step":"content_probe","n_ready":X,"n_usable":Y,"n_empty":Z}` and use
`n_sources_usable` (not `n_sources_ready`) for the source-count sanity
check below.

**Source-count sanity (uses `n_sources_usable`):**
- If < 5 usable sources: halt with a warning. NotebookLM synthesis
  requires enough material.
- If source count exceeds the NotebookLM plan limit (Standard 50, Plus
  100, Pro 300, Ultra 600), upload fails partway. Ask the user to either
  narrow the corpus or skip the overflow.

### 2.2 Top-5 Deep Read (papercheck Cross-Check)

Rank papers by signal (Zotero annotations → citation count → venue prestige
→ recency). Pick top 5.

For each with a local PDF: invoke `papercheck` via Skill tool, requesting
core claim, methodology tag, key assumptions, contested vs accepted
findings. Per Invocation Contracts, this is a recursive sub-skill load —
execute papercheck inline, then read its output per papercheck's own
conventions (the papercheck skill documents the
cached-pack location). Aggregate the results into
`02_synthesis/papercheck_topN.md`.

Papers without local PDFs: skip papercheck silently (NotebookLM still
covers them via URL/DOI ingestion in 2.1). This is the key difference
from v0.1 — no halting on missing PDFs; NotebookLM fills the gap.

Update `corpus.json` for top 5 with `papercheck_extracted: true/false`.

### 2.3 Intake Map (Piyas Prompt 3) — NotebookLM

Source prompt (verbatim):
> "I'm going to share [X] papers on [topic].
> Before I ask anything, do this:
> 1. List every paper by author + year + core claim in one sentence
> 2. Group them into clusters of shared assumptions
> 3. Flag any paper that contradicts another
> Don't summarize. Map the landscape."

Invoke:
```bash
notebooklm ask "<Piyas 3 prompt, with [X] replaced by corpus size and
[topic] replaced by run topic>" --json -n <notebook_id> \
  --save-as-note --note-title "Intake Map (Piyas 3)"
```

Parse the JSON response using the trim-to-last-`}` rule from the
Invocation Contracts section (the `--save-as-note` footer breaks strict
JSON parse). Extract `answer` + `references` (list of `{source_id,
citation_number, cited_text, chunk_id?}`). Write to
`02_synthesis/intake_map.md`:
- The answer verbatim (with citation markers — note §2.7 on `[N]`,
  `[N, M]`, and `[N-M]` forms)
- A "References" section listing each citation with its `source_id`,
  `cited_text`, and the matching citekey from `corpus.json`

**Sections §2.4, §2.5, §3.1, §3.2, §4.1, §4.2, and §8.0 use the same
parsing contract.** They reference "same format as 2.3".

### 2.4 Methodology Audit (Piyas Prompt 6) — NotebookLM

Source prompt (verbatim):
> "Compare the research methodologies used across all papers.
> Group by: surveys, experiments, simulations, meta-analyses, case studies.
> Then flag:
> - Which methodology dominates this field and why?
> - Which methodology is underused?
> - Which paper's methodology is weakest and why?"

**Economics adaptation (append to prompt):** "Expand the methodology
groups to include: structural / reduced-form (DiD, IV, RDD, event study)
/ survey / experiment / simulation / meta-analysis / case study /
sufficient statistics."

Invoke `notebooklm ask ... --save-as-note --note-title "Methodology Audit
(Piyas 6)"` and save output to `02_synthesis/methodology_audit.md` with
the same format as 2.3 (answer + references).

### 2.5 Knowledge Map (Piyas Prompt 7) — NotebookLM + Mind Map

Source prompt (verbatim):
> "Create a structured knowledge map of this entire literature.
> Format:
> - Central claim the field orbits around
> - 3-5 supporting pillars (well-established sub-claims)
> - 2-3 contested zones (active debates)
> - 1-2 frontier questions (nobody's solved yet)
> - 3 papers a newcomer MUST read first and why
> Output as a clean outline, not prose."

Invoke `notebooklm ask ... --save-as-note --note-title "Knowledge Map
(Piyas 7)"` → save to `02_synthesis/knowledge_map.md`.

**Also generate the NotebookLM mind map** (synchronous, reliable):
```bash
notebooklm generate mind-map -n <notebook_id>
notebooklm download mind-map 02_synthesis/knowledge_mindmap.json \
  -n <notebook_id>
```

### 2.6 Cross-Check Verification

For each of the 5 papers with papercheck output in 2.2:
- Ask NotebookLM targeted question: `notebooklm ask "What is the core
  claim and methodology of {author, year}? Cite only that source."
  --json -n <notebook_id>`
- Compare NotebookLM's answer with papercheck's extraction.
- If divergence on methodology tag or core claim: log a row in
  `02_synthesis/verification.md` with both versions + the papercheck
  page-anchored quote. Flag for user review but do not halt.

This catches NotebookLM hallucinations on the highest-signal papers.

### 2.7 Grounding Discipline (Phases 2–4)

Everything in phases 2.3 through 4.2 inherits **NotebookLM's native
grounding**: every claim carries citation markers `[N]` that resolve to
source IDs and quoted text. The skill must **preserve these citations
verbatim** in all derived artifacts. Do not paraphrase away the markers.

If a downstream phase (3.x, 4.x) needs a claim NOT supported by the
NotebookLM output, mark it `[synthesis — no direct citation]` — a
visible reliability flag. Do not fabricate references.

### 2.8 Log and Proceed

Append event: `{"phase":"2","step":"synthesize_complete",
"corpus_size":N, "notebook_id":"...", "n_sources_ready":N,
"n_sources_error":N}`. Update manifest, proceed to Step 3.

---

## Step 3: Phase 3 — Stress-Test (Piyas 1, 9)

### 3.1 Contradictions (Piyas Prompt 1) — NotebookLM

Source prompt (verbatim):
> "Across all papers uploaded, identify every point where two
> or more authors directly contradict each other.
> For each contradiction:
> - State both positions
> - Name the papers
> - Explain WHY they likely disagree (methodology, dataset, era)
> Format as a table."

Invoke:
```bash
notebooklm ask "<Piyas 1 verbatim>" --json -n <notebook_id> \
  --save-as-note --note-title "Contradictions (Piyas 1)"
```

Write answer + references to `03_stress_test/contradictions.md` (same
format as 2.3 — verbatim answer with `[N]` markers + References section).

### 3.2 Shared Untested Assumptions (Piyas Prompt 9) — NotebookLM

Source prompt (verbatim):
> "List every assumption that the MAJORITY of these papers share
> but never explicitly test or justify.
> For each assumption:
> - State it clearly
> - Name 1-2 papers that rely on it most
> - Explain what would happen to the field if the assumption
>   turned out to be wrong"

Invoke `notebooklm ask ... --save-as-note --note-title "Shared
Assumptions (Piyas 9)"` → save to `03_stress_test/shared_assumptions.md`.

### 3.3 Log and Proceed

Append event: `{"phase":"3","step":"stress_test_complete"}`. Proceed to Step 4.

---

## Step 4: Phase 4 — Gap-Hunt (Piyas 2, 5)

### 4.1 Citation Lineage (Piyas Prompt 2) — NotebookLM

Source prompt (verbatim):
> "Pick the 3 most-cited concepts across these papers.
> For each concept:
> - Who introduced it first?
> - Who challenged it?
> - Who refined it?
> - What's the current consensus (if any)?
> Show me the intellectual lineage like a family tree."

Invoke `notebooklm ask "<Piyas 2 verbatim>" --json -n <notebook_id>
--save-as-note --note-title "Citation Lineage (Piyas 2)"`. Save answer +
references to `04_gaps/citation_lineage.md`.

### 4.2 Gap Scanner (Piyas Prompt 5) — NotebookLM

Source prompt (verbatim):
> "Based on all uploaded papers, identify the 5 research
> questions that NOBODY has fully answered yet.
> For each gap:
> - Why does it exist? (too hard, too niche, overlooked?)
> - Which existing paper came closest to answering it?
> - What methodology would be needed to close it?"

**Economics adaptation (append to prompt):** "Expand the `why does it
exist` list to include: recent-data availability, new natural experiment,
regulatory change, non-Anglophone setting."

Invoke `notebooklm ask ... --save-as-note --note-title "Gap Scanner
(Piyas 5)"`. Save to `04_gaps/gap_scanner.md`.

### 4.3 Consolidate Gap List

Merge the gaps surfaced in 4.1 and 4.2 (and, if data-first, the data-angle
notes from 1A.4) into a single enumerated gap list. Deduplicate. Assign
gap IDs: `G1, G2, ...`.

Save to `04_gaps/gap_list.md`.

### 4.4 Log and Proceed

Append event: `{"phase":"4","step":"gaps_consolidated","n_gaps":N}`.
Proceed to Step 5.

---

## Step 5: Phase 5 — Converge (Scouts + Gap × Data Matrix)

This is the **pivot phase**. Four scout agents fan out in parallel, each
briefed with the gap list from phase 4. Their outputs become the columns of
the gap × data matrix.

### 5.1 Launch Four Scouts in Parallel

Per the Invocation Contracts section, each scout is dispatched directly
by name — the Agent tool auto-loads `~/.claude/agents/<name>.md` as the
subagent's system prompt, tools, and model. Do NOT read the `.md` files
or inject them into a `general-purpose` wrapper.

Launch all four in a **single message** (four concurrent Agent tool
calls):

- `Agent(subagent_type="data-scout", description="scout", prompt=<TASK>)`
- `Agent(subagent_type="world-watcher", description="scout", prompt=<TASK>)`
- `Agent(subagent_type="mind-scanner", description="scout", prompt=<TASK>)`
- `Agent(subagent_type="project-scanner", description="scout", prompt=<TASK>)`

No `model` override (scouts use their configured defaults). No
`isolation` flag. `<TASK>` is identical for each call:

```
## Task: econ-ideate convergence phase

Run ID: {run-id}
Input type: {corpus-first | data-first}

For each gap in the list below, find data sources, events, prior notes,
or reusable code that would enable testing it. Respect your native output
conventions (emit bullets in your usual format). AT THE END of your
report, append a single "## econ-ideate cells" section with one line per
(gap, source) pair:

  - G{N} | {source_type} | {source_id} | {availability} | {one-line note}

Where:
  gap_id        = G1..Gn (match gap_list.md)
  source_type   = dataset | api | policy-event | registry | prior-code | note
  source_id     = short identifier (e.g., "FRED:GDPC1", "EVDS:TP.TUFE1YI.T1",
                  "TCMB 2019-07-06 rate cut", "Zenodo DOI", "~/projects/X")
  availability  = in-hand | public | restricted | unknown

## Gaps
{full content of 04_gaps/gap_list.md}

## Knowledge Map (topic framing)
{full content of 02_synthesis/knowledge_map.md}

## In-Hand Dataset (data-first only)
{full content of 00_input/dataset_profile.md — skip if corpus-first}
```

Agents run concurrently. Expected wall-clock: 2–5 minutes.

**Note on format alignment:** scouts have their own output protocols;
rather than overriding them, we ask for both (native report + append
the cell list). Phase 5.2 parses the "## econ-ideate cells" section
specifically; native output is saved verbatim for audit.

### 5.2 Collect Scout Outputs

For each returned scout, save raw output to
`05_convergence/scout_{agent-name}.md`.

Parse the **"## econ-ideate cells"** section from each (see format in 5.1).
Extract each line as a row. If a scout returned no such section (failed to
follow the format), log a warning and try a second parse: look for any
bullet that references a gap id (`G\d+`) and extract what you can — treat
the rest as free-text commentary.

Write the consolidated source list to `05_convergence/data_availability.md`
with columns: `gap_id | source_type | source_id | availability | scout |
note`.

### 5.3 Build the Gap × Data Matrix

Construct `05_convergence/gap_data_matrix.md` as a **long-format
markdown table** (one row per non-zero gap/source pair). This avoids the
"wide table with one column per source" blow-up and makes the format
trivially machine-parseable.

**Preprocessing (before writing the table):**
1. From the scout cell list, dedupe sources (canonical `source_id`).
2. Drop any (gap, source) pair with feasibility `0` — keeps the table
   reviewable.
3. **Per-gap cap.** After dedup and feasibility-0 drop, cap each gap at
   `max(5, top-feasibility-rows-for-that-gap)` rows. Rank remaining rows
   by (feasibility desc, in-hand-availability, scout count). Drop the
   tail. If total matrix rows still exceed 60, log
   `{"step":"matrix_oversized","rows":N,"cap_applied":60}` and WARN the
   user at §5.5 pause so they know review is larger than expected.
   (2026-04-21 ERPT run produced 92 rows before the cap.)
4. For data-first runs, append a row for every gap where the in-hand
   dataset has a non-zero feasibility estimate (produced from the
   data-angle notes in 1A.4).

**Required table format** (verbatim header; the parser in 9.4 keys on
this exact column set, case-insensitive):

```markdown
| Gap | Source | Feasibility | Note | Flags |
|-----|--------|-------------|------|-------|
| G1  | FRED:GDPC1 | 3 | clean fit; quarterly 1947– | |
| G1  | EVDS:TP.TUFE1YI.T1 | 2 | Turkish subset; post-2005 | |
| G2  | Zenodo:doi/10.5281/... | 1 | restricted access; N~400 | [killed: KI-007, J=0.6] |
```

Column contract:
- `Gap` — gap ID matching `G\d+` from `gap_list.md`. Required.
- `Source` — canonical source_id from the scout cell list. Required.
- `Feasibility` — integer 1, 2, or 3. Required. (0 rows are dropped in
  preprocessing and never written.)
  - 1 = marginally possible (serious data gaps or weak identification)
  - 2 = feasible with caveats (needs merge / small N / restricted
    access)
  - 3 = clean fit (data in hand or public, adequate N, ID strategy
    visible)
- `Note` — one-line justification. Required (may be empty string).
- `Flags` — optional. Comma-separated. Recognized flags:
  `[killed: KI-NNN, J=0.X]` (from 5.4), `[scout-conflict]`,
  `[user-edit]`.

**Companion side-file** (for the audit trail, not parsed):
Write `05_convergence/scout_conflicts.md` listing any gaps where two or
more scouts surfaced contradictory feasibility estimates for the same
source.

### 5.4 Deduplication Check

Before proceeding, check if `~/projects/.research-factory/killed_ideas.md`
exists. If not, skip this sub-step. If yes:

**Matching algorithm** (do NOT use naive substring):

**Step 0 — Direct KI reference pass (fires first).** Scouts sometimes
self-annotate killed-idea references in their cell output (e.g.,
`source_id = ~/projects/.research-factory/killed_ideas.md#KI-019`). Run
`re.findall(r'KI-\d+', source_id + note)` on every matrix cell; any hit
is flagged unconditionally as `[killed: KI-NNN, explicit]`. Without this
pass, the Jaccard step dilutes topical tokens with shared boilerplate
(`killed`, `ideas`) and misses these (2026-04-21 ERPT run produced 4
self-annotated KI references; Jaccard at 0.3 found 0 of them).

**Step 1–4 — Jaccard pass (for cells not already flagged in Step 0):**
1. For each killed idea, extract its **keyword set**: lowercased nouns and
   adjectives from its title + `keywords:` field (if present), minus
   English + Turkish stopwords. Typical result: 4–8 tokens.
2. For each matrix cell with feasibility ≥ 2 AND no `[killed:]` flag yet,
   construct the prospective idea's keyword set: tokens from gap text +
   source_id + source_type — EXCLUDING any path segment that looks like
   a KI registry path (`.research-factory/killed_ideas.md`) so the
   Jaccard tokens reflect the topic, not the registry metadata.
3. Compute **Jaccard similarity** = |A ∩ B| / |A ∪ B|.
4. If Jaccard ≥ 0.5 OR if a rare domain-specific token (e.g., a
   specific institution, policy name, dataset code) appears in both:
   flag the cell with `[killed: KI-NNN, J=0.X]`.
5. Below 0.5: do not flag.

Do **not** silently drop any flagged cell — user sees it in Phase 5.5
review and decides.

### 5.5 PAUSE for User Review

**Default behavior (no `--auto` flag):** stop here.

Print to user:
```
Phase 5 complete. Gap × data matrix saved to:
  {run-dir}/05_convergence/gap_data_matrix.md

Review the matrix. Edit feasibility scores, remove rows/cols, or add notes.
When ready, run:
  /econ-ideate resume {run-id}

To skip this pause in future runs, pass --auto.
```

Update manifest:
```yaml
current_phase: 5
pause_reason: "awaiting user review of gap × data matrix"
```

Exit. (The next `/econ-ideate resume` re-enters at Step 6.)

**If `--auto`:** skip pause, proceed directly to Step 6.

---

## Step 6: Phase 6 — Ideate (Sonnet Per Cell)

### 6.1 Identify Viable Cells

Re-read `05_convergence/gap_data_matrix.md` (it may have been user-edited;
see parsing tolerance in 9.3).
Collect all cells with feasibility ≥ 2 AND not flagged `[killed: ...]`.

**Cell count rules:**
- **3 ≤ cells ≤ 20:** proceed to 6.2.
- **Cells < 3:**
  - Interactive mode (default): warn user, ask whether to lower threshold
    to ≥ 1 or re-run phase 5 scouts with broader context.
  - `--auto` mode: lower threshold to ≥ 1 automatically. If still < 3,
    halt with a "too few viable cells — re-run scouts or widen corpus"
    message. Do not fabricate cells.
- **Cells > 20:**
  - Warn: "{N} viable cells — Phase 6 will dispatch {N} parallel Sonnet
    agents. Estimated cost: high." Ask user to either batch top 20 (by
    feasibility, then gap ID) or proceed with all.
  - `--auto` mode: batch top 20 automatically, log the skipped cells.

### 6.2 Per-Cell Ideation — Delegate to Sonnet

For each viable cell `(gap_id, data_source)`, dispatch a Sonnet agent (per
the `model-routing` rule — 3+ mechanical-ish calls). Send in parallel.

Each agent prompt contains:
1. The specific gap (text from gap_list.md)
2. The specific data source (entry from data_availability.md)
3. Relevant excerpt from `02_synthesis/knowledge_map.md`
4. Required output (strict markdown template):

```markdown
# Idea: {slug}
## Hypothesis
{one paragraph, testable prediction with expected sign/magnitude}
## Identification strategy
{DiD | IV | RDD | event study | structural | synthetic control | ...}
## Data requirements
- Treatment var: ...
- Outcome var: ...
- Running var / instrument / timing: ...
- Sample: N ≈ {estimate}
## Main specification (pre-specified)
{one equation or clear natural-language spec}
## Threats to identification
{list 2-3}
## Related literature
{2-3 papers from corpus with one-line rationale each}
## Novelty claim
{one sentence: what's new vs closest paper}
```

Instruct each agent: *"If you are uncertain about any step, report what you
found and what you're unsure about — do not guess."*

### 6.3 Save Per-Cell Briefs

Write each result to `06_ideas/idea_{NNN}.md` (zero-padded index). Log
failures/uncertainties to `events.jsonl`.

Spot-check at least one brief as Opus before proceeding. If the sonnet
output quality is poor, re-run the whole phase at opus (not sonnet again).

### 6.4 Log and Proceed

Append event: `{"phase":"6","step":"ideation_complete","n_ideas":N}`.
Proceed to Step 7.

---

## Step 7: Phase 7 — Filter + Rank

Three-stage filter matching the factory pattern, but on ideas we generated
ourselves.

### 7.1 Data Gatekeeper

Per Invocation Contracts: `Agent(subagent_type="data-gatekeeper",
description="gatekeeper", prompt=<prompt>)`.

`<prompt>` contains:
- All ideas from `06_ideas/` (concatenated)
- The dataset registry: `~/projects/.research-factory/datasets_registry.json`
  (if exists — else pass scout-surfaced sources only)
- The killed ideas registry (same path as phase 5.4)
- Context: "Verify data exists, N is sufficient, key variables present.
  Classify each: PASS / CONDITIONAL / KILL."

Save output to `07_shortlist/gatekeeper.md`. Only PASS + CONDITIONAL
advance.

### 7.2 Research Assistant

Per Invocation Contracts: `Agent(subagent_type="research-assistant",
description="rank", prompt=<prompt>)`.

`<prompt>` contains:
- Gatekeeper-approved ideas
- Instruction: quick-kill weak designs, score survivors on identification /
  data fit / novelty / feasibility, pairwise compare top candidates,
  output ranked list.

Save output to `07_shortlist/research_assistant.md`.

### 7.3 Senior Professor (Opus)

Per Invocation Contracts with model override:
`Agent(subagent_type="senior-professor", model="opus",
description="rank", prompt=<prompt>)`.

`<prompt>` contains:
- Ranked list from 7.2
- `02_synthesis/knowledge_map.md` for context
- Strategic context: "Prof. Tasdemir, Istanbul Medeniyet University.
  Targets top-5 and strong field journals. Apply should-we-not-just-can-we."

**Model override rationale:** deep judgment phase runs at opus regardless
of the agent-file default. The `model: "opus"` parameter on the Agent
call takes precedence over any model spec in `senior-professor.md`.

Save output to `07_shortlist/ranked.md`. Expected format:
```markdown
| Rank | Idea | Contribution | Competition | Journal fit | Recommendation |
|------|------|--------------|-------------|-------------|----------------|
| 1 | ... | ... | ... | ... | PURSUE |
| 2 | ... | ... | ... | ... | PURSUE |
| 3 | ... | ... | ... | ... | CONDITIONAL |
| 4 | ... | ... | ... | ... | PASS |
```

### 7.4 Top-Idea Brief

Take the #1 idea. Expand it into a PAP-ready brief combining the idea file
from `06_ideas/`, the gatekeeper note, and the senior professor's
justification. Save to `07_shortlist/top_idea_brief.md`.

---

## Step 8: Phase 8 — Report + RDR

### 8.0 Generate Executive Summary (Piyas Prompt 8) — NotebookLM

**This step must run before 8.1.** Without it, the report template's
Executive Summary section has no content to populate.

Source prompt (verbatim):
> "Pretend I have to explain this entire body of research to a
> smart non-expert in 5 minutes.
> Give me:
> 1. The one-sentence version of what this field has proven
> 2. The one honest admission of what it still doesn't know
> 3. The single real-world implication that matters most
> No jargon. No hedging. No academic throat-clearing."

Invoke:
```bash
notebooklm ask "<Piyas 8 prompt verbatim>" --json -n <notebook_id> \
  --save-as-note --note-title "Executive Summary (Piyas 8)"
```

Parse the JSON response. Write to
`<run-dir>/08_deliverables/executive_summary.md`:
- The answer verbatim (preserving `[N]` citation markers per the 2.7
  grounding discipline)
- A "References" section listing each citation with its `source_id`,
  `cited_text`, and matching citekey from `corpus.json`

If the `ask` call fails or returns an empty answer, retry once with the
prefix "Based strictly on the uploaded sources, ". If the retry also
fails, save both attempts to `08_deliverables/_failed_piyas8.md`, write
a placeholder `executive_summary.md` with the text "*Executive summary
generation failed; see `_failed_piyas8.md`.*", and continue — the
report assembly in 8.1 should still produce a usable document.

Append event: `{"ts":"...","skill":"econ-ideate","run_id":"...",
"phase":"8","step":"executive_summary_generated","status":"ok|failed"}`.

### 8.1 Consolidate Final Report

Assemble `<run-dir>/report.md` with sections (use `<run-dir>/` prefix
on every include):

```markdown
---
run_id: {run-id}
input_type: {corpus-first | data-first}
top_idea: {slug of #1}
ideas_shortlisted: {N passing}
gaps_found: {N from phase 4}
corpus_size: {N}
completed: {YYYY-MM-DD}
---

# Econ Ideate Report — {topic or dataset}

## Executive Summary
{include content of 08_deliverables/executive_summary.md — generated by
step 8.0 from Piyas Prompt 8}

## Knowledge Map
{include content of 02_synthesis/knowledge_map.md}

## Gap × Data Matrix
{include 05_convergence/gap_data_matrix.md}

## Shortlist (Top 5)
{include 07_shortlist/ranked.md table + per-idea one-paragraph abstract
 linking to 06_ideas/idea_NNN.md}

## Top Idea — Pre-Analysis Brief
{include 07_shortlist/top_idea_brief.md}

## Audit Trail
- Phases completed: 1–8
- Scouts run: data-scout, world-watcher, mind-scanner, project-scanner
- Agents used: {list}
- Filter survival rates: gaps→ideas→gatekeeper→ra→sr (%)
- Killed-idea overlaps: {count, list of KI-NNN}
```

### 8.2 Auto-Create RDR

If the current project has a `$LAB_DIR/decisions/` directory (per the
`fact-aware-research` rule), create an RDR for the top idea:

1. Scan existing files to determine next `RDR-NNN` number
2. Write `RDR-NNN-{top-idea-slug}.md` using the RDR template
3. Update `$LAB_DIR/decisions/INDEX.md`
4. Include in the RDR: hypothesis, identification, data, scored rationale,
   link back to this run's `report.md`

If no `decisions/` directory exists, skip silently.

### 8.3 Auto-Offer Fact Collection

Scan the knowledge map and stress-test for institutional facts surfaced
(regulatory thresholds, policy dates, dataset quirks). Offer:

> "Surfaced N institutional facts. Want to record them with /fact-collect?"

Do not run `fact-collect` without user confirmation.

### 8.3b Generate NotebookLM Deliverables (Optional)

Ask the user whether to generate long-form artifacts from the NotebookLM
notebook:

> "Generate additional deliverables from the NotebookLM corpus?
>   [a] Audio overview (podcast-style deep-dive, ~10-20 min to generate)
>   [b] Briefing document (markdown, ~5-15 min)
>   [c] Both
>   [d] Skip"

On `--auto`, default to `d` (skip) to avoid unexpected rate-limit
failures. The knowledge map mind-map is already downloaded in 2.5.

If user picks (a) or (c):
```bash
notebooklm generate audio "Focus on the knowledge map's central claim, \
  contested zones, and frontier questions. Ground every statement in \
  the source papers." --json -n <notebook_id>
```
Parse `artifact_id`. Dispatch background Agent (`subagent_type:
general-purpose`) with:
```
Prompt: Wait for artifact {artifact_id} in notebook {notebook_id}. Use
  `notebooklm artifact wait {artifact_id} -n {notebook_id} --timeout 1800`.
  Then `notebooklm download audio <run-dir>/08_deliverables/podcast.mp3
  -a {artifact_id} -n {notebook_id}`. Report completion or failure.
```

If user picks (b) or (c):
```bash
notebooklm generate report --format briefing-doc -n <notebook_id> --json
```
Same background-wait-and-download pattern into
`<run-dir>/08_deliverables/briefing.md`.

**Note on rate limits.** Audio generation fails ~20% of the time due to
Google's rate limits (per notebooklm skill's known limitations). If the
subagent reports failure, log it to `events.jsonl`. The main report and
mind map are unaffected — they're already in the run directory.

### 8.4 Present to User

Print:
```
Econ-ideate run complete: {run-id}

Top 3 ideas:
  1. {slug} — PURSUE — {one-line rationale}
  2. {slug} — PURSUE — {one-line rationale}
  3. {slug} — CONDITIONAL — {one-line rationale}

Full report: {run-dir}/report.md
Top idea brief: {run-dir}/07_shortlist/top_idea_brief.md

Next steps:
- Refine the top idea interactively: /interview-me {top_idea_slug}
- Test it against data: /factory feasibility "{top_idea_hypothesis}"
- Record institutional facts: /fact-collect (if offered above)
```

Mark manifest: `completed: true`, `completed_at: {timestamp}`.

---

## Step 9: Resume (`/econ-ideate resume <run-id>`)

### 9.1 Locate Run

Search for `<run-id>` in:
- `~/projects/.econ-ideate/runs/<run-id>/`
- Any `ideas/<run-id>/` under the cwd if inside a project
- If `--output-dir` was used in the original run, it must be in the manifest

If not found, list all runs with partial-match suggestions.

### 9.2 Read Manifest

Read `<run-dir>/manifest.yaml`. Extract `current_phase`, `completed_phases`,
`input_type`, `pause_reason`.

### 9.3 Re-Enter at Correct Phase

- If paused at phase 5 (user review): re-read `gap_data_matrix.md` and jump
  to Step 6 (see 9.4 for parsing tolerance).
- If failed mid-phase: re-enter at the start of that phase (idempotent —
  each phase overwrites its own outputs). **Before overwriting**, archive
  the previous attempt to `<phase-dir>/.previous_attempt/` (with timestamp)
  in case partial work is salvageable.
- If completed: report that and offer to view the report.

Set manifest `pause_reason: null`, update `current_phase`, continue.

### 9.4 Matrix Format Tolerance

The canonical format is defined in 5.3 (long-format markdown table with
columns `Gap | Source | Feasibility | Note | Flags`). The parser MUST:

1. **Find the table.** Accept the first markdown table whose header row
   (case-insensitive) contains at least `gap`, `source`, and
   `feasibility` as distinct columns. Free text and other tables above
   or below are ignored.
2. **Extract rows.** For each data row, require `Gap` matches `G\d+`
   and `Feasibility` is an integer in `{1, 2, 3}`. Rows failing either
   check are logged to `events.jsonl` with
   `{"step":"matrix_row_skipped","reason":"...","row":"..."}` and
   dropped. Do NOT halt on individual bad rows.
3. **Accept extra columns.** User-added columns beyond the contract are
   preserved on any rewrite but otherwise ignored.
4. **Honor Flags.** Any row whose `Flags` column contains `[killed:`
   (regardless of the rest) is treated as killed — same behavior as
   dedup flags from 5.4.
5. **Halt condition.** If zero valid rows survive, do NOT silently
   proceed. Print:
   > "Matrix at {path} has no valid rows after parsing. Either edit the
   > file to add feasibility-≥1 rows or delete it and re-run
   > `/econ-ideate resume {run-id}` to rebuild from scout output."

**Backward-incompatibility note.** Pre-v0.2.1 runs wrote a wide-format
matrix (gaps × sources). If resuming such a run, the parser will find
no valid `Gap | Source | Feasibility` triples. Re-run Phase 5 from the
scout output (still in `05_convergence/scout_*.md`) rather than trying
to transform the old matrix in place.

---

## Step 10: Status (`/econ-ideate status`)

### 10.1 Find All Runs

Glob for manifest files:
```
~/projects/.econ-ideate/runs/*/manifest.yaml
<cwd>/ideas/*/manifest.yaml  (if inside a project)
```

### 10.2 Display Table

```markdown
## Econ-Ideate Runs

| Run ID | Type | Topic/Dataset | Phase | State | Started | Top Idea |
|--------|------|---------------|-------|-------|---------|----------|
| 20260420-monetary-em | corpus | monetary policy EM | 5 | paused | 2026-04-20 | — |
| 20260418-tcmb-rate | data | tcmb_policy_rate | 8 | complete | 2026-04-18 | em-policy-asymmetry |
```

If no runs: "No runs yet. Start one with `/econ-ideate data ...` or
`/econ-ideate corpus --topic ...`."

---

## Schema Contracts

### manifest.yaml

```yaml
run_id: 20260420-monetary-em
version: "0.2.1"
input_type: corpus-first          # corpus-first | data-first
input:
  topic: "monetary policy EM"     # corpus-first
  zotero_collection: null
  papers: null
  dataset_path: null              # data-first
  dataset_profile: null
depth: standard                   # quick | standard | deep
scoring_authority: senior-professor
auto: false                       # true skips phase-5 pause + phase-8 gen prompts
notebooklm_notebook_id: abc123...  # set in 2.0; used by all notebooklm calls
output_dir: ~/projects/.econ-ideate/runs/20260420-monetary-em  # example
started: 2026-04-20T10:00:00Z
completed: false                  # bool; true only after phase 8.4 finishes
completed_at: null                # ISO 8601 timestamp, set when completed: true
completed_phases: [1, 2, 3, 4]
current_phase: 5
pause_reason: "awaiting user review of gap × data matrix"
artifacts:
  corpus: 01_corpus/corpus.json
  knowledge_map: 02_synthesis/knowledge_map.md
  knowledge_mindmap: 02_synthesis/knowledge_mindmap.json
  gap_matrix: 05_convergence/gap_data_matrix.md
  executive_summary: 08_deliverables/executive_summary.md  # Piyas 8
  podcast: 08_deliverables/podcast.mp3       # optional, if generated
  briefing: 08_deliverables/briefing.md       # optional, if generated
```

**Completion semantics.** `completed: false` is the default — set at
run-dir creation time. `completed: true` and `completed_at:
<timestamp>` are written together, only at the end of phase 8.4.
Collision handling in 1A.2 tests `completed == true` (not `completed ==
null` — old runs that crashed before v0.2.1 are treated as incomplete
and trigger the "resume / fresh / overwrite" prompt).

### corpus.json

```json
[
  {
    "citekey": "acemoglu2023",
    "authors": "Acemoglu, D.",
    "year": 2023,
    "venue": "AER",
    "doi": "10.xxxx",
    "pdf_path": "/path/to/pdf",
    "abstract": "...",
    "core_claim": "filled in phase 2",
    "methodology": "DiD"
  }
]
```

### events.jsonl

Match factory's format:
```json
{"ts":"2026-04-20T10:15:00Z","skill":"econ-ideate","run_id":"20260420-monetary-em","phase":"5","step":"scouts_returned","metric":{"data_sources":12,"gaps":8}}
```

Required fields (every event, no exceptions): `ts`, `skill`, `run_id`,
`phase`, `step`.
Optional: `metric`, `artifacts`, `notes`, `status`, `reason`.

**Append protocol (binding).** Every `events.jsonl` append in this
skill MUST use the following template. Do not write shortened events
that omit required fields.

```python
# Pseudocode — actual implementation uses Bash + jq or Write tool
event = {
    "ts": iso8601_now(),
    "skill": "econ-ideate",
    "run_id": run_id,        # from manifest
    "phase": current_phase,  # "1A", "1B", "2", ..., "8"
    "step": step_name,       # descriptive snake_case
    **extra,                 # optional fields
}
append_jsonl(run_dir / "events.jsonl", event)
```

Shortened event writes elsewhere in this spec (e.g., `{"phase":"4",
"step":"gaps_consolidated","n_gaps":N}`) are abbreviations — the actual
write MUST include all required fields.

---

## Error Handling

### lit-all returns empty
If `lit-all` returns zero papers (corpus-first Mode A):
1. Check the topic string for typos / too-narrow phrasing
2. Ask user to broaden or supply `--papers` manually
3. If Zotero has any owned papers matching, proceed with those only

### Dataset profile fails (data-first)
If the R/Python profile script errors:
1. Log the error to events.jsonl
2. Ask user for a 3-sentence manual description
3. Save to `00_input/dataset_profile.md` and continue

### Scout agent fails
If any of the four phase-5 scouts fails:
1. Proceed with the other three (never block on one scout)
2. Log the failure; mark the gap × data matrix `notes` column accordingly
3. Do not re-run automatically — user can trigger re-run manually

### Senior professor returns no PURSUE
If every idea gets PASS:
1. Do not fabricate a winner
2. Report honestly and offer three paths:
   - Broaden corpus and re-run from phase 3
   - Lower phase-6 threshold and re-run from phase 6
   - Kill the run with reason

### Required agent file missing
If `~/.claude/agents/{agent}.md` not found:
1. Report which agent is missing
2. Skip that filter stage with a warning (do not block the pipeline)
3. Log: `{"step":"agent_missing","agent":"..."}`

### papercheck fails / no PDFs for top-5 cross-check
v0.2 change: papercheck is no longer blocking. If top-5 papers lack PDFs,
papercheck simply doesn't run for them (log entries with
`papercheck_extracted: false`). NotebookLM still covers those papers via
URL/DOI ingestion in 2.1, so phase 2 continues. The verification layer
(2.6) only runs on papers where papercheck succeeded — fewer rows, not a
halt.

### NotebookLM auth expired mid-run
If any `notebooklm` call fails with auth/cookie error:
1. Halt the current phase.
2. Log the error to events.jsonl.
3. Tell user: "NotebookLM session expired. Run `notebooklm login` then
   `/econ-ideate resume {run-id}`."

### NotebookLM source upload partial failure
If some sources fail to upload in 2.1:
- Continue with the sources that succeeded.
- Flag failed ones in `corpus.json` with `notebooklm_source_id: null` and
  an error reason.
- If fewer than 5 sources succeed, halt phase 2 with an actionable
  message (see 2.1 source-count sanity).

### NotebookLM plan limit hit
If `notebooklm source add` fails with a plan-limit error during 2.1:
1. Report how many sources were uploaded successfully.
2. Ask user whether to (a) proceed with what's uploaded or (b) abort and
   narrow the corpus for a fresh run.

### NotebookLM rate-limited generation (audio/video)
Documented in notebooklm skill as a known issue (~20% failure rate).
Phase 8.3b handles this: log the failure, continue; the main report and
mind map are independent.

### NotebookLM returns empty or nonsense answer
If an `ask` call returns empty `answer` or the response seems off-topic:
1. Retry once with a slightly rephrased prompt (prepend "Based strictly
   on the uploaded sources, ").
2. If retry also fails, save both attempts to
   `02_synthesis/_failed_queries.md`, mark the relevant artifact as
   incomplete, and continue (downstream phases will work with whatever
   grounded claims we do have).

### Zotero MCP unavailable
Before calling any `zotero_*` tool, check availability:
- If user is in a project where zotero plugin is disabled
  (per `mcp-management` rule) or MCP isn't responding: skip Zotero
  steps entirely. For corpus-first Mode B, fail fast with:
  > "Zotero MCP not available in this project. Either enable
  > the zotero plugin or supply `--papers` / `--topic` instead
  > of `--from-zotero`."
- For deduplication in Mode A: proceed without Zotero dedup; log a
  note in the corpus manifest.

### Scout hits network / API error
Same handling as scout agent failure: proceed with the other three.
Additionally: if all four scouts fail (possible if offline), halt
phase 5 with:
  > "All scouts failed. Check network connectivity and API keys
  > (FRED_API_KEY, EVDS_API_KEY). Re-run `/econ-ideate resume
  > {run-id}` once resolved."

### killed_ideas.md or datasets_registry.json not found
These are factory artifacts. If absent:
- `killed_ideas.md`: skip dedup in Phase 5.4 silently — no-op.
- `datasets_registry.json`: data-gatekeeper (7.1) runs with
  `data_availability.md` alone. Log note. Do not halt.

### Context length exceeded mid-phase
If a phase's context consumption approaches model limits:
1. Log the warning
2. Summarize the current in-memory content to a checkpoint file
   in the phase directory (e.g., `02_synthesis/_checkpoint.md`)
3. Halt with a message suggesting the user re-run the phase on a
   smaller corpus subset or with `--depth quick`

### User-killed mid-flight
If the user interrupts (no explicit mechanism provided by Claude
Code; detectable only on next session via stale manifest):
- `/econ-ideate status` shows stale runs (no `events.jsonl` entry
  in past 24h and `completed: null`) as `interrupted`.
- `/econ-ideate resume` handles these like any paused run.
- User can also delete the run directory to fully discard.

### Senior professor model override conflict
Phase 7.3 specifies `model: "opus"` on the Agent tool call. If the
`senior-professor.md` agent file has its own model spec, the Agent
tool parameter takes precedence. This is intentional — deep judgment
phase should run at opus regardless of the agent-file default.

---

## Integration Notes

**Calls:**
- `Skill` tool → `lit-all` (corpus assembly), `papercheck` (top-5 deep
  read / cross-check in 2.2), `fact-collect` (institutional fact capture,
  phase 8)
- `Bash` tool → `notebooklm` CLI (phases 2, 3, 4, 8):
  `auth check`, `create`, `source add`, `source list`, `source wait`,
  `ask`, `generate mind-map`, `generate audio`, `generate report`,
  `download {mind-map|audio|report}`, `artifact wait`
- `Agent` tool, named agents (harness auto-loads `<name>.md`; no
  injection — see Invocation Contracts):
  `data-scout`, `world-watcher`, `mind-scanner`, `project-scanner`,
  `data-gatekeeper`, `research-assistant`, `senior-professor` (+ `model:
  "opus"` override)
- `Agent` tool, `subagent_type: "general-purpose"` (no configured `.md`):
  (a) Sonnet workers for per-cell ideation in phase 6, (b) background
  waiters for long-running notebooklm tasks (source processing, audio
  generation)
- MCP → `zotero_*` tools for corpus assembly (`zotero_get_collections`,
  `zotero_get_collection_items`, `zotero_semantic_search`,
  `zotero_find_and_attach_pdfs`)
- Model routing → Sonnet for phase 6 (per-cell ideation, 3+ calls), Opus
  for phase 7 senior-professor

**Related skills (NOT called automatically — offered to user as next-step
actions in phase 8.4):**
- `interview-me` — formalize top idea into full research spec
- `research-ideation` — alternative hypothesis-generation per idea
- `/factory feasibility` — run the top idea through data cleaning +
  power calc + naive estimation
- `fact-collect` — offered if institutional facts are surfaced

**Called by (future integrations):**
- `/factory discover` could delegate its synthesis layer to
  `/econ-ideate corpus` and then feed the gap list directly to the
  factory scouts (replacing blind scouting with targeted briefing).
  Out of v1 scope — noted here for later.

**Depends on:**
- Sub-agent definitions in `~/.claude/agents/`
- `~/projects/.research-factory/killed_ideas.md` (optional — for dedup)
- `~/projects/.research-factory/datasets_registry.json` (optional — for
  gatekeeper context)

---

## Defaults Summary

| Setting | Default | Override |
|---------|---------|----------|
| Output dir | `~/projects/.econ-ideate/runs/<run-id>/` | `--output-dir` |
| Depth | standard | `--depth quick/deep` |
| Pause at phase 5 | yes | `--auto` |
| Synthesis engine (phases 2–4) | NotebookLM (grounded Q&A) | (v2 fixed) |
| Top-5 cross-check (2.2) | papercheck on PDFs; skip if missing | (non-blocking) |
| Mind map (2.5) | always generated (NotebookLM sync) | (v2 fixed) |
| Audio/briefing (8.3b) | user prompt; skip on `--auto` | user answer |
| Phase 6 model | sonnet | (hardcoded — change in skill if needed) |
| Phase 7 scoring | senior-professor (opus) | (v1 fixed; `/council` planned) |
| Scouts at phase 5 | all 4, always parallel | (v1 fixed) |
| Killed-idea dedup | yes | (v1 fixed; warn-not-drop) |
| Corpus cap | ~200 soft / plan-limit hard | narrow via `--topic`/Zotero/`--papers` |
