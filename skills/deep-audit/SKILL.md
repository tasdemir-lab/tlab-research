---
name: deep-audit
description: |
  Deep consistency audit of the entire research repository.
  Launches 4 parallel specialist agents to find stale references, broken paths,
  skill/rule mismatches, and cross-document inconsistencies. Then fixes all issues
  and loops until clean.
  Use when: after broad changes, before releases, or when user says
  "audit", "find inconsistencies", "check everything".
author: tlab-research plugin
version: 1.0.0
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Agent"]
---

# /tlab:deep-audit — Research Repository Consistency Audit

Run a comprehensive consistency audit across the entire repository, fix all issues found, and loop until clean.

## When to Use

- After broad changes (new skills, rules, pipeline restructuring)
- Before releases or major commits
- When the user asks to "find inconsistencies", "audit", or "check everything"

## Plugin-Aware Context

This skill runs in projects using the `tlab` plugin. Key locations:
- **Skills** live in the plugin (not `.claude/skills/`). CLAUDE.md lists them as `/tlab:*`.
- **Agents** live in the plugin (not `.claude/agents/`).
- **Rules** are synced from the plugin to `.claude/rules/_plugin_*.md` via the SessionStart hook.
- **Hooks** are defined in the plugin's `hooks/hooks.json`.
- **Settings** remain in `.claude/settings.json` in the project.

## Workflow

### PHASE 1: Launch 4 Parallel Audit Agents

Launch these 4 agents simultaneously using `Agent` with `subagent_type=general-purpose`:

#### Agent 1: CLAUDE.md & README Accuracy
Focus: `CLAUDE.md`, `README.md`
- Skills table in CLAUDE.md lists `/tlab:*` commands that match available plugin skills
- Folder structure described in README matches actual directories on disk
- Commands listed in CLAUDE.md and README are accurate and runnable
- All file paths mentioned actually exist
- No stale counts or references to removed features
- Quality thresholds table is consistent between both files
- Bibliography location is consistent across all mentions
- Plugin installation instructions are present and accurate

#### Agent 2: Infrastructure Code Quality
Focus: `.claude/settings.json`, `.claude/rules/_plugin_*.md`
- No hardcoded absolute paths in any infrastructure files
- `settings.json` is valid JSON with sensible permissions
- `settings.json` contains `extraKnownMarketplaces` pointing to `tasdemir-lab/tlab-research`
- Synced rules (`.claude/rules/_plugin_*.md`) have valid content (not corrupted copies)
- No stale references to removed skills, agents, or rules

#### Agent 3: Plugin Rules Consistency
Focus: `.claude/rules/_plugin_*.md` (synced from plugin)
- Valid YAML frontmatter in all rule files
- Rule `paths:` and file references point to existing directories
- No contradictions between rules (e.g., conflicting quality thresholds)
- All templates or files referenced in rules actually exist
- No hardcoded paths from another project

#### Agent 4: Cross-Document & Pipeline Consistency
Focus: `README.md`, `CLAUDE.md`, `code/`, `paper/`, `.gitignore`
- README folder structure tree matches actual directory layout
- `.gitignore` covers all private directories mentioned in README (`_lab/`, `_lit/`, `_trash/`, `tmp/`)
- `.gitignore` ignores render artifacts as described (`.html`, `.md` in `code/`)
- `.gitignore` ignores plugin-synced rules (`_plugin_*`)
- Data pipeline stages described in README match actual script names in `code/`
- `code/helpers/_load_all.R` (if it exists) sources all helper files that exist
- Bibliography file referenced in `CLAUDE.md` exists at the stated location
- `paper/preamble.tex` (if referenced) exists
- Render convention described matches `code/_quarto.yml` settings (if exists)
- `setup_project.sh` (if exists) creates the directories described in README

### PHASE 2: Triage Findings

Categorize each finding:
- **Genuine bug**: Fix immediately
- **False alarm**: Discard (document WHY it's false for future rounds)

Common false alarms to watch for:
- Placeholder text in `[BRACKETS]` — this is intentional in the template
- Empty `_lab/` directories — expected in a fresh project
- Missing `renv.lock` or `uv.lock` — created on first use, not part of template
- Missing data files in `data/raw/` — data is gitignored by design
- Missing `code/*.qmd` scripts — template provides structure, not content
- Missing `.claude/rules/_plugin_*.md` files — created on first session by plugin hook

### PHASE 3: Fix All Issues

Apply fixes in parallel where possible. For each fix:
1. Read the file first (required by Edit tool)
2. Apply the fix
3. Verify the fix (grep for stale values, check syntax)

### PHASE 4: Loop or Declare Clean

After fixing, launch a fresh set of 4 agents to verify.
- If new issues found -> fix and loop again
- If zero genuine issues -> declare clean and report summary

**Max loops: 5** (to prevent infinite cycling)

Save the final audit report to `_lab/evaluations/YYYY-MM-DD_deep-audit.md`.

## Common Bug Patterns to Watch For

| Bug Pattern | Where to Check | What Went Wrong |
|-------------|---------------|-----------------|
| Stale skills table | CLAUDE.md vs plugin skills | Added/removed plugin skill but didn't update CLAUDE.md |
| Wrong bibliography path | CLAUDE.md, README, `code/_quarto.yml` | Changed location but didn't update all references |
| Missing .gitignore entries | `.gitignore` vs README | Documented folder as "gitignored" but didn't add pattern |
| Broken helper loading | `code/helpers/_load_all.R` | Added helper file but didn't add `source()` call |
| Hardcoded paths | rules, settings | Used `/Users/...` instead of relative path |
| README tree drift | README.md vs `find . -type d` | Restructured folders but didn't update README tree |
| Rule contradictions | Between `_plugin_*.md` rule files | Two rules prescribe conflicting quality thresholds |
| settings.json drift | `.claude/settings.json` | Marketplace pointer or permissions changed |
| Missing plugin marker | CLAUDE.md | Missing "tlab" keyword prevents rule sync |

## Output Format

After each round, report:

```
## Round N Audit Results

### Issues Found: X genuine, Y false alarms

| # | Severity | File | Issue | Status |
|---|----------|------|-------|--------|
| 1 | Critical | CLAUDE.md:82 | Skill table lists /tlab:foo but plugin has no such skill | Fixed |
| 2 | Medium | .gitignore:15 | Missing pattern for _plugin_* | Fixed |

### Verification
- [ ] Skills table matches plugin skills
- [ ] All paths in README exist on disk
- [ ] .gitignore covers all private directories
- [ ] No hardcoded absolute paths in infrastructure
- [ ] Rules don't contradict each other
- [ ] Plugin marketplace pointer is correct

### Result: [CLEAN | N issues remaining]
```
