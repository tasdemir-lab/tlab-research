---
name: lit-check
description: Check literature across three dimensions (methods, application context, reference papers) for a research concern. Integrates with papercheck for evidence extraction and stores findings in the detected lab directory's insights/.
author: Murat Taşdemir
version: 1.2.0
tags:
  - research
  - literature-review
  - economics
  - causal-inference
  - cross-referencing
---

# Literature Dimension Check

## Purpose

When a research question requires literature grounding, systematically check across three dimensions:

1. **Methods Literature** - What do methodologists say about this technique?
2. **Application Context** - What's known about this empirical setting?
3. **Reference Papers** - How did similar papers handle this?

This skill runs in main conversation context, meaning:
- Can see full conversation history
- Can cross-reference findings immediately
- Persists via lab directory (not isolated like subagents)

## Prerequisites

Requires the lab directory's `insights/` structure with dimension folders. Run `/setup-memory` first if missing.

## How to Invoke

Ask Claude a literature-grounded question:
- "How do papers handle pre-trends in staggered DiD?"
- "What's the standard for weak instrument testing?"
- "How does [Paper X] address selection bias?"

Or explicitly: `/lit-check concern:"instrument validity" dimension:methods`

---

## Workflow

### Step 0: Detect Lab Directory

Before any file operations, detect which lab directory convention the project uses:

1. Check if `lab_notes/` exists → use it
2. Check if `_lab/` exists → use it
3. If neither exists → tell the user to run `/setup-memory` first and stop

Set `LAB_DIR` to the detected value and use it for all subsequent paths.

### Step 1: Classify the Concern

Ask: Which dimension(s) does this concern touch?

| Concern Type | Primary Dimension | Cross-refs To |
|--------------|-------------------|---------------|
| "Is my instrument valid?" | Methods | Application Context |
| "What controls should I include?" | Reference Papers | Methods |
| "How does regulation X work?" | Application Context | Reference Papers |
| "What's the standard first-stage F?" | Methods | Reference Papers |
| "Did others use this data source?" | Reference Papers | Application Context |
| "What threats could bias my estimate?" | All three | - |
| "How do I interpret heterogeneous effects?" | Methods | Reference Papers |
| "How should I handle attrition?" | Methods | Reference Papers |
| "Is my sample selection problematic?" | Methods | Reference Papers |
| "What's the policy relevance?" | Application Context | Reference Papers |
| "What's the causal parameter here?" | Methods | Application Context |
| "Should I cluster standard errors?" | Methods | Reference Papers |
| "What's the right functional form?" | Methods | Reference Papers |

### Step 2: Check Existing Knowledge

Before searching PDFs, check what's already documented:

1. Read `$LAB_DIR/insights/methods-literature/INDEX.md`
2. Read `$LAB_DIR/insights/application-context/INDEX.md`
3. Read `$LAB_DIR/insights/reference-papers/INDEX.md`
4. Check for relevant `.papercheck/packs/` that already exist

### Step 3: Extract Evidence via Papercheck

For papers not yet in evidence packs:

1. **Identify relevant PDFs** - Check `./lit/papers/`, `./papers/`, `./refs/`
2. **I will invoke the papercheck skill** for each relevant PDF
3. Papercheck extracts page-anchored quotes via Antigravity CLI (`agy`)
4. Evidence packs are cached in `.papercheck/packs/`
5. **Record which dimension** each finding belongs to

**Note:** If Antigravity CLI is not installed, I'll report findings without page anchors and note the limitation.

### Step 4: Synthesize Across Dimensions

Create a synthesis that cross-references findings:

```markdown
## Concern: [State the concern]

### Methods Perspective
- [Finding from methods literature]
- Evidence: `.papercheck/packs/[pack-name]/`

### Application Context
- [Finding about empirical setting]
- Evidence: `.papercheck/packs/[pack-name]/`

### How Reference Papers Handled It
| Paper | Approach | Evidence Pack |
|-------|----------|---------------|
| ... | ... | ... |

### Cross-References
- Methods finding X affects our interpretation of Context Y
- Reference paper Z's approach assumes Method W

### Recommendation for Our Paper
[Specific, actionable recommendation]
```

### Step 5: Store Findings

Update the appropriate INDEX files and create insight files if warranted:

1. **Add rows to INDEX tables** in relevant dimensions
2. **Create insight files** for substantial findings (see template below)
3. **Add cross-reference links** between dimensions
4. **Link to papercheck evidence packs** for audit trail

---

## Insight File Template

When creating files like `methods-literature/weak-instruments.md`:

```markdown
# Weak Instruments

## Summary
[1-2 sentence finding]

## Status
[Choose one based on criteria below]

## Sources
| Paper | Page | Quote |
|-------|------|-------|
| Stock & Yogo (2005) | p. 12 | "F < 10 indicates..." |

## Implications for Our Research
- [Specific action for your paper]

## Cross-References
- → application-context#data-limitations
- → RDR-003-first-stage-spec
```

**Status field criteria:**
- **Core**: Directly affects our identification strategy or main results; must address
- **Supporting**: Informs robustness checks or interpretation; should address
- **Pending**: Identified as potentially relevant; needs review before classifying
- **Parked**: Interesting but not critical to current paper; revisit later

---

## Directory Structure

When this skill runs in a project, ensure this structure exists:

```
$LAB_DIR/
├── insights/
│   ├── methods-literature/
│   │   ├── INDEX.md
│   │   └── [topic-specific files]
│   ├── application-context/
│   │   ├── INDEX.md
│   │   └── [topic-specific files]
│   └── reference-papers/
│       ├── INDEX.md
│       └── [topic-specific files]
```

---

## Integration with papercheck

This skill calls papercheck for evidence extraction. The evidence packs live in `.papercheck/packs/` and are referenced from the dimension INDEX files.

**Flow:**
1. lit-check identifies which papers to check
2. I invoke papercheck skill for each paper + issue
3. Papercheck creates evidence pack with page-anchored quotes
4. lit-check stores finding in appropriate dimension INDEX
5. Cross-references added between dimensions

---

## Example Usage

**User asks:** "How do papers handle pre-trends in staggered DiD?"

**lit-check response:**

1. **Dimension classification**: Methods (DiD assumptions) + Reference Papers (what others do)

2. **Check existing knowledge**: [Read INDEX files]

3. **Gap identified**: No existing notes on staggered DiD pre-trends

4. **Run papercheck** on:
   - Callaway & Sant'Anna (2021) - Methods
   - Sun & Abraham (2021) - Methods
   - [User's reference papers] - Reference Papers

5. **Synthesize**:
   - Methods: CS and SA estimators handle heterogeneous treatment timing differently
   - Reference Papers: Paper A uses event study, Paper B uses Bacon decomposition

6. **Store**: Update `$LAB_DIR/insights/methods-literature/INDEX.md` and `$LAB_DIR/insights/reference-papers/INDEX.md`

**Example output after running:**

```markdown
## Summary

| Dimension | Key Finding | Evidence |
|-----------|-------------|----------|
| Methods | CS/SA estimators handle heterogeneous timing; standard TWFE biased | pack: callaway-santanna-2021 |
| Reference | Paper A uses event study with Bacon decomp; Paper B uses CS estimator | pack: paper-a-did, paper-b-did |

## Action Items
- [ ] Switch from TWFE to Callaway-Sant'Anna estimator
- [ ] Add Bacon decomposition as robustness check
- [ ] Report event study coefficients

## Files Updated
- $LAB_DIR/insights/methods-literature/INDEX.md (added 2 rows)
- $LAB_DIR/insights/reference-papers/INDEX.md (added 2 rows)
- $LAB_DIR/insights/methods-literature/staggered-did.md (new file)
```

---

## Output Format

Always end with:

```markdown
## Summary

| Dimension | Key Finding | Evidence |
|-----------|-------------|----------|
| Methods | ... | pack: ... |
| Context | ... | pack: ... |
| Reference | ... | pack: ... |

## Action Items
- [ ] [Specific action for our paper]

## Files Updated
- $LAB_DIR/insights/[dimension]/INDEX.md
- [Any new insight files created]
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Paper doesn't address concern | Record as "Not addressed" in INDEX with note |
| Papercheck returns empty/no quotes | Paper may not discuss this issue; record "No evidence found" and try alternative search terms |
| Papercheck/Antigravity CLI unavailable | Proceed without page anchors, note limitation in output |
| INDEX.md doesn't exist | Run `/setup-memory` first |
| Duplicate findings | Check existing INDEX before adding; update existing row if new info |
| Paper not found in lit/papers/ | Ask user for PDF location or paper citation |
| Uncertain which dimension | Default to Methods for technique questions, Application Context for setting questions |
| Conflicting findings across papers | Document both views; note which applies to your context in Cross-References |

---

## When to Use This Skill

- Before making identification strategy decisions
- When a referee asks "how does the literature handle X?"
- When uncertain if a concern is standard or novel
- When comparing your approach to existing papers
- When documenting why you chose a particular method
