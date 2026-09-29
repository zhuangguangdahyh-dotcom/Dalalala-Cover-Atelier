---
name: dalala-visual-foundation
description: "Apply Dalala's distilled visual judgment from 350 source-validated design references when creating or revising covers, posters, advertisements, images, resumes, PPT slides, and presentation decks. Use alongside the relevant production Skill whenever composition, source-image transformation, image-text fit, typography, hierarchy, whitespace, information density, or visual QA affects the result."
---

# Dalala Visual Foundation

This is the persistent design-judgment layer shared by all visual production. Apply it to the finished work; do not turn the user's deliverable into a design-theory page.

The 350 references are source-validated design assets. Their visible compositions, hierarchy, typography, image treatment, colour roles, texture, and decorative logic are evidence. A reference may be trusted as a design precedent while its local machine-readable distillation is still provisional.

## Runtime sequence

1. Read [universal-visual-grammar.md](references/universal-visual-grammar.md) and identify the content job, visual protagonist, reading path, and dominant contrast.
2. Read [template-anatomy.md](references/template-anatomy.md). Select a reference family by content anatomy, not by surface resemblance.
3. If source imagery is supplied, read [material-transformation.md](references/material-transformation.md). Separate identity or fact anchors from composition freedoms, then choose T0–T3.
4. Read [image-text-fit.md](references/image-text-fit.md), [canvas-composition-engine.md](references/canvas-composition-engine.md), and [typography-engine.md](references/typography-engine.md) as needed.
5. Read [medium-transfer.md](references/medium-transfer.md) for PPT, resumes, posters, advertisements, long graphics, or a new aspect ratio.
6. When colour affects the result, use `$dalala-color-intelligence` after the spatial structure is set. Rebuild colour roles for the current content and imagery.
7. For an exact numbered cover reference, use `$dalala-cover-composition-intelligence`, inspect the original thumbnail, and lock one layout contract.
8. Apply [runtime-qa.md](references/runtime-qa.md) to the rendered artifact. Revise the artifact when it fails.

## Non-negotiable laws

- Meaning and content quantity choose structure.
- One frame has one dominant visual centre, one primary reading path, and one dominant contrast channel.
- A template is a relationship among content roles, spatial masses, scale, alignment, depth, and reading order. It is not a coordinate preset.
- A source image is material. Preserve identity and factual anchors; crop, enlarge, isolate, repeat, mask, rotate, extend, obscure, or rebuild the rest when the concept needs it.
- Text and image must follow, counterweight, embed, frame, reveal, interrupt, or deliberately obstruct each other. Simple overlay does not establish a relationship.
- Typography is geometry and rhythm. Break lines by meaning, balance, and cadence.
- Whitespace must focus, breathe, direct, delay, separate, frame, or create suspense.
- Decoration must strengthen a reading turn, boundary, group, motion, emotion, or metaphor. Remove it if the structure survives unchanged.
- Colour is a role system chosen for the current content and imagery. Never bind a template or style family to the palette shown in its reference.
- A new aspect ratio is a new composition.
- User aesthetic judgment is final. Diagnose the failed visual relationship and rebuild it.

## Completion

Check thumbnail, normal, and close views. The result must keep its hierarchy with decoration hidden, express the selected grammar with its name hidden, and weaken materially if the chosen subject placement, crop, whitespace, type mass, or primary contrast is removed. If an unrelated title and image can replace the content without recomposition, the work is still generic.
