# Anti-AI Writing Standard

Load this file when a skill is about to draft scholarly prose, synthesis, or evaluative writing.

The goal is not to beat AI detectors. Detection tools are noisy and formal academic prose is especially vulnerable to false positives. Optimize instead for concrete human writing: specific claims, field-aware structure, stable terminology, and an authorial stance that fits the task.

## Why This Matters: How Detectors Work

AI detectors measure two properties of text:

- **Perplexity**: how predictable each word is given the preceding words. LLMs choose the statistically most likely next word, producing low-perplexity text. Human writing has higher perplexity because humans make unexpected but precise word choices.
- **Burstiness**: variation in sentence length and complexity across a document. Human writing has high burstiness — long complex sentences followed by short blunt ones. AI text clusters around a uniform ~27-word average.

The antidote to both is the same: write with specificity, vary your rhythm naturally, and choose words for precision rather than probability.

## Core Rule

Do not treat `academic writing` as one monolithic style. Separate:

- authorial voice: sentence movement, paragraph rhythm, hedging, citation integration
- genre structure: what belongs in an introduction, results section, review report, or literature review
- field or journal conventions: what the target audience expects in organization, notation, and evidence

Use only the structure the task actually requires.

## What To Suppress

### Content-level patterns

- generic importance claims that say a topic is `important`, `timely`, or `relevant` without naming the puzzle, evidence, or mechanism
- contribution boilerplate such as `this study contributes to the growing literature` unless the contribution is stated concretely
- shopping-list citation prose that marches paper by paper without comparison, disagreement, or synthesis
- table-to-prose mirroring that restates a long sequence of estimates in identical sentence shapes
- filler built from `highlighting`, `reflecting`, `ensuring`, `underscoring`, or similar empty continuations
- thesis-template signposting such as `firstly`, `secondly`, `in this section we will`, or roadmap language where the genre does not call for it
- inflated certainty, inflated novelty, or inflated policy relevance
- the obligatory balanced counterpoint: `While X, it is also true that Y` on every claim. Take a position when the evidence supports one.
- opening with broad obvious statements like `X has received growing attention in recent years` instead of a precise motivation

### Vocabulary blacklist

These words saw 600-6700% frequency increases in published text after ChatGPT and are now AI-detection markers. Avoid them unless the field genuinely uses them with a specific technical meaning:

| Avoid | Write instead |
|-------|---------------|
| delve, delves into | examine, study, look at, investigate |
| leverage (verb) | use, draw on, exploit |
| utilize | use |
| harness, foster, bolster | use, support, strengthen |
| underscore, underscores | show, emphasize (or delete — let the evidence speak) |
| showcase, showcasing | show, present, report |
| robust (non-statistical) | strong, reliable, stable |
| comprehensive | thorough, full, complete |
| pivotal, crucial | important, central, key |
| nuanced | careful, qualified, detailed |
| multifaceted | complex (or describe the specific facets) |
| intricate | complex, detailed |
| innovative, cutting-edge, groundbreaking | new, recent (or name the actual innovation) |
| seamless | smooth (or describe what actually works well) |
| landscape, realm, tapestry | field, literature, context, setting |
| synergy, interplay | interaction, relationship, connection |
| paradigm, nexus | (usually deletable — say what you mean) |
| meticulous | careful, thorough |
| facilitate | help, enable, allow |
| embark | begin, start |
| encompass | include, cover |
| navigate (metaphorical) | manage, handle, address |
| illuminate, elucidate | clarify, explain, show |
| spearhead | lead |

### Transition word discipline

These transitions are AI markers when overused. Prefer letting the logical connection emerge from content, or use casual connectors:

| Overused | Prefer |
|----------|--------|
| furthermore, moreover | and, also, or delete |
| consequently, accordingly | so, as a result, or restructure |
| notably, importantly | (delete — if it is notable, the reader will see that) |
| additionally | also, and, or delete |
| it is important to note | (delete entirely) |
| it is worth noting that | (delete entirely) |
| in conclusion | (delete — the reader knows it is the conclusion) |

### Sentence and paragraph patterns

- uniformly polished cadence where every sentence has similar length, weight, and closure
- every paragraph opening with a topic sentence. Vary: sometimes open with evidence, a question, a concession, a quotation, or a concrete example
- markdown habits, boldface emphasis, and list cascades where normal prose would read more naturally
- the `not just X, but also Y` template used more than once per document
- participial phrase constructions: `The system analyzes the data, revealing key insights`
- excessive rule-of-three phrasing: `adjective, adjective, and adjective`
- copula avoidance: replacing `is` or `has` with `serves as`, `stands as`, `represents`, `boasts`, `features`, `offers`. Just say what something is.
- false ranges: `from X to Y` constructions where X and Y are not on a meaningful scale. `from micro-level mechanisms to macro-level outcomes` → name the actual topics.
- synonym cycling: renaming the same subject repeatedly (`the method`, `the approach`, `the technique`, `the procedure`) instead of using stable terminology. Pick one term and stick with it.

### Formatting patterns

- em dashes: limit to 1-2 per page in academic writing. Use commas, semicolons, parentheses, or restructured sentences instead
- colon-heavy titles and headings
- title-casing all headings unless the journal style requires it
- boldface for emphasis in running prose
- perfect uniformity in paragraph length — vary deliberately
- curly quotation marks when the target format expects straight quotes

### Communication artifacts

These are chatbot conversation patterns that leak into drafted text. They are especially obvious in emails, draft sections, and informal academic communication.

- chatbot closers: `I hope this helps`, `Let me know if you'd like me to expand on any section`, `Feel free to ask`
- chatbot openers: `Certainly!`, `Of course!`, `Great question!`, `That's an excellent point`
- sycophantic padding: `You're absolutely right that this is a complex topic` — cut to the substance
- knowledge disclaimers: `as of my last update`, `While specific details are not extensively documented in readily available sources` — either cite the source or state what is unknown
- hedged existence claims: `it appears to have been established sometime in the 1990s` — find the actual date or say the date is unknown
- meta-commentary on the writing task: `Here is an overview of...`, `The following section provides...` — just write the content

### Filler phrase quick-reference

Common inflated phrases and their plain replacements:

| Instead of | Write |
|-----------|-------|
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| in the event that | if |
| has the ability to | can |
| it is important to note that | (delete — let the note speak) |
| a number of | several, or the actual number |
| in terms of | (restructure: `in terms of efficiency` → `for efficiency`) |
| with respect to | about, for, on |
| the question as to whether | whether |
| for the purpose of | to, for |
| in light of the fact that | because, given |
| it could potentially possibly be argued | (pick one hedge or delete all) |

## What To Prefer

- plain verbs over decorative substitutes
- stable terminology instead of synonym churn
- strategic hedging: assertive on well-established findings, cautious only where genuinely uncertain. Do not hedge everything equally.
- paragraphs organized around a claim, contrast, or inferential step
- citations that do argumentative work
- deliberate variation in sentence length — follow a long complex sentence with a short blunt one. Mix 8-word sentences with 35-word sentences. Let paragraph length vary from 2 sentences to 7+.
- structure and section labels that fit the field, journal, and task
- **specificity**: concrete numbers, dates, sample sizes, coefficient values, variable names, city names, policy names. Specificity is the single strongest signal of human authorship. Replace `several studies have examined this` with the actual citation and finding.
- **first-person voice** where the field allows it: `We estimate`, `I argue`, `Our identification exploits`. Standard in economics and signals authorial presence.
- **authorial stance**: take a position when the evidence supports one. `The more convincing explanation is X, because...` reads as human. Uniform diplomatic balance reads as AI.
- **reasoning chains**: show the path to a conclusion. `At first, this result seemed inconsistent with the theory. But once we conditioned on municipality size, the coefficient stabilized.` AI states conclusions; humans show how they got there.
- **mild emotional register**: express genuine reactions where appropriate — surprise at a striking magnitude, frustration at data limitations, intellectual excitement about an avenue. Do not maintain uniform neutrality.
- **self-correction as authenticity**: parenthetical asides, qualifications mid-sentence (`or more precisely, the intent-to-treat effect`), and brief sentence fragments for emphasis (`Not even close.`) all read as human.

## Task-Specific Guidance

### Literature synthesis

- Organize around disagreements, mechanisms, designs, contexts, or time periods.
- Do not default to one-paper-at-a-time summaries unless the user explicitly asks for an annotated bibliography.
- When multiple papers are cited together, say what actually links or separates them.

### Research ideation

- Skip inflated `why this matters` paragraphs that could fit any topic.
- State the empirical puzzle, source of variation, or new data opportunity directly.
- Phrase questions so that a referee could immediately see the design challenge.

### Referee and review reports

- Sound like a referee, not a polished executive summary generator.
- State what the paper does in concrete terms before criticizing it.
- Keep essential points few, specific, and tied to actual threats.
- Avoid generic requests for `more robustness` or `clearer framing` unless the exact missing evidence or clarification is named.

### Academic drafting and rewriting

- Do not fill introductions with throat-clearing that delays the question, design, or answer.
- Use roadmaps only when the target field or journal genuinely expects them.
- If a paragraph reads like a converted bullet list, rewrite it as an argument.
- Embed lists in prose when possible: `Three factors matter here: the timing of the reform, the selection of treatment municipalities, and the availability of pre-period data.`

### Emails and informal academic communication

- Strip all chatbot closers, openers, and sycophantic padding before sending.
- Match the register of the recipient: a co-author gets different prose than a dean.
- Prefer short direct sentences. Academic emails that read like polished abstracts signal AI assistance.

## Worked Example

Before (AI-sounding academic prose):

> The growing body of literature on minimum wage effects serves as a testament to the enduring importance of this policy question. Moreover, recent studies have delved into the nuanced interplay between wage floors and employment outcomes, highlighting the multifaceted nature of labor market adjustments. It is important to note that the evidence encompasses a wide range of methodological approaches — from difference-in-differences to synthetic control — showcasing the field's commitment to robust identification. Despite these challenges, the landscape of minimum wage research continues to evolve, offering valuable insights for policymakers and researchers alike.

After (human academic prose):

> The employment effect of minimum wages remains contested. Cengiz et al. (2019) find bunching at the new minimum but no missing jobs above it, while Neumark and Shirley (2022) argue their design misses disemployment in uncovered sectors. The disagreement turns on whether the comparison group is contaminated by spillovers — a problem that border-discontinuity designs partially address but do not resolve. We exploit a setting where spillovers are mechanically limited by the geographic isolation of treatment municipalities.

What changed: removed `serves as a testament` (inflated symbolism), `Moreover` and `It is important to note` (filler transitions), `delved into` and `nuanced interplay` (AI vocabulary), `multifaceted nature` and `robust` in non-statistical sense (blacklisted words), `highlighting` and `showcasing` (superficial -ing analysis), the `from X to Y` false range, `Despite these challenges...continues to evolve` (formulaic conclusion), `landscape` and `valuable insights` (AI vocabulary). Replaced with specific citations, a named methodological dispute, and the paper's actual identification strategy.

## Final Check

Before delivering prose, ask:

1. Could any sentence be made plainer without losing precision?
2. Does each citation help make a point, or is it just being displayed?
3. Have I mistaken a genre convention for an author's voice?
4. Does any paragraph merely summarize a table, list, or outline instead of making an argument?
5. Would a strong human writer in this field actually phrase it this way?
6. Is my hedging strategic (cautious where uncertain, assertive where supported) or uniform?
7. Do I have at least one concrete specific (a number, a name, a date, a coefficient) per substantive paragraph?
8. Does sentence length vary noticeably, or does it cluster around a uniform average?
9. Have I used any word from the vocabulary blacklist? If so, is there a precise reason, or can I replace it?
10. Have any chatbot artifacts leaked into the text? Scan for closers, openers, disclaimers, and meta-commentary.
