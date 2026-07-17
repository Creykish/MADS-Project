---
description: "Use when writing or editing Report LaTeX sections or Notes markdown files. Enforces Callum Davidson's academic writing style, citation conventions, and technical precision."
name: "Report and Notes Writing Style"
applyTo:
  - "Report/**/*.tex"
  - "Notes/**/*.md"
---
# Writing Style for Report and Notes

## Core Voice and Tone
- Use first-person plural for research actions (we, our).
- Prefer precise, professional, and measured scientific prose.
- Avoid contractions.
- Avoid over-promotional or absolute claims unless evidence is unequivocal.
- Use Oxford commas consistently.
- Prefer parentheses for asides over em-dashes.

## Hedging and Claim Strength
- Calibrate certainty to evidence.
- Prefer wording such as: likely, suggests, appears to, may, might, could, generally, often, approximately.
- Distinguish clearly between established results, assumptions, and interpretation.

## Technical Precision
- Include units with quantitative values.
- Use correct mathematical notation and symbols.
- Use consistent terminology and define acronyms at first use.
- Keep discipline-specific language concise and accurate.

## Structure and Argumentation
- Build arguments methodically:
  1. Context
  2. Gap/problem
  3. Evidence
  4. Interpretation
  5. Limitations
  6. Qualified conclusion
- Use explicit transitions (however, therefore, conversely, similarly, in addition).
- Mix sentence lengths: short statements for key findings, longer sentences for nuance.

## Citations and Evidence (LaTeX)
- For Report LaTeX, use biblatex author-year conventions already present in the project.
- Prefer commands such as:
  - \textcite{key} for narrative citations
  - \parencite{key} for parenthetical citations
- Place multiple citations in logical order and ensure every substantial empirical claim is supported.

## Figures, Tables, and Results
- Lead with quantitative findings where possible.
- Compare magnitudes explicitly and report uncertainty when available.
- Reference figures/tables precisely and explain what they show.

## Method and Limitation Language
- Justify modelling and methodological choices explicitly.
- Name key alternatives and trade-offs.
- Acknowledge scope limits and unresolved uncertainty.

## File-Specific Notes
- In Report LaTeX:
  - Preserve existing sectioning, citation commands, and equation labeling style.
  - Keep notation consistent across sections.
- In Notes markdown:
  - Keep entries concise, evidence-oriented, and synthesis-focused.
  - Highlight assumptions, caveats, and practical implications.

## Avoid
- First-person singular for research claims.
- Informal phrasing and vague qualifiers without context.
- Over-hedging clear empirical statements.
- Unexplained jargon or inconsistent terminology.
- Typical AI phrasing constructions:
  - "This finding underscores a critical insight", "highlights the importance of", "underscores the significance of" → Use direct phrasing: "The key insight here is...", "This demonstrates that...", "Consequently..."
  - "It's not just X, it's Y" → Use simple statement: "X is Y" or "Rather, Y"
  - "and here the kicker:" or "here's the catch:" → Use proper transition: "However,", "The complication is", or simple comma
  - Replacing simple copulas (*is*, *are*) with inflated constructions (*serves as a*, *marks the*, *constitutes a*) → Prefer direct: "This is X" not "This serves as an important X"
- Colons unless necessary; prefer simple commas for most transitions and lists.

## Bonus Tips
- Good use of semicolons is great, as in "Colons unless necessary; prefer simple commas for most transitions and lists." Don't just use semicolons to replace colons though and don't overuse them. 