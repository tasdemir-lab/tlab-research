# Revision Strategy

Load this file when the review produces revision advice, when the user asks how to integrate reviewer feedback into a manuscript, or when the skill is used to guide a revision in progress. These principles govern how review findings should be translated into manuscript changes.

## Core Principle

The goal of a revision is submission viability, not invulnerability. Every paper will receive revision requests. The target is a paper that cannot be desk-rejected and that referees engage with seriously rather than dismiss — one where the editor thinks "this is worth developing" rather than "the authors don't trust their own results."

## Hierarchy Rule

Main text should contain the paper's strongest credible claim, its essential design defense, and the highest-value supporting evidence. Secondary nuance belongs in robustness sections or appendices.

A reader who finishes the introduction and conclusion should think: "this paper has a clear finding and the authors trust it." If they instead think: "interesting idea, but even the authors seem uncertain," the framing has failed regardless of what the evidence shows.

## Tone Translation Rule

Convert reviewer objections into author-facing revisions, not reviewer-facing prose. Reviewer language diagnoses problems. Paper language presents results. These serve different purposes and should never be confused.

| Reviewer writes | Paper should say |
|---|---|
| "The estimate is sensitive to the control group" | "The estimate is robust to alternative specifications, with more conservative approaches still yielding meaningful effects" |
| "The theory is in tension with the heterogeneity" | "The heterogeneity reveals that the treatment operates through multiple margins, consistent with the model's framework" |
| "The baseline may be inflated" | "Under more demanding controls, the estimate remains significant at [X] percentage points" |
| "The result is only marginal" | "We find suggestive evidence of [X]" |
| "This looks like an ex post rescue" | [Restructure so the evidence leads and the interpretation follows] |

The left column is what the reviewer writes. The right column is what the paper should say. The content is the same; the framing is not.

## Ten Revision Principles

### 1. Position new analysis before writing it into the text

The workflow should be:

1. Run the analysis
2. Assess the results — what do they show? How strong are they?
3. Decide positioning — main text, robustness, appendix, or omit from the main narrative?
4. Write it in with the positioning already determined

Never write new evidence into the main text before deciding where it belongs. Evidence that is written in at full intensity before assessment tends to stay at full intensity regardless of what it shows.

### 2. Do not relabel a robustness specification as preferred unless the paper's identification argument is being explicitly rebuilt around it

The baseline specification stays the baseline because it is the one the paper's identification strategy directly justifies. Alternative specifications test the claim; they do not replace it. When a robustness check yields a different number, the paper should report both and explain the difference — not abandon the baseline.

If the alternative specification genuinely should be the main specification, that requires rebuilding the identification narrative, not just relabeling.

### 3. Match the intensity of the response to the severity of the concern

| Concern severity | Appropriate response |
|---|---|
| Desk-rejection threat (e.g., missing pre-trend test, wrong estimator) | Add prominently in main text |
| Revision request (e.g., alternative control groups, additional robustness) | Add a table; mention in one sentence in the relevant section |
| Interesting nuance (e.g., mechanism decomposition, heterogeneity) | Short subsection, appendix, or one paragraph plus one table |
| Polish (e.g., citation precision, table formatting) | Fix directly |

Review-driven revisions often over-correct. AI implementations are especially prone to maximal rather than proportional responses. When a reviewer identifies a vulnerability, the natural instinct is to address it with a new section, new tables, and new language in the abstract. Usually a table and a sentence are sufficient.

### 4. Sensitivity results are robustness, not the new headline

When a more demanding specification yields a smaller estimate, the paper should present the baseline as the main result and the alternative as confirmation that the finding survives stress-testing. Framing the smaller number as a range or as the "honest" estimate tells the reader the baseline is wrong.

Standard framing: "Our main estimate is X. Under [more demanding specification], the estimate is Y, confirming that [the result is not driven by Z]."

Defensive framing (avoid): "Our estimate ranges from Y to X depending on how one controls for Z, and the true effect is likely at the lower end."

### 5. Protect distinctive theoretical claims

A paper's most memorable theoretical contribution is its highest-value asset for journal placement. When a reviewer asks for qualification, qualify — but do not apologize. State the theoretical result confidently on its own terms, then separately note where the model is silent or where additional margins complicate the aggregate prediction.

A model that correctly predicts the comparison margin for one age group is not wrong because the extensive margin dominates for another age group. The model analyzes one margin; the data reveals that multiple margins are active. These are complementary, not contradictory.

### 6. Compress secondary evidence proportionally to its strength

Page space signals importance. Two tables and a full subsection signal "this is a main finding." One table in a robustness section signals "we checked this and here is what we found."

When new evidence is tentative (marginally significant, pattern goes in an unexpected direction, interpretation is ambiguous), it should occupy space proportional to its evidential weight. Centering it in the main narrative gives it more weight than it can bear.

### 7. The abstract and conclusion control the journal ceiling

Editors read the abstract, introduction, and conclusion first. These sections should present the strongest credible version of the paper's claim.

- Abstract: one clean number, one sentence on robustness. No ranges unless the range itself is the contribution.
- Introduction: the main result in one confident sentence. Sensitivity acknowledged in one subordinate clause, not a full paragraph.
- Conclusion: open with what the paper teaches about the question, not with what it found in the data. Close with directions for future work, not with a list of reasons to distrust the result.

### 8. Acknowledge limitations without centering them

Known limitations should appear in the paper — usually in a limitations paragraph near the end of the conclusion or discussion. They should not appear in the abstract, should not lead the introduction's results paragraph, and should not dominate the conclusion.

The test: if a reader reads only the abstract and conclusion, do they come away with the paper's contribution or with its caveats? If the answer is caveats, the framing needs work.

### 9. Keep the strongest defense, not every defense

When multiple robustness checks address the same concern, lead with the strongest one. The DDD that gives 0.037 (p = 0.002) is more convincing than six alternative control-group specifications. A single strong piece of evidence, clearly presented, is more persuasive than an exhaustive catalog of partial checks.

The robustness section should feel like "we tested this carefully" rather than "we are worried about this."

### 10. A paper should know its best claim

After the revision, read the abstract and ask: what is the one thing this paper establishes? If the answer is clear and confident, the revision succeeded. If the answer is "it depends on the specification," the revision imported too much reviewer language.

The best claim is not always the largest number or the boldest theory. It is the claim the evidence most clearly supports, stated without unnecessary qualification.
