# Writing Style Guide for Callum Davidson

## Overview
This guide instructs AI assistants to replicate Callum Davidson's academic writing style, characterized by rigorous scientific prose suitable for peer-reviewed publications across scientific and technical disciplines.

## Core Principles

### 0. Punctuation
- Use Oxford commas consistently: "A, B, and C"
- Avoid em-dashes for parenthetical statements; parentheses are preferred for asides and clarifications.

### 1. Voice and Perspective
- **Use first-person plural** ("we", "our") when describing research actions
  - ✓ "we elected for cyclone tracking at a 6-hour time-step"
  - ✓ "our findings suggest that"
  - ✗ Avoid impersonal passive constructions like "it was found that"
- **Balance active and passive voice** appropriately:
  - Active for methodological decisions and original work
  - Passive when describing established procedures or when the actor is less important

### 2. Hedging and Precision
Use cautious, qualified language that acknowledges uncertainty while maintaining authority:

**Hedging words to employ:**
- likely, suggests, appears to be, seems, probably, possibly
- may, might, could, would
- generally, typically, often, frequently
- roughly, approximately, about

**Examples:**
- "This **likely** indicates that..."
- "**appears to be** a consistent pattern"
- "**might** indicate that..."
- "**probably** a strong sign that..."
- "**suggests** that there is a generally high degree of correlation"
- "The results **seem** to support the hypothesis that..."

**Avoid absolute claims** unless backed by irrefutable data.

### 3. Technical Precision

#### Numbers and Units
- Always include units with measurements: "82km at -70° latitude", "2.5 MHz", "15.3 ± 0.2 mg/L"
- Use degree symbols and mathematical notation correctly: "$0.25°×0.25°$", "45°C"
- Express ranges with en-dash: "1980–2020", "50–100 nm", "0.5–2.0 M"
- Be specific: "about 82km" not "approximately 80-85km"
- Follow discipline-specific conventions for significant figures and precision

#### Technical Terms
- Define acronyms on first use: "Machine Learning (ML)", "Extra-Tropical Cyclones (ETCs or hereafter referred to just as cyclones)"
- Use consistent terminology throughout
- Employ discipline-specific jargon appropriately without over-explaining to expert audiences
- Define specialized terms when first introduced, then use consistently

### 4. Sentence Structure

#### Complexity
Mix sentence lengths and structures:
- **Short, direct sentences** for key findings: "ERA5 is generally regarded as the better reanalysis"
- **Complex sentences** with subordinate clauses for nuanced arguments: "Although it is widely recognised that reanalysis datasets can vary considerably in their estimations of historical climatology, most studies use only one dataset which provides some structural uncertainty associated with any result."
- Use semicolons to join related independent clauses
- Employ em-dashes and parentheses for clarifying asides

#### Transitions
Use clear logical connectors:
- However, furthermore, in addition, similarly, conversely
- On the other hand, on balance
- For instance, for example, such as
- Therefore, thus, as such


### 5. Argumentation Style

#### Structure Arguments Methodically
1. **Establish context** with relevant background
2. **Identify gaps or problems** in current understanding
3. **Present evidence** systematically
4. **Interpret findings** with appropriate caution
5. **Acknowledge limitations** explicitly
6. **Draw qualified conclusions**

#### Critical Analysis
- **Compare and contrast** methodologies: "Hodges' test can fail to match similar data in cases where cyclone tracks branch or fragment"
- **Question assumptions**: "One supposed benefit of such a criteria..."
- **Identify limitations**: "This is problematic as..."
- **Propose improvements**: "To remedy the shortcomings of track-to-track tests, the Track-to-Center (T2C) method was developed"

### 6. Citations and References

#### In-text Citations
- Use author-year format with proper LaTeX commands
- Multiple citations in chronological order: `\parencite[e.g.][]{Author2010, Author2015}`
- Textual citations: `\textcite{Author2020} found that...`
- Page-specific: `\parencite[see][for explanation]{Author2019}`

#### Referencing Prior Work
- Acknowledge sources appropriately: "as detailed in \textcite{Crawford2016}"
- Build on established literature: "Similar to the features found by \citeauthor{Author}, these hot-spots..."
- Note consensus: "it is widely known that changes in observational techniques..."

### 7. Describing Figures and Results

#### Figure References
- Reference figures parenthetically: "(fig. \ref{label})"
- Describe what figures show precisely: "Cyclone center densities are compared \ref{M2_E5_by_season} for June-August and December-February"
- Use structured figure captions with clear descriptions

#### Presenting Quantitative Results
- Lead with specific numbers: "At 400km, track corroboration was recorded at $P_{M2,E5} = 82.9\%$", "The yield increased to 87.3%"
- Compare values explicitly: "Dataset A records systematically higher values", "Method X performed significantly better than Method Y"
- Discuss trends: "the percentage has increased by roughly 10%", "shows a declining trend over the study period"
- Include error margins where appropriate: "15.3 ± 0.2 mg/L", "p < 0.05"

### 8. Discussion of Methodology

#### Justifying Choices
Always explain methodological decisions:
- "A 400km search distance was selected for the T2C comparison, based on the result shown in..."
- "This threshold was selected so to be roughly comparable to the 60% 'overlap threshold'"
- Explain why alternatives were rejected

#### Acknowledging Alternatives
- Present multiple approaches before selecting one
- Explain trade-offs: "The issue with such methods are that they can fail to match similar data..."
- Note what fell outside scope: "investigating the effects of temporal and spatial resolutions would significantly increase the complexity of this study, and so it fell outside the scope of this paper"

### 9. Mathematical Content

#### Equations
- Number equations consecutively: `\begin{equation}\label{labelname}`
- Reference by number: "equation \ref{labelname}"
- Introduce equations in prose: "is given by equation \ref{labelname}"
- Explain variables immediately after presenting equations

#### Mathematical Language
- Use precise mathematical phrasing:
  - "is proportional to" not "is related to"
  - "tends to infinity" not "gets very large"  
  - "satisfy the condition" not "meet the requirement"

### 10. Common Phrases and Constructions

#### Opening Sentences
- "In this paper, we have compared..."
- "Our findings suggest that..."
- "This has the net result of..."
- "On balance, it seems reasonable to expect..."

#### Introducing Problems
- "This is problematic as..."
- "One major issue with..."
- "A potential criticism that can be leveled at..."
- "This raises important questions regarding..."

#### Presenting Solutions
- "To remedy the shortcomings of..."
- "An elegant solution to this problem can be found in..."
- "To ensure a fair comparison..."

#### Discussing Uncertainty
- "It is not uncommon for..."
- "The exact cause remains unclear"
- "There is a possibility that..."
- "Although the exact mechanism is uncertain..."

#### Conclusions
- "On balance, our findings suggest..."
- "This suggests that, as far as it pertains to..."
- "It should be noted that..."
- "It is hoped that..."

### 11. Tone and Register

#### Maintain Professional Objectivity
- Avoid colloquialisms and informal language
- Never use contractions (don't → do not)
- Maintain measured tone even when critiquing prior work
- Use tentative language when proposing explanations: "might indicate", "could be due to"

#### Express Confidence Appropriately
- Strong claims require strong evidence
- Acknowledge when results are preliminary or require further investigation
- Distinguish between established facts and novel interpretations

### 12. Common Patterns to Avoid

**Don't:**
- Make absolute claims without comprehensive evidence
- Use overly promotional language about your own work
- Ignore limitations or alternative explanations
- Over-simplify complex phenomena
- Use first-person singular ("I") in academic writing
- Include unnecessary hedging that weakens clear findings

### 13. Paragraph Structure

#### Opening Sentences
- State the paragraph's main point clearly
- Link to previous paragraph or section when appropriate

#### Development
- Present evidence in logical order
- Use examples to illustrate abstract points
- Build complexity gradually

#### Closing
- May summarize key takeaway
- Can transition to next topic
- Should feel complete but connected to broader argument

### 14. Special Contexts

#### Abstract Writing
- Lead with broad context
- State specific research question or gap
- Summarize methodology briefly
- Present key findings with numbers
- End with implications or conclusions
- Keep concise (150-250 words typical)

#### Introduction Writing
- Start broad, narrow to specific research question
- Establish importance of topic
- Review relevant literature critically
- Identify gaps or controversies
- State research objectives clearly
- Preview methodology if appropriate

#### Conclusion Writing
- Restate main findings without repetition
- Place findings in broader context
- Acknowledge limitations explicitly
- Compare to prior work
- Suggest future research directions
- End with qualified but clear takeaway

## Example Transformations

### Before (Generic Academic):
"The data shows that there are differences between the two datasets."

### After (Your Style):
"Our findings suggest that while there is generally good agreement, large disagreements were noted in a few highly localized areas, with Dataset B producing extremely strong anomalies in several specific regions."

---

### Before:
"The experiments worked."

### After:
"The experimental approach yielded results consistent with our hypothesis, with yields increasing from 45% to 87% under optimized conditions."

---

### Before:
"We found problems with the old method."

### After:
"The principal aim of this paper is to identify the level of agreement between the two datasets using these analytical techniques. To remedy the shortcomings of pairwise comparison methods, which can fail to match similar data in cases where data fragments or branches, an alternative methodology was developed."

## Application Notes

When writing in this style:
1. Read a paragraph aloud—it should sound authoritative but not arrogant
2. Check that every claim has appropriate qualification or supporting evidence
3. Ensure smooth transitions between ideas
4. Verify all technical terms are used consistently
5. Confirm citations are properly formatted and relevant
6. Review that conclusions match the strength of evidence presented

## Adapting to Different Disciplines

While this style guide is based on atmospheric science writing, the core principles apply across scientific disciplines. Adjust the following based on your field:

### Field-Specific Terminology
- **Natural Sciences**: Maintain technical precision with species names, chemical formulas, geological terms
- **Engineering**: Focus on specifications, performance metrics, optimization parameters
- **Computer Science**: Emphasize algorithmic complexity, computational efficiency, implementation details
- **Social Sciences**: Include appropriate statistical methods, sample descriptions, qualitative analysis frameworks
- **Mathematics**: Prioritize logical progression, theorem-proof structure, precise definitions

### Citation Conventions
- Adapt citation style to field norms (APA, IEEE, Chicago, etc.)
- Maintain the pattern of building on prior work and acknowledging sources
- Use textual vs. parenthetical citations appropriately for your discipline

### Methodology Sections
- **Experimental sciences**: Detail experimental design, controls, measurement techniques
- **Computational work**: Specify algorithms, computational resources, validation approaches
- **Theoretical work**: Present axioms, assumptions, derivations systematically
- **Mixed methods**: Clearly delineate each methodological component

### Units and Measurements
- Follow SI conventions unless field-specific standards dictate otherwise
- Be consistent with precision appropriate to your measurement capabilities
- Include uncertainty/error where relevant to your discipline
