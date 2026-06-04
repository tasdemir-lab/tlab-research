# econ-ideate — Known Gaps (v0.2.2)

Items that are designed but not verified end-to-end. Each is expected to
surface on the first real run and will need adjustment. Not blockers for a
dry-run — just things to watch.

**2026-04-21 update.** A spec review (Claude Opus + Codex) surfaced 13
contract/schema drift issues beyond the original 10 gaps below. Nine P0
fixes landed in v0.2.1 (see SKILL.md status banner). This file now
tracks (a) the original 10 gaps, many still unverified, and (b) a new
P1/P2 follow-up section at the bottom.

---

## v0.2 (NotebookLM refactor) — new gaps

### G1. NotebookLM `ask --json` citation format unverified
- **Assumption:** `ask --json` returns `{answer, references: [{source_id,
  citation_number, cited_text, start_char, end_char}]}` as documented in
  the notebooklm SKILL.md.
- **Unverified:** haven't parsed a real response. Field names or structure
  may differ slightly between CLI versions.
- **Action on dry-run:** capture one raw `ask --json` output early, adjust
  the parsing logic in 2.3 / 3.1 / 4.1 accordingly.

### G2. Top-5 ranking heuristic unchanged from v0.1
- In Phase 2.2, top-5 papers are ranked by: Zotero annotations → citation
  count → venue prestige → recency. NotebookLM isn't consulted for this
  ranking, even though it could be (e.g., ask NotebookLM which papers it
  considers most central).
- Not a bug; a design simplification. Worth revisiting if v0.2 surfaces
  cases where the cross-check in 2.6 repeatedly flags the "wrong" papers
  as central.

### G3. Cross-check verification (2.6) is minimum-viable
- Only checks core_claim + methodology agreement between NotebookLM and
  papercheck on the 5 top papers.
- Doesn't check: consistency across downstream artifacts, internal
  contradictions in NotebookLM's own answers across phases, numerical
  drift in specific claims.
- A more aggressive verifier would re-ask NotebookLM the same question
  with rephrasing to test answer stability. Left for v0.3.

### G4. NotebookLM-specific defaults not tuned by real use
- `--mode deep` vs `--mode fast` decision for any `add-research` call
  isn't pinned in the skill — none used in v0.2 protocol, but if added
  later, defaults aren't based on empirical observation.
- Source polling interval (2.1 wait) is "until ready" with 20-min cap;
  actual indexing times vary 30s–10min per source — 20min cap may be
  too tight for large corpora.

### G5. NotebookLM source-limit enforcement is reactive, not proactive
- The skill doesn't pre-check the user's plan tier before uploading.
  Upload proceeds until the CLI rejects — then 2.1's error path kicks in.
- Proactive check would require `notebooklm` to expose plan-tier info,
  which isn't in the documented command surface.
- Minor UX issue: user may waste time on partial uploads before hitting
  the wall.

---

## v0.1 carryovers — still unverified

### G6. Skill tool invocation pattern for `lit-all`, `papercheck`
- Phases 1A.4, 1B.1 Mode A, 2.2 invoke these via the `Skill` tool.
- Unverified: whether `Skill` tool honors the expected argument structure
  for each, and whether results come back in a parseable format.
- Fallback if it doesn't work: run the skills interactively via
  slash-commands, which breaks the single-invocation flow of econ-ideate.

### G7. Agent tool `subagent_type: general-purpose` + definition injection
- Phase 5.1 (scouts) and Phase 7 (gatekeeper / research-assistant /
  senior-professor) use the pattern documented in the `factory` skill:
  read agent .md file, inject full content into the prompt, launch with
  `subagent_type: general-purpose`.
- Works in `factory` (factory is battle-tested). Worth verifying the
  pattern transfers cleanly here — particularly for the senior-professor
  opus override.

### G8. Dataset profile script in 1A.3
- The skill says "write a profile.R or profile.py script that extracts
  [N rows, N cols, panel structure, …]" — but doesn't include a template.
- On dry-run for data-first, Claude will write this fresh each time.
  Output quality depends on how well Claude chooses libraries (haven/
  readr for R; pandas for Python) and heuristics.
- A reusable template saved as `econ-ideate/templates/profile.{R,py}`
  would make this deterministic. Deferred to v0.3.

### G9. `killed_ideas.md` format assumption
- Phase 5.4 dedup reads `~/projects/.research-factory/killed_ideas.md`
  and expects entries with `KI-NNN` IDs and `keywords:` field.
- Factory's actual file format may differ. If parsing fails, the skill
  falls through to "no dedup" (log note, continue) per error handling —
  so not catastrophic, but dedup won't fire.

### G10. Resume with user-edited matrix (9.4) — tolerance untested
- 9.4 specifies parse tolerance: accept any table with header columns
  matching `Gap` + `Source` + `Feasibility` (case-insensitive).
- **v0.2.1 update:** canonical matrix format is now long-form with a
  stable 5-column header (5.3). The parser contract (9.4) keys on that
  header. Reduces ambiguity — the 9.4 parser now tracks a concrete
  write contract, not a permissive description. Risk narrowed to:
  user pastes an unrelated table above the real one, or uses a
  different table style (e.g., Pandoc grid) that ripgrep/regex-based
  header match misses.
- Still untested against realistic user edits.

---

## v0.2.1 P1 / P2 follow-ups

Not in v0.2.1 (were P0-only). Carry forward.

### F1. Corpus-size warning ≠ NotebookLM plan cap (M1 / G5-extension)
- 1B.2 warns at `>200 papers`; NotebookLM plan limits are
  50/100/300/600 (Standard/Plus/Pro/Ultra). Standard-tier users hit
  the wall at 50 with no prior warning.
- Fix plan: ask plan tier up front, compare before upload.

### F2. Phase 6 top-20 tie-break lacks diversity (M2)
- Current rule: "feasibility, then gap ID". Could send all 20 ideations
  to the same gap.
- Fix plan: cap at 4 cells per gap, then feasibility, then gap ID.

### F3. Phase 7 filter chain output contracts (Codex #10)
- Gatekeeper + research-assistant are instructed semantically; no
  structured output template. Only senior-professor has a table
  contract.
- Fix plan: add `| idea_id | verdict | reason |` template for
  gatekeeper, `| idea_id | score | rank | rationale |` for RA, plus
  prose-fallback parser.

### F4. corpus.json data-model drift (Codex #12)
- Schema + 1B.3 imply `core_claim`/`methodology` get filled in Phase 2;
  only top-5 get `papercheck_extracted`.
- Fix plan: either add a 2.3b NotebookLM pass that fills these for the
  full corpus, or drop the fields from schema.

### F5. `datastor:` / `api:` input classes unsupported (Codex #6)
- 1A.1 accepts them; 1A.3 assumes a local file.
- Fix plan: either implement a fetch-and-profile protocol, or drop
  acceptance from 1A.1 until supported.

### F6. Phase 8.2 RDR creation is premature (M3)
- Writes an RDR for the top idea before the user has committed to
  pursuing it.
- Fix plan: gate RDR creation on explicit y/N confirmation in 8.4.

### F7. No budget guardrail (M4)
- Phase 6 can fan out 20 Sonnet calls + 1 Opus + many NotebookLM asks
  with no pre-run estimate.
- Fix plan: print a token/cost estimate at the 5.5 pause.

### F8. Piyas prompt catalog not sourced (M7)
- 9 Piyas prompts are quoted verbatim in SKILL.md. If the user's Piyas
  prompt library evolves, the skill drifts silently.
- Fix plan: extract to `econ-ideate/piyas-prompts.md` and include by
  reference.

### F9. Profile script template (G8 carryover — still unresolved)
- Dataset profiling in 1A.3 has no template. Claude writes fresh each
  time → nondeterminism on first run.
- Fix plan: `templates/profile.R` and `templates/profile.py`.

### F10. Phase 5 matrix dimension cap (M — matrix normalization)
- v0.2.1 already drops feasibility-0 rows and dedupes sources. Still
  lacks an explicit per-gap cap on sources or a total-row cap.
- Fix plan: cap N rows per gap to max(5, top-feasibility), warn user
  if total rows > 60.

---

## How to use this file

On the first real dry-run, keep this file open. When one of these gaps
surfaces:
1. Note the specific observed behavior next to the gap ID in a `-
   **Observed {date}:** ...` line.
2. Patch the SKILL.md and note the fix.
3. Once a gap has been observed-and-fixed, move it to a `## Resolved`
   section at the bottom with the date.

Gaps that don't surface in several real runs can be downgraded or
removed.

---

## Resolved

### R7. NotebookLM CLI contract drift — 6 observations from 2026-04-21 ERPT run (end-to-end Phases 1B–5) — **FIXED in v0.2.3**

This entry batches the drift captured in the first Phase-2-through-Phase-5 end-to-end run (topic: "exchange rate pass-through to inflation in Türkiye", 8 URLs submitted, 6 indexed). **All six patched in v0.2.3 (2026-04-21).** Summary of fixes: see SKILL.md status banner.

**R7.1 — `notebooklm ask --json --save-as-note` emits mixed output.** The CLI prints the JSON object and then appends a plain-text footer `Saved as note: <Title> (<id>...)` on a separate line after the closing `}`. Strict `json.loads(whole_file)` fails. All seven `ask --json --save-as-note` invocations across Phases 2–4 (Piyas 3/6/7/1/9/2/5) hit this. Workaround used: `raw[:raw.rfind('}')+1]` before parsing. **Fix plan:** §2.3/§2.4/§2.5/§3.1/§3.2/§4.1/§4.2 all need "parse by trimming the footer" tolerance in their parsing step, OR drop `--save-as-note` entirely and call it separately via a `notebooklm note add` step (if it exists — verify). This is the highest-value R7 fix because it affects every Piyas-prompt phase.

**R7.2 — `source add <url>` is not atomic: partial state persists on error.** Uploaded 8 URLs. Two (Wiley, OUP paywalls) returned `{"error": true, ...}` from `source add` with no `id` field — but `source list --json` later showed BOTH as full source records with `status: error`. §2.1 currently relies on the add-step response to decide whether a source was added. **Fix plan:** §2.1 after each add should check `source list --json` for authoritative state. When cleaning up errored sources, delete explicitly; don't assume "add failed → no cleanup needed."

**R7.3 — `status: ready` does NOT guarantee usable content.** One of the 6 indexed URLs (Tandfonline DOI page for Pierros et al. 2024) indexed as `status: ready` but NotebookLM's Piyas-3 response explicitly noted the source contained "only website boilerplate text without a title, author, or content" and excluded it from the landscape. **Fix plan:** §2.1's source-count sanity check (`< 5 sources: halt`) currently uses the `ready` count. Add a follow-up probe — ask NotebookLM `"For each source, give one sentence of content. Reply 'EMPTY' for any source that contains only boilerplate"`, then subtract the empty ones from usable count.

**R7.4 — Indexing is ~100× faster on web pages than §2.1's PDF-calibrated estimates.** All 6 indexable sources (1 PDF + 5 WEB_PAGE) reached `ready` within 32 seconds total — the 20-min poller max is PDF-calibrated. Non-blocking but the §2.1 background-agent polling pattern is overkill for URL-heavy corpora. **Fix plan:** §2.1 should use `notebooklm source wait <id> --timeout N --json` (native CLI command discovered in preflight). For URL-only corpora, this is a single-threaded pass; for PDF-heavy corpora, dispatch in parallel. No change to the ordering barrier.

**R7.5 — Zotero semantic search failure rate higher on topics outside user's curation.** 16/20 semantic-search results returned "Could not fetch full item data: Code: 404" on ERPT topic (vs 5/15 on MW topic — R3). The 4 valid items were all off-topic (demographic inflation, wage inequality, Syrian refugees). Signal: when the user's Zotero library has sparse coverage of a topic, semantic search degenerates fast. §1B.1 Mode A should detect this — if >50% of results are `Error:` AND semantic similarity of valid items is <0.2, fall through to WebSearch earlier rather than treating Zotero as primary.

**R7.6 — §5.4 Jaccard dedup misses when scouts self-annotate KI references.** Project-scanner explicitly cited KI-005, KI-019, KI-023, KI-026 in its cell notes (as revival candidates). The Jaccard-0.5 threshold (and even 0.3) found zero overlaps because the scout's source_id contained the literal path `killed_ideas.md#KI-NNN`, which diluted topical tokens with shared "killed ideas" boilerplate. **Fix plan:** §5.4 should first do a direct-ID pass: `re.findall(r'KI-\d+', source_id + note)` → flag those rows unconditionally with `[killed: KI-NNN, explicit]` BEFORE Jaccard. Then Jaccard catches the non-self-annotated cases.

**Other observations from the same run (not contract drift — carry forward as watch items):**
- §1B.2 slug generation worked cleanly on topic string ("exchange rate pass-through to inflation in Türkiye" → `exchange-rate-pass-through-inflation-turkiye`, 46 chars, passes `[a-z0-9-]{0,60}`).
- §2.2 silent-skip on missing PDFs worked (web-URL corpus had no PDFs; papercheck was never invoked; §2.6 cross-check followed).
- Mind map generated in Turkish because one source (TCMB blog) is in Turkish — no bug, but downstream consumers of `knowledge_mindmap.json` should not assume a language.
- All three Piyas-2/3 calls shared one `conversation_id` — §2.0 needs to document whether this is desired (context carry-over) or undesired (cross-contamination). See R5.

**§7 validation status.** This run stops at §5.5 pause per user directive. §7.1–§7.3 use the same Agent-tool pattern as §5.1, which WAS exercised — 4 scouts via direct `subagent_type=<name>` all ran successfully. §7 is therefore **pattern-inherited green**, not directly-fired green. First direct §7 exercise waits for a run that pushes past the Phase 5 pause.

---

### R6. Agent `.md` injection is unnecessary — `subagent_type: "<name>"` works directly (G7 observation, 2026-04-21)
- **Observed:** fired `Agent(subagent_type="project-scanner", prompt=<task only, no .md injection>)` on a 3-gap toy list. The agent:
  - Accepted the direct subagent_type by name (no "general-purpose" wrapper needed)
  - Ran per its configured system prompt (made ~16 tool calls, 77s, ~43k tokens)
  - Followed its native output conventions AND emitted the "## econ-ideate cells" section as requested
  - Surfaced real, relevant in-hand data from `~/projects/mw-passthrough/`
  - Cross-signaled other scouts (`@data-scout: ...`, `@literature-explorer: ...`)
- **Spec status:** §5.1's invocation pattern is **substantially wrong**. Current spec says:
  > `subagent_type: "general-purpose"` (Agent tool does not auto-load `.md` agent definitions by name — inject them into the prompt)
- That claim is false on this Claude Code harness. The Agent tool auto-loads `~/.claude/agents/<name>.md` as the subagent's system prompt when `subagent_type: "<name>"`. Injecting the .md is redundant and bloats each scout call by several KB.
- **Spec edits recommended (high priority):**
  1. §5.1 rewrite: drop Step 1 (reading .md files) and Step 2's "inject .md content" instruction. Replace with single-step dispatch: `Agent(subagent_type="data-scout", prompt=<task-only prompt>)` × 4 in one message.
  2. §7.1/§7.2/§7.3 same fix — drop the "Read ... .md and launch with full agent definition" prefix from each.
  3. §7.3 still needs `model: "opus"` override — that's a separate parameter and still works.
- **Side benefit surfaced:** project-scanner's real output identified `~/projects/mw-passthrough/` as carrying directly-applicable HIA worker panel + MW series + DiD/IV/stacked code for the MW topic. If the user continues this run past Phase 5, Phase 6 ideation and Phase 7 gatekeeper will have very strong "in-hand" feasibility signals for G1 and G2.
- **Status:** high-value simplification. Apply before next run.

### R4. NotebookLM `ask --json` schema verified + bonus fields (G1 observation, 2026-04-21)
- **Observed:** ran `notebooklm ask "..." --json -n <existing>` against the user's "Finansal Okuryazarlık" notebook on CLI 0.3.4. Response shape:
  - Top-level: `{"answer": str, "conversation_id": str, "turn_number": int, "is_follow_up": bool, "references": [...]}`
  - Per-reference: `{"source_id", "citation_number", "cited_text", "start_char", "end_char", "chunk_id"}`
- **Spec status:** §2.3 assumption `{answer, references: [{source_id, citation_number, cited_text, start_char, end_char}]}` is **correct** for the 5 core fields. Real response adds 3 top-level bonus fields and 1 per-reference bonus (`chunk_id`).
- **Spec edits recommended (not blockers):**
  1. §2.3 parsing logic should preserve `chunk_id` per reference — more stable than `start_char/end_char` for deduplication across paraphrased queries.
  2. §2.6 cross-check could use `conversation_id` to issue follow-up questions (e.g., "Clarify on that last paper") without starting a new conversation.
  3. **Citation marker format is NOT single `[N]`.** NotebookLM emits `[1, 2]` (comma-separated list) AND `[3-5]` (inclusive range) in addition to `[N]`. §2.7's "citation markers `[N]`" description is too narrow — any downstream parser of Phase 2-4 artifacts must handle all three forms.
- **Status:** spec is *functionally correct* on field names; §2.3/§2.6/§2.7 wording could be expanded but no contract fix is blocking.

### R5. CLI help text mentions `--new` flag that doesn't exist (2026-04-21)
- **Observed:** `notebooklm ask --help` docstring shows "Use `--new` to start fresh," but passing `--new` errors with "No such option: --new". Upstream notebooklm-py bug.
- **Impact on econ-ideate:** none directly. §2.3/2.4/2.5/3.1/3.2/4.1/4.2 don't use `--new`. But §2.6 cross-check could benefit from a fresh conversation per paper — without `--new`, it implicitly continues the last conversation (which is why §2.3 and §2.6 on sequential calls may inherit prior context). Workaround: rely on `conversation_id` + explicit conversation management, or just accept the follow-up mode.
- **Status:** upstream CLI bug. File issue with notebooklm-py; meanwhile document workaround in SKILL.md §2.6.

### R2. Skill-tool `lit-all` invocation returns a sub-skill load, not a result (G6 observation, 2026-04-21)
- **Observed:** calling `Skill(skill="lit-all", args="...")` from econ-ideate does not return a bibliography. It loads lit-all's SKILL.md into the parent conversation and hands execution back to the parent — the parent must then drive lit-all's 5 steps (Zotero scan, MCP preflight, launch agents, dedup, write files).
- **Impact on econ-ideate spec:** §1A.4 and §1B.1 say "Invoke lit-all via Skill tool ... save the returned bibliography to 01_corpus/bibliography.bib." That phrasing implies a function-call return value. The real contract is "the parent executes lit-all inline and reads the files lit-all writes to `_lit/`, `lit/`, or `literature/`."
- **Fix plan (not yet applied):** rewrite §1A.4/§1B.1 as a two-step:
  1. Invoke `Skill(skill="lit-all", args="<topic> --depth <depth>")`.
  2. After lit-all completes, glob `_lit/lit-all-results-*.md` and the matching `.bib` file (newest mtime), then copy/symlink into `01_corpus/bibliography.bib` and parse the `.md` tables into `corpus.json`.
- **Same issue applies universally to the Skill tool.** The Skill tool's documented behavior is always "execute a skill within the main conversation" — it loads the target skill's SKILL.md as instructions; there is no structured-return mode. This means §2.2 `papercheck` invocation has the same contract as §1B.1 lit-all: the parent executes papercheck inline, then reads whatever papercheck writes (typically a cached evidence pack in `.papercheck-cache/` or similar).
- **Status:** observed, pattern generalized across Skill tool. §1B.1 **and §2.2** both need spec rewrites — "invoke via Skill tool, then glob for the output files it writes" is the universal pattern. Did not fire papercheck to confirm separately because the Skill-tool contract is universal; a separate invocation would have only re-confirmed what is already known.

### R3. Zotero semantic search returns 404 for some items (2026-04-21)
- **Observed:** 5 of 15 returned items gave "Could not fetch full item data: Code: 404" from `localhost:23119/api/users/1792119/items/<key>`. Items appear in the similarity ranking but full metadata is unfetchable — possibly stale embedding index or deleted items.
- **Impact:** non-blocking. The 10 valid items are sufficient. Any parser of semantic-search output must tolerate error rows.
- **Fix plan:** add a sentence to §1B.1 Mode A noting the skill should filter out items with `"Error:"` in the semantic-search response and log them to `events.jsonl`.
- **Status:** observed, logged. Low priority.

### R1. Auth preflight check under-specified (observed 2026-04-21, pre-run)
- **Observed:** `notebooklm auth check --json` (v0.3.4) returns
  `{"status": "ok", "checks": {"cookies_present": true, "sid_cookie":
  true, "token_fetch": null}, ...}` on a functional session. The v0.2.1
  spec halted only if `token_fetch: false` — so `null` (a common
  fresh-check value) would slip past the check AND a broken-auth
  `status != "ok"` case wasn't captured.
- **Fix applied in SKILL.md §2.0:** halt on `status != "ok"`, non-zero
  exit, or `cookies_present/sid_cookie == false`. Explicitly do **not**
  halt on `token_fetch == null` — a real auth failure surfaces on the
  first `ask`/`source add` call, which the mid-run error handler covers.
- **Status:** resolved pre-run. Re-verify on first real run that no
  false-positive halt occurs.
