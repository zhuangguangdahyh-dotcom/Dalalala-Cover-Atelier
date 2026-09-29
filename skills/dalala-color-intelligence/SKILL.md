---
name: dalala-color-intelligence
description: "Build and apply independent, role-based colour systems from 742 Chinese traditional colours and 8,904 traceable harmony sets. Use for covers, posters, advertisements, PPT, resumes, brands, UI, charts, content series, print, palette repair, accessibility, or whenever colour must adapt to current content instead of being fixed to a layout or font style."
---

# Dalala Color Intelligence

Use this Skill after the content job, visual protagonist, and spatial structure are clear. Colour supports that structure; it does not choose the layout.

Read [color-system.md](references/color-system.md), then query the bundled data with `scripts/color_rule.py`. The 742 names and HEX values are canonical source candidates. The 8,904 harmony sets narrow the search; they do not make every suggested combination production-ready.

## Required workflow

1. Translate mood words into temperature, lightness, saturation, contrast, cultural signal, and risk.
2. Sample or identify important colours already present in the subject, product, brand, or environment.
3. Choose one anchor from the source data or map an outside HEX to its nearest traditional colour.
4. Choose a relationship strategy: restrained, identity, contrast, warm-cool, light-dark, series, data, UI, or print.
5. Assign roles before presenting colours: canvas, primary text, secondary text, subject support, accent, border or data states as needed.
6. Set area ratios for the actual surface. One colour must dominate; accents remain limited.
7. Calculate contrast for text and functional marks. Add labels, shape, stroke, pattern, or direct annotation when colour alone carries meaning.
8. Review the palette on the real design. Repair role competition, excessive accents, muddy lightness, and conflict with source imagery.

## Rules

- Never bind exact colours to a layout, template, composition, or font style.
- Reference colours teach role relations, area, temperature, contrast, and hierarchy. Re-select exact colours for each project.
- Do not output unordered swatches. Every colour needs a role, area, reason, and forbidden use.
- Use one strong recommendation by default. Provide alternatives only when they reveal a meaningful tradeoff.
- Keep traditional names as source metadata. Functional UI and design tokens use semantic names.
- For a content series, keep stable neutrals and identity roles while rotating controlled accents.
- For charts, data meaning and distinguishability outrank harmony.
- For print, provide HEX as a reference and require physical or printer-profile proofing before production.

## Output contract

Return the palette thesis, role mapping, Chinese colour name, HEX, area ratio, source relationship, surface placement, contrast result, risks, and forbidden combinations. When applying to an artifact, verify the rendered result rather than judging the swatches alone.
