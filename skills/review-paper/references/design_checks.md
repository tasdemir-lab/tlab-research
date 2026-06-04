# Design Checks

Load this file when the manuscript's credibility depends on design-specific diagnostics or when the paper looks technically polished but may still hide subtle identification or implementation problems.

## Cross-Design Failure Modes

- Estimand mismatch:
  Check whether the quantity estimated is the quantity interpreted in the abstract, introduction, and conclusion.
- Bad controls:
  Check for post-treatment controls, collider paths, or controls that redefine the estimand.
- Sample drift:
  Check whether sample restrictions, missingness, attrition, migration, or reporting changes vary across specifications and drive the result.
- Robustness theater:
  Distinguish tests that address the actual threat from long tables of low-value specification churn.
- Mechanism inflation:
  Check whether mechanism evidence rules out nearby alternatives or simply co-moves with them.
- Appendix burial:
  Check whether fragility is hidden by moving crucial evidence into appendices that weaken the main claim.

## DiD And Event Study

### Core checks

- Is treatment timing staggered?
- If yes, does the paper use a modern estimator when heterogeneous effects make TWFE problematic?
- Are event-study plots readable, correctly normalized, and accompanied by confidence intervals?
- Are pre-trends visible and interpreted cautiously rather than as a binary pass/fail?
- Is treatment anticipation plausible?
- Are treatment effects contaminated by differential composition, selective survival, migration, or sample entry?

### Subtle traps

- Treatment timing is correlated with underlying trends even if pre-trends look flat in noisy data.
- Controls interact with treatment timing in ways that change the estimand.
- Event-study figures look reassuring but pool incomparable cohorts.
- The paper presents a strong reduced form but the policy mechanism varies across units or over time in a way the estimator ignores.

### What a strong paper usually has

- A clean institutional explanation of treatment timing.
- Modern estimation where needed.
- Event-study plots that are legible and interpretable.
- Placebos on unaffected periods, outcomes, or groups.
- Design-specific sensitivity discussion, not just generic robustness tables.

## IV

### Core checks

- Is the instrument relevant, and is the first stage shown clearly?
- Is exclusion argued with institutional detail rather than assertion?
- Is the estimand interpreted correctly as a local effect when appropriate?
- Are monotonicity or no-defiers assumptions at least discussed when relevant?
- Does the instrument shift the treatment in the expected margin and population?

### Subtle traps

- The instrument changes other channels that look economically plausible but are waved away.
- First-stage strength exists overall but collapses in the estimation sample or key subsamples.
- Reduced form and IV magnitudes are mechanically large because the first stage is tiny.
- The paper interprets LATE as a general policy effect without discussing who the compliers are.

### What a strong paper usually has

- A transparent first stage.
- A serious exclusion argument grounded in institutions.
- Interpretation tied to the complier margin.
- At least one falsification or balance check that would be uncomfortable if the IV story were wrong.

## RDD

### Core checks

- Is the running variable precise and manipulable?
- Are bandwidth choices justified and sensitivity shown?
- Are polynomial or local-linear choices aligned with current best practice?
- Are covariates smooth at the cutoff?
- Is bunching or sorting near the threshold addressed?

### Subtle traps

- The cutoff rule is clear on paper but implemented noisily in practice.
- Covariate smoothness holds mechanically because the effective sample is tiny.
- Functional-form choices do too much work.
- Interpretation drifts from local treatment effect near the cutoff to broader policy claims.

### What a strong paper usually has

- Transparent institutional cutoff logic.
- Manipulation checks.
- Bandwidth and specification sensitivity.
- Local interpretation that stays honest about external validity.

## Panel And Administrative Data

### Core checks

- Is the sample construction reproducible and stable across tables?
- Are administrative coding conventions, merges, and data quirks understood?
- Are unit changes, ID changes, top-coding, imputation, or reporting lags relevant?
- Do standard errors reflect the real dependence structure?

### Subtle traps

- Administrative coverage changes over time in ways correlated with treatment.
- Seemingly minor linkage loss changes the composition of treated and control groups.
- Unit definitions shift across appendices and tables.
- Measurement is precise for one outcome but not the mechanism or denominator used to scale it.

### What a strong paper usually has

- Clear sample flow.
- Stable definitions across the paper.
- Attention to institutional data generation and coding.
- Checks that composition and linkage issues are not driving the findings.

## Mechanism Evidence

### Core checks

- Does the mechanism test distinguish the proposed channel from close substitutes?
- Are mechanism outcomes measured credibly?
- Is the mechanism analysis pre-specified by the framework, or does it read as ex post storytelling?

### Subtle traps

- Mechanism variables are themselves downstream outcomes and do not isolate the channel.
- Multiple mechanism tests are run until one "works."
- The mechanism evidence supports a broad family of explanations, not the paper's specific story.

### What a strong paper usually has

- A mechanism prediction tied to the framework.
- Tests that would look different under rival channels.
- Honest discussion of what the mechanism evidence can and cannot establish.

## Visual And Presentation Diagnostics

- Check whether the key figure is the right figure.
- Check whether coefficient plots, event studies, maps, or binscatters clarify the design rather than decorate it.
- Check whether table progression tells a coherent story.
- Check whether appendix figures quietly undercut the main text.

## High-Value Referee Questions

- What is the hardest design-specific objection a skeptical referee would raise first?
- If the main coefficient were correct, what alternative story would still be consistent with the evidence shown?
- Which missing test would most change your confidence in the result?
- Which appendix item is doing hidden work for the paper's credibility?
