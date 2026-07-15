---
description: "Rewrite or draft content for Report LaTeX and Notes markdown using Callum Davidson's academic style."
name: "Report and Notes Style Draft"
argument-hint: "Paste text and state whether it is for Report or Notes"
agent: "ask"
---
Rewrite or draft the provided content for either:
- Report LaTeX sections in Report/**/*.tex, or
- Research notes in Notes/**/*.md.

Requirements:
- Use first-person plural voice for research actions.
- Maintain cautious, evidence-calibrated claims.
- Preserve technical precision (units, notation, terminology consistency).
- Use clear logical flow: context, evidence, interpretation, limitations, and qualified takeaway.
- For LaTeX output, keep biblatex-compatible citation commands (for example \textcite{} and \parencite{}).
- Prefer concise, high-information prose without informal language.

Input to provide:
- Target file type (Report LaTeX or Notes markdown)
- Original text
- Optional constraints (length, section purpose, required citations)

Output format:
- Return only the revised text, ready to paste into the target file.
