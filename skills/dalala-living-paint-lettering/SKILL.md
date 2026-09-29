---
name: dalala-living-paint-lettering
description: Generate Dalala's filled, childlike dry-paint Chinese cover lettering with independently redrawn character occurrences, exact standard glyph structure, and maximum human vitality. Use for cover titles that ask for 松弛油漆体、真笔触、小孩手写感、自然缺墨 or stronger 生命力. Do not use for body copy, ordinary fixed-font typesetting, or the hollow-outline Dalala style.
---

# Dalala 生命油漆字

Apply the project-local generative lettering style. Treat the title as phrase-specific artwork rather than typeset text.

## Workflow

1. Read `../../font-style-rules/registry.json` and resolve `dalala-living-paint`.
2. Read the resolved `style.json`, `STYLE_RULES.md`, prompt template, approved reference and `VITALITY_QA.md`.
3. Copy the title exactly and index every character occurrence. Generate a `plan` with `../../font-style-rules/tools/font_style.py`; repeated characters require different instances.
4. Establish the standard Chinese skeleton of every unique character before stylisation. Treat any incorrect component or connection as a hard failure.
5. Generate 4–8 character instances at a time, or separately when a glyph is complex. Use the approved reference as the main style reference and the energy reference only for gesture strength.
6. Inspect each glyph at full size. Regenerate only failed glyphs. Never repair a wrong glyph by hiding it in layout or texture.
7. Extract transparent glyph assets, compose the phrase according to the occurrence plan, and preserve the result as a separate transparent title layer.
8. Run the hard gates and 100-point check in `VITALITY_QA.md`. Check again at 360 px width.
9. Save `plan.json`, occurrence glyphs, `title-layer.png`, and `qa.json` under the cover ID. Reuse the approved title layer on later exports unless re-lettering is requested.

Use `alive-max` by default. Never silently reduce vitality or fall back to the archived TTF.

Read `references/runtime-contract.md` when wiring this skill into the workbench.
