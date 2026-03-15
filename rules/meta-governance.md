# Meta-Governance: Three-Layer Architecture

**Research projects using this plugin operate with three distinct layers.**

Understanding this distinction is critical for deciding what to commit, what to document, and where to save learnings.

---

## The Three Layers

### Layer 1: Template Repo (`research-template-bare`)
- Provides folder structure: `code/`, `data/`, `paper/`, `output/`, `assets/`
- Contains `CLAUDE.md` skeleton with placeholders
- Contains `.claude/settings.json` (marketplace pointer + permissions)
- Contains `.gitignore`, `setup_project.sh`, helper R files
- **Rarely changes** — scaffolding is stable

### Layer 2: Plugin (`tlab`)
- Provides agentic components: skills, agents, rules, hooks
- Skills invoked with `/tlab:` prefix (e.g., `/tlab:commit`, `/tlab:proofread`)
- Rules synced to project `.claude/rules/_plugin_*.md` via SessionStart hook
- Hooks enforce protections (file protection, rule sync)
- **Updated via `claude plugin update`** — independent of template changes

### Layer 3: User-Level (`~/.claude/`)
- Personal skills, rules, agents, hooks
- Machine-specific preferences
- Auto-memory (per-machine, not synced via git)
- **Not shared** — each user's personal toolkit

---

## Decision Framework

When creating or modifying content, ask:

### "Which layer does this belong to?"

**Template (Layer 1):**
- Folder structure changes
- CLAUDE.md skeleton updates
- .gitignore pattern changes
- Helper function templates

**Plugin (Layer 2):**
- New or updated skills
- Rule changes
- Agent improvements
- Hook behavior changes

**User-Level (Layer 3):**
- Personal preferences
- Machine-specific setup
- Per-project overrides

---

## Memory Management

### MEMORY.md (project root, committed)

**Purpose:** Generic learnings that help ALL users of this template

**What goes here:**
- Workflow improvements: `[LEARN:workflow] RDS-first pattern reduces render times`
- Design principles: `[LEARN:design] Numbered scripts enforce pipeline order`
- Documentation patterns: `[LEARN:documentation] Update CLAUDE.md + README together`
- Quality standards: `[LEARN:quality] 80/90/95 thresholds work across projects`

**Size limit:** Keep under 200 lines (stays in Claude's system prompt)

### Auto-Memory (built-in, per-machine)

Claude Code's built-in auto-memory handles machine-specific and project-instance learnings. Not synced via git.

---

## Content Distribution

| Content Type | Where It Lives | Syncs Via |
|--------------|---------------|-----------|
| Folder structure | Template repo | git clone / template |
| CLAUDE.md skeleton | Template repo | git clone / template |
| Skills (7) | tlab plugin | `claude plugin update` |
| Agents (2) | tlab plugin | `claude plugin update` |
| Rules (5) | tlab plugin → synced to `.claude/rules/_plugin_*` | SessionStart hook |
| Hooks (2) | tlab plugin | `claude plugin update` |
| Personal skills | `~/.claude/skills/` | Not synced |
| Personal rules | `~/.claude/rules/` | Not synced |
| Machine settings | Auto-memory | Not synced |
| Generic learnings | MEMORY.md | git |
| Session progress | `_lab/progress.md` | git |
| Plans | `_lab/plans/` | git |
| Evaluations | `_lab/evaluations/` | git |
| Local settings | `.claude/settings.local.json` | Not synced (gitignored) |

---

## Update Flow

### Updating Agentic Components (Plugin)
```bash
claude plugin update tlab@tlab-research
# Next session: sync-rules hook copies updated rules
```

### Updating Template Scaffolding
Rarely needed. If scaffolding changes, manually pull or recreate from template.

---

## Dogfooding: Following Our Own Workflow

**We must follow the patterns we recommend to users.**

### Plan-First Workflow
- Do: Enter plan mode for non-trivial tasks (>3 files, multi-step)
- Do: Save plans to `_lab/plans/YYYY-MM-DD_description.md`
- Don't: Skip planning for "quick fixes" that turn into multi-hour tasks

### Quality Gates
- Do: Run quality scoring before commits
- Do: Nothing ships below 80/100
- Don't: Commit "WIP" code without quality verification

### Documentation Standards
- Do: Update CLAUDE.md when adding features or changing workflow
- Do: Keep dates current in progress log
- Don't: Let documentation drift from implementation

---

## Template Maintenance Principles

### Keep It Generic

**Bad (too specific):**
```markdown
# Analysis Rule
Always cluster standard errors at the county level using fixest.
```

**Good (framework-oriented):**
```markdown
# Analysis Rule
Cluster standard errors at the appropriate level. Document the choice in code comments.
Configure default clustering in CLAUDE.md for your project.
```

### Use Templates Not Prescriptions

**Bad (prescriptive):**
```markdown
Your bibliography MUST be named master.bib and live at the repo root.
```

**Good (template with placeholders):**
```markdown
Configure bibliography location in CLAUDE.md:
[YOUR_BIB_FILE] (e.g., master.bib at root, bibliography.bib, refs/main.bib)
```

---

## Amendment Process

**When to amend this file:**
- We discover better ways to distinguish the three layers
- Plugin system evolves (e.g., native rule loading support)
- User feedback reveals confusion

**Amendment protocol:**
1. Propose change in session log or plan
2. Discuss implications
3. Update this file in the plugin repo
4. Update via `claude plugin update`
