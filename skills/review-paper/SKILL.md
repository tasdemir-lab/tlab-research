---
name: review-paper
description: Use when reviewing an academic manuscript with a referee-style rubric. Score contribution, identification, data, econometrics, theory, robustness, literature, magnitudes, internal consistency, exposition, and presentation; produce page-anchored major and minor comments with concrete revision requests.
---

# Review Paper

Use this skill for referee-style reviews of `.tex`, `.qmd`, `.Rmd`, or `.pdf` manuscripts. The default standard is a top-field or top-5 applied economics referee. If the paper is outside applied empirical economics, adapt each dimension to the closest relevant analogue and say briefly how you are interpreting the rubric in that domain.

## Review Stance

- Read like a careful referee, not a copyeditor.
- Prioritize contribution, identification, theory/framework, and whether the conclusions are actually supported by the evidence.
- Judge what is on the page, not what the author may have intended.
- Anchor important claims to pages, sections, tables, figures, or equations whenever possible.
- If the paper is long, read in chunks and keep notes; do not pretend to have verified material you did not inspect.
- Use a structured multi-pass review loop. Do not stop after the first plausible report.
- Look actively for subtle problems, not just obvious flaws.
- Do not stop at diagnosis; give advice that would materially raise the paper's chances at a top-tier journal when that is feasible.

## Selective References

Load reference files when they are relevant, and treat some of them as required once the paper type is known:

This skill bundles six first-class reference modules under `references/`: `design_checks.md`, `field_patterns.md`, `top_tier_upgrade.md`, `argument_structure.md`, `report_style.md`, and `revision_strategy.md`.

- If the paper uses DiD, IV, RDD, event studies, panel/admin data, or mechanism-heavy evidence, you must read [references/design_checks.md](references/design_checks.md) before finalizing `D2`, `D4`, `D6`, or `D11`.
- If the paper sits mainly in labor, education, demography, family, public, or development, you must read [references/field_patterns.md](references/field_patterns.md) before finalizing `D1`, `D7`, `D8`, or the top-tier advice.
- When writing `Top-Tier Upgrade Advice`, read [references/top_tier_upgrade.md](references/top_tier_upgrade.md).
- When the review produces revision advice, when the user asks how to integrate feedback, or when using this skill to guide a revision in progress, read [references/revision_strategy.md](references/revision_strategy.md). This module governs how review findings should translate into manuscript changes — specifically, how to frame new evidence, position robustness checks, and maintain a confident authorial stance.
- If the paper's argument structure, framing, exposition, or internal narrative coherence is a live issue, read [references/argument_structure.md](references/argument_structure.md) before finalizing `D9`, `D10`, or the top-tier advice. This bundled reference is calibrated to an expanded sample of published papers from `AER`, `JPE`, `QJE`, `AEJ: Applied Economics`, and `Labour Economics`, and it separates mini-norms for experimental, reduced-form empirical, and theory-guided empirical papers.
- When drafting the final report, read [references/report_style.md](references/report_style.md) and [../_shared-writing/anti-ai-writing-standard.md](../_shared-writing/anti-ai-writing-standard.md).

## External Validation And Context Fact-Checking

Do not rely only on the manuscript's own framing when novelty, institutional facts, or literature positioning matter.

- Load any local fact store first if it exists, such as `lab_notes/facts.md`, `lab_notes/facts/`, `_lab/facts.md`, `_lab/facts/`, or similar project fact files.
- Use the manuscript bibliography and cited comparator papers to identify the nearest references, not just the papers the manuscript chooses to emphasize.
- If Zotero is available, use it to locate key papers, metadata, notes, and attached PDFs.
- Zotero is not enough by itself. When necessary, verify with additional sources such as the paper PDFs themselves, official institutional documents, data documentation, working-paper versions, journal pages, or other primary internet sources.
- Use internet resources when the review depends on context-specific institutional facts, disputed novelty claims, or literature comparisons that cannot be verified from the manuscript alone.
- Prefer primary sources over secondary summaries.
- If external verification is not possible, say so explicitly and lower confidence in `D1`, `D2`, `D3`, `D7`, or any context-sensitive claim that depends on it.

## Workflow

1. Locate the manuscript and any appendices, exhibits, or companion tables/figures that matter for the review.
2. Locate local fact stores, manuscript notes, bibliography files, and companion reference material that may constrain factual claims about the paper's institutional context or literature.
3. Identify the paper's main design and field early so you can load the required reference files above before scoring the relevant dimensions.
4. Read the paper to the depth required for a defensible referee report.
   - In the normal case, this means the full main text plus every appendix, exhibit, and companion table or figure set that materially bears on identification, measurement, estimation, robustness, or interpretation.
   - If the package is too long for uniform line-by-line treatment, prioritize the score-moving material and state the exact coverage limits later in `Coverage Notes`.
5. For source projects in `.tex`, `.qmd`, or `.Rmd`, reconstruct the actual manuscript under review:
   - inspect included files such as `\input`, `\include`, child documents, generated appendix files, and external table or figure sources
   - prefer reviewing the compiled manuscript or rendered output if it exists
   - if only source files are available and rendering is feasible, render or otherwise verify the assembled manuscript before relying on section numbers, figures, tables, or appendices
   - if rendering or reconstruction is not feasible, say so explicitly in `Coverage Notes` and lower confidence in presentation and cross-reference judgments
6. For long papers, use a coverage plan rather than pretending to have done uniform depth everywhere:
   - read the main text fully
   - inspect all appendix sections tied to main claims
   - spend extra time on the sections that determine `D1`, `D2`, `D4`, `D5`, and `D6`
   - explicitly note any sections or appendices that were only checked for targeted claims rather than read line by line
7. Build a paper map:
   - question and claimed contribution
   - institutional setting and source of variation
   - data source, sample, and measurement choices
   - main estimating equations or empirical design
   - main tables, figures, and headline findings
   - model or conceptual framework, if any
8. Extract hard evidence before judging:
   - where the paper states its contribution
   - where identification assumptions are defended
   - where measurement choices and sample restrictions are defined
   - where robustness, placebo, and sensitivity analyses appear
   - where magnitudes, mechanisms, and interpretation are discussed
9. Before scoring `D1` or `D7`, verify the closest-paper comparison against local fact stores, the bibliography, Zotero if available, and internet-accessible primary sources when needed. Do not score novelty or positioning from memory alone.
10. Before scoring `D2`, `D3`, `D4`, `D6`, or `D11`, verify whether the relevant support lives partly or entirely in appendices. Do not score those dimensions from the main text alone if the paper points to appendix evidence.
11. Fact-check institutional, legal, administrative, and data-context claims against local facts, key references, and external sources when those claims are material to the review. Do not argue from general priors if there is context-specific evidence pointing the other way.
12. Run a subtle-problem scan before drafting conclusions. Check for:
    - mismatch between the claimed estimand and what the design actually identifies
    - post-treatment controls, bad controls, collider risk, or conditioning that changes the estimand
    - sample changes across specifications, hidden attrition, or composition shifts driving results
    - selective heterogeneity analysis, multiple-testing risk, or subgroup stories that look ex post
    - main-text and appendix inconsistencies in samples, signs, magnitudes, or definitions
    - mechanism tests that are underpowered, non-discriminating, or consistent with rival explanations
    - policy or welfare claims that outrun the design
    - external-validity claims that exceed the evidence
    - literature positioning that understates how close the nearest papers really are
    - magnitudes that are statistically significant but economically thin, mechanically inflated, or benchmarked poorly
13. Build an evidence ledger before drafting conclusions. For each important finding, record:
    - the claim
    - the anchor: page, section, table, figure, or equation
    - whether the claim was checked only against the manuscript or also against external sources
    - the external source used when one materially affects the claim
    - whether the anchor directly supports the claim or only partially supports it
14. Run the review loop below.
15. Produce the final referee report only after the required review passes are complete unless the user explicitly asks to see the intermediate rounds.

## Review Loop

Each pass has four phases: `review -> scrutinize -> verify -> revise`.

Minimum requirement:

- Use at least 2 substantive passes for every nontrivial review.
- Add a third pass when the manuscript is long, technically complex, high-stakes, appendix-dependent, or still has unresolved score-moving uncertainty after pass 2.
- Do not claim a specific number of passes unless your work actually reflected that number.

### Pass 1. Review

- Draft a provisional scorecard on all 11 dimensions.
- Write the provisional major and minor comments.
- Make the strongest case both for and against the paper before locking scores.

### Pass 1. Scrutinize

Attack the provisional review as if you were an adversarial senior referee.

- Ask of every major claim: "What would make this judgment wrong?"
- Look for overreach, vague criticism, missing anchors, and comments that merely reflect preference rather than referee-standard necessity.
- Check whether you are punishing the paper for something it never claims.
- Check whether you are letting polished prose, technical jargon, or a fashionable design hide weak evidence.
- Check whether the paper's most serious weakness is actually a subtle one rather than the obvious issue named in the first draft.
- Force yourself to identify at least:
  - one place where the draft review may be too harsh
  - one place where it may be too lenient
  - one factual claim that still needs direct verification in the manuscript

### Pass 1. Verify

Re-open the manuscript and verify the provisional review against the paper.

- Re-check every nontrivial factual assertion in the review.
- Confirm quoted numbers, sample definitions, estimator descriptions, and whether a claimed robustness or placebo actually exists.
- Confirm that cited sections, tables, figures, and equations are the correct anchors.
- Re-check external factual claims about institutions, data context, and closest-paper comparisons against the strongest available source.
- Downgrade confidence when the evidence is indirect, ambiguous, or missing.
- Remove comments that are not supported after re-reading.
- If the paper delegates key support to an appendix, re-check the appendix directly rather than inferring from the main text summary.

### Pass 1. Revise

- Update the scorecard and comments in light of scrutiny and verification.
- Tighten broad comments into concrete revision requests.
- Note which scores or claims changed and why.
- Carry only the revised review into the next cycle.

### Pass 2+

- Each additional pass should actively challenge and refine the surviving claims from the previous pass rather than merely restating them.
- The final pass must explicitly confirm that every surviving major comment and every below-threshold score still has verified support.

For long manuscripts, pass 1 should establish broad coverage and a first scorecard. Later passes may focus on the score-moving claims, but they still must verify every surviving major comment and every below-threshold dimension against the manuscript.
If pass 2 resolves the main score-moving uncertainty, an optional third pass can be a shorter confirmation pass rather than a full redraft.

### Self-Review Pass (recommended)

After completing the standard review loop, attack the draft report itself as if you were a senior co-referee checking your work. This pass catches issues the review-loop misses because it changes the object of scrutiny from the manuscript to the review.

Check for:
- Factual errors or imprecisions in the review's own claims (e.g., characterizing a range imprecisely, echoing the manuscript's language without questioning it).
- Issues in the manuscript that the review missed (e.g., table-code inconsistencies, hardcoded indicators that don't match the model, estimand imprecision).
- Internal inconsistencies within the review (e.g., a score justification that contradicts a major comment, redundancy between major comments and upgrade advice).
- Places where the review is too harsh (punishing the paper for something it doesn't claim) or too lenient (letting polished prose hide a subtle problem).
- New ideas that emerge from re-reading (e.g., low-cost heterogeneity tests, missing placebo exercises).

Key heuristic: for every claim in the review, ask "What would make this judgment wrong?" For every term echoed from the manuscript (e.g., "different identifying assumptions"), ask "Is this technically precise?"

When prioritizing major comments, distinguish the deepest limitation (which may be unfixable) from the most improvable concern (which the author can address). Frame the lead major comment as the most *improvable*, not necessarily the most *important*.

Update the report with findings before delivering. Note the self-review pass in the closing line.

## Scoring Rules

- Allowed scores: `1.0` to `5.0` in `0.5` increments.
- `4.0` means the paper is submission-ready on that dimension.
- Treat the paper as submission-ready only if every applicable dimension scores at least `4.0`.
- `D1`, `D2`, and `D5` are "fatal if weak." A score below `3.0` on any of them indicates a fundamental problem.
- In default applied-empirical use, `D5` may be `N/A` only if the research question genuinely does not need a formal model. If so, explicitly justify the `N/A` and evaluate whether the paper still has a coherent interpretive framework.
- When the evidence is mixed, choose the lower score and explain what missing evidence would move it up.
- `D1` and `D7` should be treated as lower-confidence scores if closest-paper comparisons were not externally checked.

## Applicability Rules

- Score all 11 dimensions for standard applied-empirical papers by default.
- Outside the skill's default applied-empirical domain, adapt first and only then score. Any dimension may be marked `N/A` if it is genuinely inapplicable after good-faith adaptation, but each such `N/A` must be explicitly justified in one sentence.
- Do not silently drop a dimension because it feels less central, because the paper is outside applied micro, or because the evidence is thin.
- If a dimension is less central in a given paper, still score it using the closest relevant interpretation and state that interpretation briefly.
- If the manuscript does not provide enough evidence for a confident score, assign the score that the available evidence supports and say what is missing.

## Global Score Calibration

- `1.0` to `2.0`: major problem, often design-threatening or conceptually confused.
- `2.5` to `3.5`: plausible paper with real value, but not yet at journal standard.
- `4.0`: credible, well-executed, and publication-ready on that margin.
- `4.5` to `5.0`: unusually strong or field-leading on that margin.

## Dimension-by-Dimension Rubric

- `D1. Contribution & Novelty`
  Ask: why should the reader care, and what is genuinely new?
  Score low when the paper is a thin context extension, a repackaging of known results, or vague about what it adds.
  Score high when the gap, novelty, and implications for theory or policy are clear and well distinguished from the closest papers.

- `D2. Identification Strategy`
  Ask: is the causal claim credible, and is the institutional narrative convincing?
  Score low when exogeneity is asserted rather than defended, assumptions obviously fail, or the institutional setting is too vague.
  Score high when the source of variation is clean, assumptions are tested where possible, and remaining threats are second-order and acknowledged.

- `D3. Data & Measurement`
  Ask: do the variables and sample actually measure the constructs of interest?
  Score low when sample selection, attrition, proxy quality, or variable definitions create serious doubts.
  Score high when the data-generating process, sample construction, and measurement limitations are transparent and unlikely to drive the results.

- `D4. Econometric Implementation`
  Ask: are the methods correctly specified and up to date?
  Check clustering, estimator choice, functional form, weighting, control selection, treatment timing, and inference.
  Score low when there are implementation errors that could change inference, such as wrong clustering, problematic controls, or outdated DiD practice.
  Score high when the methods fit the design and reflect modern econometric standards.

- `D5. Theoretical Framework / Model`
  Ask: does the paper have a coherent framework that disciplines interpretation?
  This can be a conceptual model, mechanism model, structural model, or other theory-backed mapping from question to empirics.
  Score low when the framework is missing, inconsistent, or disconnected from what is estimated.
  Score high when the model generates clear predictions and the empirics speak directly to them.

- `D6. Robustness & Sensitivity`
  Ask: how fragile are the results?
  Look for design-specific checks, placebo or falsification tests, alternative specifications, bounds, and alternative estimators where relevant.
  Score low when robustness is tokenistic or misses the real threats.
  Score high when the paper directly stress-tests its own design and the findings remain stable.

- `D7. Literature & Positioning`
  Ask: does the paper know and correctly position itself relative to the closest work?
  Verify this against the actual nearby literature, not just the manuscript's own literature review.
  Score low when major related papers are missing or the distinctions are generic.
  Score high when the paper precisely differentiates itself from the closest antecedents and shows command of the field.

- `D8. Economic Magnitudes & Interpretation`
  Ask: do the estimates matter economically, and does the paper help the reader understand the numbers?
  Score low when the paper leaves coefficients uninterpreted or uses weak benchmarks.
  Score high when it translates effects into meaningful quantities, policy relevance, welfare, cost effectiveness, or credible comparisons to related estimates.

- `D9. Internal Consistency`
  Ask: do the model, empirical design, results, and interpretation tell the same story?
  Score low when sections contradict one another or secondary findings undermine the narrative without explanation.
  Score high when anomalies are acknowledged and the paper reads as an integrated whole rather than disconnected sections.

- `D10. Exposition & Structure`
  Ask: is the paper clearly written, well organized, and economical?
  Score low when the introduction buries the contribution, the paper is difficult to follow, or sections are badly ordered.
  Score high when the reader can identify the question, design, and main finding quickly and each section earns its place.

- `D11. Tables, Figures & Presentation of Results`
  Ask: can the reader understand the results from the tables and figures alone?
  Check labeling, specification progression, sample sizes, standard errors, and whether the key visual objects are present.
  For applied work this often includes event-study plots, coefficient plots, binscatters, maps, or first-stage visuals when relevant.
  Score low when tables are hard to parse or essential figures are missing.
  Score high when the results presentation is clear, professional, and helps the paper make its case.

## Higher-Order Checks

For papers that look polished or technically strong, go beyond the first-order review:

- Check whether the real weakness is subtle rather than obvious.
- Check whether the paper's claims outrun the design, data, or estimand.
- Check whether the paper is genuinely important or merely competent.
- Use the reference files above when the design, field, or ambition level requires sharper referee instincts.

## Output Requirements

Produce a human-readable referee report in Markdown unless the user explicitly asks for another format.

By default, output the final post-review-loop report. Do not dump all intermediate drafts unless the user asks for them. However, the final report should reflect the fact that unsupported claims were filtered through scrutiny and verification.

Default output should be concise and editor-usable. Unless the user asks for a full rubric dump, treat the following as a preferred schema rather than a mandatory maximum-length template.

Required sections in the normal case:

1. `Summary`
   - 2 to 4 sentences on the question, design, and main finding.
2. `Overall Assessment`
   - one short paragraph on overall quality, publication potential, and what blocks acceptance
   - state the paper's main strength before the main blocking weakness
   - if the paper is outside applied empirical economics, briefly note how the rubric was adapted
3. `Scorecard`
   - one line per dimension with the score, a terse justification, and at least one anchor
   - anchors should point to a page, section, table, figure, or equation
   - if a score materially depends on an external fact check or literature comparison, cite the external source briefly on that line
   - explicitly flag any below-threshold dimensions
   - explicitly flag any fatal weakness in `D1`, `D2`, or `D5`
   - explicitly justify any `N/A` used
4. `Major Comments`
   - numbered list
   - treat these as the essential points the authors would need to address
   - include at most 3 major comments in the normal case
   - if there are more than 3 independent publication-blocking problems, you may exceed that cap, but only for distinct fatal issues
   - each item must identify the relevant dimensions, state the problem precisely, cite the supporting anchor and any material external source, or explicitly say that the paper is missing the needed evidence, and request a concrete fix, test, clarification, or reframing
5. `Minor Comments`
   - specific actionable comments on writing, organization, citations, table design, interpretation, or missing references
   - use this section for nonessential suggestions rather than inflating the major comments list
   - anchor minor comments when practical; if not practical, keep them clearly non-factual
6. `Priority Fixes`
   - the 3 to 5 highest-leverage revisions the author should do first
7. `Verification Notes`
   - short paragraph or bullets on what the final pass re-checked most carefully
   - note which appendices or companion materials were checked
   - note which local fact stores, key references, Zotero items, or internet sources were used for fact-checking
   - mention any claims that remain uncertain because the manuscript did not provide enough evidence
Optional sections when they add real value:

8. `External Check Notes`
   - list the specific external checks that materially affected `D1`, `D2`, `D3`, `D7`, or any institutional-context claim
   - say whether each external check confirmed, complicated, or contradicted the manuscript's framing
9. `Coverage Notes`
   - if the paper is long or appendix-heavy, state the review coverage explicitly
   - distinguish material read fully from material checked only for targeted verification
10. `Top-Tier Upgrade Advice`
   - 3 to 6 concrete suggestions aimed at raising the paper toward top-field or top-5 standards
   - focus on the highest-return changes in contribution framing, identification credibility, mechanism evidence, interpretation, and exposition
   - distinguish advice that is realistically feasible in revision from advice that would require a different paper
   - if the paper is unlikely to be a plausible top-tier submission, say so plainly and redirect this section toward the best realistic quality-improving path

## Internal Working Rules

- Maintain a private evidence ledger while reviewing, even if the user only wants the final prose report.
- A comment may survive to the final report only if it is:
  - materially important, or useful as a minor point
  - tied to a dimension
  - supported by verified manuscript evidence, or explicitly labeled as an uncertainty
- Do not make context-sensitive claims about institutions, legal rules, data generation, or literature novelty from generic background knowledge alone when project facts, key references, Zotero, or internet primary sources can verify them.
- If a score changes across cycles, keep the final score only, but make sure the final justification reflects the corrected reasoning.
- If the scrutiny or verification pass reveals that a major criticism was mistaken, delete it rather than softening it into a vague complaint.
- A major comment must be either:
  - a verified criticism tied to manuscript evidence, or
  - a verified statement that the manuscript fails to provide evidence it would need to support a claim
- Keep the report concise enough to be usable. The final report should normally fit within roughly 1 to 3 pages of prose-equivalent length, but may exceed that when multiple independent fatal issues require separate treatment.
- If the user asks for a short review, compress the schema instead of insisting on every optional section.
- Do not keep a major comment merely because the concern is plausible. Plausibility without manuscript support is not enough.
- If a point remains uncertain after verification, downgrade it to a minor comment or frame it as a request for clarification rather than a factual criticism.
- At least one major comment should target the paper's most subtle or easy-to-miss weakness when such a weakness exists.
- `Top-Tier Upgrade Advice` should not repeat the major comments verbatim. It should synthesize what would most improve the paper's ceiling, not just patch local defects.

## Guardrails

- Distinguish fatal design problems from fixable polish issues.
- Do not invent sections, tables, regressions, appendices, or citations that you did not verify.
- If the paper does not provide the evidence needed to assess a dimension, say so plainly and score accordingly.
- Do not let polished writing hide weak identification or weak contribution.
- Do not let a clever design hide weak magnitudes, poor exposition, or missing literature positioning.
- Do not confuse technical sophistication with contribution or credibility.
- Do not let generic prior beliefs override project facts or institution-specific evidence.
- Do not recommend top-tier upgrades that contradict the actual design, data, or claims of the paper.
- When appropriate, name the specific modern checks a top referee would expect, such as placebo outcomes, placebo groups, alternative estimators, Oster bounds, Lee bounds, or sensitivity to violations of parallel trends.
